#!/usr/bin/env python3
"""
Project Archiving Helper

Moves a project from active to archived, creates a project node summary,
and identifies candidates for Layer 2 promotion.

Usage:
    python archive_project.py --kb-root <path> --project <name> --action <action>

Actions:
    check       Check if a project is ready to archive (lists contents)
    move        Move project from active/ to archived/
    summarize   Generate a project node summary for Layer 2
    promotions  Identify candidates for Layer 2 promotion
"""

import argparse
import json
import os
import shutil
import sys
from pathlib import Path
from datetime import date

try:
    import yaml
except ImportError:
    print(json.dumps({"status": "error", "message": "PyYAML not installed. Run: pip install pyyaml --break-system-packages"}))
    sys.exit(1)


def load_yaml_safe(filepath):
    """Load YAML safely."""
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data


def check_project(kb_root, project_name):
    """Check project contents and readiness for archiving."""
    proj_path = Path(kb_root) / "projects" / "active" / project_name
    if not proj_path.exists():
        return {"status": "error", "message": f"Project '{project_name}' not found in active projects"}

    contents = {}
    # Check each expected file
    files_to_check = [
        ("overview.md", "Project overview"),
        ("progress-summary.md", "Progress summary"),
        ("skimmed-papers.xlsx", "Skimmed papers spreadsheet"),
        ("papers-reference.md", "Papers reference"),
        ("claims.yaml", "Claims"),
        ("arguments.yaml", "Arguments"),
        ("concepts.yaml", "Project concepts"),
        ("method-instantiations.yaml", "Method instantiations"),
        ("competing-explanations.md", "Competing explanations"),
        ("override-log.yaml", "Override log"),
        ("external-links.yaml", "External links"),
    ]

    for filename, label in files_to_check:
        filepath = proj_path / filename
        exists = filepath.exists()
        size = filepath.stat().st_size if exists else 0
        contents[label] = {"file": filename, "exists": exists, "size_bytes": size}

    # Count papers
    papers_dir = proj_path / "papers"
    paper_count = len(list(papers_dir.glob("*.pdf"))) if papers_dir.exists() else 0
    contents["Curated papers (PDFs)"] = {"count": paper_count}

    # Count claims and arguments
    claims_data = load_yaml_safe(str(proj_path / "claims.yaml"))
    if claims_data and isinstance(claims_data, list):
        contents["Claims"]["count"] = len(claims_data)
    elif claims_data and isinstance(claims_data, dict):
        for key in ["claims"]:
            if key in claims_data and isinstance(claims_data[key], list):
                contents["Claims"]["count"] = len(claims_data[key])

    args_data = load_yaml_safe(str(proj_path / "arguments.yaml"))
    if args_data and isinstance(args_data, list):
        contents["Arguments"]["count"] = len(args_data)
    elif args_data and isinstance(args_data, dict):
        for key in ["arguments"]:
            if key in args_data and isinstance(args_data[key], list):
                contents["Arguments"]["count"] = len(args_data[key])

    return {"status": "success", "project": project_name, "path": str(proj_path), "contents": contents}


def move_project(kb_root, project_name):
    """Move project from active to archived."""
    src = Path(kb_root) / "projects" / "active" / project_name
    dst = Path(kb_root) / "projects" / "archived" / project_name

    if not src.exists():
        return {"status": "error", "message": f"Project '{project_name}' not found in active projects"}
    if dst.exists():
        return {"status": "error", "message": f"Project '{project_name}' already exists in archived projects"}

    shutil.move(str(src), str(dst))
    return {"status": "success", "message": f"Moved '{project_name}' from active to archived", "new_path": str(dst)}


