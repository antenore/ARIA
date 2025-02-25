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

import os
from pathlib import Path
from typing import List, Optional, Dict, Any, Type, TypeVar, Set, cast, Union
import yaml

from pydantic import BaseModel, Field

from aria.core.policy import AIPolicy, PolicyModel, PolicyStatement, PathPolicy, PolicyEffect, AIAction
from aria.logger import get_logger

logger = get_logger(__name__)

T = TypeVar('T', bound='Template')

class Template(BaseModel):
    """Template for policy configuration.
    
    A template defines a pre-configured policy setup that can be applied to
    quickly set up ARIA with common settings. Templates support all policy
    models defined in the ARIA framework.
    
    Attributes:
        name: Template name
        model: Policy model (GUARDIAN, OBSERVER, ASSISTANT, COLLABORATOR, PARTNER)
        description: Template description
        tags: Template tags for categorization
        statements: List of policy statements
        path_policies: List of path-specific policies
    """
    
    name: str
    model: Union[PolicyModel, str]  # Allow string values for flexibility
    description: str = ""
    tags: List[str] = Field(default_factory=list)
    statements: List[PolicyStatement] = Field(default_factory=list)
    path_policies: List[PathPolicy] = Field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Template':
        """Create template from dictionary data.

        Handles conversion of string values to appropriate enums, with proper
        validation and error handling.

        Args:
            data: Template data dictionary

        Returns:
            Template: Created template instance

        Raises:
            ValueError: If required fields are missing or invalid
        """
        # Handle model conversion
        if isinstance(data.get('model'), str):
            try:
                model_str = data['model'].upper()  # Normalize to upper case
                if model_str not in PolicyModel.__members__:
                    raise ValueError(
                        f"Invalid model '{data['model']}'. Must be one of: "
                        f"{', '.join(PolicyModel.__members__.keys())}"
                    )
                data['model'] = PolicyModel[model_str]
            except KeyError as e:
                logger.error(f"Invalid model value: {data['model']}")
                raise ValueError(f"Invalid policy model: {data['model']}") from e

        # Handle statements conversion
        if 'statements' in data and data['statements']:
            processed_statements = []
            for stmt in data['statements']:
                if isinstance(stmt, dict):
                    # Convert effect
                    if isinstance(stmt.get('effect'), str):
                        try:
                            effect_str = stmt['effect'].upper()
                            if effect_str not in PolicyEffect.__members__:
                                raise ValueError(
                                    f"Invalid effect '{stmt['effect']}'. Must be one of: "
                                    f"{', '.join(PolicyEffect.__members__.keys())}"
                                )
                            stmt['effect'] = PolicyEffect[effect_str]
                        except KeyError as e:
                            logger.error(f"Invalid effect value: {stmt['effect']}")
                            raise ValueError(f"Invalid policy effect: {stmt['effect']}") from e

                    # Convert actions
                    if 'actions' in stmt:
                        try:
                            actions = []
                            for action in stmt['actions']:
                                if isinstance(action, str):
                                    action_str = action.upper()
                                    if action_str not in AIAction.__members__:
                                        raise ValueError(
                                            f"Invalid action '{action}'. Must be one of: "
                                            f"{', '.join(AIAction.__members__.keys())}"
                                        )
                                    actions.append(AIAction[action_str])
                                else:
                                    actions.append(action)
                            stmt['actions'] = actions
                        except KeyError as e:
                            logger.error(f"Invalid action value in statement")
                            raise ValueError(f"Invalid action in policy statement") from e

                    processed_statements.append(PolicyStatement(**stmt))
                else:
                    processed_statements.append(stmt)
            data['statements'] = processed_statements

        # Similar conversion for path_policies
        if 'path_policies' in data and data['path_policies']:
            processed_policies = []
            for policy in data['path_policies']:
                if isinstance(policy, dict):
                    if 'statements' in policy:
                        # Process statements for path policy
                        temp_statements = []
                        for stmt in policy['statements']:
                            if isinstance(stmt, dict):
                                # Process effect
                                if isinstance(stmt.get('effect'), str):
                                    try:
                                        effect_str = stmt['effect'].upper()
                                        if effect_str not in PolicyEffect.__members__:
                                            raise ValueError(f"Invalid effect: {stmt['effect']}")
                                        stmt['effect'] = PolicyEffect[effect_str]
                                    except KeyError as e:
                                        logger.error(f"Invalid effect value: {stmt['effect']}")
                                        raise ValueError(f"Invalid effect: {stmt['effect']}") from e
                                        
                                # Process actions
                                if 'actions' in stmt:
                                    try:
                                        actions = []
                                        for action in stmt['actions']:
                                            if isinstance(action, str):
                                                action_str = action.upper()
                                                if action_str not in AIAction.__members__:
                                                    raise ValueError(f"Invalid action: {action}")
                                                actions.append(AIAction[action_str])
                                            else:
                                                actions.append(action)
                                        stmt['actions'] = actions
                                    except KeyError as e:
                                        logger.error(f"Invalid action value in statement")
                                        raise ValueError(f"Invalid action in statement") from e
                                        
                                temp_statements.append(PolicyStatement(**stmt))
                            else:
                                temp_statements.append(stmt)
                        policy['statements'] = temp_statements
                    processed_policies.append(PathPolicy(**policy))
                else:
                    processed_policies.append(policy)
            data['path_policies'] = processed_policies

        # If this is a recursive call to just process statements,
        # handle it differently to avoid validation errors
        if set(data.keys()) == {'statements'}:
            template = cls(
                name="temp",
                model=PolicyModel.ASSISTANT,
                statements=data['statements']
            )
            return template
            
        return cls(**data)

    def model_dump(self, **kwargs: Any) -> Dict[str, Any]:
        """Convert template to dictionary."""
        data = super().model_dump(**kwargs)
        # Convert enums to strings for YAML serialization
        if isinstance(self.model, PolicyModel):
            data['model'] = self.model.value
        if self.statements:
            data['statements'] = [
                {
                    'effect': stmt.effect.value,
                    'actions': [a.value for a in stmt.actions],
                    'resources': stmt.resources,
                    **({"conditions": stmt.conditions} if stmt.conditions else {})
                }
                for stmt in self.statements
            ]
        if self.path_policies:
            data['path_policies'] = [
                {
                    'pattern': pp.pattern,
                    'statements': [
                        {
                            'effect': stmt.effect.value,
                            'actions': [a.value for a in stmt.actions],
                            'resources': stmt.resources,
                            **({"conditions": stmt.conditions} if stmt.conditions else {})
                        }
                        for stmt in pp.statements
                    ]
                }
                for pp in self.path_policies
            ]
        return data

    @classmethod
    def from_yaml(cls, content: str) -> 'Template':
        """Create template from YAML content."""
        try:
            data = yaml.safe_load(content)
            if not isinstance(data, dict):
                raise ValueError("Template YAML must be a dictionary")
                
            # Convert model to enum if it's a string
            if isinstance(data.get('model'), str):
                try:
                    model_upper = data['model'].upper()
                    if model_upper in PolicyModel.__members__:
                        data['model'] = PolicyModel[model_upper]
                    else:
                        data['model'] = PolicyModel(data['model'])
                except ValueError:
                    logger.warning(f"Invalid model value: {data['model']}")
                    
            # Convert statements to proper types
            if 'statements' in data and data['statements']:
                processed_statements = []
                for stmt in data['statements']:
                    if isinstance(stmt, dict):
                        # Convert effect and actions to enums if they're strings
                        if isinstance(stmt.get('effect'), str):
                            try:
                                effect_upper = stmt['effect'].upper()
                                if effect_upper in PolicyEffect.__members__:
                                    stmt['effect'] = PolicyEffect[effect_upper]
                                else:
                                    stmt['effect'] = PolicyEffect(stmt['effect'])
                            except ValueError:
                                logger.warning(f"Invalid effect value: {stmt['effect']}")
                        if 'actions' in stmt:
                            try:
                                actions = []
                                for action in stmt['actions']:
                                    if isinstance(action, str):
                                        action_upper = action.upper()
                                        if action_upper in AIAction.__members__:
                                            actions.append(AIAction[action_upper])
                                        else:
                                            actions.append(AIAction(action))
                                    else:
                                        actions.append(action)
                                stmt['actions'] = actions
                            except ValueError as e:
                                logger.warning(f"Invalid action value: {e}")
                        processed_statements.append(PolicyStatement(**stmt))
                    else:
                        processed_statements.append(stmt)
                data['statements'] = processed_statements
                
            # Convert path policies to proper types
            if 'path_policies' in data and data['path_policies']:
                processed_policies = []
                for policy in data['path_policies']:
                    if isinstance(policy, dict):
                        if 'statements' in policy:
                            processed_statements = []
                            for stmt in policy['statements']:
                                if isinstance(stmt, dict):
                                    if isinstance(stmt.get('effect'), str):
                                        try:
                                            effect_upper = stmt['effect'].upper()
                                            if effect_upper in PolicyEffect.__members__:
                                                stmt['effect'] = PolicyEffect[effect_upper]
                                            else:
                                                stmt['effect'] = PolicyEffect(stmt['effect'])
                                        except ValueError:
                                            logger.warning(f"Invalid effect value: {stmt['effect']}")
                                    if 'actions' in stmt:
                                        try:
                                            actions = []
                                            for action in stmt['actions']:
                                                if isinstance(action, str):
                                                    action_upper = action.upper()
                                                    if action_upper in AIAction.__members__:
                                                        actions.append(AIAction[action_upper])
                                                    else:
                                                        actions.append(AIAction(action))
                                                else:
                                                    actions.append(action)
                                            stmt['actions'] = actions
                                        except ValueError as e:
                                            logger.warning(f"Invalid action value: {e}")
                                    processed_statements.append(PolicyStatement(**stmt))
                                else:
                                    processed_statements.append(stmt)
                            policy['statements'] = processed_statements
                        processed_policies.append(PathPolicy(**policy))
                    else:
                        processed_policies.append(policy)
                data['path_policies'] = processed_policies
                
            return cls.from_dict(data)
        except yaml.YAMLError as e:
            logger.error(f"Failed to parse template YAML: {e}")
            raise ValueError(f"Invalid template YAML: {e}")
            
    def apply(self) -> AIPolicy:
        """Apply template to create a new policy.
        
        Returns:
            AIPolicy: Created policy instance
        """
        # Make sure to convert model to PolicyModel enum if it's a string
        model = self.model
        if isinstance(model, str):
            try:
                model_upper = model.upper()
                if model_upper in PolicyModel.__members__:
                    model = PolicyModel[model_upper]
                else:
                    model = PolicyModel(model)
            except ValueError:
                raise ValueError(f"Invalid policy model: {model}")
        
        return AIPolicy(
            model=model,
            name=self.name,
            description=self.description,
            statements=self.statements,
            path_policies=self.path_policies
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
        data: Dict[str, Any] = yaml.safe_load(f)
        return data

class TemplateManager:
    """Manages policy templates."""
    
    # Default templates with proper enum values
    DEFAULT_TEMPLATES = {
        "default": {
            "name": "default",
            "model": PolicyModel.ASSISTANT,
            "description": "Default policy template with moderate AI permissions",
            "statements": [
                {
                    "effect": PolicyEffect.ALLOW,
                    "actions": [AIAction.ANALYZE, AIAction.REVIEW],
                    "resources": ["*.py"]
                }
            ],
            "path_policies": [
                {
                    "pattern": "docs/**",
                    "statements": [
                        {
                            "effect": PolicyEffect.ALLOW,
                            "actions": [AIAction.GENERATE, AIAction.MODIFY, AIAction.SUGGEST],
                            "resources": ["*"]
                        }
                    ]
                }
            ]
        },
        "strict": {
            "name": "strict",
            "model": PolicyModel.GUARDIAN,
            "description": "Strict policy template with minimal AI permissions",
            "statements": [
                {
                    "effect": PolicyEffect.DENY,
                    "actions": [AIAction.ALL],
                    "resources": ["*"]
                }
            ],
            "path_policies": [
                {
                    "pattern": "tests/**",
                    "statements": [
                        {
                            "effect": PolicyEffect.ALLOW,
                            "actions": [AIAction.SUGGEST],
                            "resources": ["*.py"]
                        }
                    ]
                }
            ]
        }
    }
    
    def __init__(self, templates_dir: Optional[str] = None) -> None:
        """Initialize template manager.
        
        Args:
            templates_dir: Directory containing template files
        """
        # If no templates_dir provided, use the default location in aria/templates
        if templates_dir is None:
            templates_dir = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), 
                "templates"
            )
        
        self.templates_dir = templates_dir
        
        # Create templates directory if it doesn't exist
        os.makedirs(self.templates_dir, exist_ok=True)
        
        # Create default templates if they don't exist
        self._create_base_templates()

    def get_template_path(self, template_name: str) -> str:
        """Get full path to a template file.
        
        Args:
            template_name: Template name
            
        Returns:
            Full path to template file
        """
        # Use os.path.join instead of / operator
        return os.path.join(self.templates_dir, f"{template_name}.yml")

    def _create_base_templates(self) -> None:
        """Create default templates if they don't exist."""
        for template_name, template_data in self.DEFAULT_TEMPLATES.items():
            # Use os.path.join for safe path construction
            template_file = os.path.join(self.templates_dir, f"{template_name}.yml")
            
            if not os.path.exists(template_file):
                try:
                    # Create a copy of template data to avoid modifying the original
                    template_dict = template_data.copy()
                    
                    # Ensure template has a name
                    if "name" not in template_dict:
                        template_dict["name"] = template_name
                    
                    # Use from_dict to properly handle type conversions
                    template = Template.from_dict(template_dict)
                    
                    # Write template to file
                    with open(template_file, "w") as f:
                        yaml.dump(template.model_dump(), f, default_flow_style=False)
                        
                    logger.info(f"Created default template {template_name}")
                except Exception as e:
                    logger.error(f"Failed to create default template {template_name}: {e}")
            else:
                # Load template from file to ensure it's available
                try:
                    with open(template_file, "r") as f:
                        template_data = yaml.safe_load(f)
                    
                    template = Template.from_dict(template_data)
                    logger.info(f"Loaded default template {template_name} from file")
                except Exception as e:
                    logger.error(f"Failed to load template {template_name}: {e}")
    
    def list_templates(self) -> List[Template]:
        """List all available templates.
        
        Returns:
            List of available templates
        """
        templates = []
        
        try:
            # List all .yml files in templates directory
            for filename in os.listdir(self.templates_dir):
                if filename.endswith('.yml'):
                    template_path = os.path.join(self.templates_dir, filename)
                    try:
                        with open(template_path, 'r') as f:
                            data = yaml.safe_load(f)
                            template = Template.from_dict(data)
                            templates.append(template)
                    except Exception as e:
                        logger.warning(f"Failed to load template {filename}: {e}")
                        continue
        except Exception as e:
            logger.error(f"Failed to list templates: {e}")
            
        return templates

    def get_template(self, template_name: str) -> Optional[Template]:
        """Get a template by name.
        
        Args:
            template_name: Template name
            
        Returns:
            Template instance, or None if not found
            
        Raises:
            ValueError: If template file is invalid
        """
        template_file = os.path.join(self.templates_dir, f"{template_name}.yml")
        
        if not os.path.exists(template_file):
            logger.warning(f"Template '{template_name}' not found")
            return None
            
        try:
            with open(template_file, "r") as f:
                template_data = yaml.safe_load(f)
                
            if not template_data:
                raise ValueError(f"Template file {template_name} is empty")
                
            return Template.from_dict(template_data)
        except Exception as e:
            logger.error(f"Failed to load template {template_name}: {e}")
            raise ValueError(f"Invalid template file {template_name}: {e}")

    def save_template(self, name: str, template: Template) -> None:
        """Save a template.
        
        Args:
            name: Template name
            template: Template to save
        """
        template_path = os.path.join(self.templates_dir, f"{name}.yml")
        with open(template_path, 'w') as f:
            yaml.dump(template.model_dump(), f, default_flow_style=False)

    def create_policy(self, template: Template) -> AIPolicy:
        """Create a policy from a template.
        
        Args:
            template: Template to use
            
        Returns:
            AIPolicy: Created policy
        """
        # Make sure to convert model to PolicyModel enum if it's a string
        model = template.model
        if isinstance(model, str):
            try:
                model_upper = model.upper()
                if model_upper in PolicyModel.__members__:
                    model = PolicyModel[model_upper]
                else:
                    model = PolicyModel(model)
            except ValueError:
                raise ValueError(f"Invalid policy model: {model}")
                
        return AIPolicy(
            name=template.name,
            description=template.description,
            model=model,
            statements=template.statements,
            path_policies=template.path_policies
        )