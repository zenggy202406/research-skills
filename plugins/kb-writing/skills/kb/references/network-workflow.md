# Paper Network Workflow (Within a Project)

The paper network is a graph where nodes are deep-read papers and edges represent meaningful connections between them, grounded in extracted claims and key concepts. It sits between deep reading and argument building in the project pipeline:

**Skim → Select → Deep Read → Network Estimation → Claim Refinement → Argument Building → Writing**

The network serves two purposes:
1. **Discovery** — reveals clusters, bridges, and gaps across the curated literature
2. **Retrieval** — when building arguments or writing, quickly find which papers speak to each other and why

## When to Build the Network

### Batch Initialization (Project Start)

After the initial batch of papers has been deep-read and claims extracted:

1. Read the project's `claims.yaml` (all claims across all deep-read papers)
2. Read `papers-reference.md` for the full paper list
3. Run pairwise relevance estimation across all papers (see Estimation Process below)
4. Present candidate edges to the user for curation
5. Save approved edges to `paper-network.yaml`

### On-Demand Addition (Later in Project)

When the user adds a new paper later in the project:

1. Deep-read the new paper and extract claims (as normal)
2. Run relevance estimation between the new paper and all existing network nodes only
3. Present candidate edges for curation
4. Append approved edges to `paper-network.yaml`

## File: paper-network.yaml

Located at: `projects/active/[project-name]/paper-network.yaml`

```yaml
# Paper Network — [project name]
# Nodes: deep-read papers with extracted claims
# Edges: researcher-approved connections grounded in claims and concepts

nodes:
  - id: PAP-001
    short_label: "Garcia2024_EF"
    claim_count: 5          # number of claims extracted from this paper
    key_concepts: [executive function, bilingualism, inhibitory control]

edges:
  - source: PAP-001
    target: PAP-003
    type: converging_evidence
    relevance: 0.85
    basis: "Both report inhibitory control advantages in bilingual children using different paradigms"
    shared_claims:
      - source_claim: CLM-002
        source_hint: "Bilingual children showed faster Go/No-Go responses"
        target_claim: CLM-014
        target_hint: "Bilingual advantage in Flanker task accuracy"
        relationship: converging  # converging | contradicting | extending
    shared_concepts: [inhibitory control, bilingual advantage]
    layer2_refs: [CON-005]     # optional Layer 2 concept IDs if they exist
    status: approved           # proposed | approved | rejected
    added: "2026-04-20"
    method: batch_init         # batch_init | on_demand
```

### Node Fields

| Field | Description |
|-------|-------------|
| `id` | PAP-XXX from papers-reference.md |
| `short_label` | Compact display label (Author + Year + keyword) |
| `claim_count` | Total claims extracted from this paper |
| `key_concepts` | 3-5 most central concepts from this paper's claims |

### Edge Fields

| Field | Description |
|-------|-------------|
| `source`, `target` | PAP-XXX IDs of connected papers |
| `type` | One of: `shared_concept`, `converging_evidence`, `contradicting_evidence`, `extends` |
| `relevance` | 0.0-1.0 score (see Relevance Scale below) |
| `basis` | One-sentence human-readable description of why these papers connect |
| `shared_claims` | List of specific claim pairs that create the connection |
| `shared_concepts` | Concept keywords shared between the papers |
| `layer2_refs` | Optional Layer 2 concept IDs if the shared concepts exist in the field graph |
| `status` | `proposed` (awaiting curation), `approved` (user confirmed), `rejected` (user declined) |
| `added` | Date the edge was created |
| `method` | `batch_init` or `on_demand` |

### Edge Types

- **`shared_concept`** — Both papers substantively engage the same construct. Not just citing it in passing — the construct is central to their research questions or findings.
- **`converging_evidence`** — Different methods, samples, or designs reaching compatible conclusions about the same phenomenon. The strongest type for argument building.
- **`contradicting_evidence`** — Findings in tension or opposite directions. Important for identifying debates, boundary conditions, and gaps.
- **`extends`** — One paper directly builds on the other's method, sample, or finding. Indicates intellectual lineage.

