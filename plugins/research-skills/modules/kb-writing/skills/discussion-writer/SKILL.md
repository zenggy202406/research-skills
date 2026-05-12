---
name: discussion-writer
description: "Interactive Discussion section writer for psychology papers with Research Knowledge Base integration. Reads user's Results section, confirms key findings to emphasize, generates paragraph-level outline with topic sentences, then writes one paragraph at a time with user confirmation. Uses Layer 3 claims/arguments as evidence base, Layer 2 concepts for theoretical framing, and Layer 1 writing/reasoning rules. Can skim and search the full Layer 3 article pool for additional context. Enforces grounding policy: unsupported arguments flagged and confirmed with user before inclusion. Triggers on: write discussion, help me write the discussion, discussion section, draft discussion, interpret my results, discuss my findings."
metadata:
  version: "1.0.0"
  created: "2026-04-28"
  updated: "2026-04-28"
  depends_on: "docx"
  status: active
---

# Discussion Writer

An interactive, mentored skill for writing the Discussion section of a psychology research paper. Takes the user from their Results section through interpretation, outline construction, and paragraph-by-paragraph drafting — with the user involved at every decision point.

---

## Trigger Conditions

### Trigger Keywords

**English:** write discussion, write the discussion, discussion section, draft discussion, help me write the discussion, interpret my results, discuss my findings, what do my results mean, discussion for my paper, I need to write the discussion

### Auto-Activation Conditions

This skill should activate when:
1. **User has completed their Results section** and wants help interpreting and discussing them
2. **User asks to write the Discussion section** specifically (not a full paper)
3. **User wants to interpret findings** in the context of prior literature
4. **User is in psychology** (or related behavioral/social sciences) and mentions writing a discussion

### Does NOT Trigger

| Scenario | Use Instead |
|----------|-------------|
| User wants a full research paper (all sections) | academic-paper |
| User wants only a literature review | lit-review-generator |
| User wants to write the Introduction section | intro-writer |
| User wants a research report, not a paper section | deep-research |

---

## Knowledge Base Integration

### Grounding Policy

During writing, strictly observe this priority:
1. **Layer 3 is primary** — all interpretive claims must connect to `claims.yaml`, `arguments.yaml`, and `papers-reference.md`
2. **Layer 2 is supportive** — use `field-summary.md` for conceptual framing and gap awareness; grep specific concepts from `graph.yaml` by ID only when needed
3. **External knowledge is minimal** — do NOT introduce factual claims not in the knowledge base
4. **Unsupported arguments require user confirmation** — if an interpretive point or comparison cannot be grounded in existing KB data, flag it explicitly: "⚠️ UNSUPPORTED: [idea]. I can't find evidence for this in the KB. Should I include it? If so, can you point me to a paper, or should I search for one?"
5. Maintain clear separation between **evidence**, **interpretation**, and **speculation**

### Data Sources in KB Context

Load from the active project folder:

1. **Arguments** (`arguments.yaml`) — Structured reasoning units that connect claims to conclusions. These are the primary anchors for Discussion paragraphs.

2. **Claims** (`claims.yaml`) — Atomic evidence statements extracted from deep-read papers. Every comparison with prior literature should trace to a claim.

3. **Project overview** (`overview.md`) — Research questions, hypotheses, aims, and expected contributions.

4. **Competing explanations** (`competing-explanations.md`) — Alternative theoretical accounts and how the current findings bear on them.

5. **Paper network** (`paper-network.yaml`) — Converging/contradicting evidence links between papers. Use to identify which prior findings to compare results against.

6. **Papers reference** (`papers-reference.md`) — Full list of curated papers with roles and tags. Use to find papers relevant to specific discussion points.

7. **Layer 2 field summary** (`layer2-field/field-summary.md`) — Gaps, open questions, theoretical constraints, methodological limitations, and research guides. Use to frame broader implications and future directions.

8. **Layer 1 rules**:
   - `rules/writing-style.md` — Writing tone and structure preferences
   - `rules/reasoning-style.md` — How arguments should be constructed (abductive reasoning, competing explanations, cautious causal language, mechanism over phenotype, null findings as informative)
   - `rules/interpretation.md` — Interpretive stance

### Searching the Article Pool

When writing the Discussion, the existing claims and arguments may not cover every comparison needed. The skill can:

1. **Search claims** across the project using `cross_search.py` for keywords relevant to a discussion point
2. **Search papers-reference.md** by tags to identify papers that may inform a specific comparison
3. **Skim additional papers** from the project's article pool if needed — check with user first whether to use NotebookLM summaries or raw markdowns before reading any paper
4. If no relevant paper exists in the KB, **flag the gap** and ask the user to find an additional paper

