"""
Policy models for ARIA.

This module defines the core policy models used by ARIA to manage AI participation.
It provides classes and utilities for defining, loading, and evaluating AI participation
policies in a project.

Classes:
    AIAction: Possible actions an AI can take on code
    PolicyEffect: Effect of a policy statement (allow/deny)
    PolicyModel: Available policy models for AI participation
    PolicyStatement: Individual policy statement with AWS-style structure
    PathPolicy: Policy for a specific path pattern
    AIPolicy: AI participation policy
    PolicyManager: Manages AI participation policies for a project

Example:
    >>> from aria.core.policy import AIPolicy, PolicyModel
    >>> policy = AIPolicy(
    ...     name="My Policy",
    ...     description="Example policy",
    ...     model=PolicyModel.ASSISTANT
    ... )
    >>> policy.validate_model()
    True
"""

from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import List, Set, Dict, Any, Optional, Union, TypeVar, Type, cast
import fnmatch
import yaml

from pydantic import BaseModel, Field, ValidationError

from aria.logger import get_logger

logger = get_logger(__name__)

T = TypeVar('T', bound='BaseModel')

class AIAction(str, Enum):
    """Possible actions an AI can take on code.
    
    This enum defines the set of actions that an AI can perform on code within
    the scope of a policy. Each action represents a specific type of interaction
    with the codebase.
    
    Attributes:
        ANALYZE: Read and analyze code without modification
        REVIEW: Review code and provide feedback
        SUGGEST: Suggest code changes without implementing them
        GENERATE: Generate new code
        MODIFY: Modify existing code
        EXECUTE: Execute code or commands
    """
    ANALYZE = "analyze"  # Read and analyze code
    REVIEW = "review"   # Review code and provide feedback
    SUGGEST = "suggest" # Suggest code changes
    GENERATE = "generate" # Generate new code
    MODIFY = "modify"   # Modify existing code
    EXECUTE = "execute" # Execute code or commands

class PolicyEffect(str, Enum):
    """Effect of a policy statement.
    
    This enum defines whether a policy statement allows or denies an action.
    Similar to AWS IAM policy effects.
    
    Attributes:
        ALLOW: Allow the action
        DENY: Deny the action
    """
    ALLOW = "allow"
    DENY = "deny"

class PolicyModel(str, Enum):
    """Available policy models for AI participation.
    
    This enum defines the predefined policy models that determine the overall
    behavior and permissions of the AI assistant.
    
    Attributes:
        GUARDIAN: Most restrictive, can only analyze and review
        OBSERVER: Can only analyze code
        ASSISTANT: Can analyze, review, and suggest changes
        COLLABORATOR: Can analyze, review, suggest, and generate code
        PARTNER: Most permissive, can perform all actions
    """
    GUARDIAN = "guardian"
    OBSERVER = "observer"
    ASSISTANT = "assistant"
    COLLABORATOR = "collaborator"
    PARTNER = "partner"

# Add YAML representers for enums
def _enum_representer(dumper: yaml.Dumper, data: Enum) -> yaml.ScalarNode:
    """Custom YAML representer for Enum values."""
    return dumper.represent_scalar('tag:yaml.org,2002:str', str(data.value))

yaml.add_representer(AIAction, _enum_representer)
yaml.add_representer(PolicyEffect, _enum_representer)
yaml.add_representer(PolicyModel, _enum_representer)

class PolicyStatement(BaseModel):
    """Individual policy statement with AWS-style structure.
    
    A policy statement defines permissions for specific actions on resources.
    Similar to AWS IAM policy statements.
    
    Attributes:
        effect: Whether to allow or deny the actions
        actions: List of actions this statement applies to
        resources: List of resource patterns this statement applies to
        conditions: Optional conditions for when this statement applies
    """
    effect: PolicyEffect
    actions: List[AIAction]
    resources: List[str]
    conditions: Optional[Dict[str, Any]] = None

    def matches_action(self, action: AIAction) -> bool:
        """Check if this statement matches an action.
        
        Args:
            action: Action to check
            
        Returns:
            bool: True if action matches, False otherwise
        """
        return action in self.actions

    def matches_resource(self, resource: str) -> bool:
        """Check if this statement matches a resource.
        
        Args:
            resource: Resource path to check
            
        Returns:
            bool: True if resource matches any pattern, False otherwise
        """
        for pattern in self.resources:
            if fnmatch.fnmatch(str(resource), pattern):
                return True
        return False

