# Codebase Structure

**Analysis Date:** 2026-03-25

## Directory Layout

```
investment-memory/
├── .memory/                              # Data storage (JSON files)
│   ├── crisis_knowledge/                 # Crisis event knowledge base
│   │   ├── index.json                    # Index with summaries for all events
│   │   └── events/                       # Individual event detail files
│   │       ├── CRISIS_2000_DOTCOM.json
│   │       ├── CRISIS_2008_SUBPRIME.json
│   │       ├── CRISIS_2020_COVID.json
│   │       ├── CRISIS_2026_USIRAN.json
│   │       └── ... (13 events total)
│   ├── lessons_learned/                  # Investment mistake learnings
│   │   ├── index.json                    # Index with summaries for all lessons
│   │   └── lessons/                      # Individual lesson detail files
│   │       ├── LESSON_20260325_85e32e4e.json
│   │       └── ... (3 lessons total)
│   ├── investment_patterns.json          # Extracted investment patterns
│   ├── conclusions.json                  # Analysis conclusions
│   ├── operations.json                   # Operation history
│   └── portfolio.json                    # Current portfolio holdings
├── skills/                               # Skill definitions and scripts
│   ├── memory/                           # Memory management skill
│   │   ├── SKILL.md                      # Skill definition and usage docs
│   │   ├── scripts/                      # Python scripts for data operations
│   │   │   ├── config.py                 # Shared configuration and helpers
│   │   │   ├── record_operation.py       # Record operations
│   │   │   ├── get_history.py            # Query operation history
│   │   │   ├── save_conclusion.py        # Save analysis conclusions
│   │   │   ├── get_conclusion.py         # Query saved conclusions
│   │   │   ├── update_portfolio.py       # Manage portfolio holdings
│   │   │   ├── summarize.py              # Generate operation summaries
│   │   │   ├── record_lesson.py          # Record investment mistakes
│   │   │   ├── get_relevant_knowledge.py # Smart knowledge retrieval
│   │   │   ├── extract_patterns.py       # Extract investment patterns
│   │   │   └── manage_links.py           # Manage cross-references
│   │   ├── assets/                       # Sample/seed data
│   │   │   └── memory/                   # Default .memory structure
│   │   └── evals/                        # Evaluation test cases
│   │       └── evals.json
│   └── crisis-knowledge-maintainer/      # Crisis knowledge maintenance skill
│       ├── SKILL.md                      # Skill definition
│       ├── scripts/                      # Maintenance scripts
│       │   ├── add_crisis_event.py       # Add new crisis events
│       │   ├── update_crisis_event.py    # Update existing events
│       │   └── update_crisis_index.py    # Sync index with events
│       └── evals/                        # Evaluation test cases
├── .opencode/                            # OpenCode platform config
│   ├── opencode.json                     # Platform permissions config
│   ├── settings.json                     # User settings (empty)
│   ├── package.json                      # Node dependencies
│   ├── agents/                           # AI agent definitions
│   │   ├── gsd-codebase-mapper.md        # Codebase analysis agent
│   │   ├── gsd-planner.md                # Planning agent
│   │   ├── gsd-executor.md               # Execution agent
│   │   └── ... (16 agents total)
│   ├── command/                          # Slash command definitions
│   │   ├── gsd-plan-phase.md             # Plan a development phase
│   │   ├── gsd-execute-phase.md          # Execute a planned phase
│   │   ├── gsd-map-codebase.md           # Map codebase architecture
│   │   └── ... (50+ commands total)
│   ├── hooks/                            # Platform hook scripts
│   │   ├── gsd-prompt-guard.js
│   │   ├── gsd-workflow-guard.js
│   │   └── ... (5 hooks total)
│   └── get-shit-done/                    # GSD framework
│       ├── VERSION
│       ├── bin/                          # CLI tools
│       │   ├── gsd-tools.cjs             # Main CLI entry point
│       │   └── lib/                      # Core libraries
│       │       ├── core.cjs              # Shared utilities
│       │       ├── config.cjs            # Configuration management
│       │       ├── state.cjs             # State management
│       │       └── ... (15+ modules)
│       ├── references/                   # Framework documentation
│       ├── templates/                    # Document templates
│       │   └── codebase/                 # Codebase analysis templates
│       │       ├── architecture.md
│       │       ├── structure.md
│       │       └── ... (7 templates)
│       └── workflows/                    # Workflow definitions
│           ├── plan-phase.md
│           ├── execute-phase.md
│           └── ... (50+ workflows)
├── README.md                             # Project documentation
└── .gitignore                            # Git ignore rules
```

