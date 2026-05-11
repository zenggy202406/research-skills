# Research Skills

A version-controlled collection of [Claude Cowork](https://claude.ai) skills for academic research, with a focus on developmental psychology. The skills span the full research lifecycle — from literature screening through knowledge management to manuscript writing — and are organized into three installable plugin packages by workflow stage.

This repo is designed for researchers who use Claude Cowork as a research assistant and want a reproducible, portable skill setup across machines.

## Plugins

| Plugin | Skills | Description |
|--------|--------|-------------|
| [paper-pipeline](plugins/paper-pipeline/) | 5 (3 custom + 2 upstream) | Literature screening, selection, and deep reading |
| [kb-writing](plugins/kb-writing/) | 6 (all custom) | Knowledge Base management and mentored section writing |
| [academic-pipeline](plugins/academic-pipeline@8988ca4/) | 4 (all upstream) | End-to-end research-to-publication pipeline |

## Skill Overview

### paper-pipeline — Literature Screening & Reading

| Skill | What it does |
|-------|-------------|
| **paper-skimmer** | Quick-scans papers and extracts structured metadata into a per-project Excel spreadsheet. Handles single papers and batches. |
| **paper-selector** | Filters skimmed papers by research-alignment scoring. Conducts a structured interview about your project, then scores and ranks papers by relevance. |
| **paper-deep-reader** | Mentored deep reading with Bloom-taxonomy questioning. Produces 300-word integrated summaries per paper. Extracts draft claims for the Knowledge Base. |
| **paper-reader**\* | Converts one or more papers into a single self-contained interactive HTML file with library, analysis, quiz, glossary, and AI chat. |
| **paper-mentor**\* | Searches HuggingFace Papers for related work, maps the research domain, and generates interactive learning questions with feedback. |

### kb-writing — Knowledge Base & Academic Writing

| Skill | What it does |
|-------|-------------|
| **kb** | Daily Knowledge Base operations: manage projects, run paper workflows, extract and refine claims, build arguments, browse and search the knowledge graph. |
| **kb-init** | First-time KB setup: structured interview to build the Layer 1 Researcher Model, seeding of the Layer 2 Field Knowledge Base from fundamental readings. |
| **kb-health** | Health checks, maintenance, and diagnostics. Handles project archiving, Layer 1/2 on-demand updates, and consistency validation. |
| **lit-review-generator** | Interactive, mentored literature review writing. Generates APA-7 Word documents grounded in your extracted claims and argument units. |
| **intro-writer** | Interactive Introduction section writer. Takes you from a broad research idea through gap identification and RQ formulation to a polished draft. |
| **discussion-writer** | Interactive Discussion section writer. Reads your Results, confirms key findings, outlines, t
