"""Tests for ARIA policy models."""
import pytest
from aria.core.policy import (
    AIAction, AIPolicy, PathPolicy, PolicyEffect,
    PolicyModel, PolicyStatement
)

def test_model_permissions():
    """Test permissions for different policy models."""
    # Test GUARDIAN model
    policy = AIPolicy(
        name="Guardian Policy",
        description="Test guardian model",
        model=PolicyModel.GUARDIAN,
        statements=[],
        path_policies=[]
    )
    perms = policy.get_permissions("test.py")
    assert AIAction.ANALYZE in perms
    assert AIAction.REVIEW in perms
    assert AIAction.SUGGEST not in perms
    assert AIAction.GENERATE not in perms
    assert AIAction.MODIFY not in perms
    assert AIAction.EXECUTE not in perms

    # Test OBSERVER model
    policy = AIPolicy(
        name="Observer Policy",
        description="Test observer model",
        model=PolicyModel.OBSERVER,
        statements=[],
        path_policies=[]
    )
    perms = policy.get_permissions("test.py")
    assert AIAction.ANALYZE in perms
    assert AIAction.REVIEW not in perms
    assert AIAction.SUGGEST not in perms
    assert AIAction.GENERATE not in perms
    assert AIAction.MODIFY not in perms
    assert AIAction.EXECUTE not in perms

    # Test ASSISTANT model
    policy = AIPolicy(
        name="Assistant Policy",
        description="Test assistant model",
        model=PolicyModel.ASSISTANT,
        statements=[],
        path_policies=[]
    )
    perms = policy.get_permissions("test.py")
    assert AIAction.ANALYZE in perms
    assert AIAction.REVIEW in perms
    assert AIAction.SUGGEST in perms
    assert AIAction.GENERATE not in perms
    assert AIAction.MODIFY not in perms
    assert AIAction.EXECUTE not in perms

def test_policy_statement_override():
    """Test policy statement overrides."""
    policy = AIPolicy(
        name="Test Policy",
        description="Test statement override",
        model=PolicyModel.ASSISTANT,
        statements=[
            PolicyStatement(
                effect=PolicyEffect.DENY,
                actions=[AIAction.ANALYZE],
                resources=["*.py"]
            )
        ]
    )
    perms = policy.get_permissions("test.py")
    assert AIAction.ANALYZE not in perms  # Explicitly denied
    assert AIAction.REVIEW in perms      # Still allowed by model
    assert AIAction.SUGGEST in perms     # Still allowed by model

def test_path_policy_precedence():
    """Test path policy precedence."""
    policy = AIPolicy(
        name="Test Policy",
        description="Test path precedence",
        model=PolicyModel.ASSISTANT,
        statements=[
            PolicyStatement(
                effect=PolicyEffect.DENY,
                actions=[AIAction.ANALYZE],
                resources=["*.py"]
            )
        ],
        path_policies=[
            PathPolicy(
                pattern="test/*",
                statements=[
                    PolicyStatement(
                        effect=PolicyEffect.ALLOW,
                        actions=[AIAction.ANALYZE],
                        resources=["*.py"]
                    )
                ]
            )
        ]
    )
    
    # Path policy should take precedence
    perms = policy.get_permissions("test/script.py")
    assert AIAction.ANALYZE in perms
    
    # Global policy applies elsewhere
    perms = policy.get_permissions("other/script.py")
    assert AIAction.ANALYZE not in perms
