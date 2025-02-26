# ARIA Framework v0.1.1-alpha

## Overview

This alpha release of the ARIA Framework includes significant improvements to documentation, IDE integration, and policy management. The focus has been on making the framework more accessible to users and providing better tools for integrating ARIA policies with development environments.

## Key Features

### IDE Integration

- **Policy to IDE Rules Converter**: New tool to convert ARIA policies to IDE-specific rule formats
- **IDE Ignore File Generation**: Generate `.codeiumignore` and `.cursorignore` files from policies
- **Enhanced Protection**: Better safeguards for policy files and sensitive paths
- **Multiple IDE Support**: Support for Windsurf and Cursor, with more planned

### Documentation Improvements

- **Comprehensive Structure**: Reorganized documentation with API references, user guides, and tutorials
- **Integration Guides**: Added guides for CI/CD integration with GitHub Actions, GitLab CI, and Jenkins
- **Policy Examples**: Added example policies demonstrating inheritance and template usage
- **Technical Documentation**: Detailed architecture documentation for templates and validation

### Policy Management

- **Enhanced Validation**: Support for both capability-based and model-based policies
- **Improved Type Safety**: Better type handling across template and policy management
- **Expanded Policy Models**: Support for 'guardian', 'observer', 'collaborator', and 'partner' models

### CI/CD Integration

- **GitHub Actions Workflow**: Automated testing and documentation building
- **Test Status Badge**: Added status badge to README.md
- **Integration Guides**: Documentation for integrating with popular CI/CD platforms

## Installation

```bash
pip install aria-framework==0.1.1-alpha
```

## Known Issues

- IDE integration is currently limited to rule generation, with full plugin support planned for future releases
- Some advanced policy validation features are still in development

## Future Plans

- Full SDK plugins for various IDEs
- Improved policy validation tools
- Runtime policy enforcement mechanisms
- Expanded multiplatform support
