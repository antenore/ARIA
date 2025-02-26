# ARIA Documentation

Welcome to the ARIA (AI Responsibility and Integration Assistant) documentation. ARIA helps you manage AI participation in your software projects through flexible policies and templates.

## Getting Started

- [Quick Start Guide](guides/getting-started.md)
- [Working with Templates](guides/templates.md)
- [Understanding Policy Inheritance](guides/inheritance.md)
- [Policy Validation Guide](guides/policy-validation.md)
- [Command Line Interface](guides/cli.md)
- [Integration Guide](guides/integration.md)

## Examples

- [Basic Policy](examples/basic-policy.yml)
- [Inherited Policy](examples/inherited-policy.yml)
- [Template Usage Examples](examples/template-usage.yml)
- [Policy Format Examples](examples/policy-formats.yml)

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
  - Support for capability-based and model-based policies

- **Template System**
  - Pre-defined templates for common scenarios
  - Custom template support
  - Template versioning
  - Easy template application
  - Support for multiple template formats

- **Advanced Validation**
  - Dual-purpose validator for testing and production
  - Strict validation mode with detailed warnings
  - Clear error messages and suggestions
  - Support for multiple policy formats
  - Path-specific validation rules
  - ValidationResult class with comprehensive feedback

- **Error Handling**
  - Comprehensive error messages
  - Proper exit codes
  - Detailed logging
  - Input validation

- **Policy Formats**
  - Capability-based format for testing and development
  - Model-based format for production environments
  - Automatic format detection
  - Format-specific validation rules
  - Inheritance support for both formats

## Installation

```bash
# Install ARIA using pip
python -m pip install --user aria-policy
```

## Quick Commands

```bash
# Create a new capability-based policy
aria init -f capability -o policy.yml

# Create a new model-based policy
aria init -m assistant -f model -o policy.yml

# List templates
aria ls

# Apply a capability-based template
aria apply basic_capabilities -f capability -o policy.yml

# Apply a model-based template
aria apply basic_model -f model -o policy.yml

# Validate a policy with automatic format detection
aria validate policy.yml

# Validate with strict validation
aria validate policy.yml --strict
```

## Contributing

For more information about contributing to ARIA, please read our [Contributing Guide](guides/contributing.md).

## License

For license information, see our [License](guides/license.md).
