# GitLab CI Integration

## Overview

This guide explains how to integrate ARIA with GitLab CI/CD for automated policy validation and deployment.

## Pipeline Example

```yaml
image: python:3.8

stages:
  - validate
  - test
  - deploy

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.pip-cache"

cache:
  paths:
    - .pip-cache/

validate_policies:
  stage: validate
  script:
    - pip install aria-policy
    - aria validate policies/
  rules:
    - changes:
        - policies/**/*
        - templates/**/*

test_templates:
  stage: test
  script:
    - pip install aria-policy
    - aria test-templates templates/
  rules:
    - changes:
        - templates/**/*

deploy_policies:
  stage: deploy
  script:
    - pip install aria-policy
    - aria deploy policies/
  only:
    - main
  when: manual
```

## Setup Instructions

1. Add `.gitlab-ci.yml`
2. Configure CI/CD variables
3. Enable GitLab CI/CD
4. Set up runners

## Best Practices

1. Stage organization
2. Caching strategy
3. Error handling
4. Documentation

## See Also

- [GitHub Actions](github-actions.md)
- [Jenkins Pipeline](jenkins.md)
- [Deployment Guide](../technical/deployment.md)
