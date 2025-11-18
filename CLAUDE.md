# CLAUDE.md - cookiecutter-pypackage

## Project Overview

This is a **CookieCutter template repository** for generating production-ready Python packages. It's not a Python package itself—it's a template that generates Python packages with comprehensive CI/CD, testing, Docker support, and best practices built-in.

### Two-Level Architecture

Understanding this dual structure is critical:

1. **Template Level** (root directory): The cookiecutter template infrastructure
2. **Generated Project Level** (`{{ cookiecutter.project_slug }}/`): The actual Python package template that gets generated

Most files exist in both levels with similar purposes but different scopes. For example:
- `.github/workflows/ci.yml` (root) tests the template generation process
- `{{ cookiecutter.project_slug }}/.github/workflows/ci.yml` is the CI that will be used by generated projects

## Essential Commands

### Template Development

```bash
# Install template development dependencies
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
python3 -m pip install -r requirements-dev.txt

# Test template generation (as done in CI)
cookiecutter . --config-file .github/cookiecutter-example.yml --no-input

# Run pre-commit on template files
pre-commit run --all-files
```

### Generated Project Development

After generating a project, these commands apply within the generated project directory:

```bash
# Initial setup (required after generation)
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements-dev.txt

# Compile pinned dependencies (required after generation and when deps change)
pip-compile --resolver=backtracking --generate-hashes
pip-compile --resolver=backtracking requirements-dev.in
pip-compile --resolver=backtracking requirements-build.in

# Install package in development mode
python3 -m pip install -e .

# Testing
tox -e py3                    # Test with system Python 3
tox -e py37                   # Test with Python 3.7
tox -e py37-piplatest        # Test with Python 3.7 + latest pip
tox -e pipprevious           # Test with pip 21.3.*
tox -e pipmain               # Test with pip development version
tox -e pre-commit            # Run all pre-commit hooks

# Single test file (requires pytest installed)
pytest tests/test_specific.py

# Docker smoke test
python3 docker_smoke_test.py

# Version management
bump2version patch           # 0.1.0 → 0.1.1
bump2version minor           # 0.1.1 → 0.2.0
bump2version major           # 0.2.0 → 1.0.0

# Push version tag to trigger PyPI release
git push origin v1.0.0
# OR push latest tag
git push origin $(git describe --match "v*")

# Build package
python -m build
```

## Template Variables (cookiecutter.json)

Key template variables that control generation:

- `project_name` → Generates `project_slug` (hyphenated) and `pkg_name` (underscored)
- `command_line_interface`: ["Click", "Argparse", "No command-line interface"]
- `open_source_license`: 8 options including MIT, Apache, GPL, or "Not open source"
- `use_pytest`: "y" (preferred) or unittest
- `use_renovate`: true/false for automated dependency updates

## Code Architecture

### Jinja2 Templating Patterns

Files in `{{ cookiecutter.project_slug }}/` extensively use Jinja2:

```jinja2
{% if cookiecutter.command_line_interface|lower == 'click' %}
import click
{% elif cookiecutter.command_line_interface|lower == 'argparse' %}
import argparse
{% endif %}
```

Key conditional blocks to understand:
- CLI framework selection (Click vs Argparse vs None)
- Test framework (pytest vs unittest)
- License classifier mappings in `setup.cfg`

### Tox Test Matrix

The test matrix is defined in `tox.ini` and creates 26+ environments:

```
py{37,38,39,310,311,py3}-pip{previous,latest,main}
```

This generates combinations like:
- `py37-pipprevious`: Python 3.7 with pip 21.3.*
- `py310-piplatest`: Python 3.10 with latest pip
- `py311-pipmain`: Python 3.11 with pip from main branch

The CI matrix (`{{ cookiecutter.project_slug }}/.github/workflows/ci.yml`) tests:
- 3 OS: Ubuntu, Windows, macOS
- 4 Python versions: 3.7, 3.8, 3.9, 3.10
- 2 pip versions: latest, previous
- Plus PyPy3 on Ubuntu

### Generated Package Structure

```
{{ cookiecutter.project_slug }}/
├── {{ cookiecutter.pkg_name }}/          # Source package
│   ├── __init__.py
│   └── {{ cookiecutter.pkg_name }}.py   # Main module with CLI
├── tests/                               # Test directory
├── setup.cfg                            # Declarative package config
├── setup.py                             # Minimal setuptools entry
├── pyproject.toml                       # PEP 517/518 build system
├── tox.ini                              # Test orchestration
├── Dockerfile                           # Production container
├── docker_smoke_test.py                 # Docker testing script
├── .pre-commit-config.yaml             # 15+ pre-commit hooks
├── .bumpversion.cfg                     # Version bump config
└── requirements*.in/txt                 # Dependency files
```

