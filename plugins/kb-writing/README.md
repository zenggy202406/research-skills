# KB & Writing Plugin

Research Knowledge Base management and academic section writing for developmental psychology.

## Skills

| Skill | Version | Description |
|-------|---------|-------------|
| kb | 2.1.0 | Daily KB operations: projects, paper workflows, claims, arguments, search |
| kb-init | 2.1.0 | First-time KB setup: Layer 1 researcher model + Layer 2 field seeding |
| kb-health | 2.0.0 | Health checks, maintenance, archiving, Layer 1/2 updates |
| lit-review-generator | — | APA-7 literature review writing grounded in Layer 3 argument units |
| intro-writer | — | Interactive Introduction section writer with KB integration |
| discussion-writer | — | Interactive Discussion section writer with KB integration |

## Architecture

All skills operate on a 3-layer Knowledge Base:
- **Layer 1**: Researcher Model (preferences, style, reasoning rules)
- **Layer 2**: Field Knowledge Base (concepts, theories, methodological norms)
- **Layer 3**: Project-level data (papers, claims, arguments, writing artifacts)

## Workflow

```
kb-init (one-time setup)
    ↓
kb (daily operations: skim/select/deep-read → extract claims → build arguments)
    ↓
lit-review-generator / intro-writer / discussion-writer
    ↓
kb-health (maintenance, archiving, Layer 1/2 updates)
```

## All skills are original work.
