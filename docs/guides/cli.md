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

### Template Management

List available templates:

```bash
aria template list [options]
# or use the shorter alias
aria ls
```

Apply a template:

```bash
aria template apply NAME [options]
# or use the shorter alias
aria apply NAME
```

Options:
- `-t, --templates-dir DIR` - Directory containing templates
- `-o, --output FILE` - Output file for the policy

### Policy Management

Validate a policy file:

```bash
aria policy validate FILE
# or use the shorter alias
aria validate FILE
```

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

1. Create a new policy using the assistant model:
   ```bash
   aria init -m assistant -o my-policy.yml
   ```

2. List available templates:
   ```bash
   aria ls
   # or
   aria template list
   ```

3. Apply a template and save to a file:
   ```bash
   aria apply basic -o new-policy.yml
   # or
   aria template apply basic -o new-policy.yml
   ```

4. Validate an existing policy:
   ```bash
   aria validate policy.yml
   # or
   aria policy validate policy.yml
   ```

## Environment Variables

- `ARIA_TEMPLATES_DIR` - Default templates directory
- `ARIA_LOG_LEVEL` - Logging level (default: INFO)

## Exit Codes

- 0: Success
- 1: Error (with error message)
