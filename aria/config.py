"""
Configuration management for ARIA.

Handles configuration loading and management for the ARIA framework.

Copyright 2024 ARIA Team

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from pydantic import BaseModel, Field

class AriaConfig(BaseModel):
    """Base configuration model for ARIA."""
    version: str = Field(default="1.0", description="ARIA configuration version")
    policy_file: str = Field(default="aria-policy.yml", description="Default policy file name")
    templates_dir: str = Field(default="templates", description="Directory containing policy templates")
    strict_mode: bool = Field(default=False, description="Enable strict validation mode")
    log_level: str = Field(default="INFO", description="Logging level")
    
    class Config:
        """Pydantic config."""
        validate_assignment = True

class ConfigManager:
    """Manages ARIA configuration loading and saving."""
    
    DEFAULT_CONFIG_FILE = ".aria-config.yml"
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration manager.
        
        Args:
            config_path: Optional path to configuration file
        """
        self.config_path = Path(config_path or self.DEFAULT_CONFIG_FILE)
        self.config = self._load_config()
    
    def _load_config(self) -> AriaConfig:
        """Load configuration from file or create default."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config_data = yaml.safe_load(f)
                return AriaConfig(**config_data)
            except Exception as e:
                raise ValueError(f"Failed to load config from {self.config_path}: {str(e)}")
        return AriaConfig()
    
    def save_config(self) -> None:
        """Save current configuration to file."""
        config_dict = self.config.model_dump()
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump(config_dict, f, default_flow_style=False)
        except Exception as e:
            raise ValueError(f"Failed to save config to {self.config_path}: {str(e)}")
    
    def update_config(self, **kwargs: Any) -> None:
        """Update configuration with new values.
        
        Args:
            **kwargs: Configuration key-value pairs to update
        """
        config_dict = self.config.model_dump()
        config_dict.update(kwargs)
        self.config = AriaConfig(**config_dict)
        self.save_config()
    
    def get_config(self) -> Dict[str, Any]:
        """Get current configuration as dictionary.
        
        Returns:
            Dict containing current configuration
        """
        return self.config.model_dump()
    
    @property
    def policy_file(self) -> Path:
        """Get path to policy file."""
        return Path(self.config.policy_file)
    
    @property
    def templates_dir(self) -> Path:
        """Get path to templates directory."""
        return Path(self.config.templates_dir)
    
    @property
    def strict_mode(self) -> bool:
        """Get strict mode setting."""
        return self.config.strict_mode
    
    @property
    def log_level(self) -> str:
        """Get logging level."""
        return self.config.log_level