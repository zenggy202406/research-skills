# Cross-Layer Search Operations

Search is a core capability of the knowledge base, enabling the user to find and connect knowledge across layers and projects.

## Search Modes

### 1. Concept Search
**What**: Find concepts across Layer 2 and all project-level concept refinements.
**How**:
1. Search `layer2-field/graph.yaml` node names and definitions for the keyword
2. Search each project's `concepts.yaml` for project-specific refinements
3. Present results grouped by layer (Layer 2 first, then by project)

### 2. Method Search
**What**: Find methods/paradigms and how they've been used.
**How**:
1. Search `layer2-field/graph.yaml` method nodes
2. Search each project's `method-instantiations.yaml`
3. Read method markdown files if the user wants details

### 3. Claim Search
**What**: Find empirical claims across all projects.
**How**:
1. Use `cross_search.py --mode claims --keyword <keyword> [--tags "tag1,tag2"] [--project <name>]`
2. Match against: statement, conditions, population, source, source_id, method_hint, tags
3. Tag filtering uses AND logic — all specified tags must be present
4. Present results with project name, claim status, and full details

### 4. Argument Search
**What**: Find structured arguments across all projects.
**How**:
1. Use `cross_search.py --mode arguments --keyword <keyword> [--tags "tag1,tag2"] [--project <name>]`
2. Match against: conclusion, tags, premises (with claim_hints), theoretical grounding (with concept_hints), scope conditions
3. Present results with project context

### 5. Paper Search
**What**: Find papers across all projects by author, title, journal, tags, or PAP-XXX ID.
**How**:
1. Use `cross_search.py --mode papers --keyword <keyword>`
2. Search `papers-reference.md` in all projects — matches against PAP-IDs, authors, titles, journal names, and tags
3. Search `skimmed-papers.xlsx` in all projects (read via xlsx skill or pandas)
4. Present results with project name and paper details

### 6. Relationship Search
**What**: Find how two concepts, methods, or projects are connected.
**How**:
1. Read `layer2-field/graph.yaml`
2. Find direct relationships between the two nodes
3. If no direct connection, find paths (up to 2 hops)
4. Present the connection chain

### 7. Free-Text Search
**What**: Search everything for a keyword or phrase.
**How**:
1. Search across all YAML and markdown files in the entire knowledge base
2. Use grep/ripgrep for efficient full-text search
3. Present results organized by layer and file

## Search Implementation

**Primary tool**: Use `cross_search.py` for structured YAML searches with keyword + tag filtering.
**Supplementary**: Use `yaml_manager.py --action list --filter-tags` for within-project filtered listing.
For markdown files, use text search (grep).
For Excel files, read with openpyxl or pandas.

Always present results concisely with enough context for the user to decide what to look at more closely.

## Cross-Project Patterns

When searching across projects, also surface patterns:
- "This concept appears in 3 of your 4 projects"
- "This method was used differently in Project A vs. Project B"
- "This counterargument recurs across projects — might be worth addressing systematically"

These observations help the user see their research trajectory and identify themes.
