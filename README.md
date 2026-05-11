# Research Skills

Version-controlled collection of Claude Cowork skills for academic research in developmental psychology. Organized as 3 plugin marketplaces by research workflow stage.

## Plugins

| Plugin | Skills | Description |
|--------|--------|-------------|
| [paper-pipeline](plugins/paper-pipeline/) | 5 (3 custom, 2 upstream) | Paper screening and reading workflow |
| [kb-writing](plugins/kb-writing/) | 6 (all custom) | Knowledge Base management and section writing |
| [academic-pipeline](plugins/academic-pipeline/) | 4 (all upstream) | Full research-to-publication pipeline |

## Research Workflow

```
                    ┌─────────────────────────────────────────────┐
                    │           academic-pipeline plugin          │
                    │  deep-research → academic-paper → reviewer  │
                    └──────┬──────────────────▲───────────────────┘
                           │                  │
                    ┌──────▼──────────────────┼───────────────────┐
                    │         paper-pipeline plugin               │
                    │  paper-skimmer → selector → deep-reader     │
                    │                    paper-reader / mentor     │
                    └──────────────────┬──────────────────────────┘
                                       │
                    ┌──────────────────▼──────────────────────────┐
                    │          kb-writing plugin                  │
                    │  kb-init → kb → lit-review / intro / disc.  │
                    │                  kb-health                  │
                    └─────────────────────────────────────────────┘
```

## Installation

### Option A: Install a single plugin
Copy the desired plugin folder into your Cowork skills directory.

### Option B: Install everything
Clone this repo and symlink or copy the `plugins/*/skills/*` folders into your Cowork skills directory.

## Upstream Skills

Some skills are forked from open-source projects. See [UPSTREAM.md](UPSTREAM.md) for source URLs and sync status.

## Git Workflow

This repo uses a simple main-branch workflow:
1. Make changes to skills locally
2. Test in Cowork
3. Commit and push to main
4. On another machine: pull to get the latest

For larger changes, create a feature branch and merge when ready.
