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

class Template:
    """Template for policy configuration."""
    
    def __init__(self, name: str, model: PolicyModel, description: str = "", tags: Optional[List[str]] = None,
                 statements: Optional[List[Dict[str, Any]]] = None, path_policies: Optional[List[Dict[str, Any]]] = None):
        """Initialize template.
        
        Args:
            name: Template name
            model: Policy model type
            description: Template description
            tags: Template tags
            statements: Policy statements
            path_policies: Path-specific policies
        """
        self.name: str = name
        self.model: PolicyModel = model
        self.description: str = description
        self.tags: List[str] = tags or []
        self.statements: List[Dict[str, Any]] = statements or []
        self.path_policies: List[Dict[str, Any]] = path_policies or []
        
    @classmethod
    def from_yaml(cls, content: str) -> 'Template':
        """Create template from YAML content."""
        try:
            data = yaml.safe_load(content)
            if not isinstance(data, dict):
                raise ValueError("Template YAML must be a dictionary")
                
            model = PolicyModel(data.get('model', 'assistant'))
            return cls(
                name=data.get('name', ''),
                model=model,
                description=data.get('description', ''),
                tags=data.get('tags', []),
                statements=data.get('statements', []),
                path_policies=data.get('path_policies', [])
            )
        except yaml.YAMLError as e:
            logger.error(f"Failed to parse template YAML: {e}")
            raise ValueError(f"Invalid template YAML: {e}")
            
    def apply(self) -> AIPolicy:
        """Apply template to create a new policy.
        
        Returns:
            AIPolicy: Created policy instance
        """
        return AIPolicy(
            model=self.model,
            name=self.name,
            description=self.description,
            tags=self.tags,
            statements=self.statements,  # Ensure types match expected
            path_policies=self.path_policies  # Ensure types match expected
        )

def load_template(template_path: Union[str, Path]) -> Dict[str, Any]:
    """Load a template from a YAML file.
    
    Args:
        template_path: Path to template file
        
    Returns:
        Dict containing template data
        
    Raises:
        FileNotFoundError: If template file doesn't exist
        yaml.YAMLError: If template is invalid YAML
    """
    path = Path(template_path)
    if not path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")
        
    with path.open() as f:
        return yaml.safe_load(f)

class TemplateManager:
    """Manages policy templates."""
    
    def __init__(self, templates_dir: Optional[str] = None):
        """Initialize template manager.
        
        Args:
            templates_dir: Directory containing templates
        """
        if templates_dir:
            self.templates_dir = Path(templates_dir)
        else:
            self.templates_dir = Path(__file__).parent.parent / 'templates'
            
        if not self.templates_dir.exists():
            self.templates_dir.mkdir(parents=True)
            self._create_base_templates()

    def _create_base_templates(self) -> None:
        """Create base templates if they don't exist."""
        base_assistant = {
            'model': 'assistant',
            'name': 'Base Assistant Template',
            'description': 'Base template for AI assistants',
            'tags': ['base', 'assistant'],
            'statements': [
                {
                    'effect': 'allow',
                    'actions': ['read', 'write'],
                    'resources': ['/docs/*', '/code/*']
                }
            ]
        }
        
        base_tool = {
            'model': 'tool',
            'name': 'Base Tool Template',
            'description': 'Base template for AI tools',
            'tags': ['base', 'tool'],
            'statements': [
                {
                    'effect': 'allow',
                    'actions': ['read'],
                    'resources': ['/docs/*']
                }
            ]
        }
        
        (self.templates_dir / 'base_assistant.yml').write_text(yaml.safe_dump(base_assistant))
        (self.templates_dir / 'base_tool.yml').write_text(yaml.safe_dump(base_tool))

    def get_template(self, name: str) -> Template:
        """Get a template by name.
        
        Args:
            name: Template name
            
        Returns:
            Template: Found template
            
        Raises:
            ValueError: If template not found
        """
        template_path = self.templates_dir / f"{name}.yml"
        if not template_path.exists():
            raise ValueError(f"Template not found: {name}")
            
        return Template.from_yaml(template_path.read_text())

    def list_templates(self) -> List[Template]:
        """List all available templates.
        
        Returns:
            List[Template]: List of available templates
        """
        if not self.templates_dir.exists():
            return []
            
        templates = []
        for path in self.templates_dir.glob('*.yml'):
            try:
                template = Template.from_yaml(path.read_text())
                templates.append(template)
            except Exception as e:
                logger.warning(f"Failed to load template {path}: {e}")
                
        return sorted(templates, key=lambda t: t.name)

    def create_policy(self, template: Template) -> AIPolicy:
        """Create a policy from a template.
        
        Args:
            template: Template to use
            
        Returns:
            AIPolicy: Created policy
        """
        policy_data = {
            "name": f"{template.name} Policy",
            "description": template.description,
            "model": template.model.value,
            "tags": template.tags,
            "statements": template.statements,
            "path_policies": template.path_policies
        }
        return AIPolicy.model_validate(policy_data)