# research-skills Plugin

One Claude Code plugin for academic research workflows.

The plugin bundles three internal modules:

| Module | Purpose |
|---|---|
| `paper-pipeline` | Literature screening, paper selection, deep reading, and interactive paper reading. |
| `kb-writing` | Research Knowledge Base management and mentored literature review, introduction, and discussion writing. |
| `academic-pipeline` | Upstream end-to-end academic research, paper writing, peer review, revision, and finalization workflows. |

Claude Code loads skills from all three modules through `.claude-plugin/plugin.json`.

## Exposed Components

- Skills: `modules/paper-pipeline/skills`, `modules/kb-writing/skills`, and `modules/academic-pipeline`
- Commands: `modules/academic-pipeline/commands`
- Agents: `modules/academic-pipeline/agents`
- Hooks: `hooks/hooks.json`

The hook file intentionally lives at the plugin root so paths resolve correctly after Claude copies the plugin into its cache.
