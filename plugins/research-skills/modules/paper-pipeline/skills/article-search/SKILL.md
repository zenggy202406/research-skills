---
name: article-search
description: "Search Google Scholar for research articles using a 4-stage keyword generator tailored to the caller's needs. Stage 1 (Exploratory): broad research questions for pipeline entry. Stage 2 (Topical): specific constructs/variables for lit-review or deep-research. Stage 3 (Evidential): targeted evidence for specific claims/hypotheses/mechanisms, called by discussion-writer or intro-writer when evidence gaps are found. Stage 4 (Citation-targeted): locate a specific known paper by author/title/year. Integrates with Research Knowledge Base when available. All search results require user confirmation before writing to any output. Zero relevant results is a valid outcome — relevance and quality always take priority over quantity. Triggers on: search articles, find papers, search Google Scholar, find research, search literature, look for papers, find evidence for, search for studies, article search, scholar search, find me papers on, 搜尋論文, 搜尋文獻, 找論文, 學術搜尋, Google Scholar 搜尋."
metadata:
  version: "1.0.0"
  created: "2026-05-14"
  updated: "2026-05-14"
  depends_on: "google-scholar MCP"
  status: active
---

# Article Search

Search Google Scholar for research articles relevant to a research project, using a 4-stage keyword generator that adapts search specificity to the caller's context. Can operate as the pipeline entry point (broad exploration) or as a precision tool called by downstream writing skills when they encounter evidence gaps.

---

## Trigger Conditions

### Trigger Keywords

**English:** search articles, find papers, search Google Scholar, find research, search literature, look for papers, find evidence for, search for studies, article search, scholar search, find me papers on, search for articles about, look up research on, find studies on, Google Scholar search, literature search, search for evidence, find supporting papers, search academic databases

**中文:** 搜尋論文, 搜尋文獻, 找論文, 學術搜尋, Google Scholar 搜尋, 查找文獻, 搜尋研究, 找研究證據, 學術論文搜索

### Auto-Activation Conditions

This skill should activate automatically when:
1. **User asks to find or search for papers** on a topic, construct, or research question
2. **User wants to start a new project** by surveying the literature landscape — pipeline entry
3. **A writing skill encounters an evidence gap** — e.g., discussion-writer flags "⚠️ UNSUPPORTED" or "⚠️ THIN EVIDENCE" and the user requests a search
4. **User wants to find a specific paper** by author, title, or approximate description
5. **User wants to explore a new research direction** before committing to a project

### Pipeline Context

This skill operates in **two modes**:

#### Mode A — Pipeline Entry Point (Exploratory)
Positioned **before paper-skimmer** in the pipeline:
```
article-search → paper-skimmer → paper-selector → paper-deep-reader → lit-review-generator
```
In this mode, the skill performs broad searches to build an initial paper collection. Its output (user-approved search results written to `{project}_search_results.xlsx`) feeds into paper-skimmer for further processing.

#### Mode B — Evidence Support (Called by Other Skills)
Called **on-demand** by downstream skills when they need additional evidence:
- **discussion-writer** — when interpreting findings but lacking KB evidence for a comparison or mechanism
- **intro-writer** — when building theoretical background but needing more papers for a construct or gap
- **lit-review-generator** — when a thematic section has thin coverage
- **deep-research** — when systematic search needs supplementary database coverage
- **Any skill** — when a specific citation needs to be located

In this mode, the skill receives a **search context** (the specific claim, argument, or gap that triggered the search) and uses Stage 2, 3, or 4 keywords accordingly. Results are presented to the user for approval before being passed back to the calling skill.

### Knowledge Base Integration

When operating within the Research Knowledge Base context (invoked via `/kb` or when a KB project is active):

1. **Field intelligence**: Before generating keywords, read `Research Knowledge Base/layer2-field/field-summary.md` to understand the field's conceptual landscape, established terminology, key constructs, and known gaps. Use this to generate more precise and field-appropriate search terms.

2. **Researcher preferences**: Check if `Research Knowledge Base/layer1-researcher/rules/literature-selection.md` exists. If it does, use these rules to guide which results to highlight as potentially relevant (e.g., preferred methodologies, theoretical orientations, populations of interest).

