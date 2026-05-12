# Project Lifecycle Operations

## Create a New Project

1. Ask the user for:
   - Project name (short, kebab-case for folder name, e.g., "ef-bilingualism-preschoolers")
   - A description of the research idea, questions, background, and aims
   - Whether the idea is concrete or vague (this determines the workflow)
   - **External folders** (optional): paths to folders on their computer where this project's other files live (manuscripts, data, analysis scripts, etc.)

2. Create the project folder structure:
   ```
   projects/active/[project-name]/
   ├── overview.md
   ├── external-links.yaml
   ├── progress-summary.md
   ├── papers/
   ├── papers-reference.md
   ├── claims.yaml
   ├── arguments.yaml
   ├── paper-network.yaml
   ├── concepts.yaml
   ├── method-instantiations.yaml
   ├── competing-explanations.md
   └── override-log.yaml
   ```

3. Draft `overview.md` collaboratively with the user using this template:

   ```markdown
   # [Project Title]

   ## Research Idea
   <!-- What is the core idea? What sparked it? -->

   ## Motivation
   <!-- Why does this matter? What gap does it address? -->

   ## Research Questions
   <!-- Numbered list of specific research questions, or exploratory directions if vague -->
   1. ...

   ## Background Context
   <!-- Key theoretical and empirical context -->

   ## Aims and Expected Contributions
   <!-- What will this project contribute? -->

   ## Relevance Notes
   <!-- How does this connect to other projects or broader research agenda? -->

   ## External Locations
   <!-- Folders on your computer linked to this KB project. Kept in sync with external-links.yaml. -->
   <!-- e.g., Manuscript: C:\Users\hp\Desktop\..., Data: C:\Users\hp\Desktop\... -->
   ```

   Include:
   - Research idea and motivation
   - Research questions (if concrete) or exploratory directions (if vague)
   - Background context
   - Aims and expected contributions
   - Relevance notes (for future cross-project assessment)

4. Initialize `progress-summary.md` with this template:

   ```markdown
   # Progress Summary — [Project Name]

   ## Current Stage
   <!-- e.g., paper skimming, claim extraction, argument building, writing -->

   ## Key Decisions Made
   <!-- Important choices and their rationale, chronological -->

   ## Open Questions
   <!-- Unresolved issues, uncertainties, pending decisions -->

   ## Next Steps
   <!-- What needs to happen next -->
   ```

5. Initialize `competing-explanations.md` with this template:

   ```markdown
   # Competing Explanations — [Project Name]

   ## Overview
   <!-- Brief description of the phenomenon and why multiple explanations exist -->

   ## Explanation 1: [Name]
   <!-- Description, key evidence, strengths, weaknesses -->

   ## Explanation 2: [Name]
   <!-- Description, key evidence, strengths, weaknesses -->

   ## Synthesis
   <!-- How do these explanations relate? Are they complementary or mutually exclusive? -->

   ## Implications for This Project
   <!-- How does this competition affect our research questions and argument construction? -->
   ```

6. Initialize `external-links.yaml` and set up bidirectional linking:

   ```yaml
   # External folders on the user's computer linked to this KB project.
   # Types: manuscript, data, analysis, supplementary, other
   links: []
   #  - type: manuscript
   #    path: "C:\\Users\\hp\\Desktop\\My Research\\project-name\\writing"
   #    description: "Dissertation chapter draft"
   #  - type: data
   #    path: "C:\\Users\\hp\\Desktop\\My Research\\project-name\\data"
   #    description: "Raw and processed data"
   ```

   If the user provided external folder paths:
   a. Add each as a typed entry in `external-links.yaml`
   b. For each linked folder, **create a `kb-link.md` file** inside that folder:

   ```markdown
   # Knowledge Base Link

   This folder is linked to a Research Knowledge Base project.

   - **KB Project**: [project-name]
   - **KB Location**: C:\Users\hp\Desktop\Knowledge Base Manage\Research Knowledge Base
   - **Project Path**: projects/active/[project-name]/
   - **Link Type**: [manuscript/data/analysis/etc.]
   - **Created**: [date]

   To work with the knowledge base, open the KB folder in Cowork and use /kb.
   ```

   If no external folders provided, initialize with empty `links: []` — they can add links later.

   External links can also be added or updated at any time during the project by editing `external-links.yaml` and dropping a new `kb-link.md` into the target folder.

