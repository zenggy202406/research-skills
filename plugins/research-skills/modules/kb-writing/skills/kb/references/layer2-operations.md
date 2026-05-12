# Layer 2 Operations — Field Knowledge Base

## Location

All Layer 2 files live in `layer2-field/`:
- `field-summary.md` — **compact briefing (~40 lines). READ THIS FIRST for any task needing Layer 2 context.**
- `graph.yaml` — the knowledge graph (nodes + relationships + field intelligence)
- `relationship-schema.yaml` — allowed relationship types
- `concepts/` — markdown files for complex concepts
- `methods/` — markdown files for each method/paradigm
- `fundamental-readings/` — foundational texts in developmental psychology (PDFs or preprocessed markdown)
- `fundamental-readings.yaml` — registry of readings with extraction status
- `index.md` — human-readable overview

## Tiered Reading Protocol

**Do not read `graph.yaml` by default.** Use the smallest file that answers the question.

| Tier | File | When to read |
|------|------|-------------|
| 0 | SKILL.md instructions | Always (loaded automatically) |
| 1 | `field-summary.md` | Any task needing Layer 2 context — gaps, constraints, guides, coverage overview |
| 2 | Specific entries via grep | When a task needs detail on a specific concept, method, or field intelligence entry (grep `graph.yaml` by ID or name) |
| 3 | Full `graph.yaml` | Only for browse-all, graph-wide search, or integrity checks |

**"Grep before read" pattern**: When you need a specific entry (e.g., GAP-001, CON-012), grep `graph.yaml` for that ID rather than reading the entire file.

## Node Types

The knowledge graph contains these node types:

| Type | ID prefix | Purpose |
|------|-----------|---------|
| concept | CON-XXX | Domain concepts with definitions, boundaries, relationships |
| method | MET-XXX | Research methods/paradigms with detail files in `methods/` |
| project | PRJ-XXX | Archived Layer 3 projects promoted to Layer 2 |
| gap | GAP-XXX | Known research gaps — what hasn't been studied |
| open_question | OQ-XXX | Debated questions without consensus |
| theoretical_constraint | TC-XXX | Theoretical boundaries on what research can claim |
| methodological_limitation | ML-XXX | Known weaknesses of common methods |
| research_guide | RG-XXX | Practical/theoretical guidance for research design |

The last five types (gap through research_guide) are collectively called **field intelligence** — they guide Layer 3 research decisions.

## Browse the Knowledge Graph

### Browse Concepts
1. Grep `graph.yaml` for `type: concept` or read the concepts section
2. Present a concise list: name, brief definition, and relationship count
3. If the user selects a concept, show full details including all relationships and linked markdown file if it exists

### Browse Methods
1. Grep `graph.yaml` for `type: method` or read the methods section
2. Present a concise list: name, brief definition
3. If the user selects a method, read its markdown file from `methods/` and display

### Browse Project Nodes
1. Grep `graph.yaml` for `type: project`
2. Present: name, summary, key findings, research questions
3. Show relationships to concepts and methods, and to other projects

### Browse Field Intelligence
1. Read `field-summary.md` for an overview of all gaps, open questions, constraints, limitations, and guides
2. If the user wants detail on a specific entry, grep `graph.yaml` by ID (e.g., `GAP-001`)
3. Allow filtering by tag (e.g., "show me all autism-related gaps") — grep `graph.yaml` for the tag within field intelligence sections

### Browse Relationships
1. Read `graph.yaml` and extract all relationships
2. Allow filtering by relationship type, source node, or target node
3. Present as a readable list or narrative

## Search the Knowledge Graph

Support multiple search modes:

- **By name**: Grep node names for a keyword
- **By definition**: Grep definitions and descriptions
- **By relationship**: Find all nodes connected to a given node
- **By type**: List all nodes of a given type
- **By tag**: Grep for a specific tag across all node types
- **Path query**: Find how two nodes are connected (direct or indirect)

Use grep on `graph.yaml` first. Only read the full file for path queries or complex cross-node searches.

## Add a Concept

1. Ask for:
   - Name
   - Definition
   - Conceptual boundaries
   - Light illustrative examples (optional)
   - Tags (flat list, for filtering)
   - Relationships to existing nodes

2. Determine storage:
   - If the concept is short (definition < 100 words, no complex structure) → inline in `graph.yaml`
   - If complex → create a markdown file in `concepts/[concept-name].md`

3. Generate a unique ID: `CON-XXX` (next available number)

4. Validate relationships against `relationship-schema.yaml` — ensure the relationship type is valid for the node type pair.

5. Present the entry for approval, then add to `graph.yaml`.

6. **Regenerate `field-summary.md`** if the change affects coverage stats.

### Concept Markdown Template (for complex concepts)
```markdown
# [Concept Name]

## Definition
[Full definition]

## Conceptual Boundaries
[What this concept is and is not; how it differs from related concepts]

## Key Dimensions / Components
[If applicable, the internal structure of the concept]

## Illustrative Examples
[Minimal, canonical examples]

## Notes
[Optional: historical context, ongoing debates, caveats]
```

