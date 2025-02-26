# Using IDE Rules for ARIA Policies

This guide explains how to use existing IDE rule systems to implement ARIA policies without requiring additional plugins.

## Overview

Many AI-powered IDEs already have built-in rule systems:
- Windsurf uses `.windsurfrules`
- Cursor uses `.cursorrules`
- Other IDEs have similar mechanisms

We can leverage these existing mechanisms to enforce ARIA policies with minimal setup.

## Converting ARIA Policies to IDE Rules

### Basic Conversion Examples

| ARIA Policy Statement | Equivalent IDE Rule |
|------------------------|--------------------------|
| `deny` actions on `docs/**/*` | `AI assistants must not modify files in the docs/ directory` |
| `allow: ["suggest"]` on `src/**/*.py` | `AI assistants may suggest changes to Python files in src/ but must not implement them directly` |
| `require: ["human_review"]` | `All AI-generated code must be reviewed by a human before being committed` |

## Implementation Steps

1. **Create a rules file** in your project root (e.g., `.windsurfrules` or `.cursorrules`)
2. **Translate your ARIA policy** into natural language rules
3. **Add specific path restrictions** for protected directories

## Example: Docs Protection Policy

Here's how to convert the `docs_protection_policy.yml` to IDE rules:

```
# ARIA Policy Enforcement
1. AI assistants must not modify, create, or delete any files in the docs/ directory
2. AI assistants may suggest changes to documentation but must not implement them
3. All documentation changes require human review and approval from the docs team
```

## Example: General ARIA Policy

For the main `aria_policy.yml`, you might use:

```
# ARIA Policy Enforcement
1. AI assistants may suggest and review code in all areas by default
2. AI assistants may modify and generate code in the aria/ directory with human review
3. AI assistants may modify and generate tests with appropriate test coverage
4. AI assistants may suggest changes to GitHub workflows but must not implement them directly
```

## Using the Conversion Tool

ARIA provides a tool to automatically convert policies to IDE rules:

```bash
# Convert to Windsurf rules (default)
python -m aria.tools.policy_to_iderules aria_policy.yml

# Convert to Cursor rules
python -m aria.tools.policy_to_iderules aria_policy.yml -i cursor

# Convert to a custom rules file
python -m aria.tools.policy_to_iderules aria_policy.yml -o custom_rules.txt
```

The tool preserves existing content in rules files and only updates the ARIA policy section.

## Supported IDEs

Currently, the tool supports:
- Windsurf (`.windsurfrules`)
- Cursor (`.cursorrules`)

Future support is planned for:
- Visual Studio Code (`.vscode/aria-rules.json`)
- Neovim (`.nvim/aria-rules.lua`)
- Emacs (`.emacs.d/aria-rules.el`)

## Advantages and Limitations

### Advantages
- Uses existing IDE functionality
- No additional plugins required
- Simple to implement and understand
- Works immediately

### Limitations
- Less granular control than a full ARIA implementation
- Manual translation required (unless using the conversion tool)
- Enforcement depends on the AI assistant's compliance
- No programmatic validation

## Best Practices

1. **Be explicit** about which directories are protected
2. **Use clear language** that both humans and AI can understand
3. **Organize rules** by area of concern
4. **Update rules** when your ARIA policies change

## Future Integration

While this approach works as an immediate solution, a full ARIA SDK would provide:
- Automated policy translation
- Programmatic enforcement
- More granular control
- Policy validation

The ARIA project is actively working on developing plugins for various IDEs:
- Windsurf
- Cursor
- Visual Studio Code
- Neovim
- Emacs
- JetBrains IDEs

## Next Steps

1. Create your IDE rules file based on your ARIA policies
2. Test with your IDE to ensure proper enforcement
3. Consider contributing to the development of full ARIA plugins for your favorite IDE
