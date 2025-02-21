"""
Policy validation for ARIA.

This module provides validation functionality for ARIA policies, ensuring that
policies meet the required format and constraints before being applied.
It includes validation for both policy statements and path-specific rules.

Classes:
    PolicyValidator: Main validator class for ARIA policies
    ValidationResult: Container for validation results

Example:
    >>> from aria.core.validator import PolicyValidator
    >>> validator = PolicyValidator()
    >>> result = validator.validate_policy(policy)
    >>> if result.valid:
    ...     print("Policy is valid!")
    ... else:
    ...     print(f"Validation errors: {result.errors}")
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union, Final
import yaml
from pydantic import ValidationError

from aria.core.policy import AIAction, PolicyModel
from aria.logger import get_logger

logger = get_logger(__name__)

class ValidationResult:
    """Represents a policy validation result.
    
    Stores the outcome of policy validation including any errors encountered
    and provides methods to check validation status.
    
    Attributes:
        valid: Whether validation passed
        errors: List of validation errors
        warnings: List of validation warnings
    """
    def __init__(self) -> None:
        """Initialize validation result."""
        self.valid: bool = True
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def add_error(self, message: str) -> None:
        """Add an error message.
        
        Args:
            message: Error message to add
        """
        self.valid = False
        self.errors.append(message)
    
    def add_warning(self, message: str) -> None:
        """Add a warning message.
        
        Args:
            message: Warning message to add
        """
        self.warnings.append(message)
    
    def as_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary.
        
        Returns:
            Dictionary containing validation results
        """
        return {
            "valid": self.valid,
            "errors": self.errors,
            "warnings": self.warnings
        }

