"""
Unit tests for ARIA policy management.

Tests the core policy functionality including loading, saving, and applying AI policies.
"""
import json
from pathlib import Path
import pytest
import yaml
import os

from aria.core.policy import (
    AIPolicy, PolicyManager, PolicyModel,
    PolicyStatement, PathPolicy, PolicyEffect, AIAction
)

@pytest.fixture
def sample_policy_dict():
    """Sample policy data for testing."""
    return {
        "name": "Test Policy",
        "description": "A test policy for unit testing",
        "model": PolicyModel.ASSISTANT,
        "tags": ["test"],
        "statements": [
            {
                "effect": PolicyEffect.ALLOW,
                "actions": [AIAction.ANALYZE, AIAction.REVIEW],
                "resources": ["*"]
            }
        ],
        "path_policies": [
            {
                "pattern": "tests/*",
                "statements": [
                    {
                        "effect": PolicyEffect.ALLOW,
                        "actions": [AIAction.ANALYZE],
                        "resources": ["*.py"]
                    }
                ]
            }
        ]
    }

@pytest.fixture
def sample_policy(sample_policy_dict):
    """Create a sample AIPolicy instance."""
    return AIPolicy.model_validate(sample_policy_dict)

@pytest.fixture
def temp_project_dir(tmp_path):
    """Create a temporary project directory."""
    return tmp_path

@pytest.fixture
def policy_manager(temp_project_dir):
    """Create a PolicyManager instance."""
    return PolicyManager(temp_project_dir)

class TestAIPolicy:
    """Tests for AIPolicy model."""
    
    def test_create_policy(self, sample_policy_dict):
        """Test creating an AIPolicy instance."""
        policy = AIPolicy.model_validate(sample_policy_dict)
        assert policy.name == "Test Policy"
        assert policy.model == PolicyModel.ASSISTANT
        assert len(policy.statements) == 1
        assert len(policy.path_policies) == 1
    
    def test_default_values(self):
        """Test default values for AIPolicy."""
        policy = AIPolicy(
            name="test",
            description="test",
            model=PolicyModel.ASSISTANT
        )
        assert policy.tags == []
        assert policy.statements == []
        assert policy.path_policies == []
    
    def test_policy_validation(self):
        """Test policy validation."""
        with pytest.raises(ValueError):
            AIPolicy(
                name="test",
                description="test",
                model="invalid"
            )

class TestPolicyManager:
    """Tests for PolicyManager class."""
    
    def test_init_project(self, policy_manager, sample_policy_dict):
        """Test project initialization."""
        policy = AIPolicy.model_validate(sample_policy_dict)
        policy_manager.save_policy(policy)
        assert os.path.exists(policy_manager.policy_file)
    
    def test_load_policy(self, policy_manager, sample_policy_dict):
        """Test loading policy from file."""
        # Save policy first
        policy = AIPolicy.model_validate(sample_policy_dict)
        policy_manager.save_policy(policy)
        
        # Load and verify
        loaded = policy_manager.load_policy()
        assert loaded.name == policy.name
        assert loaded.model == policy.model
        assert len(loaded.statements) == len(policy.statements)
        
    def test_load_policy_not_found(self, policy_manager):
        """Test loading non-existent policy."""
        with pytest.raises(FileNotFoundError):
            policy_manager.load_policy()
            
    def test_save_policy(self, policy_manager, sample_policy):
        """Test saving policy to file."""
        policy_manager.save_policy(sample_policy)
        assert os.path.exists(policy_manager.policy_file)
        
        # Verify saved content
        with open(policy_manager.policy_file) as f:
            saved = yaml.safe_load(f)
        assert saved["name"] == sample_policy.name
        assert saved["model"] == sample_policy.model.value
        
    def test_get_description(self, policy_manager, sample_policy):
        """Test getting policy description."""
        desc = policy_manager.get_description(sample_policy)
        assert isinstance(desc, str)
        assert sample_policy.name in desc
        assert sample_policy.description in desc