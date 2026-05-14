---
name: kb
description: "Research Knowledge Base daily operations for developmental psychology. Manages projects (create, continue, list), paper workflows (skim, select, deep read, paper network), claim extraction and refinement, argument construction, writing integration, browsing and searching the knowledge graph, and cross-project search. Use when: my research, my project, start a project, continue project, skim papers, select papers, deep read, extract claims, build network, paper connections, build arguments, write literature review, write introduction, browse concepts, search claims, search arguments, cross-project search, Layer 3 work. For first-time setup use /kb-init. For archiving, maintenance, or Layer 1/2 updates use /kb-health."
metadata:
  version: "2.1.0"
  created: "2026-04-18"
  updated: "2026-04-21"
  depends_on: "paper-skimmer, paper-selector, paper-deep-reader, lit-review-generator, intro-writer, docx, xlsx"
  status: active
---

# Research Knowledge Base — Daily Operations

This skill handles day-to-day research workflow within the knowledge base: managing projects, working with papers, extracting and refining claims, building arguments, and writing. For first-time setup, use `/kb-init`. For maintenance, archiving, and Layer 1/2 structural updates, use `/kb-health`.

## Knowledge Base Location

All knowledge base files live at: `C:\Users\hp\Desktop\Research Knowledge Base`

Use bash path: `/sessions/lucid-clever-galileo/mnt/Knowledge Base Manage/Research Knowledge Base`

## Architecture Summary

The knowledge base has three layers:

**Layer 1 — Researcher Model** (Global, Personal, Evolving): The researcher's theoretical preferences, methodological attitudes, reasoning style. Stored in `layer1-researcher/`. Includes the researcher's own publications (`my-publications/`) as primary evidence. Acts as a top-down guiding constraint. Updated after project completion, on-demand, or when new publications are added.

**Layer 2 — Field Knowledge Base** (Global, Structured, Expanding): General developmental psychology knowledge — concepts, methods/paradigms, archived project summaries, and **field intelligence** (gaps, open questions, theoretical constraints, methodological limitations, research guides). Stored as a hybrid YAML graph (`layer2-field/graph.yaml`) plus markdown detail files. Eight node types: concept, method, project, gap, open_question, theoretical_constraint, methodological_limitation, research_guide. The compact entry point is `layer2-field/field-summary.md` (~40 lines) — **read this first** instead of the full graph. Fundamental readings (`fundamental-readings/`) are the source material. Typed relationships defined in `layer2-field/relationship-schema.yaml`.

**Layer 2 Reading Protocol — Do NOT read `graph.yaml` by default:**
- **Tier 1**: Read `field-summary.md` for any task needing Layer 2 context (gaps, constraints, guides, coverage overview)
- **Tier 2**: Grep `graph.yaml` by ID or name for specific entries only when more detail is needed
- **Tier 3**: Read full `graph.yaml` only for browse-all, graph-wide search, or integrity checks

**Layer 3 — Project Knowledge Base** (Local, Dynamic, Write-Ready): Per-project knowledge including curated papers, atomic claims, structured argument units, project-specific concepts, and method instantiations. Stored in `projects/active/[project-name]/` or `projects/archived/[project-name]/`.

## Grounding Policy

When reasoning or writing using this knowledge base:
1. **Layer 3 is primary** — the source of truth for the current project
2. **Layer 2 is supportive** — provides conceptual and methodological background
3. **External knowledge is minimal** — must not override Layer 3
4. Never introduce unsupported claims
5. Maintain clear separation between evidence, interpretation, and speculation
6. When a gap is encountered, flag it clearly as a suggestion and integrate user input

## Helper Scripts

This skill includes three Python scripts in `scripts/` for reliable data operations. Install PyYAML before use (`pip install pyyaml --break-system-packages`).

**`scripts/graph_ops.py`** — Layer 2 graph operations: search nodes, browse by type, find relationships, find paths between nodes, get neighbors, graph summary.
```bash
python "<skill-dir>/scripts/graph_ops.py" --kb-root <kb-path> --action <search|browse|relations|path|summary|neighbors> [options]
```

**`scripts/cross_search.py`** — Cross-project and cross-layer search: search claims, arguments, concepts, methods, papers, or all at once. Supports tag-based filtering.
```bash
python "<skill-dir>/scripts/cross_search.py" --kb-root <kb-path> --mode <claims|arguments|concepts|methods|papers|all> --keyword <keyword> [--tags "tag1,tag2"] [--project <name>]
```

**`scripts/yaml_manager.py`** — YAML file management: generate next IDs, append/update entries with version history, list/get entries with tag filtering, add graph nodes and relationships with schema validation and hint auto-population.
```bash
python "<skill-dir>/scripts/yaml_manager.py" --file <path> --action <next-id|append|update|list|get|add-node|add-rel> [options]
# Tag filtering for list: --filter-tags "tag1,tag2" (AND logic)
```

**`scripts/archive_project.py`** — Project archiving: check project readiness, move from active to archived, generate a project node summary for Layer 2, and identify candidates for Layer 2 promotion.
```bash
python "<skill-dir>/scripts/archive_project.py" --kb-root <kb-path> --project <name> --action <check|move|summarize|promotions>
```

