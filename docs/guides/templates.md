# Working with Templates

This guide explains how to work with ARIA templates effectively.

## What are Templates?

Templates are pre-defined policy configurations that help you:
- Start quickly with common scenarios
- Maintain consistency across policies
- Follow best practices
- Create both capability-based and model-based policies

## Template Formats

ARIA supports two template formats that correspond to the two policy formats:

### Capability-Based Templates
- Focus on specific AI capabilities
- Clear conditions and restrictions
- Simplified structure for non-technical users
- Ideal for testing and development

### Model-Based Templates
- Focus on model types and path-specific rules
- Integration with code repositories
- More granular control over permissions
- Ideal for production environments

## Available Templates

1. `chat_assistant` (Capability-based)
   - Basic chat functionality
   - Safety guardrails
   - Error handling
   - Text generation capabilities

2. `code_assistant` (Model-based)
   - Code analysis
   - Generation capabilities
   - Security checks
   - Path-specific permissions

3. `review_assistant` (Model-based)
   - Code review capabilities
   - Documentation generation
   - Restricted modification permissions
   - Path-specific rules

4. `custom_assistant` (Both formats)
   - Fully customizable
   - Advanced features
   - Special use cases
   - Support for both policy formats

## Using Templates

```bash
# List available templates
aria list-templates

# Apply a template (capability-based)
aria apply chat_assistant -o policy.yml

# Apply a template (model-based)
aria apply code_assistant -o code-policy.yml

# Apply with parameters
aria apply chat_assistant --param safety_level=high -o policy.yml

# Customize a template
aria customize chat_assistant -o custom.yml
```

## Template Structure

### Capability-Based Template Structure
```yaml
name: template_name
version: 1.0.0
description: Template purpose
type: capability
parameters:
  - name: param1
    type: string
    description: Parameter description
    required: true
    default: default_value
    options:
      - option1
      - option2
capabilities:
  - name: capability_name
    description: Capability description
    allowed: true
    conditions:
      - Condition text
restrictions:
  - Restriction text
```

### Model-Based Template Structure
```yaml
name: template_name
version: 1.0.0
description: Template purpose
type: model
parameters:
  - name: param1
    type: string
    description: Parameter description
    required: true
    default: default_value
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

## Customizing Templates

Templates can be customized in several ways:

1. **Parameter Customization**: Provide parameter values when applying a template
   ```bash
   aria apply chat_assistant --param safety_level=high
   ```

2. **Template Modification**: Create a modified version of an existing template
   ```bash
   aria customize chat_assistant -o custom_template.yml
   ```

3. **Template Inheritance**: Create a new template that inherits from an existing one
   ```yaml
   name: custom_template
   version: 1.0.0
   inherits: chat_assistant
   description: Customized chat assistant
   ```

## Best Practices

1. Choose the appropriate template format for your use case
   - Capability-based for testing and human-readable policies
   - Model-based for production and integration with code repositories
2. Version your templates
3. Document customizations
4. Test before deployment
5. Keep templates simple and focused
6. Use parameters for customization points
7. Validate templates before sharing

## See Also

- [Policy Validation Guide](policy-validation.md)
- [Policy Inheritance](inheritance.md)
- [CLI Reference](cli.md)
- [Template API](../api/templates.md)
- [Policy Format Examples](../examples/policy-formats.yml)
