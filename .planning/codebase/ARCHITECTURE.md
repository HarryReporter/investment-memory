# Architecture

**Analysis Date:** 2026-03-25

## Pattern Overview

**Overall:** Script-based Memory System with AI Agent Orchestration

**Key Characteristics:**
- JSON file-based data persistence (no database)
- Python scripts expose CLI interface for data operations
- AI agents consume data via shell commands (`uv run python ...`)
- Knowledge retrieval uses keyword-based relevance scoring
- Index-detail pattern for efficient lookups

## Layers

**Data Storage Layer:**
- Purpose: Persist all investment knowledge, operations, and portfolio data
- Location: `.memory/`
- Contains: JSON files for crisis events, lessons, patterns, portfolio, conclusions, operations
- Depends on: Local filesystem
- Used by: Python scripts in `skills/memory/scripts/`

**Script Layer (Business Logic):**
- Purpose: Provide CLI tools for CRUD operations on knowledge data
- Location: `skills/memory/scripts/`, `skills/crisis-knowledge-maintainer/scripts/`
- Contains: Python scripts with argparse interfaces
- Depends on: `config.py` for shared utilities, `.memory/` for data
- Used by: AI agents via shell commands

**Agent Orchestration Layer:**
- Purpose: Coordinate AI agent workflows, commands, and knowledge retrieval
- Location: `.opencode/`
- Contains: Agent definitions, command definitions, workflow specs, GSD framework
- Depends on: Python scripts, JSON data files
- Used by: OpenCode platform

**Knowledge Retrieval Layer:**
- Purpose: Find relevant historical knowledge for current market situations
- Location: `skills/memory/scripts/get_relevant_knowledge.py`
- Contains: Keyword-based relevance scoring algorithms
- Depends on: Crisis index, lessons index, patterns file
- Used by: AI agents before generating analysis

## Data Flow

**Market Analysis Flow:**

1. User asks agent to analyze current market situation
2. Agent invokes `get_relevant_knowledge.py --situation "..." --type all`
3. Script loads `.memory/crisis_knowledge/index.json` and `.memory/lessons_learned/index.json`
4. Relevance scoring matches situation keywords against event keywords and types
5. Top-N relevant events/lessons are loaded from detail files
6. Full knowledge is returned to agent as JSON
7. Agent uses historical knowledge to generate analysis
8. Agent records operation via `record_operation.py`
9. Agent saves conclusion via `save_conclusion.py`

**Lesson Recording Flow:**

1. Agent/user identifies an investment judgment error
2. Agent invokes `record_lesson.py` with judgment details
3. Script generates unique lesson ID (LESSON_YYYYMMDD_uuid)
4. Lesson detail file saved to `.memory/lessons_learned/lessons/`
5. Lessons index updated with summary entry
6. Links file updated to associate lesson with related crisis
7. Confirmation returned

**Crisis Knowledge Update Flow:**

1. User provides new information about a crisis event
2. Agent invokes `update_crisis_event.py --event-id CRISIS_XXX --section YYY --content "..."`
3. Script loads event detail JSON from `.memory/crisis_knowledge/events/`
4. Specified section is updated or appended
5. Index summary updated via `update_crisis_index.py`

**State Management:**
- All state is file-based JSON in `.memory/` directory
- No in-memory state or caching layer
- Each script operation reads-modifies-writes JSON files
- Index files contain metadata/summaries for efficient scanning
- Detail files contain full event/lesson content

## Key Abstractions

**Crisis Event:**
- Purpose: Represents a historical crisis with market impact analysis
- Examples: `.memory/crisis_knowledge/events/CRISIS_2026_USIRAN.json`
- Pattern: Structured JSON with `basic_info`, `event_details`, `market_impact`, `investment_opportunities`
- Fields: event_id, event_name, severity, time_period, keywords, summary

**Lesson:**
- Purpose: Records an investment judgment error and its learning
- Examples: `.memory/lessons_learned/lessons/LESSON_20260325_85e32e4e.json`
- Pattern: Structured JSON with `judgment`, `actual_result`, `error_analysis`, `lessons_learned`
- Fields: lesson_id, date, related_crisis, avoidance_strategy

**Investment Pattern:**
- Purpose: Generalized investment rule extracted from crisis events
- Examples: `.memory/investment_patterns.json` (patterns array)
- Pattern: JSON object with crisis_types, keywords, confidence, source_events
- Fields: pattern_id, name, description, confidence

**Index:**
- Purpose: Lightweight summary of all items for efficient scanning
- Examples: `.memory/crisis_knowledge/index.json`, `.memory/lessons_learned/index.json`
- Pattern: JSON array of summary objects with metadata
- Contains: event_id/lesson_id, keywords, summary, severity

## Entry Points

**Python Scripts (Primary Interface):**
- Location: `skills/memory/scripts/*.py`
- Triggers: Shell commands from AI agents (`uv run python ...`)
- Responsibilities: CRUD operations on knowledge data

**Skill Definitions:**
- Location: `skills/memory/SKILL.md`, `skills/crisis-knowledge-maintainer/SKILL.md`
- Triggers: Natural language queries matched by OpenCode
- Responsibilities: Define capabilities and usage patterns

**GSD Commands:**
- Location: `.opencode/command/gsd-*.md`
- Triggers: User slash commands
- Responsibilities: Orchestrate project management workflows

## Error Handling

**Strategy:** Fail-safe with fallback defaults

**Patterns:**
- `load_json_file()` returns default value if file missing or invalid (see `config.py:33-48`)
- Argument validation exits with error message if required params missing
- Try/except blocks catch `json.JSONDecodeError` and `IOError`
- Scripts return exit code 0 on success, 1 on error

## Cross-Cutting Concerns

**Logging:** `print()` statements to stdout (captured by agent framework)
**Validation:** argparse parameter validation, JSON format validation
**Authentication:** None (local filesystem access only)
**Configuration:** Centralized in `skills/memory/scripts/config.py`

---

*Architecture analysis: 2026-03-25*