### Article-Level Evidence Extraction

When reading articles — whether skimming papers for additional context (Phase 3/5) or deep reading for critical comparisons — extract key arguments and claims **from within the article's text** along with **the in-text citations the article uses to support them**. These extracted items supplement KB claims/arguments and provide richer evidence for interpreting and contextualizing findings.

#### What to Extract

For each article being read, look for:

1. **Empirical claims with citations** — Factual statements about prior findings that the article supports with references. Example: "Maternal sensitivity during infancy predicts secure attachment at 12 months (Ainsworth et al., 1978; De Wolff & van IJzendoorn, 1997)."
2. **Theoretical interpretations with citations** — How the authors explain mechanisms, invoke frameworks, or connect findings to theory. Example: "From a dynamic systems perspective, self-regulation emerges through repeated co-regulation experiences (Fogel, 1993; Thelen & Smith, 1994)."
3. **Boundary conditions and qualifications** — Claims about when/where effects hold or don't, with supporting citations.
4. **Competing explanations** — Alternative accounts the authors consider, with the evidence they cite for or against each.

**Extraction priority**: Focus on claims and arguments **relevant to interpreting the user's findings** — especially those that support, contradict, or extend the current results.

#### Extraction Format

For each extracted item, record:

```
- Claim/Argument: [Paraphrased content in your own words]
- Original citations: [The in-text citations used in the source article, e.g., "Ainsworth et al., 1978; De Wolff & van IJzendoorn, 1997"]
- Source article: [The article you are reading, e.g., "Smith, 2023"]
- Location: [Section of the article where this appears, e.g., "Discussion, p. 12"]
- Relevance: [Which finding (F1, F2...) this helps interpret]
```

#### Citation Rule: Secondary Citations

Because you have not read the original sources directly — you encountered them cited within another article — you **must** use APA 7 secondary citation format when using these claims in writing:

- **Parenthetical:** (Ainsworth et al., 1978, as cited in Smith, 2023)
- **Narrative:** Ainsworth et al. (1978, as cited in Smith, 2023) demonstrated that...

**Exception:** If the original source is also one of the papers in the project (i.e., you have read or skimmed the original directly), cite it directly without "as cited in."

#### Extraction Depth by Reading Mode

- **During skimming (Phase 3 or 5, when consulting additional papers):** Extract 3–5 key claims per paper from the abstract, introduction, discussion, and conclusion. Focus on interpretive claims and theoretical arguments.
- **During deep reading (on-demand for critical comparisons):** Extract all relevant claims and arguments from the full text, including nuanced interpretations, effect sizes, methodological caveats, and theoretical reasoning chains.

#### Using Extracted Evidence in Writing (Phase 5)

During drafting, the extracted claims and arguments enrich the Discussion:

1. **Paraphrase, never copy** — Restate claims in your own words, adapted to interpreting the current findings
2. **Cite with secondary format** — Always use "as cited in" unless the original source is in the project's paper collection
3. **Integrate, don't dump** — Weave extracted claims into the interpretive argument; do not list them sequentially
4. **Prioritize convergence and divergence** — When multiple articles cite the same original source, the claim is well-established; when articles cite contradicting originals, this is a productive tension to discuss
5. **Flag thin evidence** — If an interpretive comparison rests on a single secondary citation and is central to the argument, flag it: "⚠️ THIN EVIDENCE: This comparison relies on a single secondary citation. Consider finding the original source or additional support."

---

## Overview: The Full Workflow

```
Phase 1: READ RESULTS    → Read user's Results section, extract all findings
Phase 2: PRIORITIZE       → Confirm with user which findings to emphasize vs. treat briefly
Phase 3: EVIDENCE SCAN    → Search KB for relevant claims, arguments, and comparisons
Phase 4: OUTLINE          → Generate paragraph-level outline with topic sentences
Phase 5: DRAFT            → Write one paragraph at a time, user confirms each before next
Phase 6: COMPILE          → Assemble full Discussion, final review, generate .docx
```

Each phase involves the user. No phase proceeds without user confirmation.

---

## Phase 1 — Read the Results Section

### 1a. Receive the Results

Ask the user to provide their Results section (paste text, upload document, or point to a file).

> "Please share your Results section — you can paste it here, upload a document, or tell me where the file is."

### 1b. Extract All Findings

