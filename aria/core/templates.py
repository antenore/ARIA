"""
Template management for ARIA policies.

This module handles loading and applying policy templates. Templates provide
predefined policy configurations that can be used to quickly set up ARIA
in a project with common settings.

Classes:
    Template: Policy template model
    TemplateManager: Manages loading and applying templates

Example:
    >>> from aria.core.templates import TemplateManager
    >>> manager = TemplateManager()
    >>> templates = manager.list_templates()
    >>> template = manager.get_template("assistant")
    >>> policy = manager.create_policy(template)
"""
from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Dict, Any, Type, TypeVar, Set, cast, Union
import yaml

from pydantic import BaseModel, Field, ValidationError

from aria.core.policy import AIPolicy, PolicyModel
from aria.logger import get_logger

logger = get_logger(__name__)

T = TypeVar('T', bound='Template')

class Template(BaseModel):
    """Policy template model.
    
    A template defines a reusable policy configuration that can be applied
    to create new policies. Templates include metadata like name and description,
    as well as predefined statements and path policies.
    
    Attributes:
        name: Template name
        description: Template description
        model: Policy model this template is for
        tags: List of tags for categorizing templates
        global_statements: List of global policy statements
        path_policies: List of path-specific policies
    """
    name: str
    description: str
    model: PolicyModel
    tags: List[str] = Field(default_factory=list)
    global_statements: List[Dict[str, Any]] = Field(default_factory=list)
    path_policies: List[Dict[str, Any]] = Field(default_factory=list)

    def __hash__(self) -> int:
        """Make Template hashable for set operations.
        
        Returns:
            int: Hash value for the template based on name and model
        """
        return hash((self.name, self.model))

    def __eq__(self, other: object) -> bool:
        """Define equality for Template objects.
        
        Args:
            other: Object to compare with
            
        Returns:
            bool: True if objects have same name and model, False otherwise
        """
        if not isinstance(other, Template):
            return False
        return self.name == other.name and self.model == other.model

    def model_dump(self, **kwargs) -> Dict[str, Any]:
        """Override model_dump to handle enum serialization.
        
        Args:
            **kwargs: Additional arguments passed to parent model_dump
            
        Returns:
            Dict[str, Any]: Dictionary with serialized values where enums are
                converted to their string values
        """
        data = super().model_dump(**kwargs)
        data['model'] = self.model.value
        return data

    @classmethod
    def from_yaml(cls: Type[T], yaml_str: str) -> T:
        """Create template from YAML string.
        
        Args:
            yaml_str: YAML content string
            
        Returns:
            T: Created template instance
            
        Raises:
            ValueError: If YAML content is invalid
        """
        try:
            data = yaml.safe_load(yaml_str)
            return cls.model_validate(data)
        except Exception as e:
            logger.error(f"Failed to parse template YAML: {e}")
            raise ValueError(f"Invalid template YAML: {e}")

class TemplateManager:
    """Manages policy templates.
    
    This class handles loading templates from a directory and creating policies
    from those templates. It supports both default templates shipped with ARIA
    and custom templates provided by users.
    
    Attributes:
        DEFAULT_TEMPLATES_DIR: Default directory containing templates
        templates_dir: Directory to load templates from
    """
    DEFAULT_TEMPLATES_DIR: Path = Path(__file__).parent / "templates"
    
    def __init__(self, templates_dir: Optional[Union[str, Path]] = None) -> None:
        """Initialize template manager.
        
        Args:
            templates_dir: Optional custom templates directory. If not provided,
                uses the default templates directory
        """
        self.templates_dir: Path = Path(templates_dir) if templates_dir else self.DEFAULT_TEMPLATES_DIR
        self._templates: Dict[str, Template] = {}
        self._load_templates()

    def _load_templates(self) -> None:
        """Load templates from directory.
        
        Loads all .yml files from the templates directory and parses them
        as templates. Invalid templates are logged and skipped.
        """
        if not self.templates_dir.exists():
            logger.warning(f"Templates directory not found: {self.templates_dir}")
            return
            
        for file in self.templates_dir.glob("*.yml"):
            try:
                template = Template.from_yaml(file.read_text())
                self._templates[template.name.lower()] = template
                self._templates[file.stem.lower()] = template
            except Exception as e:
                logger.error(f"Failed to load template {file}: {e}")

    def list_templates(self) -> List[Template]:
        """List available templates.
        
        Returns:
            List[Template]: List of unique templates, excluding duplicates
                where a template is available under multiple names
        """
        return list(set(self._templates.values()))

    def get_template(self, name: str) -> Template:
        """Get template by name.
        
        Args:
            name: Template name or filename (case insensitive)
            
        Returns:
            Template: Template instance
            
        Raises:
            ValueError: If template not found
        """
        name = name.lower()
        if name not in self._templates:
            raise ValueError(f"Template not found: {name}")
        return self._templates[name]

    def create_policy(self, template: Template) -> AIPolicy:
        """Create policy from template.
        
        Creates a new policy using the configuration defined in the template,
        including the policy model, statements, and path policies.
        
        Args:
            template: Template to use
            
        Returns:
            AIPolicy: Created policy instance
            
        Raises:
            ValueError: If policy creation fails
        """
        try:
            policy_data = {
                "version": "1.0",
                "name": f"{template.name} Policy",
                "description": template.description,
                "model": template.model.value,  # Convert enum to string
                "statements": template.global_statements,
                "path_policies": template.path_policies
            }
            return AIPolicy.model_validate(policy_data)
        except Exception as e:
            logger.error(f"Failed to create policy from template: {e}")
            raise ValueError(f"Failed to create policy: {e}")