# Codebase Concerns

**Analysis Date:** 2026-03-25

## Tech Debt

**Duplicate file I/O code across crisis-knowledge-maintainer scripts:**
- Issue: `update_crisis_event.py`, `update_crisis_index.py`, and `add_crisis_event.py` each have their own `load_event_file()` and `save_event_file()` functions with hardcoded paths like `".memory/crisis_knowledge/events/{event_id}.json"`. The memory skill scripts use `config.py` as a shared module, but crisis-knowledge-maintainer does not.
- Files: `skills/crisis-knowledge-maintainer/scripts/update_crisis_event.py` (lines 13-31), `skills/crisis-knowledge-maintainer/scripts/update_crisis_index.py` (lines 13-43), `skills/crisis-knowledge-maintainer/scripts/add_crisis_event.py` (lines 41-48)
- Impact: Any path change requires updates in 3+ files; code inconsistency increases maintenance burden
- Fix approach: Refactor crisis-knowledge-maintainer scripts to import shared functions from `skills/memory/scripts/config.py` or create a local config module

**Duplicated utility functions across scripts:**
- Issue: `load_event_detail()` appears in both `skills/memory/scripts/get_relevant_knowledge.py` (line 20) and `skills/memory/scripts/extract_patterns.py` (line 38). Same for `load_lesson_detail()`. These should be centralized.
- Files: `skills/memory/scripts/get_relevant_knowledge.py`, `skills/memory/scripts/extract_patterns.py`
- Impact: Changes to file loading logic must be replicated in multiple places
- Fix approach: Move these functions to `config.py` as shared utilities

**Inconsistent path references in documentation:**
- Issue: `skills/crisis-knowledge-maintainer/SKILL.md` uses `.opencode/skills/crisis-knowledge-maintainer/scripts/` in all code examples (lines 103-106, 115-116, 147, 153-154, 171, 175-176, 195), but the actual scripts are located at `skills/crisis-knowledge-maintainer/scripts/`. This path mismatch will cause command failures.
- Files: `skills/crisis-knowledge-maintainer/SKILL.md`
- Impact: Users copying examples from documentation will get "file not found" errors
- Fix approach: Update SKILL.md examples to use correct relative paths (`skills/` not `.opencode/skills/`)

## Known Bugs

**Inconsistent crisis event ID references in lessons:**
- Symptoms: `LESSON_20260325_5774c4b6.json` references `CRISIS_2025_USIRAN` (line 5), but the actual event file is named `CRISIS_2026_USIRAN.json`. Similarly, `LESSON_20260325_d3a34799.json` references `CRISIS_2026_MIDEAST` which does not exist as an event file at all.
- Files: `.memory/lessons_learned/lessons/LESSON_20260325_5774c4b6.json` (line 5), `.memory/lessons_learned/lessons/LESSON_20260325_d3a34799.json` (line 4), `.memory/lessons_learned/index.json` (lines 8, 32)
- Trigger: Querying lessons related to a crisis will fail to find cross-references when IDs don't match
- Workaround: Manually correct the `related_crisis` field in lesson files and index to match actual event IDs (`CRISIS_2026_USIRAN`)

**Optional argument handling with `hasattr` is fragile:**
- Symptoms: `record_lesson.py` uses `hasattr(args, "reasoning")` (line 38), `hasattr(args, "time_period")` (line 44), etc. to check for optional arguments. Since `argparse` always sets attributes (to `None` if not provided), `hasattr` will always return `True`, meaning empty strings or `None` values will be stored instead of being omitted.
- Files: `skills/memory/scripts/record_lesson.py` (lines 38, 44, 48-53)
- Trigger: Any call to `record_lesson.py` without optional args will store `null` values
- Fix approach: Replace `hasattr(args, "reasoning")` with `args.reasoning is not None` or use `getattr(args, "reasoning", "")`

## Security Considerations

**No input validation on JSON content:**
- Risk: Scripts accept arbitrary JSON strings via `--details`, `--result`, `--content` arguments without schema validation. Malformed or deeply nested JSON could cause issues or be stored in data files.
- Files: `skills/memory/scripts/record_operation.py` (lines 36-46), `skills/crisis-knowledge-maintainer/scripts/update_crisis_event.py` (line 182)
- Current mitigation: `json.loads()` will reject invalid JSON, but no structural validation exists
- Recommendations: Add JSON schema validation for critical data structures (operations, conclusions, lessons)

**Memory data is gitignored:**
- Risk: `.memory/` directory is listed in `.gitignore` (line 26), meaning all investment data, crisis knowledge, and lessons learned are not version controlled. Data loss on disk failure is unrecoverable.
- Files: `.gitignore` (line 26)
- Current mitigation: None
- Recommendations: Implement automated backup strategy; consider committing `.memory/` to git or using a proper database

## Performance Bottlenecks