## Directory Purposes

**.memory/:**
- Purpose: All persistent data storage
- Contains: JSON files for crisis knowledge, lessons, patterns, portfolio, operations, conclusions
- Key files: `crisis_knowledge/index.json`, `lessons_learned/index.json`, `portfolio.json`

**skills/memory/scripts/:**
- Purpose: Core business logic as CLI scripts
- Contains: Python scripts with argparse interfaces
- Key files: `config.py` (shared config), `get_relevant_knowledge.py` (knowledge retrieval)

**skills/crisis-knowledge-maintainer/scripts/:**
- Purpose: Crisis knowledge CRUD operations
- Contains: Scripts for adding/updating crisis events
- Key files: `add_crisis_event.py`, `update_crisis_event.py`

**.opencode/:**
- Purpose: AI agent platform configuration and framework
- Contains: Agent definitions, command definitions, GSD framework
- Key files: `opencode.json`, `get-shit-done/bin/gsd-tools.cjs`

## Key File Locations

**Entry Points:**
- `skills/memory/SKILL.md`: Main skill definition - describes all capabilities
- `skills/crisis-knowledge-maintainer/SKILL.md`: Crisis maintenance skill definition

**Configuration:**
- `skills/memory/scripts/config.py`: Central config - all paths, helpers, constants
- `.opencode/opencode.json`: Platform permissions

**Core Logic:**
- `skills/memory/scripts/get_relevant_knowledge.py`: Keyword-based knowledge retrieval
- `skills/memory/scripts/record_lesson.py`: Lesson recording with index + links update
- `skills/memory/scripts/extract_patterns.py`: Pattern extraction from crisis events

**Data:**
- `.memory/crisis_knowledge/events/CRISIS_*.json`: Crisis event details
- `.memory/lessons_learned/lessons/LESSON_*.json`: Lesson details
- `.memory/investment_patterns.json`: Extracted patterns

**Testing:**
- `skills/memory/evals/evals.json`: Memory skill evaluation cases
- `skills/crisis-knowledge-maintainer/evals/`: Crisis skill evaluation cases

## Naming Conventions

**Files:**
- Python scripts: `snake_case.py` (e.g., `record_operation.py`)
- Crisis events: `CRISIS_YYYY_NAME.json` (e.g., `CRISIS_2026_USIRAN.json`)
- Lessons: `LESSON_YYYYMMDD_uuid.json` (e.g., `LESSON_20260325_85e32e4e.json`)
- Patterns: `PATTERN_CRISIS_XXX_TYPE.json` (e.g., `PATTERN_CRISIS_2026_USIRAN_SHORT`)
- Skill docs: `SKILL.md` (uppercase)
- Agent/command docs: `gsd-*.md` (kebab-case with prefix)

**Directories:**
- Skill directories: `snake_case` or `kebab-case` (e.g., `crisis-knowledge-maintainer`)
- Data directories: `snake_case` (e.g., `crisis_knowledge`, `lessons_learned`)
- GSD framework: `kebab-case` (e.g., `get-shit-done`)

## Where to Add New Code

**New Crisis Event:**
- Detail file: `.memory/crisis_knowledge/events/CRISIS_YYYY_NAME.json`
- Index entry: Add to `.memory/crisis_knowledge/index.json` events array
- Or use: `skills/crisis-knowledge-maintainer/scripts/add_crisis_event.py`

**New Lesson:**
- Detail file: `.memory/lessons_learned/lessons/LESSON_YYYYMMDD_uuid.json`
- Or use: `skills/memory/scripts/record_lesson.py`

**New Memory Script:**
- Implementation: `skills/memory/scripts/new_script_name.py`
- Follow pattern: Import from `config.py`, use argparse, output JSON or formatted text
- Update: `skills/memory/SKILL.md` with new capability

**New Skill:**
- Directory: `skills/new-skill-name/`
- Required: `SKILL.md`, `scripts/` directory
- Optional: `evals/`, `assets/`

## Special Directories

**.memory/:**
- Purpose: All application data (crisis events, lessons, patterns, portfolio)
- Generated: No (user and script-created)
- Committed: Yes (seed data lives here)

**.opencode/:**
- Purpose: OpenCode platform configuration and GSD framework
- Generated: Partially (framework installed, config added)
- Committed: Yes

**skills/*/evals/:**
- Purpose: Evaluation test cases for skill scripts
- Generated: No
- Committed: Yes

---

*Structure analysis: 2026-03-25*
