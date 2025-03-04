#!/usr/bin/env python3
"""
Tests for the ignore file generation functionality.
"""

import os
import tempfile
from typing import Dict, Any

import pytest
import yaml

from aria.tools.policy_to_iderules import policy_to_ignore_patterns, update_ignore_file


def test_policy_to_ignore_patterns_basic():
    """Test that basic policy to ignore patterns conversion works."""
    # Create a simple policy
    policy = {
        "name": "Test Policy",
        "description": "A test policy",
        "model": "assistant"
    }
    
    # Generate ignore patterns
    patterns = policy_to_ignore_patterns(policy)
    
    # Check that the basic patterns are included
    assert any("ARIA Policy: Test Policy" in p for p in patterns)
    assert any("A test policy" in p for p in patterns)
    assert any("*.aria.yaml" in p for p in patterns)
    assert any("*.aria.yml" in p for p in patterns)
    assert any("aria_policy.yml" in p for p in patterns)
    
    # Check that sensitive file patterns are included
    assert any(".env" in p for p in patterns)
    assert any("*.pem" in p for p in patterns)
    assert any("*.key" in p for p in patterns)
    assert any("*secret*" in p for p in patterns)
    assert any("*password*" in p for p in patterns)
    assert any("*credential*" in p for p in patterns)
    assert any("*token*" in p for p in patterns)
    assert any("terraform.tfstate" in p for p in patterns)
    assert any("*.db" in p for p in patterns)


def test_policy_to_ignore_patterns_with_paths():
    """Test that path-specific patterns are correctly generated."""
    # Create a policy with path-specific rules
    policy = {
        "name": "Test Policy",
        "description": "A test policy",
        "model": "assistant",
        "paths": {
            "src/secrets/": {
                "model": "guardian"
            },
            "config/sensitive.yml": {
                "deny": ["read"]
            }
        }
    }
    
    # Generate ignore patterns
    patterns = policy_to_ignore_patterns(policy)
    
    # Check that path-specific patterns are included
    assert any("src/secrets/" in p for p in patterns)
    assert any("config/sensitive.yml" in p for p in patterns)


def test_update_ignore_file():
    """Test that the update_ignore_file function works correctly."""
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file_path = temp_file.name
    
    try:
        # Create a simple policy
        policy = {
            "name": "Test Policy",
            "description": "A test policy",
            "model": "assistant"
        }
        
        # Generate ignore patterns
        patterns = policy_to_ignore_patterns(policy)
        
        # Update the ignore file
        update_ignore_file(patterns, temp_file_path)
        
        # Read the file back
        with open(temp_file_path, 'r') as f:
            content = f.read()
        
        # Check that the content includes our patterns
        assert "ARIA Policy: Test Policy" in content
        assert "A test policy" in content
        assert "*.aria.yaml" in content
        assert "*.aria.yml" in content
        assert "aria_policy.yml" in content
        assert ".env" in content
        assert "*.pem" in content
        assert "*secret*" in content
        
    finally:
        # Clean up
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)


def test_update_ignore_file_with_existing_content():
    """Test that the update_ignore_file function preserves existing content."""
    # Create a temporary file with existing content
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(b"# Existing content\n*.log\n\n")
        temp_file_path = temp_file.name
    
    try:
        # Create a simple policy
        policy = {
            "name": "Test Policy",
            "description": "A test policy",
            "model": "assistant"
        }
        
        # Generate ignore patterns
        patterns = policy_to_ignore_patterns(policy)
        
        # Update the ignore file
        update_ignore_file(patterns, temp_file_path)
        
        # Read the file back
        with open(temp_file_path, 'r') as f:
            content = f.read()
        
        # Check that the existing content is preserved
        assert "# Existing content" in content
        assert "*.log" in content
        
        # Check that our patterns are also included
        assert "ARIA Policy: Test Policy" in content
        assert "*.aria.yaml" in content
        
    finally:
        # Clean up
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)


def test_update_ignore_file_with_existing_aria_section():
    """Test that the update_ignore_file function updates existing ARIA section."""
    # Create a temporary file with an existing ARIA section
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(b"# Existing content\n*.log\n\n")
        temp_file.write(b"# BEGIN ARIA POLICY\n")
        temp_file.write(b"# Old ARIA Policy\n")
        temp_file.write(b"*.old\n")
        temp_file.write(b"# END ARIA POLICY\n\n")
        temp_file.write(b"# More content\n*.tmp\n")
        temp_file_path = temp_file.name
    
    try:
        # Create a simple policy
        policy = {
            "name": "Test Policy",
            "description": "A test policy",
            "model": "assistant"
        }
        
        # Generate ignore patterns
        patterns = policy_to_ignore_patterns(policy)
        
        # Update the ignore file
        update_ignore_file(patterns, temp_file_path)
        
        # Read the file back
        with open(temp_file_path, 'r') as f:
            content = f.read()
        
        # Check that the existing content is preserved
        assert "# Existing content" in content
        assert "*.log" in content
        assert "# More content" in content
        assert "*.tmp" in content
        
        # Check that our patterns replaced the old ARIA section
        assert "# Old ARIA Policy" not in content
        assert "*.old" not in content
        assert "ARIA Policy: Test Policy" in content
        assert "*.aria.yaml" in content
        
    finally:
        # Clean up
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
