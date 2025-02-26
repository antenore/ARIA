# Testing ARIA on Itself

This guide demonstrates how to use ARIA to manage AI participation in the ARIA project itself, providing a practical example of how the framework can be applied.

## Overview

We've created two policy files to demonstrate ARIA's capabilities:

1. **Main Policy** (`aria_policy.yml`): Defines how AI can participate in different parts of the ARIA codebase
2. **Docs Protection Policy** (`docs_protection_policy.yml`): A more restrictive policy that prevents any changes to the documentation folder

## Main Policy

The main policy allows AI to suggest, modify, and generate code in the core ARIA modules, tests, and documentation, with appropriate safeguards:

```yaml
name: "ARIA Self-Policy"
description: "Policy defining how AI can participate in the ARIA project itself"
version: "1.0"
model: "assistant"

defaults:
  allow: ["suggest", "review"]  # Allow suggestions and reviews by default
  require:
    - human_review
    - tests

paths:
  'aria/**/*.py':
    allow: 
      - suggest
      - modify
      - generate
    require:
      - human_review
      - tests
      - documentation
  
  'tests/**/*.py':
    allow:
      - suggest
      - modify
      - generate
    require:
      - test_coverage
  
  'docs/**/*':
    allow:
      - suggest
      - modify
      - generate
    require:
      - human_review
      - spell_check
  
  '.github/**/*':
    allow:
      - suggest
    require:
      - human_review
```

## Docs Protection Policy

The docs protection policy demonstrates how to create a more restrictive policy that completely prevents changes to the documentation folder:

```yaml
name: "ARIA Docs Protection Policy"
description: "Prevents changes to the docs folder"
version: "1.0"
model: "guardian"

defaults:
  allow: ["suggest", "review"]  # Allow suggestions and reviews by default
  require:
    - human_review

paths:
  'docs/**/*':
    allow: []  # No actions allowed on docs folder
    effect: "deny"
    require:
      - human_review
      - approval_by_docs_team
```

## Testing the Policies

You can validate these policies using the ARIA CLI:

```bash
# Validate the main policy
ariacli policy validate aria_policy.yml

# Validate the docs protection policy
ariacli policy validate docs_protection_policy.yml
```

## Using the Policies with AI Tools

When working with AI tools on the ARIA codebase:

1. The main policy allows AI to suggest and generate code in the core modules, with human review
2. The docs protection policy prevents any AI modifications to documentation without explicit approval

## Testing with IDE Rules

ARIA provides a tool to convert ARIA policies to various IDE rule formats, which can be used for immediate integration:

```bash
# Convert an ARIA policy to Windsurf rules
python -m aria.tools.policy_to_iderules aria_policy.yml

# Convert an ARIA policy to Cursor rules
python -m aria.tools.policy_to_iderules aria_policy.yml -i cursor
```

This creates rule files that IDEs like Windsurf and Cursor will automatically use to enforce your policy. The tool preserves existing content in rules files and only updates the ARIA policy section.

For more information, see [Using IDE Rules for ARIA Policies](tool-integration/ide-rules.md).

## Benefits of Self-Testing

Using ARIA on itself provides several benefits:

1. **Dogfooding**: We use our own product, experiencing it as users would
2. **Practical Example**: Demonstrates real-world application of the framework
3. **Validation**: Confirms that the policy system works as expected
4. **Documentation**: Provides a concrete example for users to follow

## Next Steps

After testing these policies, you might want to:

1. Create more specialized policies for different parts of the codebase
2. Integrate the policies with your CI/CD pipeline
3. Develop custom validation rules specific to your project needs
