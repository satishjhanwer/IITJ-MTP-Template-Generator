# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**IITJ MTP Template Generator** generates professional LaTeX academic reports for IIT Jodhpur's Major Technical Project (MTP). It supports three report types: proposal reports, major project reports, and Beamer presentation slides.

## Commands

### Installation

```bash
pip install -r scripts/requirements.txt      # Runtime: jinja2, pyyaml
pip install -r requirements-dev.txt          # Dev: pytest, pytest-cov, pytest-mock
```

### Running the Generator

```bash
# Interactive mode
python scripts/generate.py

# Config file mode
python scripts/generate.py --config examples/sample-proposal/config.yaml

# With output directory
python scripts/generate.py --config config.yaml --output my-report
```

### Tests

```bash
# Run all tests with coverage
pytest --cov=scripts --cov-report=html --cov-report=term-missing

# Run a single test file
pytest tests/test_generate.py -v

# Run a specific test
pytest tests/test_generate.py::TestClassName::test_name -v
```

### Code Quality (all configured in pyproject.toml and .flake8)

```bash
python -m black scripts/          # Format code
python -m isort scripts/          # Sort imports
python -m flake8 scripts/         # Lint (style + errors)
python -m mypy scripts/           # Type check
python -m bandit -r scripts/      # Security scan
python -m pylint scripts/         # Deep lint (target: 9.5+/10)
```

### LaTeX Compilation (after generation)

```bash
cd output/<project-name>
# Proposal:
pdflatex proposal.tex && bibtex proposal && pdflatex proposal.tex && pdflatex proposal.tex
# Major project:
pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
# Presentation:
pdflatex slides.tex && pdflatex slides.tex
```

## Architecture

### Generation Flow

```text
User Input (CLI prompts or YAML config)
    → Validation (validators.py)
    → Context Preparation (template_engine.py)
    → Jinja2 Template Rendering (templates/)
    → File Output (LaTeX + assets copied to output/)
    → User compiles with pdflatex externally
```

### Key Files

**`scripts/generate.py`** — Main orchestrator. Handles CLI argument parsing, interactive input collection (`collect_interactive_inputs()`), YAML config loading (`load_config_file()`), and invokes `generate_report()` which calls into the utils.

**`scripts/generate_simple.py`** — Zero-dependency fallback using only Python stdlib. Use when Jinja2/PyYAML are unavailable.

**`scripts/utils/`** — All supporting utilities:

- `template_engine.py` — Sets up Jinja2 with LaTeX-compatible delimiters (`\VAR{...}`, `\BLOCK{...}`, `\#{...}`), prepares context dict from config, and escapes LaTeX special characters.
- `validators.py` — Validates emails, required fields (with nested dict support), project types, logo file existence, and date formats.
- `errors.py` — Custom exception hierarchy with user-friendly messages and documentation links. Use pre-built factories like `config_file_not_found()`.
- `content_extractor.py` — Parses existing LaTeX reports to extract sections (intro, objectives, methodology, results, conclusion) for auto-populating presentation slides.
- `latex_parser.py` — Low-level LaTeX parsing: section/chapter extraction, environment extraction, itemize list parsing, LaTeX cleanup.
- `performance.py` — Caches Jinja2 template environments (~66% speedup), memoization decorator, profiling utilities.
- `progress.py` — Progress bars with ETA, spinner animation, context managers and decorators.
- `parallel_io.py` — Parallel file copy/write operations for bulk asset copying.

### Templates

Three template directories under `templates/`:

- `proposal/` — Title page, abstract, declaration, acknowledgments, chapters, bibliography
- `major-project/` — Extends proposal with certificate, optional glossary, optional appendix
- `presentation/` — Beamer slides with configurable theme/color/aspect ratio; can auto-extract content from an existing report

Templates use Jinja2 with **non-standard LaTeX-safe delimiters**:

- Variables: `\VAR{variable_name}`
- Control blocks: `\BLOCK{if condition}` ... `\BLOCK{endif}`
- Comments: `\#{comment text}`

### YAML Config Structure

The key top-level sections in user config files:

```yaml
project: {title, type}          # type: proposal | major-project | presentation
author: {name, roll_number, email}
academic: {supervisor, department, university, degree, session, ...}
dates: {submission_date}
formatting: {font_size, line_spacing, bibliography_style, color_scheme}
content: {include_declaration, include_certificate, include_acknowledgments, include_abstract, include_appendix, include_glossary}
assets: {logo_path}
presentation: {theme, color_scheme, aspect_ratio, extract_from_report, report_path}
```

See `docs/input_schema.md` for the complete reference.

### CI/CD

GitHub Actions (`.github/workflows/`) runs tests on Python 3.10–3.12 across Windows, macOS, and Linux on every push/PR to main. Coverage is uploaded to Codecov. A separate workflow compiles the example LaTeX output to verify template correctness.
