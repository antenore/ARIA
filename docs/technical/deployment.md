# Deployment Guide

This guide covers deploying and integrating ARIA into your development workflow.

## CI/CD Integration

ARIA can be integrated into various CI/CD platforms:

### GitHub Actions
See [GitHub Actions Integration](../ci/github-actions.md) for detailed setup.

### GitLab CI
See [GitLab CI Integration](../ci/gitlab-ci.md) for detailed setup.

### Jenkins
See [Jenkins Integration](../ci/jenkins.md) for detailed setup.

## Installation

### From PyPI
```bash
pip install aria-policy
```

### From Source
```bash
git clone https://github.com/antenore/ARIA.git
cd ARIA
pip install -e .
```

## Configuration

1. Initialize ARIA in your project:
   ```bash
   aria init
   ```

2. Configure your policy:
   ```bash
   aria policy validate aria-policy.yml
   ```

3. Apply templates:
   ```bash
   aria template apply assistant
   ```

## Best Practices

1. Store policy files in version control
2. Use CI/CD to validate policies
3. Review policy changes in pull requests
4. Document policy decisions
5. Use templates for consistency
