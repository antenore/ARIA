# AI Tool Integration

This section covers how to integrate ARIA policies with various AI coding assistants and tools.

## Available Integrations

ARIA can be integrated with several popular AI coding tools:

- [Windsurf Integration](windsurf.md)
- [Cursor Integration](cursor.md)
- [GitHub Copilot Integration](github-copilot.md)
- [Visual Studio Code Integration](vscode.md)
- [Using IDE Rules for ARIA Policies](ide-rules.md)

## Integration Approaches

There are two main approaches to integrating ARIA with AI tools:

1. **Full SDK Integration**: Developing plugins that use the ARIA SDK for complete policy enforcement
2. **Rules-Based Integration**: Using existing rules mechanisms (like `.windsurfrules` or `.cursorrules`) for simpler implementation

Choose the approach that best fits your needs:
- Use **Full SDK Integration** for comprehensive policy enforcement with granular control
- Use **Rules-Based Integration** for quick implementation with existing tools

## General Integration Approach

While each tool has its specific integration method, the general approach follows these steps:

1. **Policy Loading**: The integration loads your ARIA policy file
2. **Change Interception**: The integration intercepts changes proposed by the AI tool
3. **Policy Validation**: Changes are validated against the policy
4. **Enforcement**: Based on validation results, changes are allowed, blocked, or flagged

## Integration Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│             │     │              │     │             │
│  AI Coding  │────▶│ ARIA Policy  │────▶│  Modified   │
│    Tool     │     │  Validator   │     │   Files     │
│             │     │              │     │             │
└─────────────┘     └──────────────┘     └─────────────┘
                           │
                           │
                           ▼
                    ┌──────────────┐
                    │              │
                    │   Policy     │
                    │    File      │
                    │              │
                    └──────────────┘
```

## Core Integration Components

### 1. Policy Loader

Loads and parses ARIA policy files, handling inheritance and template application.

### 2. Change Analyzer

Analyzes proposed changes to determine:
- Which files are being modified
- What type of modifications are being made
- Which policy statements apply to these changes

### 3. Policy Enforcer

Enforces policy decisions by:
- Blocking prohibited changes
- Allowing permitted changes
- Logging policy violations
- Providing feedback to users

## Creating Custom Integrations

If you need to integrate ARIA with a tool not listed here, you can create a custom integration using the ARIA API:

```python
from aria.core.policy import PolicyManager
from aria.core.validator import PolicyValidator

# Load policy
policy_manager = PolicyManager()
policy = policy_manager.load_policy("./docs_protection_policy.yml")

# Create validator
validator = PolicyValidator(policy)

# Validate a proposed change
result = validator.validate_change(
    file_path="docs/guides/getting-started.md",
    action="modify",
    actor="ai_assistant"
)

if not result.is_allowed:
    print(f"Change not allowed: {result.reason}")
```

## Best Practices

1. **Clear Error Messages**: Provide clear feedback when changes are blocked
2. **Performance Optimization**: Cache policy validation results when possible
3. **Graceful Degradation**: If policy validation fails, default to a safe mode
4. **User Override**: Allow users to override policy decisions with proper authentication
5. **Audit Logging**: Log all policy decisions for later review

## Next Steps

- Learn how to [create custom policy validators](custom-validators.md)
- Explore [policy visualization tools](policy-visualization.md)
- Set up [CI/CD integration](ci-integration.md)
