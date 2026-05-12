---
name: paper-selector
description: "Interactive research-alignment tool that filters skimmed papers by relevance to your project, integrated with the Research Knowledge Base. Use this skill when the user wants to select, filter, narrow down, or prioritize papers from a skimmed collection for a specific research project — whether they have 5 papers or 150. Triggers when the user says things like 'help me pick the relevant papers', 'which papers should I read for my project', 'filter my papers', 'select papers for my dissertation', 'narrow down my literature', or 'which of these papers matter for my RQ'. Works with spreadsheets produced by the paper-skimmer skill. When in KB context, uses Layer 1 researcher preferences and Layer 2 field concepts to enhance relevance scoring, and can skip the research interview if the project overview already defines domain, core idea, and research questions."
---

# Paper Selector

Guides the user through a structured research interview, then filters their skimmed papers by relevance to produce a curated selection with justification — and optionally hands off to paper-reader for deep study.

---

## Trigger Conditions

### Trigger Keywords

**English:** select papers, filter papers, pick papers, choose papers, narrow down papers, prioritize papers, which papers should I read, which papers are relevant, relevant papers for my project, score papers, rank papers, sort by relevance, papers for my dissertation, papers for my thesis, papers for my RQ, align papers with research questions, curate papers, shortlist papers, paper screening, inclusion criteria, exclude irrelevant papers, triage papers, which ones matter, most important papers, core papers

**中文:** 篩選論文, 選擇論文, 挑選論文, 哪些論文相關, 論文排序, 縮小範圍, 論文篩選, 核心論文, 與研究問題相關, 論文優先順序, 精選論文

### Auto-Activation Conditions

This skill should activate automatically when:
1. **User has a `*_papers.xlsx` spreadsheet** and asks "which papers should I focus on" or "which are relevant"
2. **User mentions research questions** in the context of their paper collection — e.g., "my RQ is about X, which papers fit?"
3. **User says they have too many papers** — e.g., "I have 50 papers and need to narrow it down"
4. **User asks to score or rank papers** by relevance to a topic or research direction
5. **After paper-skimmer completes** and the user wants to move to the next step — e.g., "now help me pick the important ones"
6. **User wants to prepare for deep reading** — e.g., "which papers should I read carefully?"

### Pipeline Context

This is the **second skill** in the academic pipeline. It:
- **Reads from:** `{project}_papers.xlsx` (produced by paper-skimmer)
- **Writes to:** A "Selected" sheet in the same spreadsheet
- **Feeds into:** paper-deep-reader (for in-depth analysis) and paper-reader (for interactive HTML reader)

### Knowledge Base Integration

When operating within the Research Knowledge Base context (invoked via `/kb` or when a KB project is active):

1. **Spreadsheet location**: Read from `Research Knowledge Base/projects/active/[project-name]/skimmed-papers.xlsx` instead of asking for a project spreadsheet.

2. **Skip or shorten the research interview**: Read `Research Knowledge Base/projects/active/[project-name]/overview.md` to extract the research domain, core idea, and research questions. If these are clearly defined, present them as the research profile and ask the user to confirm — no need to conduct the full 3-question interview. If the overview is vague, conduct the interview as usual.

3. **Layer 1 enrichment**: Read `Research Knowledge Base/layer1-researcher/rules/literature-selection.md` to understand the researcher's preferences. Use these rules to refine scoring. For example:
   - If the researcher prefers longitudinal designs, give a small scoring bonus to papers using longitudinal methods
   - If the researcher values mechanistic explanations, weight theoretical alignment more heavily for papers offering causal mechanisms
   - These adjustments are moderate — they nudge scores, not override the rubric

4. **Layer 2 field awareness**: Read `Research Knowledge Base/layer2-field/field-summary.md` (compact ~40-line briefing) to understand the field's conceptual landscape, known gaps, theoretical constraints, and research guides. Use this to:
   - Check whether a paper's constructs connect to known Layer 2 concepts (papers that connect score higher)
   - Identify papers that address known field gaps (GAP entries) — these are especially valuable
   - Apply theoretical constraints and research guides when assessing alignment
   - **Do NOT read the full `graph.yaml`** — if you need detail on a specific concept, grep `graph.yaml` by name or ID

5. **Output**: After selection, copy the selected paper PDFs (if the user provides them) to `Research Knowledge Base/projects/active/[project-name]/papers/` with clear naming (e.g., `Author_Year_ShortTitle.pdf`). Update `papers-reference.md` with selected papers.

When NOT in a KB context, the skill operates exactly as described below — all KB integration steps are skipped.

---

### Does NOT Trigger

| Scenario | Use Instead |
|----------|-------------|
| User wants to skim/extract info from new papers | paper-skimmer |
| User wants to do an in-depth critical reading of papers | paper-deep-reader |
| User wants to write a literature review | lit-review-generator |
| User wants to understand a paper with Q&A (arXiv) | paper-mentor |
| User wants to create an interactive HTML reader | paper-reader |

---

## Overview

