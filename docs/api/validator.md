# Validator API Reference

## Overview

The Validator API provides tools for validating ARIA policies and templates.

## Classes

### Validator

```python
class Validator:
    """Base validator for ARIA configurations."""
    
    def validate(self, config: Dict) -> bool:
        """Validate a configuration."""
        
    def get_errors(self) -> List[str]:
        """Get validation errors."""
```

### PolicyValidator

```python
class PolicyValidator(Validator):
    """Validates ARIA policies."""
    
    def validate_inheritance(self, policy: Policy) -> bool:
        """Validate policy inheritance chain."""
        
    def validate_permissions(self, policy: Policy) -> bool:
        """Validate policy permissions."""
```

### TemplateValidator

```python
class TemplateValidator(Validator):
    """Validates ARIA templates."""
    
    def validate_parameters(self, template: Template) -> bool:
        """Validate template parameters."""
        
    def validate_compatibility(self, template: Template, policy: Policy) -> bool:
        """Check template-policy compatibility."""
```

## Usage Examples

```python
# Validate a policy
validator = PolicyValidator()
if validator.validate(policy):
    print("Policy is valid")
else:
    print("Errors:", validator.get_errors())

# Check template compatibility
template_validator = TemplateValidator()
if template_validator.validate_compatibility(template, policy):
    print("Template can be applied")
```

## Best Practices

1. Always validate before saving
2. Check inheritance chains
3. Verify template compatibility
4. Handle validation errors gracefully

## See Also

- [Policy API](policy.md)
- [Templates API](templates.md)
- [Validation Guide](../technical/validation.md)
