# Research-Brain Marketplace

A Claude Code plugin marketplace for academic research workflows and skills.

This repo now exposes **one installable plugin**, `research-skills`, instead of three separate plugins. Inside that plugin, the skills are organized into three workflow modules:

- `paper-pipeline`: literature screening, selection, and close reading
- `kb-writing`: Research Knowledge Base management and mentored section writing
- `academic-pipeline`: upstream end-to-end academic research, writing, review, and revision pipeline

This structure matches Claude Code marketplace behavior: users add one marketplace, install one plugin, and get the complete research skill set.

## Install

For local testing from the marketplace root:

```text
/plugin marketplace add .
/plugin install research-skills@research-skills
```

If you are in the parent folder instead:

```text
/plugin marketplace add ./research-skills
/plugin install research-skills@research-skills
```

For GitHub distribution after publishing:

```text
/plugin marketplace add zenggy202406/research-skills
/plugin install research-skills@research-skills
```

The marketplace catalog lives at:

```text
.claude-plugin/marketplace.json
```

The installable plugin lives at:

```text
plugins/research-skills/
```

## Plugin Layout

```text
research-skills/
  .claude-plugin/
    marketplace.json
  plugins/
    research-skills/
      .claude-plugin/
        plugin.json
      hooks/
        hooks.json
      modules/
        paper-pipeline/
          skills/
        kb-writing/
          skills/
        academic-pipeline/
          commands/
          agents/
          hooks/
          scripts/
          deep-research/
          academic-paper/
          academic-paper-reviewer/
          academic-pipeline/
```

The plugin manifest points Claude Code to all skill locations:

```json
{
  "skills": [
    "modules/paper-pipeline/skills",
    "modules/kb-writing/skills",
    "modules/academic-pipeline"
  ],
  "commands": "modules/academic-pipeline/commands",
  "agents": "modules/academic-pipeline/agents",
  "hooks": "hooks/hooks.json"
}
```

## Skill Overview

### paper-pipeline

| Skill | What it does |
|---|---|
| `paper-skimmer` | Quick-scans papers and extracts structured metadata into a per-project spreadsheet. |
| `paper-selector` | Scores skimmed papers against a project idea or research question and writes a selected-paper sheet. |
| `paper-deep-reader` | Guides close reading with Bloom-taxonomy questions, concise summaries, and optional claim extraction. |
| `paper-reader` | Upstream interactive HTML reader for paper libraries, analysis, quizzes, glossary, and chat. |
| `paper-mentor` | Upstream related-paper discovery, domain mapping, and interactive learning questions. |

### kb-writing

| Skill | What it does |
|---|---|
| `kb` | Daily Research Knowledge Base operations for projects, papers, claims, arguments, search, and writing integration. |
| `kb-init` | First-time Knowledge Base setup for the researcher model and field knowledge base. |
| `kb-health` | Diagnostics, project archiving, Layer 1 updates, Layer 2 expansion, and consistency checks. |
| `kb-dream` | Memory consolidation, vitality scoring, dormant-node pruning, duplicate detection, and relationship suggestions. |
| `lit-review-generator` | Interactive literature review drafting grounded in claims, arguments, and field concepts. |
| `intro-writer` | Interactive introduction drafting from broad topic to research gap, RQs, outline, and prose. |
| `discussion-writer` | Interactive discussion drafting from Results through evidence mapping, outline, and paragraph-level drafting. |

### academic-pipeline

| Skill | What it does |
|---|---|
| `deep-research` | Research briefs, literature review support, systematic-review support, fact-checking, and guided research. |
| `academic-paper` | Academic paper planning, drafting, revision, abstract writing, citation checks, and format conversion. |
| `academic-paper-reviewer` | Multi-perspective peer review, editorial assessment, re-review, and reviewer calibration. |
| `academic-pipeline` | Orchestrated research-to-publication workflow with checkpoints, integrity verification, and handoffs. |

## Knowledge Base Model

The custom KB skills use a three-layer Research Knowledge Base:

| Layer | Scope | Role |
|---|---|---|
| Layer 1: Researcher Model | Global and personal | Stores theoretical preferences, methodological attitudes, reasoning habits, and writing rules. |
| Layer 2: Field Knowledge Base | Global and structured | Stores concepts, methods, theories, gaps, limitations, and field-level relationships. |
| Layer 3: Project Data | Per project | Stores papers, claims, argument units, writing artifacts, and project-specific evidence. |

## Recommended Workflow

1. Initialize the Knowledge Base with `kb-init`.
2. Start or continue a project with `kb`.
3. Add papers with `paper-skimmer`.
4. Prioritize papers with `paper-selector`.
5. Deep-read important papers with `paper-deep-reader`.
6. Refine claims and build arguments with `kb`.
7. Draft sections with `intro-writer`, `lit-review-generator`, or `discussion-writer`.
8. Run maintenance with `kb-health` and consolidation with `kb-dream`.
9. Use `academic-pipeline` for larger end-to-end research, writing, review, and revision workflows.

## Validate

From the marketplace root:

```bash
claude plugin validate .
```

Or inside Claude Code:

```text
/plugin validate .
```

## Upstream Sources

This repository bundles or mirrors the following upstream work:

| Skill or package | Source |
|---|---|
| `academic-pipeline` module | [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) |
| `paper-reader` | [AIED007/paper-reader](https://github.com/AIED007/paper-reader) |
| `paper-mentor` | [sellerbubble/paper-mentor-skill](https://github.com/sellerbubble/paper-mentor-skill) |

## Acknowledgments

Thank you to the upstream authors and contributors whose work makes this plugin possible:

- **Cheng-I Wu / [Imbad0202](https://github.com/Imbad0202)**, author and maintainer of `academic-research-skills`.
- **[aspi6246](https://github.com/aspi6246)**, **[mchesbro1](https://github.com/mchesbro1)**, and **[cloudenochcsis](https://github.com/cloudenochcsis)**, acknowledged contributors in the upstream academic research skills project.
- **[sellerbubble](https://github.com/sellerbubble)**, author of `paper-mentor-skill`.
- **[AIED007](https://github.com/AIED007)**, maintainer of `paper-reader`.

The custom skills in this repository are intended to complement those projects. Upstream projects retain their own authorship, licenses, and design history.

## License

This repository combines custom skills with upstream work. Upstream packages retain their original licenses. Add a root `LICENSE` file before public distribution to state the license for the original custom material maintained here.