## Add a Method / Paradigm

1. Ask for the method details using this template:

```markdown
# [Method Name]

## Description
[What the method/paradigm is and how it works]

## Constructs Measured
[What psychological constructs this method assesses]

## Typical Design
[Standard implementation: participants, procedure, conditions, measures]

## Variants
[Known modifications or adaptations]

## Strengths
[Methodological advantages]

## Limitations
[Known weaknesses or constraints]

## When to Use
[Conditions where this method is appropriate]

## When NOT to Use
[Conditions where this method is inappropriate]
```

2. Generate ID: `MET-XXX` (next available)
3. Save the markdown file to `methods/[method-name].md`
4. Add node to `graph.yaml` with pointer to the file
5. Add relationships to concepts (typically `is_measured_by` from concept to method)
6. **Regenerate `field-summary.md`** if this adds a new method area.

## Add Field Intelligence

Field intelligence entries (gaps, open questions, theoretical constraints, methodological limitations, research guides) are added directly to `graph.yaml`.

### Common fields for all field intelligence types:
- `id`: Use appropriate prefix (GAP-XXX, OQ-XXX, TC-XXX, ML-XXX, RG-XXX)
- `type`: One of `gap`, `open_question`, `theoretical_constraint`, `methodological_limitation`, `research_guide`
- `name`: Short descriptive name
- `statement`: Full description of the entry
- `tags`: Flat list for filtering (e.g., `[autism, methodology, infant]`)
- `sources`: Human-readable source labels (e.g., `["FR-005 Happé", "FR-014 ASD Review"]`)

### Type-specific fields:
- **gap**: `significance` — why this gap matters
- **open_question**: `current_state` — where the debate stands
- **theoretical_constraint**: `implications` — what this means for research design
- **methodological_limitation**: `impact` + `workarounds` — consequences and mitigation strategies
- **research_guide**: `guide_type` (theoretical | practical) — nature of the guidance

### Process:
1. Identify the type and gather required fields
2. Generate the next available ID for that type
3. Present entry for approval
4. Add to `graph.yaml` in the appropriate section
5. **Regenerate `field-summary.md`** — add the one-line summary for the new entry

## Edit a Concept, Method, or Field Intelligence Entry

1. Identify the node by name or ID
2. Grep `graph.yaml` for that ID to read current content (or read markdown file for concepts/methods)
3. Present current content and ask what to change
4. Apply edits after approval
5. If changing relationships, validate against schema
6. **Regenerate `field-summary.md`** if the change affects any summary line

## Add or Edit Relationships

1. Identify source and target nodes
2. Check `relationship-schema.yaml` for valid relationship types between these node types
3. Present valid options and let the user choose
4. Add to `graph.yaml` under the source node's relationships list

## Register a New Relationship Type

1. Ask for:
   - ID (snake_case)
   - Label (human-readable)
   - Description
   - Valid source→target node type pairs

2. Validate that the ID doesn't already exist
3. Present for approval
4. Add to `relationship-schema.yaml`

## Fundamental Readings — Source Material for Layer 2

Fundamental readings are the canonical and foundational texts in developmental psychology that form the evidence base for Layer 2. They include textbook chapters, major review articles, landmark empirical papers, and influential theoretical papers. They serve as the primary material for seeding and expanding the knowledge graph.

### Adding Readings

1. User provides readings placed in `fundamental-readings/`. Two formats are supported:

   **Format A — Raw PDF** (fallback):
   ```
   fundamental-readings/Piaget_1952_Origins_Intelligence.pdf
   ```

   **Format B — Preprocessed markdown** (preferred, 3-5x cheaper in tokens):
   ```
   fundamental-readings/
     Piaget_1952_Origins_Intelligence.pdf          # original (may be kept or removed)
     Piaget_1952_Origins_Intelligence.md           # full text as markdown
     Piaget_1952_Origins_Intelligence_meta.json    # structured metadata
     fig1.png                                      # extracted figures (same folder)
   ```

   **Format detection**: If `fundamental-readings/Name.md` exists (same base name as PDF) → use Format B (read .md, load `_meta.json` for citation info). Otherwise → use Format A (read PDF directly). Broken image links in markdown are expected — use caption text and skip missing files.

2. For each reading, create a registry entry in `fundamental-readings.yaml`:
   ```yaml
   - id: FR-001
     citation: "Piaget, J. (1952). The origins of intelligence in children. International Universities Press."
     file: "fundamental-readings/Piaget_1952_Origins_Intelligence.pdf"
     type: theoretical  # theoretical | review | empirical-landmark | textbook-chapter | methodological
     domain: [cognitive development, constructivism]
     extraction_status: pending  # pending | extracted | updated
     extracted_date: null
     nodes_added: []  # IDs of concepts/methods added from this reading
     relationships_added: 0
     extraction_notes: ""
   ```