## CI/CD Workflows

### Root Level (`./github/workflows/ci.yml`)

Tests the template generation process:
1. Generates example project from cookiecutter
2. Runs pip-compile in generated project
3. Installs dependencies and runs pre-commit
4. Tests with PyPy3
5. Builds Docker image and scans with Trivy
6. Runs docker_smoke_test.py
7. Tests across OS/Python/pip matrix

### Generated Project Workflows

**ci.yml**: Multi-OS testing, coverage reporting, package build verification

**docker.yml**: Build, scan with Trivy, push to DockerHub on tags
- Tags: `1.2.3`, `1.2`, `latest` for release tags
- Branch tags: `master`, `pr-123`, etc.
- Requires `DOCKERHUB_TOKEN` and `DOCKERHUB_PASSWORD` secrets

**release-to-pypi.yml**: Auto-publish to PyPI on `v*` tags
- Requires `PYPI_API_KEY` secret
- Triggered by tags like `v1.0.0`

**gh-pages.yml**: Documentation generation
- Converts `README.orig.adoc` → `README.adoc` (asciidoctor-reducer)
- Converts to `README.md` (pandoc)
- Publishes to GitHub Pages

**codeql-analysis.yml**: Weekly security scanning

## Dependency Management

### pip-tools Workflow

Dependencies are managed with pip-tools in generated projects:

1. Edit `.in` files (human-maintained, unpinned)
2. Run `pip-compile` to generate `.txt` files (pinned with hashes)
3. Install from `.txt` files with `--require-hashes`

**Files:**
- `setup.cfg`: Runtime dependencies (install_requires)
- `requirements.in`: Derived from setup.cfg (empty by default)
- `requirements.txt`: Runtime deps with hashes
- `requirements-dev.in`: Dev tools (pytest, tox, pre-commit, etc.)
- `requirements-dev.txt`: Pinned dev dependencies
- `requirements-build.in`: Build tools (build, twine, wheel)
- `requirements-build.txt`: Pinned build dependencies

**Always use:** `pip-compile --resolver=backtracking`

Hash verification provides supply chain security but requires use of `.txt` files with `--require-hashes`.

## Pre-commit Hooks

Generated projects include extensive pre-commit configuration:

**General:**
- commitlint: Conventional commits enforcement
- detect-secrets: Secret scanning
- prettier: Multi-format formatting (YAML, JSON, MD)
- yamllint: YAML validation

**Python:**
- black: Code formatting (88 char line length)
- reorder-python-imports: Import sorting with `from __future__ import annotations`
- pyupgrade: Syntax upgrades for Python 3.7+
- docformatter: PEP 257 docstring formatting
- mypy: Static type checking (strict mode)
- flake8: Style and quality checks
- setup-cfg-fmt: setup.cfg formatting

**Installation:** Optional for contributors (pre-commit.ci handles it), but recommended:
```bash
pre-commit install
pre-commit run --all-files  # Run manually anytime
```

## Docker Infrastructure

### Best-Practice Dockerfile

Generated projects include production-ready Dockerfiles:
- Base: `python:3.11-slim-bullseye`
- Non-root user: `secureappuser`
- Virtual environment in `/app/venv`
- Tini init system for signal handling
- Hash-verified dependency installation
- Optimized layer caching

### docker_smoke_test.py

Dependency-free Python3 script that:
1. Builds Docker image: `docker build -t test-image .`
2. Runs detached container: `docker run -d test-image`
3. Validates exit code
4. Auto-cleanup with `docker kill/rm`

Framework for adding actual smoke tests to validate container functionality.

## Documentation Structure

### AsciiDoc Processing Pipeline

Generated projects use AsciiDoc with a special workflow:

1. **README.orig.adoc**: Source README with `include::` directives
2. **asciidoctor-reducer**: Resolves includes → `README.adoc`
3. **pandoc**: Converts to `README.md`
4. GitHub Pages: HTML generated from AsciiDoc

This solves GitHub's lack of support for AsciiDoc includes (github/markup#1095).

**Included files:**
- `SECURITY.adoc`: Security policy
- `DEVELOPMENT.adoc`: Developer docs
- `CONTRIBUTING.adoc`: Contribution guidelines

Edit `README.orig.adoc`, never `README.adoc` or `README.md` (both auto-generated).

## Important Patterns

### Conventional Commits

**For contributors:** Optional (PRs are squash-merged)
**For maintainers:** Required (enables automatic versioning)

Format: `type(scope): description`
- Types: feat, fix, docs, style, refactor, test, chore
- Example: `chore: Bump version 0.1.0 → 0.2.0`

### Cruft for Template Syncing

Generated projects should stay synchronized with template updates:

