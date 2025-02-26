# Validator API Reference

## Overview

The Validator API provides tools for validating ARIA policies and templates. The validator supports both capability-based policies (primarily used for testing) and model-based policies (used in production).

## Classes

### ValidationResult

```python
class ValidationResult:
    """Represents a policy validation result.
    
    Attributes:
        valid: Whether validation passed
        errors: List of validation errors
        warnings: List of validation warnings
    """
    
    def add_error(self, message: str) -> None:
        """Add an error message."""
        
    def add_warning(self, message: str) -> None:
        """Add a warning message."""
        
    def as_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
```

### PolicyValidator

```python
class PolicyValidator:
    """Validates AI participation policies.
    
    This validator supports two policy formats:
    1. Capability-based policies - Used primarily for testing, with capabilities, 
       conditions, and restrictions
    2. Model-based policies - Used in production, with model types, defaults, and paths
    
    Attributes:
        REQUIRED_FIELDS: Set of required fields in policy
        OPTIONAL_FIELDS: Set of optional fields in policy
        MODEL_REQUIREMENTS: Valid requirements for each model
        MODEL_ACTIONS: Valid actions for each model
    """
    
    def validate_file(self, path: Union[str, Path], strict: bool = False) -> ValidationResult:
        """Validate a policy file."""
        
    def validate_policy(self, policy: Dict[str, Any], strict: bool = False) -> ValidationResult:
        """Validate policy data.
        
        Supports both capability-based policies (for testing) and model-based policies
        (for production).
        """
```

## Usage Examples

```python
# Validate a policy file
validator = PolicyValidator()
result = validator.validate_file("aria-policy.yml")
if result.valid:
    print("Policy is valid")
else:
    print("Errors:", result.errors)
    print("Warnings:", result.warnings)

# Validate a policy dictionary with strict validation
policy_data = {
    "version": "1.0.0",
    "name": "Test Policy",
    "description": "A comprehensive test policy.",
    "capabilities": [
        {
            "name": "test_capability",
            "description": "A detailed test capability description.",
            "allowed": True,
            "conditions": ["Must follow all testing guidelines."]
        }
    ],
    "restrictions": ["No unauthorized testing."]
}
result = validator.validate_policy(policy_data, strict=True)
if result.valid:
    print("Policy is valid")
    if result.warnings:
        print("Warnings:", result.warnings)
else:
    print("Errors:", result.errors)
```

## Validation Rules

### Required Fields
- `version`: String, policy version (required)
- `name`: String, policy name (required)

### Optional Fields
- `description`: String, policy description
- `capabilities`: List of capability dictionaries
- `restrictions`: List of restriction strings
- `model`: String, policy model type
- `defaults`: Dictionary of default rules
- `paths`: Dictionary of path-specific rules

### Strict Validation
When strict validation is enabled, the validator performs additional checks:
- Version format (semantic versioning)
- Description length
- Capability description length
- Condition format (ending with a period)
- Path pattern validity

## Best Practices

1. Always validate before saving or applying policies
2. Use strict validation during development
3. Handle validation errors and warnings appropriately
4. Provide clear error messages to users

## See Also

- [Policy API](policy.md)
- [Templates API](templates.md)
- [Validation Guide](../technical/validation.md)
