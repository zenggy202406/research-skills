---
title: Evidence Integrity Rules
version: "1.0.0"
created: "2026-05-14"
scope: "All writing skills that produce academic prose — discussion-writer, intro-writer, lit-review-generator, and any future writing skill."
---

# Evidence Integrity Rules

Mandatory rules for all writing skills that produce academic text. These rules ensure that every written output is grounded in evidence, transparent about uncertainty, and free from fabrication.

**Used by**: discussion-writer, intro-writer, lit-review-generator, and any writing skill that generates prose for academic manuscripts.

---

## Rule 1 — No Fabrication (Absolute)

**Never fabricate any of the following:**
- Paper titles, author names, publication years, journal names, DOIs
- Statistical results, effect sizes, p-values, confidence intervals, sample sizes
- Quotes, paraphrases, or claims attributed to specific sources
- Dates, decisions, approvals, or data that were not provided by the user or found in the KB

**If you are unsure whether something is real, do not include it.** Say you don't know and ask the user.

This rule has no exceptions. It applies regardless of how plausible the fabricated content might seem.

---

## Rule 2 — Evidence-First Writing

Every empirical claim in the output must be traceable to one of these sources (in priority order):

1. **Knowledge Base Layer 3** — `claims.yaml`, `arguments.yaml`, `papers-reference.md`
2. **Knowledge Base Layer 2** — `field-summary.md`, `graph.yaml` (by concept ID)
3. **User-provided data** — results, papers, or information the user shared in the conversation
4. **Search results** — papers found via article-search and approved by the user
5. **Clearly flagged reasoning** — logical inferences the writer makes, explicitly marked (see Rule 3)

If no evidence exists for a claim, do not write it as if evidence exists. See Rule 3 for how to handle unsupported ideas.

---

## Rule 3 — Transparent Handling of Unsupported Ideas

When the writing flow logically calls for a point but no evidence supports it, follow this protocol:

### 3a. Flag It

Mark the unsupported idea with a visible flag:

> ⚠️ UNSUPPORTED: [the idea or claim]. No evidence found in the KB or search results.

### 3b. Present Options to the User

> **Options:**
> (a) Search for evidence — I can invoke article-search (Stage 3) to look for papers supporting this point
> (b) Include with explicit hedging — write it as a cautious speculation with appropriate language (see 3c)
> (c) Remove it — drop this point from the writing
> (d) You provide a source — point me to a paper or reference

### 3c. If the User Chooses to Include Without Evidence

Use cautious, transparent language that clearly separates speculation from evidence. Acceptable phrasings:

- "One possible explanation is that..." / "It is plausible that..."
- "Although no empirical evidence directly addresses this point, it is conceivable that..."
- "We speculate that... however, this interpretation remains untested."
- "To our knowledge, no prior study has examined... Future research might explore..."
- "This finding tentatively suggests... though this interpretation should be treated with caution."

**Never use:** "Research shows that..." / "Studies have found that..." / "Evidence suggests that..." / "It is well established that..." — unless you can point to the actual evidence.

### 3d. Maintain a Speculation Log

During drafting, keep a running count of speculative/unsupported points in the output. If the density exceeds approximately 1 speculative claim per 3 paragraphs, pause and alert the user:

> "The current draft has [N] speculative points across [M] paragraphs. This is getting speculation-heavy. Should we search for more evidence, or are you comfortable with this density?"

---

## Rule 4 — Sound Logic Flow

When evidence is absent but the writing offers an interpretation or explanation, the logic must be sound:

1. **State the finding clearly** — what was actually observed
2. **Acknowledge the absence** — "no prior evidence directly addresses this"
3. **Present the reasoning chain** — explain the logical steps from finding to interpretation
4. **Identify assumptions** — what must be true for this interpretation to hold
5. **Note alternative explanations** — what else could explain the finding
6. **State the testable prediction** — what future study would confirm or disconfirm this interpretation

A well-reasoned speculation with transparent assumptions is scientifically valuable. An unsupported assertion dressed as established fact is not.

---

## Rule 5 — Secondary Citation Integrity

When using claims extracted from within an article (not from the original source directly):

1. **Always use APA 7 secondary citation format:** (Original Author, Year, as cited in Source Article Author, Year)
2. **Never cite the original as if you read it** — unless the original is in the project's paper collection
3. **Flag thin evidence:** If an important argument rests on a single secondary citation, flag it: "⚠️ THIN EVIDENCE: This comparison relies on a single secondary citation."

---

## Rule 6 — Honest Reporting of Null and Absent Evidence

Two distinct situations, handled differently:

### Null findings (the study found no effect)
- Report honestly — null findings are informative
- Explore possible reasons: measurement limitations, developmental timing, sample characteristics, genuine absence of effect
- Do not frame null findings as failures

### Absent evidence (no prior research exists on the specific point)
- Report honestly — "To our knowledge, no prior study has examined..."
- Do not fill the gap with tangential citations that don't actually address the point
- Frame the absence as a contribution: "This study is among the first to..."
- Or frame it as a limitation: "The absence of prior evidence on this specific point limits our ability to contextualize this finding"

**Critical distinction:** Never use tangential citations to create a false impression that evidence exists for a point when it doesn't. A citation that is vaguely related but doesn't actually support the specific claim is worse than no citation — it misleads the reader.

---

## Rule 7 — Confidence Calibration

When making interpretive claims, calibrate language to the strength of evidence:

| Evidence Strength | Language |
|-------------------|----------|
| Multiple converging studies in KB | "Consistent with a robust body of evidence..." / "Converging evidence indicates..." |
| 2-3 studies, same direction | "In line with prior findings..." / "This is consistent with..." |
| 1 study, direct support | "This aligns with [Author, Year], who found..." |
| 1 secondary citation | "This appears consistent with [Author, Year, as cited in...]" + ⚠️ THIN EVIDENCE flag |
| Logical inference, no evidence | "We speculate that..." / "One possible explanation..." |
| Contradicts prior evidence | "Contrary to [Author, Year]..." — then explore why |

---

## How Writing Skills Should Reference This File

At the start of any writing phase (before generating prose), the writing skill should:

1. Read this file: `modules/kb-writing/shared/evidence-integrity-rules.md`
2. Apply all rules during drafting
3. Include a brief evidence-integrity check at the end of the draft, reporting:
   - Number of evidence-grounded claims
   - Number of flagged speculative points
   - Number of thin-evidence warnings
   - Any gaps where article-search was or could be invoked
