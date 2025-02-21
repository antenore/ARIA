# ARIA Documentation

Welcome to the ARIA (AI Responsibility and Integration Assistant) documentation. ARIA helps you manage AI participation in your software projects through flexible policies and templates.

## Getting Started

- [Quick Start Guide](guides/getting-started.md)
- [Working with Templates](guides/templates.md)
- [Understanding Policy Inheritance](guides/inheritance.md)
- [Command Line Interface](guides/cli.md)

## Examples

- [Basic Policy](examples/basic-policy.yml)
- [Inherited Policy](examples/inherited-policy.yml)
- [Template Usage Examples](examples/template-usage.yml)

## API Reference

- [Policy API](api/policy.md)
- [Templates API](api/templates.md)
- [Validator API](api/validator.md)
- [CLI API](api/cli.md)
- [Configuration API](api/config.md)

## Technical Documentation

- [Policy Architecture](technical/policy.md)
- [Template System](technical/templates.md)
- [Validation System](technical/validation.md)

## CI/CD Integration

- [GitHub Actions](ci/github-actions.md)
- [GitLab CI](ci/gitlab-ci.md)
- [Jenkins Pipeline](ci/jenkins.md)

## Features

- **Simple CLI Interface**
  - Intuitive command structure
  - Command aliases for common operations
  - Progress indicators for long-running tasks
  - Rich console output with color-coding

- **Policy Management**
  - Create and validate policies
  - Apply templates
  - Flexible policy models
  - YAML-based configuration

- **Template System**
  - Pre-defined templates for common scenarios
  - Custom template support
  - Template versioning
  - Easy template application

- **Error Handling**
  - Comprehensive error messages
  - Proper exit codes
  - Detailed logging
  - Input validation

## Installation

```bash
# Install ARIA using pip
python -m pip install --user aria-policy
```

## Quick Commands

```bash
# Create a new policy
aria init -m assistant -o policy.yml

# List templates
aria list-templates

# Apply a template
aria apply chat_assistant -o policy.yml

# Validate a policy
aria validate policy.yml
```

## Contributing

See our [Contributing Guide](../CONTRIBUTING.md) for details on how to:
- Set up your development environment
- Run tests
- Submit pull requests
- Follow our coding standards

## License

ARIA is licensed under the Apache License 2.0. See [LICENSE](../LICENSE) for details.
