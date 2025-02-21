# CLI Module API Reference

::: aria.cli
    options:
      show_source: true
      show_root_heading: true
      show_category_heading: true

## Command Groups

### Main CLI Group

The main entry point for the ARIA CLI.

```python
@click.group()
def cli():
    """ARIA - AI Participation Manager."""
    pass
```

### Template Commands

Commands for managing templates:

- `list` - List available templates
- `apply` - Apply a template to create a policy

### Policy Commands

Commands for managing policies:

- `validate` - Validate a policy file

## Decorators

### @handle_error

Error handling decorator that provides consistent error handling across all commands.

```python
def handle_error(func):
    """Decorator to handle errors in CLI commands."""
    pass
```

### @with_progress

Progress indicator decorator for long-running operations.

```python
def with_progress(description: str):
    """Decorator to add progress indicator for long-running operations."""
    pass
```

## Command Aliases

The CLI provides several aliases for commonly used commands:

```python
@cli.command(name='ls')
def list_templates_alias():
    """Alias for 'template list'"""
    pass

@cli.command(name='apply')
def apply_alias():
    """Alias for 'template apply'"""
    pass

@cli.command(name='validate')
def validate_alias():
    """Alias for 'policy validate'"""
    pass
```

## Progress Indicators

The CLI uses Rich's progress bars and spinners to provide visual feedback:

```python
with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    console=console,
) as progress:
    task = progress.add_task(description)
    # Perform operation
```

## Error Handling

All commands use the `handle_error` decorator to ensure consistent error handling:

1. Catch all exceptions
2. Log the error
3. Display user-friendly message
4. Exit with appropriate code
