# Writing Integration

Writing is grounded in the knowledge base, primarily Layer 3. This reference describes how to connect the knowledge base to the writing skills (lit-review-generator, intro-writer).

## Grounding Policy During Writing

1. **Layer 3 is primary**: All claims, arguments, and evidence cited in writing must come from the project's knowledge base
2. **Layer 2 is supportive**: Concepts and theoretical frameworks from Layer 2 provide framing and context
3. **Layer 1 guides style**: Writing style rules from `layer1-researcher/rules/writing-style.md` shape tone, structure, and register
4. **No unsupported claims**: Do not introduce factual claims that are not backed by a claim unit in `claims.yaml`
5. **Separation discipline**: Clearly distinguish between evidence (from claims), interpretation (from arguments), and speculation (flagged explicitly)

## Preparing for Writing

Before invoking a writing skill, gather the grounding context:

1. Read `projects/active/[project]/arguments.yaml` — these are the reasoning scaffolds
2. Read `projects/active/[project]/claims.yaml` — these are the evidence base
3. Read `projects/active/[project]/overview.md` — research questions and aims
4. Read `projects/active/[project]/competing-explanations.md` — alternatives to address
5. Read relevant Layer 2 concepts from `graph.yaml`
6. Read `layer1-researcher/rules/writing-style.md`

## Invoking lit-review-generator

When the user wants to write a literature review grounded in the knowledge base:

1. Gather all grounding context (above)
2. Invoke lit-review-generator with the following additional context injected:
   - The argument units as the logical structure to organize the review around
   - The claims as the evidence base to draw from
   - Layer 2 concepts for theoretical framing
   - Writing style rules from Layer 1
3. The lit-review-generator should use arguments as organizational anchors — each major section or theme maps loosely to one or more argument units
4. Every empirical statement should be traceable to a claim unit (though explicit IDs need not appear in the text)

## Invoking intro-writer

When the user wants to write an introduction:

1. Gather all grounding context
2. Invoke intro-writer with:
   - The project overview for research questions and motivation
   - Argument units for the logical flow from broad context → gap → research question
   - Layer 2 concepts for establishing the theoretical landscape
   - Writing style rules from Layer 1
3. The introduction should build toward the research questions using the argument structure as a guide

## Gap Detection

During writing, if Claude encounters a point where:
- An argument needs support but no claim exists for it
- A theoretical connection is needed but not represented in Layer 2
- A counterargument should be addressed but isn't in the argument unit

Claude should:
1. **Flag the gap clearly**: "⚠️ GAP: [description of what's missing]"
2. **Propose a suggestion**: Offer what Claude thinks could fill the gap, clearly marked as a suggestion
3. **Ask for input**: Let the user decide whether to:
   - Accept the suggestion (and optionally add it to the knowledge base)
   - Provide their own content
   - Leave the gap for now and return to it later
   - Search for additional literature to fill it

## Writing Output

Writing outputs (literature reviews, introductions, etc.) are saved to the project folder and also delivered to the user's workspace via the writing skill's normal output mechanism (typically .docx via the docx skill).
