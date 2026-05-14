# Paper Workflow (Within a Project)

All paper operations happen within the context of an active project. Ensure a project is selected before proceeding.

**Full pipeline: Skim → Select → Deep Read → Build Paper Network → Claim Refinement → Argument Building → Writing**

## Skim Papers

Invoke the `paper-skimmer` skill with project-aware configuration:

1. Identify the target project folder: `projects/active/[project-name]/`
2. The user provides papers (PDFs uploaded or paths)
3. Invoke paper-skimmer, directing output to the project's `skimmed-papers.xlsx`
4. After skimming, update `progress-summary.md` with a synthesis of what was found across all skimmed papers — the broad landscape of the research area, key themes, and gaps noticed

### Integration with Layer 1
Before skimming, read `layer1-researcher/rules/literature-selection.md`. Use these rules to guide what the skimmer prioritizes and highlights.

## Select Papers

Invoke the `paper-selector` skill with knowledge base context:

1. Read the project's `skimmed-papers.xlsx`
2. Read `layer1-researcher/rules/literature-selection.md` for selection preferences
3. Read `layer2-field/graph.yaml` to identify relevant concepts and methods
4. Read the project's `overview.md` for research questions and aims
5. Invoke paper-selector, providing this context to enhance relevance scoring:
   - Layer 1 rules influence what counts as "relevant" and "high quality"
   - Layer 2 concepts help identify papers that connect to the broader field knowledge
   - Project overview provides the specific research question for alignment scoring

6. After selection, copy selected papers to `projects/active/[project-name]/papers/` with clear naming
7. Update `papers-reference.md` with a reference list using the paper ID format:
   ```markdown
   ### PAP-001
   **Garcia & Lee (2024)** — Bilingual effects on executive function in preschoolers
   - File: `papers/Garcia_Lee_2024_Bilingual_EF.pdf`
   - Format: pdf
   - Journal: Journal of Experimental Child Psychology, 228, 105-121
   - Tags: bilingualism, executive function, preschool, inhibitory control
   ```
   Each paper gets a sequential PAP-XXX ID. Include the filename, journal info, and keyword tags.

### Paper Storage Formats

Papers can be stored in two formats. **Preprocessed markdown is strongly preferred** for token efficiency (3-5x cheaper to read than PDF).

**Format A — Raw PDF** (fallback):
```
papers/Garcia_Lee_2024_Bilingual_EF.pdf
```

**Format B — Preprocessed** (preferred):
All files share the same folder. The markdown and metadata files derive their names from the original PDF filename.
```
papers/
  Garcia_Lee_2024_Bilingual_EF.pdf          # original (may be kept or removed)
  Garcia_Lee_2024_Bilingual_EF.md           # full text as markdown
  Garcia_Lee_2024_Bilingual_EF_meta.json    # structured metadata
  fig1.png                                  # extracted figures, same folder
  fig2.png
  table1.png
```

**metadata.json schema** (`OriginalName_meta.json`):
```json
{
  "title": "Bilingual effects on executive function in preschoolers",
  "authors": ["Garcia, A.", "Lee, B."],
  "year": 2024,
  "journal": "Journal of Experimental Child Psychology",
  "volume": "228",
  "pages": "105-121",
  "doi": "10.1016/j.jecp.2024.xxxxx",
  "keywords": ["bilingualism", "executive function", "preschool"]
}
```

**content.md conventions:**
- Section headings as markdown headings (`## Introduction`, `## Methods`, etc.)
- Tables as markdown tables when possible; complex tables as image references
- Figure references link to image files in the same folder (e.g., `![Figure 1: Caption](fig1.png)`)
- **Broken image links are expected.** The user may delete irrelevant figure files. When an in-text image link fails (file not found), skip it silently — the caption text is still usable context. Only load an image file when it exists AND is needed for claim extraction or closer inspection.
- References section may be omitted or kept at the end
- No page numbers, headers, footers, or journal boilerplate

**How skills detect format:**
- If `papers/Name.md` exists (same base name as a PDF) → use Format B (read .md, load images only when needed and they exist)
- If only `papers/Name.pdf` exists → use Format A (read PDF directly)
- papers-reference.md `Format` field records which format: `pdf` or `markdown`

