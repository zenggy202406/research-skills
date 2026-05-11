---
name: lit-review-generator
description: "Interactive, mentored literature review writing with Research Knowledge Base integration. Generates APA-7 .docx grounded in Layer 3 argument units and claims. When in KB context, uses argument units as organizational anchors, claims as the evidence base, Layer 2 concepts for theoretical framing, and Layer 1 writing style rules. Enforces grounding policy: Layer 3 primary, Layer 2 supportive, no unsupported claims. Triggers on: write literature review, synthesize papers, generate lit review, integrate literature, theoretical background, identify research gaps, generate hypotheses, literature review chapter. Also works standalone with spreadsheets from paper-skimmer/selector/deep-reader."
---

# Literature Review Generator

An interactive, mentored literature review writing experience. Integrates information from skimmed and deeply-read papers, involves the user through critical questioning at every major stage, and produces a comprehensive APA-7 literature review enriched with the user's scholarly perspective — delivered as a formatted Word document.

---

## Trigger Conditions

### Trigger Keywords

**English:** write literature review, generate lit review, synthesize papers, synthesize my literature, integrate papers, literature synthesis, theoretical background, write background section, write theory section, identify research gaps, find gaps, research gaps, generate hypotheses, propose hypotheses, literature review chapter, review of literature, related work section, state of the art, current state of knowledge, what does the literature say, connect my papers, weave papers together, narrative review, integrative review, thematic synthesis, paper synthesis, combine my readings, write up my papers, turn papers into review, literature review draft, APA literature review, dissertation lit review, thesis literature review

**中文:** 寫文獻回顧, 文獻探討, 文獻綜述, 整合論文, 理論背景, 研究缺口, 提出假設, 文獻整合, 撰寫文獻回顧, 文獻分析, 研究假設, 合成文獻, 綜合分析, 研究方向, 論文綜述

### Auto-Activation Conditions

This skill should activate automatically when:
1. **User has completed deep reading** and asks "now what?" or "write it up" or "put it all together"
2. **User mentions writing a literature review** in any context — thesis, dissertation, journal article, coursework
3. **User asks about research gaps** in their collected papers — e.g., "what's missing in the literature?"
4. **User wants hypotheses** generated from their paper collection
5. **User has `*_deep_reading.xlsx` or `*_papers.xlsx`** and asks to synthesize or integrate
6. **User asks for a theoretical background** or "related work" section
7. **User says they need to connect or weave papers together** into a narrative
8. **After paper-deep-reader completes** and the user wants the final pipeline step — e.g., "now write the review"

### Pipeline Context

This is the **fourth and final skill** in the academic pipeline. It:
- **Reads from:** `{project}_papers.xlsx` (skimmed + selected data) and `{project}_deep_reading.xlsx` (integrated paragraph summaries from deep reading)
- **Optionally invokes:** deep-research (for supplementary literature search), paper-reader (for interactive HTML study)
- **Applies standards from:** academic-paper (writing quality), paper-mentor (Bloom-taxonomy questioning)
- **Writes to:** `{project}_literature_review.docx` (APA-7 formatted Word document)

### Knowledge Base Integration

When operating within the Research Knowledge Base context (invoked via `/kb` or when a KB project is active), the literature review writing process is enriched with structured knowledge from all three layers. This is the primary intended use — the KB provides the reasoning scaffolding that transforms a collection of papers into a grounded, defensible review.

#### Grounding Policy

During writing, strictly observe this priority:
1. **Layer 3 is primary** — all claims, evidence, and arguments in the review must trace to the project's `claims.yaml` and `arguments.yaml`
2. **Layer 2 is supportive** — use `field-summary.md` for field orientation (gaps, constraints, guides), and grep specific concepts from `graph.yaml` by ID for theoretical framing. Do NOT read full `graph.yaml`.
3. **External knowledge is minimal** — do NOT introduce factual claims not backed by the knowledge base
4. Maintain clear separation between **evidence** (from claims), **interpretation** (from arguments), and **speculation** (flagged explicitly)

#### Data Sources (replaces standard Step 1)

