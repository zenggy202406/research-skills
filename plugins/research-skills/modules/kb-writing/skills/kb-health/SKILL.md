---
name: kb-health
description: "Knowledge base health check, maintenance, and diagnostics. Validates structural integrity, checks for orphaned references, stale data, paper network consistency, and cross-layer inconsistencies. Also handles project archiving (with Layer 2 promotion and Layer 1 reflection), Layer 1 on-demand updates, and Layer 2 on-demand expansion. Use when: 'check my kb', 'kb health', 'archive project', 'update my researcher profile', 'update Layer 1', 'add concept to Layer 2', 'expand Layer 2', 'kb maintenance', 'consistency check', 'fix my kb'."
metadata:
  version: "2.0.0"
  created: "2026-04-19"
  updated: "2026-04-23"
  depends_on: ""
  status: active
---

# KB Health & Maintenance Skill

This skill handles maintenance, diagnostics, and structural updates for the Research Knowledge Base. It is separate from initialization (`/kb-init`) and daily project operations (`/kb`).

## Knowledge Base Location

All knowledge base files live at: `C:\Users\hp\Desktop\Research Knowledge Base`

Use bash path: `/sessions/lucid-clever-galileo/mnt/Knowledge Base Manage/Research Knowledge Base`

## Shared Resources

Scripts and reference files are in the main kb-skill directory:
- Scripts: `system/kb-skill/scripts/`
- References: `system/kb-skill/references/`

Install PyYAML before using scripts: `pip install pyyaml --break-system-packages`

## Operations

### 1. Health Check / Diagnostics

Run a comprehensive check on the KB and report issues.

#### Structure Check
Verify all expected directories and files exist:
- `kb-state.yaml`, `system/kb-config.yaml`
- `layer1-researcher/narrative-profile.md` and `rules/` with expected categories
- `layer2-field/graph.yaml`, `relationship-schema.yaml`, `concepts/`, `methods/`
- `projects/active/`, `projects/archived/`

#### Consistency Check
1. **Orphaned cross-references**: Scan claims for `method_ref` pointing to non-existent MET-XXX in Layer 2 graph. Scan arguments for `claim_id` pointing to non-existent CLM-XXX in the same project. Scan arguments for `concept_id` pointing to non-existent CON-XXX in Layer 2 graph.

2. **Stale paper references**: Check that `source_id` (PAP-XXX) in claims matches entries in the project's `papers-reference.md`.

3. **Paper network integrity** (for projects with `paper-network.yaml`):
   - All node IDs in `paper-network.yaml` must match entries in `papers-reference.md`
   - All edge `source` and `target` must reference valid node IDs
   - All `shared_claims` entries must reference valid CLM-XXX IDs in `claims.yaml`
   - Node `claim_count` should match actual claim count for that paper's `source_id`
   - Flag approved edges whose `shared_claims` reference claims that have since been rejected or removed

4. **Missing hints**: Scan for cross-references without `_hint` fields (claim_hint, concept_hint, method_hint, target_hint) and report them.

5. **Missing tags**: Scan claims, arguments, and concepts for entries without `tags` lists.

6. **Graph integrity**: Validate all relationships in `graph.yaml` against `relationship-schema.yaml`. Check that relationship targets exist as nodes.

7. **Isolated nodes**: Flag any nodes in `graph.yaml` with zero relationships (neither source nor target in any relationship). Every node must have at least one connection. Report isolated nodes as **Warning** items and recommend adding appropriate relationships using the relationship schema.

8. **Field intelligence integrity**: Check that all field intelligence entries in `graph.yaml` (types: gap, open_question, theoretical_constraint, methodological_limitation, research_guide) have required fields:
   - All types: `id`, `type`, `name`, `statement`, `tags`, `sources`
   - gap: `significance`
   - open_question: `current_state`
   - theoretical_constraint: `implications`
   - methodological_limitation: `impact`, `workarounds`
   - research_guide: `guide_type` (must be `theoretical` or `practical`)

9. **Field summary sync**: Compare `layer2-field/field-summary.md` against `graph.yaml` to ensure:
   - Concept and method counts match
   - Every field intelligence entry in graph.yaml has a corresponding one-line summary in field-summary.md
   - No entries in field-summary.md reference IDs that don't exist in graph.yaml
   - If out of sync, offer to regenerate field-summary.md

10. **State manifest staleness**: Compare `kb-state.yaml` last_updated to current state by re-running:
   ```bash
   python "system/kb-skill/scripts/update_state.py" --kb-root <kb-path>
   ```

#### Report Format
Present findings as:
- **OK**: things that look good
- **Warning**: non-critical issues (missing hints, missing tags, stale network counts)
- **Error**: broken references, missing required files, orphaned network edges

Offer to fix warnings automatically (add missing hints by looking up IDs, add empty tag lists, update stale network node counts).

### 2. Archive a Project

Read `system/kb-skill/references/project-lifecycle.md` for the full archive workflow.

