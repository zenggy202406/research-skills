#!/usr/bin/env python3
"""
Cross-Project and Cross-Layer Search

Searches across all projects and layers in the Research Knowledge Base
for claims, arguments, concepts, methods, and free text.

Usage:
    python cross_search.py --kb-root <path> --mode <mode> --keyword <keyword> [options]

Modes:
    claims      Search claims.yaml across all projects
    arguments   Search arguments.yaml across all projects
    concepts    Search concepts across Layer 2 and all project concepts.yaml
    methods     Search methods across Layer 2 and all project method-instantiations.yaml
    papers      Search papers-reference.md across all projects
    all         Search everything for a keyword

Options:
    --tags      Comma-separated tags to filter by (entries must match ALL tags)
    --project   Filter to a specific project name
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print(json.dumps({"status": "error", "message": "PyYAML not installed. Run: pip install pyyaml --break-system-packages"}))
    sys.exit(1)


def find_projects(kb_root):
    """Find all active and archived project directories."""
    projects = []
    for status in ["active", "archived"]:
        proj_dir = Path(kb_root) / "projects" / status
        if proj_dir.exists():
            for p in proj_dir.iterdir():
                if p.is_dir():
                    projects.append({
                        "name": p.name,
                        "status": status,
                        "path": str(p)
                    })
    return projects


def load_yaml_safe(filepath):
    """Load a YAML file safely, returning empty list if missing or empty."""
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if data is None:
        return []
    if isinstance(data, dict):
        # Files like claims.yaml might just be a list, or might have a wrapper key
        for key in ["claims", "arguments", "concepts", "method_instantiations", "nodes"]:
            if key in data:
                return data[key] if data[key] else []
        return []
    if isinstance(data, list):
        return data
    return []


def search_in_text(text, keyword):
    """Case-insensitive keyword search in text."""
    return keyword.lower() in text.lower()


def matches_tags(entry, required_tags):
    """Check if an entry's tags list contains ALL required tags (case-insensitive)."""
    if not required_tags:
        return True
    entry_tags = [t.lower() for t in entry.get("tags", [])]
    return all(rt.lower() in entry_tags for rt in required_tags)


def search_claims(kb_root, keyword, project_filter=None, required_tags=None):
    """Search claims across all projects. Supports keyword + tag filtering."""
    results = []
    projects = find_projects(kb_root)

    for proj in projects:
        if project_filter and proj["name"] != project_filter:
            continue
        claims_path = os.path.join(proj["path"], "claims.yaml")
        claims = load_yaml_safe(claims_path)
        for claim in claims:
            if not isinstance(claim, dict):
                continue
            if not matches_tags(claim, required_tags):
                continue
            searchable = " ".join(str(v) for v in [
                claim.get("statement", ""),
                claim.get("conditions", ""),
                claim.get("population", ""),
                claim.get("source", ""),
                claim.get("source_id", ""),
                claim.get("method_hint", ""),
                " ".join(claim.get("tags", [])),
                claim.get("notes", ""),
            ])
            if search_in_text(searchable, keyword):
                results.append({
                    "project": proj["name"],
                    "project_status": proj["status"],
                    "claim": claim
                })
    return results


def search_arguments(kb_root, keyword, project_filter=None, required_tags=None):
    """Search arguments across all projects. Supports keyword + tag filtering."""
    results = []
    projects = find_projects(kb_root)

    for proj in projects:
        if project_filter and proj["name"] != project_filter:
            continue
        args_path = os.path.join(proj["path"], "arguments.yaml")
        arguments = load_yaml_safe(args_path)
        for arg in arguments:
            if not isinstance(arg, dict):
                continue
            if not matches_tags(arg, required_tags):
                continue
            searchable = " ".join(str(v) for v in [
                arg.get("conclusion", ""),
                " ".join(arg.get("tags", [])),
                json.dumps(arg.get("premises", [])),
                json.dumps(arg.get("theoretical_grounding", [])),
                json.dumps(arg.get("assumptions", [])),
                json.dumps(arg.get("counterarguments", [])),
                json.dumps(arg.get("scope_conditions", [])),
                arg.get("notes", ""),
            ])
            if search_in_text(searchable, keyword):
                results.append({
                    "project": proj["name"],
                    "project_status": proj["status"],
                    "argument": arg
                })
    return results


def search_concepts(kb_root, keyword, required_tags=None):
    """Search concepts across Layer 2 and all project concepts. Supports tag filtering."""
    results = []

    # Layer 2 concepts
    graph_path = Path(kb_root) / "layer2-field" / "graph.yaml"
    if graph_path.exists():
        with open(graph_path, "r", encoding="utf-8") as f:
            graph = yaml.safe_load(f)
        if graph and graph.get("nodes"):
            for node in graph["nodes"]:
                if node.get("type") != "concept":
                    continue
                if not matches_tags(node, required_tags):
                    continue
                searchable = " ".join(str(v) for v in [
                    node.get("name", ""),
                    node.get("definition", ""),
                    node.get("boundaries", ""),
                    " ".join(node.get("tags", [])),
                ])
                if search_in_text(searchable, keyword):
                    results.append({
                        "layer": "Layer 2",
                        "concept": node
                    })

    # Layer 2 concept markdown files
    concepts_dir = Path(kb_root) / "layer2-field" / "concepts"
    if concepts_dir.exists():
        for md_file in concepts_dir.glob("*.md"):
            content = md_file.read_text(encoding="utf-8")
            if search_in_text(content, keyword):
                results.append({
                    "layer": "Layer 2",
                    "file": str(md_file.name),
                    "match_type": "markdown_file"
                })

    # Project-level concepts
    projects = find_projects(kb_root)
    for proj in projects:
        concepts_path = os.path.join(proj["path"], "concepts.yaml")
        concepts = load_yaml_safe(concepts_path)
        for concept in concepts:
            if not isinstance(concept, dict):
                continue
            if not matches_tags(concept, required_tags):
                continue
            searchable = " ".join(str(v) for v in [
                concept.get("name", ""),
                concept.get("base_concept_hint", ""),
                " ".join(concept.get("tags", [])),
                concept.get("refinement", ""),
                concept.get("notes", ""),
            ])
            if search_in_text(searchable, keyword):
                results.append({
                    "layer": "Layer 3",
                    "project": proj["name"],
                    "concept": concept
                })

    return results


