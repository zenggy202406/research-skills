#!/usr/bin/env python3
"""
KB Dream — Memory Consolidation for the Research Knowledge Base (v2)

Performs sleep-like memory consolidation on Layer 2 with cumulative vitality
scoring, incremental scanning (only changes since last dream), and mild
Layer 1 reshaping proposals.

Usage:
    python kb_dream.py --kb-root <path> --action <action> [options]

Actions:
    analyze       Incremental scan since last dream; apply vitality deltas
    consolidate   Auto-apply: tag normalization, hint population
    prune         Move nodes below vitality cutoff to cold storage
    report        Generate dream-report-YYYY-MM-DD.md
    restore       Restore a node from cold storage
    full          Run analyze -> consolidate -> prune -> report in sequence
    init-node     Initialize vitality for a single node (used when adding to L2)

Vitality model (cumulative):
    New node enters with baseline 1.0 + connectedness bonus (degree/max_degree * 0.5).
    Each dream cycle applies a delta:
      +0.15 per new project reference since last dream
      +0.05 per new relationship (degree increase) since last dream
      -0.2 decay if no new activity
    Pruning cutoff: vitality < 0.25 (configurable via --threshold).
"""

import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print(json.dumps({"status": "error",
                       "message": "PyYAML not installed. Run: pip install pyyaml --break-system-packages"}))
    sys.exit(1)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
BASELINE_VITALITY = 1.0
CONNECTEDNESS_BONUS_MAX = 0.5
PROJECT_USE_DELTA = 0.15
CONNECTION_DELTA = 0.05
DECAY_DELTA = -0.20
DEFAULT_PRUNE_THRESHOLD = 0.25

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_yaml(filepath):
    p = Path(filepath)
    if not p.exists():
        return None
    with open(p, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_yaml(filepath, data):
    p = Path(filepath)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True,
                  sort_keys=False, width=120)


def load_graph(kb_root):
    data = load_yaml(Path(kb_root) / "layer2-field" / "graph.yaml")
    if data is None or "nodes" not in data:
        return {"nodes": []}
    if data["nodes"] is None:
        data["nodes"] = []
    return data


def save_graph(kb_root, graph):
    save_yaml(Path(kb_root) / "layer2-field" / "graph.yaml", graph)


def get_all_projects(kb_root):
    projects = []
    for status_dir in ["active", "archived"]:
        pdir = Path(kb_root) / "projects" / status_dir
        if not pdir.exists():
            continue
        for proj in sorted(pdir.iterdir()):
            if proj.is_dir():
                projects.append((proj.name, status_dir, str(proj)))
    return projects


def extract_list(data, keys=None):
    if data is None:
        return []
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and keys:
        for k in keys:
            if k in data and isinstance(data[k], list):
                return data[k]
    return []


def load_dream_log(kb_root):
    data = load_yaml(Path(kb_root) / "system" / "dream-log.yaml")
    if data is None:
        data = {"last_dream": None, "dreams": []}
    if "dreams" not in data:
        data["dreams"] = []
    return data


def save_dream_log(kb_root, log):
    save_yaml(Path(kb_root) / "system" / "dream-log.yaml", log)


def load_vitality_store(kb_root):
    data = load_yaml(Path(kb_root) / "system" / "usage-metrics.yaml")
    if data is None:
        data = {"node_vitality": {}}
    if "node_vitality" not in data:
        data["node_vitality"] = {}
    return data


def save_vitality_store(kb_root, store):
    save_yaml(Path(kb_root) / "system" / "usage-metrics.yaml", store)


def file_modified_since(filepath, since_dt):
    p = Path(filepath)
    if not p.exists():
        return False
    if since_dt is None:
        return True
    mtime = datetime.fromtimestamp(p.stat().st_mtime)
    return mtime > since_dt


def compute_degrees(graph):
    degrees = defaultdict(int)
    for node in graph["nodes"]:
        nid = node["id"]
        out_deg = len(node.get("relationships") or [])
        degrees[nid] += out_deg
        for rel in (node.get("relationships") or []):
            degrees[rel.get("target", "")] += 1
    return dict(degrees)


