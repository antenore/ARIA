"""Tests for ARIA CLI."""
import pytest
from click.testing import CliRunner
from pathlib import Path
import yaml

from aria.cli import cli
from aria.core.policy import PolicyModel, PolicyEffect, AIAction

@pytest.fixture
def runner():
    """Create a CLI runner."""
    return CliRunner()

@pytest.fixture
def test_templates_dir(tmp_path):
    """Create a test templates directory with valid templates."""
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    
    # Create base templates
    base_assistant = templates_dir / "base_assistant.yml"
    base_assistant.write_text("""
model: assistant
name: Base Assistant Template
description: Base template for AI assistants
tags: [base, assistant]
statements:
  - effect: allow
    actions: [analyze, modify]
    resources: [/docs/*, /code/*]
""")
    
    base_tool = templates_dir / "base_tool.yml"
    base_tool.write_text("""
model: observer
name: Base Tool Template  
description: Base template for AI tools
tags: [base, tool]
statements:
  - effect: allow
    actions: [analyze]
    resources: [/docs/*]
""")
    
    # Create example templates
    chat = templates_dir / "chat_assistant.yml"
    chat.write_text("""
model: assistant
name: Chat Assistant
description: Template for chat-based AI assistants
tags: [chat, assistant]
statements:
  - effect: allow
    actions: [analyze, generate]
    resources: [/chat/*]
""")
    
    return templates_dir

@pytest.fixture
def sample_policy():
    """Create a sample valid policy."""
    return {
        "version": "1.0",
        "name": "Test Policy",
        "description": "Test policy",
        "model": PolicyModel.ASSISTANT.value,
        "statements": [
            {
                "effect": PolicyEffect.ALLOW.value,
                "actions": [AIAction.ANALYZE.value, AIAction.REVIEW.value],
                "resources": ["*"]
            }
        ],
        "path_policies": []
    }

def test_cli_help(runner):
    """Test CLI help output."""
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'ARIA - AI Participation Manager' in result.output

def test_init_policy(runner, test_templates_dir):
    """Test initializing a new policy."""
    with runner.isolated_filesystem():
        result = runner.invoke(cli, [
            'init',
            '--model', 'assistant',
            '-o', 'test_policy.yml',
            '--templates-dir', str(test_templates_dir)
        ])
        assert result.exit_code == 0
        assert Path('test_policy.yml').exists()
        assert 'Created new policy' in result.output

def test_template_list(runner, test_templates_dir):
    """Test listing templates."""
    result = runner.invoke(cli, [
        'template', 'list',
        '--templates-dir', str(test_templates_dir)
    ])
    assert result.exit_code == 0
    assert 'Available Templates' in result.output
    assert 'Base Assistant' in result.output
    assert 'Base Tool' in result.output
    assert 'Chat Assistant' in result.output

def test_template_apply(runner, test_templates_dir):
    """Test applying a template."""
    with runner.isolated_filesystem():
        result = runner.invoke(cli, [
            'template', 'apply',
            'chat_assistant',
            '--templates-dir', str(test_templates_dir),
            '-o', 'test_policy.yml'
        ])
        assert result.exit_code == 0
        assert Path('test_policy.yml').exists()
        assert 'Created new policy at' in result.output

def test_policy_validate_valid(runner, sample_policy):
    """Test validating a valid policy."""
    with runner.isolated_filesystem():
        # Create a valid policy file
        Path('test_policy.yml').write_text(yaml.safe_dump(sample_policy))
        
        # Validate it
        result = runner.invoke(cli, ['policy', 'validate', 'test_policy.yml'])
        assert result.exit_code == 0
        assert 'Policy is valid' in result.output

def test_policy_validate_invalid(runner):
    """Test validating an invalid policy."""
    with runner.isolated_filesystem():
        # Create an invalid policy file
        Path('invalid.yml').write_text('invalid: yaml: content')
        
        # This should fail with exit code 1
        result = runner.invoke(cli, ['policy', 'validate', 'invalid.yml'], catch_exceptions=False)
        assert result.exit_code == 1
        assert 'Error: ' in result.output

def test_init_policy_error(runner):
    """Test error handling when initializing policy fails."""
    with runner.isolated_filesystem():
        # Try to create policy in a non-existent directory
        result = runner.invoke(cli, [
            'init',
            '--model', 'assistant',
            '-o', 'nonexistent/test_policy.yml'
        ], catch_exceptions=False)
        assert result.exit_code == 1
        assert 'Error: ' in result.output

def test_template_apply_error(runner, test_templates_dir):
    """Test error handling when applying template fails."""
    with runner.isolated_filesystem():
        # Try to apply non-existent template
        result = runner.invoke(cli, [
            'template', 'apply',
            'nonexistent',
            '--templates-dir', str(test_templates_dir),
            '-o', 'test_policy.yml'
        ], catch_exceptions=False)
        assert result.exit_code == 1
        assert 'Error: ' in result.output