# Policy API Reference

## Overview

The Policy API provides interfaces for creating, managing, and validating ARIA policies. The system supports two policy formats: capability-based (primarily for testing) and model-based (for production).

## Policy Formats

### Capability-Based Policy

```yaml
version: "1.0.0"
name: "Test Policy"
description: "A comprehensive test policy."
capabilities:
  - name: "code_generation"
    description: "Generate code based on user requirements."
    allowed: true
    conditions:
      - "Must include appropriate comments."
restrictions:
  - "Must not retain user data beyond the session."
```

### Model-Based Policy

```yaml
version: "1.0.0"
name: "Production Policy"
model: "assistant"
defaults:
  allow:
    - "review"
    - "suggest"
  require:
    - "human_review"
paths:
  "src/**/*.py":
    allow:
      - "generate"
      - "modify"
```

## Classes

### Policy

```python
class Policy:
    """Represents an ARIA policy configuration.
    
    Supports both capability-based and model-based policy formats.
    """
    
    def __init__(self, name: str, version: str = "1.0.0", policy_type: str = "capability"):
        """Initialize a new policy.
        
        Args:
            name: Policy name
            version: Policy version (default: "1.0.0")
            policy_type: Type of policy ("capability" or "model")
        """
        
    def validate(self, strict: bool = False) -> ValidationResult:
        """Validate the policy configuration.
        
        Args:
            strict: Enable strict validation mode
            
        Returns:
            ValidationResult object with validation status and messages
        """
        
    def apply_template(self, template: str) -> None:
        """Apply a template to this policy."""
```

### PolicyManager

```python
class PolicyManager:
    """Manages policy operations and inheritance."""
    
    def load(self, path: str) -> Policy:
        """Load a policy from file."""
        
    def save(self, policy: Policy, path: str) -> None:
        """Save a policy to file."""
        
    def merge(self, base: Policy, child: Policy) -> Policy:
        """Merge two policies following inheritance rules."""
```

## Usage Examples

```python
# Create a new capability-based policy
policy = Policy("test_assistant", policy_type="capability")
policy.add_capability("code_generation", allowed=True)
policy.add_restriction("Must not retain user data beyond the session.")

# Create a new model-based policy
model_policy = Policy("production_assistant", policy_type="model")
model_policy.set_model("assistant")
model_policy.add_default_allow("review", "suggest")
model_policy.add_path_rule("src/**/*.py", allow=["generate", "modify"])

# Validate policies
validator = PolicyValidator()
result = validator.validate_policy(policy.as_dict(), strict=True)
if result.valid:
    print("Policy is valid!")
else:
    print("Validation errors:", result.errors)
```

## Best Practices

1. Choose the appropriate policy format for your use case
   - Capability-based for testing and human-readable policies
   - Model-based for production and integration with code repositories
2. Always validate policies after changes
3. Use version control
4. Document policy changes
5. Test inheritance chains
6. Use strict validation during development

## See Also

- [Templates API](templates.md)
- [Validator API](validator.md)
- [Policy Validation Guide](../guides/policy-validation.md)
- [Policy Format Examples](../examples/policy-formats.yml)
