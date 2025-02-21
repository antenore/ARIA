# Working with Templates

This guide explains how to work with ARIA templates effectively.

## What are Templates?

Templates are pre-defined policy configurations that help you:
- Start quickly with common scenarios
- Maintain consistency across policies
- Follow best practices

## Available Templates

1. `chat_assistant`
   - Basic chat functionality
   - Safety guardrails
   - Error handling

2. `code_assistant`
   - Code analysis
   - Generation capabilities
   - Security checks

3. `custom_assistant`
   - Fully customizable
   - Advanced features
   - Special use cases

## Using Templates

```bash
# List available templates
aria list-templates

# Apply a template
aria apply chat_assistant -o policy.yml

# Customize a template
aria customize chat_assistant -o custom.yml
```

## Template Structure

Templates follow this structure:
```yaml
name: template_name
version: 1.0.0
description: Template purpose
parameters:
  - name: param1
    type: string
    required: true
```

## Best Practices

1. Version your templates
2. Document customizations
3. Test before deployment
4. Keep templates simple

## See Also

- [Policy Inheritance](inheritance.md)
- [CLI Reference](cli.md)
- [Template API](../api/templates.md)
