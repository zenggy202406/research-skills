---
name: intro-writer
description: "Interactive Introduction section writer for psychology papers with Research Knowledge Base integration. When in KB context, uses Layer 3 argument units for logical flow (broad context → gap → RQ), claims as evidence base, Layer 2 concepts for theoretical landscape, and Layer 1 writing/reasoning rules. Enforces grounding policy. Can skip early phases if project already has curated papers and refined claims/arguments. Triggers on: write introduction, help me write the intro, introduction section, draft introduction, develop research idea, develop research questions, find research gaps, intro for my paper. Focus: psychology and behavioral/social sciences."
---

# Introduction Writer

An interactive, mentored skill for writing the Introduction section of a psychology research paper. Takes the user from a broad research idea all the way to a polished Introduction draft — finding papers, identifying gaps, formulating research questions, outlining, and writing — with the user involved at every critical decision point.

---

## Trigger Conditions

### Trigger Keywords

**English:** write introduction, write intro, introduction section, draft introduction, help me write the intro, I have a research idea, develop my research idea, develop research questions, find research gaps, write the intro for my paper, introduction for my study, research idea to introduction, intro section, help me start my paper, paper introduction, opening section, background section, develop my RQs, research gap identification, what should I study, turn my idea into a paper

**中文:** 寫緒論, 撰寫引言, 研究構想, 發展研究問題, 尋找研究缺口, 撰寫研究背景, 論文緒論, 研究想法, 幫我寫引言

### Auto-Activation Conditions

This skill should activate automatically when:
1. **User says they have a research idea** and wants help developing it into a paper
2. **User asks to write just the Introduction section** (not a full paper)
3. **User wants to identify research gaps** from a topic area and develop RQs
4. **User has papers** and wants to write the Introduction around them
5. **User is in psychology** (or related behavioral/social sciences) and mentions writing an introduction

### Pipeline Context

This skill **orchestrates** other skills in the pipeline rather than replacing them:
- **Invokes paper-skimmer** to build initial literature understanding
- **Invokes paper-selector** twice — first for broad relevance, then for RQ-specific relevance
- **Invokes paper-deep-reader** for the most critical papers during writing
- **Reads from** `resources/introduction_writing_guide.md` for writing principles and anti-patterns
- **Applies** academic-paper writing quality standards during drafting
- **Outputs** the Introduction section as part of a Word document (.docx)

### Knowledge Base Integration

When operating within the Research Knowledge Base context (invoked via `/kb` or when a KB project is active), the Introduction writing process benefits from the structured knowledge already built in the project.

#### Grounding Policy

During writing, strictly observe this priority:
1. **Layer 3 is primary** — all claims and arguments in the Introduction must trace to `claims.yaml` and `arguments.yaml`
2. **Layer 2 is supportive** — use `field-summary.md` for field orientation and gap awareness, and grep specific concepts from `graph.yaml` by ID for the theoretical landscape. Do NOT read full `graph.yaml`.
3. **External knowledge is minimal** — do NOT introduce factual claims not in the knowledge base
4. Maintain clear separation between **evidence**, **interpretation**, and **speculation**

#### Data Sources in KB Context

Load from the active project folder:

1. **Arguments** (`arguments.yaml`) — Use to structure the Introduction's logical flow: from broad theoretical context, through the specific problem, to the research gap, to the research questions. Each argument unit can serve as the backbone for one or more paragraphs.

2. **Claims** (`claims.yaml`) — The evidence base for empirical statements in the Introduction. Every cited finding should be traceable to a claim.

3. **Project overview** (`overview.md`) — Research idea, questions, background, and aims.

4. **Competing explanations** (`competing-explanations.md`) — Alternative perspectives to acknowledge.

5. **Project concepts** (`concepts.yaml`) — Project-specific concept refinements.

6. **Layer 2 field summary** (`layer2-field/field-summary.md`) — Compact overview of the field's conceptual landscape, known gaps, open questions, theoretical constraints, methodological limitations, and research guides. **Read this first** for Layer 2 orientation. Use known gaps (GAP entries) and open questions (OQ entries) to inform gap identification in Phase 4. Use theoretical constraints (TC entries) and research guides (RG entries) to frame the study's positioning. If a specific concept definition is needed, grep `layer2-field/graph.yaml` by ID — **do NOT read the full graph.yaml**.

