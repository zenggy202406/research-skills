---
name: paper-deep-reader
description: "Mentored deep reading of academic papers with Bloom-taxonomy questioning, 300-word integrated summaries, and Research Knowledge Base integration. When in KB context, extracts atomic draft claims to claims.yaml and consults Layer 1 rules. Triggers on: deep read, thorough analysis, critical review, critically analyze, read together, read in depth, detailed extraction, study this paper, walk me through. Requires PDF files."
---

# Paper Deep Reader

An interactive, mentored deep-reading experience. Reads selected academic papers thoroughly, involves the user by directing them to key passages and asking multiple-choice critical questions with theoretically grounded options, then produces an integrated 300-word paragraph summary per paper — synthesizing theory, methodology, findings, critique, and the user's own insights into a cohesive analytical narrative saved to a per-project Excel spreadsheet.

---

## Trigger Conditions

### Trigger Keywords

**English:** deep read, read in depth, thorough reading, in-depth analysis, critically analyze paper, critical reading, detailed extraction, read paper carefully, comprehensive reading, analyze this paper, study this paper, read together, guided reading, mentor me through this paper, walk me through this paper, let's read this, read selected papers, extract methodology, extract theory, extract findings, what are the limitations, strengths and weaknesses, critical review, paper analysis, detailed paper review, close reading

**中文:** 深度閱讀, 精讀論文, 仔細閱讀, 批判性分析, 論文分析, 詳細提取, 一起讀, 引導閱讀, 方法論分析, 理論分析, 優缺點分析, 深入分析, 逐篇閱讀

### Auto-Activation Conditions

This skill should activate automatically when:
1. **User has selected papers** (from paper-selector) and says "now read them" or "let's go deeper" or "analyze these"
2. **User uploads PDFs** and asks for critical analysis, detailed extraction, or thorough reading (not just skimming)
3. **User asks about strengths, limitations, or flaws** of specific papers — e.g., "what are the methodological weaknesses?"
4. **User wants to prepare for writing** — e.g., "I need to understand these papers before writing my review"
5. **User references the deep-reading spreadsheet** — e.g., "add this to my deep reading" or "update the deep reading file"
6. **User wants interactive scholarly discussion** about a paper — e.g., "let's discuss this paper," "what should I pay attention to?"
7. **After paper-selector completes** and the user wants the next step — e.g., "now let's read the selected papers"

### Pipeline Context

This is the **third skill** in the academic pipeline. It:
- **Reads from:** The "Selected" sheet in `{project}_papers.xlsx` (produced by paper-selector) to identify which papers to read
- **Requires:** Actual PDF files of the papers
- **Writes to:** `{project}_deep_reading.xlsx` (a spreadsheet with identification fields + a 300-word integrated paragraph summary per paper)
- **Feeds into:** lit-review-generator (as the primary data source for synthesis)

### Knowledge Base Integration

When operating within the Research Knowledge Base context (invoked via `/kb` or when a KB project is active):

1. **Layer 1 consultation**: Before reading, load these Layer 1 rule files if they exist:
   - `Research Knowledge Base/layer1-researcher/rules/interpretation.md` — guides how findings are interpreted (e.g., cautious vs. bold causal language)
   - `Research Knowledge Base/layer1-researcher/rules/method-evaluation.md` — guides quality assessment (e.g., what counts as a methodological dealbreaker)
   - `Research Knowledge Base/layer1-researcher/rules/research-evaluation.md` — guides overall study evaluation
   Use these rules as moderate constraints during your reading and when formulating critical questions. They should inform your analysis without rigidly constraining it.

2. **Layer 2 field awareness**: After reading the paper, consult `Research Knowledge Base/layer2-field/field-summary.md` (compact ~40-line briefing) to understand the existing conceptual vocabulary and field intelligence. Use this to:
   - Contextualize the paper's constructs against known Layer 2 concepts
   - Check whether the paper addresses any known field gaps (GAP entries) or open questions (OQ entries)
   - Note if the paper confirms or challenges any theoretical constraints (TC entries)
   - Flag new concepts not yet in Layer 2 as potential additions
   - If you need the full definition of a specific concept, grep `Research Knowledge Base/layer2-field/graph.yaml` by name or ID — **do NOT read the full graph.yaml**

