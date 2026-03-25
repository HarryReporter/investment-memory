# Technology Stack

**Analysis Date:** 2026-03-25

## Languages

**Primary:**
- Python 3 - All scripts in `skills/memory/scripts/` and `skills/crisis-knowledge-maintainer/scripts/`

**Secondary:**
- Markdown - Documentation files (`SKILL.md`, `README.md`)

## Runtime

**Environment:**
- Python 3 (version not specified)

**Package Manager:**
- uv (Python package manager)
- Lockfile: Not detected (no `uv.lock` or `requirements.txt`)

## Frameworks

**Core:**
- No web framework - CLI-based scripts using `argparse`
- Standard library only for all functionality

**Testing:**
- Not detected (no test files or test configuration found)

**Build/Dev:**
- No build system - direct script execution via `uv run python`

## Key Dependencies

**Critical:**
- Python Standard Library:
  - `json` - JSON serialization/deserialization
  - `os` - File system operations
  - `datetime` - Date/time handling
  - `uuid` - Unique ID generation
  - `argparse` - Command-line argument parsing
  - `pathlib` - Path manipulation
  - `collections` - Data structure utilities

**Infrastructure:**
- None - all data stored locally in JSON files

## Configuration

**Environment:**
- No environment variables detected
- No `.env` files present
- Configuration via hardcoded paths in `skills/memory/scripts/config.py`

**Build:**
- No build configuration files detected
- No `pyproject.toml`, `setup.py`, or `requirements.txt`

## Platform Requirements

**Development:**
- Python 3 runtime
- uv package manager (optional, for script execution)
- File system access for `.memory/` directory

**Production:**
- Local file system only
- No server deployment - script-based CLI tool

---

*Stack analysis: 2026-03-25*