### Relevance Scale

| Score | Label | Meaning |
|-------|-------|---------|
| 0.90+ | Core | Directly comparable findings — same construct, similar population, strong methodological overlap |
| 0.70-0.89 | Strong | Shared framework or method, closely related findings, clear argumentative link |
| 0.50-0.69 | Moderate | Shared broad topic, indirect relevance, useful as background but not central |
| < 0.50 | Weak | Not proposed as an edge, unless `contradicting_evidence` (always flagged regardless of score) |

## Relevance Estimation Process

### Input

For each pair of deep-read papers (Paper A and Paper B):
1. All claims from Paper A (from `claims.yaml`, filtered by `source_id`)
2. All claims from Paper B
3. Key concepts from both papers' claims (from `tags` fields)

### Estimation Steps

1. **Concept overlap**: Count shared tags/concepts across claims. Weight by specificity — "pupil dilation to emotional faces in infants" > "infant development"
2. **Claim alignment**: For each claim in Paper A, check if any claim in Paper B addresses the same phenomenon. Score by:
   - Same construct measured? (+0.3)
   - Same population/age range? (+0.2)
   - Compatible or contradictory findings? (+0.2 for either — both are informative)
   - Same or similar method? (+0.1)
   - Same theoretical framework invoked? (+0.2)
3. **Aggregate**: Average across all claim pairs, weighted by the number of aligning claims
4. **Type assignment**: Based on claim pair relationships:
   - Mostly compatible findings → `converging_evidence`
   - Mostly conflicting findings → `contradicting_evidence`
   - One paper cites or builds on the other → `extends`
   - Conceptual overlap but no direct empirical link → `shared_concept`

### Output for User Curation

Present candidate edges sorted by relevance score, grouped by type. For each:

```
PAP-001 (Garcia2024) ←→ PAP-003 (Lee2023)
  Relevance: 0.85 (Strong)
  Suggested type: converging_evidence
  Basis: Both report inhibitory control advantages in bilingual children
  Shared claims:
    CLM-002 ↔ CLM-014: Both measure inhibitory control, converging findings
    CLM-004 ↔ CLM-016: Both report no working memory difference, converging null
  Shared concepts: inhibitory control, bilingual advantage, preschool
  ─────────────────────────────────
  Your decision: [approve / reject / reclassify]
```

Use AskUserQuestion to present edges in manageable batches (5-8 at a time). For each edge, the user can:
- **Approve** — edge goes into the network as-is
- **Reject** — edge is saved with `status: rejected` (not shown in future queries but preserved for audit)
- **Reclassify** — change the edge type (e.g., from `shared_concept` to `converging_evidence`)
- **Edit basis** — refine the description

## Using the Network

### During Argument Building

When building arguments (see `argument-workflow.md`), consult the paper network to:
- Find papers with `converging_evidence` edges — these are natural candidates for multi-source argument premises
- Find `contradicting_evidence` edges — these inform counterargument sections
- Identify isolated papers (few or no connections) — may need additional literature or may serve a unique role

### During Writing

When writing literature reviews or introductions (via `lit-review-generator` or `intro-writer`):
- Use network clusters to organize thematic sections
- Use `extends` edges to trace the development of a line of research
- Use `contradicting_evidence` edges to frame debates

### Searching the Network

Query the network for:
- **All connections of a paper**: "What connects to PAP-005?"
- **Papers sharing a concept**: "Which papers share 'social motivation'?"
- **Contradictions**: "Show me all contradicting_evidence edges"
- **Bridge papers**: Papers that connect otherwise separate clusters
- **Isolated papers**: Papers with no approved edges

## Integration with Layer 2

When a shared concept on an edge matches a Layer 2 concept (from `graph.yaml`), record the `layer2_refs`. This creates a bridge:
- Searching a Layer 2 concept can surface all project papers connected through that concept
- The network makes Layer 2 concepts actionable within a specific project's literature