**Full file scan for history queries:**
- Problem: `get_history.py` loads the entire `operations.json` file into memory and iterates through all records to filter (lines 37-67). As operations accumulate, this becomes increasingly slow.
- Files: `skills/memory/scripts/get_history.py` (lines 37-67)
- Cause: Linear scan O(n) for every query; no indexing or pagination at storage level
- Improvement path: Implement date-based partitioning (e.g., monthly files) or add an in-memory index

**Relevance scoring loads all events into memory:**
- Problem: `get_relevant_knowledge.py` loads the entire crisis index, then for each event computes relevance by string matching (lines 97-124). This is O(n*m) where n=events and m=keywords.
- Files: `skills/memory/scripts/get_relevant_knowledge.py` (lines 32-64, 97-124)
- Cause: No pre-computed embeddings or search index; pure text matching
- Improvement path: Consider adding TF-IDF scoring, embedding-based similarity, or at minimum caching keyword lookups

## Fragile Areas

**Crisis event schema inconsistency:**
- Issue: The crisis event data structure is inconsistent between what `index.json` expects and what event detail files contain. For example, `CRISIS_2026_USIRAN.json` has `basic_info.keywords` but the index expects `keywords` at the top level of the event object. The `extract_patterns.py` script reads `event.get("basic_info", {}).get("keywords", [])` (line 50) while `get_relevant_knowledge.py` reads `event.get("keywords", [])` (line 38) from the index structure.
- Files: `.memory/crisis_knowledge/events/CRISIS_2026_USIRAN.json` (nested structure), `.memory/crisis_knowledge/index.json` (flat structure), `skills/memory/scripts/extract_patterns.py` (line 50), `skills/memory/scripts/get_relevant_knowledge.py` (line 38)
- Why fragile: Any script that reads crisis data must know whether it's reading from the index (flat) or event file (nested)
- Safe modification: Standardize schema; either flatten event files or nest index entries

**No atomic file writes:**
- Issue: All scripts read JSON, modify in memory, then write back. If a process crashes mid-write, the JSON file becomes corrupted. `save_json_file()` in `config.py` (line 51-60) opens the file directly for writing without atomic rename or backup.
- Files: `skills/memory/scripts/config.py` (lines 51-60)
- Why fragile: Power loss or process kill during write corrupts data permanently
- Safe modification: Write to temp file first, then atomic rename; or implement write-ahead logging

**No concurrency protection:**
- Issue: Multiple scripts could read and write the same JSON file simultaneously (e.g., two `record_operation.py` calls). Since each reads-modifies-writes the entire file, the last writer wins and earlier writes are lost.
- Files: All scripts that use `load_json_file()` then `save_json_file()`
- Why fragile: Parallel agent operations will lose data
- Safe modification: Implement file locking (e.g., `fcntl.flock`) or use append-only log format

## Test Coverage Gaps

**No automated tests for any scripts:**
- What's not tested: All 11 Python scripts have zero unit tests. Evals exist but are manual integration tests (`skills/memory/evals/evals.json`, `skills/crisis-knowledge-maintainer/evals/evals.json`).
- Files: `skills/memory/scripts/*.py`, `skills/crisis-knowledge-maintainer/scripts/*.py`
- Risk: Refactoring or bug fixes may silently break functionality
- Priority: High

**No validation of data integrity after writes:**
- What's not tested: After `save_json_file()` writes data, no verification that the written file is valid JSON or matches expected schema
- Files: `skills/memory/scripts/config.py` (lines 51-60)
- Risk: Silent data corruption goes undetected
- Priority: High

## Dependencies at Risk

**Python environment assumption:**
- Risk: Scripts use `#!/usr/bin/env python3` shebang and assume Python 3.7+ (for `datetime.fromisoformat()`). The README recommends `uv` for environment management but scripts don't validate Python version.
- Impact: Scripts may fail on older Python versions with unclear error messages
- Migration plan: Add Python version check in `config.py` or document minimum version requirement

**No dependency pinning:**
- Risk: Scripts only use standard library (`json`, `os`, `datetime`, `argparse`, `uuid`, `collections`), which is good. However, there's no `requirements.txt` or `pyproject.toml` to document this explicitly.
- Impact: Future contributors may add external dependencies without tracking
- Migration plan: Add a minimal `pyproject.toml` or `requirements.txt` documenting Python version requirement

## Missing Critical Features

**No data backup/restore mechanism:**
- Problem: The system stores all investment data in `.memory/` which is gitignored. There is no backup script, no export functionality, and no way to restore from corruption.
- Blocks: Safe production use; any disk failure or accidental deletion is catastrophic

**No operation rollback:**
- Problem: `update_crisis_event.py` and `update_portfolio.py` modify data in place with no undo capability. A mistaken update cannot be reverted.
- Blocks: Confident data maintenance; users must manually backup before every update

**No duplicate operation prevention:**
- Problem: `record_operation.py` appends every call to `operations.json` without checking for duplicates. The same market snapshot can be recorded multiple times.
- Files: `skills/memory/scripts/record_operation.py` (line 66)
- Blocks: Accurate operation statistics in `summarize.py`