def scan_project_refs(kb_root, projects, since_dt=None):
    graph = load_graph(kb_root)
    node_ids = {n["id"] for n in graph["nodes"]}
    refs = defaultdict(set)

    for proj_name, proj_status, proj_path in projects:
        proj_path = Path(proj_path)
        files_to_scan = [
            (proj_path / "concepts.yaml", "concepts"),
            (proj_path / "method-instantiations.yaml", "methods"),
            (proj_path / "arguments.yaml", "arguments"),
            (proj_path / "claims.yaml", "claims"),
            (proj_path / "paper-network.yaml", "network"),
        ]

        for fpath, ftype in files_to_scan:
            if not fpath.exists():
                continue
            if since_dt is not None and not file_modified_since(fpath, since_dt):
                continue

            if ftype == "concepts":
                for c in extract_list(load_yaml(fpath), ["concepts"]):
                    if isinstance(c, dict) and c.get("base_concept_id") in node_ids:
                        refs[c["base_concept_id"]].add(proj_name)
            elif ftype == "methods":
                for m in extract_list(load_yaml(fpath), ["method_instantiations"]):
                    if isinstance(m, dict) and m.get("base_method_id") in node_ids:
                        refs[m["base_method_id"]].add(proj_name)
            elif ftype == "arguments":
                for a in extract_list(load_yaml(fpath), ["arguments"]):
                    if not isinstance(a, dict):
                        continue
                    for tg in (a.get("theoretical_grounding") or []):
                        if isinstance(tg, dict) and tg.get("concept_id") in node_ids:
                            refs[tg["concept_id"]].add(proj_name)
            elif ftype == "claims":
                for cl in extract_list(load_yaml(fpath), ["claims"]):
                    if isinstance(cl, dict) and cl.get("method_ref") in node_ids:
                        refs[cl["method_ref"]].add(proj_name)
            elif ftype == "network":
                pnet = load_yaml(fpath)
                if pnet and isinstance(pnet, dict):
                    for edge in (pnet.get("edges") or []):
                        if not isinstance(edge, dict):
                            continue
                        for ref_id in (edge.get("layer2_refs") or []):
                            if ref_id in node_ids:
                                refs[ref_id].add(proj_name)

    return refs


# ---------------------------------------------------------------------------
# Vitality initialization
# ---------------------------------------------------------------------------

def initialize_node_vitality(node_id, degree, max_degree, today_str):
    conn_bonus = round((degree / max_degree) * CONNECTEDNESS_BONUS_MAX, 3) if max_degree > 0 else 0
    vitality = round(BASELINE_VITALITY + conn_bonus, 3)
    return {
        "vitality": vitality,
        "last_degree": degree,
        "last_project_refs": [],
        "history": [
            {"date": today_str, "event": "initialized",
             "delta": BASELINE_VITALITY, "vitality_after": BASELINE_VITALITY,
             "reason": "baseline for new node"},
            {"date": today_str, "event": "connectedness_bonus",
             "delta": conn_bonus, "vitality_after": vitality,
             "reason": f"initial degree {degree}/{max_degree}"},
        ],
    }


# ---------------------------------------------------------------------------
# Action: analyze
# ---------------------------------------------------------------------------

