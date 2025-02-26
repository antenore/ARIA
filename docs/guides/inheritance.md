# Understanding Policy Inheritance

This guide explains ARIA's policy inheritance system, which works with both capability-based and model-based policies.

## Overview

Policy inheritance allows you to:
- Create hierarchical policies
- Share common configurations
- Override specific settings
- Maintain consistency
- Extend existing policies without duplication

## Inheritance Models

ARIA supports inheritance for both policy formats:

### Capability-Based Inheritance

For capability-based policies, inheritance works by combining and overriding capabilities:

```yaml
# Base policy (capability-based)
name: base_policy
version: 1.0.0
capabilities:
  - name: text_generation
    description: Generate text responses
    allowed: true
    conditions:
      - Must follow content guidelines.
  - name: code_analysis
    description: Analyze code
    allowed: true
    conditions:
      - Must not execute code.
restrictions:
  - Must not retain user data.

# Child policy (capability-based)
name: child_policy
version: 1.0.0
inherits: base_policy
capabilities:
  - name: text_generation
    description: Generate text responses
    allowed: true
    conditions:
      - Must follow content guidelines.
      - Must cite sources when appropriate.  # Added condition
  - name: code_generation
    description: Generate code
    allowed: true  # New capability
restrictions:
  - Must not retain user data.
  - Must inform users about limitations.  # Added restriction
```

### Model-Based Inheritance

For model-based policies, inheritance works by merging model settings, defaults, and path rules:

```yaml
# Base policy (model-based)
name: base_model_policy
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
      - analyze
    require:
      - logging

# Child policy (model-based)
name: child_model_policy
version: 1.0.0
inherits: base_model_policy
defaults:
  allow:
    - generate  # Added permission
  require:
    - human_review
paths:
  "src/**/*.py":
    allow:
      - analyze
      - modify  # Added permission
  "docs/**":
    allow:
      - generate  # New path rule
```

## Inheritance Rules

### Common Rules
- Child policies must specify the parent policy using the `inherits` field
- Child policies must have the same or higher version number
- Child policies can add new settings but cannot remove parent settings

### Capability-Based Rules
- Child policies can add new capabilities
- Child policies can modify existing capabilities by adding conditions
- Child policies can add new restrictions
- Child policies cannot remove parent capabilities or restrictions

### Model-Based Rules
- Child policies can add new permissions to defaults and paths
- Child policies can add new path patterns
- Child policies can add new requirements
- Child policies cannot remove parent permissions or requirements

## Common Patterns

### Base Policies
- Define core capabilities or permissions
- Set default settings
- Establish common restrictions or requirements
- Provide a foundation for specialized policies

### Specialized Policies
- Inherit from base policies
- Add domain-specific capabilities or permissions
- Add context-specific conditions or requirements
- Customize for specific use cases

### Environment-Specific Policies
- Inherit from specialized policies
- Add environment-specific settings
- Adjust permissions based on environment (dev, test, prod)
- Fine-tune requirements for different contexts

## Best Practices

1. Keep inheritance chains short (ideally no more than 2-3 levels)
2. Document inheritance relationships clearly
3. Test inherited policies thoroughly
4. Version control all policies
5. Use consistent naming conventions
6. Validate policies after inheritance
7. Use strict validation during development

## Examples

See [example inherited policies](../examples/inherited-policy.yml) for detailed implementations.

## See Also

- [Policy Validation Guide](policy-validation.md)
- [Templates Guide](templates.md)
- [Policy API](../api/policy.md)
- [CLI Reference](cli.md)
- [Policy Format Examples](../examples/policy-formats.yml)
