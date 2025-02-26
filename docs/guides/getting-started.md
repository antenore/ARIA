# Getting Started with ARIA

This guide will help you get started with ARIA quickly and efficiently.

## Installation

```bash
python -m pip install --user aria-framework
```
## Local Development Installation

If you're working on ARIA itself or want to install from a local copy:

```bash
# Clone the repository
git clone https://github.com/antenore/ARIA.git
cd ARIA

# Install in development mode
python -m pip install --user -e .
```

> **Note**: After installation, the `ariacli` command might not be available in your PATH. You can either:
> 1. Add the Python Scripts directory to your PATH (typically `%APPDATA%\Python\Python3xx\Scripts` on Windows)
> 2. Use the full path to the executable: `%APPDATA%\Python\Python3xx\Scripts\ariacli.exe`
> 3. Create an alias in your shell profile

## Basic Usage

1. Initialize a new policy:
   ```bash
   ariacli init -m assistant -o policy.yml
   ```

2. Apply a template:
   ```bash
   ariacli template apply chat_assistant -o policy.yml
   ```

3. Validate your policy:
   ```bash
   ariacli policy validate policy.yml
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