def analyze(kb_root):
    graph = load_graph(kb_root)
    projects = get_all_projects(kb_root)
    dream_log = load_dream_log(kb_root)
    store = load_vitality_store(kb_root)
    today_str = str(date.today())

    last_dream_str = dream_log.get("last_dream")
    since_dt = None
    if last_dream_str:
        try:
            since_dt = datetime.fromisoformat(last_dream_str)
        except (ValueError, TypeError):
            since_dt = None

    is_first_dream = since_dt is None
    degrees = compute_degrees(graph)
    max_degree = max(degrees.values()) if degrees else 1

    current_refs = scan_project_refs(kb_root, projects, since_dt=None)
    new_refs = scan_project_refs(kb_root, projects, since_dt=since_dt) if not is_first_dream else current_refs

    initialized = []
    deltas_applied = []
    node_vitality = store.get("node_vitality", {})

    for node in graph["nodes"]:
        nid = node["id"]
        degree = degrees.get(nid, 0)
        all_project_refs = sorted(current_refs.get(nid, set()))

        if nid not in node_vitality:
            record = initialize_node_vitality(nid, degree, max_degree, today_str)
            record["last_project_refs"] = all_project_refs
            record["last_degree"] = degree
            node_vitality[nid] = record
            initialized.append({"id": nid, "name": node.get("name", ""),
                                 "vitality": record["vitality"]})
        else:
            record = node_vitality[nid]
            prev_refs = set(record.get("last_project_refs", []))
            prev_degree = record.get("last_degree", 0)

            new_project_refs = set(new_refs.get(nid, set())) - prev_refs
            degree_increase = max(0, degree - prev_degree)

            delta = 0.0
            reasons = []

            if new_project_refs:
                proj_delta = len(new_project_refs) * PROJECT_USE_DELTA
                delta += proj_delta
                reasons.append(f"+{proj_delta:.2f} from {len(new_project_refs)} new project ref(s)")

            if degree_increase > 0:
                conn_delta = degree_increase * CONNECTION_DELTA
                delta += conn_delta
                reasons.append(f"+{conn_delta:.2f} from {degree_increase} new connection(s)")

            if not new_project_refs and degree_increase == 0:
                delta = DECAY_DELTA
                reasons.append(f"{DECAY_DELTA} decay (no new activity)")

            delta = round(delta, 3)
            old_vitality = record["vitality"]
            new_vitality = round(max(0.0, old_vitality + delta), 3)

            record["vitality"] = new_vitality
            record["last_degree"] = degree
            record["last_project_refs"] = all_project_refs
            record["history"].append({
                "date": today_str, "event": "dream_cycle",
                "delta": delta, "vitality_after": new_vitality,
                "reason": "; ".join(reasons),
            })

            if delta != 0:
                deltas_applied.append({
                    "id": nid, "name": node.get("name", ""),
                    "old_vitality": old_vitality, "delta": delta,
                    "new_vitality": new_vitality,
                })

    store["node_vitality"] = node_vitality
    store["generated"] = datetime.now().isoformat()
    store["total_nodes"] = len(graph["nodes"])
    store["total_projects"] = len(projects)
    store["active_projects"] = len([p for p in projects if p[1] == "active"])
    store["archived_projects"] = len([p for p in projects if p[1] == "archived"])
    save_vitality_store(kb_root, store)

    active_ids = {n["id"] for n in graph["nodes"]}
    active_vitalities = {nid: v["vitality"] for nid, v in node_vitality.items() if nid in active_ids}

    high = len([v for v in active_vitalities.values() if v >= 1.0])
    medium = len([v for v in active_vitalities.values() if DEFAULT_PRUNE_THRESHOLD <= v < 1.0])
    low = len([v for v in active_vitalities.values() if v < DEFAULT_PRUNE_THRESHOLD])

    layer1_data = collect_layer1_data(kb_root, projects, node_vitality, active_ids, graph)

    return {
        "status": "success",
        "is_first_dream": is_first_dream,
        "total_nodes": len(graph["nodes"]),
        "total_projects": len(projects),
        "nodes_initialized": len(initialized),
        "deltas_applied": len(deltas_applied),
        "vitality_distribution": {
            "high (>=1.0)": high,
            "medium (0.3-1.0)": medium,
            "low (<0.3)": low,
        },
        "initialized": initialized[:20],
        "delta_details": sorted(deltas_applied, key=lambda x: x["delta"])[:20],
        "layer1_proposals": layer1_data,
        "metrics_saved_to": "system/usage-metrics.yaml",
    }


# ---------------------------------------------------------------------------
# Layer 1 mild reshaping
# ---------------------------------------------------------------------------

