# Contributing to ARIA

Thank you for your interest in contributing to ARIA! This guide will help you understand how to contribute effectively.

## ⚠️ Important Notes for Contributors

- **Limited Maintainer Availability**: This project is maintained on a part-time basis. Response times to issues and pull requests may be delayed.
- **Project Status**: ARIA is currently in alpha stage (v0.1.0). APIs may change without notice.
- **Prioritized Contributions**: Please check the [ToDo.md](ToDo.md) file for tasks marked with priority indicators (🔥, 🔴, 🟠, etc.) to see where help is most needed.

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

1. **Python Version**: Target Python 3.9+ compatibility
2. **Type Hints**: Add proper type hints to all functions and methods
   - Use `-> None` for functions that don't return values
   - Avoid using `Any` when a more specific type can be used
3. **Documentation**:
   - Write comprehensive docstrings in Google style format
   - Keep docstrings up-to-date with code changes
   - Update relevant markdown files in `/docs` when adding features
4. **Testing**:
   - Include unit tests for all new features
   - Maintain or improve test coverage
   - Test edge cases and error conditions
5. **Code Style**:
   - Follow PEP 8 style guidelines
   - Use consistent naming conventions
   - Keep functions focused and reasonably sized
   - Use meaningful variable and function names

## Pull Request Process

1. **Before Starting Work**:
   - Check the [ToDo.md](ToDo.md) file for prioritized tasks
   - Open an issue discussing your proposed changes (if one doesn't exist)
   - Wait for feedback before investing significant time

2. **Creating Your PR**:
   - Create a feature branch with a descriptive name
   - Make focused, logical commits with clear messages
   - Run tests and linting before submitting
   - Update documentation as needed
   - Reference the issue number in your PR description

3. **PR Description Template**:
   ```
   ## Description
   Brief description of the changes

   ## Related Issue
   Fixes #(issue)

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Code refactoring
   - [ ] Other (please describe)

   ## Testing
   Description of testing performed

   ## Documentation
   - [ ] I have updated the documentation accordingly
   ```

4. **Review Process**:
   - Be patient as reviews may take time due to maintainer availability
   - Be open to feedback and willing to make requested changes
   - Respond to comments in a timely manner

## Documentation

1. **Documentation Structure**:
   - API reference: `/docs/api/`
   - User guides: `/docs/guides/`
   - Technical docs: `/docs/technical/`
   - CI/CD integration: `/docs/ci/`

2. **Building Documentation**:
   ```bash
   mkdocs serve
   ```

3. **Documentation Standards**:
   - Use clear, concise language
   - Include examples where appropriate
   - Check for broken links and proper formatting
   - Ensure documentation is accessible to users of all experience levels

## Where to Start Contributing

1. **Good First Issues**: Look for issues labeled "good-first-issue"
2. **Documentation**: Improving documentation is always valuable
3. **Testing**: Adding tests or improving test coverage
4. **Bug Fixes**: Addressing open bugs
5. **Feature Implementation**: Check the [ToDo.md](ToDo.md) file for prioritized features

## Need Help?

- Open an issue for bugs or feature requests
- Discuss features in GitHub Discussions
- Contact the maintainer directly for urgent matters

Thank you for contributing to ARIA! Your efforts help make AI participation in software development more transparent and manageable.