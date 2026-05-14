#!/usr/bin/env python3
"""
YAML Management for Research Knowledge Base

Safely read, append, update, and manage YAML files for claims, arguments,
concepts, method instantiations, and the Layer 2 graph. Handles ID generation
and version history.

Usage:
    python yaml_manager.py --file <path> --action <action> [options]

Actions:
    next-id     Get the next available ID for a given prefix
    append      Append a new entry to a YAML list file
    update      Update an existing entry by ID
    list        List all entries (optionally filtered)
    get         Get a single entry by ID
    add-node    Add a node to graph.yaml
    add-rel     Add a relationship to a node in graph.yaml
"""

import argparse
import json
import sys
import os
from datetime import date
from pathlib import Path
from copy import deepcopy

try:
    import yaml
except ImportError:
    print(json.dumps({"status": "error", "message": "PyYAML not installed. Run: pip install pyyaml --break-system-packages"}))
    sys.exit(1)


def load_yaml(filepath):
    """Load a YAML file, returning parsed data."""
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data


def save_yaml(filepath, data):
    """Save data to a YAML file."""
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=120)


def get_entries(filepath):
    """Get list entries from a YAML file. Handles both raw lists and dict wrappers."""
    data = load_yaml(filepath)
    if data is None:
        return []
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        # Check common wrapper keys
        for key in ["claims", "arguments", "concepts", "method_instantiations",
                     "overrides", "nodes"]:
            if key in data and isinstance(data[key], list):
                return data[key]
        # If single-key dict with a list value
        for key, val in data.items():
            if isinstance(val, list):
                return val
    return []


def get_wrapper_key(filepath):
    """Determine the wrapper key used in the YAML file."""
    data = load_yaml(filepath)
    if data is None or isinstance(data, list):
        return None
    if isinstance(data, dict):
        for key in ["claims", "arguments", "concepts", "method_instantiations",
                     "overrides", "nodes"]:
            if key in data:
                return key
    return None


def save_entries(filepath, entries, wrapper_key=None):
    """Save entries back to a YAML file, preserving wrapper structure."""
    if wrapper_key:
        data = load_yaml(filepath) or {}
        data[wrapper_key] = entries
        save_yaml(filepath, data)
    else:
        save_yaml(filepath, entries)


def next_id(entries, prefix):
    """Generate the next available ID for a given prefix (e.g., CLM, ARG, CON)."""
    max_num = 0
    for entry in entries:
        eid = entry.get("id", "")
        if isinstance(eid, str) and eid.startswith(prefix + "-"):
            try:
                num = int(eid.split("-")[1])
                max_num = max(max_num, num)
            except (ValueError, IndexError):
                pass
    return f"{prefix}-{max_num + 1:03d}"


def append_entry(filepath, entry, wrapper_key=None):
    """Append a new entry to a YAML list file."""
    entries = get_entries(filepath)
    entries.append(entry)
    wk = wrapper_key or get_wrapper_key(filepath)
    save_entries(filepath, entries, wk)
    return entry


def update_entry(filepath, entry_id, updates, add_history=True):
    """Update an existing entry by ID. Optionally adds version history."""
    entries = get_entries(filepath)
    wk = get_wrapper_key(filepath)

    for i, entry in enumerate(entries):
        if entry.get("id") == entry_id:
            # Add version history if requested
            if add_history and "history" in entry:
                history = entry.get("history", [])
                version_num = len(history) + 1
                history_entry = {
                    "version": version_num,
                    "date": str(date.today()),
                }
                # Capture the fields being changed
                for key in updates:
                    if key in entry and key != "history":
                        history_entry[key] = entry[key]
                history_entry["changed_by"] = updates.pop("changed_by", "user-updated")
                history.append(history_entry)
                entry["history"] = history

            # Apply updates
            for key, value in updates.items():
                if key != "history":
                    entry[key] = value

            entries[i] = entry
            save_entries(filepath, entries, wk)
            return entry

    return None


def get_entry(filepath, entry_id):
    """Get a single entry by ID."""
    entries = get_entries(filepath)
    for entry in entries:
        if entry.get("id") == entry_id:
            return entry
    return None


def list_entries(filepath, filter_field=None, filter_value=None, filter_tags=None):
    """List all entries, optionally filtered by field value and/or tags.

    filter_tags: list of tags — entries must contain ALL specified tags (AND logic).
    """
    entries = get_entries(filepath)
    if filter_field and filter_value:
        entries = [e for e in entries if str(e.get(filter_field, "")).lower() == filter_value.lower()]
    if filter_tags:
        required = [t.lower() for t in filter_tags]
        entries = [e for e in entries
                   if all(rt in [t.lower() for t in e.get("tags", [])] for rt in required)]
    return entries


def add_graph_node(kb_root, node):
    """Add a node to graph.yaml."""
    graph_path = os.path.join(kb_root, "layer2-field", "graph.yaml")
    data = load_yaml(graph_path) or {"nodes": []}
    if data.get("nodes") is None:
        data["nodes"] = []

    # Check for duplicate ID
    for existing in data["nodes"]:
        if existing.get("id") == node.get("id"):
            return {"status": "error", "message": f"Node {node['id']} already exists"}

    data["nodes"].append(node)
    save_yaml(graph_path, data)
    return {"status": "success", "node": node}