def collect_layer1_data(kb_root, projects, node_vitality, active_ids, graph):
    proposals = []

    # 1. Usage concentration
    concept_vitalities = []
    for node in graph["nodes"]:
        if node.get("type") == "concept" and node["id"] in node_vitality:
            nv = node_vitality[node["id"]]
            concept_vitalities.append({
                "id": node["id"], "name": node.get("name", ""),
                "vitality": nv["vitality"],
                "project_count": len(nv.get("last_project_refs", [])),
                "projects": nv.get("last_project_refs", []),
            })
    top_concepts = sorted(concept_vitalities, key=lambda x: -x["vitality"])[:5]
    if top_concepts and top_concepts[0]["project_count"] >= 2:
        proposals.append({
            "type": "usage_concentration",
            "description": "Concepts with highest vitality across multiple projects -- "
                           "consider whether these reflect a strengthening research focus "
                           "that should be noted in the narrative profile.",
            "data": top_concepts,
        })

    # 2. Override pattern detection
    override_counts = defaultdict(lambda: {"count": 0, "projects": [], "justifications": []})
    for proj_name, proj_status, proj_path in projects:
        olog = load_yaml(Path(proj_path) / "override-log.yaml")
        if not olog:
            continue
        entries = olog if isinstance(olog, list) else olog.get("overrides", [])
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            rule_key = entry.get("rule_category", entry.get("rule_summary", "unknown"))
            override_counts[rule_key]["count"] += 1
            override_counts[rule_key]["projects"].append(proj_name)
            if entry.get("justification"):
                override_counts[rule_key]["justifications"].append(entry["justification"])

    repeated_overrides = [
        {"rule": k, "count": v["count"], "projects": sorted(set(v["projects"])),
         "sample_justifications": v["justifications"][:3]}
        for k, v in override_counts.items() if v["count"] >= 2
    ]
    if repeated_overrides:
        proposals.append({
            "type": "override_pattern",
            "description": "Layer 1 rules overridden multiple times across projects. "
                           "Consider softening or revising to match evolving practice.",
            "data": sorted(repeated_overrides, key=lambda x: -x["count"]),
        })

    # 3. Dormancy-based interest pruning
    profile_path = Path(kb_root) / "layer1-researcher" / "narrative-profile.md"
    if profile_path.exists():
        try:
            profile_text = profile_path.read_text(encoding="utf-8").lower()
        except Exception:
            profile_text = ""

        dormant_in_profile = []
        for node in graph["nodes"]:
            if node.get("type") != "concept":
                continue
            nid = node["id"]
            name = node.get("name", "").lower()
            if nid in node_vitality and name and len(name) > 3:
                vit = node_vitality[nid]["vitality"]
                if vit < DEFAULT_PRUNE_THRESHOLD and name in profile_text:
                    dormant_in_profile.append({
                        "id": nid, "name": node.get("name", ""), "vitality": vit,
                    })

        if dormant_in_profile:
            proposals.append({
                "type": "dormant_profile_concepts",
                "description": "Concepts in your narrative profile that have become dormant. "
                               "Consider whether your interests have shifted.",
                "data": dormant_in_profile,
            })

    return proposals


# ---------------------------------------------------------------------------
# Action: init-node
# ---------------------------------------------------------------------------

def init_node(kb_root, node_id):
    graph = load_graph(kb_root)
    degrees = compute_degrees(graph)
    max_degree = max(degrees.values()) if degrees else 1
    degree = degrees.get(node_id, 0)

    store = load_vitality_store(kb_root)
    today_str = str(date.today())

    if node_id in store.get("node_vitality", {}):
        return {"status": "error", "message": f"Node {node_id} already has a vitality record"}

    record = initialize_node_vitality(node_id, degree, max_degree, today_str)
    store.setdefault("node_vitality", {})[node_id] = record
    save_vitality_store(kb_root, store)

    return {"status": "success", "node_id": node_id, "vitality": record["vitality"],
            "degree": degree, "max_degree": max_degree}


# ---------------------------------------------------------------------------
# Action: consolidate
# ---------------------------------------------------------------------------