def search_methods(kb_root, keyword, required_tags=None):
    """Search methods across Layer 2 and all project instantiations. Supports tag filtering."""
    results = []

    # Layer 2 methods
    graph_path = Path(kb_root) / "layer2-field" / "graph.yaml"
    if graph_path.exists():
        with open(graph_path, "r", encoding="utf-8") as f:
            graph = yaml.safe_load(f)
        if graph and graph.get("nodes"):
            for node in graph["nodes"]:
                if node.get("type") != "method":
                    continue
                if not matches_tags(node, required_tags):
                    continue
                searchable = " ".join(str(v) for v in [
                    node.get("name", ""),
                    node.get("definition", ""),
                    " ".join(node.get("tags", [])),
                ])
                if search_in_text(searchable, keyword):
                    results.append({
                        "layer": "Layer 2",
                        "method": node
                    })

    # Layer 2 method markdown files
    methods_dir = Path(kb_root) / "layer2-field" / "methods"
    if methods_dir.exists():
        for md_file in methods_dir.glob("*.md"):
            content = md_file.read_text(encoding="utf-8")
            if search_in_text(content, keyword):
                results.append({
                    "layer": "Layer 2",
                    "file": str(md_file.name),
                    "match_type": "markdown_file"
                })

    # Project-level method instantiations
    projects = find_projects(kb_root)
    for proj in projects:
        methods_path = os.path.join(proj["path"], "method-instantiations.yaml")
        methods = load_yaml_safe(methods_path)
        for method in methods:
            if not isinstance(method, dict):
                continue
            if not matches_tags(method, required_tags):
                continue
            searchable = " ".join(str(v) for v in [
                method.get("name", ""),
                method.get("base_method_hint", ""),
                " ".join(method.get("tags", [])),
                method.get("description", ""),
                method.get("deviations", ""),
            ])
            if search_in_text(searchable, keyword):
                results.append({
                    "layer": "Layer 3",
                    "project": proj["name"],
                    "method_instantiation": method
                })

    return results


def search_papers(kb_root, keyword):
    """Search papers-reference.md across all projects."""
    results = []
    projects = find_projects(kb_root)

    for proj in projects:
        ref_path = os.path.join(proj["path"], "papers-reference.md")
        if os.path.exists(ref_path):
            content = Path(ref_path).read_text(encoding="utf-8")
            lines = content.split("\n")
            for line in lines:
                if search_in_text(line, keyword) and line.strip():
                    results.append({
                        "project": proj["name"],
                        "project_status": proj["status"],
                        "reference_line": line.strip()
                    })

    return results


def search_all(kb_root, keyword, required_tags=None):
    """Search everything."""
    return {
        "claims": search_claims(kb_root, keyword, required_tags=required_tags),
        "arguments": search_arguments(kb_root, keyword, required_tags=required_tags),
        "concepts": search_concepts(kb_root, keyword, required_tags=required_tags),
        "methods": search_methods(kb_root, keyword, required_tags=required_tags),
        "papers": search_papers(kb_root, keyword),
    }


def main():
    parser = argparse.ArgumentParser(description="Cross-Project and Cross-Layer Search")
    parser.add_argument("--kb-root", required=True, help="Path to Research Knowledge Base root")
    parser.add_argument("--mode", required=True, choices=["claims", "arguments", "concepts", "methods", "papers", "all"])
    parser.add_argument("--keyword", required=True, help="Search keyword")
    parser.add_argument("--project", help="Filter to a specific project name")
    parser.add_argument("--tags", help="Comma-separated tags to filter by (entries must match ALL)")

    args = parser.parse_args()
    required_tags = [t.strip() for t in args.tags.split(",")] if args.tags else None

    if args.mode == "claims":
        results = search_claims(args.kb_root, args.keyword, args.project, required_tags)
    elif args.mode == "arguments":
        results = search_arguments(args.kb_root, args.keyword, args.project, required_tags)
    elif args.mode == "concepts":
        results = search_concepts(args.kb_root, args.keyword, required_tags)
    elif args.mode == "methods":
        results = search_methods(args.kb_root, args.keyword, required_tags)
    elif args.mode == "papers":
        results = search_papers(args.kb_root, args.keyword)
    elif args.mode == "all":
        results = search_all(args.kb_root, args.keyword, required_tags)

    if isinstance(results, dict):
        total = sum(len(v) for v in results.values())
        print(json.dumps({"status": "success", "total_results": total, "results": results}, indent=2, default=str))
    else:
        print(json.dumps({"status": "success", "count": len(results), "results": results}, indent=2, default=str))


if __name__ == "__main__":
    main()
