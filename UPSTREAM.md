# Upstream Skill Sources

This repo distributes one Claude Code plugin, `research-skills`, with three internal modules:

```text
plugins/research-skills/modules/paper-pipeline/
plugins/research-skills/modules/kb-writing/
plugins/research-skills/modules/academic-pipeline/
```

Some module content comes from upstream open-source projects.

## Sources

| Content | Bundled path | Source repo |
|---|---|---|
| `academic-pipeline` module | `plugins/research-skills/modules/academic-pipeline/` | https://github.com/Imbad0202/academic-research-skills |
| `paper-reader` skill | `plugins/research-skills/modules/paper-pipeline/skills/paper-reader/` | https://github.com/AIED007/paper-reader |
| `paper-mentor` skill | `plugins/research-skills/modules/paper-pipeline/skills/paper-mentor/` | https://github.com/sellerbubble/paper-mentor-skill |

## Maintenance Notes

- The installable plugin must be self-contained under `plugins/research-skills/`; Claude Code copies only the plugin directory into its cache.
- Do not make plugin components depend on files outside `plugins/research-skills/`.
- When refreshing upstream content, update the bundled module copy and then validate the marketplace with `claude plugin validate .`.
- Preserve upstream authorship and license notes in README documentation.
