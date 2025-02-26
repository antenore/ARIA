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

## Limitations of Current Implementation

The current IDE integration has some important limitations to be aware of:

1. **Partial Enforcement**: 
   - Ignore files (`.codeiumignore`, `.cursorignore`) provide technical enforcement by preventing AI from accessing certain files
   - Rule files (`.windsurfrules`, `.cursorrules`) provide policy guidance but don't technically prevent modifications

2. **Reliance on AI Behavior**:
   - Rules rely on the AI assistant following them
   - There's no technical mechanism to prevent an AI from modifying files it can access

3. **Future Improvements**:
   - Full IDE plugins are planned that will provide proper technical enforcement
   - These will intercept and validate AI actions against policies before allowing them

For maximum protection with the current implementation:
- Use ignore files for truly sensitive files that AI should never access
- Use rule files for files that AI can read but should not modify
- Regularly audit AI-generated changes against your policies

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

## IDE Ignore Files

In addition to rules files, many IDEs support ignore files that control which files the AI assistant can access. ARIA can generate these files based on your policy:

- `.codeiumignore` for Windsurf
- `.cursorignore` for Cursor

These files follow the same syntax as `.gitignore` and help enforce your ARIA policy by:

1. Protecting policy files themselves from AI modification
2. Restricting AI access to sensitive paths defined in your policy
3. Protecting IDE rule files from modification

### Generating Ignore Files

You can generate ignore files alongside rules files:

```bash
python -m aria.tools.policy_to_iderules policy.yml --ignore
```

This will generate both a rules file and an ignore file appropriate for your selected IDE.

### Ignore File Structure

The generated ignore files include:

```
# BEGIN ARIA POLICY
# ARIA Policy: Your Policy Name
# Your policy description

# Protect ARIA policy files
*.aria.yaml
*.aria.yml
.aria/

# Protect IDE rule files
.windsurfrules
.cursorrules
...

# Protect IDE ignore files
.codeiumignore
.cursorignore

# Protected paths from ARIA policy
/sensitive/path/
/config/secrets.json
...
# END ARIA POLICY
```

### Benefits of Ignore Files

Using ignore files provides stronger enforcement than rules alone:

- **Technical Enforcement**: While rules rely on the AI assistant's compliance, ignore files technically prevent access
- **Defense in Depth**: Combining rules and ignore files creates multiple layers of protection
- **Clear Boundaries**: Explicitly defines which files are off-limits to AI assistance

### Customizing Ignore Patterns

You can customize the generated ignore files by:

1. Editing the patterns outside the ARIA policy section
2. Modifying your ARIA policy to include different path protections
3. Using a custom output file with the `--ignore-output` option

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