Use these scripts for reliable, consistent data operations rather than manually editing YAML files. They handle ID generation, version history, relationship validation, and safe file operations.

## How to Route Requests

When this skill is triggered, first read `kb-state.yaml` for orientation, then route to the appropriate operation.

### Redirect to Other Skills

If the user's request matches these categories, redirect them:
- **First-time setup** (Layer 1 not initialized, Layer 2 empty) → Tell user to use `/kb-init`
- **Archive a project** → Tell user to use `/kb-health`
- **Update researcher profile / Layer 1 rules** → Tell user to use `/kb-health`
- **Add/edit Layer 2 concepts, methods, or field intelligence** → Tell user to use `/kb-health`
- **KB health check or diagnostics** → Tell user to use `/kb-health`

### Operation Categories (This Skill)

**Project Lifecycle** → Read `references/project-lifecycle.md`
- Create a new project
- List active/archived projects
- Continue working on an existing project

**Paper Workflow** (within a project) → Read `references/paper-workflow.md`
- Skim papers → invoke paper-skimmer, output to project folder
- Select papers → invoke paper-selector with Layer 1 + Layer 2 context
- Deep read papers → invoke paper-deep-reader with claim extraction
- Build paper network → estimate connections, user curates edges
- Manage curated papers and references

**Paper Network** (within a project) → Read `references/network-workflow.md`
- Build network after deep reading (batch init or on-demand addition)
- Query connections, shared concepts, contradictions, bridges, isolated papers
- Network feeds into argument building and writing

**Claim Workflow** (within a project) → Read `references/claim-workflow.md`
- View draft claims extracted from deep reading
- Refine, edit, or reject claims
- Search claims across projects
- Versioning

**Argument Workflow** (within a project) → Read `references/argument-workflow.md`
- Claude proposes argument units from reading and claims
- Review, refine, or reject arguments
- Link arguments to claims and Layer 2 concepts
- Search arguments across projects
- Versioning

**Writing Integration** → Read `references/writing-integration.md`
- Write grounded in Layer 3 argument units
- Invoke lit-review-generator or intro-writer with grounding policy
- Gap detection and flagged suggestions

**Browse & Search** → Read `references/search-operations.md`
- Browse Layer 2 concepts, methods, project nodes, and field intelligence (read-only)
- Browse field intelligence via `field-summary.md` first; grep `graph.yaml` for detail
- Search across all layers and projects
- Find how a concept was used across projects
- Find related claims or arguments

### Context Detection — Use the State Manifest

Before routing, read `kb-state.yaml` at the KB root. This compact file tells you everything about the current state in one read: whether Layer 1 is initialized, how many Layer 2 nodes exist, which projects are active/archived and their stages, claim/argument counts per project. This eliminates the need to scan directories or open multiple files to orient yourself.

After every significant operation (project creation, claim extraction, archiving, Layer 2 updates), run the state manifest updater:
```bash
python "<skill-dir>/scripts/update_state.py" --kb-root <kb-path>
```

### Override Logging

When executing any operation that involves applying Layer 1 rules, and the user chooses to override a rule:
1. Record the override in the project's `override-log.yaml`
2. Include: date, rule category, rule summary, justification, outcome

Do NOT log other decision traces (paper rejections, claim revisions, etc.).

## YAML Schema Quick Reference

### Retrieval Optimization Conventions

These conventions apply across all YAML entries to optimize LLM retrieval:

1. **Inline name hints**: Every cross-reference ID includes a `_hint` field with a human/LLM-readable short name. This eliminates most lookup hops.
2. **Keyword tags**: Every claim, argument, and concept has a `tags` list for fast semantic filtering. Tags are lowercase, concise terms.
3. **Paper IDs**: Papers are referenced by `source_id: PAP-XXX` (for cross-referencing) alongside `source: "Author (Year)"` (for inline readability).

### Paper Reference Entry (in papers-reference.md)

Each paper in `papers-reference.md` follows this format:
```markdown
### PAP-001
**Garcia & Lee (2024)** — Bilingual effects on executive function in preschoolers
- File: `papers/Garcia_Lee_2024_Bilingual_EF/` (or `papers/Garcia_Lee_2024_Bilingual_EF.pdf`)
- Format: markdown (or pdf)
- Journal: Journal of Experimental Child Psychology, 228, 105-121
- Tags: bilingualism, executive function, preschool, inhibitory control
```
Format detection: if `papers/Name.md` exists (same base name as PDF) → `markdown`; if only `papers/Name.pdf` exists → `pdf`. Preprocessed markdown files share the papers folder: `Name.md`, `Name_meta.json`, and image files alongside the original PDF. Broken image links are expected (user may delete irrelevant figures) — use caption text and skip missing files.

### Claim Entry (in claims.yaml)
```yaml
- id: CLM-001
  statement: "The claim text"
  conditions: "Under what conditions this holds"
  population: "Who was studied"
  method_ref: "MET-XXX"
  method_hint: "Go/No-Go task"
  source_id: "PAP-001"
  source: "Garcia & Lee (2024)"
  tags: [bilingualism, inhibitory control, preschool]
  status: draft  # or refined
  notes: ""
  history:
    - version: 1
      date: "2026-04-18"
      statement: "Original statement"
      changed_by: "auto-extracted"
```

