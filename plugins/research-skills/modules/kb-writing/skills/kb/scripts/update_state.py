#!/usr/bin/env python3
"""
State Manifest Builder

Scans the entire Research Knowledge Base and produces a compact
kb-state.yaml snapshot. Claude reads this one file to orient itself
at the start of any conversation.

Usage:
    python update_state.py --kb-root <path>

Run after every significant operation (project creation, archiving,
claim extraction, Layer 2 updates, etc.).
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print(json.dumps({"status": "error", "message": "PyYAML not installed. Run: pip install pyyaml --break-system-packages"}))
    sys.exit(1)


def load_yaml_safe(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data


def count_entries(filepath, wrapper_keys=None):
    data = load_yaml_safe(filepath)
    if data is None:
        return 0
    if isinstance(data, list):
        return len(data)
    if isinstance(data, dict) and wrapper_keys:
        for key in wrapper_keys:
            if key in data and isinstance(data[key], list):
                return len(data[key])
    return 0


def file_exists_nonempty(filepath):
    if not os.path.exists(filepath):
        return False
    return os.path.getsize(filepath) > 10


def scan_layer1(kb_root):
    l1_path = Path(kb_root) / "layer1-researcher"
    profile_path = l1_path / "narrative-profile.md"
    rules_dir = l1_path / "rules"
    rule_files = []
    if rules_dir.exists():
        rule_files = [f.stem for f in rules_dir.glob("*.md")]
    override_count = count_entries(str(l1_path / "override-log.yaml"), ["overrides"])
    pubs_data = load_yaml_safe(str(l1_path / "my-publications.yaml"))
    pubs_list = pubs_data if isinstance(pubs_data, list) else []
    pubs_total = len(pubs_list)
    pubs_extracted = sum(1 for p in pubs_list if isinstance(p, dict) and p.get("extraction_status") == "extracted")
    pubs_pending = sum(1 for p in pubs_list if isinstance(p, dict) and p.get("extraction_status") == "pending")
    return {
        "initialized": file_exists_nonempty(str(profile_path)),
        "profile_exists": profile_path.exists(),
        "rule_categories": rule_files,
        "rule_count": len(rule_files),
        "total_overrides_logged": override_count,
        "publications": {"total": pubs_total, "extracted": pubs_extracted, "pending": pubs_pending},
    }


def scan_layer2(kb_root):
    l2_path = Path(kb_root) / "layer2-field"
    graph_path = l2_path / "graph.yaml"
    graph = load_yaml_safe(str(graph_path)) or {"nodes": []}
    nodes = graph.get("nodes") or []
    concept_count = sum(1 for n in nodes if n.get("type") == "concept")
    method_count = sum(1 for n in nodes if n.get("type") == "method")
    project_count = sum(1 for n in nodes if n.get("type") == "project")
    total_rels = 0
    for node in nodes:
        total_rels += len(node.get("relationships") or [])
    concept_files = list((l2_path / "concepts").glob("*.md")) if (l2_path / "concepts").exists() else []
    method_files = list((l2_path / "methods").glob("*.md")) if (l2_path / "methods").exists() else []
    readings_data = load_yaml_safe(str(l2_path / "fundamental-readings.yaml"))
    readings_list = readings_data if isinstance(readings_data, list) else []
    readings_total = len(readings_list)
    readings_extracted = sum(1 for r in readings_list if isinstance(r, dict) and r.get("extraction_status") == "extracted")
    readings_pending = sum(1 for r in readings_list if isinstance(r, dict) and r.get("extraction_status") == "pending")
    return {
        "total_nodes": len(nodes),
        "concepts": concept_count,
        "methods": method_count,
        "project_nodes": project_count,
        "total_relationships": total_rels,
        "concept_detail_files": len(concept_files),
        "method_detail_files": len(method_files),
        "fundamental_readings": {"total": readings_total, "extracted": readings_extracted, "pending": readings_pending},
    }


def scan_project(proj_path):
    name = proj_path.name
    overview_exists = file_exists_nonempty(str(proj_path / "overview.md"))
    claim_count = count_entries(str(proj_path / "claims.yaml"), ["claims"])
    arg_count = count_entries(str(proj_path / "arguments.yaml"), ["arguments"])
    concept_count = count_entries(str(proj_path / "concepts.yaml"), ["concepts"])
    method_count = count_entries(str(proj_path / "method-instantiations.yaml"), ["method_instantiations"])
    claims_data = load_yaml_safe(str(proj_path / "claims.yaml"))
    claims_list = []
    if isinstance(claims_data, list):
        claims_list = claims_data
    elif isinstance(claims_data, dict):
        for key in ["claims"]:
            if key in claims_data and isinstance(claims_data[key], list):
                claims_list = claims_data[key]
                break
    draft_claims = sum(1 for c in claims_list if isinstance(c, dict) and c.get("status") == "draft")
    refined_claims = sum(1 for c in claims_list if isinstance(c, dict) and c.get("status") == "refined")
    paper_count = len(list((proj_path / "papers").glob("*.pdf"))) if (proj_path / "papers").exists() else 0
    has_skimmed = (proj_path / "skimmed-papers.xlsx").exists()
    has_deep_reading = any(proj_path.glob("*_deep_reading.xlsx"))
    override_count = count_entries(str(proj_path / "override-log.yaml"), ["overrides"])
    links_data = load_yaml_safe(str(proj_path / "external-links.yaml"))
    external_links = []
    if isinstance(links_data, dict) and isinstance(links_data.get("links"), list):
        external_links = links_data["links"]
    stage = "empty"
    if overview_exists:
        stage = "initialized"
    if has_skimmed:
        stage = "papers_skimmed"
    if paper_count > 0:
        stage = "papers_curated"
    if claim_count > 0:
        stage = "claims_extracted"
    if refined_claims > 0:
        stage = "claims_refined"
    if arg_count > 0:
        stage = "arguments_built"
    if any(proj_path.glob("*_literature_review.docx")) or any(proj_path.glob("*_introduction.docx")):
        stage = "writing_done"
    result = {
        "name": name, "stage": stage, "overview": overview_exists,
        "papers": {"curated_pdfs": paper_count, "skimmed_spreadsheet": has_skimmed, "deep_reading": has_deep_reading},
        "claims": {"total": claim_count, "draft": draft_claims, "refined": refined_claims},
        "arguments": arg_count, "project_concepts": concept_count,
        "method_instantiations": method_count, "overrides_logged": override_count,
    }
    if external_links:
        result["external_links"] = len(external_links)
    return result


def scan_projects(kb_root):
    active = []
    archived = []
    active_dir = Path(kb_root) / "projects" / "active"
    archived_dir = Path(kb_root) / "projects" / "archived"
    if active_dir.exists():
        for p in sorted(active_dir.iterdir()):
            if p.is_dir():
                active.append(scan_project(p))
    if archived_dir.exists():
        for p in sorted(archived_dir.iterdir()):
            if p.is_dir():
                archived.append(scan_project(p))
    return {"active": active, "archived": archived}


def build_state(kb_root):
    state = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "kb_root": str(kb_root),
        "layer1": scan_layer1(kb_root),
        "layer2": scan_layer2(kb_root),
        "projects": scan_projects(kb_root),
    }
    projects = state["projects"]
    state["summary"] = {
        "layer1_initialized": state["layer1"]["initialized"],
        "layer2_nodes": state["layer2"]["total_nodes"],
        "active_projects": len(projects["active"]),
        "archived_projects": len(projects["archived"]),
        "active_project_names": [p["name"] for p in projects["active"]],
        "archived_project_names": [p["name"] for p in projects["archived"]],
    }
    return state


def main():
    parser = argparse.ArgumentParser(description="State Manifest Builder")
    parser.add_argument("--kb-root", required=True, help="Path to Research Knowledge Base root")
    args = parser.parse_args()
    state = build_state(args.kb_root)
    state_path = os.path.join(args.kb_root, "kb-state.yaml")
    with open(state_path, "w", encoding="utf-8") as f:
        yaml.dump(state, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=120)
    print(json.dumps({"status": "success", "state_file": state_path, "summary": state["summary"]}, indent=2))


if __name__ == "__main__":
    main()
