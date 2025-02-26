# Command Line Interface

ARIA provides a powerful command-line interface (CLI) for managing AI participation policies and templates.

## Command Structure

The CLI follows a simple and intuitive structure:

```bash
ariacli <command> [subcommand] [options]
```

## Basic Commands

### Initialize a Policy

Create a new policy file:

```bash
ariacli init [options]
```

Options:
- `-m, --model MODEL` - Initial policy model (default: 'assistant')
- `-o, --output FILE` - Output file for the policy (default: 'aria.yml')
- `-t, --templates-dir DIR` - Directory containing templates
- `-f, --format FORMAT` - Policy format: 'capability' or 'model' (default: 'model')

### Template Management

List available templates:

```bash
ariacli template list [options]
# or use the shorter alias
ariacli ls
```

Options:
- `-f, --format FORMAT` - Filter templates by format: 'capability' or 'model'

Apply a template:

```bash
ariacli template apply NAME [options]
# or use the shorter alias
ariacli apply NAME
```

Options:
- `-t, --templates-dir DIR` - Directory containing templates
- `-o, --output FILE` - Output file for the policy
- `-f, --format FORMAT` - Template format: 'capability' or 'model' (default: 'model')

### Policy Management

Validate a policy file:

```bash
ariacli policy validate FILE [options]
# or use the shorter alias
ariacli validate FILE [options]
```

Options:
- `-s, --strict` - Enable strict validation mode
- `--format FORMAT` - Specify policy format for validation: 'capability', 'model', or 'auto' (default: 'auto')

## Command Aliases

ARIA provides convenient aliases for commonly used commands:

| Full Command | Alias | Description |
|-------------|-------|-------------|
| `ariacli template list` | `ariacli ls` | List available templates |
| `ariacli template apply` | `ariacli apply` | Apply a template |
| `ariacli policy validate` | `ariacli validate` | Validate a policy file |

## Progress Indicators

All commands now include progress indicators to provide feedback during long-running operations:

- Spinners for ongoing operations
- Clear success/error messages
- Rich console output with color-coding

## Error Handling

The CLI provides comprehensive error handling:

- Descriptive error messages
- Proper exit codes (0 for success, 1 for errors)
- Logging of all operations
- Input validation before execution

## Examples

1. Create a new capability-based policy:
   ```bash
   ariacli init -f capability -o my-policy.yml
   ```

2. Create a new model-based policy:
   ```bash
   ariacli init -m assistant -f model -o my-policy.yml
   ```

3. List all available templates:
   ```bash
   ariacli ls
   ```

4. List only capability-based templates:
   ```bash
   ariacli ls -f capability
   ```

5. Apply a capability-based template:
   ```bash
   ariacli apply basic_capabilities -f capability -o new-policy.yml
   ```

6. Apply a model-based template:
   ```bash
   ariacli apply basic_model -f model -o new-policy.yml
   ```

7. Validate a policy with automatic format detection:
   ```bash
   ariacli validate policy.yml
   ```

8. Validate a policy with strict validation:
   ```bash
   ariacli validate policy.yml --strict
   ```

9. Validate a policy with explicit format:
   ```bash
   ariacli validate policy.yml --format capability
   ```

## Additional Tools

ARIA includes additional utility tools:

### IDE Integration Commands

ARIA provides commands for integrating with various IDEs:

```bash
ariacli ide [command] [options]
```

Available commands:

#### Generate IDE Rules

```bash
ariacli ide rules [policy_file] [options]
```

Options:
- `policy_file` - Path to ARIA policy file (optional, defaults to aria.yml)
- `-i, --ide` - Target IDE (default: windsurf, options: windsurf, cursor, vscode, nvim, emacs)
- `-o, --output` - Custom output file for rules (default depends on IDE)

#### Generate IDE Ignore Files

```bash
ariacli ide ignore [policy_file] [options]
```

Options:
- `policy_file` - Path to ARIA policy file (optional, defaults to aria.yml)
- `-i, --ide` - Target IDE (default: windsurf, options: windsurf, cursor)
- `-o, --output` - Custom output file for ignore patterns (default depends on IDE)

#### Generate Both Rules and Ignore Files

```bash
ariacli ide generate [policy_file] [options]
```

Options:
- `policy_file` - Path to ARIA policy file (optional, defaults to aria.yml)
- `-i, --ide` - Target IDE (default: windsurf, options: windsurf, cursor, vscode, nvim, emacs)
- `--rules-output` - Custom output file for rules (default depends on IDE)
- `--ignore-output` - Custom output file for ignore patterns (default depends on IDE)
- `--no-ignore` - Skip generating ignore file

Examples:
```bash
# Generate Windsurf rules from default policy
ariacli ide rules

# Generate Cursor rules from a specific policy
ariacli ide rules my_policy.yml -i cursor

# Generate both rules and ignore file for Windsurf
ariacli ide generate my_policy.yml

# Generate both rules and ignore file for Cursor with custom ignore file
ariacli ide generate -i cursor --ignore-output .custom_ignore
```

### Policy to IDE Rules Converter

Convert ARIA policy files to various IDE rules formats:

```bash
python -m aria.tools.policy_to_iderules <policy_file> [-i <ide>] [-o <output_file>] [--ignore] [--ignore-output <file>]
```

Options:
- `<policy_file>`: Path to ARIA policy file
- `-i, --ide`: Target IDE (default: windsurf, options: windsurf, cursor, vscode, nvim, emacs)
- `-o, --output`: Custom output file for rules (default depends on IDE)
- `--ignore`: Also generate IDE ignore file (.codeiumignore for Windsurf, .cursorignore for Cursor)
- `--ignore-output`: Custom output file for ignore patterns (default depends on IDE)

Examples:
```bash
# Convert a policy to Windsurf rules
python -m aria.tools.policy_to_iderules docs_protection_policy.yml

# Convert a policy to Cursor rules
python -m aria.tools.policy_to_iderules aria_policy.yml -i cursor

# Convert a policy to a custom rules file
python -m aria.tools.policy_to_iderules aria_policy.yml -o custom_rules.txt

# Generate both rules and ignore file for Windsurf
python -m aria.tools.policy_to_iderules aria_policy.yml --ignore

# Generate both rules and ignore file for Cursor with custom ignore file
python -m aria.tools.policy_to_iderules aria_policy.yml -i cursor --ignore --ignore-output .custom_ignore
```

This tool helps you quickly implement ARIA policies using existing IDE rule systems. The tool preserves existing content in rules files and only updates the ARIA policy section. When generating ignore files, it creates patterns that protect policy files and sensitive paths based on your ARIA policy.

## Environment Variables

- `ARIA_TEMPLATES_DIR` - Default templates directory
- `ARIA_LOG_LEVEL` - Logging level (default: INFO)
- `ARIA_DEFAULT_FORMAT` - Default policy format (capability or model)

## Exit Codes

- 0: Success
- 1: Error (with error message)