3. **Claim extraction** (new Step 5.5 — see below): After the interactive reading and before writing the paragraph summary, extract atomic empirical claims from the paper into structured YAML format and append to the project's `claims.yaml`.

4. **Output location**: Save the deep-reading spreadsheet to `Research Knowledge Base/projects/active/[project-name]/` instead of the default workspace.

When NOT in a KB context, the skill operates exactly as described below — all KB integration steps are skipped (including claim extraction).

---

### Does NOT Trigger

| Scenario | Use Instead |
|----------|-------------|
| User wants a quick skim or catalog of papers | paper-skimmer |
| User wants to filter/score papers by relevance | paper-selector |
| User wants to write a literature review | lit-review-generator |
| User wants to understand an arXiv paper with domain context | paper-mentor |
| User wants an interactive HTML study environment | paper-reader |
| User wants a formal peer review simulation | academic-paper-reviewer |

---

## What Makes This Different from a Skim

This skill treats paper reading as a **collaborative activity**, not a one-way extraction. Inspired by the paper-mentor approach, it:
1. Reads the paper thoroughly (as before)
2. **Directs the user to specific key passages** they should read themselves
3. **Asks multiple-choice critical questions** — each with 3-4 theoretically grounded options plus "None of the above" — at increasing cognitive depth (Bloom's taxonomy)
4. **Produces an integrated 300-word paragraph summary** per paper that weaves together theory, method, findings, critique, and the user's own insights into a single cohesive narrative

The result is deeper understanding for the user and a rich analytical summary that blends AI extraction with human scholarly judgment — ready to feed directly into the lit-review-generator.

---

## Step 1 — Identify Papers and Project

Determine which papers to read and which project they belong to.

**If coming from paper-selector:** The user should have a project spreadsheet with a "Selected" sheet. Read it to identify the High and Moderate relevance papers. Ask the user to provide the PDF files for these papers.

**If standalone:** Ask the user for:
1. A project name (for the output spreadsheet)
2. The PDF files to read

Confirm the list of papers before starting:

> "I'll do an in-depth guided reading of these [N] papers for your [project-name] project:
> 1. [Author (Year) — Title]
> 2. ...
>
> For each paper, I'll read it thoroughly, then guide you through key sections and ask you critical questions. Your insights will be woven into the final analysis. Ready to begin with the first paper?"

---

## Step 2 — Read the Paper Thoroughly (AI First Pass)

For each PDF, read the **entire paper** section by section. Use pdfplumber or pypdf to extract text:

```python
import pdfplumber

with pdfplumber.open("paper.pdf") as pdf:
    full_text = ""
    for page in pdf.pages:
        full_text += page.extract_text() + "\n"
```

**Reading strategy — go section by section:**

1. **Abstract** — Get the overview
2. **Introduction / Literature Review** — Extract theoretical rationale, conceptual framework, research questions or hypotheses
3. **Methods** — Design, sample, instruments, analysis approach
4. **Results / Findings** — Main results with statistics, effect sizes, confidence intervals
5. **Discussion** — Authors' interpretation, acknowledged limitations, future directions
6. **References** — Note key cited works that recur

After your first pass, prepare a brief orientation for the user before starting the interactive phase.

---

## Step 3 — Guided Reading: Direct User to Key Passages

After your AI first pass, guide the user through the paper's most important parts. This step is **interactive and sequential** — present one section at a time, wait for the user's response before moving on.

### 3a. Paper Orientation

Give the user a 3-4 sentence overview of what the paper does, then direct them to the first key passage:

> **Paper overview:** This paper by [Authors] examines [topic] using [method]. The core argument is that [main claim]. The key contribution is [what's new].
>
> **Let's start with the theoretical foundation.** Please read [Section X, paragraphs Y-Z / pages A-B]. This is where the authors lay out their theoretical rationale — pay attention to how they connect [Construct A] to [Construct B] and the specific mechanism they propose.

### 3b. Section-by-Section Guided Reading

Direct the user through **3-4 key sections** of the paper. For each section:

1. **Point them to the specific location** (section name, page numbers, or paragraph identifiers)
2. **Tell them what to focus on** (what makes this passage important)
3. **Wait for them to read it** (they'll tell you when ready)
4. **Ask critical questions** about what they just read (see Step 4)

The key sections to cover are typically:

| Section | What to Direct Attention To |
|---------|---------------------------|
| Theoretical framework (Introduction) | The mechanism or logic connecting constructs; how the study positions itself relative to prior work |
| Methodology (Methods) | Design choices and their trade-offs; how constructs are operationalized; potential threats to validity |
| Key results (Results) | The primary findings, especially effect sizes and unexpected results; what was NOT found |
| Interpretation (Discussion) | How authors explain their results; what limitations they acknowledge vs. what they miss |

Adapt based on the paper — some papers have their most interesting content in an unusual section (e.g., a novel analytical approach, a surprising secondary finding, a rich qualitative theme).

---

## Step 4 — Critical Questions (Bloom's Taxonomy, Multiple-Choice)

After the user reads each key section, ask **2-3 critical questions** that progress through Bloom's cognitive levels. This is adapted from the paper-mentor skill's questioning framework.

### CRITICAL: Question Format — Multiple-Choice with Options

**Every question MUST be presented as a multiple-choice question** with 3-4 options plus a "None of the above" option. This is an iron rule of this skill.

**How to generate options:**
- Each option must be **logically and theoretically sound** — no obviously wrong or trivial answers
- Options should represent genuinely different scholarly perspectives, methodological stances, or theoretical interpretations that a knowledgeable researcher could plausibly hold
- Options should be grounded in the actual content of the paper and relevant theoretical frameworks in the field
- Options should differ meaningfully from each other — they should not be paraphrases of the same idea
- The final option is always **"None of the above"** — if the user selects this, ask them to provide their own reasoning in text

**Format template:**
> **[Question text]**
>
> (a) [Option grounded in theoretical perspective A — 1-2 sentences explaining the reasoning]
> (b) [Option grounded in theoretical perspective B — 1-2 sentences explaining the reasoning]
> (c) [Option grounded in theoretical perspective C — 1-2 sentences explaining the reasoning]
> (d) [Option grounded in theoretical perspective D — if 4 options are warranted]
> (e) None of the above — please share your own reasoning.

### Question Design by Cognitive Level

**For the theoretical framework section:**

- **Understand:**
  > "How would you characterize the relationship between [Construct A] and [Construct B] as framed in this paper?"
  >
  > (a) [Construct A] is a prerequisite for [Construct B] — the authors argue that [A] must be established before [B] can emerge, following [Theorist]'s stage model.
  > (b) [Construct A] and [Construct B] are reciprocal — they mutually reinforce each other through [mechanism], consistent with [Theory X].
  > (c) [Construct A] moderates the effect of [external factor] on [Construct B] — the key claim is about boundary conditions, not direct effects.
  > (d) None of the above — please share your own reasoning.

- **Analyze:**
  > "The authors argue that [mechanism] explains why [X affects Y]. Which alternative explanation do you find most plausible?"
  >
  > (a) A [competing theory] explanation — [X affects Y] because [alternative mechanism 1], which the authors don't adequately rule out.
  > (b) A methodological artifact — the observed relationship may be driven by [confound or design issue] rather than the proposed mechanism.
  > (c) A partial explanation — [mechanism] is necessary but not sufficient; [additional factor] likely plays a mediating role that the authors overlook.
  > (d) None of the above — please share your own reasoning.

- **Evaluate:**
  > "Given your research focus on [user's RQ], how applicable is this theoretical framework to your context?"
  >
  > (a) Highly applicable — the constructs map directly to my variables, and the mechanism aligns with what I expect to find in [user's context].
  > (b) Partially applicable — the core constructs are relevant, but the framework doesn't account for [contextual factor] that is central to my research.
  > (c) Useful as a contrast — this framework represents an alternative perspective that I should acknowledge but argue against in favor of [different framework].
  > (d) None of the above — please share your own reasoning.

**For the methodology section:**

- **Analyze:**
  > "Given the authors' choice of [design type] with [sample], what is the most significant limitation of this design for answering their research question?"
  >
  > (a) Causal inference — [the design] cannot establish directionality; the relationship between [X] and [Y] could run in either direction or be driven by [unmeasured variable].
  > (b) Ecological validity — [the sample/context] is too far from real-world conditions, limiting how much these findings tell us about [the phenomenon] in practice.
  > (c) Measurement validity — the way [key construct] is operationalized through [instrument/measure] may not capture the full construct as theorized.
  > (d) None of the above — please share your own reasoning.

- **Create:**
  > "If you were designing a follow-up study to address this paper's limitations, which approach would you take?"
  >
  > (a) A [longitudinal/experimental/mixed-methods] design to address the [causality/temporal] limitation, measuring [variables] at [timepoints/conditions].
  > (b) Replicate with [different population/context] to test the boundary conditions — specifically whether [finding] holds when [contextual factor] differs.
  > (c) Add [process-level measures / mediator variables / qualitative component] to unpack the mechanism — the current study shows *that* [X affects Y] but not *how*.
  > (d) None of the above — please share your own reasoning.

**For the results section:**

- **Evaluate:**
  > "How much weight would you give this finding in your literature review?"
  >
  > (a) Strong weight — the effect size is [substantial], the methodology is rigorous, and it directly addresses a variable central to my RQ.
  > (b) Moderate weight — the finding is relevant but the [sample size / design / measurement] introduces uncertainty that I'd need to acknowledge.
  > (c) Limited weight — the finding is interesting but [the context is too different / the effect is small / the methodology has a flaw] that limits its applicability to my research.
  > (d) None of the above — please share your own reasoning.

**For the discussion section:**

- **Evaluate:**
  > "The authors claim [interpretation]. How well do the results support this claim?"
  >
  > (a) Well-supported — the evidence directly matches the claim, and the authors appropriately limit their interpretation to what the data can show.
  > (b) Over-reaching — the authors go beyond what [their design/data] can support; a more cautious interpretation would be [alternative].
  > (c) Under-selling — the results actually suggest something more interesting than the authors claim, specifically [stronger/broader implication].
  > (d) None of the above — please share your own reasoning.

- **Create:**
  > "Based on what you've read, what research question does this paper leave unanswered?"
  >
  > (a) The mechanism question — we know [X affects Y], but the *how* (through what process or mediator) remains untested.
  > (b) The boundary question — would [finding] hold in [different population / context / time frame]? The generalizability is unexamined.
  > (c) The integration question — how does [this finding] interact with [finding from another paper in the collection]? The two results seem [complementary/contradictory] but nobody has tested them together.
  > (d) None of the above — please share your own reasoning.

### Question Delivery

Ask questions **one at a time**. Wait for the user's selection before asking the next question. After each answer:

1. **If they select an option (a-d):** Acknowledge their choice briefly (1-2 sentences), extend or nuance their reasoning, and note how this perspective will shape the final summary
2. **If they select "None of the above":** Ask them to share their reasoning in their own words. Then acknowledge and integrate their response.
3. If their answer reveals a misunderstanding, gently correct it with reference to the paper
4. If their answer adds a perspective you hadn't considered, note it — this will enrich the final output
5. Move to the next question or section

Keep the total interactive engagement to **8-12 questions per paper** (2-3 per section across 3-4 sections). Respect the user's time — if they give brief answers or consistently pick options quickly, adapt by asking fewer but more targeted questions. If they frequently choose "None of the above" and give rich text responses, lean into deeper discussion.

---

## Step 5 — Write the Integrated Paragraph Summary (300 Words Max)

After the interactive reading, compose a single **integrated paragraph summary** for each paper. This paragraph replaces the previous multi-column extraction — it weaves together all analytical dimensions into one cohesive narrative that is immediately useful for literature review writing.

### What the Paragraph Must Cover

The 300-word paragraph integrates all of the following (previously separate spreadsheet columns) into a flowing narrative:

1. **Theoretical rationale** — the framework, key constructs, and the theoretical logic of the study
2. **Methodology** — design type, sample, instruments, and analysis approach (concisely)
3. **Main findings** — key results with effect sizes or key statistics where available
4. **Critical analysis** — strengths, limitations, methodological flaws, and theoretical gaps (woven into the narrative, not listed)
5. **User insights** — the user's scholarly perspective from the interactive reading, including their assessment of the framework's applicability, alternative explanations they proposed, methodological concerns, and connections to other papers or their own research

### Writing Guidelines

**Narrative flow, not a checklist.** The paragraph should read as a scholarly analytical summary — the kind a researcher would write in their reading notes after carefully studying a paper and discussing it with a colleague. It should NOT read as a series of labeled fields stitched together.

**Structure suggestion:** Open with the study's theoretical positioning and purpose → transition to how they tested it (method, briefly) → what they found (key results) → critical assessment (what's strong, what's limited) → close with the user's perspective and how the paper connects to their research direction.

**Integrate user insights naturally.** Don't separate them into a distinct section or label them as "the researcher noted." Instead, weave the user's assessments into the critical analysis portion — e.g., "While the RCT design lends strong internal validity, the absence of process-level data leaves the feedback engagement mechanism untested — a gap that think-aloud protocols could address."

**Be precise with numbers.** Include effect sizes, sample sizes, and key statistics where they add value, but don't let them dominate the narrative.

**300 words maximum.** This is a hard ceiling. Aim for 250-300 words — enough for substance, short enough to scan across many papers.

### Example Paragraph

> Garcia et al. (2022) investigated the effect of elaborated feedback on self-regulated learning (SRL) in undergraduate education, grounding their work in Zimmerman's cyclical SRL model and arguing that feedback quality — not merely feedback presence — drives the forethought-performance-reflection cycle. Using a randomized controlled trial with 284 psychology undergraduates, participants received either elaborated feedback (with metacognitive prompts) or standard corrective feedback across an 8-week intervention, measured via the MSLQ (α = .82–.91) and analyzed with two-way ANCOVA. Students in the elaborated condition showed significantly higher metacognitive self-regulation (d = 0.62, p < .01) and academic performance (d = 0.45, p < .05), though no significant difference emerged for time management or effort regulation. The study's strength lies in its well-powered experimental design with random assignment, providing stronger causal evidence than the correlational work that dominates the SRL-feedback literature. However, the single-institution sample and reliance on self-report measures limit both external validity and the ability to capture actual regulatory behavior. Critically, the study demonstrates that elaborated feedback affects SRL outcomes but does not examine how students process the feedback — the theoretical model assumes metacognitive comparison occurs during feedback engagement, yet no process-level data verify this assumption. Think-aloud protocols during feedback processing could reveal whether the proposed mechanism operates as theorized or whether students engage in simpler heuristic processing. The finding also invites integration with Self-Determination Theory, as autonomy-supportive framing of feedback may moderate the SRL effects, a connection the authors do not explore but that could explain the null results on effort regulation — a construct more closely tied to intrinsic motivation than to cognitive strategy use.

*(297 words — integrates theory, method, findings, critique, and user insights in a single narrative)*

---

## Step 5.5 — Extract Claims (KB Context Only)

This step runs only when operating within the Research Knowledge Base context. Skip it otherwise.

After the interactive reading and paragraph composition (but before writing to the spreadsheet), extract atomic empirical claims from the paper.

### What Constitutes a Claim

A claim is a single, atomic empirical finding or conclusion from the study. Claims should be:
- **Atomic**: One finding per claim — do not combine multiple results
- **Context-aware**: Include the conditions under which the finding holds
- **Traceable**: Linked to the specific paper and method

### Extraction Process

1. Review the paper's results and key findings identified during deep reading
2. For each distinct empirical finding, formulate a claim entry
3. Determine the next available claim ID by reading the project's existing `claims.yaml`

### Claim Format

Each claim is a YAML entry:

```yaml
- id: CLM-XXX
  statement: "Children aged 4-5 showed significantly higher inhibitory control scores after the bilingual intervention compared to the monolingual control group."
  conditions: "8-week intervention period; structured bilingual classroom activities"
  population: "Typically developing preschoolers (N=84), middle-class families, urban setting"
  method_ref: "Go/No-Go task; DCCS"
  source: "Garcia & Lee (2024) — Bilingual effects on executive function in preschoolers"
  status: draft
  notes: "Effect size d=0.62; auto-extracted during deep reading"
  history:
    - version: 1
      date: "[today's date]"
      statement: "[same as above]"
      changed_by: "auto-extracted"
```

### Guidelines

- Extract **3-8 claims per paper** depending on the paper's richness. Focus on:
  - Primary findings (main results addressing research questions)
  - Surprising or unexpected findings
  - Null results that are theoretically informative
  - Boundary conditions or moderator effects
- Do NOT extract trivial findings (e.g., manipulation checks, demographic descriptions)
- Include effect sizes and key statistics in the `notes` field when available
- Set `method_ref` to the Layer 2 method ID if the method exists in the knowledge graph, otherwise use the method name
- All claims start as `status: draft` — the user will refine them later

### Writing Claims to File

Read the project's existing `claims.yaml` from `Research Knowledge Base/projects/active/[project-name]/claims.yaml`. If it contains existing claims, determine the next ID number. Append the new claims and write back.

After extraction, briefly inform the user:
> "I've extracted [N] draft claims from this paper and added them to your project's claims file. You can review and refine them later via `/kb`."

---

## Step 6 — Write to the Deep-Reading Spreadsheet

Use the helper script at `scripts/write_deep_reading.py` to create or update the spreadsheet.

Run via bash:

```bash
python "<skill-directory>/scripts/write_deep_reading.py" \
  --file "<output-path>/{project_name}_deep_reading.xlsx" \
  --papers '<JSON array of paper objects>'
```

The JSON array uses a simplified structure — identification fields plus the integrated summary:
```json
{
  "authors": "Garcia, M., Berger, T., & Tanaka, Y.",
  "year": 2022,
  "title": "Effect of Elaborated Feedback on Self-Regulated Learning in Undergraduate Education",
  "journal": "Journal of Educational Psychology, 114(3), 512-528",
  "summary": "Garcia et al. (2022) investigated the effect of elaborated feedback on self-regulated learning (SRL) in undergraduate education, grounding their work in Zimmerman's cyclical SRL model and arguing that feedback quality — not merely feedback presence — drives the forethought-performance-reflection cycle. Using a randomized controlled trial with 284 psychology undergraduates, participants received either elaborated feedback (with metacognitive prompts) or standard corrective feedback across an 8-week intervention, measured via the MSLQ (α = .82–.91) and analyzed with two-way ANCOVA. Students in the elaborated condition showed significantly higher metacognitive self-regulation (d = 0.62, p < .01) and academic performance (d = 0.45, p < .05), though no significant difference emerged for time management or effort regulation. The study's strength lies in its well-powered experimental design with random assignment, providing stronger causal evidence than the correlational work that dominates the SRL-feedback literature. However, the single-institution sample and reliance on self-report measures limit both external validity and the ability to capture actual regulatory behavior. Critically, the study demonstrates that elaborated feedback affects SRL outcomes but does not examine how students process the feedback — the theoretical model assumes metacognitive comparison occurs during feedback engagement, yet no process-level data verify this assumption. Think-aloud protocols during feedback processing could reveal whether the proposed mechanism operates as theorized or whether students engage in simpler heuristic processing. The finding also invites integration with Self-Determination Theory, as autonomy-supportive framing of feedback may moderate the SRL effects, a connection the authors do not explore but that could explain the null results on effort regulation — a construct more closely tied to intrinsic motivation than to cognitive strategy use."
}
```

---

## Step 7 — Present Results and Transition

After processing each paper (or all papers), give a brief summary:

> **Deep reading complete.** I've analyzed [N] papers for your [project-name] project, incorporating your insights from our guided reading.
>
> Key observations across the set:
> - [1-2 sentences on recurring theoretical themes]
> - [1-2 sentences on common methodological approaches or gaps]
> - [Your most notable insights across the papers]

Then link the spreadsheet file. If processing multiple papers, offer to continue with the next paper or take a break.

---

## Processing Sequence for Multiple Papers

For multiple papers, process one at a time — including the full interactive cycle:

1. **Paper 1:** AI reads → Guide user through key sections → Ask multiple-choice questions → Write integrated paragraph
2. **Paper 2:** Same cycle
3. After all papers: Write to spreadsheet → Present summary

Between papers, briefly ask: "Ready for the next paper, or would you like to take a break?" Respect the user's cognitive load — this is intensive work.

---

## Adapting the Interaction Level

Not every reading session needs the same depth of interaction. Adapt based on cues:

- **User says "just read it for me":** Skip the guided reading (Steps 3-4) and do a standard deep extraction without user involvement. Still produce the integrated paragraph summary, but note that user insights are not included.
- **User gives very brief answers:** Reduce to 1-2 questions per section instead of 2-3. Focus on the highest-value questions (Evaluate and Create levels).
- **User is deeply engaged:** Let the conversation go deeper. Add follow-up questions. Allow digressions into related topics — these often produce the richest insights for the summary.
- **Time-constrained:** Ask only 4-5 total questions per paper, focused on the methodology and discussion sections (where user expertise adds the most value).

---

## Edge Cases

- **Non-empirical papers** (theoretical, conceptual): Adapt the paragraph accordingly. Methodology becomes "Theoretical analysis" or "Conceptual framework development." Focus the narrative on the argumentative structure, conceptual contributions, and logical coherence rather than empirical results.
- **Review papers / meta-analyses:** Focus the paragraph on scope, inclusion criteria, synthesis approach, moderator analyses, and overall conclusions. User questions should target assessment of the review's comprehensiveness.
- **Poor PDF quality:** Inform the user and ask for an alternative format.
- **Very long papers (>30 pages):** Still read fully, but be selective about which sections to direct the user to — focus on the 3-4 most important passages.
- **Papers not in English:** Note the language. If you can read it, proceed. If not, inform the user.
- **User skips all questions:** That's fine — produce the paragraph summary without user insights. Don't pressure them.

---

## Quality Standards

- **The integrated paragraph** must read as a cohesive scholarly narrative, not a list of fields joined by transitions
- **Theory** should explain the *logic* of the study, not just name the framework
- **Method** should be concise but specific enough for the reader to assess the design's appropriateness
- **Findings** must include actual numbers where available — effect sizes, significance levels, key statistics
- **Critique** should be woven naturally into the narrative, not appended as a separate section
- **User insights** should be seamlessly integrated, not labeled or separated
- **300-word maximum** is a hard ceiling — enforce it during writing
- **Multiple-choice questions** must always have 3-4 theoretically grounded options plus "None of the above"
- **Guided reading** should feel like a scholarly conversation, not an exam
