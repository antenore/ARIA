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
from typing import List, Set, Dict, Any, Optional, Union, TypeVar, Type, cast, Callable
import fnmatch
import yaml
import os

from pydantic import BaseModel, Field, ValidationError

from aria.logger import get_logger

logger = get_logger(__name__)

T = TypeVar('T', bound='AIPolicy')

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
    ALL = "all"  # Special value representing all actions

    @classmethod
    def all_actions(cls) -> List['AIAction']:
        """Return all actions except the special ALL value."""
        return [action for action in cls if action != cls.ALL]

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
        tags: List of policy tags
        statements: List of global policy statements
        path_policies: List of path-specific policies
    """
    version: str = Field(default="1.0")
    name: str
    description: str
    model: PolicyModel
    tags: List[str] = Field(default_factory=list)
    statements: List[PolicyStatement] = Field(default_factory=list)
    path_policies: List[PathPolicy] = Field(default_factory=list)

    def model_dump(self, **kwargs: Any) -> Dict[str, Any]:
        """Override model_dump to handle enum serialization."""
        data = super().model_dump(**kwargs)
        # Convert enums to their values
        if 'model' in data:
            data['model'] = data['model'].value
        if 'statements' in data:
            for statement in data['statements']:
                if 'effect' in statement:
                    statement['effect'] = statement['effect'].value
                if 'actions' in statement:
                    statement['actions'] = [
                        action.value if isinstance(action, AIAction) else action
                        for action in statement['actions']
                    ]
        if 'path_policies' in data:
            for policy in data['path_policies']:
                if 'statements' in policy:
                    for statement in policy['statements']:
                        if 'effect' in statement:
                            statement['effect'] = statement['effect'].value
                        if 'actions' in statement:
                            statement['actions'] = [
                                action.value if isinstance(action, AIAction) else action
                                for action in statement['actions']
                            ]
        return data

    def to_yaml(self) -> str:
        """Convert policy to YAML string."""
        return yaml.dump(self.model_dump(), default_flow_style=False)

    def to_yaml_file(self, file_path: str) -> None:
        """Save policy to a YAML file.
        
        Args:
            file_path: Path to save the policy to
        """
        with open(file_path, 'w') as f:
            yaml.dump(self.model_dump(), f, default_flow_style=False)

    @classmethod
    def from_yaml(cls, yaml_str: str) -> 'AIPolicy':
        """Create an instance from a YAML string.
        
        Args:
            yaml_str: YAML string to parse
            
        Returns:
            New policy instance
        """
        data = yaml.safe_load(yaml_str)
        if not data:
            raise ValueError("Empty YAML string")
        return cls(**data)

    @classmethod
    def from_yaml_file(cls, file_path: str) -> 'AIPolicy':
        """Load policy from a YAML file.
        
        Args:
            file_path: Path to load policy from
            
        Returns:
            New policy instance
        """
        with open(file_path) as f:
            return cls.from_yaml(f.read())

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

    def evaluate(self, action: AIAction, path: Union[str, Path]) -> PolicyEffect:
        """Evaluate policy for an action and path following AWS IAM principles.
        
        Args:
            action: Action to evaluate
            path: Path to evaluate
            
        Returns:
            PolicyEffect: Final policy effect (DENY by default)
        """
        # Start with model's default permissions
        allowed_by_model = action in self._get_allowed_actions()
        
        # Check path-specific policies first (highest precedence)
        for policy in self.path_policies:
            effect = policy.evaluate(action, path)
            if effect is not None:
                return effect
                
        # Then check global statements (last matching statement wins)
        last_matching_effect = None
        for statement in self.statements:
            if statement.matches_action(action) and statement.matches_resource(str(path)):
                last_matching_effect = statement.effect
                
        if last_matching_effect is not None:
            return last_matching_effect
                
        # If no explicit policy found, use model's default
        return PolicyEffect.ALLOW if allowed_by_model else PolicyEffect.DENY
        
    def get_permissions(self, path: Union[str, Path]) -> Set[AIAction]:
        """Get allowed actions for a path.
        
        Args:
            path: Path to check permissions for
            
        Returns:
            Set of allowed actions
        """
        # Start with model default permissions
        allowed = self._get_allowed_actions()
        
        # Apply policy evaluation for each action
        result = set()
        for action in AIAction.all_actions():
            if self.evaluate(action, path) == PolicyEffect.ALLOW:
                result.add(action)
                
        return result

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
        self.project_path = os.path.abspath(project_path)
        self.policy_file = os.path.join(self.project_path, self.DEFAULT_POLICY_FILE)
    
    def init_project(self, model: PolicyModel = PolicyModel.ASSISTANT) -> AIPolicy:
        """Initialize ARIA in a project.
        
        Creates a new policy file with default settings based on the specified model.
        
        Args:
            model: Default policy model to use
            
        Returns:
            AIPolicy: Created policy
        """
        policy = AIPolicy(
            name="Default Policy",
            description="Default ARIA policy for this project",
            model=model
        )
        self.save_policy(policy)
        return policy
    
    def load_policy(self) -> AIPolicy:
        """Load policy from file.
        
        Returns:
            AIPolicy: Loaded policy
            
        Raises:
            FileNotFoundError: If policy file does not exist
        """
        if not os.path.exists(self.policy_file):
            raise FileNotFoundError(f"Policy file not found: {self.policy_file}")
        
        with open(self.policy_file) as f:
            return AIPolicy.from_yaml(f.read())
    
    def save_policy(self, policy: AIPolicy) -> None:
        """Save policy to file.
        
        Args:
            policy: Policy to save
        """
        policy.to_yaml_file(self.policy_file)
    
    def get_description(self, policy: AIPolicy) -> str:
        """Get a human-readable description of the policy.
        
        Args:
            policy: Policy to describe
            
        Returns:
            str: Policy description
        """
        return f"Policy '{policy.name}': {policy.description}"