# Understanding Policy Inheritance

This guide explains ARIA's policy inheritance system.

## Overview

Policy inheritance allows you to:
- Create hierarchical policies
- Share common configurations
- Override specific settings
- Maintain consistency

## Inheritance Model

ARIA uses an AWS IAM-style inheritance model:
```yaml
# Base policy
base:
  permissions:
    - read
    - write

# Child policy
child:
  inherits: base
  permissions:
    - execute  # Adds to base permissions
```

## Common Patterns

1. Base Policies
   - Core permissions
   - Default settings
   - Common configurations

2. Specialized Policies
   - Additional permissions
   - Custom settings
   - Use-case specific rules

## Best Practices

1. Keep inheritance chains short
2. Document inheritance relationships
3. Test inherited policies
4. Version control all policies

## Examples

See [example policies](../examples/inherited-policy.yml) for detailed implementations.

## See Also

- [Templates Guide](templates.md)
- [Policy API](../api/policy.md)
- [CLI Reference](cli.md)