When in KB context, gather data from the project folder instead of asking for spreadsheets:

1. **Arguments** (`arguments.yaml`) — These are the primary organizational anchors. Each argument unit has a conclusion, premises linked to claims, theoretical grounding linked to Layer 2 concepts, assumptions, counterarguments, and scope conditions. Use these to structure the review's logical flow.

2. **Claims** (`claims.yaml`) — The atomic evidence base. Every empirical statement in the review should be traceable to a claim here (though explicit IDs need not appear in the text).

3. **Deep reading summaries** (`{project}_deep_reading.xlsx`) — Rich paragraph summaries per paper, still used for writing substance.

4. **Skimmed papers** (`skimmed-papers.xlsx`) — Broader context from non-core papers.

5. **Project overview** (`overview.md`) — Research questions, aims, and context. Replaces the research interview if sufficiently detailed.

6. **Competing explanations** (`competing-explanations.md`) — Alternative hypotheses to address in the review.

7. **Project concepts** (`concepts.yaml`) — Project-specific refinements of Layer 2 concepts.

8. **Field summary** (`layer2-field/field-summary.md`) — Compact overview of Layer 2 field intelligence: known gaps, open questions, theoretical constraints, methodological limitations, and research guides. Read this for orientation — it replaces reading full `graph.yaml`. If a specific concept definition is needed, grep `graph.yaml` by ID.

#### Layer 1 Writing Style

Read `layer1-researcher/rules/writing-style.md` and apply these rules as moderate constraints on the writing style — formality, structure preferences, citation density, etc.

#### Modified Workflow in KB Context

- **Step 2 (Research Interview)**: Skip if `overview.md` has clear domain, core idea, and RQs. Confirm with user.
- **Step 3 (Analysis)**: Use argument units as the starting point for theoretical mapping, evidence synthesis, and gap identification instead of deriving these from scratch. The arguments have already been constructed and refined — the analysis step becomes a review and extension rather than a first-pass synthesis.
- **Step 4 (Structure)**: Propose a structure that maps loosely to the argument units. Each major section or theme should correspond to one or more arguments. The mapping is flexible — arguments can be combined, split, or reframed for narrative flow.
- **Step 5 (Writing)**: Ground every paragraph in specific claims and arguments. When a gap is encountered (an argument needs support but no claim exists), flag it: "⚠️ GAP: [description]" and propose a suggestion, clearly marked. Ask the user whether to accept, provide their own content, or search for additional literature.

#### Output in KB Context

Save the .docx to both the project folder and the user's workspace:
- `Research Knowledge Base/projects/active/[project-name]/{project}_literature_review.docx`
- User's workspace folder (for easy access)

When NOT in a KB context, the skill operates exactly as described below — all KB integration steps are skipped.

---

### Does NOT Trigger

| Scenario | Use Instead |
|----------|-------------|
| User wants to skim or extract info from new papers | paper-skimmer |
| User wants to filter/score papers by relevance | paper-selector |
| User wants to do a critical deep reading of papers | paper-deep-reader |
| User wants to write a full research paper (not just lit review) | academic-paper |
| User wants a formal peer review of a manuscript | academic-paper-reviewer |
| User wants a standalone research report | deep-research |

---

## What Makes This Different

This skill treats literature review writing as a **collaborative scholarly activity**, not a one-way generation. Inspired by the paper-mentor approach and the academic-paper writing pipeline, it:

