"""Tests for ARIA template management."""
import pytest
import yaml
from pathlib import Path

from aria.core.policy import AIAction, PolicyEffect, PolicyModel
from aria.core.templates import Template, TemplateManager

@pytest.fixture
def sample_template() -> Template:
    """Sample template for testing."""
    return Template(
        name="Test Template",
        description="A test template for unit testing",
        tags=["test", "example"],
        model=PolicyModel.ASSISTANT,
        global_statements=[
            {
                "effect": PolicyEffect.DENY,
                "actions": [AIAction.EXECUTE],
                "resources": ["*"]
            }
        ],
        path_policies=[
            {
                "pattern": "tests/*",
                "statements": [
                    {
                        "effect": PolicyEffect.ALLOW,
                        "actions": [AIAction.ANALYZE, AIAction.REVIEW],
                        "resources": ["*.py"]
                    }
                ]
            }
        ]
    )

@pytest.fixture
def template_manager(tmp_path) -> TemplateManager:
    """Create a TemplateManager instance with temp directory."""
    return TemplateManager(templates_dir=str(tmp_path))

class TestTemplate:
    """Tests for Template model."""
    
    def test_create_template(self, sample_template):
        """Test creating a Template instance."""
        assert sample_template.name == "Test Template"
        assert sample_template.description == "A test template for unit testing"
        assert sample_template.tags == ["test", "example"]
        assert sample_template.model == PolicyModel.ASSISTANT
        assert len(sample_template.global_statements) == 1
        assert len(sample_template.path_policies) == 1
    
    def test_default_values(self):
        """Test default values for Template."""
        template = Template(
            name="test",
            description="test",
            model=PolicyModel.OBSERVER
        )
        assert template.tags == []
        assert template.global_statements == []
        assert template.path_policies == []

class TestTemplateManager:
    """Tests for TemplateManager class."""
    
    def test_init_creates_directory(self, template_manager):
        """Test that initialization creates templates directory."""
        assert template_manager.templates_dir.exists()
        assert template_manager.templates_dir.is_dir()
    
    def test_init_creates_default_templates(self, template_manager):
        """Test that initialization creates default templates."""
        for name in TemplateManager.DEFAULT_TEMPLATES:
            template_path = template_manager.templates_dir / f"{name}.yml"
            assert template_path.exists()
            content = yaml.safe_load(template_path.read_text())
            assert content == TemplateManager.DEFAULT_TEMPLATES[name]
    
    def test_list_templates(self, template_manager):
        """Test listing default templates."""
        templates = template_manager.list_templates()
        assert len(templates) == len(TemplateManager.DEFAULT_TEMPLATES)
        template_names = {t.name for t in templates}
        expected_names = {t["name"] for t in TemplateManager.DEFAULT_TEMPLATES.values()}
        assert template_names == expected_names
    
    def test_get_template_default(self, template_manager):
        """Test getting default template."""
        template = template_manager.get_template("default")
        assert template.name == "Default Policy"
        assert template.model == PolicyModel.ASSISTANT
        assert len(template.global_statements) == 1
        assert template.global_statements[0]["effect"] == PolicyEffect.DENY
        assert template.global_statements[0]["actions"] == [AIAction.EXECUTE]
    
    def test_get_template_strict(self, template_manager):
        """Test getting strict template."""
        template = template_manager.get_template("strict")
        assert template.name == "Strict Policy"
        assert template.model == PolicyModel.GUARDIAN
        assert len(template.path_policies) == 1
        assert template.path_policies[0]["pattern"] == "tests/*"
    
    def test_get_template_not_found(self, template_manager):
        """Test getting non-existent template."""
        with pytest.raises(ValueError, match="Template not found"):
            template_manager.get_template("nonexistent")
    
    def test_save_template(self, template_manager, sample_template):
        """Test saving a template."""
        template_manager.save_template(sample_template)
        
        template_path = template_manager.templates_dir / f"{sample_template.name}.yml"
        assert template_path.exists()
        
        loaded = yaml.safe_load(template_path.read_text())
        assert loaded["name"] == sample_template.name
        assert loaded["model"] == sample_template.model
        assert loaded["global_statements"] == sample_template.global_statements
        assert loaded["path_policies"] == sample_template.path_policies
    
    def test_create_policy(self, template_manager):
        """Test creating policy from template."""
        template = template_manager.get_template("default")
        policy = template_manager.create_policy(template)
        
        assert policy.name == template.name
        assert policy.description == template.description
        assert policy.model == template.model
        assert len(policy.statements) == len(template.global_statements)
        assert len(policy.path_policies) == len(template.path_policies)
    
    def test_create_policy_with_path_policies(self, template_manager):
        """Test creating policy from template with path policies."""
        template = template_manager.get_template("strict")
        policy = template_manager.create_policy(template)
        
        assert policy.model == PolicyModel.GUARDIAN
        assert len(policy.path_policies) == 1
        assert policy.path_policies[0].pattern == "tests/*"
        assert len(policy.path_policies[0].statements) == 1
        assert policy.path_policies[0].statements[0].actions == [AIAction.ANALYZE, AIAction.REVIEW]