# ARIA (Artificial Intelligence Regulation Interface & Agreements)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## What is ARIA?

ARIA is an open-source framework for defining and enforcing AI participation policies in software projects. It provides a standardized way to specify how AI can interact with your codebase, ensuring clear boundaries and responsibilities between human and AI contributors.

## Overview

In an era where AI is increasingly involved in software development, ARIA offers a structured approach to managing AI contributions. Similar to how `.gitignore` helps manage file tracking, ARIA helps manage AI participation through clear, human-readable policies.

## Core Features

- YAML-based policy definition with AWS-style inheritance
- Built-in policy templates for common scenarios
- Policy validation and enforcement tools
- Integration with popular CI/CD platforms
- Human-readable policy documentation generation

## Policy Models

ARIA provides several foundational models for AI participation:

### GUARDIAN
- Complete restriction of AI participation
- Suitable for highly sensitive or regulated projects

### OBSERVER
- AI can only analyze and review code
- Can suggest improvements without direct modifications
- Ideal for security-focused projects

### ASSISTANT
- AI can suggest and generate code
- All contributions require human review and approval
- Maintains strong human oversight

### COLLABORATOR
- AI can contribute to specific project areas
- Different rules for different components
- Granular permission control

### PARTNER
- Maximum AI participation with safety guardrails
- Human oversight on critical changes
- Comprehensive testing requirements

## Quick Start

```bash
# Install ARIA
pip install aria-policies

# Initialize ARIA in your project
aria init

# Use a template policy
aria template apply assistant

# Validate your policy
aria validate

# View current permissions
aria describe
```

## Policy Example

```yaml
version: 1.0
model: ASSISTANT

defaults:
  allow: []  # Deny-all by default
  require:
    - human_review
    - tests

paths:
  'src/tests/**':
    allow: 
      - generate
      - modify
    require:
      - test_coverage

  'docs/**':
    allow:
      - generate
      - modify
      - suggest
```

## Human Responsibilities

Project maintainers must:
1. Clearly define AI participation boundaries
2. Review AI-generated contributions
3. Ensure policy compliance
4. Maintain documentation accuracy

## Documentation

### Getting Started
- [Quick Start Guide](guides/getting-started.md)
- [Working with Templates](guides/templates.md)
- [Understanding Policy Inheritance](guides/inheritance.md)
- [Command Line Interface](guides/cli.md)

### API Reference
- [Policy API](api/policy.md)
- [Templates API](api/templates.md)
- [Validator API](api/validator.md)
- [CLI API](api/cli.md)
- [Configuration API](api/config.md)

### Technical Documentation
- [Policy Architecture](technical/policy.md)
- [Template System](technical/templates.md)
- [Validation System](technical/validation.md)
- [Configuration](technical/configuration.md)
- [Deployment](technical/deployment.md)

### CI/CD Integration
- [GitHub Actions](ci/github-actions.md)
- [GitLab CI](ci/gitlab-ci.md)
- [Jenkins Pipeline](ci/jenkins.md)

## Contributing

We welcome contributions! Please see our [Contributing Guide](guides/contributing.md) for guidelines.

## License

ARIA is licensed under the Apache License 2.0. See our [License](guides/license.md) for details.

## Project Status

This project is currently in active development. APIs may change.

## Author

**Antenore Gatta**
- GitHub: [@antenore](https://github.com/antenore)
- GitLab: [@antenore](https://gitlab.com/antenore)
- Email: antenore@simbiosi.org

## Links

- GitHub: [antenore/ARIA](https://github.com/antenore/ARIA)
- GitLab: [antenore/ARIA](https://gitlab.com/antenore/ARIA)
- Documentation: [docs/index.md](docs/index.md)
- Issues: [GitHub Issues](https://github.com/antenore/ARIA/issues)