def consolidate(kb_root):
    graph = load_graph(kb_root)
    changes = {"tags_normalized": 0, "tags_deduped": 0, "hints_added": 0, "details": []}
    id_to_name = {n["id"]: n.get("name", "") for n in graph["nodes"]}

    for node in graph["nodes"]:
        nid = node["id"]
        if "tags" in node and isinstance(node["tags"], list):
            original = list(node["tags"])
            seen = set()
            normalized = []
            for tag in node["tags"]:
                t = str(tag).strip().lower()
                if t and t not in seen:
                    seen.add(t)
                    normalized.append(t)
            if normalized != original:
                if len(normalized) < len(original):
                    changes["tags_deduped"] += 1
                changes["tags_normalized"] += 1
                node["tags"] = normalized

        for rel in (node.get("relationships") or []):
            target_id = rel.get("target")
            if target_id and not rel.get("target_hint") and target_id in id_to_name:
                rel["target_hint"] = id_to_name[target_id]
                changes["hints_added"] += 1

    # Near-duplicate detection
    duplicates = []
    names = [(n["id"], n.get("name", "").lower().strip(), n.get("type", "")) for n in graph["nodes"]]
    for i, (id1, name1, type1) in enumerate(names):
        if not name1:
            continue
        for j in range(i + 1, len(names)):
            id2, name2, type2 = names[j]
            if not name2 or type1 != type2:
                continue
            if name1 == name2:
                duplicates.append({"ids": [id1, id2], "names": [name1, name2], "reason": "identical"})
            elif (name1 in name2 or name2 in name1) and min(len(name1), len(name2)) > 3:
                duplicates.append({"ids": [id1, id2], "names": [name1, name2], "reason": "substring"})
            else:
                w1, w2 = set(name1.split()), set(name2.split())
                if len(w1) >= 2 and len(w2) >= 2:
                    ov = len(w1 & w2)
                    tot = len(w1 | w2)
                    if tot > 0 and ov / tot >= 0.7:
                        duplicates.append({"ids": [id1, id2], "names": [name1, name2],
                                           "reason": f"overlap {ov}/{tot}"})

    verbose = [{"id": n["id"], "name": n.get("name", ""), "word_count": len(n.get("definition", "").split())}
               for n in graph["nodes"] if isinstance(n.get("definition", ""), str) and len(n.get("definition", "").split()) > 80]

    # Co-occurrence
    store = load_vitality_store(kb_root)
    nv = store.get("node_vitality", {})
    cooccurrence = []
    active_nids = [nid for nid in nv if any(n["id"] == nid for n in graph["nodes"])]
    for i, nid1 in enumerate(active_nids):
        p1 = set(nv[nid1].get("last_project_refs", []))
        if not p1:
            continue
        for j in range(i + 1, len(active_nids)):
            nid2 = active_nids[j]
            p2 = set(nv[nid2].get("last_project_refs", []))
            shared = p1 & p2
            if len(shared) >= 2:
                linked = False
                for nd in graph["nodes"]:
                    if nd["id"] in (nid1, nid2):
                        for r in (nd.get("relationships") or []):
                            if r.get("target") in (nid1, nid2) and r.get("target") != nd["id"]:
                                linked = True
                                break
                    if linked:
                        break
                if not linked:
                    cooccurrence.append({"ids": [nid1, nid2], "shared_projects": sorted(shared)})

    if changes["tags_normalized"] > 0 or changes["hints_added"] > 0:
        save_graph(kb_root, graph)

    return {
        "status": "success",
        "auto_applied": {"tags_normalized": changes["tags_normalized"],
                         "tags_deduped": changes["tags_deduped"],
                         "hints_added": changes["hints_added"]},
        "proposals": {"near_duplicates": duplicates[:20],
                      "verbose_definitions": verbose[:20],
                      "missing_relationships": cooccurrence[:20]},
    }


# ---------------------------------------------------------------------------
# Action: prune
# ---------------------------------------------------------------------------

def prune(kb_root, threshold=DEFAULT_PRUNE_THRESHOLD, dry_run=False):
    graph = load_graph(kb_root)
    store = load_vitality_store(kb_root)
    nv = store.get("node_vitality", {})

    if not nv:
        return {"status": "error", "message": "Run 'analyze' first"}

    degrees = compute_degrees(graph)
    dormant_ids = set()
    for node in graph["nodes"]:
        nid = node["id"]
        if nid in nv and nv[nid]["vitality"] < threshold and degrees.get(nid, 0) <= 1:
            dormant_ids.add(nid)

    if not dormant_ids:
        return {"status": "success", "message": "No nodes below threshold", "pruned_count": 0}

    if dry_run:
        return {"status": "success", "dry_run": True, "dormant_count": len(dormant_ids),
                "dormant_nodes": [{"id": nid, "vitality": nv[nid]["vitality"],
                                   "degree": degrees.get(nid, 0)} for nid in dormant_ids]}

    cold_path = Path(kb_root) / "system" / "dormant-nodes.yaml"
    cold = load_yaml(cold_path) or {"dormant_nodes": [], "move_log": []}
    cold.setdefault("dormant_nodes", [])
    cold.setdefault("move_log", [])

    pruned = []
    remaining = []
    for node in graph["nodes"]:
        if node["id"] in dormant_ids:
            node["_dormant_date"] = str(date.today())
            node["_vitality_at_prune"] = nv[node["id"]]["vitality"]
            node["_vitality_history"] = nv[node["id"]].get("history", [])
            cold["dormant_nodes"].append(node)
            cold["move_log"].append({"id": node["id"], "name": node.get("name", ""),
                                     "date": str(date.today()), "vitality": nv[node["id"]]["vitality"],
                                     "action": "pruned"})
            pruned.append({"id": node["id"], "name": node.get("name", ""),
                           "vitality": nv[node["id"]]["vitality"]})
            del nv[node["id"]]
        else:
            remaining.append(node)

    orphaned = 0
    for node in remaining:
        if node.get("relationships"):
            before = len(node["relationships"])
            node["relationships"] = [r for r in node["relationships"] if r.get("target") not in dormant_ids]
            orphaned += before - len(node["relationships"])

    graph["nodes"] = remaining
    save_graph(kb_root, graph)
    save_yaml(cold_path, cold)
    save_vitality_store(kb_root, store)

    return {"status": "success", "pruned_count": len(pruned), "pruned_nodes": pruned,
            "orphaned_relationships_removed": orphaned}