```bash
cruft check              # Check for updates
cruft update            # Apply updates interactively
cruft diff              # See differences
```

The `.cruft.json` file tracks template version and variables.

## GitHub Configuration Requirements

Generated projects require manual GitHub setup:

### Secrets

**For Docker workflow:**
- `DOCKERHUB_TOKEN`
- `DOCKERHUB_PASSWORD`

**For PyPI workflow:**
- `PYPI_API_KEY`

### Renovate Setup

Install the [Renovate GitHub App](https://github.com/marketplace/renovate) to enable automated dependency updates.

Configuration in `.github/renovate.json5`:
- Monthly schedule
- PR limits (2 hourly, 10 concurrent)
- 7-day minimum release age
- Grouped monorepo updates
- Docker and GitHub Action digest pinning

### GitHub Pages

To enable the generated README on GitHub Pages:
1. Go to repository Settings → Pages
2. Under Source, select: `gh-pages` branch, `/ (root)` directory
3. Click Save

### Labels

Run the issue-label-manager workflow to create predefined labels (Kubernetes-inspired).

## Version Management

Versions are git tags starting with `v`:

```bash
# Bump version (auto-commits and tags)
bump2version patch

# Push code (does NOT push tags)
git push origin master

# Push tag to trigger release workflows
git push origin v1.0.0
```

**Version tag triggers:**
- `release-to-pypi.yml`: Builds wheels, uploads to PyPI
- `docker.yml`: Builds multi-arch image, pushes to DockerHub with semantic tags

**Important:** Just `git push` doesn't push tags! Always push tags explicitly.

## Development Workflow for Generated Projects

1. **Setup:**
   ```bash
   python3 -m venv venv && source venv/bin/activate
   pip install -r requirements-dev.txt
   pip-compile --resolver=backtracking --generate-hashes
   pip-compile --resolver=backtracking requirements-dev.in
   pip-compile --resolver=backtracking requirements-build.in
   pip install -e .
   pre-commit install  # optional but recommended
   ```

2. **Code changes:**
   - Edit source code in `{{ cookiecutter.pkg_name }}/`
   - Add tests in `tests/`
   - Pre-commit runs automatically on commit (if installed)

3. **Testing:**
   ```bash
   tox -e py3              # Quick local test
   tox -e pre-commit       # All linting/formatting
   python3 docker_smoke_test.py  # Docker validation
   ```

4. **Dependency changes:**
   - Edit `setup.cfg` for runtime deps
   - Edit `requirements-*.in` for dev/build deps
   - Run appropriate `pip-compile` commands
   - Re-run `pip install -e .` if setup.cfg changed

5. **Release:**
   ```bash
   bump2version minor      # Creates commit and tag
   git push origin master
   git push origin $(git describe --match "v*")
   # CI automatically publishes to PyPI and DockerHub
   # Manually create GitHub Release with changelog
   ```

## Key Files to Edit When Modifying Template

- `cookiecutter.json`: Add/modify template variables
- `{{ cookiecutter.project_slug }}/`: All generated project files
- `.github/cookiecutter-example.yml`: Update test configuration
- `.github/workflows/ci.yml`: Update template CI
- `README.adoc`: Update template documentation

When adding conditional features, use Jinja2 conditionals and update `cookiecutter.json`.

## Common Gotchas

1. **Paths with spaces:** The directory name `{{ cookiecutter.project_slug }}` literally contains spaces and curly braces in the repository
2. **Hash pinning:** Must use `.txt` files with `--require-hashes`, not `.in` files
3. **Tag pushing:** `git push` does NOT push tags; must push explicitly
4. **Setup.cfg changes:** Require re-running `pip install -e .`
5. **README editing:** Edit `README.orig.adoc`, not `README.adoc` or `README.md`
6. **Two CI systems:** Template CI tests generation, generated project CI tests actual package
7. **pip-compile skipping:** Use `SKIP=pip-compile` in pre-commit if deps unchanged (as seen in tox pre-commit env)

## Python Version Support

- **Minimum:** Python 3.7 / PyPy 3.7
- **Tested:** CPython 3.7, 3.8, 3.9, 3.10, 3.11 + PyPy3
- **Type hints:** Uses `from __future__ import annotations` (PEP 563)
- **pyupgrade:** Automatically modernizes syntax for 3.7+

## License Options

Template supports 8 open source licenses via choosealicense.com:
- MIT License, The Unlicense, Boost Software License 1.0
- Apache License 2.0, Mozilla Public License 2.0
- GNU LGPLv3, GNU GPLv3, GNU AGPLv3
- "Not open source"

License selection affects:
- `LICENSE` file content
- `setup.cfg` classifiers and metadata
- README badges and sections