3. **Deduplication**: Before presenting results, cross-check against:
   - `Research Knowledge Base/projects/active/[project-name]/papers-reference.md` — papers already in the project
   - Any existing `{project}_papers.xlsx` or `{project}_search_results.xlsx` — papers already skimmed or found
   - Flag duplicates: "Already in your project" rather than silently excluding them (the user may want to note that the paper surfaced again in a new search context).

4. **Gap-aware searching**: When called by a writing skill with a specific gap, also consult `field-summary.md` GAP entries and OQ (open question) entries to see if the gap is a known field-level issue (which may mean literature genuinely doesn't exist yet) vs. a gap in the project's coverage (which means papers exist but haven't been collected).

When NOT in a KB context, the skill operates exactly as described below — all KB integration steps are skipped.

---

### Does NOT Trigger

| Scenario | Use Instead |
|----------|-------------|
| User wants to skim or extract info from a PDF they already have | paper-skimmer |
| User wants to filter/select papers from an existing spreadsheet | paper-selector |
| User wants a thorough deep reading of a specific paper | paper-deep-reader |
| User wants to write a literature review from collected papers | lit-review-generator |
| User wants a full systematic research report | deep-research |
| User wants to look up a specific author's profile and publication list | Use `get_author_info` tool directly — no need for this skill |

---

## The 4-Stage Keyword Generator

The keyword generator is the core of this skill. It adapts search specificity based on **who is calling and why**.

### Stage 1 — Exploratory (Pipeline Entry)

**When:** User triggers article-search directly to survey a research area. This is the pipeline entry point.

**Keyword strategy:**
- Broad conceptual terms and research questions
- Include major theoretical frameworks and constructs
- Use OR-combined synonyms to cast a wide net
- Include the population/context if specified by the user
- Aim for breadth — the goal is to discover what's out there

**Example:**
- User says: "I'm interested in how parent-child interaction affects children's self-regulation"
- Generated queries:
  - `"parent-child interaction" self-regulation child OR preschool`
  - `"parental sensitivity" "executive function" OR "effortful control" child`
  - `co-regulation "self-regulation development" early childhood`

**Number of searches:** 2-4 queries, 5-10 results each

### Stage 2 — Topical (Called by lit-review, deep-research)

**When:** A downstream skill needs papers on a specific construct, variable, or theoretical relationship.

**Keyword strategy:**
- Narrower than Stage 1 — focus on specific constructs and their relationships
- Include methodological terms if the caller specifies a design preference
- Include measurement tools or paradigms if relevant
- Use year range filters when the caller requests recent work

**Example:**
- Caller context: lit-review-generator is writing a section on "the role of temperament in moderating parenting effects"
- Generated queries:
  - `temperament moderation "parenting intervention" child outcomes`
  - `"differential susceptibility" OR "biological sensitivity to context" parenting`

**Number of searches:** 1-3 queries, 5-8 results each

### Stage 3 — Evidential (Called by discussion-writer, intro-writer)

**When:** A writing skill has a specific interpretive claim, hypothesis, or mechanism that lacks evidence support in the current KB.

**Keyword strategy:**
- Highly specific — target the exact claim or mechanism
- Use precise technical terms, specific constructs, and directional language
- Include effect modifiers (mediator, moderator, mechanism)
- Include the specific population or age range if relevant
- May include specific statistical approaches (e.g., "longitudinal mediation")

**Example:**
- Caller context: discussion-writer flags "⚠️ UNSUPPORTED: The finding that parental scaffolding predicted inhibitory control only for temperamentally reactive children may reflect differential susceptibility, but I can't find evidence for this specific pathway in the KB."
- Generated queries:
  - `"differential susceptibility" scaffolding "inhibitory control" temperament reactive`
  - `"parental scaffolding" "executive function" temperament moderation`

**Number of searches:** 1-2 queries, 3-5 results each

**Critical rule for Stage 3:** It is entirely acceptable — and expected — that some searches return zero relevant results. This means:
- The specific mechanism or pathway may be genuinely unstudied
- The claim may be a novel contribution of the current study
- The writing skill should note the absence of prior evidence honestly

**Never force relevance.** Do not stretch marginal results to fit the search context. If nothing relevant is found, say so clearly.

### Stage 4 — Citation-Targeted (Called by any skill)

**When:** A skill or the user needs to locate a specific known paper.

**Keyword strategy:**
- Use author names, publication year, and distinctive title words
- Use the `search_google_scholar_advanced` tool with `author` and `year_range` parameters
- Single, precise query

**Example:**
- Caller context: "Find the Bakermans-Kranenburg and van IJzendoorn 2015 meta-analysis on attachment interventions"
- Generated query: `search_google_scholar_advanced(query="attachment intervention meta-analysis sensitivity", author="Bakermans-Kranenburg", year_range=[2014, 2016])`

**Number of searches:** 1 query, 3-5 results

---

## Core Workflow

### Step 1: Determine Search Stage and Context

Identify the search stage based on how the skill was invoked:

| Invocation | Stage | Context to Gather |
|------------|-------|-------------------|
| User triggers directly, new project or exploration | Stage 1 — Exploratory | Research topic, broad questions, population |
| Called by lit-review-generator, deep-research | Stage 2 — Topical | Specific construct, theoretical relationship, section theme |
| Called by discussion-writer, intro-writer with evidence gap | Stage 3 — Evidential | The specific unsupported claim/argument, the finding being interpreted |
| Called by any skill or user to find a specific paper | Stage 4 — Citation-targeted | Author, approximate title, year |

If the stage is ambiguous, ask the user:

> "What kind of search do you need?"
> (a) Broad exploration of a research area (Stage 1)
> (b) Papers on a specific construct or relationship (Stage 2)
> (c) Evidence for a specific claim or mechanism (Stage 3)
> (d) Locate a specific known paper (Stage 4)

### Step 2: Generate Keywords

Using the stage-appropriate strategy (see above), generate candidate search queries.

**If KB context is available:**
1. Read `field-summary.md` for established terminology and field-specific jargon
2. Read `literature-selection.md` (if exists) for researcher preferences
3. Incorporate field-appropriate terms into the queries

**Present the generated queries to the user before searching:**

> **I've generated the following search queries based on your [topic / evidence gap / citation request]:**
>
> Query 1: `[query string]`
> Query 2: `[query string]`
> [Query 3: `[query string]` — if applicable]
>
> **Parameters:**
> - Results per query: [N]
> - Year range: [if applicable]
> - Author filter: [if applicable]
>
> **Want me to proceed with these, or adjust any queries?**

Wait for user confirmation before executing searches.

### Step 3: Execute Searches

Use the Google Scholar MCP tools:

- **For keyword searches:** `mcp__google-scholar__search_google_scholar_key_words(query, num_results)`
- **For filtered searches:** `mcp__google-scholar__search_google_scholar_advanced(query, author, year_range, num_results)`
- **For author lookups:** `mcp__google-scholar__get_author_info(author_name)` — only when the user specifically asks about an author's body of work

Execute each query sequentially. Collect all results.

### Step 4: Evaluate and Present Results

#### 4a. Deduplicate

Remove duplicate results across queries (same title or DOI).

If KB context is available, cross-check against existing project papers and flag any that are already in the project.

#### 4b. Assess Relevance

For each result, assess relevance to the search context:
- **Stage 1:** Does the paper address the broad research area?
- **Stage 2:** Does the paper address the specific construct or relationship?
- **Stage 3:** Does the paper provide evidence for the specific claim or mechanism?
- **Stage 4:** Is this the paper the user is looking for?

**Relevance rating:**
- **High** — Directly addresses the search context
- **Moderate** — Partially relevant, tangentially related, or addresses a related construct
- **Low** — Marginally related at best

**Critical rule:** Only present papers rated High or Moderate. Do NOT pad results with Low-relevance papers to make the output look fuller. If few or no papers are relevant, report that honestly.

#### 4c. Present Results to User

Present results as a summary table in chat:

> **Search Results — [Search Context Summary]**
>
> | # | Title | Authors | Year | Citations | Relevance | Note |
> |---|-------|---------|------|-----------|-----------|------|
> | 1 | [title] | [authors] | [year] | [count] | High | [1-line relevance note] |
> | 2 | [title] | [authors] | [year] | [count] | Moderate | [1-line relevance note] |
> | ... | | | | | | |
>
> **[N] results found. [M] rated High or Moderate relevance.**

**If zero relevant results:**

> **Search Results — [Search Context Summary]**
>
> I searched [N] queries and found [X] total results, but **none are directly relevant** to [the specific search context].
>
> **Possible reasons:**
> - [e.g., "This specific pathway (scaffolding → inhibitory control moderated by temperamental reactivity) may be genuinely unstudied"]
> - [e.g., "The terminology may differ — this construct might be discussed under a different name in the literature"]
> - [e.g., "This may be an emerging area with limited published work"]
>
> **Suggested adjusted queries (if you'd like to try again):**
> - Query A: `[broadened or reframed query]` — [rationale for adjustment]
> - Query B: `[alternative terminology query]` — [rationale]
>
> **Or we can accept that no prior evidence exists for this specific point.** This is a valid outcome — the calling skill should note the absence of prior evidence honestly in the writing.

Wait for user decision before proceeding.

### Step 5: User Confirmation Gate

**This step is mandatory. No search results are written to any output without explicit user approval.**

> **Which papers would you like to keep?**
> (a) All of them
> (b) Only specific ones — tell me which numbers
> (c) None — reject all results
> (d) None — and accept that no relevant evidence exists for this search context

If the user selects (c) or (d), respect the decision. Do not suggest re-searching unless the user asks.

If the user selects (b), note which papers are approved.

### Step 6: Output

#### 6a. Mode A — Pipeline Entry (write to spreadsheet)

For approved papers, write to `{project}_search_results.xlsx` using the helper script:

```bash
python "<skill-directory>/scripts/write_search_results.py" \
  --file "<output-path>/{project}_search_results.xlsx" \
  --data '[{"title": "...", "authors": "...", "year": 2023, "citations": 45, "abstract": "...", "url": "...", "relevance": "High", "search_context": "Exploratory — parent-child interaction and self-regulation"}]'
```

After writing:
> **[N] papers added to `{project}_search_results.xlsx`.** You can now proceed with paper-skimmer to extract detailed information from the full papers.

#### 6b. Mode B — Evidence Support (return to calling skill)

Do NOT write to any file. Instead, return the approved results to the calling skill as structured data that the calling skill can use:

> **Approved search results for [calling skill]:**
>
> For each approved paper:
> - **Title:** [title]
> - **Authors:** [authors]
> - **Year:** [year]
> - **Citations:** [count]
> - **Abstract:** [if available from search results]
> - **URL:** [url]
> - **Search context:** [the specific claim/gap this was searched for]
> - **Relevance note:** [1-line note on why this is relevant]

The calling skill decides how to use these results (e.g., discussion-writer may ask to skim the paper, intro-writer may incorporate the citation).

#### 6c. No Results Accepted

If the user rejected all results or no relevant results were found:

> **No papers retained from this search.** [Appropriate next step based on context:]
> - Stage 1: "Would you like to try different search terms, or explore a related topic?"
> - Stage 3: "The calling skill should note that no prior evidence was found for this specific point. This absence is itself informative and should be reported honestly in the writing — not filled with tangential citations."

---

## Usage Scenarios

### Scenario 1: New Project Exploration (Stage 1)

> **User:** "I want to explore research on how screen time affects toddlers' language development."
>
> **article-search activates in Stage 1 (Exploratory)**
> 1. Generates 3-4 broad queries covering screen time + language + toddlers + related constructs
> 2. Presents queries for user approval
> 3. Executes searches, presents summary table
> 4. User selects papers to keep
> 5. Writes to `screen-time-language_search_results.xlsx`
> 6. Offers: "Ready to skim these papers? I can invoke paper-skimmer next."

### Scenario 2: Lit-Review Needs More Papers (Stage 2)

> **lit-review-generator** is writing a section on "bidirectional effects in parent-child interaction" but has only 2 papers covering this theme.
>
> **article-search is called in Stage 2 (Topical)**
> 1. Receives context: "bidirectional effects, parent-child interaction, transactional model"
> 2. Generates 2 targeted queries
> 3. Presents results to user
> 4. User approves 3 papers
> 5. Returns structured results to lit-review-generator (no spreadsheet write)
> 6. lit-review-generator decides whether to skim these papers or incorporate citations

### Scenario 3: Discussion-Writer Hits Evidence Gap (Stage 3)

> **discussion-writer** flags: "⚠️ UNSUPPORTED: The finding that father involvement predicted social competence only in low-SES families may reflect stress-buffering, but I can't find evidence for this mechanism in the KB."
>
> **article-search is called in Stage 3 (Evidential)**
> 1. Receives the specific unsupported claim as context
> 2. Generates 1-2 highly specific queries targeting father involvement + social competence + SES + stress-buffering
> 3. Searches — finds 1 highly relevant paper and 1 moderately relevant paper
> 4. Presents to user with relevance notes
> 5. User approves 1 paper
> 6. Returns to discussion-writer, which decides to skim the paper and use it as supporting evidence
>
> **Alternative outcome:** Search finds nothing relevant.
> 1. Reports: "No prior evidence found for this specific stress-buffering pathway in father involvement research"
> 2. Suggests 2 broadened queries if user wants to try again
> 3. User says: "Accept that there's no evidence. Note it as a novel contribution."
> 4. discussion-writer proceeds, framing this as: "To our knowledge, this is the first study to demonstrate..."

### Scenario 4: Finding a Specific Paper (Stage 4)

> **User or any skill:** "Find the Raver 2004 paper on emotional regulation in Head Start children"
>
> **article-search activates in Stage 4 (Citation-targeted)**
> 1. Uses `search_google_scholar_advanced` with author="Raver" and year_range=[2003, 2005]
> 2. Presents top 3-5 results
> 3. User confirms which is the correct paper
> 4. Returns the citation details

### Scenario 5: KB-Aware Exploratory Search (Stage 1 + KB)

> **User** is starting a new project within the KB context. field-summary.md identifies known gaps in "cultural variation in parental mind-mindedness."
>
> **article-search activates in Stage 1, KB-aware**
> 1. Reads field-summary.md — notes GAP entries about cross-cultural mind-mindedness research
> 2. Reads literature-selection.md — notes researcher prefers longitudinal designs and developmental samples
> 3. Generates queries informed by field terminology and gap awareness
> 4. After results: flags papers that directly address known field gaps
> 5. Cross-checks against papers-reference.md — flags "Already in project" for any duplicates
> 6. Presents results with KB-informed relevance notes

---

## Important Rules

### Quality Over Quantity
- Never pad results with irrelevant papers
- Never stretch marginal results to appear relevant
- Zero results is a valid and informative outcome
- The user may reject all results — this is normal and expected

### No Fabrication
- Never invent or hallucinate paper titles, authors, years, or findings
- All results come directly from Google Scholar MCP tool responses
- If a search tool returns unexpected or malformed data, report it transparently
- Never fabricate an abstract or citation count that wasn't in the tool response

### User Authority
- The user has final say on which papers are relevant — even if your relevance assessment disagrees
- The user may reject all results; do not argue or re-suggest
- The user may ask for different search terms; always comply
- Never write to any output (spreadsheet, manuscript, reference list) without explicit user approval

### Honest Reporting of Absence
- When no relevant evidence is found (especially Stage 3), report this honestly
- Frame the absence appropriately: "genuinely unstudied" vs. "may exist under different terminology" vs. "emerging area"
- The calling skill must handle absence honestly in its writing output — never fill gaps with tangential citations

### Search Limitations
- Google Scholar results depend on the query terms and Google's ranking algorithm
- Citation counts are approximate and may lag
- Not all papers have abstracts available in search results
- Some results may be behind paywalls — note this if relevant
- The skill searches Google Scholar only; it does not search PubMed, PsycINFO, or other databases

---

## Edge Cases

1. **User provides very vague topic:** Ask clarifying questions before generating keywords. Do not search with overly broad terms that will return thousands of irrelevant results.

2. **Calling skill provides contradictory context:** Present the ambiguity to the user and ask which interpretation to search for.

3. **Google Scholar returns errors or no results at all:** Report the technical issue. Suggest retrying with simplified query terms.

4. **User wants to search multiple topics in one session:** Process each search context separately with its own confirmation gate. Do not mix results from different search contexts.

5. **User asks to search a non-English literature:** Generate keywords in the requested language if possible. Note that Google Scholar coverage varies by language and region.

6. **Result appears to be a retracted paper:** If the title or snippet indicates retraction, flag it explicitly. Do not include retracted papers in recommendations without the user's knowledge.