def summarize_project(kb_root, project_name):
    """Generate a project node summary for Layer 2 graph."""
    # Look in both active and archived
    for status in ["active", "archived"]:
        proj_path = Path(kb_root) / "projects" / status / project_name
        if proj_path.exists():
            break
    else:
        return {"status": "error", "message": f"Project '{project_name}' not found"}

    # Read overview
    overview_path = proj_path / "overview.md"
    overview_text = overview_path.read_text(encoding="utf-8") if overview_path.exists() else ""

    # Read claims
    claims = load_yaml_safe(str(proj_path / "claims.yaml")) or []
    if isinstance(claims, dict):
        for key in ["claims"]:
            if key in claims:
                claims = claims[key] or []
                break
    refined_claims = [c for c in claims if isinstance(c, dict) and c.get("status") == "refined"]

    # Read arguments
    arguments = load_yaml_safe(str(proj_path / "arguments.yaml")) or []
    if isinstance(arguments, dict):
        for key in ["arguments"]:
            if key in arguments:
                arguments = arguments[key] or []
                break

    # Read project concepts
    concepts = load_yaml_safe(str(proj_path / "concepts.yaml")) or []
    if isinstance(concepts, dict):
        for key in ["concepts"]:
            if key in concepts:
                concepts = concepts[key] or []
                break

    # Read method instantiations
    methods = load_yaml_safe(str(proj_path / "method-instantiations.yaml")) or []
    if isinstance(methods, dict):
        for key in ["method_instantiations"]:
            if key in methods:
                methods = methods[key] or []
                break

    # Extract key findings from refined claims
    key_findings = [c.get("statement", "") for c in refined_claims[:5]]

    # Extract research questions from overview (heuristic: lines containing "?")
    rqs = [line.strip() for line in overview_text.split("\n")
           if "?" in line and len(line.strip()) > 10 and not line.strip().startswith("#")][:5]

    # Get next project ID from graph
    graph_path = Path(kb_root) / "layer2-field" / "graph.yaml"
    graph = load_yaml_safe(str(graph_path)) or {"nodes": []}
    if graph.get("nodes") is None:
        graph["nodes"] = []
    max_prj = 0
    for node in graph["nodes"]:
        if node.get("id", "").startswith("PRJ-"):
            try:
                num = int(node["id"].split("-")[1])
                max_prj = max(max_prj, num)
            except (ValueError, IndexError):
                pass
    next_id = f"PRJ-{max_prj + 1:03d}"

    # Build relationships
    relationships = []
    # Concepts investigated
    for c in concepts:
        if isinstance(c, dict) and c.get("base_concept_id"):
            relationships.append({"type": "investigated", "target": c["base_concept_id"]})
    # Methods used
    for m in methods:
        if isinstance(m, dict) and m.get("base_method_id"):
            relationships.append({"type": "used", "target": m["base_method_id"]})

    node = {
        "id": next_id,
        "type": "project",
        "name": project_name.replace("-", " ").title(),
        "summary": f"Project with {len(refined_claims)} refined claims and {len(arguments)} argument units.",
        "key_findings": key_findings,
        "research_questions": rqs,
        "folder": f"projects/archived/{project_name}",
        "relationships": relationships,
        "archived_date": str(date.today()),
    }

    return {
        "status": "success",
        "proposed_node": node,
        "stats": {
            "total_claims": len(claims),
            "refined_claims": len(refined_claims),
            "arguments": len(arguments),
            "project_concepts": len(concepts),
            "method_instantiations": len(methods),
        }
    }


def identify_promotions(kb_root, project_name):
    """Identify knowledge candidates for promotion to Layer 2."""
    for status in ["active", "archived"]:
        proj_path = Path(kb_root) / "projects" / status / project_name
        if proj_path.exists():
            break
    else:
        return {"status": "error", "message": f"Project '{project_name}' not found"}

    promotions = []

    # Check project concepts — are any generalizable?
    concepts = load_yaml_safe(str(proj_path / "concepts.yaml")) or []
    if isinstance(concepts, dict):
        for key in ["concepts"]:
            if key in concepts:
                concepts = concepts[key] or []
                break
    for c in concepts:
        if isinstance(c, dict) and not c.get("base_concept_id"):
            # Novel concept — candidate for Layer 2
            promotions.append({
                "type": "concept",
                "name": c.get("name", "Unknown"),
                "description": c.get("refinement", ""),
                "reason": "Novel project-specific concept with no Layer 2 equivalent — may be generalizable."
            })

    # Check method instantiations — any novel usage?
    methods = load_yaml_safe(str(proj_path / "method-instantiations.yaml")) or []
    if isinstance(methods, dict):
        for key in ["method_instantiations"]:
            if key in methods:
                methods = methods[key] or []
                break
    for m in methods:
        if isinstance(m, dict) and m.get("deviations"):
            promotions.append({
                "type": "method_variant",
                "name": m.get("name", "Unknown"),
                "base_method": m.get("base_method_id", "Unknown"),
                "deviations": m.get("deviations", ""),
                "reason": "Method used with deviations — the variant may be worth adding to Layer 2."
            })

    # Check refined claims — any canonical findings?
    claims = load_yaml_safe(str(proj_path / "claims.yaml")) or []
    if isinstance(claims, dict):
        for key in ["claims"]:
            if key in claims:
                claims = claims[key] or []
                break
    refined = [c for c in claims if isinstance(c, dict) and c.get("status") == "refined"]
    if len(refined) > 3:
        # Suggest the strongest claims as potential canonical findings
        promotions.append({
            "type": "canonical_findings",
            "count": len(refined),
            "reason": f"This project has {len(refined)} refined claims. Consider whether any are canonical enough to note in Layer 2 concept entries as illustrative examples."
        })

    return {"status": "success", "project": project_name, "promotion_candidates": promotions}


def main():
    parser = argparse.ArgumentParser(description="Project Archiving Helper")
    parser.add_argument("--kb-root", required=True, help="Path to Research Knowledge Base root")
    parser.add_argument("--project", required=True, help="Project name")
    parser.add_argument("--action", required=True, choices=["check", "move", "summarize", "promotions"])

    args = parser.parse_args()

    if args.action == "check":
        result = check_project(args.kb_root, args.project)
    elif args.action == "move":
        result = move_project(args.kb_root, args.project)
    elif args.action == "summarize":
        result = summarize_project(args.kb_root, args.project)
    elif args.action == "promotions":
        result = identify_promotions(args.kb_root, args.project)

    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
