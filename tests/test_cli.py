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
    
    # Create default template
    default_template = templates_dir / "default.yml"
    default_template.write_text("""
model: assistant
name: default
description: Default AI policy with basic restrictions and capabilities
statements:
  - effect: deny
    actions: [execute]
    resources: ["*"]
  - effect: allow
    actions: [analyze, review]
    resources: ["*.py"]
path_policies:
  - pattern: docs/**
    statements:
      - effect: allow
        actions: [generate, modify, suggest]
        resources: ["*"]
""")
    
    # Create strict template
    strict_template = templates_dir / "strict.yml"
    strict_template.write_text("""
model: guardian
name: strict
description: Strict policy template with minimal AI permissions
statements:
  - effect: deny
    actions: [all]
    resources: ["*"]
path_policies:
  - pattern: tests/**
    statements:
      - effect: allow
        actions: [suggest]
        resources: ["*.py"]
""")
    
    return templates_dir

@pytest.fixture
def sample_policy():
    """Create a sample valid policy."""
    return {
        "version": "1.0",
        "name": "Test Policy",
        "description": "Test policy for code review and documentation",
        "model": PolicyModel.ASSISTANT.value,
        "statements": [
            {
                "effect": PolicyEffect.ALLOW.value,
                "actions": [AIAction.ANALYZE.value, AIAction.REVIEW.value],
                "resources": ["*.py"]
            }
        ],
        "path_policies": []
    }

def test_cli_help(runner):
    """Test CLI help output."""
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'ARIA - Artificial Intelligence Regulation Interface & Agreements' in result.output

def test_init_policy_with_options(runner, test_templates_dir):
    """Test initializing a new policy with specific options."""
    with runner.isolated_filesystem():
        result = runner.invoke(cli, [
            'init',
            '--model', 'assistant',
            '--name', 'Test Policy',
            '--description', 'A test policy for code review and documentation',
            '-o', 'test_policy.yml',
            '--templates-dir', str(test_templates_dir)
        ])
        assert result.exit_code == 0
        assert Path('test_policy.yml').exists()
        assert 'Created new policy' in result.output

        # Verify policy contents
        with open('test_policy.yml') as f:
            policy = yaml.safe_load(f)
            assert policy['name'] == 'Test Policy'
            assert policy['model'] == 'assistant'
            assert 'code review and documentation' in policy['description'].lower()

def test_init_policy_error(runner, test_templates_dir):
    """Test error handling when initializing policy fails."""
    with runner.isolated_filesystem():
        result = runner.invoke(cli, [
            'init',
            '--model', 'invalid_model',
            '--name', 'Test Policy',
            '-o', 'test_policy.yml'
        ])
        assert result.exit_code != 0
        assert 'Error:' in result.output

def test_template_list(runner, test_templates_dir):
    """Test listing templates."""
    result = runner.invoke(cli, [
        'template', 'list',
        '--templates-dir', str(test_templates_dir)
    ])
    assert result.exit_code == 0
    assert 'Available Templates' in result.output
    assert 'default' in result.output
    assert 'strict' in result.output

def test_template_apply(runner, test_templates_dir):
    """Test applying a template."""
    with runner.isolated_filesystem():
        result = runner.invoke(cli, [
            'template', 'apply',
            'default',
            '--templates-dir', str(test_templates_dir),
            '-o', 'test_policy.yml'
        ])
        assert result.exit_code == 0
        assert Path('test_policy.yml').exists()
        assert any(msg in result.output for msg in ['Policy saved', 'Applied template'])

        # Verify policy contents
        with open('test_policy.yml') as f:
            policy = yaml.safe_load(f)
            assert isinstance(policy, dict)
            assert 'name' in policy
            assert 'description' in policy
            assert 'model' in policy
            assert 'statements' in policy

def test_policy_validate_valid(runner, sample_policy):
    """Test validating a valid policy."""
    with runner.isolated_filesystem():
        with open('test_policy.yml', 'w') as f:
            yaml.dump(sample_policy, f)
            
        result = runner.invoke(cli, ['policy', 'validate', 'test_policy.yml'])
        assert result.exit_code == 0
        assert 'Policy is valid' in result.output

def test_policy_validate_invalid(runner):
    """Test validating an invalid policy."""
    with runner.isolated_filesystem():
        with open('invalid_policy.yml', 'w') as f:
            yaml.dump({'invalid': 'policy'}, f)
            
        result = runner.invoke(cli, ['policy', 'validate', 'invalid_policy.yml'])
        assert result.exit_code != 0
        assert 'Error:' in result.output

def test_template_apply_error(runner, test_templates_dir):
    """Test error handling when applying template fails."""
    with runner.isolated_filesystem():
        result = runner.invoke(cli, [
            'template', 'apply',
            'nonexistent_template',
            '--templates-dir', str(test_templates_dir),
            '-o', 'test_policy.yml'
        ])
        assert result.exit_code != 0
        assert 'Error:' in result.output
        assert not Path('test_policy.yml').exists()