# ---------------------------------------------------------------------------
# Action: restore
# ---------------------------------------------------------------------------

def restore(kb_root, node_id):
    cold_path = Path(kb_root) / "system" / "dormant-nodes.yaml"
    cold = load_yaml(cold_path)
    if cold is None or not cold.get("dormant_nodes"):
        return {"status": "error", "message": "No dormant nodes in cold storage"}

    target = None
    remaining = []
    for node in cold["dormant_nodes"]:
        if node.get("id") == node_id:
            target = node
        else:
            remaining.append(node)

    if target is None:
        avail = [{"id": n["id"], "name": n.get("name", "")} for n in cold["dormant_nodes"]]
        return {"status": "error", "message": f"Node {node_id} not found", "available": avail}

    old_history = target.pop("_vitality_history", [])
    target.pop("_dormant_date", None)
    target.pop("_vitality_at_prune", None)

    graph = load_graph(kb_root)
    graph["nodes"].append(target)
    save_graph(kb_root, graph)

    degrees = compute_degrees(graph)
    max_degree = max(degrees.values()) if degrees else 1
    degree = degrees.get(node_id, 0)
    today_str = str(date.today())

    store = load_vitality_store(kb_root)
    record = initialize_node_vitality(node_id, degree, max_degree, today_str)
    record["history"] = old_history + [
        {"date": today_str, "event": "restored_from_cold_storage",
         "delta": 0, "vitality_after": record["vitality"],
         "reason": "re-initialized after manual restore"}
    ] + record["history"]
    store.setdefault("node_vitality", {})[node_id] = record
    save_vitality_store(kb_root, store)

    cold["dormant_nodes"] = remaining
    cold["move_log"].append({"id": node_id, "name": target.get("name", ""),
                             "date": today_str, "action": "restored"})
    save_yaml(cold_path, cold)

    return {"status": "success", "restored": {"id": node_id, "name": target.get("name", ""),
                                               "new_vitality": record["vitality"]}}


# ---------------------------------------------------------------------------
# Action: report
# ---------------------------------------------------------------------------

