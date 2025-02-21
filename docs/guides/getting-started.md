# Getting Started with ARIA

This guide will help you get started with ARIA quickly and efficiently.

## Installation

```bash
python -m pip install --user aria-policy
```

## Basic Usage

1. Initialize a new policy:
   ```bash
   aria init -m assistant -o policy.yml
   ```

2. Apply a template:
   ```bash
   aria apply chat_assistant -o policy.yml
   ```

3. Validate your policy:
   ```bash
   aria validate policy.yml
   ```

## Next Steps

- Learn about [policy inheritance](inheritance.md)
- Explore [templates](templates.md)
- Check out the [CLI reference](cli.md)

## Common Issues

- Permission errors
- Template compatibility
- Policy validation failures

## Best Practices

1. Always validate policies
2. Use version control
3. Document policy changes
4. Test before deployment
