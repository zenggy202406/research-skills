---
name: kb-dream
description: "Memory consolidation for the Research Knowledge Base. Functions like dreaming: tracks cumulative vitality scores for Layer 2 nodes across dream cycles, consolidates high-value knowledge (tags, hints), prunes dormant nodes to cold storage, detects near-duplicates, suggests missing relationships, and proposes mild Layer 1 reshaping based on usage patterns. Incremental: only scans changes since last dream. Use when: 'dream', 'consolidate kb', 'prune kb', 'kb memory', 'clean up Layer 2', 'optimize kb', 'kb dream', 'dormant nodes', 'restore node', 'vitality check', 'check node health'."
metadata:
  version: "2.0.0"
  created: "2026-05-11"
  updated: "2026-05-11"
  depends_on: "kb"
  status: active
---

# KB Dream — Memory Consolidation (v2)

This skill performs sleep-like memory consolidation on the Layer 2 knowledge graph. It uses **cumulative vitality scoring** — each node accumulates vitality over time based on usage and connections, and gradually decays when unused. Dream cycles are **incremental**, scanning only changes since the previous dream.

## Knowledge Base Location

All knowledge base files live at: `C:\Users\hp\Desktop\Research Knowledge Base`

## Conceptual Model

| Cognitive Operation | KB Action |
|---------------------|-----------|
| **Replay** | Scan project activity since last dream for Layer 2 references |
| **Consolidation** | Strengthen high-use nodes: normalize tags, populate hints, suggest relationships |
| **Pruning** | Move low-vitality nodes to recoverable cold storage |
| **Mild reshaping** | Propose gradual Layer 1 updates based on usage concentration, override patterns, and dormant interests |

## Cumulative Vitality Scoring

Unlike a stateless evaluation, vitality accumulates across dream cycles:

### Initialization (when a node first enters Layer 2)

Every new Layer 2 node receives:
- **Baseline**: 1.0 (reflecting recency as fresh knowledge)
- **Connectedness bonus**: `(degree / max_degree) × 0.5` (max 0.5)
- Initial vitality range: **1.0 – 1.5**

**Important**: When adding nodes to Layer 2 via `/kb-health` or `/kb`, also initialize their vitality:
```bash
python "<skill-dir>/scripts/kb_dream.py" --kb-root <kb-path> --action init-node --node-id <ID>
```

### Dream Cycle Deltas

Each dream cycle computes a delta per node:

| Activity | Delta | Condition |
|----------|-------|-----------|
| New project reference | **+0.15** per project | Project file modified since last dream contains a new reference to this node |
| New connection | **+0.10** per relationship | Node's degree increased since last dream |
| No activity | **−0.10** | Neither of the above detected |

The delta is added to the existing vitality: `new_vitality = max(0, old_vitality + delta)`

### Pruning Cutoff

**Default threshold: 0.3** (configurable via `--threshold`).

A node is a pruning candidate when: vitality < threshold AND degree ≤ 1.

With -0.1 decay per cycle, an unused node with initial vitality 1.0 survives ~7 dream cycles before reaching the cutoff.

### History

Each node's vitality record includes a full history of events (initialization, dream cycles, restores), providing an audit trail of how a node's importance evolved.

## Incremental Scanning

The skill maintains `system/dream-log.yaml` tracking when each dream occurred:

```yaml
last_dream: "2026-05-11T14:30:00"
dreams:
  - date: "2026-05-11T14:30:00"
    nodes_analyzed: 45
    nodes_initialized: 3
    deltas_applied: 42
    nodes_pruned: 1
```

On each dream:
1. Read `last_dream` timestamp from dream log
2. Scan project files — only files modified after `last_dream` are checked for new references
3. Compare current state (degree, project refs) against snapshot stored in each node's vitality record
4. **First dream** (no log): bootstraps all nodes, treats everything as new

## Layer 1 Mild Reshaping

Dreaming detects gradual shifts in the researcher's practice and proposes mild, incremental Layer 1 updates. These are **proposals only** — presented in the dream report for the researcher to review. Three signal types:

### 1. Usage Concentration Shifts
When certain concepts consistently accumulate high vitality across multiple projects, the dream proposes adding or strengthening them in the narrative profile. This reflects an organic shift in research focus.

### 2. Override Pattern Detection
When the same Layer 1 rule is overridden in multiple projects (detected from `override-log.yaml` files), the dream proposes softening or revising that rule to better match evolved practice.

### 3. Dormancy-Based Interest Pruning
When concepts mentioned in the narrative profile have gone dormant in Layer 2 (low vitality), the dream proposes gently deprioritizing them. Research interests shift; the profile should reflect that.

