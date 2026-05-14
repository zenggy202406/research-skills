# Argument Workflow (Within a Project)

Argument units are structured reasoning structures that bridge knowledge and writing. They organize claims, theoretical grounding, and critical analysis into a coherent reasoning unit. Arguments are proposed by Claude after deep reading and claim extraction, then reviewed and refined by the user.

## Propose Arguments

After a set of claims has been extracted and (ideally) refined, Claude proposes argument units:

### Process

1. Read the project's `claims.yaml` (focus on refined claims, but drafts can inform proposals too)
2. Read the project's `paper-network.yaml` to identify clusters, converging/contradicting evidence, and bridge papers
3. Read the project's `overview.md` for research questions and aims
4. Read relevant Layer 2 concepts from `graph.yaml` for theoretical grounding
5. Read `layer1-researcher/rules/reasoning-style.md` for the researcher's reasoning preferences

Use the paper network to guide argument construction:
- `converging_evidence` edges → natural multi-source argument premises
- `contradicting_evidence` edges → inform counterargument sections
- `extends` edges → trace intellectual lineage within an argument
- Isolated papers → may need special handling or serve a unique role

5. For each proposed argument:
   - Identify a conclusion that the evidence supports (aligned with a research question)
   - Select claims that serve as premises, specifying each claim's role
   - Identify Layer 2 concepts that provide theoretical grounding
   - Make explicit any assumptions
   - Articulate counterarguments or competing explanations
   - Define scope conditions

6. Format as:
   ```yaml
   - id: ARG-XXX
     conclusion: "Main claim supported by this argument"
     tags: [keyword1, keyword2, keyword3]
     premises:
       - claim_id: CLM-001
         claim_hint: "Short description of the claim"
         role: "Establishes baseline finding"
       - claim_id: CLM-005
         claim_hint: "Short description of the claim"
         role: "Provides developmental evidence"
     theoretical_grounding:
       - concept_id: CON-003
         concept_hint: "Dynamic Systems Theory"
         explanation: "Dynamic systems theory predicts this pattern because..."
     assumptions:
       - "Participants are typically developing"
       - "Task demands are comparable across age groups"
     counterarguments:
       - "Alternative: the effect could be driven by task familiarity rather than cognitive development"
     scope_conditions:
       - "Holds for Western, middle-class samples"
       - "Age range 3-6 years"
     notes: ""
     history:
       - version: 1
         date: "[today]"
         conclusion: "[same]"
         changed_by: "Claude-proposed"
   ```
   - **tags**: 2-5 lowercase keyword tags for semantic filtering.
   - **claim_hint**: Short description of the referenced claim, avoiding ID lookup.
   - **concept_hint**: Short name of the Layer 2 concept, avoiding ID lookup.

7. Present each proposed argument to the user for review

## Review and Refine Arguments

For each proposed argument, the user may:

1. **Accept as-is**: Mark as approved
2. **Edit conclusion**: Sharpen or reframe the main claim
3. **Adjust premises**: Add, remove, or reorder claim links; change role descriptions
4. **Revise theoretical grounding**: Change which concepts are cited; improve explanations
5. **Add or modify assumptions**: Make implicit assumptions explicit
6. **Strengthen counterarguments**: Add competing explanations the user knows about
7. **Adjust scope conditions**: Narrow or broaden applicability
8. **Reject**: If the argument doesn't hold together

### After Refinement
Update the argument entry and add a version history entry:
```yaml
history:
  - version: 1
    date: "2026-04-18"
    conclusion: "Original conclusion"
    changed_by: "Claude-proposed"
  - version: 2
    date: "2026-04-19"
    conclusion: "Refined conclusion"
    changed_by: "user-refined"
```

## Relationship to Writing

Arguments inform writing but the mapping is NOT explicit:
- Writers (lit-review-generator, intro-writer) should consult arguments.yaml for structured reasoning
- Arguments provide the logical backbone, but paragraphs may combine, split, or reframe arguments
- No argument-to-paragraph tracking is required

## Search Arguments

### Within a Project
Search `arguments.yaml` by keyword in conclusion, premises, theoretical grounding, scope conditions, or tags.

Use `yaml_manager.py --action list --filter-tags "tag1,tag2"` for tag-based filtering.

### Across Projects
Use `cross_search.py --mode arguments --keyword <keyword> [--tags "tag1,tag2"]`.

This is useful for:
- Finding how a concept was used in argumentation before
- Identifying recurring counterarguments
- Building on prior reasoning in new projects

## When to Propose Arguments

Arguments should be proposed:
- After a substantial set of claims has been extracted and refined (at least 5-10 claims)
- When the user explicitly asks for argument construction
- When transitioning from the reading phase to the writing phase

Do NOT propose arguments prematurely when the evidence base is thin.