7. Initialize empty YAML files with commented examples (same format as the schema in SKILL.md).

8. If the idea is vague, suggest starting with paper skimming to build a progress summary and sharpen the research questions iteratively.

9. If the idea is concrete, suggest the typical workflow: skim → select → deep read → build paper network → extract/refine claims → build arguments → write.

## List Projects

Read `projects/active/` and `projects/archived/` directories. For each project, read `overview.md` and `external-links.yaml` to extract the title, research questions, status, and linked external folders. Present as a concise summary including external folder paths if set.

## Continue a Project

1. Identify which project the user wants to work on (ask if ambiguous).
2. Read the project's `overview.md`, `external-links.yaml`, `claims.yaml`, and `arguments.yaml` to understand current state.
3. If `external-links.yaml` has entries, mention the linked folders so the user knows where their external files are.
4. Assess what stage the project is in:
   - No papers yet → suggest skimming
   - Papers skimmed but not selected → suggest selection
   - Papers selected but not deeply read → suggest deep reading
   - Papers deeply read but no paper network → suggest building paper network
   - Claims extracted but no arguments → suggest claim refinement then argument construction
   - Arguments built → suggest writing
5. Present the assessment and ask what the user wants to do next.

## Archive a Project

Archiving is a multi-step process. Use the `scripts/archive_project.py` helper for Steps 2-4.

### Step 1: Confirm Archiving
Ask the user to confirm they want to archive the project.

### Step 2: Check Project and Move to Archived

First, check the project's readiness:
```bash
python "<skill-dir>/scripts/archive_project.py" --kb-root <kb-path> --project <name> --action check
```
Present the contents summary to the user — this shows what's in the project and helps confirm nothing is missing.

Then move:
```bash
python "<skill-dir>/scripts/archive_project.py" --kb-root <kb-path> --project <name> --action move
```

After moving, update any `kb-link.md` files in linked external folders:
- Read the project's `external-links.yaml`
- For each linked folder, update the `kb-link.md` to reflect `projects/archived/[project-name]/` instead of `projects/active/[project-name]/`

### Step 3: Create Project Node in Layer 2

Generate a project node summary:
```bash
python "<skill-dir>/scripts/archive_project.py" --kb-root <kb-path> --project <name> --action summarize
```

This produces a draft project node with:
- Auto-generated ID (PRJ-XXX)
- Summary, key findings, research questions extracted from project files
- Relationships to Layer 2 concepts and methods based on project concepts and method instantiations

**Important**: The auto-generated summary is a starting point. Review it yourself and improve:
- Write a substantive summary that captures the project's contributions (not just "N claims and M arguments")
- Add key findings that represent the most important conclusions
- Ensure research questions are accurately captured
- Verify all relationships are correct

Present the improved node to the user for approval. Then add to graph.yaml using:
```bash
python "<skill-dir>/scripts/yaml_manager.py" --kb-root <kb-path> --action add-node --entry '<JSON of approved node>'
```

### Step 4: Propose Layer 2 Promotions

Identify candidates:
```bash
python "<skill-dir>/scripts/archive_project.py" --kb-root <kb-path> --project <name> --action promotions
```

This identifies:
- Novel project concepts (no Layer 2 equivalent) that may be generalizable
- Method variants with notable deviations worth adding to Layer 2
- Whether refined claims might serve as canonical findings in Layer 2 concept entries

For each candidate, present to the user with:
- What would be added to Layer 2
- Why it's generalizable (not just project-specific)
- Where it would connect in the graph

Apply approved promotions using `yaml_manager.py`.

### Step 5: Trigger Layer 1 Reflection

Read `references/layer1-operations.md` for the post-project reflection workflow. This reviews:

1. **The project's override log** (`override-log.yaml`): For each override, assess whether the rule needs updating or if it was a justified exception.

2. **The project's trajectory**: What theoretical choices were made? What interpretive stances were taken? Were there new methodological preferences?

3. **Propose updates**: Specific changes to the narrative profile or categorized rules, with evidence from the project.

4. **Apply after approval**: Only update Layer 1 files after the user confirms each change.
