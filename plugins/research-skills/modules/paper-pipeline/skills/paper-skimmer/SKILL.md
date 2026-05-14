---
name: paper-skimmer
description: "Quick-scan academic papers and extract structured information into a per-project Excel spreadsheet, integrated with the Research Knowledge Base. Use this skill whenever the user wants to skim, scan, extract key info from, or catalog a research paper — whether uploaded as a PDF, pasted as text, or referenced by content in the conversation. Also trigger when the user mentions adding a paper to their literature spreadsheet, building a reading log, or organizing papers for a project. Handles both single papers and batches. The output is always an .xlsx file with one row per paper, maintained per named project. When a Knowledge Base project is active, outputs go to the project folder and Layer 1 literature selection rules guide the skimming."
---

# Paper Skimmer

Quickly extract structured information from empirical research papers and organize it into a per-project Excel spreadsheet. Integrates with the Research Knowledge Base when a project context is available.

---

## Trigger Conditions

### Trigger Keywords

**English:** skim paper, skim this, scan paper, extract paper info, catalog paper, quick read, quick scan, add to spreadsheet, add to my project, add paper, paper extraction, reading log, organize papers, paper summary, summarize this paper, what does this paper say, log this paper, process these papers, batch skim, skim these PDFs, extract from paper, paper to spreadsheet, build literature spreadsheet, paper database, collect papers

**中文:** 略讀論文, 快速掃描, 提取論文資訊, 加入專案, 論文整理, 建立文獻表, 論文目錄, 掃描這篇, 加到試算表, 論文摘錄

### Auto-Activation Conditions

This skill should activate automatically when:
1. **User uploads a PDF** and says anything like "skim," "scan," "extract," "what's this about," "add this to my project," or "summarize"
2. **User pastes academic text** (identifiable by abstract, methodology, references sections) and asks for extraction or summary
3. **User mentions a project name** with a paper — e.g., "add this to my teacher-retention project"
4. **User has multiple PDFs** and wants to process them — e.g., "I have 10 papers to go through"
5. **User asks to build or update a literature spreadsheet** for any project

### Pipeline Context

This is the **first skill** in the academic pipeline. Its output (`{project}_papers.xlsx`) feeds into:
- **paper-selector** (for filtering by relevance)
- **paper-deep-reader** (for in-depth analysis of selected papers)
- **lit-review-generator** (as supporting context for the review)

### Knowledge Base Integration

When operating within the Research Knowledge Base context (invoked via `/kb` or when a KB project is active):

1. **Output location**: Save the spreadsheet to the active project folder: `Research Knowledge Base/projects/active/[project-name]/skimmed-papers.xlsx` instead of the default workspace location. Use the project name from the KB, not a separate project name prompt.

2. **Layer 1 guidance**: Before skimming, check if `Research Knowledge Base/layer1-researcher/rules/literature-selection.md` exists. If it does, read it and use these rules to guide what you prioritize and highlight during extraction. For example, if the researcher prefers mechanistic explanations, pay extra attention to papers' theoretical framing and causal claims.

3. **Progress summary**: After processing a batch of papers, update `Research Knowledge Base/projects/active/[project-name]/progress-summary.md` with a synthesis of the broad research landscape observed across all skimmed papers — key themes, dominant methodologies, apparent gaps, and emerging patterns. This summary helps the researcher understand the state of the field before diving deeper.

4. **Papers reference**: After processing, also update `Research Knowledge Base/projects/active/[project-name]/papers-reference.md` with a reference list entry for each skimmed paper (Author, Year, Title).

When NOT in a KB context, the skill operates exactly as described below — all KB integration steps are skipped.

---

### Does NOT Trigger

| Scenario | Use Instead |
|----------|-------------|
| User wants to select/filter papers from an existing spreadsheet | paper-selector |
| User wants a thorough, in-depth reading with critical analysis | paper-deep-reader |
| User wants to write a literature review from collected papers | lit-review-generator |
| User wants to understand a single paper deeply with Q&A | paper-mentor |
| User wants an interactive HTML reader for studying papers | paper-reader |

---

## When This Skill Activates

A user wants to skim or catalog one or more academic papers. They may:
- Upload a PDF and say "skim this" or "add this to my project spreadsheet"
- Paste paper text and ask for extraction
- Ask to process multiple papers for a project
- Reference a project name and want to append new papers to an existing spreadsheet

## Core Workflow

### Step 1: Identify the Project Name

Ask the user which project this paper belongs to, unless they've already named one. The project name determines the spreadsheet filename: `{project-name}_papers.xlsx`. Use kebab-case or snake_case for the filename.

If the user has previously mentioned a project name in this conversation, reuse it without asking again.

### Step 2: Read the Paper

**PDF input:** Use the Read tool or bash to extract text from the uploaded PDF. You do not need to read every page — skim strategically, focusing only on the sections listed below.

**Pasted text:** Work directly with the text provided in the conversation.

