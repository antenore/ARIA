"""Test configuration for ARIA."""
import pytest
from pathlib import Path
import yaml

from aria.core.policy import AIAction, PolicyModel, PolicyEffect

@pytest.fixture
def test_templates_dir(tmp_path):
    """Create a temporary templates directory with test templates."""
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    
    # Create test templates
    templates = {
        "assistant": {
            "name": "Assistant",
            "description": "Suggestions and review template",
            "model": PolicyModel.ASSISTANT.value,
            "global_statements": [
                {
                    "effect": PolicyEffect.ALLOW.value,
                    "actions": [AIAction.ANALYZE.value, AIAction.REVIEW.value],
                    "resources": ["*"]
                }
            ]
        },
        "guardian": {
            "name": "Guardian",
            "description": "Maximum restriction template",
            "model": PolicyModel.GUARDIAN.value,
            "global_statements": [
                {
                    "effect": PolicyEffect.ALLOW.value,
                    "actions": [AIAction.ANALYZE.value],
                    "resources": ["*"]
                }
            ]
        }
    }
    
    for name, data in templates.items():
        template_file = templates_dir / f"{name}.yml"
        template_file.write_text(yaml.safe_dump(data))
    
    return templates_dir

@pytest.fixture
def sample_policy():
    """Create a sample valid policy."""
    return {
        "name": "Test Policy",
        "description": "Test policy",
        "model": PolicyModel.ASSISTANT.value,
        "statements": [
            {
                "effect": PolicyEffect.ALLOW.value,
                "actions": [AIAction.ANALYZE.value, AIAction.REVIEW.value],
                "resources": ["*"]
            }
        ]
    }