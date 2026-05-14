# Layer 1 Operations — Researcher Model

## Location

All Layer 1 files live in `layer1-researcher/`:
- `narrative-profile.md` — descriptive summary of the researcher
- `rules/` — one markdown file per rule category
- `override-log.yaml` — logged rule overrides across projects
- `my-publications/` — the researcher's own publications (PDFs or preprocessed markdown)
- `my-publications.yaml` — registry of publications with extraction status and metadata

## Initialize Layer 1 (First-Time Interview)

If `narrative-profile.md` does not exist or is empty, conduct a structured interview to help the user articulate their researcher identity.

### Interview Structure

Use AskUserQuestion for each section. The interview has three parts:

**Part 1: Narrative Profile**

Explore the following areas through conversation (not rigid questionnaire):

1. **Research Interests**: What areas of developmental psychology are you most drawn to? What questions keep you coming back?

2. **Theoretical Orientation**: Do you lean toward particular theoretical frameworks (e.g., dynamic systems, nativist, constructivist, ecological, sociocultural)? How do you think about development — as continuous or stage-like, domain-general or domain-specific?

3. **Preferred Level of Explanation**: Do you gravitate toward mechanistic explanations, computational models, behavioral descriptions, or contextual accounts? How do you think about the relationship between levels (neural, cognitive, behavioral, social)?

4. **Scientific Style**: Are you more hypothesis-driven or exploratory? Do you prefer focused, tightly controlled studies or broader, more ecological designs? How do you weigh internal vs. external validity?

5. **General Thought Flow**: How do you typically move from reading to reasoning to writing? Do you start with theory and look for evidence, or start with phenomena and build explanations?

If the user has publications available in `my-publications/`, read them first to inform the interview. The publications reveal the researcher's actual practices — see "Extract from Publications" below.

After the conversation, draft `narrative-profile.md` as a coherent narrative (not bullet points) and present for approval.

**Part 2: Categorized Rules**

For each category, ask the user about their preferences and formalize them as rules. Each rule should:
- Be stated clearly
- Include cross-category links if applicable (e.g., "Affects: Writing Style")
- Be understood as a moderate constraint, not rigid

Categories and example probing questions:

- **Literature Selection** (`rules/literature-selection.md`): What makes you pick up a paper? How do you decide what's worth reading deeply? Do you prefer recent work or canonical studies? How do you handle papers outside your main area?

- **Interpretation** (`rules/interpretation.md`): How do you interpret null results? How cautious are you about causal language? Do you prefer conservative or bold interpretations?

- **Method Evaluation** (`rules/method-evaluation.md`): What methodological standards do you hold? How do you weigh sample size vs. design elegance? What are dealbreakers?

- **Research Evaluation** (`rules/research-evaluation.md`): How do you evaluate the quality of a study overall? What do you look for first? What flaws are forgivable vs. fatal?

- **Reasoning Style** (`rules/reasoning-style.md`): How do you build an argument? Do you prefer deductive or abductive reasoning? How do you handle competing explanations?

- **Writing Style** (`rules/writing-style.md`): How formal is your writing? Do you prefer dense or accessible prose? How do you structure a literature review — chronologically, thematically, or by argument?

For each category, draft a markdown file with 3-7 rules. Each rule has:
```markdown
## Rule: [Short name]

[Rule statement]

- **Strength**: moderate / strong
- **Affects**: [other categories this influences]
- **Depends on**: [other categories or rules this draws from]
- **Override condition**: [when it's acceptable to deviate]
```

Present each category for approval before saving.

**Part 3: Cross-Category Review**

After all rules are drafted, review cross-category links for consistency. Present a summary of how rules interact across categories.

## My Publications — Source Material for Layer 1

The researcher's own publications are the strongest evidence for their researcher model. They reveal actual writing style, reasoning patterns, theoretical commitments, methodological preferences, and interpretive habits — far more reliably than self-report alone.

### Adding Publications

1. User provides publications placed in `my-publications/`. Two formats are supported:

   **Format A — Raw PDF** (fallback):
   ```
   my-publications/Zeng_2024_ShortTitle.pdf
   ```

   **Format B — Preprocessed markdown** (preferred, 3-5x cheaper in tokens):
   ```
   my-publications/
     Zeng_2024_ShortTitle.pdf          # original (may be kept or removed)
     Zeng_2024_ShortTitle.md           # full text as markdown
     Zeng_2024_ShortTitle_meta.json    # structured metadata
     fig1.png                          # extracted figures (same folder)
   ```

   **Format detection**: If `my-publications/Name.md` exists (same base name as PDF) → use Format B (read .md). Otherwise → use Format A (read PDF directly). Broken image links in markdown are expected — use caption text and skip missing files.