class PathPolicy(BaseModel):
    """Policy for a specific path pattern.
    
    Defines policy statements that apply to files matching a specific path pattern.
    
    Attributes:
        pattern: Path pattern this policy applies to
        statements: List of policy statements for this path
    """
    pattern: str
    statements: List[PolicyStatement]

    def matches_path(self, path: Union[str, Path]) -> bool:
        """Check if this policy matches a path.
        
        Args:
            path: Path to check
            
        Returns:
            bool: True if path matches pattern, False otherwise
        """
        return fnmatch.fnmatch(str(path), self.pattern)

    def evaluate(self, action: AIAction, path: Union[str, Path]) -> Optional[PolicyEffect]:
        """Evaluate this policy for an action and path.
        
        Args:
            action: Action to evaluate
            path: Path to evaluate
            
        Returns:
            Optional[PolicyEffect]: PolicyEffect if a matching statement is found,
                None otherwise
        """
        if not self.matches_path(path):
            return None
            
        for statement in self.statements:
            if statement.matches_action(action) and statement.matches_resource(str(path)):
                return statement.effect
        return None

class AIPolicy(BaseModel):
    """AI participation policy.
    
    Defines the overall policy for AI participation in a project, including
    global statements and path-specific policies.
    
    Attributes:
        version: Policy version string
        name: Policy name
        description: Policy description
        model: Policy model determining overall behavior
        statements: List of global policy statements
        path_policies: List of path-specific policies
    """
    version: str = Field(default="1.0")
    name: str
    description: str
    model: PolicyModel
    statements: List[PolicyStatement] = Field(default_factory=list)
    path_policies: List[PathPolicy] = Field(default_factory=list)

    def model_dump(self, **kwargs: Any) -> Dict[str, Any]:
        """Override model_dump to handle enum serialization."""
        data = super().model_dump(**kwargs)
        data['model'] = self.model.value
        
        # Convert enums in statements
        for statement in data['statements']:
            statement['effect'] = statement['effect'].value
            statement['actions'] = [action.value for action in statement['actions']]
            
        # Convert enums in path policies
        for policy in data['path_policies']:
            for statement in policy['statements']:
                statement['effect'] = statement['effect'].value
                statement['actions'] = [action.value for action in statement['actions']]
                
        return data

    @classmethod
    def from_yaml(cls: Type[T], yaml_str: str) -> T:
        """Create an instance from a YAML string.
        
        Args:
            yaml_str: YAML string to parse
            
        Returns:
            T: Created policy instance
            
        Raises:
            ValueError: If YAML is invalid
        """
        data = yaml.safe_load(yaml_str)
        if not isinstance(data, dict):
            raise ValueError("YAML must contain a dictionary")
        return cls(**data)

    @classmethod
    def from_yaml_file(cls: Type[T], path: Union[str, Path]) -> T:
        """Create policy from YAML file.
        
        Args:
            path: Path to YAML file
            
        Returns:
            T: Created policy instance
            
        Raises:
            FileNotFoundError: If file does not exist
            ValidationError: If file content is invalid
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Policy file not found: {path}")
            
        return cls.from_yaml(path.read_text())

    @classmethod
    def validate_data(cls, value: Any) -> 'AIPolicy':
        """Validate the policy configuration data.
        
        Args:
            value: Data to validate
            
        Returns:
            AIPolicy: Validated policy instance
            
        Raises:
            ValueError: If validation fails
        """
        if isinstance(value, dict):
            return cls(**value)
        elif isinstance(value, cls):
            return value
        raise ValueError(f"Cannot validate {type(value)} as {cls.__name__}")

    def validate_model(self) -> bool:
        """Validate policy configuration against model constraints."""
        try:
            allowed_actions = self._get_allowed_actions()
            for statement in self.statements:
                for action in statement.actions:
                    if action not in allowed_actions:
                        logger.error(f"Action {action} not allowed in {self.model} model")
                        return False
            return True
        except Exception as e:
            logger.error(f"Policy validation failed: {e}")
            return False

    def _get_allowed_actions(self) -> Set[AIAction]:
        """Get allowed actions based on policy model."""
        if self.model == PolicyModel.GUARDIAN:
            return {AIAction.ANALYZE, AIAction.REVIEW}
        elif self.model == PolicyModel.OBSERVER:
            return {AIAction.ANALYZE}
        elif self.model == PolicyModel.ASSISTANT:
            return {AIAction.ANALYZE, AIAction.REVIEW, AIAction.SUGGEST}
        elif self.model == PolicyModel.COLLABORATOR:
            return {AIAction.ANALYZE, AIAction.REVIEW, AIAction.SUGGEST, AIAction.GENERATE}
        elif self.model == PolicyModel.PARTNER:
            return {AIAction.ANALYZE, AIAction.REVIEW, AIAction.SUGGEST, AIAction.GENERATE, AIAction.MODIFY, AIAction.EXECUTE}
        else:
            raise ValueError(f"Unknown policy model: {self.model}")

    def to_yaml(self) -> str:
        """Convert policy to YAML string.
        
        Returns:
            str: YAML representation of policy
        """
        return yaml.safe_dump(self.model_dump(), sort_keys=False)

    def save(self, path: Union[str, Path]) -> None:
        """Save policy to YAML file.
        
        Args:
            path: Path to save to
        """
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.to_yaml())

    def evaluate(self, action: AIAction, path: Union[str, Path]) -> PolicyEffect:
        """Evaluate policy for an action and path.
        
        Args:
            action: Action to evaluate
            path: Path to evaluate
            
        Returns:
            PolicyEffect: Final policy effect
        """
        # Check path-specific policies first
        for policy in self.path_policies:
            effect = policy.evaluate(action, path)
            if effect is not None:
                return effect
                
        # Then check global statements
        for statement in self.statements:
            if statement.matches_action(action) and statement.matches_resource(str(path)):
                return statement.effect
                
        # Default deny
        return PolicyEffect.DENY

class PolicyManager:
    """Manages AI participation policies for a project.
    
    This class handles loading, saving, and managing policies for a project.
    It provides methods for initializing new policies and loading existing ones.
    
    Attributes:
        DEFAULT_POLICY_FILE: Default name for policy files
        project_path: Path to project root
        policy_file: Path to policy file
    """
    DEFAULT_POLICY_FILE = "aria-policy.yml"
    
    def __init__(self, project_path: Union[str, Path]) -> None:
        """Initialize policy manager.
        
        Args:
            project_path: Path to project root
        """
        self.project_path: Path = Path(project_path)
        self.policy_file: Path = self.project_path / self.DEFAULT_POLICY_FILE
        self._policy: Optional[AIPolicy] = None

    def init_project(self, model: PolicyModel = PolicyModel.ASSISTANT) -> AIPolicy:
        """Initialize ARIA in a project.
        
        Creates a new policy file with default settings based on the specified model.
        
        Args:
            model: Default policy model to use
            
        Returns:
            AIPolicy: Created policy
        """
        policy = AIPolicy(
            name=f"{model.value.title()} Policy",
            description=f"Default {model.value} policy for ARIA",
            model=model
        )
        self._save_policy(policy)
        return policy

    def load_policy(self) -> AIPolicy:
        """Load policy from file.
        
        Returns:
            AIPolicy: Loaded policy
            
        Raises:
            FileNotFoundError: If policy file does not exist
        """
        if not self.policy_file.exists():
            raise FileNotFoundError(f"Policy file not found: {self.policy_file}")
            
        self._policy = AIPolicy.from_yaml_file(self.policy_file)
        return self._policy

    def _save_policy(self, policy: AIPolicy) -> None:
        """Save policy to file.
        
        Args:
            policy: Policy to save
        """
        policy.save(self.policy_file)
        self._policy = policy