def add_graph_relationship(kb_root, source_id, rel_type, target_id):
    """Add a relationship to a node in graph.yaml."""
    graph_path = os.path.join(kb_root, "layer2-field", "graph.yaml")
    data = load_yaml(graph_path) or {"nodes": []}
    if data.get("nodes") is None:
        return {"status": "error", "message": "No nodes in graph"}

    # Validate source and target exist
    source = None
    target = None
    for node in data["nodes"]:
        if node["id"] == source_id:
            source = node
        if node["id"] == target_id:
            target = node

    if not source:
        return {"status": "error", "message": f"Source node {source_id} not found"}
    if not target:
        return {"status": "error", "message": f"Target node {target_id} not found"}

    # Validate relationship type against schema
    schema_path = os.path.join(kb_root, "layer2-field", "relationship-schema.yaml")
    schema = load_yaml(schema_path)
    if schema and schema.get("relationship_types"):
        valid = False
        for rt in schema["relationship_types"]:
            if rt["id"] == rel_type:
                for pair in rt.get("valid_pairs", []):
                    if pair["source"] == source.get("type") and pair["target"] == target.get("type"):
                        valid = True
                        break
                break
        if not valid:
            return {"status": "error", "message": f"Relationship '{rel_type}' is not valid between {source.get('type')} and {target.get('type')}"}

    # Add relationship
    if source.get("relationships") is None:
        source["relationships"] = []

    # Check for duplicate
    for rel in source["relationships"]:
        if rel["type"] == rel_type and rel["target"] == target_id:
            return {"status": "error", "message": "Relationship already exists"}

    # Include target_hint for LLM-readable cross-references
    rel_entry = {"type": rel_type, "target": target_id, "target_hint": target.get("name", "")}
    source["relationships"].append(rel_entry)
    save_yaml(graph_path, data)
    return {"status": "success", "source": source_id, "type": rel_type, "target": target_id, "target_hint": rel_entry["target_hint"]}


def main():
    parser = argparse.ArgumentParser(description="YAML Management for Research Knowledge Base")
    parser.add_argument("--file", help="Path to the YAML file")
    parser.add_argument("--kb-root", help="Path to KB root (for graph operations)")
    parser.add_argument("--action", required=True,
                       choices=["next-id", "append", "update", "list", "get", "add-node", "add-rel"])
    parser.add_argument("--prefix", help="ID prefix for next-id (e.g., CLM, ARG, CON)")
    parser.add_argument("--entry", help="JSON string of the entry to append or node to add")
    parser.add_argument("--entry-id", help="Entry ID for update/get")
    parser.add_argument("--updates", help="JSON string of fields to update")
    parser.add_argument("--filter-field", help="Field name to filter by")
    parser.add_argument("--filter-value", help="Value to filter for")
    parser.add_argument("--source-id", help="Source node ID for add-rel")
    parser.add_argument("--rel-type", help="Relationship type for add-rel")
    parser.add_argument("--target-id", help="Target node ID for add-rel")
    parser.add_argument("--wrapper-key", help="YAML wrapper key (e.g., 'claims')")
    parser.add_argument("--filter-tags", help="Comma-separated tags to filter by (AND logic)")

    args = parser.parse_args()

    if args.action == "next-id":
        if not args.file or not args.prefix:
            print(json.dumps({"status": "error", "message": "--file and --prefix required"}))
            sys.exit(1)
        entries = get_entries(args.file)
        nid = next_id(entries, args.prefix)
        print(json.dumps({"status": "success", "next_id": nid}))

    elif args.action == "append":
        if not args.file or not args.entry:
            print(json.dumps({"status": "error", "message": "--file and --entry required"}))
            sys.exit(1)
        entry = json.loads(args.entry)
        result = append_entry(args.file, entry, args.wrapper_key)
        print(json.dumps({"status": "success", "appended": result}, indent=2, default=str))

    elif args.action == "update":
        if not args.file or not args.entry_id or not args.updates:
            print(json.dumps({"status": "error", "message": "--file, --entry-id, and --updates required"}))
            sys.exit(1)
        updates = json.loads(args.updates)
        result = update_entry(args.file, args.entry_id, updates)
        if result:
            print(json.dumps({"status": "success", "updated": result}, indent=2, default=str))
        else:
            print(json.dumps({"status": "error", "message": f"Entry {args.entry_id} not found"}))

    elif args.action == "list":
        if not args.file:
            print(json.dumps({"status": "error", "message": "--file required"}))
            sys.exit(1)
        filter_tags = [t.strip() for t in args.filter_tags.split(",")] if args.filter_tags else None
        results = list_entries(args.file, args.filter_field, args.filter_value, filter_tags)
        print(json.dumps({"status": "success", "count": len(results), "entries": results}, indent=2, default=str))

    elif args.action == "get":
        if not args.file or not args.entry_id:
            print(json.dumps({"status": "error", "message": "--file and --entry-id required"}))
            sys.exit(1)
        result = get_entry(args.file, args.entry_id)
        if result:
            print(json.dumps({"status": "success", "entry": result}, indent=2, default=str))
        else:
            print(json.dumps({"status": "error", "message": f"Entry {args.entry_id} not found"}))

    elif args.action == "add-node":
        if not args.kb_root or not args.entry:
            print(json.dumps({"status": "error", "message": "--kb-root and --entry required"}))
            sys.exit(1)
        node = json.loads(args.entry)
        result = add_graph_node(args.kb_root, node)
        print(json.dumps(result, indent=2, default=str))

    elif args.action == "add-rel":
        if not args.kb_root or not args.source_id or not args.rel_type or not args.target_id:
            print(json.dumps({"status": "error", "message": "--kb-root, --source-id, --rel-type, --target-id required"}))
            sys.exit(1)
        result = add_graph_relationship(args.kb_root, args.source_id, args.rel_type, args.target_id)
        print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
