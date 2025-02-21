# Configuration System

ARIA's configuration system provides a flexible way to manage AI participation policies and templates.

## Overview

The configuration system handles:
- Policy file locations and naming conventions
- Template directory structure
- Default policy settings
- Validation rules and constraints

## Configuration Files

### Policy Configuration
Policy files use YAML format and follow a specific schema:
```yaml
version: "1.0"
name: "Policy Name"
description: "Policy Description"
model: "assistant"  # One of: guardian, observer, assistant, collaborator, partner
statements:
  - effect: "allow"
    actions: ["analyze", "review"]
    resources: ["*"]
path_policies: []
```

### Template Configuration
Templates are stored in the `templates` directory and follow a similar structure:
```yaml
name: "Template Name"
model: "assistant"
description: "Template Description"
tags: ["tag1", "tag2"]
statements:
  - effect: "allow"
    actions: ["analyze", "review"]
    resources: ["*"]
```

## Configuration API

The configuration system is accessible through the `aria.core.config` module. See the [Configuration API](../api/config.md) for detailed usage.