7. **Layer 1 rules**:
   - `rules/writing-style.md` — Writing tone and structure preferences
   - `rules/reasoning-style.md` — How arguments should be constructed
   - `rules/interpretation.md` — Interpretive stance for discussing prior work

#### Modified Workflow in KB Context

The standard 8-phase workflow adapts when KB data is available:

- **Phase 1 (Collect)**: Skip if `overview.md` has clear topic, ideas, and RQs. Confirm with user.
- **Phases 2-3 (Skim/Select)**: Skip if the project already has `skimmed-papers.xlsx` and curated papers in `papers/`. The KB workflow has already handled this.
- **Phase 4 (Elaborate)**: Use argument units, competing explanations, and **Layer 2 field intelligence** (from `field-summary.md`) as the starting point for gap identification. Check known gaps (GAP entries) and open questions (OQ entries) — the project may be addressing one of these. The gaps may also be explicit in the argument units' counterarguments and scope conditions.
- **Phase 5 (RQ Formation)**: Skip if RQs are already defined in `overview.md`. Confirm with user.
- **Phase 6 (Select 2nd)**: Skip — papers are already curated for this project.
- **Phase 7 (Outline)**: Structure the outline around argument units. The Introduction's narrative arc should reflect the logical flow from broad context → theoretical framework → specific gap → research questions, with each section grounded in specific arguments.
- **Phase 8 (Draft)**: Ground every paragraph in claims and arguments. Use Layer 2 concepts for the opening theoretical landscape. When a gap is encountered: "⚠️ GAP: [description]" — propose a suggestion, ask user to decide.

#### Output in KB Context

Save the .docx to both:
- `Research Knowledge Base/projects/active/[project-name]/{project}_introduction.docx`
- User's workspace folder

When NOT in a KB context, the skill operates exactly as described below — all KB integration steps are skipped.

---

### Article-Level Evidence Extraction

When reading articles — whether skimming (Phase 2) or deep reading (Phase 8, on-demand) — extract key arguments and claims **from within the article's text** along with **the in-text citations the article uses to support them**. These extracted items become additional evidence for writing the Introduction, supplementing any KB claims/arguments.

#### What to Extract

For each article being read, look for:

1. **Empirical claims with citations** — Factual statements about prior findings that the article supports with references. Example: "Joint attention at 12 months predicts vocabulary size at 24 months (Tomasello & Farrar, 1986; Carpenter et al., 1998)."
2. **Theoretical arguments with citations** — Conceptual claims about mechanisms, frameworks, or models. Example: "According to social-pragmatic theory, children learn words by reading the communicative intentions of others (Tomasello, 2003)."
3. **Gap statements** — Statements about what is unknown, unresolved, or untested, especially those relevant to the user's research questions.
4. **Boundary conditions and qualifications** — Claims about when/where an effect holds or doesn't, with supporting citations.

**Extraction priority**: Focus on claims and arguments **relevant to the user's research questions and identified gaps**. Do not extract everything — extract what serves the Introduction's argument.

#### Extraction Format

For each extracted item, record:

```
- Claim/Argument: [Paraphrased content in your own words]
- Original citations: [The in-text citations used in the source article, e.g., "Tomasello & Farrar, 1986; Carpenter et al., 1998"]
- Source article: [The article you are reading, e.g., "Smith, 2023"]
- Location: [Section of the article where this appears, e.g., "Introduction, p. 3"]
- Relevance: [Which RQ or gap this supports]
```

#### Citation Rule: Secondary Citations

Because you have not read the original sources directly — you encountered them cited within another article — you **must** use APA 7 secondary citation format when using these claims in writing:

- **Parenthetical:** (Tomasello & Farrar, 1986, as cited in Smith, 2023)
- **Narrative:** Tomasello and Farrar (1986, as cited in Smith, 2023) found that...

**Exception:** If the original source is also one of the papers in the project (i.e., you have read or skimmed the original directly), cite it directly without "as cited in."

#### Extraction Depth by Reading Mode

- **During skimming (Phase 2):** Extract 3–5 key claims per paper from the abstract, introduction, and conclusion. Focus on high-level empirical and theoretical claims with broad citations.
- **During deep reading (Phase 8, on-demand):** Extract all relevant claims and arguments from the full text, including nuanced findings, methodological qualifications, and theoretical reasoning. This yields richer, more specific evidence for paragraphs that require detailed support.

#### Using Extracted Evidence in Writing (Phase 8)

During drafting, the extracted claims and arguments become building blocks alongside KB evidence:

