# Contributing Guide

Thank you for your interest in contributing to ARIA! This guide will help you get started.

## Development Environment

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/yourusername/ARIA.git
   cd ARIA
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -e .[test,docs]
   ```

## Running Tests

1. Run unit tests:
   ```bash
   python -m pytest
   ```

2. Run type checking:
   ```bash
   mypy aria
   ```

3. Run linting:
   ```bash
   flake8 aria tests
   ```

## Coding Standards

1. Follow PEP 8 style guide
2. Add type hints to all functions
3. Write comprehensive docstrings
4. Include unit tests for new features
5. Update documentation as needed

## Pull Request Process

1. Create a feature branch
2. Make your changes
3. Run tests and linting
4. Update documentation
5. Submit a pull request

## Documentation

1. Update relevant markdown files in `/docs`
2. Build docs locally:
   ```bash
   mkdocs serve
   ```
3. Check for broken links and formatting

## Need Help?

- Open an issue for bugs
- Discuss features in discussions
- Ask questions in our community channels