**Summary** — 5 steps:
1. **Confirm** with the user
2. **Check & Move**: Use `archive_project.py --action check` then `--action move`
3. **Create Layer 2 Project Node**: Use `archive_project.py --action summarize`, improve the auto-summary, present for approval, add to graph via `yaml_manager.py`
4. **Propose Layer 2 Promotions**: Use `archive_project.py --action promotions`, present candidates, apply approved ones
5. **Layer 2 Field Intelligence Feedback**: Review the project's findings for generalizable field intelligence updates:
   - **New gaps discovered** during project work → propose new GAP entries
   - **Gaps addressed** (partially or fully) by this project → update existing GAP entry statements
   - **Constraints confirmed/refuted** by project findings → update TC entry implications
   - **New limitations encountered** in hands-on method use → propose new ML entries or update existing ones
   - **New open questions** raised by the project → propose new OQ entries
   - **Concept refinements** from deep engagement → propose edits to concept nodes
   - Present all proposals grouped by type, apply after user approval
   - **Regenerate `field-summary.md`** after any Layer 2 updates
6. **Layer 1 Reflection**: Read `system/kb-skill/references/layer1-operations.md` Post-Project Reflection section. Review override log, project trajectory, propose Layer 1 updates.

```bash
# Archive scripts
python "system/kb-skill/scripts/archive_project.py" --kb-root <kb-path> --project <name> --action <check|move|summarize|promotions>

# Add project node to graph
python "system/kb-skill/scripts/yaml_manager.py" --kb-root <kb-path> --action add-node --entry '<JSON>'

# Update state after archiving
python "system/kb-skill/scripts/update_state.py" --kb-root <kb-path>
```

### 3. Layer 1 — On-Demand Update

Read `system/kb-skill/references/layer1-operations.md` for details.

**From new thinking**: When the user wants to update their researcher model:
1. Listen to what they want to add or change
2. Determine which component it affects (narrative profile or which rule category)
3. Read the current content of that file
4. Propose specific edits with tracked reasoning
5. Apply after user approval

**From a new publication**: When the user has a new publication to add:
1. Place the file in `layer1-researcher/my-publications/`
2. Detect format: if `Name.md` exists (same base name as PDF) → read markdown (preferred, token-efficient); otherwise → read PDF directly. Load `Name_meta.json` for citation info if available. Broken image links in markdown are expected — use caption text and skip missing files.
3. Add a registry entry in `my-publications.yaml` with `extraction_status: pending`
4. Read the paper and extract evidence of writing style, reasoning patterns, theoretical stances, methodological preferences, and interpretation habits (see layer1-operations.md "Extracting from Publications")
5. Compare with existing Layer 1 content — identify confirmations, additions, and tensions
6. Pay special attention to what's **new or different** compared to earlier work
7. Propose targeted updates to profile and rules, citing specific sections
8. Apply after approval, update registry to `extraction_status: extracted`

### 4. Layer 2 — On-Demand Expansion

Read `system/kb-skill/references/layer2-operations.md` for details.

**Manual additions**:
- **Add a concept**: Gather name, definition, boundaries, examples, **and at least one relationship** → add to graph with `yaml_manager.py` → create markdown if complex → regenerate `field-summary.md`
- **Add a method**: Gather details using the method template → add to graph **with at least one relationship** (e.g., `is_measured_by` from a concept) → create markdown file → regenerate `field-summary.md`
- **Add field intelligence** (gap, open question, constraint, limitation, research guide): Gather required fields per type (see `layer2-operations.md` "Add Field Intelligence") → **add at least one typed relationship** (pertains_to, asks_about, constrains, limits, or addresses) → add to `graph.yaml` → regenerate `field-summary.md`
- **Add relationships**: Identify source/target, validate type against schema, add via `yaml_manager.py`
- **Edit existing**: Read current content, propose edits, apply after approval → regenerate `field-summary.md` if field intelligence or coverage changed
- **Register new relationship type**: Add to `relationship-schema.yaml` after validation

**From a new fundamental reading**: When the user has a new foundational text to add:
1. Place the file in `layer2-field/fundamental-readings/`
2. Detect format: if `Name.md` exists (same base name as PDF) → read markdown (preferred, token-efficient); otherwise → read PDF directly. Load `Name_meta.json` for citation info if available. Broken image links in markdown are expected — use caption text and skip missing files.
3. Add a registry entry in `fundamental-readings.yaml` with `extraction_status: pending`
4. Read the paper and compare with the existing graph — identify what's new vs. already covered
5. Extract: new concepts → propose nodes **with relationships**; refinements to existing concepts → propose edits; new methods → propose nodes **with relationships**; new relationships → propose with validation; **new field intelligence** (gaps, open questions, constraints, limitations, guides) → propose entries **with typed relationships**; challenges to existing knowledge → flag. **No isolated nodes** — every new node must connect to at least one existing node.
6. Present all proposals grouped by type (concepts, methods, relationships, field intelligence, challenges)
7. Apply approved changes, update registry entry with `nodes_added`, `relationships_added`
8. **Regenerate `field-summary.md`** to reflect new content

```bash
# Graph operations
python "system/kb-skill/scripts/graph_ops.py" --kb-root <kb-path> --action <search|browse|relations|path|summary|neighbors> [options]

# Add/edit nodes and relationships
python "system/kb-skill/scripts/yaml_manager.py" --kb-root <kb-path> --action <add-node|add-rel> [options]
```

### 5. Refresh State Manifest

Run at the end of any maintenance operation:
```bash
python "system/kb-skill/scripts/update_state.py" --kb-root <kb-path>
```
