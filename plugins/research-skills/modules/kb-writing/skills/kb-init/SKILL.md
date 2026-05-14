---
name: kb-init
description: "First-time initialization of the Research Knowledge Base. Handles Layer 1 Researcher Model setup (structured interview + extraction from user's own publications), Layer 2 Field Knowledge Base seeding (from fundamental readings), and folder structure verification. Supports both raw PDF and preprocessed markdown input. Use when: initialize kb, set up knowledge base, seed Layer 2, initialize Layer 1, researcher profile setup, add my publications, add fundamental readings."
metadata:
  version: "2.1.0"
  created: "2026-04-19"
  updated: "2026-04-23"
  depends_on: "xlsx"
  status: active
---

# KB Initialization Skill

This skill handles first-time setup of the Research Knowledge Base. It is separate from daily operations (`/kb`) and maintenance (`/kb-health`).

## Knowledge Base Location

All knowledge base files live at: `C:\Users\hp\Desktop\Research Knowledge Base`

Use bash path: `/sessions/lucid-clever-galileo/mnt/Knowledge Base Manage/Research Knowledge Base`

## Shared Resources

Scripts and reference files are in the main kb-skill directory:
- Scripts: `system/kb-skill/scripts/`
- References: `system/kb-skill/references/`

Install PyYAML before using scripts: `pip install pyyaml --break-system-packages`

## When to Trigger

Check `kb-state.yaml` first. This skill is needed when:
- `layer1.initialized` is `false` → Run Layer 1 setup
- `layer2.total_nodes` is `0` → Run Layer 2 seeding
- The KB folder structure is missing or incomplete → Run folder verification

If both Layer 1 and Layer 2 are initialized, redirect the user to `/kb` for daily operations or `/kb-health` for updates.

## Reading Format Detection

Publications and fundamental readings can be stored as raw PDFs or preprocessed markdown. **Preprocessed markdown is preferred** (3-5x cheaper in tokens).

**Format A — Raw PDF** (fallback):
```
folder/AuthorLastName_Year_ShortTitle.pdf
```

**Format B — Preprocessed markdown** (preferred):
```
folder/
  AuthorLastName_Year_ShortTitle.pdf          # original (may be kept or removed)
  AuthorLastName_Year_ShortTitle.md           # full text as markdown
  AuthorLastName_Year_ShortTitle_meta.json    # structured metadata (title, authors, year, journal, etc.)
  fig1.png                                    # extracted figures (same folder)
```

**How to detect**: If `folder/Name.md` exists (same base name as PDF) → use Format B (read .md, load `_meta.json` for citation info). Otherwise → use Format A (read PDF directly).

**Broken image links**: The user may delete irrelevant figure files. When an in-text image link fails (file not found), use the caption text and skip the missing file.

## Operations

### 1. Verify KB Folder Structure

Before any initialization, ensure the KB has the expected structure:

```
Research Knowledge Base/
├── kb-state.yaml
├── system/
│   ├── kb-config.yaml
│   └── kb-skill/ (shared scripts + references)
├── layer1-researcher/
│   ├── narrative-profile.md
│   ├── override-log.yaml
│   ├── my-publications.yaml
│   ├── my-publications/
│   └── rules/
├── layer2-field/
│   ├── field-summary.md          # compact ~40-line briefing — READ FIRST for Layer 2 context
│   ├── graph.yaml                # full knowledge graph (concepts, methods, field intelligence)
│   ├── relationship-schema.yaml
│   ├── fundamental-readings.yaml
│   ├── fundamental-readings/
│   ├── index.md
│   ├── concepts/
│   └── methods/
└── projects/
    ├── active/
    └── archived/
```

Create any missing directories or files.

### 2. Initialize Layer 1 — Researcher Model

Read `system/kb-skill/references/layer1-operations.md` for the full protocol.

Layer 1 initialization uses **two complementary sources**:

#### Source A: The User's Own Publications
The researcher's publications are the strongest evidence for their researcher model. If the user has publications available:

1. Ask the user to provide their publications (placed in `layer1-researcher/my-publications/`)
2. Detect format for each publication (see Reading Format Detection above)
3. Register each in `my-publications.yaml` with `extraction_status: pending`
4. Process chronologically (oldest first) to capture evolution
5. For each publication, extract evidence of:
   - **Writing style**: prose patterns, argument structure, hedging, citation integration
   - **Reasoning style**: argument construction, handling of competing explanations, causal language
   - **Theoretical orientation**: frameworks invoked, level of explanation preferred
   - **Methodological preferences**: designs chosen, statistical approaches, limitations framed
   - **Interpretation patterns**: how findings are discussed, null results handled, generalization degree

6. After processing all publications, synthesize patterns and note any evolution over time

#### Source B: Structured Interview
Conduct the 3-part interview (see layer1-operations.md):
1. **Narrative Profile** — informed by publication analysis if available → write `narrative-profile.md`
2. **Categorized Rules** — for 6 categories, establish rules grounded in both self-report and publication evidence → write `rules/[category].md`
3. **Cross-Category Review** — check consistency

When publications are available, the interview becomes a **validation and refinement** step rather than the sole source. Present extracted patterns and ask the user to confirm, adjust, or add nuance.

### 3. Seed Layer 2 — Field Knowledge Base

Read `system/kb-skill/references/layer2-operations.md`, specifically the "Fundamental Readings" section.

Layer 2 seeding uses **fundamental readings** — canonical texts in developmental psychology:

1. Ask the user to provide foundational texts (review papers, textbook chapters, major theoretical works)
2. Place files in `layer2-field/fundamental-readings/`
3. Detect format for each reading (see Reading Format Detection above)
4. Register each in `fundamental-readings.yaml` with type and domain tags
5. Process in order: broad reviews → theoretical papers → landmark empirical papers
6. For each reading, extract concepts, methods, relationships, and **field intelligence** (gaps, open questions, theoretical constraints, methodological limitations, research guides)
7. Claude also proposes additional core concepts and field intelligence entries the field KB should include
8. Compile and present the full proposed graph for review
9. Apply approved items using `yaml_manager.py`
10. Create markdown detail files for complex concepts and all methods
11. Update each reading's registry entry

```bash
# Add nodes to graph
python "system/kb-skill/scripts/yaml_manager.py" --kb-root <kb-path> --action add-node --entry '<JSON>'

# Add relationships
python "system/kb-skill/scripts/yaml_manager.py" --kb-root <kb-path> --action add-rel --source-id <id> --rel-type <type> --target-id <id>

# Update state after seeding
python "system/kb-skill/scripts/update_state.py" --kb-root <kb-path>
```

### 4. Post-Initialization

After both Layer 1 and Layer 2 are initialized:
1. Generate `layer2-field/field-summary.md` — the compact ~40-line briefing with concept/method counts and one-line entries for each field intelligence item (see layer2-operations.md "Regenerate field-summary.md")
2. Run `update_state.py` to refresh `kb-state.yaml`
3. Inform the user that the KB is ready
3. Suggest next steps:
   - Create their first project using `/kb`
   - Add more publications or readings over time using `/kb-health`