**Key principle:** Be efficient. You're skimming, not doing a deep read. The goal is to capture what the study is about, why it matters, and what it found — not how it was done in detail. Methodology and results details are reserved for the paper-deep-reader skill later in the pipeline.

**Reading priority (in order):**

1. **Title** — Captures the core topic and often signals the design or variables
2. **Abstract** — The single most information-dense section; usually contains everything you need for a quick scan. Extract RQ, brief method mention, and key findings from here.
3. **Introduction** — Read for:
   - Theoretical framing and background context (the "why" of the study)
   - Research questions or hypotheses (often at the end of the introduction)
   - **"The Current Study" / "The Present Study" subsection** — if present, this is the most critical part of the introduction. It typically summarizes the study's purpose, rationale, and how it extends prior work. **Always look for this subsection and read it carefully.**
4. **Conclusion / Discussion (final paragraphs)** — Read the last 1-2 paragraphs of the discussion or the conclusion section for the main takeaway, practical implications, and acknowledged limitations.

**Sections to SKIP during skimming:**

- **Methods / Methodology section** — Do not read the detailed methodology. The abstract's method mention is sufficient for the skimming spreadsheet. Full methodological extraction happens in paper-deep-reader.
- **Results / Findings section** — Do not read the detailed results with statistics, tables, or figures. The abstract's findings summary and the discussion's interpretation are sufficient. Detailed statistical extraction happens in paper-deep-reader.
- **References / Appendices** — Skip entirely.

**Why skip methods and results?** The paper-skimmer is designed for rapid cataloging — capturing what the study investigated and what it concluded, not the procedural details. A method summary derived from the abstract (e.g., "RCT with 200 participants") is sufficient at this stage. The paper-deep-reader skill handles full methodological and statistical extraction later.

### Step 3: Extract Information

For each paper, extract these fields:

| Field | What to Capture | Guidance |
|-------|----------------|----------|
| **Author(s)** | Last names of all authors (e.g., "Smith, Jones, & Lee") | Use APA-style author listing |
| **Year** | Publication year | Integer |
| **Title** | Full paper title | Preserve original casing |
| **Research Question / Purpose** | The main RQ or study purpose in one sentence | Paraphrase concisely; if multiple RQs, capture the primary one. Look in the "Current Study" subsection first, then abstract, then end of introduction. |
| **Method Summary** | Study design and sample only — from the abstract | Keep to 1 brief sentence (e.g., "RCT with 200 teachers" or "Qualitative case study, 12 interviews"). Extract this from the abstract only — do NOT read the Methods section. |
| **Key Findings** | The 2-3 most important conclusions | Brief phrases joined by semicolons. Derive from the abstract and conclusion — do NOT read the Results section for detailed statistics. Focus on what was concluded, not the numbers. |

If a field genuinely cannot be determined from the available text, write "Not identified" rather than guessing.

### Step 4: Write to the Excel Spreadsheet

Use the helper script at `scripts/append_paper.py` (located in this skill's directory) to either create a new spreadsheet or append to an existing one.

Run it via bash:

```bash
python "<skill-directory>/scripts/append_paper.py" \
  --file "<output-path>/{project_name}_papers.xlsx" \
  --authors "Smith, Jones, & Lee" \
  --year 2023 \
  --title "Paper Title Here" \
  --rq "What is the effect of X on Y?" \
  --method "Quasi-experimental design with 150 participants; pre-post surveys analyzed with ANCOVA" \
  --findings "X significantly improved Y (p < .01); No effect found for Z; Moderating role of W confirmed"
```

The script handles:
- Creating a new workbook with formatted headers if the file doesn't exist
- Appending a new row if the file already exists
- Professional formatting (header styling, column widths, text wrapping)
- Duplicate detection (warns if a paper with the same title already exists)

After running the script, confirm to the user what was added and how many papers are now in the spreadsheet.

### Step 5: Offer Next Steps

After processing, briefly let the user know the paper was added and offer:
- "Want me to skim another paper for this project?"
- If they have multiple papers, offer to process them in sequence.

## Processing Multiple Papers

If the user provides several papers at once (multiple PDFs or a batch of text), process them one at a time in sequence. For each paper:
1. Extract the information
2. Append to the spreadsheet
3. Move to the next paper

Give a brief summary after all papers are processed (e.g., "Added 4 papers to your project spreadsheet. It now has 12 entries total.").

## Edge Cases

- **Non-empirical papers** (theoretical, conceptual, review papers): Still extract what you can. For Method Summary, write the paper type (e.g., "Theoretical analysis" or "Systematic literature review of 45 studies"). For Key Findings, capture the main arguments or conclusions.
- **Non-English papers with English abstracts**: Extract from the English abstract. Note the original language in the findings field if relevant.
- **Incomplete papers** (e.g., only abstract available): Extract what's available and note which fields are incomplete.

## Important Notes

- The spreadsheet is the deliverable. Always save it to the user's workspace folder.
- Keep extractions concise — this is a quick-scan tool, not a deep analysis tool. Each field should be brief enough to scan in a table view.
- Preserve the user's project organization. One spreadsheet per project, always append.