class PolicyValidator:
    """Validates AI participation policies.
    
    Validates policy configuration including statements, path policies,
    and model-specific constraints. Ensures policies are well-formed
    and meet all requirements before being applied.
    
    Attributes:
        REQUIRED_FIELDS: Set of required fields in policy
        OPTIONAL_FIELDS: Set of optional fields in policy
        MODEL_REQUIREMENTS: Valid requirements for each model
        MODEL_ACTIONS: Valid actions for each model
    """
    
    REQUIRED_FIELDS: Final[List[str]] = ["version", "model"]
    OPTIONAL_FIELDS: Final[List[str]] = ["defaults", "paths"]
    
    # Valid requirements for each model
    MODEL_REQUIREMENTS: Final[Dict[PolicyModel, Set[str]]] = {
        PolicyModel.GUARDIAN: {"human_review"},
        PolicyModel.OBSERVER: {"human_review"},
        PolicyModel.ASSISTANT: {"human_review", "tests"},
        PolicyModel.COLLABORATOR: {"human_review", "tests", "documentation"},
        PolicyModel.PARTNER: {"tests", "documentation"}
    }
    
    # Valid actions for each model
    MODEL_ACTIONS: Final[Dict[PolicyModel, Set[AIAction]]] = {
        PolicyModel.GUARDIAN: set(),  # No actions allowed
        PolicyModel.OBSERVER: {AIAction.REVIEW},
        PolicyModel.ASSISTANT: {AIAction.SUGGEST, AIAction.REVIEW},
        PolicyModel.COLLABORATOR: {AIAction.GENERATE, AIAction.MODIFY, AIAction.SUGGEST, AIAction.REVIEW},
        PolicyModel.PARTNER: {AIAction.GENERATE, AIAction.MODIFY, AIAction.SUGGEST, AIAction.REVIEW, AIAction.EXECUTE}
    }
    
    def __init__(self) -> None:
        """Initialize policy validator."""
        pass
    
    def validate_file(
        self,
        path: Union[str, Path],
        strict: bool = False
    ) -> ValidationResult:
        """Validate a policy file.
        
        Args:
            path: Path to policy file
            strict: Enable strict validation
            
        Returns:
            Validation result
        """
        path = Path(path)
        if not path.exists():
            result = ValidationResult()
            result.add_error(f"Policy file not found: {path}")
            return result
        
        try:
            policy_data = yaml.safe_load(path.read_text())
            return self.validate_policy(policy_data, strict)
        except yaml.YAMLError as e:
            result = ValidationResult()
            result.add_error(f"Invalid YAML format: {str(e)}")
            return result
        except Exception as e:
            result = ValidationResult()
            result.add_error(f"Validation error: {str(e)}")
            return result
    
    def validate_policy(
        self,
        policy: Dict[str, Any],
        strict: bool = False
    ) -> ValidationResult:
        """Validate policy data.
        
        Performs comprehensive validation of a policy including required fields,
        statement format, and path policies.
        
        Args:
            policy: Policy data dictionary
            strict: Enable strict validation
            
        Returns:
            Validation result containing any errors
            
        Example:
            >>> validator = PolicyValidator()
            >>> result = validator.validate_policy({
            ...     'version': '1.0',
            ...     'model': 'assistant',
            ...     'defaults': {}
            ... })
        """
        result = ValidationResult()
        
        # Check required fields
        for field in self.REQUIRED_FIELDS:
            if field not in policy:
                result.add_error(f"Missing required field: {field}")
        
        if not result.valid:
            return result
        
        # Validate version
        if not isinstance(policy["version"], (str, float)):
            result.add_error("Version must be a string or number")
        
        # Validate model
        try:
            model = PolicyModel(policy["model"])
        except ValueError:
            result.add_error(f"Invalid model: {policy['model']}. Must be one of {[m.value for m in PolicyModel]}")
            return result
        
        # Validate defaults section
        if "defaults" in policy:
            self._validate_rules_section(policy["defaults"], model, "defaults", result)
        
        # Validate paths section
        if "paths" in policy:
            if not isinstance(policy["paths"], dict):
                result.add_error("Paths must be a dictionary")
            else:
                for path, rules in policy["paths"].items():
                    self._validate_rules_section(rules, model, f"path '{path}'", result)
        
        # Strict mode validation
        if strict:
            self._validate_strict(policy, result)
        
        return result
    
    def _validate_rules_section(
        self,
        rules: Dict[str, Any],
        model: PolicyModel,
        section: str,
        result: ValidationResult
    ) -> None:
        """Validate a rules section (defaults or path-specific).
        
        Args:
            rules: Rules dictionary
            model: Policy model
            section: Section name for error messages
            result: Validation result to update
        """
        if not isinstance(rules, dict):
            result.add_error(f"{section} must be a dictionary")
            return
        
        # Validate allowed actions
        if "allow" in rules:
            if not isinstance(rules["allow"], list):
                result.add_error(f"{section} allow must be a list")
            else:
                valid_actions = self.MODEL_ACTIONS[model]
                for action in rules["allow"]:
                    try:
                        action_enum = AIAction(action)
                        if action_enum not in valid_actions:
                            result.add_error(
                                f"Action '{action}' not allowed for model {model.value} in {section}"
                            )
                    except ValueError:
                        result.add_error(
                            f"Invalid action '{action}' in {section}. Must be one of {[a.value for a in AIAction]}"
                        )
        
        # Validate requirements
        if "require" in rules:
            if not isinstance(rules["require"], list):
                result.add_error(f"{section} require must be a list")
            else:
                valid_requirements = self.MODEL_REQUIREMENTS[model]
                for req in rules["require"]:
                    if req not in valid_requirements:
                        result.add_error(
                            f"Requirement '{req}' not valid for model {model.value} in {section}"
                        )
    
    def _validate_strict(self, policy: Dict[str, Any], result: ValidationResult) -> None:
        """Perform strict validation checks.
        
        Args:
            policy: Policy data
            result: Validation result to update
        """
        # Check version format
        from packaging import version
        try:
            version.parse(str(policy["version"]))
        except version.InvalidVersion:
            result.add_warning("Version should follow semantic versioning (e.g., 1.0.0)")
        
        # Check path patterns
        if "paths" in policy:
            for path in policy["paths"]:
                if not path.strip():
                    result.add_warning("Path patterns should not be empty")
                if path.strip() == "**":
                    result.add_warning("Overly broad path pattern '**' should be avoided")
                if not any(c in path for c in ["*", "/"]):
                    result.add_warning(f"Path pattern '{path}' might be too specific")