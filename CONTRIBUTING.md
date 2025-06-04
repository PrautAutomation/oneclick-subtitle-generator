# Contributing to OneClick Subtitle Generator

First off, thank you for considering contributing to the OneClick Subtitle Generator! We welcome any help to make this project better.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Setting Up Development Environment](#setting-up-development-environment)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Code Contributions](#code-contributions)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Release Process](#release-process)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report any unacceptable behavior.

## Getting Started

### Prerequisites

- Python 3.8+
- Git
- FFmpeg (for audio processing)
- [Poetry](https://python-poetry.org/) (recommended) or pip

### Setting Up Development Environment

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/oneclick-subtitle-generator.git
   cd oneclick-subtitle-generator
   ```

3. **Set up Python virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install development dependencies**:
   ```bash
   # Using pip
   pip install -e ".[dev]"
   
   # Or using Poetry
   poetry install --with dev
   ```

5. **Install pre-commit hooks**:
   ```bash
   pre-commit install
   ```

6. **Run tests** to verify your setup:
   ```bash
   pytest
   ```

## How Can I Contribute?

### Reporting Bugs
- If you find a bug, please check the [issue tracker](https://github.com/PrautAutomation/oneclick-subtitle-generator/issues) to see if it has already been reported.
- If it hasn't, please [open a new issue](https://github.com/PrautAutomation/oneclick-subtitle-generator/issues/new/choose).
- Be sure to include a clear title and description, as much relevant information as possible, and steps to reproduce the bug.

### Suggesting Enhancements
- If you have an idea for a new feature or an improvement to an existing one, please check the [issue tracker](https://github.com/PrautAutomation/oneclick-subtitle-generator/issues) to see if it has already been suggested.
- If not, [open a new feature request issue](https://github.com/PrautAutomation/oneclick-subtitle-generator/issues/new/choose).
- Clearly describe the proposed enhancement and its potential benefits.

## Development Workflow

1. **Create a new branch** for your changes:
   ```bash
   git checkout -b type/descriptive-name
   ```
   Branch types:
   - `feature/` - New features
   - `bugfix/` - Bug fixes
   - `docs/` - Documentation improvements
   - `refactor/` - Code refactoring
   - `test/` - Test additions/improvements
   - `chore/` - Build process or tooling changes

2. **Make your changes** following the coding standards below.

3. **Run tests** and linters:
   ```bash
   # Run tests
   pytest
   
   # Run linters
   black .
   flake8
   mypy .
   ```

4. **Commit your changes** with a descriptive message:
   ```bash
   git add .
   git commit -m "type(scope): short description"
   ```
   Example commit message:
   ```
   feat(translator): add support for French language
   
   - Added French language model
   - Updated language detection
   - Added tests for French translation
   
   Closes #123
   ```

5. **Push your changes** to your fork:
   ```bash
   git push origin your-branch-name
   ```

## Coding Standards

- **Code Style**: We use Black for code formatting (line length: 88) and isort for import sorting.
- **Type Hints**: Use type hints for all function parameters and return values.
- **Docstrings**: Follow Google style docstrings for all public functions and classes.
- **Testing**: Write unit tests for new features and bug fixes (aim for >80% coverage).
- **Error Handling**: Use custom exceptions and provide meaningful error messages.

## Testing

- Write tests in the `tests/` directory.
- Use `pytest` for testing.
- Follow the naming convention `test_*.py` for test files.
- Use fixtures for common test setups.
- Mark slow tests with `@pytest.mark.slow`.

To run tests:
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=src --cov-report=term-missing

# Run a specific test file
pytest tests/test_module.py
```

## Documentation

- Keep documentation up to date with code changes.
- Update README.md for major changes.
- Add docstrings to all public functions and classes.
- Document any new command-line arguments or configuration options.

## Pull Request Process

1. Ensure your fork is up to date with the main branch:
   ```bash
   git remote add upstream https://github.com/PrautAutomation/oneclick-subtitle-generator.git
   git fetch upstream
   git merge upstream/main
   ```

2. Push your changes to your fork and open a Pull Request (PR).

3. Fill out the PR template with details about your changes.

4. Ensure all CI checks pass.

5. Request reviews from maintainers.

6. Address any feedback and update your PR as needed.

## Release Process

1. Update the version number in `pyproject.toml` following [Semantic Versioning](https://semver.org/).
2. Update `CHANGELOG.md` with the changes in this release.
3. Create a release tag:
   ```bash
   git tag -a v1.0.0 -m "v1.0.0: Release notes here"
   git push origin v1.0.0
   ```
4. Create a new GitHub release with the same tag.
5. The CI/CD pipeline will automatically publish the package to PyPI.

## Code of Conduct

This project adheres to the Contributor Covenant [code of conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report any unacceptable behavior to the project maintainers.

Thank you for contributing to the OneClick Subtitle Generator! Your help is greatly appreciated.