3. Name files clearly: `AuthorLastName_Year_ShortTitle` (with `.pdf`, `.md`, or `_meta.json` extension)

### Seeding Layer 2 (Initial Population)

This is a first-time operation to populate Layer 2 with foundational knowledge from the fundamental readings collection.

#### Process

1. User provides an initial set of fundamental readings (review papers, textbook chapters, major theoretical works)
2. Add all readings to the registry with `extraction_status: pending`
3. Process readings in a logical order:
   - **Broad reviews and textbooks first** — these establish the conceptual landscape
   - **Theoretical papers next** — these add depth to specific frameworks
   - **Landmark empirical papers last** — these add methods and concrete findings

4. For each reading, extract:
   - Key concepts defined or discussed → propose as concept nodes
   - Methods/paradigms described → propose as method nodes
   - Relationships between concepts → propose typed relationships
   - Concept-method links → propose `is_measured_by` relationships
   - **Field intelligence**: gaps, open questions, theoretical constraints, methodological limitations, and research guides mentioned or implied by the text

5. After processing a batch, compile the full proposed graph:
   - List all concepts with definitions
   - List all methods with brief descriptions
   - List all proposed relationships
   - List all proposed field intelligence entries
   - Highlight any where Claude is less certain

6. Claude also proposes additional core concepts, methods, and field intelligence that a developmental psychology knowledge base should include, based on the readings' domain

7. Present for user review and apply approved items to `graph.yaml`
8. Create markdown detail files for complex concepts and all methods
9. Update each reading's registry entry: `extraction_status: extracted`, `nodes_added`, `relationships_added`
10. **Regenerate `field-summary.md`** to reflect the new content

### On-Demand Extraction from a New Reading

When the user adds a new fundamental reading and wants it processed:

1. Detect format (markdown preferred over PDF for token efficiency) and read the paper carefully
2. **Compare with existing graph**: Identify what's already covered vs. what's new
3. Extract new knowledge:
   - **New concepts** not yet in the graph → propose as new nodes
   - **Refinements** to existing concepts (new dimensions, boundary conditions, updated definitions) → propose edits to existing nodes/markdown files
   - **New methods** or method variants → propose new method nodes
   - **New relationships** between existing or new nodes → propose with type validation
   - **Challenges or updates** to existing knowledge → flag for user (e.g., "This paper challenges the existing definition of CON-005")
   - **New field intelligence** — gaps, open questions, constraints, limitations, or guides revealed by the text

4. Present all proposals grouped by type (new concepts, edits, new methods, new relationships, field intelligence, challenges)
5. Apply approved changes
6. Update the reading's registry entry
7. **Regenerate `field-summary.md`**

### Batch Update

When the user adds several new readings at once:

1. Add all to registry
2. Process sequentially, accumulating proposals
3. Present a consolidated set of proposed changes (deduplicated — if two readings both suggest the same concept, merge into one proposal)
4. Apply after approval
5. **Regenerate `field-summary.md`**

## On-Demand Update from New Thinking

When the user wants to add knowledge to Layer 2 outside of a reading context:

1. Listen to what they want to add (new concept, new relationship, revised understanding, new field intelligence)
2. Map it to the appropriate operation (add concept, add relationship, edit concept, add field intelligence, etc.)
3. Execute with approval
4. **Regenerate `field-summary.md`** if affected

## Layer 3 → Layer 2 Feedback

When a Layer 3 project is archived or reaches a milestone, it may return feedback to update Layer 2. This is the upward flow in the bidirectional Layer 2↔3 relationship.

### Types of feedback from Layer 3:

- **New gap discovered**: Project work revealed a gap not previously in Layer 2 → add as new GAP entry
- **Gap addressed**: Project partially or fully addressed an existing gap → update the GAP entry's statement or mark with a note
- **Constraint confirmed/refuted**: Project findings support or challenge a theoretical constraint → update TC entry's implications
- **New limitation encountered**: Hands-on use of a method revealed a limitation → add as new ML entry or update existing
- **New open question**: Project raised a question the field hasn't answered → add as new OQ entry
- **Concept refinement**: Deep engagement with a concept revealed new boundaries or dimensions → update concept node
- **Method refinement**: Practical experience with a method → update method markdown file

### Process:

1. During project archival (via kb-health), review what the project learned
2. Identify which findings are generalizable to the field (not project-specific)
3. Propose Layer 2 updates grouped by type
4. Apply after user approval
5. **Regenerate `field-summary.md`**

## Regenerate field-summary.md

Whenever `graph.yaml` is modified (nodes added, edited, or removed), regenerate `field-summary.md`:

1. Read `graph.yaml` (or use grep to count nodes by type)
2. Rebuild the summary with updated counts and one-line entries for each field intelligence item
3. Update the "Last updated" date
4. Write to `layer2-field/field-summary.md`

Keep the format compact (~40 lines). Each field intelligence entry gets one line: `**ID** short name [key tags]`.
