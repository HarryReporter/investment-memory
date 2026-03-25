# Coding Conventions

**Analysis Date:** 2026-03-25

## Naming Patterns

**Files:**
- Python scripts use snake_case: `record_operation.py`, `get_history.py`, `save_conclusion.py`
- Scripts are action-oriented: verb_noun pattern (e.g., `record_lesson.py`, `update_portfolio.py`, `extract_patterns.py`)
- Config files use lowercase: `config.py`
- JSON data files use lowercase: `portfolio.json`, `operations.json`, `conclusions.json`

**Functions:**
- Python functions use snake_case: `load_json_file()`, `save_json_file()`, `generate_id()`
- Main functions often named `main()` or descriptive names like `record_operation()`, `get_history()`
- Helper functions are descriptive: `calculate_relevance_score()`, `load_event_detail()`

**Variables:**
- Local variables use snake_case: `operation_type`, `filtered_ops`, `type_counter`
- Constants use UPPER_SNAKE_CASE: `MEMORY_DIR`, `CRISIS_KNOWLEDGE_DIR`, `OPERATIONS_FILE`
- Function parameters use snake_case: `output_json`, `start_date`, `end_date`

**Types:**
- No explicit type annotations used (Python 3 without type hints)
- JSON structures use snake_case keys: `event_id`, `event_name`, `basic_info`, `time_period`
- IDs follow patterns: `CRISIS_YYYY_NAME`, `LESSON_YYYYMMDD_uuid`

## Code Style

**Formatting:**
- No explicit formatter configuration detected (no `.prettierrc`, `.editorconfig`, or ruff config)
- Consistent 4-space indentation throughout
- Double quotes for strings in Python code
- UTF-8 encoding specified for file operations: `encoding="utf-8"`

**Linting:**
- Ruff cache present (version 0.15.7) indicating ruff is used
- No explicit `.ruff.toml` configuration file found
- `.gitignore` includes standard Python exclusions (`__pycache__/`, `*.py[cod]`)

## Import Organization

**Order:**
1. Standard library imports: `os`, `json`, `sys`, `argparse`, `datetime`, `uuid`, `pathlib`
2. Local imports: `from config import ...`

**Pattern:**
```python
import argparse
import json
import sys
from datetime import datetime
from config import (
    OPERATIONS_FILE,
    load_json_file,
    save_json_file,
    generate_id,
    get_current_datetime,
)
```

**Path Aliases:**
- No path aliases used; relative imports from `config` module

## Error Handling

**Patterns:**
- Graceful fallback for JSON parsing errors:
  ```python
  try:
      details = json.loads(details)
  except json.JSONDecodeError:
      details = {"raw": details}
  ```
- File existence checks before reading: `if not os.path.exists(file_path)`
- Default values for missing files: `load_json_file(file_path, default=[])`
- User-facing error messages via `print()`: `print(f"错误: 无效的操作 '{action}'")`
- `sys.exit(1)` for critical validation failures

## Logging

**Framework:** Standard `print()` statements (no logging framework)

**Patterns:**
- Status messages: `print(f"操作已记录")`
- Progress indicators: `print(f"创建教训详情文件: {lesson_file_path}")`
- Error messages: `print(f"错误: 保存文件失败 {file_path}: {e}")`
- Result summaries: `print(f"找到 {len(filtered)} 条记录")`

## Comments

**When to Comment:**
- Module-level docstrings: Triple-quoted description of script purpose and usage
- Function docstrings: Args/Returns documentation in Chinese
- Inline comments for complex logic (rare)

**Docstring Pattern:**
```python
#!/usr/bin/env python3
"""
记录操作到记忆文件

功能：记录每次OpenAPI调用和分析操作
用法：python record_operation.py --type "quote" --details '{"code": "HK.00700"}' --result '{"price": 350.5}'
"""
```

**Function Docstring Pattern:**
```python
def get_history(operation_type=None, code=None, limit=None, start_date=None, end_date=None, output_json=False):
    """
    查询操作历史

    Args:
        operation_type: 操作类型过滤
        code: 股票代码过滤
        limit: 返回记录数量限制
        start_date: 开始日期（YYYY-MM-DD）
        end_date: 结束日期（YYYY-MM-DD）
        output_json: 是否输出JSON格式

    Returns:
        过滤后的操作记录列表
    """
```

## Function Design

**Size:** Functions typically 20-60 lines; larger scripts up to 200 lines

**Parameters:** 
- Use keyword arguments with defaults for optional parameters
- Required parameters listed first
- `output_json` parameter common for dual output modes (human-readable vs JSON)

**Return Values:**
- Return data structures (dicts, lists) for programmatic use
- Print output for human consumption
- Return `True`/`False` for success/failure operations
- Return file paths for save operations

## Module Design

**Exports:**
- No explicit `__all__` definitions
- Functions intended for CLI use guarded by `if __name__ == "__main__":`
- Core logic separated from CLI argument parsing

**Barrel Files:**
- Not used; each script is self-contained
- Shared utilities in `config.py` imported by all scripts

## CLI Patterns

**Argument Parsing:**
- All scripts use `argparse.ArgumentParser`
- Required vs optional arguments clearly marked
- `--json` flag for JSON output format
- `dest` used for parameter name mapping: `--start` → `start_date`

**Output Modes:**
- Default: Human-readable formatted output with Chinese labels
- `--json`: Machine-readable JSON output via `json.dumps(result, ensure_ascii=False, indent=2)`

---

*Convention analysis: 2026-03-25*