### Argument Entry (in arguments.yaml)
```yaml
- id: ARG-001
  conclusion: "The main claim this argument supports"
  tags: [bilingual advantage, executive function, development]
  premises:
    - claim_id: CLM-001
      claim_hint: "Bilingual children showed higher inhibitory control"
      role: "Establishes the main effect"
    - claim_id: CLM-003
      claim_hint: "No difference in working memory"
      role: "Defines boundary condition"
  theoretical_grounding:
    - concept_id: CON-005
      concept_hint: "Executive Function"
      explanation: "How this concept frames the argument"
  assumptions:
    - "Assumption 1"
    - "Assumption 2"
  counterarguments:
    - "Alternative interpretation 1"
    - "Competing explanation"
  scope_conditions:
    - "This argument holds when..."
    - "Does not apply to..."
  notes: ""
  history:
    - version: 1
      date: "2026-04-18"
      conclusion: "Original conclusion"
      changed_by: "Claude-proposed"
```

### Project concepts.yaml Entry
```yaml
- id: PCON-001
  name: "Project-specific concept name"
  base_concept_id: CON-005
  base_concept_hint: "Executive Function"
  tags: [cognitive flexibility, bilingualism]
  refinement: "How this concept is refined or specialized for this project"
  notes: ""
```

### Paper Network Entry (in paper-network.yaml)

```yaml
nodes:
  - id: PAP-001
    short_label: "Garcia2024_EF"
    claim_count: 5
    key_concepts: [executive function, bilingualism, inhibitory control]

edges:
  - source: PAP-001
    target: PAP-003
    type: converging_evidence  # shared_concept | converging_evidence | contradicting_evidence | extends
    relevance: 0.85            # 0.0-1.0
    basis: "Both report inhibitory control advantages in bilingual children"
    shared_claims:
      - source_claim: CLM-002
        source_hint: "Bilingual children showed faster Go/No-Go responses"
        target_claim: CLM-014
        target_hint: "Bilingual advantage in Flanker task accuracy"
        relationship: converging  # converging | contradicting | extending
    shared_concepts: [inhibitory control, bilingual advantage]
    layer2_refs: [CON-005]     # optional Layer 2 concept IDs
    status: approved           # proposed | approved | rejected
    added: "2026-04-20"
    method: batch_init         # batch_init | on_demand
```

### External Links (in external-links.yaml)

Bidirectional linking between KB projects and external folders on the user's computer.

```yaml
# Each entry links to an external folder related to this KB project.
# Types: manuscript, data, analysis, supplementary, other
links:
  - type: manuscript
    path: "C:\\Users\\hp\\Desktop\\My Research\\dissertation-ch3"
    description: "Dissertation Chapter 3 draft folder"
  - type: data
    path: "C:\\Users\\hp\\Desktop\\My Research\\study1-data"
    description: "Raw and processed data for Study 1"
  - type: analysis
    path: "C:\\Users\\hp\\Desktop\\My Research\\r-scripts"
    description: "R analysis scripts"
```

When adding a link, also drop a `kb-link.md` file into the external folder pointing back:
```markdown
# Knowledge Base Link

This folder is linked to a Research Knowledge Base project.

- **KB Project**: [project-name]
- **KB Location**: C:\Users\hp\Desktop\Knowledge Base Manage\Research Knowledge Base
- **Project Path**: projects/active/[project-name]/
- **Link Type**: manuscript
- **Created**: 2026-04-20

To work with the knowledge base, open the KB folder in Cowork and use /kb.
```

### Method Instantiation Entry
```yaml
- id: MINST-001
  name: "Method as used in this project"
  base_method_id: MET-003
  base_method_hint: "Dimensional Change Card Sort"
  tags: [cognitive flexibility, card sort, preschool]
  description: "How the paradigm is used in this project"
  deviations: "Differences from the standard design"
  justification: "Why these deviations were made"
```

### My Publications Entry (in layer1-researcher/my-publications.yaml)
```yaml
- id: PUB-001
  citation: "Zeng, G., et al. (2024). Title. Journal, Vol(Issue), pages."
  file: "my-publications/Zeng_2024_ShortTitle.pdf"
  year: 2024
  topics: [topic1, topic2]
  extraction_status: pending  # pending | extracted | updated
  extracted_date: null
  extraction_notes: ""
```

### Fundamental Reading Entry (in layer2-field/fundamental-readings.yaml)
```yaml
- id: FR-001
  citation: "Piaget, J. (1952). The origins of intelligence in children."
  file: "fundamental-readings/Piaget_1952_Origins_Intelligence.pdf"
  type: theoretical  # theoretical | review | empirical-landmark | textbook-chapter | methodological
  domain: [cognitive development, constructivism]
  extraction_status: pending  # pending | extracted | updated
  extracted_date: null
  nodes_added: []
  relationships_added: 0
  extraction_notes: ""
```