1. **Paraphrase, never copy** — Restate claims in your own words, adapted to the paragraph's argument
2. **Cite with secondary format** — Always use "as cited in" unless the original source is in the project's paper collection
3. **Integrate, don't dump** — Weave extracted claims into the paragraph's argument flow; do not list them sequentially
4. **Prioritize convergence** — When multiple articles cite the same original source for the same claim, that claim is well-established and can anchor a paragraph's argument
5. **Flag thin evidence** — If a claim is supported by only one secondary citation and is central to the argument, flag it: "⚠️ THIN EVIDENCE: This claim relies on a single secondary citation. Consider finding the original source or additional support."

---

### Does NOT Trigger

| Scenario | Use Instead |
|----------|-------------|
| User wants a full research paper (all sections) | academic-paper |
| User wants only a literature review (no Introduction structure) | lit-review-generator |
| User wants to skim papers without writing context | paper-skimmer |
| User wants a research report, not a paper section | deep-research |

---

## Overview: The Full Workflow

```
Phase 1: COLLECT       → Gather research topic and broad ideas from the user
Phase 2: SKIM          → Invoke paper-skimmer on provided papers for broad understanding
Phase 3: SELECT (1st)  → Invoke paper-selector to filter by broad relevance
Phase 4: ELABORATE     → Q&A to refine ideas, identify 2-3 theoretical gaps
Phase 5: RQ FORMATION  → Guide user to formulate concrete research questions
Phase 6: SELECT (2nd)  → Re-invoke paper-selector with refined RQs as criteria
Phase 7: OUTLINE       → Generate detailed paragraph-level Introduction outline
Phase 8: DRAFT         → Write the Introduction, invoking paper-deep-reader on-demand
```

Each phase involves the user. No phase proceeds without the user's confirmation or input.

---

## Phase 1 — Collect Research Topic and Broad Ideas

Start with an open conversation to understand what the user wants to study.

### 1a. Ask for the research topic

> "What broad topic or area are you interested in? This can be as general as 'feedback in education' or as specific as 'the effect of peer feedback on self-regulated learning in online courses.'"

### 1b. Ask for initial ideas

> "What's your rough idea or hunch about this topic? What do you think might be happening, or what do you want to find out? Don't worry about being precise — I'll help you sharpen it."

### 1c. Ask for available papers

> "Do you have papers you'd like me to work with? You can upload PDFs now, or we can proceed with what you have and add more later."

### 1d. Establish a project name

Ask the user for a project name (used for all spreadsheet files downstream).

**Output of Phase 1:** A working statement of the research topic, the user's initial ideas, and any uploaded papers.

---

## Phase 2 — Skim Papers for Broad Understanding

Invoke the **paper-skimmer** skill on all provided papers. If the user hasn't provided papers yet, ask them to upload PDFs or provide references.

### How to invoke paper-skimmer

Follow the paper-skimmer SKILL.md workflow:
- Use the project name from Phase 1
- For each paper: read the title, abstract, introduction (especially "The Current Study" section), and conclusion
- Extract: Authors, Year, Title, Research Question/Purpose, Method Summary (from abstract only), Key Findings (from abstract and conclusion)
- Save to `{project}_papers.xlsx`

### After skimming, synthesize

After all papers are skimmed, present a brief synthesis to the user:

> **Here's what I found across your [N] papers:**
> - **Dominant theoretical frameworks:** [list the main theories/models that appear]
> - **Common phenomena studied:** [what DV/IV patterns emerge]
> - **Converging findings:** [where do papers agree]
> - **Tensions or contradictions:** [where do papers disagree or leave uncertainty]
> - **Populations and contexts:** [who has been studied, where]

This synthesis primes the gap-identification conversation in Phase 4.

### After synthesis, extract evidence

For each skimmed paper, apply the **Article-Level Evidence Extraction** protocol (see above). During skimming, extract 3–5 key claims per paper — focusing on:
- Empirical findings with their original in-text citations
- Theoretical framing statements with citations
- Gap statements relevant to the user's emerging research interest

Store these extracted items for use during Phase 8 (Draft). Present a brief summary to the user:

> **I also extracted [N] key claims from across your papers that we can draw on when writing. Here are the most notable ones:**
> - [Claim 1 — paraphrased] (Original citations: Author, Year; Author, Year — from Source Article)
> - [Claim 2 — paraphrased] (...)
> [etc., top 5-8 most relevant]

---

## Phase 3 — First Paper Selection (Broad Relevance)

