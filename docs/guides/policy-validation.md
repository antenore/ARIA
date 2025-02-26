# ARIA Policy Validation Guide

## Introduction

This guide explains how to use ARIA's policy validation system to ensure your policies are correctly formatted and contain all required information. The validator supports two policy formats: capability-based (for testing) and model-based (for production).

## Policy Formats

ARIA supports two primary policy formats:

### 1. Capability-Based Policies

Capability-based policies are primarily used for testing and focus on specific AI capabilities, conditions, and restrictions. This format is more human-readable and easier to understand for non-technical users.

**Example:**
```yaml
name: capability_based_policy
version: 1.0.0
description: Example of a capability-based policy

capabilities:
  - name: code_generation
    description: Generate code based on user requirements
    allowed: true
    conditions:
      - Must include appropriate comments.
  
  - name: data_analysis
    description: Analyze data provided by the user
    allowed: true
    conditions:
      - Must maintain data privacy.

restrictions:
  - Must not retain user data beyond the session.
```

### 2. Model-Based Policies

Model-based policies are used in production environments and focus on model types, default permissions, and path-specific rules. This format is more suitable for integration with code repositories and CI/CD pipelines.

**Example:**
```yaml
name: model_based_policy
version: 1.0.0
model: assistant
defaults:
  allow:
    - review
    - suggest
  require:
    - human_review
paths:
  "src/**/*.py":
    allow:
      - generate
      - modify
    require:
      - unit_tests
```

## Using the Policy Validator

### Basic Validation

To validate a policy file:

```python
from aria.core.validator import PolicyValidator

validator = PolicyValidator()
result = validator.validate_file("path/to/policy.yml")

if result.valid:
    print("Policy is valid!")
else:
    print("Validation errors:")
    for error in result.errors:
        print(f"- {error}")
    
    if result.warnings:
        print("Validation warnings:")
        for warning in result.warnings:
            print(f"- {warning}")
```

### Strict Validation

For more thorough validation, enable strict mode:

```python
result = validator.validate_file("path/to/policy.yml", strict=True)
```

Strict validation performs additional checks:
- Version format (semantic versioning)
- Description length and quality
- Capability description length and quality
- Condition format (ending with a period)
- Path pattern validity

### Validating Policy Dictionaries

If you have a policy as a Python dictionary:

```python
policy_data = {
    "version": "1.0.0",
    "name": "Test Policy",
    "capabilities": [
        {
            "name": "test_capability",
            "description": "A test capability",
            "allowed": True
        }
    ]
}

result = validator.validate_policy(policy_data)
```

## Common Validation Errors

### Missing Required Fields
```
Error: Missing required field 'name'
Error: Missing required field 'version'
```

### Invalid Capability Format
```
Error: Capability must have 'name', 'description', and 'allowed' fields
Error: Capability 'name' must be a string
```

### Invalid Model-Based Policy
```
Error: Invalid model type 'unknown_model'
Error: Invalid action 'unknown_action' for model 'assistant'
Error: Invalid path pattern '**'
```

## Best Practices

1. **Use Version Control**: Keep your policies in version control alongside your code.

2. **Validate Early and Often**: Validate policies during development to catch issues early.

3. **Use Strict Validation**: Enable strict validation during development for more thorough checks.

4. **Document Policies**: Include clear descriptions for policies, capabilities, and conditions.

5. **Test Both Formats**: If your system needs to support both policy formats, test with both.

6. **Automate Validation**: Include policy validation in your CI/CD pipeline.

## See Also

- [Validator API Reference](../api/validator.md)
- [Validation System Architecture](../technical/validation.md)
- [Example Policies](../examples/policy-formats.yml)
