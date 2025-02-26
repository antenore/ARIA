# Integrating ARIA with Cursor

This guide explains how to integrate ARIA policies with the Cursor AI coding assistant.

## Overview

Cursor can be configured to respect ARIA policies through a custom extension that validates all AI-suggested changes against your policy files before applying them.

## Integration Options

Cursor offers two approaches for integrating with ARIA:

1. **Full ARIA Plugin Integration** (as described below)
2. **Using Existing Cursor Rules** (see [Using IDE Rules for ARIA Policies](ide-rules.md))

For quick implementation, consider using the existing `.cursorrules` mechanism, which requires no additional plugins.

## Setup

### 1. Install the ARIA-Cursor Extension

```bash
# Install the ARIA framework
python -m pip install --user aria-framework

# Install the Cursor extension
npm install -g aria-cursor-extension
```

### 2. Configure Cursor

Add the following to your Cursor configuration file:

```json
{
  "extensions": {
    "aria": {
      "enabled": true,
      "policyFile": "./docs_protection_policy.yml",
      "enforcementLevel": "strict",
      "violationAction": "prevent"
    }
  }
}
```

Configuration options:
- `policyFile`: Path to your ARIA policy file
- `enforcementLevel`: Level of enforcement ("strict", "standard", or "relaxed")
- `violationAction`: Action to take when policy is violated ("prevent", "warn", or "record")

## How It Works

1. When Cursor suggests code changes, the ARIA extension analyzes the changes
2. The extension checks if the changes comply with your ARIA policy
3. If the changes violate the policy (e.g., modifying files in a restricted directory), the extension takes the configured action
4. For "prevent" mode, Cursor will display an error message and not apply the changes

## Example: Enforcing Docs Protection

With the `docs_protection_policy.yml` that denies changes to the docs folder:

1. When Cursor attempts to modify a file in the docs folder, the ARIA extension checks the policy
2. The extension detects that the policy denies modifications to the docs folder
3. The change is blocked, and Cursor displays a message: "This change violates the ARIA policy: docs folder modifications are not allowed"

## Command Line Interface

You can also use the ARIA CLI to validate Cursor suggestions before applying them:

```bash
# Export Cursor suggestions to a patch file
cursor export-suggestions --format=patch > suggestions.patch

# Validate the patch against your ARIA policy
ariacli policy validate-patch --policy=docs_protection_policy.yml --patch=suggestions.patch

# If validation passes, apply the patch
git apply suggestions.patch
```

## Enforcement Levels

The ARIA-Cursor extension supports different enforcement levels:

- **Strict**: Blocks any changes that violate the policy
- **Standard**: Blocks critical violations but allows minor ones with warnings
- **Relaxed**: Only warns about violations without blocking changes

## Troubleshooting

If you encounter issues with the ARIA-Cursor integration:

1. Verify your policy file is valid: `ariacli policy validate your_policy.yml`
2. Check that the policy path in your Cursor configuration is correct
3. Examine the Cursor extension logs for detailed error messages

## Next Steps

- Learn about [custom policy rules](custom-rules.md) for Cursor
- Set up [automated policy checks](automated-checks.md) in your workflow
- Explore [policy visualization](policy-visualization.md) in Cursor
