"""
Unit tests for ARIA policy validation.

Tests the validation functionality including policy validation and compliance checking.
"""
import pytest
import yaml
from pathlib import Path
from typing import Dict, Any

from aria.core.validator import ValidationResult, PolicyValidator

@pytest.fixture
def valid_policy() -> Dict[str, Any]:
    """Sample valid policy data for testing."""
    return {
        "version": "1.0.0",
        "name": "Test Policy",
        "description": "A comprehensive test policy for validating the ARIA validation system.",
        "capabilities": [
            {
                "name": "test_capability",
                "description": "A detailed test capability description that meets length requirements.",
                "allowed": True,
                "conditions": ["Must follow all testing guidelines.", "Must document all test cases."]
            }
        ],
        "restrictions": ["No unauthorized testing.", "Must follow security protocols."]
    }

@pytest.fixture
def validator() -> PolicyValidator:
    """Create a PolicyValidator instance."""
    return PolicyValidator()

class TestValidationResult:
    """Tests for ValidationResult class."""
    
    def test_init(self):
        """Test initialization of ValidationResult."""
        result = ValidationResult()
        assert result.valid is True
        assert result.errors == []
        assert result.warnings == []
    
    def test_add_error(self):
        """Test adding an error."""
        result = ValidationResult()
        result.add_error("Test error")
        assert result.valid is False
        assert len(result.errors) == 1
        assert result.errors[0] == "Test error"
    
    def test_add_warning(self):
        """Test adding a warning."""
        result = ValidationResult()
        result.add_warning("Test warning")
        assert result.valid is True  # Warnings don't affect validity
        assert len(result.warnings) == 1
        assert result.warnings[0] == "Test warning"
    
    def test_as_dict(self):
        """Test dictionary conversion."""
        result = ValidationResult()
        result.add_error("Test error")
        result.add_warning("Test warning")
        
        data = result.as_dict()
        assert data["valid"] is False
        assert len(data["errors"]) == 1
        assert len(data["warnings"]) == 1

class TestPolicyValidator:
    """Tests for PolicyValidator class."""
    
    def test_validate_valid_policy(self, validator, valid_policy):
        """Test validating a valid policy."""
        result = validator.validate_policy(valid_policy)
        assert result.valid is True
        assert not result.errors
        assert not result.warnings
    
    def test_validate_missing_required_field(self, validator, valid_policy):
        """Test validation with missing required field."""
        del valid_policy["name"]
        result = validator.validate_policy(valid_policy)
        assert result.valid is False
        assert any("Missing required field: name" in error for error in result.errors)
    
    def test_validate_invalid_version_type(self, validator, valid_policy):
        """Test validation with invalid version type."""
        valid_policy["version"] = 1.0  # Should be string
        result = validator.validate_policy(valid_policy)
        assert result.valid is False
        assert any("Version must be a string" in error for error in result.errors)
    
    def test_validate_invalid_capabilities_type(self, validator, valid_policy):
        """Test validation with invalid capabilities type."""
        valid_policy["capabilities"] = "not a list"
        result = validator.validate_policy(valid_policy)
        assert result.valid is False
        assert any("Capabilities must be a list" in error for error in result.errors)
    
    def test_validate_invalid_capability_format(self, validator, valid_policy):
        """Test validation with invalid capability format."""
        valid_policy["capabilities"] = [{"invalid": "format"}]
        result = validator.validate_policy(valid_policy)
        assert result.valid is False
        assert any("missing required field" in error for error in result.errors)
    
    def test_validate_invalid_conditions_type(self, validator, valid_policy):
        """Test validation with invalid conditions type."""
        valid_policy["capabilities"][0]["conditions"] = "not a list"
        result = validator.validate_policy(valid_policy)
        assert result.valid is False
        assert any("conditions must be a list" in error for error in result.errors)
    
    def test_validate_invalid_restrictions_type(self, validator, valid_policy):
        """Test validation with invalid restrictions type."""
        valid_policy["restrictions"] = "not a list"
        result = validator.validate_policy(valid_policy)
        assert result.valid is False
        assert any("Restrictions must be a list" in error for error in result.errors)
    
    def test_validate_file_not_found(self, validator, tmp_path):
        """Test validation with non-existent file."""
        result = validator.validate_file(tmp_path / "nonexistent.yml")
        assert result.valid is False
        assert any("Policy file not found" in error for error in result.errors)
    
    def test_validate_file_invalid_yaml(self, validator, tmp_path):
        """Test validation with invalid YAML file."""
        test_file = tmp_path / "invalid.yml"
        test_file.write_text("invalid: {")
        
        result = validator.validate_file(test_file)
        assert result.valid is False
        assert any("Invalid YAML format" in error for error in result.errors)
    
    def test_validate_file_valid(self, validator, valid_policy, tmp_path):
        """Test validation with valid file."""
        test_file = tmp_path / "valid.yml"
        test_file.write_text(yaml.safe_dump(valid_policy))
        
        result = validator.validate_file(test_file)
        assert result.valid is True
        assert not result.errors
    
    def test_strict_validation_version(self, validator, valid_policy):
        """Test strict validation of version format."""
        valid_policy["version"] = "invalid"
        result = validator.validate_policy(valid_policy, strict=True)
        assert result.valid is True  # Invalid version format is a warning in strict mode
        assert any("should follow semantic versioning" in warning for warning in result.warnings)
    
    def test_strict_validation_description_length(self, validator, valid_policy):
        """Test strict validation of description length."""
        valid_policy["description"] = "Too short"
        result = validator.validate_policy(valid_policy, strict=True)
        assert result.valid is True  # Short description is a warning in strict mode
        assert any("should be at least 50 characters" in warning for warning in result.warnings)
    
    def test_strict_validation_capability_description(self, validator, valid_policy):
        """Test strict validation of capability description length."""
        valid_policy["capabilities"][0]["description"] = "Too short"
        result = validator.validate_policy(valid_policy, strict=True)
        assert result.valid is True  # Short capability description is a warning
        assert any("should be at least 30 characters" in warning for warning in result.warnings)
    
    def test_strict_validation_condition_format(self, validator, valid_policy):
        """Test strict validation of condition format."""
        valid_policy["capabilities"][0]["conditions"] = ["Invalid format"]
        result = validator.validate_policy(valid_policy, strict=True)
        assert result.valid is True  # Invalid condition format is a warning
        assert any("should end with a period" in warning for warning in result.warnings)