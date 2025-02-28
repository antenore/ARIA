
<div align="center">
  <img src="assets/ARIA-Logo-adaptive.svg" alt="ARIA Logo" width="400" height="400">
</div>

# ARIA (Artificial Intelligence Regulation Interface & Agreements)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![CI](https://img.shields.io/github/actions/workflow/status/antenore/ARIA/ci.yml?branch=main)](https://github.com/antenore/ARIA/actions/workflows/ci.yml)
[![Project Status: Alpha](https://img.shields.io/badge/Project%20Status-Alpha-orange.svg)](https://github.com/antenore/ARIA)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/antenore?label=Sponsor&logo=GitHub)](https://github.com/sponsors/antenore)

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
- IDE integration for Windsurf, Cursor, and more (coming soon)

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
pip install aria-framework

# Initialize ARIA in your project
ariacli init

# Use a template policy
ariacli template apply assistant

# Validate your policy
ariacli policy validate

# View current permissions
ariacli describe

# Generate IDE rules from policy
ariacli ide rules --ide windsurf

# Generate IDE ignore files
ariacli ide ignore --ide cursor
```

## Policy Example

```yaml
version: 1.0
model: assistant

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
- [Quick Start Guide](docs/guides/getting-started.md)
- [Working with Templates](docs/guides/templates.md)
- [Understanding Policy Inheritance](docs/guides/inheritance.md)
- [Command Line Interface](docs/guides/cli.md)
- [Self-Testing ARIA](docs/guides/self-testing.md)
- [AI Tool Integrations](docs/guides/tool-integration/index.md)

### API Reference
- [Policy API](docs/api/policy.md)
- [Templates API](docs/api/templates.md)
- [Validator API](docs/api/validator.md)
- [CLI API](docs/api/cli.md)
- [Configuration API](docs/api/config.md)

### Technical Documentation
- [Policy Architecture](docs/technical/policy.md)
- [Template System](docs/technical/templates.md)
- [Validation System](docs/technical/validation.md)
- [Configuration](docs/technical/configuration.md)
- [Deployment](docs/technical/deployment.md)

### CI/CD Integration
- [GitHub Actions](docs/ci/github-actions.md)
- [GitLab CI](docs/ci/gitlab-ci.md)
- [Jenkins Pipeline](docs/ci/jenkins.md)

### Tool Integration
- [IDE Integration](docs/guides/tool-integration/index.md)
  - [Windsurf](docs/guides/tool-integration/windsurf.md)
  - [Cursor](docs/guides/tool-integration/cursor.md)
  - [IDE Rules](docs/guides/tool-integration/ide-rules.md)

## Contributing

We welcome contributions! Please see our [Contributing Guide](docs/guides/contributing.md) for guidelines.

## License

ARIA is licensed under the Apache License 2.0. See our [License](docs/guides/license.md) for details.

## Project Status

This project is currently in **alpha stage** development (v0.1.2-dev). The core concepts and architecture are established, but many features are still being implemented.

### ⚠️ Important Notes for Users and Contributors

- **Limited Maintainer Availability**: This project is maintained on a part-time basis. Response times to issues and pull requests may be delayed.
- **API Stability**: APIs are subject to change without notice during this early stage.
- **Current Focus**: 
  - Improving IDE integration
  - Enhancing policy enforcement mechanisms
  - Building comprehensive documentation
  - Creating a robust test suite
- **Help Wanted**: See our [ToDo.md](ToDo.md) for prioritized tasks where contributions would be most valuable.

For more details on how to contribute, please see our [Contributing Guide](CONTRIBUTING.md).

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

## GitHub Topics

When searching for this project, look for these topics:
- `ai-regulation`
- `ai-governance`
- `ai-policy`
- `artificial-intelligence`
- `policy-enforcement`
- `development-tools`

## AI Contribution Acknowledgment

In the spirit of transparency and dogfooding our own principles, portions of this project (including code, documentation, and project governance) were developed with the assistance of AI tools. All AI contributions were made under human supervision and review, following the principles outlined in our own ARIA policies.

This acknowledgment serves as a practical example of how AI participation can be transparently disclosed in software projects. For more details, see [AI_CONTRIBUTIONS.md](AI_CONTRIBUTIONS.md).

## Sponsorship

ARIA is an open-source project maintained in my free time. If you find this project useful, please consider supporting its development through [GitHub Sponsors](https://github.com/sponsors/antenore).

Your sponsorship helps:
- Maintain and improve ARIA
- Add new features and integrations
- Create better documentation
- Provide support to users

Thank you for your support! ❤️