Read the Results section carefully and extract every finding into a structured list:

For each finding:
- **Finding ID** (F1, F2, F3...)
- **Description** (plain language)
- **Statistical detail** (test, p-value, effect size if reported)
- **Direction and magnitude** (which condition was higher/lower, by how much)
- **Related RQ** (which research question it addresses)
- **Status** (significant / non-significant / marginal)

### 1c. Present the Extracted Findings

> **Here are the findings I extracted from your Results section:**
>
> F1: [description] — [stat] — Addresses RQ[X]
> F2: [description] — [stat] — Addresses RQ[X]
> ...
>
> **Did I miss anything, or do any need correction?**

Wait for user confirmation before proceeding.

---

## Phase 2 — Prioritize Findings for Discussion

### 2a. Ask for Emphasis Priorities

Not all findings deserve equal discussion depth. Ask the user to categorize:

> **Which findings do you want to discuss in depth, and which can be briefer?**
>
> For each finding, I suggest one of three levels:
>
> **Deep** — Central to your contribution. Gets its own paragraph(s) with theoretical interpretation, comparison to prior work, and mechanistic speculation.
>
> **Moderate** — Important but not the centerpiece. Gets a paragraph shared with related findings, with brief comparison to prior work.
>
> **Brief** — Peripheral, expected, or confirmatory. Mentioned in passing, perhaps grouped with other brief findings.
>
> Here's my suggested prioritization based on your RQs and the significance of the findings:
>
> [Present each finding with a suggested level and brief rationale]
>
> **Do you agree with these priorities, or would you adjust any?**

### 2b. Ask About Null Findings

Following the Layer 1 reasoning rule "Null Findings as Informative":

> **You have [N] non-significant findings. How would you like to handle them?**
>
> (a) Treat as informative — explore why the predicted effect may not have appeared (measurement, developmental stage, design constraints, genuine absence)
> (b) Mention briefly and move on
> (c) Some are informative, some can be brief — let me specify

### 2c. Ask About Unexpected Findings

If any findings were unexpected or contradictory:

> **Finding F[X] seems unexpected based on the hypotheses in your Introduction. Would you like to:**
>
> (a) Discuss it in depth — this is an important result that needs theoretical explanation
> (b) Acknowledge it but defer to future research
> (c) I actually expected this — let me explain

**Output of Phase 2:** A prioritized findings list with emphasis levels confirmed by the user.

---

## Phase 3 — Evidence Scan: Search KB for Comparisons

### 3a. Map Findings to KB Evidence

For each finding marked "Deep" or "Moderate," search the KB:

1. **Search arguments.yaml** — Which argument units are relevant to interpreting this finding?
2. **Search claims.yaml** — Which prior claims can this finding be compared against?
3. **Search paper-network.yaml** — Which papers have converging or contradicting evidence?
4. **Check competing-explanations.md** — Does this finding bear on any theoretical debate?

### 3b. Identify Gaps in KB Coverage

For each finding, assess whether the KB has sufficient evidence for the Discussion. If not:

> **For Finding F[X], I couldn't find KB evidence for:**
> - [Comparison point that lacks a claim or paper]
>
> **Options:**
> (a) I can search the broader article pool (papers-reference.md) for papers that might address this — should I skim them? (If so: summary or raw markdown?)
> (b) Can you point me to a specific paper for this?
> (c) Skip this comparison — it's not essential

### 3c. Extract Evidence from Consulted Papers

For each paper consulted during the evidence scan — whether from the KB or newly skimmed — apply the **Article-Level Evidence Extraction** protocol. Extract claims and arguments with their original in-text citations, focusing on:
- How other authors interpreted similar or related findings
- Theoretical explanations they invoked, with the citations they used
- Boundary conditions or qualifications on their claims

This extraction supplements the KB's structured claims with richer interpretive context drawn directly from how authors discuss their findings.

### 3d. Present the Evidence Map

> **Here's what I found in the KB for each prioritized finding:**
>
> **F1:** [finding] — Connects to ARG-[X], CLM-[Y], CLM-[Z]. Converges with [Paper A], contradicts [Paper B].
> **F2:** [finding] — Connects to ARG-[X]. Limited prior evidence — may need additional paper.
> ...
>
> **I also extracted [N] claims from the papers I consulted that can enrich the Discussion. Key ones:**
> - [Claim — paraphrased] (Original citations: Author, Year — from Source Article) → relevant to F[X]
> - [...]
>
> **Does this coverage look right? Any comparisons I should add or skip?**

