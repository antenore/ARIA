# Configuration API Reference

## Overview

The Configuration API provides interfaces for managing ARIA configuration settings.

## Classes

### Config

```python
class Config:
    """Manages ARIA configuration settings."""
    
    def __init__(self, path: Optional[str] = None):
        """Initialize configuration."""
        
    def load(self) -> Dict:
        """Load configuration from file."""
        
    def save(self) -> None:
        """Save configuration to file."""
        
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
```

### ConfigManager

```python
class ConfigManager:
    """Manages global and local configurations."""
    
    def get_global_config(self) -> Config:
        """Get global configuration."""
        
    def get_local_config(self) -> Config:
        """Get local configuration."""
        
    def merge_configs(self, global_config: Config, local_config: Config) -> Config:
        """Merge global and local configurations."""
```

## Configuration File Format

```yaml
# Global configuration
global:
  default_model: gpt-4
  log_level: info
  templates_dir: ~/.aria/templates

# Local configuration
local:
  model: gpt-3.5-turbo
  max_tokens: 2000
  temperature: 0.7
```

## Usage Examples

```python
# Load configuration
config = Config()
config.load()

# Get specific settings
model = config.get("model", "gpt-4")
temperature = config.get("temperature", 0.7)

# Save changes
config.save()
```

## Best Practices

1. Use environment variables
2. Separate global/local configs
3. Version control configs
4. Document changes

## See Also

- [Policy API](policy.md)
- [Templates API](templates.md)
- [Configuration Guide](../technical/configuration.md)