def generate_report(kb_root, analyze_result=None):
    store = load_vitality_store(kb_root)
    nv = store.get("node_vitality", {})
    if not nv:
        return {"status": "error", "message": "Run 'analyze' first"}

    graph = load_graph(kb_root)
    cold = load_yaml(Path(kb_root) / "system" / "dormant-nodes.yaml")
    dream_log = load_dream_log(kb_root)
    active_ids = {n["id"] for n in graph["nodes"]}
    today = str(date.today())

    L = []  # report lines
    L.append(f"# KB Dream Report -- {today}")
    L.append("")
    L.append("## 1. Summary")
    L.append("")
    L.append(f"- **Dream #**: {len(dream_log.get('dreams', [])) + 1}")
    prev = dream_log.get("last_dream")
    L.append(f"- **Previous dream**: {prev if prev else 'first dream'}")
    L.append(f"- **Active nodes**: {len(graph['nodes'])}")
    L.append(f"- **Total projects**: {store.get('total_projects', '?')}")
    L.append("")

    active_vit = {nid: nv[nid]["vitality"] for nid in active_ids if nid in nv}
    high = [(nid, v) for nid, v in active_vit.items() if v >= 1.0]
    medium = [(nid, v) for nid, v in active_vit.items() if DEFAULT_PRUNE_THRESHOLD <= v < 1.0]
    low = [(nid, v) for nid, v in active_vit.items() if v < DEFAULT_PRUNE_THRESHOLD]

    L.append("## 2. Vitality Distribution")
    L.append("")
    L.append("| Band | Count |")
    L.append("|------|-------|")
    L.append(f"| High (>=1.0) | {len(high)} |")
    L.append(f"| Medium (0.3-1.0) | {len(medium)} |")
    L.append(f"| Low (<0.3) | {len(low)} |")
    L.append("")

    sorted_vit = sorted(active_vit.items(), key=lambda x: -x[1])
    L.append("### Top 10 Nodes by Vitality")
    L.append("")
    L.append("| ID | Name | Type | Vitality | Projects |")
    L.append("|---|---|---|---|---|")
    for nid, vit in sorted_vit[:10]:
        nd = next((n for n in graph["nodes"] if n["id"] == nid), {})
        pc = len(nv[nid].get("last_project_refs", []))
        L.append(f"| {nid} | {nd.get('name', '')} | {nd.get('type', '')} | {vit:.3f} | {pc} |")
    L.append("")

    if analyze_result and analyze_result.get("delta_details"):
        L.append("### Vitality Changes This Cycle")
        L.append("")
        L.append("| ID | Name | Old | Delta | New |")
        L.append("|---|---|---|---|---|")
        for d in analyze_result["delta_details"]:
            L.append(f"| {d['id']} | {d['name']} | {d['old_vitality']:.3f} | "
                     f"{d['delta']:+.3f} | {d['new_vitality']:.3f} |")
        L.append("")

    if low:
        L.append("### Low Vitality Nodes")
        L.append("")
        L.append("| ID | Name | Vitality |")
        L.append("|---|---|---|")
        for nid, vit in sorted(low, key=lambda x: x[1]):
            nd = next((n for n in graph["nodes"] if n["id"] == nid), {})
            L.append(f"| {nid} | {nd.get('name', '')} | {vit:.3f} |")
        L.append("")

    if cold and cold.get("dormant_nodes"):
        L.append("### Cold Storage")
        L.append("")
        L.append(f"**{len(cold['dormant_nodes'])}** nodes in cold storage.")
        L.append("")
        for n in cold["dormant_nodes"]:
            L.append(f"- **{n.get('id')}** {n.get('name', '')} "
                     f"(moved: {n.get('_dormant_date', '?')}, vit: {n.get('_vitality_at_prune', '?')})")
        L.append("")

    if analyze_result and analyze_result.get("layer1_proposals"):
        L.append("## 3. Layer 1 Reshaping Proposals")
        L.append("")
        for prop in analyze_result["layer1_proposals"]:
            pt = prop["type"]
            if pt == "usage_concentration":
                L.append("### Usage Concentration Shift")
                L.append("")
                L.append(prop["description"])
                L.append("")
                for c in prop["data"]:
                    L.append(f"- **{c['name']}** (vitality: {c['vitality']:.3f}, "
                             f"projects: {', '.join(c.get('projects', []))})")
                L.append("")
            elif pt == "override_pattern":
                L.append("### Repeated Rule Overrides")
                L.append("")
                L.append(prop["description"])
                L.append("")
                for o in prop["data"]:
                    L.append(f"- **{o['rule']}** -- overridden {o['count']} times "
                             f"across {', '.join(o['projects'])}")
                    for jj in o.get("sample_justifications", []):
                        L.append(f"  - Justification: {jj}")
                L.append("")
            elif pt == "dormant_profile_concepts":
                L.append("### Dormant Profile Concepts")
                L.append("")
                L.append(prop["description"])
                L.append("")
                for c in prop["data"]:
                    L.append(f"- **{c['name']}** (vitality: {c['vitality']:.3f})")
                L.append("")

    L.append("## 4. Graph Health")
    L.append("")
    degs = compute_degrees(graph)
    total_rels = sum(len(n.get("relationships") or []) for n in graph["nodes"])
    avg_d = sum(degs.values()) / len(degs) if degs else 0
    iso = len([d for d in degs.values() if d == 0])
    L.append(f"- **Active nodes**: {len(graph['nodes'])}")
    L.append(f"- **Total relationships**: {total_rels}")
    L.append(f"- **Average degree**: {avg_d:.1f}")
    L.append(f"- **Isolated nodes**: {iso}")
    L.append("")

    gp = Path(kb_root) / "layer2-field" / "graph.yaml"
    sp = Path(kb_root) / "layer2-field" / "field-summary.md"
    gs = gp.stat().st_size if gp.exists() else 0
    ss = sp.stat().st_size if sp.exists() else 0
    L.append(f"- **graph.yaml**: {gs:,} bytes (~{gs // 4:,} tokens)")
    L.append(f"- **field-summary.md**: {ss:,} bytes (~{ss // 4:,} tokens)")
    L.append("")
    L.append("---")
    L.append(f"*Generated by kb-dream v2 on {today}*")

    report_text = "\n".join(L)
    report_path = Path(kb_root) / "system" / f"dream-report-{today}.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_text)

    return {"status": "success", "report_relative": f"system/dream-report-{today}.md"}


