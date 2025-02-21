"""Tests for ARIA policy inheritance system."""
import pytest
from aria.core.policy import (
    AIAction, AIPolicy, PathPolicy, PolicyEffect,
    PolicyModel, PolicyStatement
)

def test_basic_inheritance():
    """Test basic policy inheritance from model."""
    policy = AIPolicy(
        name="Test Policy",
        description="Test policy inheritance",
        model=PolicyModel.ASSISTANT,
        statements=[],
        path_policies=[]
    )
    
    # ASSISTANT model should allow ANALYZE, REVIEW, SUGGEST
    perms = policy.get_permissions("test.py")
    assert AIAction.ANALYZE in perms
    assert AIAction.REVIEW in perms
    assert AIAction.SUGGEST in perms
    assert AIAction.MODIFY not in perms
    assert AIAction.GENERATE not in perms
    assert AIAction.EXECUTE not in perms

def test_global_statement_override():
    """Test global policy statements override model defaults."""
    policy = AIPolicy(
        name="Test Policy",
        description="Test global statement override",
        model=PolicyModel.ASSISTANT,
        statements=[
            PolicyStatement(
                effect=PolicyEffect.DENY,
                actions=[AIAction.SUGGEST],
                resources=["*.py"]
            )
        ]
    )
    
    perms = policy.get_permissions("test.py")
    assert AIAction.ANALYZE in perms
    assert AIAction.REVIEW in perms
    assert AIAction.SUGGEST not in perms  # Denied by global statement

def test_path_policy_override():
    """Test path-specific policies override global statements."""
    policy = AIPolicy(
        name="Test Policy",
        description="Test path override",
        model=PolicyModel.ASSISTANT,
        statements=[
            PolicyStatement(
                effect=PolicyEffect.DENY,
                actions=[AIAction.SUGGEST],
                resources=["*.py"]
            )
        ],
        path_policies=[
            PathPolicy(
                pattern="test/*",
                statements=[
                    PolicyStatement(
                        effect=PolicyEffect.ALLOW,
                        actions=[AIAction.SUGGEST],
                        resources=["*.py"]
                    )
                ]
            )
        ]
    )
    
    # Global deny doesn't affect path with explicit allow
    perms = policy.get_permissions("test/script.py")
    assert AIAction.SUGGEST in perms
    
    # Global deny affects other paths
    perms = policy.get_permissions("other/script.py")
    assert AIAction.SUGGEST not in perms

def test_multiple_statements():
    """Test multiple policy statements evaluation."""
    policy = AIPolicy(
        name="Test Policy",
        description="Test multiple statements",
        model=PolicyModel.ASSISTANT,
        statements=[
            PolicyStatement(
                effect=PolicyEffect.ALLOW,
                actions=[AIAction.GENERATE],
                resources=["*.py"]
            ),
            PolicyStatement(
                effect=PolicyEffect.DENY,
                actions=[AIAction.GENERATE],
                resources=["test/*.py"]
            )
        ]
    )
    
    # Last matching statement wins
    perms = policy.get_permissions("test/script.py")
    assert AIAction.GENERATE not in perms
    
    perms = policy.get_permissions("other/script.py")
    assert AIAction.GENERATE in perms
