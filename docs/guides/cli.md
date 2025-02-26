# Command Line Interface

ARIA provides a powerful command-line interface (CLI) for managing AI participation policies and templates.

## Command Structure

The CLI follows a simple and intuitive structure:

```bash
aria <command> [subcommand] [options]
```

## Basic Commands

### Initialize a Policy

Create a new policy file:

```bash
aria init [options]
```

Options:
- `-m, --model MODEL` - Initial policy model (default: 'assistant')
- `-o, --output FILE` - Output file for the policy (default: 'aria.yml')
- `-t, --templates-dir DIR` - Directory containing templates
- `-f, --format FORMAT` - Policy format: 'capability' or 'model' (default: 'model')

### Template Management

List available templates:

```bash
aria template list [options]
# or use the shorter alias
aria ls
```

Options:
- `-f, --format FORMAT` - Filter templates by format: 'capability' or 'model'

Apply a template:

```bash
aria template apply NAME [options]
# or use the shorter alias
aria apply NAME
```

Options:
- `-t, --templates-dir DIR` - Directory containing templates
- `-o, --output FILE` - Output file for the policy
- `-f, --format FORMAT` - Template format: 'capability' or 'model' (default: 'model')

### Policy Management

Validate a policy file:

```bash
aria policy validate FILE [options]
# or use the shorter alias
aria validate FILE [options]
```

Options:
- `-s, --strict` - Enable strict validation mode
- `--format FORMAT` - Specify policy format for validation: 'capability', 'model', or 'auto' (default: 'auto')

## Command Aliases

ARIA provides convenient aliases for commonly used commands:

| Full Command | Alias | Description |
|-------------|-------|-------------|
| `aria template list` | `aria ls` | List available templates |
| `aria template apply` | `aria apply` | Apply a template |
| `aria policy validate` | `aria validate` | Validate a policy file |

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
   aria init -f capability -o my-policy.yml
   ```

2. Create a new model-based policy:
   ```bash
   aria init -m assistant -f model -o my-policy.yml
   ```

3. List all available templates:
   ```bash
   aria ls
   ```

4. List only capability-based templates:
   ```bash
   aria ls -f capability
   ```

5. Apply a capability-based template:
   ```bash
   aria apply basic_capabilities -f capability -o new-policy.yml
   ```

6. Apply a model-based template:
   ```bash
   aria apply basic_model -f model -o new-policy.yml
   ```

7. Validate a policy with automatic format detection:
   ```bash
   aria validate policy.yml
   ```

8. Validate a policy with strict validation:
   ```bash
   aria validate policy.yml --strict
   ```

9. Validate a policy with explicit format:
   ```bash
   aria validate policy.yml --format capability
   ```

## Environment Variables

- `ARIA_TEMPLATES_DIR` - Default templates directory
- `ARIA_LOG_LEVEL` - Logging level (default: INFO)
- `ARIA_DEFAULT_FORMAT` - Default policy format (capability or model)

## Exit Codes

- 0: Success
- 1: Error (with error message)