# ---------------------------------------------------------------------------
# Action: full
# ---------------------------------------------------------------------------

def full(kb_root, prune_threshold=DEFAULT_PRUNE_THRESHOLD):
    results = {}

    results["analyze"] = analyze(kb_root)
    if results["analyze"]["status"] != "success":
        return {"status": "error", "stage": "analyze", "detail": results["analyze"]}

    results["consolidate"] = consolidate(kb_root)
    results["prune"] = prune(kb_root, threshold=prune_threshold)
    results["report"] = generate_report(kb_root, analyze_result=results["analyze"])

    dream_log = load_dream_log(kb_root)
    now_str = datetime.now().isoformat()
    dream_log["last_dream"] = now_str
    dream_log["dreams"].append({
        "date": now_str,
        "nodes_analyzed": results["analyze"]["total_nodes"],
        "nodes_initialized": results["analyze"]["nodes_initialized"],
        "deltas_applied": results["analyze"]["deltas_applied"],
        "nodes_pruned": results["prune"].get("pruned_count", 0),
        "tags_normalized": results["consolidate"]["auto_applied"]["tags_normalized"],
        "hints_added": results["consolidate"]["auto_applied"]["hints_added"],
        "layer1_proposals": len(results["analyze"].get("layer1_proposals", [])),
    })
    save_dream_log(kb_root, dream_log)

    return {
        "status": "success",
        "summary": {
            "nodes_analyzed": results["analyze"]["total_nodes"],
            "is_first_dream": results["analyze"]["is_first_dream"],
            "nodes_initialized": results["analyze"]["nodes_initialized"],
            "deltas_applied": results["analyze"]["deltas_applied"],
            "tags_normalized": results["consolidate"]["auto_applied"]["tags_normalized"],
            "hints_added": results["consolidate"]["auto_applied"]["hints_added"],
            "nodes_pruned": results["prune"].get("pruned_count", 0),
            "proposals": {
                "near_duplicates": len(results["consolidate"]["proposals"]["near_duplicates"]),
                "verbose_definitions": len(results["consolidate"]["proposals"]["verbose_definitions"]),
                "missing_relationships": len(results["consolidate"]["proposals"]["missing_relationships"]),
                "layer1_proposals": len(results["analyze"].get("layer1_proposals", [])),
            },
            "report_path": results["report"].get("report_relative", ""),
        },
        "full_results": results,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="KB Dream v2")
    parser.add_argument("--kb-root", required=True)
    parser.add_argument("--action", required=True,
                        choices=["analyze", "consolidate", "prune", "report",
                                 "restore", "full", "init-node"])
    parser.add_argument("--node-id", help="Node ID (for restore / init-node)")
    parser.add_argument("--threshold", type=float, default=DEFAULT_PRUNE_THRESHOLD)
    parser.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()

    if args.action == "analyze":
        result = analyze(args.kb_root)
    elif args.action == "consolidate":
        result = consolidate(args.kb_root)
    elif args.action == "prune":
        result = prune(args.kb_root, threshold=args.threshold, dry_run=args.dry_run)
    elif args.action == "report":
        result = generate_report(args.kb_root)
    elif args.action == "restore":
        if not args.node_id:
            result = {"status": "error", "message": "--node-id required"}
        else:
            result = restore(args.kb_root, args.node_id)
    elif args.action == "init-node":
        if not args.node_id:
            result = {"status": "error", "message": "--node-id required"}
        else:
            result = init_node(args.kb_root, args.node_id)
    elif args.action == "full":
        result = full(args.kb_root, prune_threshold=args.threshold)

    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