1. Analyzes the paper collection (as before)
2. **Consults the user at key synthesis decisions** — theoretical framing, evidence weighting, gap prioritization
3. **Asks critical questions** at increasing cognitive depth (Bloom's taxonomy) about the literature landscape
4. **Integrates the user's responses** into the writing, creating a review that reflects their scholarly voice and judgment
5. **Applies writing quality standards** from the academic-paper skill to ensure professional prose

The result is a literature review that the user deeply understands and can defend, because they participated in the intellectual work of synthesis — not just the mechanical work of citation.

---

## Step 1 — Gather All Available Data

### Load the project spreadsheets

Ask the user for the project name, then look for these files in their workspace:
- `{project}_papers.xlsx` — the full skimmed collection (Papers sheet + Selected sheet)
- `{project}_deep_reading.xlsx` — the in-depth reading analysis

Read both spreadsheets. The deep-reading spreadsheet contains an **integrated paragraph summary** per paper (300 words max) that weaves together the theoretical rationale, methodology, findings, critical analysis, and the user's own scholarly insights from the interactive reading sessions. These summaries are the primary source for the review — they are dense analytical narratives ready to be synthesized. The skimmed data from non-selected papers provides broader context.

### Build a paper inventory

Create an internal inventory showing:
- Which papers have deep-reading summaries (these are the core papers for synthesis — each has a rich analytical paragraph integrating theory, method, findings, critique, and user insights)
- Which papers have only skimmed data (these can appear as supporting citations)
- The research profile from the Selected sheet (domain, core idea, RQs)

If the user hasn't done the full pipeline (e.g., they have skimmed data but no deep reading), note what's available and adapt. You can still write a review from skimmed data alone — it will be less detailed but still structured and useful.

### Optionally re-read papers

If you find that extracted data is insufficient for a particular paper — missing theoretical detail, unclear methodology, or ambiguous findings — and the user has the PDFs available, ask to re-read specific sections. This is particularly important for papers that will anchor key arguments in the review.

### Supplementary literature search (deep-research integration)

After building the inventory, assess whether the collection has coverage gaps. If the theoretical background needs broader context, or a gap analysis would benefit from knowing what other research exists beyond the collected papers, proactively flag this:

> "Your collection has strong empirical evidence on [topic], but the theoretical background could benefit from broader context on [framework]. Would you like me to run a targeted literature search to strengthen that section?"

If the user agrees, use the deep-research skill in `lit-review` mode to search for additional sources, then integrate the findings into the inventory before proceeding.

---

## Step 2 — Research Interview (if not already captured)

If the research profile is already available from the Selected sheet, confirm it with the user. If not, conduct a brief interview:

1. **Research domain** — the broad field
2. **Core research idea** — the central phenomenon or relationship
3. **Research questions** — the specific questions guiding the project

Then ask two additional questions specific to the literature review:

### Structure preference
> "Which structure works best for your literature review?"
>
> 1. **Thematic synthesis** — Organized by themes or constructs that cut across papers
> 2. **Theoretical → Empirical → Gaps** — Start with theory, then evidence, then what's missing
> 3. **Funnel: broad → narrow** — Classic funnel from domain overview to specific gaps

### Target length
> "How long should the literature review be?"
>
> - Short (2,000–3,000 words) — for a journal article introduction
> - Medium (4,000–6,000 words) — for a thesis chapter or review article
> - Long (7,000–10,000+ words) — for a dissertation chapter

These choices shape the depth and structure of the output.

---

## Step 3 — Analyze Relationships and Identify Gaps (Interactive)

Before writing, perform a systematic analysis of the paper collection. This is the intellectual heart of the skill — the synthesis that transforms a pile of papers into a coherent argument. **This step is now interactive**: after completing each analysis sub-step, consult the user with critical questions before proceeding.

### 3a. Theoretical Mapping

Map the theoretical landscape across all deeply-read papers:
- Which theoretical frameworks appear? How do they relate?
- Are papers using the same constructs but defining them differently?
- Where do theoretical frameworks converge? Where do they diverge?
- What is the dominant theoretical narrative? What alternatives exist?

**User consultation — Theoretical framing:**

Present your theoretical mapping to the user, then ask 2-3 questions at the Analyze and Evaluate levels:

> **Here's what I see in the theoretical landscape across your papers:**
> [Brief summary of the theoretical mapping]
>
> I have a few questions about how you want to frame this:
>
> 1. **[Evaluate]** "Several of your papers use [Framework A] while others draw on [Framework B]. These frameworks make different assumptions about [key difference]. Which perspective do you find more compelling for explaining your core phenomenon, and why?"
>
> 2. **[Analyze]** "I notice that [Author X] and [Author Y] both use the term '[construct]' but define it differently — [definition A] vs. [definition B]. Which definition aligns better with your research questions? Or do you see a way to reconcile them?"
>
> 3. **[Create]** "Based on your reading of these papers, is there a theoretical connection that the authors haven't made explicitly but that you see? Sometimes the most valuable contribution of a literature review is connecting ideas across papers that haven't been in conversation."

Wait for the user's response before proceeding. Their answers will directly shape the theoretical narrative of the review.

### 3b. Methodological Patterns

Identify methodological patterns:
- What designs dominate (experimental, correlational, qualitative)?
- What populations have been studied? What populations are missing?
- What measurement approaches are used? Are they consistent?
- What analytical methods are common?

**User consultation — Methodological assessment:**

> **Methodological patterns I've identified:**
> [Brief summary]
>
> 1. **[Evaluate]** "Most studies in your collection use [dominant design]. From your perspective, is this design sufficient to answer the kinds of questions being asked, or do you see a methodological limitation that the field hasn't addressed?"
>
> 2. **[Analyze]** "The populations studied are predominantly [description]. Does this limit the generalizability of the findings for your research context?"

### 3c. Evidence Synthesis

Synthesize findings across papers:
- Where do findings converge (multiple papers supporting the same conclusion)?
- Where do findings contradict each other? Why might they differ?
- What effect sizes or magnitudes are reported? Are they consistent?
- What moderators or boundary conditions have been identified?

**User consultation — Evidence weighting:**

> **Here's how the evidence lines up:**
> [Summary of convergent and contradictory findings]
>
> 1. **[Evaluate]** "Studies by [Author A] and [Author B] reach opposite conclusions about [relationship]. Based on your deep reading, which study's methodology do you find more rigorous, and does that affect how you weigh the evidence?"
>
> 2. **[Analyze]** "The effect sizes range from [small] to [large] across studies. What factors do you think explain this variation? This will help me frame the evidence section appropriately."

### 3d. Gap Identification (Interactive)

This is the most critical interactive step. Present your initial gap analysis and refine it with the user's input.

Genuine gaps fall into these categories:

**Theoretical gaps:** Constructs or mechanisms that are theorized but untested, or relationships that existing frameworks predict but no study has examined.

**Methodological gaps:** Important questions that have only been studied with one design type (e.g., only cross-sectional, only self-report), or populations that haven't been included.

**Empirical gaps:** Contradictory findings that remain unresolved, moderators that are suspected but untested, or contexts where established findings haven't been replicated.

**Integration gaps:** Theoretical perspectives that exist in parallel but haven't been brought together, or research streams that address the same phenomenon but haven't cross-pollinated.

**User consultation — Gap prioritization:**

> **I've identified these potential research gaps:**
> [List each gap with 1-2 sentences of justification]
>
> 1. **[Evaluate]** "Looking at this list, which gaps do you find most significant for advancing the field? Are there gaps you expected to see that I haven't identified?"
>
> 2. **[Create]** "Based on your reading and your research questions, is there a gap that emerges from connecting ideas across papers — something that might not be obvious from any single paper but becomes visible when you look at the collection as a whole?"
>
> 3. **[Evaluate]** "Which of these gaps is most feasible to address with the kind of research you're planning? A gap that's important but impractical to study is less useful for your project."

A good gap is specific, justified by the evidence in the review, and points naturally toward a feasible study. Vague gaps like "more research is needed" are not useful.

### 3e. Generate Hypotheses (Interactive)

For each gap the user has prioritized, generate one or more research hypotheses. Present them to the user for refinement:

> **Based on the gaps we've identified, here are draft hypotheses:**
> [List each hypothesis with its theoretical rationale]
>
> 1. **[Evaluate]** "Does this hypothesis capture the relationship you expect? Would you modify the direction, the conditions, or the variables?"
>
> 2. **[Create]** "Can you think of a moderating or mediating variable that should be included? Sometimes the most interesting hypothesis isn't 'X affects Y' but 'X affects Y through Z' or 'X affects Y only when W is present.'"

Each hypothesis should:
- Be specific and testable
- Follow logically from the evidence and theory in the reviewed literature
- Name the variables and the expected direction of the relationship
- Be framed in the conventional format: "H1: [Independent variable] will [positively/negatively] affect [dependent variable] when [condition], because [theoretical rationale from the review]."

Revise hypotheses based on user feedback. The final hypotheses should reflect the user's scholarly judgment, not just AI generation.

---

## Step 4 — Plan the Literature Review Structure (Interactive)

Based on the user's structure preference and the analysis from Step 3, plan the document outline before writing.

### Structure A: Thematic Synthesis
```
1. Introduction (research context, purpose, scope)
2. Theme 1: [Name] (weaves multiple papers around a construct)
3. Theme 2: [Name]
4. Theme 3: [Name]
...
5. Synthesis and Emerging Patterns
6. Research Gaps and Hypotheses
7. References
```

### Structure B: Theoretical → Empirical → Gaps
```
1. Introduction (research context, purpose, scope)
2. Theoretical Background
   2.1 [Framework 1]
   2.2 [Framework 2]
   2.3 Theoretical Integration
3. Empirical Evidence
   3.1 [Theme/variable 1]
   3.2 [Theme/variable 2]
   3.3 [Theme/variable 3]
4. Critical Synthesis
5. Research Gaps and Hypotheses
6. References
```

### Structure C: Funnel (Broad → Narrow)
```
1. Introduction (broad domain overview)
2. [Broad topic area]
3. [Narrower focus within the topic]
4. [Specific phenomenon of interest]
5. Current State of Knowledge
6. Research Gaps and Hypotheses
7. References
```

Present the planned outline to the user with:
- Proposed section headings
- Which papers will anchor each section
- How their responses from Step 3 will be woven in

**User consultation — Structure review:**

> **Here's the proposed outline:**
> [Outline with paper assignments]
>
> "Does this structure tell the story you want to tell? Are there papers that should be more prominent, or sections that should be reordered? The introduction will frame the review around [framing from user's theoretical preference], and the gaps section will build toward [prioritized gaps]."

Wait for confirmation and adjust before writing.

---

## Step 5 — Write the Literature Review (Interactive Drafting)

### Writing Principles

**Synthesize, don't summarize.** The most common failure in literature reviews is "Paper A found X. Paper B found Y. Paper C found Z." Instead, organize by ideas: "The relationship between X and Y has been established through multiple methodological approaches (A, 2022; B, 2023), though the mechanism remains debated — some evidence supports [explanation 1] (A, 2022) while others suggest [explanation 2] (C, 2024)."

**Every paragraph should make an argument.** Each paragraph needs a topic sentence stating a claim, evidence from multiple papers supporting or complicating that claim, and a concluding sentence connecting to the next paragraph. Papers are evidence, not the organizing unit.

**Use the deep-reading summaries.** Each paper's integrated paragraph summary from the deep-reading spreadsheet is a dense analytical narrative covering theory, method, findings, critique, and the user's own scholarly perspective. These summaries are your primary raw material — draw on the specific effect sizes, theoretical arguments, methodological assessments, and user insights they contain. This is what distinguishes a substantive review from a surface-level one.

**Weave in the user's perspective.** Where the user expressed opinions during Step 3 (theoretical preferences, evidence weighting, gap assessment), integrate these into the writing. The review should reflect the user's scholarly voice: if they argued that Framework A is more compelling than Framework B, the review's theoretical narrative should reflect that judgment (with supporting evidence).

**Connect, don't just list.** Use transition language that shows relationships: "Building on this finding...", "In contrast to the experimental evidence...", "While these studies establish the main effect, the question of moderators remains...", "This theoretical prediction has been tested empirically by..."

**Be critical and balanced.** Note methodological limitations that affect how findings should be interpreted. Acknowledge contradictions honestly. Evaluate the strength of evidence rather than treating all findings as equally valid.

### Writing Quality Standards (from academic-paper skill)

Apply these quality checks during drafting:

- **No AI-typical terms:** Avoid overused phrases like "delve into," "it is important to note," "a nuanced understanding," "the landscape of," "it is worth noting that." Use natural academic prose.
- **Varied sentence rhythm:** Alternate sentence lengths. Avoid monotonous patterns of similar-length sentences.
- **No throat-clearing openers:** Don't start paragraphs with "It is widely acknowledged that..." or "In recent years, there has been growing interest in..." Get to the point.
- **Varied paragraph lengths:** Mix shorter transition paragraphs with longer analytical ones.
- **Disciplined citation integration:** Blend parenthetical and narrative citations. Don't stack more than 3 citations in a single parenthetical unless making a convergence argument.

### APA 7th Style Requirements

- **In-text citations:** (Author, Year) for one work; (Author1 & Author2, Year) for two authors; (Author1 et al., Year) for three or more
- **Narrative citations:** Author (Year) found that...
- **Multiple citations in same parenthetical:** alphabetical order, separated by semicolons: (Adams, 2020; Baker, 2021; Chen et al., 2022)
- **Direct quotes:** include page number: (Author, Year, p. 42)
- **Headings:** Level 1 (centered, bold), Level 2 (left-aligned, bold), Level 3 (left-aligned, bold, italic)
- **No first-person** unless discussing the author's own research decisions
- **Past tense** for reporting specific findings ("Smith (2022) found..."); **present tense** for discussing established knowledge ("Research demonstrates that...")

### Interactive Drafting Process

Write the review in sections, following the planned outline. **After completing each major section**, present it to the user for review before proceeding to the next:

> **Here's the draft of [Section Name]:**
> [Section text]
>
> "Does this section capture the argument accurately? Are there points you'd like me to strengthen, reframe, or add? I can also adjust the emphasis on particular papers if you feel the balance isn't right."

For the Introduction, ask specifically:

> **[Evaluate]** "The introduction frames your review around [theoretical angle]. Does this framing set up your research questions effectively? Is there anything missing that a reader would need to understand before diving into the detailed review?"

For the Gaps and Hypotheses section, ask:

> **[Create]** "Here are the research gaps and hypotheses as they'll appear in the review. These build directly from our earlier discussion. Is there anything you'd revise now that you see them in the context of the full review? Sometimes the writing process reveals connections we didn't see during the analysis phase."

Wait for the user's response after each major section. Incorporate their feedback before moving on. If the user gives brief responses or says "looks good," take that as approval and proceed. If they offer substantive revisions, integrate them.

After all sections are drafted, compile the reference list in APA 7th format.

---

## Step 6 — Generate the Word Document

Use the docx skill's approach (docx-js via Node.js) to create a properly formatted APA-7 Word document.

Read the docx skill at the standard skill path for the detailed technical instructions on creating .docx files with docx-js.

### APA-7 Document Formatting

- **Font:** Times New Roman, 12pt throughout
- **Margins:** 1 inch on all sides
- **Line spacing:** Double-spaced
- **Page numbers:** Top right corner, starting from title page
- **Running head:** Shortened title in all caps, top left
- **Title page:** Title, author, affiliation, centered
- **Headings:** APA Level 1 (centered, bold), Level 2 (flush left, bold), Level 3 (flush left, bold italic)
- **Paragraphs:** First line indent 0.5 inch (except after headings, block quotes, and titles)
- **References:** Hanging indent 0.5 inch, double-spaced, alphabetical

### Document Structure

```
Title Page
Literature Review body (sections per outline)
Research Gaps and Hypotheses (final body section)
References
```

Save the document as `{project_name}_literature_review.docx` in the user's workspace folder.

---

## Step 7 — Review and Verify

Before delivering, perform a comprehensive quality check. This combines the original verification with writing quality standards from the academic-paper skill.

### Content Quality

1. **Citation audit:** Every paper referenced in text must appear in the reference list, and vice versa. Check for orphaned citations.
2. **Synthesis check:** Scan each paragraph — if any paragraph discusses only one paper, it's a summary, not a synthesis. Revise to integrate.
3. **Gap justification check:** Every gap claimed must be supported by specific evidence from the review (e.g., "Only two studies have examined X, both using Y methodology, leaving Z unexplored").
4. **Hypothesis grounding check:** Every hypothesis must trace back to specific theoretical or empirical content in the review.
5. **User input integration check:** Verify that the user's key insights — both from the deep-reading paragraph summaries (which already contain their scholarly perspective) and from the interactive sessions in Steps 3-5 — are reflected in the final text. The review should feel like it represents their scholarly perspective, not a generic AI output.

### Writing Quality

6. **AI-pattern scan:** Check for overused AI-typical phrases and replace with natural academic prose.
7. **Sentence rhythm check:** Verify varied sentence lengths. No more than 3 consecutive sentences of similar length.
8. **Paragraph structure check:** Every paragraph has a clear topic sentence and concluding transition.
9. **Citation balance check:** Mix of narrative and parenthetical citations. No excessive citation stacking.
10. **APA format check:** Verify citation format, heading levels, and reference list formatting.

If any issues are found, revise before presenting the final document.

---

## Adapting the Interaction Level

Not every literature review session needs the same depth of interaction. Adapt based on cues:

- **User says "just write it":** Skip the interactive consultations (Steps 3-5 questions). Do a standard analysis and write the review without user involvement. Still apply writing quality standards and produce the full document.
- **User gives very brief answers:** Reduce to 1 question per analysis sub-step. Focus on the highest-value decisions: theoretical framing and gap prioritization.
- **User is deeply engaged:** Let the conversation go deeper. Add follow-up questions. Allow tangential discussions about the literature — these often produce the most insightful framing decisions.
- **Time-constrained:** Ask only 3-4 total questions across the entire process: one about theoretical framing, one about evidence weighting, one about gap prioritization, and one about the draft structure.

---

## Supplementary Skills Integration

### Deep-Research Integration

Already described in Step 1. Use the deep-research skill in `lit-review` mode whenever the paper collection needs supplementary sources. This is especially valuable for:
- Strengthening the theoretical background with foundational works
- Identifying additional studies that address a gap the user wants to fill
- Verifying whether a claimed gap is genuine (has anyone published on this since the user's collection was assembled?)

### Academic-Paper Integration

The writing quality standards in Step 5 and the verification checks in Step 7 are drawn from the academic-paper skill's quality framework. Additionally:
- If the user is writing the literature review as part of a larger paper, offer to use the academic-paper skill's `lit-review` mode for additional formatting and style calibration.
- The academic-paper skill's anti-pattern checklist (references/writing_quality_check.md) should be applied during the final verification step.

### Paper-Reader Integration

If the user wants an interactive study environment alongside the written review — for instance, to quiz themselves on the papers or explore glossary terms — offer to invoke the paper-reader skill to create an HTML reader for the core papers. This complements the written review with an interactive learning tool.

---

## Edge Cases

- **Only skimmed data available (no deep reading):** Write a lighter review focused on themes and findings from the skimmed extractions. Flag that the review would be stronger with deeper reading and suggest the user run paper-deep-reader on the core papers. Interactive questions will be less specific without deep-reading data but still useful for framing decisions.
- **Very few papers (< 5):** A traditional multi-section literature review may not be appropriate. Instead, offer a focused integrative summary with clear gap identification. Be transparent: "With 4 papers, I can write a targeted review, but the gap analysis will be tentative." Reduce interactive questions accordingly.
- **Papers span multiple distinct topics:** The user may have papers that cluster into sub-themes. Propose a thematic structure that addresses each cluster and identifies cross-cutting patterns. The interactive consultation is especially valuable here — ask the user how they see the themes connecting.
- **No clear gaps emerge:** This is rare but possible if the research area is mature and well-covered. Be honest about it: "The literature appears fairly comprehensive on this topic. The most promising direction may be [replication in new context / methodological improvement / integration of parallel frameworks]."
- **User wants to add more papers mid-process:** Accommodate it. Re-run the analysis with the expanded set before finalizing.
- **User skips all questions:** That's fine — produce the standard literature review output without interactive enrichment. Don't pressure them.
