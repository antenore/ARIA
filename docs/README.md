# ARIA Documentation Structure

This directory contains the complete documentation for the ARIA framework. The documentation is organized into the following sections:

## Directory Structure

```
docs/
├── api/          # API reference documentation
│   ├── cli.md    # CLI module API
│   ├── policy.md # Policy module API
│   └── ...       # Other API docs
│
├── guides/       # User guides and tutorials
│   ├── getting-started.md  # Quick start guide
│   ├── inheritance.md      # Policy inheritance guide
│   ├── templates.md        # Template usage guide
│   └── cli.md             # CLI usage guide
│
├── examples/     # Example files and configurations
│   ├── basic-policy.yml
│   ├── inherited-policy.yml
│   └── template-usage.yml
│
├── technical/    # Technical documentation
│   ├── policy.md          # Policy architecture
│   └── architecture.md    # System architecture
│
├── ci/           # CI/CD integration guides
│   └── github-actions.md  # GitHub Actions setup
│
└── index.md      # Main documentation page
```

## Documentation Standards

1. **File Format**: All documentation is written in Markdown
2. **Links**: Use relative links between documents
3. **Examples**: Include practical examples in all guides
4. **Versioning**: Documentation versions match ARIA releases

## Contributing

When contributing to the documentation:

1. Follow the existing structure
2. Update the index.md when adding new pages
3. Include examples for new features
4. Test all links and code examples
5. Update relevant sections when making code changes

## Building Documentation

The documentation can be built using MkDocs:

```bash
# Install MkDocs
python -m pip install --user mkdocs

# Build documentation
mkdocs build

# Serve documentation locally
mkdocs serve
```

## Contact

For questions about the documentation:
- File an issue on GitHub
- Join our Discord community
- Email the maintainers
