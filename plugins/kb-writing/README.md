# KB & Writing Plugin

Research Knowledge Base management and mentored academic section writing, designed for developmental psychology and adaptable to other behavioral and social sciences. All six skills are original work.

## Knowledge Base Architecture

All skills operate on a three-layer Knowledge Base:

- **Layer 1 — Researcher Model** (global, personal, evolving): Your theoretical preferences, methodological attitudes, reasoning style, and writing rules. Stored in `layer1-researcher/`. Initialized through a structured interview and extraction from your own publications. Updated after project archiving or on demand.

- **Layer 2 — Field Knowledge Base** (global, structured, expanding): A hybrid YAML knowledge graph of concepts, methods, theories, gaps, open questions, and methodological limitations in your field. Stored in `layer2-field/`. Seeded from fundamental readings. Eight node types with typed relationships.

- **Layer 3 — Project Data** (per-project, transient): Papers, claims, argument units, and writing artifacts for your current project. This is where day-to-day research happens. Claims are extracted from deep-read papers; arguments are built from clusters of claims; writing skills consume arguments as their evidence base.

## Skills

### Knowledge Base Management

#### kb-init

First-t