**Output of Phase 3:** An evidence map linking each finding to KB claims, arguments, papers, **and extracted article-level evidence with original citations**.

---

## Phase 4 — Generate Discussion Outline

### Structure: The Inverse Hourglass

The Discussion is the **bottom half** of the hourglass — it starts specific and broadens:

```
SPECIFIC:  Summary of key findings (what you found)
  ↓        Interpretation of findings in light of theory and prior work
  ↓        Comparison with prior literature (convergences, divergences)
  ↓        Alternative explanations and limitations
  ↓        Broader implications (theoretical, practical, methodological)
BROAD:     Future directions and closing statement
```

### Outline Format

Generate a paragraph-level outline with topic sentences:

```
## Discussion

### Opening: Summary of Key Findings
¶1: [Topic sentence — Restate the primary finding(s) and their implications in conceptual terms. Do NOT repeat statistical details.]

### Interpretation of [Theme 1 — e.g., Temporal Dissociation]
¶2: [Topic sentence — Interpret the central finding in light of the theoretical framework from the Introduction]
    KB grounding: ARG-XXX, CLM-XXX
¶3: [Topic sentence — Compare with specific prior findings — convergence or extension]
    KB grounding: CLM-XXX vs. F1

### Interpretation of [Theme 2 — e.g., Social Specificity]
¶4: [Topic sentence — ...]
    KB grounding: ARG-XXX, CLM-XXX
¶5: [Topic sentence — ...]

### Interpretation of [Theme 3 — e.g., Individual Differences]
¶6: [Topic sentence — ...]
¶7: [Topic sentence — ...]

### Null or Unexpected Findings
¶8: [Topic sentence — Address non-significant results as informative]

### Alternative Explanations and Limitations
¶9: [Topic sentence — Consider at least two competing explanations for the key findings]
    Source: competing-explanations.md
¶10: [Topic sentence — Methodological limitations and what they constrain]

### Broader Implications
¶11: [Topic sentence — Theoretical implications — what does this change about how we understand X?]
¶12: [Topic sentence — Practical or methodological implications]

### Future Directions and Closing
¶13: [Topic sentence — Specific, actionable future research questions arising from this work]
¶14: [Topic sentence — Closing statement — broad significance, end with a bang not a whimper]
```

### Present to User

> **Here's the proposed outline for your Discussion. Each line is a paragraph with its topic sentence and KB grounding.**
>
> [Outline]
>
> **Would you like to:**
> (a) Approve and proceed to drafting
> (b) Reorder sections or paragraphs
> (c) Add or remove paragraphs
> (d) Change emphasis
> (e) Revise specific topic sentences

Wait for approval. Iterate until confirmed.

**Output of Phase 4:** A finalized paragraph-level outline with topic sentences and KB grounding annotations.

---

## Phase 5 — Draft the Discussion

### Writing Principles

Before drafting, read the full writing guide: `resources/discussion_writing_guide.md` (in the skill folder). It contains the 10 writing principles (from Bem 2004 + Layer 1 rules), the inverse hourglass template, examples of good vs. bad Discussion prose, and anti-patterns to avoid.

Key principles (see guide for details and examples):
1. Open with what you learned, not what you did
2. Each statement should contribute something new
3. Interpret at multiple levels (data-close → interpretive → theoretical)
4. Compare with prior work substantively
5. Present competing explanations (Layer 1: abductive reasoning)
6. Use cautious causal language (Layer 1)
7. Treat null findings as informative (Layer 1)
8. Don't dwell compulsively on every flaw
9. End with a bang, not a whimper
10. The Discussion mirrors the Introduction

### Writing Quality Standards

- No AI-typical phrases ("delve into," "it is important to note," "a nuanced understanding," "sheds light on," "underscores the importance")
- Varied sentence rhythm (alternate lengths, avoid monotony)
- No throat-clearing openers ("It is widely acknowledged that...")
- Disciplined citation integration (blend narrative and parenthetical; prefer parenthetical)
- APA 7th citation format
- Write in prose, not jargon — technical terms should already be familiar from the Introduction

### Drawing on Extracted Evidence

When writing each paragraph, consult the claims and arguments extracted during Phase 3 (and any on-demand reading). These provide:

- **Richer comparisons with prior work** — use secondary citations to show how the current findings relate to established evidence
- **Theoretical interpretations** drawn from how other authors have framed similar results — paraphrase and cite with "as cited in"
- **Competing explanations** that other authors have considered — these strengthen the alternative-explanations section

When using extracted evidence:
- Check whether the