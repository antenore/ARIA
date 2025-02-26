# Templates API Reference

## Overview

The Templates API provides functionality for creating, managing, and applying ARIA templates. Templates support both capability-based and model-based policy formats.

## Classes

### Template

```python
class Template:
    """Represents an ARIA template.
    
    Templates can be used to create both capability-based and model-based policies.
    """
    
    def __init__(self, name: str, version: str = "1.0.0", template_type: str = "capability"):
        """Initialize a new template.
        
        Args:
            name: Template name
            version: Template version (default: "1.0.0")
            template_type: Type of template ("capability" or "model")
        """
        
    def validate(self, strict: bool = False) -> ValidationResult:
        """Validate the template structure.
        
        Args:
            strict: Enable strict validation mode
            
        Returns:
            ValidationResult object with validation status and messages
        """
        
    def apply(self, policy: Policy) -> None:
        """Apply this template to a policy."""
        
    def get_parameters(self) -> List[Dict[str, Any]]:
        """Get template parameters."""
        
    def set_parameter(self, name: str, value: Any) -> None:
        """Set a parameter value."""
```

### TemplateManager

```python
class TemplateManager:
    """Manages template operations."""
    
    def load(self, path: str) -> Template:
        """Load a template from file."""
        
    def save(self, template: Template, path: str) -> None:
        """Save a template to file."""
        
    def list_templates(self, directory: str = None) -> List[str]:
        """List available templates.
        
        Args:
            directory: Optional directory to search for templates
            
        Returns:
            List of template names
        """
        
    def get_template_info(self, name: str) -> Dict[str, Any]:
        """Get detailed information about a template.
        
        Args:
            name: Template name
            
        Returns:
            Dictionary with template metadata
        """
```

## Template Formats

### Capability-Based Template

```yaml
name: capability_template
version: 1.0.0
description: Template for capability-based policies
type: capability
parameters:
  - name: capability_level
    type: string
    description: Level of capabilities to enable
    default: basic
    options:
      - basic
      - advanced
      - expert
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

### Model-Based Template

```yaml
name: model_template
version: 1.0.0
description: Template for model-based policies
type: model
parameters:
  - name: security_level
    type: string
    description: Security level for the policy
    default: standard
    options:
      - minimal
      - standard
      - strict
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

## Usage Examples

```python
# Create a new capability-based template
template = Template("chat_assistant", template_type="capability")
template.add_capability("text_generation", allowed=True)
template.add_restriction("Must not retain user data beyond the session.")

# Create a new model-based template
model_template = Template("code_assistant", template_type="model")
model_template.set_model("assistant")
model_template.add_default_allow("review", "suggest")
model_template.add_path_rule("src/**/*.py", allow=["generate", "modify"])

# Save templates
manager = TemplateManager()
manager.save(template, "chat_template.yml")
manager.save(model_template, "code_template.yml")

# List available templates
templates = manager.list_templates()
for template_name in templates:
    info = manager.get_template_info(template_name)
    print(f"{info['name']} (v{info['version']}): {info['description']}")
```

## Best Practices

1. Choose the appropriate template format for your use case
   - Capability-based for testing and human-readable policies
   - Model-based for production and integration with code repositories
2. Version your templates
3. Document parameters and their purpose
4. Test templates with different parameter values
5. Keep templates focused on specific use cases

## See Also

- [Policy API](policy.md)
- [Validator API](validator.md)
- [Templates Guide](../guides/templates.md)
- [Example Templates](../examples/template-usage.yml)
- [Policy Format Examples](../examples/policy-formats.yml)
