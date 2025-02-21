# GitHub Actions Integration

## Overview

This guide explains how to integrate ARIA with GitHub Actions for automated policy validation and deployment.

## Workflow Example

```yaml
name: ARIA Policy Validation

on:
  push:
    paths:
      - 'policies/**'
      - 'templates/**'
  pull_request:
    paths:
      - 'policies/**'
      - 'templates/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'
          
      - name: Install ARIA
        run: |
          python -m pip install --upgrade pip
          pip install aria-policy
          
      - name: Validate Policies
        run: |
          aria validate policies/
          
      - name: Test Templates
        run: |
          aria test-templates templates/
```

## Setup Instructions

1. Create `.github/workflows` directory
2. Add workflow YAML file
3. Configure secrets
4. Enable GitHub Actions

## Best Practices

1. Version control policies
2. Automated testing
3. Clear error reporting
4. Documentation updates

## See Also

- [GitLab CI](gitlab-ci.md)
- [Jenkins Pipeline](jenkins.md)
- [Policy Validation](../technical/validation.md)
