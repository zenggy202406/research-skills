# Academic Pipeline Plugin

Full academic research-to-publication pipeline. All skills in this plugin are upstream/open-source, included as forks for portability.

## Skills

| Skill | Version | Description |
|-------|---------|-------------|
| deep-research | 2.8.1 | 13-agent research pipeline: question formulation → systematic search → synthesis → report |
| academic-paper | 3.0.1 | 12-agent paper writing: intake → structure → draft → review → format |
| academic-paper-reviewer | 1.8.1 | 5-reviewer peer review simulation (EIC + 3 peers + Devil's Advocate) |
| academic-pipeline | 3.2.1 | Orchestrator: research → write → review → revise → finalize |

## Upstream Sources

All source URLs are tracked in the root `UPSTREAM.md`. Fill in when identified.

## Workflow

```
deep-research → academic-paper → academic-paper-reviewer
                      ↑                    ↓
                      └──── revision ──────┘
                              ↓
                   academic-pipeline (orchestrates all)
```
