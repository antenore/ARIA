"""
Unit tests for ARIA policy management.

Tests the core policy functionality including loading, saving, and applying AI policies.
"""
import json
from pathlib import Path
import pytest
import yaml

from aria.core.policy import AICapability, AIPolicy, PolicyManager

@pytest.fixture
def sample_policy_dict():
    """Sample policy data for testing."""
    return {
        "version": "1.0",
        "name": "Test Policy",
        "description": "A test policy for unit testing",
        "capabilities": [
            {
                "name": "code_generation",
                "description": "Generate code based on requirements",
                "allowed": True,
                "conditions": ["Must include tests", "Must follow style guide"]
            },
            {
                "name": "data_access",
                "description": "Access sensitive data",
                "allowed": False,
                "conditions": []
            }
        ],
        "restrictions": [
            "No external API calls",
            "No system modifications"
        ]
    }

@pytest.fixture
def sample_policy(sample_policy_dict):
    """Create a sample AIPolicy instance."""
    return AIPolicy(**sample_policy_dict)

@pytest.fixture
def temp_project_dir(tmp_path):
    """Create a temporary project directory."""
    return tmp_path

@pytest.fixture
def policy_manager(temp_project_dir):
    """Create a PolicyManager instance."""
    return PolicyManager(temp_project_dir)

class TestAICapability:
    """Tests for AICapability model."""
    
    def test_create_capability(self):
        """Test creating an AICapability instance."""
        cap = AICapability(
            name="test_cap",
            description="Test capability",
            allowed=True,
            conditions=["condition1", "condition2"]
        )
        assert cap.name == "test_cap"
        assert cap.description == "Test capability"
        assert cap.allowed is True
        assert cap.conditions == ["condition1", "condition2"]
    
    def test_default_values(self):
        """Test default values for AICapability."""
        cap = AICapability(name="test", description="test")
        assert cap.allowed is True
        assert cap.conditions == []

class TestAIPolicy:
    """Tests for AIPolicy model."""
    
    def test_create_policy(self, sample_policy_dict):
        """Test creating an AIPolicy instance."""
        policy = AIPolicy(**sample_policy_dict)
        assert policy.version == "1.0"
        assert policy.name == "Test Policy"
        assert len(policy.capabilities) == 2
        assert len(policy.restrictions) == 2
    
    def test_default_values(self):
        """Test default values for AIPolicy."""
        policy = AIPolicy(name="test", description="test")
        assert policy.version == "1.0"
        assert policy.capabilities == []
        assert policy.restrictions == []
    
    def test_capability_validation(self):
        """Test capability validation in policy."""
        with pytest.raises(ValueError):
            AIPolicy(
                name="test",
                description="test",
                capabilities=[{"invalid": "data"}]
            )

class TestPolicyManager:
    """Tests for PolicyManager class."""
    
    def test_init_project(self, policy_manager, sample_policy_dict, mocker):
        """Test project initialization."""
        # Mock template manager
        mock_template_manager = mocker.Mock()
        mock_template_manager.get_template.return_value = sample_policy_dict
        mocker.patch("aria.core.policy.TemplateManager", return_value=mock_template_manager)
        
        policy_manager.init_project()
        
        assert policy_manager.policy_file.exists()
        loaded_policy = yaml.safe_load(policy_manager.policy_file.read_text())
        assert loaded_policy["name"] == sample_policy_dict["name"]
    
    def test_init_project_existing_file(self, policy_manager):
        """Test initialization with existing policy file."""
        policy_manager.policy_file.touch()
        with pytest.raises(ValueError, match="Policy file already exists"):
            policy_manager.init_project()
    
    def test_load_policy(self, policy_manager, sample_policy_dict):
        """Test loading policy from file."""
        policy_manager.policy_file.write_text(yaml.safe_dump(sample_policy_dict))
        
        policy = policy_manager.load_policy()
        assert isinstance(policy, AIPolicy)
        assert policy.name == sample_policy_dict["name"]
        assert len(policy.capabilities) == len(sample_policy_dict["capabilities"])
    
    def test_load_policy_not_found(self, policy_manager):
        """Test loading non-existent policy."""
        with pytest.raises(FileNotFoundError):
            policy_manager.load_policy()
    
    def test_save_policy(self, policy_manager, sample_policy):
        """Test saving policy to file."""
        policy_manager._policy = sample_policy
        policy_manager.save_policy()
        
        assert policy_manager.policy_file.exists()
        loaded_data = yaml.safe_load(policy_manager.policy_file.read_text())
        assert loaded_data["name"] == sample_policy.name
    
    def test_save_policy_no_policy(self, policy_manager):
        """Test saving when no policy is loaded."""
        with pytest.raises(ValueError, match="No policy loaded"):
            policy_manager.save_policy()
    
    def test_get_description_text(self, policy_manager, sample_policy):
        """Test getting policy description in text format."""
        policy_manager._policy = sample_policy
        desc = policy_manager.get_description()
        
        assert sample_policy.name in desc
        assert sample_policy.version in desc
        assert "✓ Allowed" in desc
        assert "✗ Denied" in desc
    
    def test_get_description_json(self, policy_manager, sample_policy):
        """Test getting policy description in JSON format."""
        policy_manager._policy = sample_policy
        desc = policy_manager.get_description(format="json")
        
        data = json.loads(desc)
        assert data["name"] == sample_policy.name
        assert len(data["capabilities"]) == len(sample_policy.capabilities)
    
    def test_get_description_yaml(self, policy_manager, sample_policy):
        """Test getting policy description in YAML format."""
        policy_manager._policy = sample_policy
        desc = policy_manager.get_description(format="yaml")
        
        data = yaml.safe_load(desc)
        assert data["name"] == sample_policy.name
        assert len(data["capabilities"]) == len(sample_policy.capabilities)
    
    def test_check_compliance(self, policy_manager, sample_policy, tmp_path):
        """Test compliance checking."""
        policy_manager._policy = sample_policy
        test_file = tmp_path / "test.py"
        test_file.touch()
        
        results = policy_manager.check_compliance([str(test_file)])
        assert results["compliant"] is True
        assert str(test_file) in results["checked_files"]
    
    def test_check_compliance_missing_file(self, policy_manager, sample_policy):
        """Test compliance checking with missing file."""
        policy_manager._policy = sample_policy
        results = policy_manager.check_compliance(["nonexistent.py"])
        assert "Path not found" in results["warnings"][0]