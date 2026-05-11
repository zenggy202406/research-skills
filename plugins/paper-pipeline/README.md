# Paper Pipeline Plugin

Academic paper screening and reading workflow.

## Skills

| Skill | Origin | Description |
|-------|--------|-------------|
| paper-skimmer | Custom | Quick-scan papers into per-project Excel spreadsheets |
| paper-selector | Custom | Filter skimmed papers by research-alignment scoring |
| paper-deep-reader | Custom | Mentored deep reading with Bloom-taxonomy questioning |
| paper-reader | Upstream | Converts papers into interactive HTML study files |
| paper-mentor | Upstream | HuggingFace-powered paper comprehension mentor |

## Workflow

```
paper-skimmer → paper-selector → paper-deep-reader
                                        ↓
                              paper-reader / paper-mentor
```

## Upstream Sources

- **paper-mentor**: https://github.com/sellerbubble/paper-mentor-skill
- **paper-reader**: Source URL TBD