This skill works downstream of paper-skimmer. The user has already skimmed a collection of papers into a project spreadsheet — anywhere from a handful to a hundred or more. Now they need to figure out which papers are most relevant to their specific research direction. Rather than asking the user to specify everything upfront, this skill conducts a short sequential interview to draw out the research focus, then uses that understanding to score and filter papers.

The approach adapts to the size of the pool — see the Pool Size Guidance section below.

---

## Step 1 — Locate the Project Spreadsheet

Ask the user which project they want to select papers for. They may name it directly or you can list available `*_papers.xlsx` files in their workspace folder.

Read the spreadsheet using openpyxl or pandas to load all papers from the "Papers" sheet. Confirm with the user how many papers are in the file (e.g., "I found 23 papers in your teacher-retention project. Let's figure out which ones matter most for your research.").

---

## Step 2 — Research Interview (Sequential)

Conduct a structured interview with the user. Ask these questions **one at a time**, waiting for each response before asking the next. This sequencing matters — each answer informs how you frame the next question, and it feels more like a research conversation than a form.

### Question 1: Research Domain
> "What is the broad research domain or field for this project?"

**Purpose:** Establishes the disciplinary context. Shapes how you interpret alignment later.
**Examples of answers:** "Educational technology in higher education", "Teacher professional development", "STEM education equity"

After they answer, briefly reflect back your understanding (one sentence) before moving on.

### Question 2: Core Research Idea
> "What is the main idea or focus of your research? What phenomenon, relationship, or problem are you investigating?"

**Purpose:** Identifies the conceptual center of their project. This is the anchor for relevance scoring.
**Examples:** "I'm looking at how formative assessment feedback affects student self-regulation", "I want to understand why some teachers stay in high-poverty schools while others leave"

Again, reflect back briefly and connect it to the domain they mentioned.

### Question 3: Research Questions
> "What are your specific research questions? (List as many as you have — even draft or tentative ones are helpful.)"

**Purpose:** These are the sharpest tool for scoring. Papers that speak directly to one or more RQs get the highest relevance.
**Examples:** "RQ1: How does elaborated feedback in formative assessment affect metacognitive self-regulation? RQ2: Does the effect vary by student prior achievement?"

After receiving the RQs, summarize all three answers back to the user as a compact research profile:

> **Your research profile:**
> - **Domain:** [domain]
> - **Core idea:** [idea]
> - **Research questions:** [RQ1, RQ2, ...]
>
> Does this capture your project accurately? I'll use this to score your [N] papers.

Wait for confirmation. If they correct anything, update accordingly.

---

## Step 3 — Score Each Paper

For each paper in the spreadsheet, evaluate its relevance to the user's research profile. Scoring is based primarily on **theoretical and research question alignment**.

### Scoring Rubric (0-10 scale)

**Theoretical Alignment (0-5 points):**
- 5 — Paper investigates the same or closely related theoretical constructs as the user's core idea
- 4 — Paper addresses a directly overlapping construct or framework
- 3 — Paper shares the same broad domain and touches on related constructs
- 2 — Paper is in the same domain but addresses a tangentially related construct
- 1 — Paper is in the same broad field but different subdomain
- 0 — No theoretical connection

**RQ Alignment (0-5 points):**
- 5 — Paper directly answers or closely parallels one of the user's RQs
- 4 — Paper addresses the same variables/relationships but in a different context
- 3 — Paper provides evidence relevant to a component of the user's RQ (e.g., one variable)
- 2 — Paper offers methodological or contextual insight useful for the user's RQs
- 1 — Paper has peripheral relevance (e.g., same population but different questions)
- 0 — No alignment with any RQ

**Total score = Theoretical + RQ alignment (0-10)**

### Selection Threshold

- **Highly relevant (7-10):** Auto-selected. These papers are core to the project.
- **Moderately relevant (4-6):** Included with a note — may be useful for background or methodology.
- **Low relevance (0-3):** Excluded from the selected set.

**Calibrate the threshold to the pool size.** The goal is always to surface a manageable, meaningful core — not to apply a fixed cut mechanically:

| Pool size | Target selected | Guidance |
|-----------|----------------|----------|
| < 10 | All or nearly all | Skip formal scoring — see Pool Size Guidance |
| 10–20 | 50–70% | Be inclusive; most papers are probably relevant if the pool was curated |
| 20–50 | 40–60% | Standard threshold (7+ for High, 4+ for Moderate) |
| 50–100 | 25–40% | Tighten slightly — raise High threshold to 8+ if too many papers qualify |
| 100+ | 15–25% (or a fixed target the user names) | Ask the user upfront how many papers they want to end up with; use that as the calibration target |

If the resulting selection feels too broad or too narrow given the pool, flag it: "I've selected [X] out of [N] papers. Does that feel like the right scope, or would you like me to tighten/widen the threshold?" Let the user decide — they know their project best.

### Scoring Process

Use the data already in the spreadsheet (title, research question, method summary, key findings) to score each paper. You have enough information from the quick scan to make a reasonable relevance judgment — you don't need to re-read the full papers.