2. For each publication, create a registry entry in `my-publications.yaml`:
   ```yaml
   - id: PUB-001
     citation: "Zeng, G., et al. (2024). Title of paper. Journal Name, Vol(Issue), pages."
     file: "my-publications/Zeng_2024_ShortTitle.pdf"
     year: 2024
     topics: [topic1, topic2, topic3]
     extraction_status: pending  # pending | extracted | updated
     extracted_date: null
     extraction_notes: ""
   ```
3. Name files clearly: `AuthorLastName_Year_ShortTitle` (with `.pdf`, `.md`, or `_meta.json` extension)

### Extracting from Publications

When processing a publication for Layer 1, detect format (markdown preferred over PDF for token efficiency) and read the paper carefully. Extract:

**Writing Style Evidence:**
- Prose style: formal/accessible, dense/clear, hedging patterns
- Paragraph and argument structure
- How literature is integrated (parenthetical vs. narrative citation style)
- Introduction structure: funnel, gap-spotting, or theoretical framing
- Transition patterns between ideas
- Typical sentence complexity and vocabulary level

**Reasoning Style Evidence:**
- How arguments are constructed: deductive, inductive, abductive
- How competing explanations are handled
- How limitations are framed
- Causal language patterns (cautious, moderate, bold)
- How theoretical claims connect to empirical evidence

**Theoretical Orientation Evidence:**
- Which theoretical frameworks are invoked and how
- How phenomena are explained (mechanistic, functional, contextual)
- Level of analysis preferred (neural, cognitive, behavioral, social)
- Developmental models referenced or assumed

**Methodological Preferences Evidence:**
- Study designs chosen and why
- How statistical evidence is presented and interpreted
- What methodological limitations are acknowledged
- Attitude toward replication, effect sizes, Bayesian approaches

**Interpretation Patterns Evidence:**
- How null results are handled
- How unexpected findings are framed
- Degree of generalization from specific findings
- How the Discussion section moves from results to implications

### Applying Extractions to Layer 1

After extracting from a publication:

1. **Compare with existing Layer 1 content**: Read `narrative-profile.md` and relevant `rules/` files
2. **Identify confirmations**: Evidence that supports existing rules or profile descriptions → strengthen confidence
3. **Identify additions**: New patterns not yet captured → propose new rules or profile updates
4. **Identify tensions**: Evidence that contradicts existing rules → flag for user discussion (the user may have evolved, or the paper may be context-specific)
5. **Propose specific updates**: For each proposed change, cite the publication and specific section/pattern
6. **Apply after approval**
7. **Update the registry**: Set `extraction_status: extracted`, `extracted_date: [today]`, and note what was extracted in `extraction_notes`

### Batch Processing

When the user provides multiple publications at once (e.g., during initial setup):

1. Process chronologically (oldest first) to capture evolution over time
2. After processing all, synthesize: note patterns that are consistent vs. those that changed
3. Present a consolidated set of proposed Layer 1 updates
4. Flag any evolution over time (e.g., "Your earlier work used X framing, but your recent papers shifted to Y")

### On-Demand Update from New Publication

When the user publishes something new:
1. Add the PDF and registry entry
2. Extract as above
3. Pay special attention to what's **new or different** compared to earlier work
4. Propose targeted updates to profile and rules

## View or Edit Narrative Profile

Read and display `narrative-profile.md`. If the user wants to edit, help them revise and save.

## View, Add, or Edit Rules

Read the relevant `rules/[category].md` file. Support:
- Viewing all rules in a category
- Adding a new rule
- Editing an existing rule
- Adding or updating cross-category links

## On-Demand Update

When the user wants to integrate new thinking:
1. Listen to what they want to add or change
2. Determine which component it affects (profile or which rule category)
3. Propose specific edits
4. Apply after approval

## Post-Project Reflection

Triggered during project archiving. This is the most important update mechanism.

### Process

1. **Read the override log**: Read `projects/archived/[project]/override-log.yaml`. For each override, consider:
   - Was the override a one-time exception, or does it suggest the rule needs updating?
   - Did the override lead to better outcomes?

2. **Review project decisions**: Consider the overall project trajectory:
   - What theoretical choices were made?
   - What interpretive stances were taken?
   - Were there new methodological preferences that emerged?

3. **Propose updates**: For each proposed change:
   - State what would change (rule modification, new rule, profile update)
   - Explain why, based on the project evidence
   - Classify as: strengthen existing rule, weaken existing rule, add new rule, modify profile

4. **Apply after approval**: Only update files after the user confirms each change.
