# Templates API Reference

## Overview

The Templates API provides functionality for creating, managing, and applying ARIA templates.

## Classes

### Template

```python
class Template:
    """Represents an ARIA template."""
    
    def __init__(self, name: str, version: str = "1.0.0"):
        """Initialize a new template."""
        
    def validate(self) -> bool:
        """Validate the template structure."""
        
    def apply(self, policy: Policy) -> None:
        """Apply this template to a policy."""
```

### TemplateManager

```python
class TemplateManager:
    """Manages template operations."""
    
    def load(self, path: str) -> Template:
        """Load a template from file."""
        
    def save(self, template: Template, path: str) -> None:
        """Save a template to file."""
        
    def list_templates(self) -> List[str]:
        """List available templates."""
```

## Usage Examples

```python
# Create a new template
template = Template("chat_assistant")

# Save the template
manager = TemplateManager()
manager.save(template, "template.yml")

# List available templates
templates = manager.list_templates()
```

## Best Practices

1. Version your templates
2. Document parameters
3. Test templates
4. Keep templates focused

## See Also

- [Policy API](policy.md)
- [Templates Guide](../guides/templates.md)
- [Example Templates](../examples/template-usage.yml)