Invoke the **paper-selector** skill to filter papers by broad relevance to the user's research topic.

### How to invoke paper-selector

Follow the paper-selector SKILL.md workflow:
- Use the research topic and initial ideas from Phase 1 as the research profile
- Score papers by theoretical alignment and topic relevance
- Produce a "Selected" sheet in the project spreadsheet

### After selection

Report how many papers were selected and which were filtered out:

> "From your [N] papers, I've identified [M] as most relevant to your topic. The selected papers cluster around [main themes]. [K] papers were filtered out because [reasons]."

---

## Phase 4 — Elaborate Ideas and Identify Research Gaps

This is the intellectual heart of the skill. Through several rounds of Q&A, help the user move from a broad idea to 2-3 specific, theoretically grounded research gaps.

### 4a. Theoretical Landscape Discussion

Based on the skimming synthesis, ask the user about the theoretical landscape:

> **Looking at the theories and frameworks across your papers, I see [summary]. Let me ask you some questions to sharpen your thinking:**

Ask 2-3 multiple-choice questions (3-4 options + "None of the above") about the theoretical positioning:

> **Where do you see the most important theoretical tension or uncertainty in this area?**
>
> (a) [Tension between Framework A and Framework B — they make competing predictions about X because they differ on Y]
> (b) [Framework C is well-established for Z but hasn't been extended to explain W, which your topic touches on]
> (c) [Most studies assume Mechanism M, but recent work by Author (Year) suggests Alternative Mechanism N — this hasn't been resolved]
> (d) None of the above — please share your own thinking.

### 4b. Gap Identification (Theoretical Focus)

After 2-3 rounds of discussion, propose 2-3 candidate research gaps. **Prioritize theoretical gaps over methodological ones** — the goal is to advance understanding, not just apply a different method.

**Types of gaps to prioritize (in order):**

1. **Theoretical mechanism gaps** — We know X affects Y, but not *how* or *through what process*. A mediating mechanism is theorized but untested.
2. **Theoretical integration gaps** — Two frameworks or research streams address the same phenomenon from different angles but haven't been connected. Bringing them together would create new predictions.
3. **Boundary condition gaps** — A theoretical prediction is well-supported in Context A, but the theory itself suggests it should operate differently in Context B — and nobody has tested this.
4. **Construct refinement gaps** — A key construct is defined and measured inconsistently, and the inconsistency masks meaningful differences.

**Types of gaps to de-prioritize:**
- "Nobody has used Method X to study this" (purely methodological)
- "This hasn't been studied in Population Z" (purely demographic replication)
- "More research is needed" (vague, not actionable)

Present each candidate gap with a justification drawn from the skimmed papers:

> **I've identified these potential research gaps based on our discussion and the literature:**
>
> **Gap 1: [Name]**
> [2-3 sentences: what is missing, which papers reveal this, why it matters theoretically]
>
> **Gap 2: [Name]**
> [2-3 sentences]
>
> **Gap 3: [Name]**
> [2-3 sentences]
>
> **Which of these gaps resonates most with your research interests? Would you prioritize them differently, or do you see a gap I've missed?**

### 4c. Refine Through Follow-Up Q&A

After the user responds, conduct 1-2 more rounds of multiple-choice questions to sharpen each gap:

> **For Gap 1 ([name]), which theoretical angle would be most productive to pursue?**
>
> (a) [Angle A — investigating the mediating role of Z between X and Y, following Theorist's framework]
> (b) [Angle B — testing whether X operates through a different mechanism in Context C than in Context D]
> (c) [Angle C — integrating Framework P's predictions about Z with Framework Q's model of the X-Y relationship]
> (d) None of the above — please share your own thinking.

**Output of Phase 4:** 2-3 clearly articulated research gaps, each with theoretical justification from the literature, ranked by the user's priority.

---

## Phase 5 — Formulate Research Questions

Guide the user from gaps to concrete, testable research questions. This is a structured thought process, not just RQ generation.

### 5a. Gap-to-RQ Mapping

For each prioritized gap, walk the user through the logic:

> **Let's turn Gap 1 into a research question. Here's my reasoning:**
>
> The gap says: [restate the gap]
> The theoretical prediction is: [what the theory would expect]
> To test this, we need to ask: [draft RQ]
>
> **Does this research question capture what you want to investigate?**
>
> (a) Yes, this is exactly right.
> (b) Close, but I'd want to focus more on [aspect] — specifically [modification].
> (c) The question is too narrow — I'd rather ask about [broader version].
> (d) The question is too broad — I'd rather ask about [more specific version].
> (e) None of the above — please share your own version.

### 5b. RQ Quality Check

For each finalized RQ, verify it meets these criteria:
- **Specific:** Names the variables and the expected relationship
- **Testable:** Could be answered with an empirical study
- **Theoretically grounded:** Follows from the gap and the theoretical framework
- **Novel:** Not already answered by the reviewed literature
- **Feasible:** Could realistically be studied (don't assess this yourself — ask the user)

Present the final set of RQs for confirmation:

> **Here are your finalized research questions:**
>
> RQ1: [Full statement]
> *Gap addressed:* [Gap name] | *Theoretical basis:* [1 sentence]
>
> RQ2: [Full statement]
> *Gap addressed:* [Gap name] | *Theoretical basis:* [1 sentence]
>
> [RQ3 if applicable]
>
> **Are these ready? Any revisions before we proceed?**

**Output of Phase 5:** 2-3 finalized research questions with gap and theory traceability.

---

## Phase 6 — Second Paper Selection (RQ-Specific)

Now that the RQs are concrete, invoke **paper-selector** again with the refined research questions as the scoring criteria. This second pass identifies papers that are most directly relevant to the specific gaps and RQs — not just the broad topic.

### How to invoke paper-selector (second pass)

- Use the same project spreadsheet
- Update the research profile with the finalized RQs and gap descriptions
- Re-score all papers (including those filtered out in the first pass — a paper irrelevant to the broad topic may be highly relevant to a specific RQ)
- Produce an updated "Selected" sheet

### After selection

> "For your refined research questions, the most relevant papers are [list top-scored papers]. These will anchor the Introduction's argument. I recommend deep reading [top N] of these — they're central to the rationale and logic flow."

Ask the user to confirm which papers to deep-read, and to provide any additional PDFs they want to add.

---

## Phase 7 — Generate Detailed Introduction Outline

Before writing, generate a detailed paragraph-level outline based on:
- The writing guidelines in `resources/introduction_writing_guide.md`
- The hourglass structure (broad → narrow)
- The user's gaps, RQs, and paper collection
- APA-7 style conventions

### Outline Format

Generate the outline with **subsection headers** and **topic sentences** for every paragraph:

```
## Introduction

### [Subsection 1 title — Opening Hook / Broad Context]
¶1: [Topic sentence — Broad accessible statement about the phenomenon and why it matters]
¶2: [Topic sentence — Narrow from the broad phenomenon to the specific theoretical domain]

### [Subsection 2 title — Theoretical Background]
¶3: [Topic sentence — Present Framework A and its key constructs]
¶4: [Topic sentence — How Framework A explains/predicts the core relationship]
¶5: [Topic sentence — Present Framework B or competing perspective, if relevant]
¶6: [Topic sentence — Theoretical integration or tension between frameworks]

### [Subsection 3 title — Empirical Evidence on Theme 1]
¶7: [Topic sentence — Converging evidence for Claim X (cite: Author1, Year; Author2, Year)]
¶8: [Topic sentence — Contradictions or boundary conditions for Claim X]

### [Subsection 4 title — Empirical Evidence on Theme 2]
¶9: [Topic sentence — Evidence related to the second key variable or relationship]
¶10: [Topic sentence — What remains unresolved or inconsistent]

### [Subsection 5 title — Research Gaps]
¶11: [Topic sentence — Gap 1: state the theoretical gap with evidence justification]
¶12: [Topic sentence — Gap 2: state the theoretical gap]
¶13: [Topic sentence — Gap 3 if applicable]

### [Subsection 6 title — The Current Study]
¶14: [Topic sentence — Purpose and rationale of the study]
¶15: [Topic sentence — Research questions/hypotheses]
¶16: [Topic sentence — Brief conceptual overview of the approach and contribution]
```

### Present to the user for approval

> **Here's the proposed outline for your Introduction. Each line is a paragraph topic sentence — the full draft will expand each into a complete paragraph with evidence and citations.**
>
> [Outline]
>
> **Would you like to:**
> (a) Approve this outline and proceed to drafting
> (b) Reorder some sections or paragraphs
> (c) Add or remove paragraphs
> (d) Change the emphasis on certain themes
> (e) Revise specific topic sentences

Wait for the user's approval or revisions. Iterate until they confirm.

**Output of Phase 7:** A finalized paragraph-level outline with subsection headers and topic sentences.

---

## Phase 8 — Draft the Introduction

Write the Introduction section paragraph by paragraph, following the finalized outline.

### Before writing, read the writing guidelines

Read `resources/introduction_writing_guide.md` for the full writing principles, template, and anti-patterns. Apply all of them during drafting.

### Writing Principles (Summary)

1. **Hourglass structure** — Start broad and accessible, narrow progressively to your specific study
2. **Prose, not jargon** — Open in plain language; introduce technical terms through context
3. **Synthesize, don't list** — Organize by themes and arguments, not by individual studies
4. **Every paragraph makes a claim** — Topic sentence states the claim; body provides evidence from multiple sources; closing connects to the next paragraph
5. **The argument drives the structure** — Each paragraph should feel like a logical step toward the research gaps
6. **Theoretical focus** — Prioritize theoretical rationale and mechanisms over procedural details of past studies

### Writing Quality Standards (from academic-paper skill)

- No AI-typical phrases ("delve into," "it is important to note," "a nuanced understanding")
- Varied sentence rhythm (alternate lengths, avoid monotony)
- No throat-clearing openers ("It is widely acknowledged that...")
- Disciplined citation integration (blend narrative and parenthetical citations)
- APA 7th citation format throughout

### Drawing on Extracted Evidence

When writing each paragraph, consult the claims and arguments extracted during skimming (Phase 2) and any on-demand deep reading. These provide:

- **Additional empirical support** for claims being made — use secondary citations to broaden the evidence base
- **Theoretical framing** drawn from how other authors have positioned their arguments — paraphrase and cite with "as cited in"
- **Gap justifications** that other authors have articulated — these strengthen the case for the research gaps

When using extracted evidence:
- Check whether the original source is in the project's paper collection. If yes, cite directly. If no, use secondary citation format.
- Prefer extracted claims that multiple source articles agree on — convergence across sources strengthens the argument.
- Do not over-rely on secondary citations. If a paragraph's core argument rests entirely on secondary citations, flag it and suggest deep-reading the original source or finding it directly.

### On-Demand Deep Reading During Writing

**This is a critical feature.** As you write each paragraph, assess whether the argument being made is **central to the rationale and logic flow** leading to the research gaps and questions. If it is, and the supporting paper has only been skimmed (not deeply read), **pause writing and invoke paper-deep-reader** on that paper before continuing.

#### When to trigger deep reading:

- The paragraph makes a **core theoretical argument** that anchors the rationale for a gap
- The paragraph presents **key empirical evidence** whose specific findings, effect sizes, or methodological details are needed to support the argument
- The paragraph discusses a **contradiction or inconsistency** between studies that is central to identifying a gap
- The paragraph is in the **Research Gaps** or **Current Study** subsection and needs precise justification from specific papers

#### When NOT to trigger deep reading:

- The paragraph provides **broad context** or background that doesn't require specific details
- The paper is used as one of several **supporting citations** in a convergence argument
- The information from skimming (abstract-level findings) is sufficient for the argument being made

#### How to deep-read during writing:

1. Pause the drafting process
2. Tell the user: "To write this paragraph well, I need to read [Author (Year)] more carefully — it's central to the argument about [topic]. Let me do a deep read."
3. Invoke paper-deep-reader on that specific paper (follow the paper-deep-reader SKILL.md workflow, including the multiple-choice interactive questions)
4. After deep reading produces the integrated paragraph summary, **apply the Article-Level Evidence Extraction protocol** — extract all relevant claims and arguments from the full text with their original in-text citations. Deep reading yields richer extraction than skimming: capture nuanced findings, specific effect sizes, methodological qualifications, and theoretical reasoning chains with their citations.
5. Resume writing with both the enriched understanding and the newly extracted evidence. Use secondary citation format ("as cited in") for any original citations encountered in the paper, unless those original sources are also in the project's paper collection.

This means the writing process may alternate between drafting and deep-reading. That's intentional — it mirrors how researchers actually write, going back to papers when they need more detail for a specific argument.

### Drafting Process

Write section by section, following the outline. After completing each subsection (not each paragraph), present it to the user:

> **Here's the draft of [Subsection Name]:**
>
> [Subsection text with all paragraphs]
>
> **How does this read? Any points to strengthen, reframe, or adjust?**

Incorporate feedback before moving to the next subsection.

After all subsections are drafted, compile the fu