#!/usr/bin/env python3
"""
Layer 2 Knowledge Graph Operations

Provides search, browse, path-finding, and summary operations
on the Layer 2 field knowledge graph (graph.yaml).

Usage:
    python graph_ops.py --kb-root <path> --action <action> [options]

Actions:
    search      Search nodes by keyword in name/definition
    browse      List all nodes of a given type
    relations   Show all relationships for a node
    path        Find connection path between two nodes (up to 2 hops)
    summary     Print a summary of the entire graph
    neighbors   Show direct neighbors of a node
"""

import argparse
import json
import sys
from pathlib import Path
from collections import defaultdict

try:
    import yaml
except ImportError:
    print(json.dumps({"status": "error", "message": "PyYAML not installed. Run: pip install pyyaml --break-system-packages"}))
    sys.exit(1)


def load_graph(kb_root):
    graph_path = Path(kb_root) / "layer2-field" / "graph.yaml"
    if not graph_path.exists():
        return {"nodes": []}
    with open(graph_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if data is None or "nodes" not in data:
        return {"nodes": []}
    # Handle case where nodes is None (empty list in YAML)
    if data["nodes"] is None:
        data["nodes"] = []
    return data


def load_schema(kb_root):
    schema_path = Path(kb_root) / "layer2-field" / "relationship-schema.yaml"
    if not schema_path.exists():
        return {"relationship_types": []}
    with open(schema_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def search_nodes(graph, keyword, node_type=None):
    """Search nodes by keyword in name, definition, or summary."""
    keyword_lower = keyword.lower()
    results = []
    for node in graph["nodes"]:
        if node_type and node.get("type") != node_type:
            continue
        searchable = " ".join([
            node.get("name", ""),
            node.get("definition", ""),
            node.get("summary", ""),
            node.get("boundaries", ""),
        ]).lower()
        if keyword_lower in searchable:
            results.append(node)
    return results


def browse_nodes(graph, node_type):
    """List all nodes of a given type."""
    return [n for n in graph["nodes"] if n.get("type") == node_type]


def get_node(graph, node_id):
    """Get a node by ID."""
    for node in graph["nodes"]:
        if node.get("id") == node_id:
            return node
    return None


def get_node_by_name(graph, name):
    """Get a node by name (case-insensitive)."""
    name_lower = name.lower()
    for node in graph["nodes"]:
        if node.get("name", "").lower() == name_lower:
            return node
    return None


def get_relationships(graph, node_id):
    """Get all relationships for a node (both outgoing and incoming)."""
    outgoing = []
    incoming = []
    node = get_node(graph, node_id)
    if node and node.get("relationships"):
        for rel in node["relationships"]:
            target = get_node(graph, rel["target"])
            outgoing.append({
                "type": rel["type"],
                "target_id": rel["target"],
                "target_name": target["name"] if target else "unknown",
                "direction": "outgoing"
            })
    # Find incoming
    for other in graph["nodes"]:
        if other.get("id") == node_id:
            continue
        for rel in (other.get("relationships") or []):
            if rel["target"] == node_id:
                incoming.append({
                    "type": rel["type"],
                    "source_id": other["id"],
                    "source_name": other.get("name", "unknown"),
                    "direction": "incoming"
                })
    return {"outgoing": outgoing, "incoming": incoming}


def find_neighbors(graph, node_id):
    """Find all directly connected nodes."""
    rels = get_relationships(graph, node_id)
    neighbor_ids = set()
    for r in rels["outgoing"]:
        neighbor_ids.add(r["target_id"])
    for r in rels["incoming"]:
        neighbor_ids.add(r["source_id"])
    return [get_node(graph, nid) for nid in neighbor_ids if get_node(graph, nid)]


def find_path(graph, start_id, end_id, max_hops=2):
    """Find a path between two nodes (BFS, up to max_hops)."""
    if start_id == end_id:
        return [start_id]

    # Build adjacency list (undirected)
    adj = defaultdict(set)
    for node in graph["nodes"]:
        nid = node.get("id")
        for rel in (node.get("relationships") or []):
            adj[nid].add((rel["target"], rel["type"]))
            adj[rel["target"]].add((nid, rel["type"]))

    # BFS
    visited = {start_id}
    queue = [(start_id, [start_id], [])]

    while queue:
        current, path, rel_path = queue.pop(0)
        if len(path) - 1 >= max_hops:
            continue
        for neighbor, rel_type in adj[current]:
            if neighbor in visited:
                continue
            new_path = path + [neighbor]
            new_rel_path = rel_path + [rel_type]
            if neighbor == end_id:
                return {"nodes": new_path, "relationships": new_rel_path}
            visited.add(neighbor)
            queue.append((neighbor, new_path, new_rel_path))

    return None


def graph_summary(graph):
    """Generate a summary of the entire graph."""
    type_counts = defaultdict(int)
    rel_counts = defaultdict(int)
    total_rels = 0

    for node in graph["nodes"]:
        type_counts[node.get("type", "unknown")] += 1
        for rel in (node.get("relationships") or []):
            rel_counts[rel["type"]] += 1
            total_rels += 1

    return {
        "total_nodes": len(graph["nodes"]),
        "nodes_by_type": dict(type_counts),
        "total_relationships": total_rels,
        "relationships_by_type": dict(rel_counts),
    }


def main():
    parser = argparse.ArgumentParser(description="Layer 2 Knowledge Graph Operations")
    parser.add_argument("--kb-root", required=True, help="Path to Research Knowledge Base root")
    parser.add_argument("--action", required=True, choices=["search", "browse", "relations", "path", "summary", "neighbors"])
    parser.add_argument("--keyword", help="Search keyword")
    parser.add_argument("--type", help="Node type filter (concept, method, project)")
    parser.add_argument("--node-id", help="Node ID for relations/neighbors")
    parser.add_argument("--node-name", help="Node name (alternative to ID)")
    parser.add_argument("--start", help="Start node ID for path finding")
    parser.add_argument("--end", help="End node ID for path finding")

    args = parser.parse_args()
    graph = load_graph(args.kb_root)

    if args.action == "search":
        if not args.keyword:
            print(json.dumps({"status": "error", "message": "--keyword required for search"}))
            sys.exit(1)
        results = search_nodes(graph, args.keyword, args.type)
        print(json.dumps({"status": "success", "count": len(results), "results": results}, indent=2, default=str))

    elif args.action == "browse":
        if not args.type:
            print(json.dumps({"status": "error", "message": "--type required for browse"}))
            sys.exit(1)
        results = browse_nodes(graph, args.type)
        print(json.dumps({"status": "success", "count": len(results), "results": results}, indent=2, default=str))

    elif args.action == "relations":
        node_id = args.node_id
        if not node_id and args.node_name:
            node = get_node_by_name(graph, args.node_name)
            if node:
                node_id = node["id"]
        if not node_id:
            print(json.dumps({"status": "error", "message": "--node-id or --node-name required"}))
            sys.exit(1)
        rels = get_relationships(graph, node_id)
        node = get_node(graph, node_id)
        print(json.dumps({
            "status": "success",
            "node": node.get("name") if node else "unknown",
            "outgoing_count": len(rels["outgoing"]),
            "incoming_count": len(rels["incoming"]),
            "relationships": rels
        }, indent=2, default=str))

    elif args.action == "neighbors":
        node_id = args.node_id
        if not node_id and args.node_name:
            node = get_node_by_name(graph, args.node_name)
            if node:
                node_id = node["id"]
        if not node_id:
            print(json.dumps({"status": "error", "message": "--node-id or --node-name required"}))
            sys.exit(1)
        neighbors = find_neighbors(graph, node_id)
        print(json.dumps({
            "status": "success",
            "count": len(neighbors),
            "neighbors": neighbors
        }, indent=2, default=str))

    elif args.action == "path":
        if not args.start or not args.end:
            print(json.dumps({"status": "error", "message": "--start and --end required for path"}))
            sys.exit(1)
        path = find_path(graph, args.start, args.end)
        if path:
            # Resolve node names
            if isinstance(path, dict):
                named_path = []
                for nid in path["nodes"]:
                    node = get_node(graph, nid)
                    named_path.append({"id": nid, "name": node["name"] if node else "unknown"})
                path["named_nodes"] = named_path
            print(json.dumps({"status": "success", "path": path}, indent=2, default=str))
        else:
            print(json.dumps({"status": "success", "path": None, "message": "No path found within 2 hops"}, indent=2))

    elif args.action == "summary":
        summary = graph_summary(graph)
        print(json.dumps({"status": "success", "summary": summary}, indent=2))


if __name__ == "__main__":
    main()
