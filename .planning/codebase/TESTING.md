# Testing Patterns

**Analysis Date:** 2026-03-25

## Test Framework

**Runner:**
- No standard test runner configured (no pytest, unittest, or nose)
- Ruff linter detected (version 0.15.7) but no test execution framework

**Assertion Library:**
- Not applicable (no unit tests found)

**Run Commands:**
```bash
# No test commands found
# Potential setup would be:
uv run pytest                    # If pytest installed
uv run python -m unittest        # If using unittest
```

## Test File Organization

**Location:**
- No test files found (`*_test.py`, `test_*.py`, `*_spec.py`)
- No `tests/` directory present
- `.gitignore` includes pytest configuration (`.pytest_cache/`, `.coverage`, `htmlcov/`) suggesting pytest awareness

**Naming:**
- No established naming pattern for tests
- `.gitignore` pattern suggests intended use: `*_test.py` or `test_*.py`

**Structure:**
```
# Expected structure (not yet implemented):
skills/
├── memory/
│   └── scripts/
│       ├── config.py
│       └── tests/              # Not present
│           ├── test_record_operation.py
│           ├── test_get_history.py
│           └── ...
└── crisis-knowledge-maintainer/
    └── scripts/
        └── tests/              # Not present
```

## Test Structure

**Suite Organization:**
- No test suites exist
- Scripts are structured for CLI usage, not testability

**Recommended Pattern:**
```python
# Based on codebase patterns, tests would follow:
import pytest
from config import load_json_file, save_json_file

class TestRecordOperation:
    def test_record_operation_basic(self, tmp_path):
        # Setup
        # Execute
        # Assert
        pass
```

## Mocking

**Framework:** Not applicable (no mocking framework configured)

**Recommended Approach:**
- Mock file I/O operations (`open()`, `os.path.exists()`)
- Mock `datetime.now()` for deterministic timestamps
- Use `tmp_path` fixture for file operations

**What to Mock:**
- File system operations (JSON read/write)
- Timestamp generation
- UUID generation (currently uses `uuid.uuid4()`)

**What NOT to Mock:**
- Data transformation logic
- Relevance scoring algorithms
- JSON parsing/serialization

## Fixtures and Factories

**Test Data:**
- Sample data exists in `skills/memory/assets/memory/`
- Crisis events: `skills/memory/assets/memory/crisis_knowledge/events/*.json`
- Lessons: `skills/memory/assets/memory/lessons_learned/lessons/*.json`

**Location:**
- Example data: `skills/memory/assets/`
- Eval prompts: `skills/memory/evals/evals.json`, `skills/crisis-knowledge-maintainer/evals/evals.json`

## Coverage

**Requirements:** None enforced

**View Coverage:**
```bash
# Would require pytest-cov installation:
uv run pytest --cov=skills --cov-report=html
```

## Test Types

**Unit Tests:**
- Not implemented
- Target areas: `config.py` utilities, relevance scoring, JSON operations
- Priority: `load_json_file()`, `save_json_file()`, `calculate_relevance_score()`

**Integration Tests:**
- Not implemented
- Target areas: Full script execution with mock data
- Priority: `record_operation.py`, `record_lesson.py` (multi-file operations)

**E2E Tests:**
- Eval system exists (`evals/` directories) but contains prompts only, not automated tests
- Eval format:
  ```json
  {
    "id": 1,
    "prompt": "记录这次查询腾讯股票的操作",
    "expected_output": "智能体应该调用 record_operation.py 记录操作",
    "files": []
  }
  ```

## Common Patterns

**Async Testing:**
- Not applicable (all scripts are synchronous)

**Error Testing:**
- No error test cases found
- Scripts use `sys.exit(1)` for failures, making them harder to test
- Recommended: Refactor to return error codes instead of calling `sys.exit()`

**CLI Testing:**
- All scripts have `argparse` entry points
- Use `capsys` fixture (pytest) to capture stdout
- Test both `--json` and default output modes

## Eval System (Skill Testing)

**Structure:**
```
skills/
├── memory/
│   └── evals/
│       └── evals.json              # 8 eval cases
└── crisis-knowledge-maintainer/
    └── evals/
        ├── evals.json              # 3 eval cases
        └── iteration-1/
            ├── eval-1-update-investment/
            │   └── eval_metadata.json
            ├── eval-2-supplement-impact/
            │   └── eval_metadata.json
            └── eval-3-add-event/
                └── eval_metadata.json
```

**Eval Format:**
```json
{
  "id": 1,
  "prompt": "User prompt text",
  "expected_output": "Expected agent behavior description",
  "files": []
}
```

**Limitations:**
- Evals test agent behavior, not code correctness
- No automated assertion mechanism
- Manual verification required
- Empty `assertions` arrays in metadata files

## Test Data Management

**Sample Data:**
- 16 crisis event files in `skills/memory/assets/memory/crisis_knowledge/events/`
- 3 lesson files in `skills/memory/assets/memory/lessons_learned/lessons/`
- Portfolio, operations, conclusions JSON files

**Data Cleanup:**
- `.memory/` directory in `.gitignore` (runtime data excluded from version control)
- Tests should use temporary directories to avoid modifying production data

## Recommended Testing Setup

**Step 1: Add pytest configuration**
```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["skills/*/scripts/tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
```

**Step 2: Create test utilities**
```python
# skills/memory/scripts/tests/conftest.py
import pytest
import json
import tempfile
from pathlib import Path

@pytest.fixture
def memory_dir(tmp_path):
    """Create temporary memory directory structure"""
    memory = tmp_path / ".memory"
    memory.mkdir()
    (memory / "crisis_knowledge" / "events").mkdir(parents=True)
    (memory / "lessons_learned" / "lessons").mkdir(parents=True)
    return memory

@pytest.fixture
def sample_crisis_event():
    """Sample crisis event data"""
    return {
        "event_id": "CRISIS_TEST_001",
        "event_name": "Test Crisis",
        "basic_info": {"event_type": "economic", "severity": "high"},
        "event_details": "Test details",
        "market_impact": {"us_stock": {"content": "Test impact"}},
    }
```

**Step 3: Priority test files**
1. `test_config.py` - Test utility functions
2. `test_record_operation.py` - Test operation recording
3. `test_get_relevant_knowledge.py` - Test relevance scoring
4. `test_record_lesson.py` - Test lesson recording workflow

---

*Testing analysis: 2026-03-25*
