# Claim Workflow (Within a Project)

Claims are atomic empirical units — the building blocks of arguments. They are auto-extracted as drafts during deep reading, then reviewed and refined by the user.

## View Claims

1. Read the project's `claims.yaml`
2. Present claims grouped by status (draft vs. refined) and by source paper
3. For each claim, show: ID, statement, conditions, population, method_ref (with method_hint), source (with source_id), tags, status

## Refine a Claim

The user reviews draft claims and refines them. Refinement may involve:

1. **Editing the statement**: Make it more precise, atomic, or accurately scoped
2. **Adjusting conditions**: Narrow or broaden the conditions under which the claim holds
3. **Correcting population**: Specify or generalize the population
4. **Updating method reference**: Link to the correct Layer 2 method node (MET-XXX) and add `method_hint`
5. **Updating tags**: Add or adjust keyword tags for search and filtering
6. **Adding notes**: The user's own interpretation or caveats

### Refinement Process

1. Present the draft claim
2. Ask the user what they'd like to change (or if it's acceptable as-is)
3. Apply edits
4. Update the claim's status from `draft` to `refined`
5. Add a version history entry:
   ```yaml
   history:
     - version: 1
       date: "2026-04-18"
       statement: "Original auto-extracted statement"
       changed_by: "auto-extracted"
     - version: 2
       date: "2026-04-19"
       statement: "Refined statement"
       changed_by: "user-refined"
   ```

## Reject a Claim

If a draft claim is not worth keeping:
1. Ask the user to confirm rejection
2. Remove from `claims.yaml` (or mark with `status: rejected` if the user prefers to keep a record)

## Batch Review

For efficiency, present multiple draft claims from the same paper in sequence:
1. Show claim 1, get feedback (keep/edit/reject)
2. Show claim 2, get feedback
3. Continue until all drafts from that paper are reviewed

## Search Claims

### Within a Project
Search `claims.yaml` by keyword in statement, conditions, population, source, or tags.

Use `yaml_manager.py --action list --filter-tags "tag1,tag2"` for tag-based filtering.

### Across Projects
Use `cross_search.py --mode claims --keyword <keyword>` to search across all projects.

Add `--tags "tag1,tag2"` for tag-based filtering (AND logic — entries must match all tags).

Present results with project name, claim details, and status.

## Versioning

Every edit creates a new version entry in the claim's `history` list. The current fields (statement, conditions, etc.) always reflect the latest version. History preserves only the statement and date for each prior version to keep files manageable.
