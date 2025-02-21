"""Minimal test to verify imports."""
import pytest
from aria.core.policy import PolicyModel

def test_minimal():
    """Verify basic import works."""
    assert PolicyModel.GUARDIAN == "guardian"
