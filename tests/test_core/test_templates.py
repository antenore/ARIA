"""Tests for ARIA template management."""
import os
import pytest
import yaml
from pathlib import Path

from aria.core.policy import AIAction, PolicyEffect, PolicyModel, PolicyStatement, PathPolicy
from aria.core.templates import Template, TemplateManager

@pytest.fixture
def sample_template() -> Template:
    """Sample template for testing."""
    return Template(
        name="Test Template",
        description="A test template for unit testing",
        tags=["test", "example"],
        model=PolicyModel.ASSISTANT,
        statements=[
            PolicyStatement(
                effect=PolicyEffect.DENY,
                actions=[AIAction.EXECUTE],
                resources=["*"]
            )
        ],
        path_policies=[
            PathPolicy(
                pattern="tests/*",
                statements=[
                    PolicyStatement(
                        effect=PolicyEffect.ALLOW,
                        actions=[AIAction.ANALYZE, AIAction.REVIEW],
                        resources=["*.py"]
                    )
                ]
            )
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
        assert len(sample_template.statements) == 1
        assert len(sample_template.path_policies) == 1
    
    def test_default_values(self):
        """Test default values for Template."""
        template = Template(
            name="test",
            description="test",
            model=PolicyModel.OBSERVER
        )
        assert template.tags == []
        assert template.statements == []
        assert template.path_policies == []
    
    def test_from_dict(self):
        """Test creating template from dictionary."""
        data = {
            "name": "Test",
            "description": "Test template",
            "model": PolicyModel.ASSISTANT,
            "tags": ["test"],
            "statements": [
                {
                    "effect": PolicyEffect.ALLOW,
                    "actions": [AIAction.ANALYZE],
                    "resources": ["*"]
                }
            ]
        }
        template = Template.from_dict(data)
        assert template.name == "Test"
        assert template.tags == ["test"]
        assert len(template.statements) == 1
        assert template.statements[0].effect == PolicyEffect.ALLOW

class TestTemplateManager:
    """Tests for TemplateManager class."""
    
    def test_init_creates_directory(self, template_manager, tmp_path):
        """Test that initialization creates templates directory."""
        assert os.path.exists(template_manager.templates_dir)
        assert os.path.isdir(template_manager.templates_dir)
    
    def test_init_creates_default_templates(self, template_manager):
        """Test that initialization creates default templates."""
        templates = template_manager.list_templates()
        assert len(templates) > 0  # Should have at least one template
        
        # Check default template exists
        default = template_manager.get_template("default")
        assert default is not None
        assert default.name == "default"
        assert default.model == PolicyModel.ASSISTANT
    
    def test_list_templates(self, template_manager, sample_template):
        """Test listing templates."""
        # Save a test template
        template_manager.save_template("test", sample_template)
        
        templates = template_manager.list_templates()
        assert len(templates) > 0
        
        # Find our test template
        test_template = next((t for t in templates if t.name == "Test Template"), None)
        assert test_template is not None
        assert test_template.description == "A test template for unit testing"
    
    def test_get_template(self, template_manager, sample_template):
        """Test getting a template."""
        # Save a test template
        template_file = os.path.join(template_manager.templates_dir, "test.yml")
        with open(template_file, "w") as f:
            yaml.dump(sample_template.model_dump(), f)
        
        # Get the template
        template = template_manager.get_template("test")
        assert template is not None
        assert template.name == "Test Template"
        assert template.model == PolicyModel.ASSISTANT
    
    def test_get_template_not_found(self, template_manager):
        """Test getting a non-existent template."""
        template = template_manager.get_template("nonexistent")
        assert template is None