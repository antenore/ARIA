# Integrating ARIA with Windsurf

This guide explains how to integrate ARIA policies with the Windsurf AI coding assistant.

## Overview

Windsurf can be configured to respect ARIA policies through a custom integration that validates all AI-suggested changes against your policy files before applying them.

## Setup

### 1. Install the ARIA-Windsurf Plugin

```bash
# Install the ARIA framework
python -m pip install --user aria-framework

# Install the Windsurf plugin
python -m pip install --user aria-windsurf-plugin
```

### 2. Configure Windsurf

Add the following to your Windsurf configuration file:

```json
{
  "plugins": {
    "aria": {
      "enabled": true,
      "policyPath": "./docs_protection_policy.yml",
      "strictMode": true,
      "onViolation": "block"
    }
  }
}
```

Configuration options:
- `policyPath`: Path to your ARIA policy file
- `strictMode`: If true, any policy validation errors will block changes
- `onViolation`: Action to take when policy is violated ("block", "warn", or "log")

## Integration Options

Windsurf offers two approaches for integrating with ARIA:

1. **Full ARIA Plugin Integration** (as described below)
2. **Using Existing Windsurf Rules** (see [Using IDE Rules for ARIA Policies](ide-rules.md))

For quick implementation, consider using the existing `.windsurfrules` mechanism, which requires no additional plugins.

## Plugin Architecture

## How It Works

1. When you use Windsurf to generate or modify code, the ARIA plugin intercepts the changes
2. The plugin checks if the proposed changes comply with your ARIA policy
3. If the changes violate the policy (e.g., modifying files in a restricted directory), the plugin blocks the changes
4. Windsurf displays an error message explaining why the changes were blocked

## Example: Enforcing Docs Protection

With the `docs_protection_policy.yml` that denies changes to the docs folder:

1. When Windsurf attempts to modify a file in the docs folder, the ARIA plugin checks the policy
2. The plugin detects that the policy denies modifications to the docs folder
3. The change is blocked, and Windsurf displays a message: "Changes to docs folder are not allowed per ARIA policy"

## Programmatic Usage

You can also integrate ARIA validation directly in your Windsurf workflows:

```python
from aria_windsurf import PolicyValidator

# Initialize the validator with your policy
validator = PolicyValidator("./docs_protection_policy.yml")

# Check if a file modification is allowed
is_allowed = validator.check_modification("docs/guides/getting-started.md")
if not is_allowed:
    print("This modification is not allowed by the ARIA policy")
```

## Customizing Behavior

You can customize how Windsurf responds to policy violations:

- **Block Mode**: Prevents any changes that violate the policy
- **Warning Mode**: Allows changes but displays warnings
- **Logging Mode**: Allows changes but logs violations for later review

## Troubleshooting

If you encounter issues with the ARIA-Windsurf integration:

1. Ensure your policy file is valid: `ariacli policy validate your_policy.yml`
2. Check that the policy path in your Windsurf configuration is correct
3. Review the Windsurf logs for detailed error messages

## Next Steps

- Explore [advanced configuration options](advanced-windsurf-integration.md)
- Learn how to [create custom policy validators](custom-validators.md) for Windsurf
- Set up [CI/CD integration](ci-integration.md) to validate policies automatically