## Deep Read Papers

Invoke the `paper-deep-reader` skill with claim extraction:

1. Identify which papers to read deeply (from `papers/` folder)
2. Detect format for each paper:
   - **Format B (markdown)**: Read `Name.md` first. Read `Name_meta.json` for citation info. Only load image files from the same folder when specifically needed for claim extraction AND the file exists. If an in-text image link points to a deleted file, use the caption text and move on.
   - **Format A (PDF)**: Read PDF directly as before.
3. Read Layer 1 rules that apply during reading:
   - `rules/interpretation.md` — guides how findings are interpreted
   - `rules/method-evaluation.md` — guides quality assessment
   - `rules/research-evaluation.md` — guides overall evaluation
4. Read Layer 2 concepts relevant to the paper's topic (from `graph.yaml`)
5. Invoke paper-deep-reader for each paper

### Claim Extraction During Deep Reading

After (or during) deep reading of each paper, extract draft claims:

1. Identify empirical findings, key results, and notable conclusions
2. For each, formulate a draft claim entry:
   ```yaml
   - id: CLM-XXX  # next available
     statement: "Clear, atomic statement of the finding"
     conditions: "Under what conditions (e.g., age range, context)"
     population: "Who was studied"
     method_ref: "MET-XXX"
     method_hint: "Short name of the method (e.g., Go/No-Go task)"
     source_id: "PAP-XXX"
     source: "Author (Year)"
     tags: [keyword1, keyword2, keyword3]
     status: draft
     notes: "Any extraction notes"
     history:
       - version: 1
         date: "[today]"
         statement: "[same as above]"
         changed_by: "auto-extracted"
   ```
   - **source_id**: The PAP-XXX ID from `papers-reference.md`. Enables cross-referencing.
   - **source**: Human-readable "Author (Year)" for inline readability.
   - **method_hint**: Short name so readers don't need to look up the MET-XXX ID.
   - **tags**: 2-5 lowercase keyword tags for semantic filtering and search.

3. Append draft claims to the project's `claims.yaml`
4. Notify the user that draft claims have been extracted and are ready for review

### Integration Notes

- Deep reading summaries from paper-deep-reader are stored as per that skill's normal output
- Claims extracted here feed into the network estimation and claim refinement workflows
- If a paper introduces a concept not yet in Layer 2, note it for potential future addition

## Build Paper Network

**Trigger**: After all initial papers have been deep-read and claims extracted. See `network-workflow.md` for full details.

This step creates a graph of connections between curated papers, grounded in their extracted claims and key concepts. The graph supports discovery (clusters, bridges, gaps) and retrieval (finding related papers during argument building and writing).

### Batch Initialization (after initial deep reading)

1. Read `claims.yaml` — all claims across all deep-read papers
2. Read `papers-reference.md` for paper metadata and tags
3. For each pair of papers, estimate relevance based on:
   - Shared concepts (weighted by specificity)
   - Claim alignment (same construct, population, method, framework)
   - Compatibility or contradiction of findings
4. Present candidate edges to the user sorted by relevance, grouped by type
5. User approves, rejects, or reclassifies each edge
6. Save to `paper-network.yaml`

### On-Demand Addition (later in project)

When a new paper is added later:
1. Deep-read and extract claims as normal
2. Estimate connections only against existing network nodes
3. Present new candidate edges for user curation
4. Append approved edges to `paper-network.yaml`

### Network Queries

Use `network_ops.py` script for querying:
```bash
python "<kb-root>/system/scripts/network_ops.py" --project <project-path> --action <connections|concept|contradictions|bridges|isolated|summary> [options]
```

## Manage Curated Papers

- **Rename**: Help the user rename papers in `papers/` for efficient retrieval (e.g., "Author_Year_ShortTitle.pdf")
- **Update references**: Keep `papers-reference.md` in sync with the papers folder
- **Remove**: If a paper is later deemed irrelevant, remove from `papers/` and update references. Also remove the corresponding node and edges from `paper-network.yaml`.