For each paper, generate:
- **Relevance score** (0-10)
- **Relevance tier** ("High", "Moderate", or "Low")
- **Rationale** — 1-2 sentences explaining why this paper scored where it did, referencing specific connections (or lack thereof) to the user's research profile

---

## Step 4 — Write the "Selected" Sheet

Use the helper script at `scripts/write_selected.py` to add a "Selected" sheet to the existing project spreadsheet.

Run via bash:

```bash
python "<skill-directory>/scripts/write_selected.py" \
  --file "<path-to-project-xlsx>" \
  --selections '<JSON array of selections>'
```

The JSON array format:
```json
[
  {
    "authors": "Garcia, Berger, & Tanaka",
    "year": 2022,
    "title": "Paper Title",
    "rq": "Original RQ from skimmed data",
    "method": "Original method summary",
    "findings": "Original key findings",
    "score": 8,
    "tier": "High",
    "rationale": "Directly examines formative assessment and self-regulation, matching RQ1 closely."
  }
]
```

The script:
- Creates a "Selected" sheet with all original columns plus Score, Tier, and Rationale
- Sorts papers by score (highest first)
- Color-codes rows by tier (green for High, yellow for Moderate)
- Adds a summary header row showing the research profile
- Preserves the original "Papers" sheet untouched

After writing, present a summary to the user:

> **Selection complete.** Out of [N] papers:
> - **[X] highly relevant** (score 7-10) — core papers for your project
> - **[Y] moderately relevant** (score 4-6) — useful for background/methods
> - **[Z] excluded** (score 0-3) — not aligned with your current RQs
>
> The "Selected" sheet has been added to your spreadsheet with scores and rationale for each paper.

---

## Step 5 — Hand Off to Paper-Reader

After presenting the selection results, offer to create a deep-reading environment for the selected papers:

> "Would you like me to create an interactive Paper Reader for the [X] highly relevant papers? This gives you a full reading environment with analysis, quizzes, glossary, and AI chat."

If the user agrees:

1. **Check if the user has the actual paper files** (PDFs or full text). The skimmed data in the spreadsheet is not enough for paper-reader — it needs full paper content. Ask:
   > "To create the deep reader, I'll need the full papers. Do you have the PDFs for the selected papers?"

2. If they have PDFs, invoke the paper-reader skill (read SKILL.md from the paper-reader skill directory). Pass it the selected papers.

3. If they don't have the PDFs yet, provide the list of selected papers with full citations so they can retrieve them:
   > "Here are the [X] papers to retrieve for deep reading: [list with authors, year, title, journal]"

The paper-reader integration is optional — the core deliverable of this skill is the scored and filtered "Selected" sheet in the spreadsheet.

---

## Pool Size Guidance

The scoring approach stays the same regardless of pool size, but the interaction and calibration adapt:

**Very small pool (< 10 papers):** Skip the formal scoring threshold entirely. Instead, after the interview, discuss each paper briefly with the user — naming it and asking whether they think it's relevant. Use scores internally to order the conversation, but present the outcome as a ranked reading list rather than a binary selected/excluded split. The overhead of a full scoring table adds little value when the user can probably name the relevant papers themselves.

**Small pool (10–20 papers):** Run the full scoring process but be inclusive. Most papers in a tight collection were probably collected for a reason. Prefer to include papers at the borderline (score 4–6) rather than exclude them, and explain your reasoning briefly for each one.

**Medium pool (20–50 papers):** The standard workflow. Apply the scoring rubric and thresholds as written. Aim for 40–60% selected. Present the full scored table and offer to adjust the threshold if the selection feels off.

**Large pool (50–100 papers):** Before scoring, ask the user: "You have [N] papers — roughly how many would be a manageable set to work with?" Use their answer to calibrate. If they say 20, score all papers and take the top 20. If they're unsure, apply a tighter threshold (High = 8+ rather than 7+) and show them the count before committing.

**Very large pool (100+ papers):** This is a systematic review situation. Before scoring, it's worth asking whether some papers can be pre-filtered by year, geography, or methodology before you score for relevance — scoring 100+ papers from skimmed data is feasible but takes time. Confirm with the user how to proceed. Once the approach is agreed, apply scoring in batches if needed, and calibrate to a target count the user specifies.

---

## Edge Cases

- **All papers score high:** The skimming phase was probably well-targeted. Congratulate the user, confirm they want all of them, and offer to rank by score as a reading priority order.
- **No papers score above 4:** This usually means the skimmed collection and the current RQs have drifted apart. Point this out gently and ask if their research direction has shifted since they started collecting papers — it often has.
- **User changes RQs mid-interview:** That's fine and common. Research is iterative. Use their latest answers for scoring, and note in the summary which RQs shaped the selection.
- **Multiple project spreadsheets:** Work with one project at a time.

---

## Important Notes

- The interview is the heart of this skill. Don't rush it. The quality of the scoring depends entirely on how well you understand the user's research focus.
- Scoring is inherently approximate — you're working from quick-scan data, not full paper reads. Frame your rationales accordingly ("Based on the abstract and findings..." not "This paper definitively...").
- Always preserve the original "Papers" sheet. The "Selected" sheet is additive — the user should never lose their full collection.