**Implementation**: These proposals are generated as structured data by the script and included in the dream report. The LLM reads the report and presents them to the user as gentle suggestions, not commands. At most 1-2 proposals per dream cycle to keep changes gradual.

## Script

Install PyYAML before use: `pip install pyyaml --break-system-packages`

```bash
python "<skill-dir>/scripts/kb_dream.py" --kb-root <kb-path> --action <action> [options]
```

### Actions

| Action | Description |
|--------|-------------|
| `analyze` | Incremental scan since last dream; initialize new nodes; apply vitality deltas |
| `consolidate` | Auto-apply tag normalization and hint population; detect duplicates, verbose defs, co-occurrence |
| `prune` | Move nodes below vitality cutoff to `system/dormant-nodes.yaml` |
| `report` | Generate `system/dream-report-YYYY-MM-DD.md` |
| `restore` | Restore a node from cold storage (re-initializes vitality) |
| `init-node` | Initialize vitality for a single newly added node |
| `full` | Run analyze → consolidate → prune → report; update dream log |

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--threshold` | 0.3 | Vitality cutoff for pruning |
| `--dry-run` | false | For prune: list candidates without moving |
| `--node-id` | — | Required for restore and init-node |

## How to Route Requests

### Quick dream (most common)

User says: "dream", "consolidate my kb", "kb dream"

1. Run the full dream cycle:
   ```bash
   python "<skill-dir>/scripts/kb_dream.py" --kb-root <kb-path> --action full
   ```
2. Read the generated report from `system/dream-report-YYYY-MM-DD.md`
3. Present a concise summary:
   - Dream number, time since last dream
   - Nodes initialized (if any new since last dream)
   - Vitality changes: which nodes gained/lost, any approaching cutoff
   - Auto-applied: tags normalized, hints added
   - Pruned nodes (if any)
4. Present proposals for review:
   - **Near-duplicates** → suggest merge via `/kb-health`
   - **Verbose definitions** → offer to propose tighter versions
   - **Missing relationships** → ask which should be added
   - **Layer 1 proposals** → present gently, at most 1-2 per cycle
5. For approved changes, use existing scripts:
   ```bash
   # Add relationship
   python "<kb-root>/system/kb-skill/scripts/yaml_manager.py" --kb-root <kb-path> --action add-rel --entry '<JSON>'
   # Update state
   python "<kb-root>/system/kb-skill/scripts/update_state.py" --kb-root <kb-path>
   ```
6. Regenerate `field-summary.md` after changes

### Check vitality

User says: "check node health", "vitality report", "how is my kb doing"

1. Run analyze only:
   ```bash
   python "<skill-dir>/scripts/kb_dream.py" --kb-root <kb-path> --action analyze
   ```
2. Present vitality distribution and any nodes approaching cutoff

### Prune check (dry run)

User says: "what's dormant", "pruning candidates"

1. Run prune with dry-run:
   ```bash
   python "<skill-dir>/scripts/kb_dream.py" --kb-root <kb-path> --action prune --dry-run
   ```
2. Present candidates with vitality scores and history

### Restore

User says: "restore CON-015", "bring back [name]"

1. Run restore (re-initializes vitality at baseline):
   ```bash
   python "<skill-dir>/scripts/kb_dream.py" --kb-root <kb-path> --action restore --node-id <ID>
   ```

### Initialize a new node

When adding a node to Layer 2 via `/kb-health`, also run:
```bash
python "<skill-dir>/scripts/kb_dream.py" --kb-root <kb-path> --action init-node --node-id <ID>
```

### View dream history

User says: "dream history", "past reports"
1. List files matching `system/dream-report-*.md`
2. Or read `system/dream-log.yaml` for a compact timeline

## Files Created / Modified

| File | Purpose |
|------|---------|
| `system/usage-metrics.yaml` | Persistent per-node vitality scores and history |
| `system/dream-log.yaml` | Dream timestamps and summary stats |
| `system/dormant-nodes.yaml` | Cold storage with move log |
| `system/dream-report-YYYY-MM-DD.md` | Persistent report per dream cycle |
| `layer2-field/graph.yaml` | Modified during consolidation (tags, hints) and pruning |

## Integration

- **`/kb` and `/kb-health`**: When adding nodes to Layer 2, call `init-node` to set baseline vitality
- **Post-archive**: After archiving a project, run a dream to consolidate newly promoted knowledge
- **Layer 1 updates**: Dream proposes mild changes; actual edits to Layer 1 files are done via `/kb-health`

## Token Efficiency Design

- All scoring is done by Python script — zero LLM calls for analysis
- Incremental scanning skips unmodified files (file mtime check)
- Vitality records are cached in `usage-metrics.yaml`
- Pruning directly reduces graph.yaml token cost
- Tag normalization improves grep accuracy, reducing false-negative follow-up reads
