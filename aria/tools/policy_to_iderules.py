#!/usr/bin/env python3
"""
ARIA Policy to IDE Rules Converter

This tool converts ARIA policy files to various IDE rules formats,
including Windsurf (.windsurfrules) and Cursor (.cursorrules).
"""

import argparse
import os
import sys
from typing import Dict, List, Any, Optional, Tuple

import yaml

# IDE-specific rule file paths
IDE_RULE_FILES = {
    "windsurf": ".windsurfrules",
    "cursor": ".cursorrules",
    "vscode": ".vscode/aria-rules.json",  # Future support
    "nvim": ".nvim/aria-rules.lua",       # Future support
    "emacs": ".emacs.d/aria-rules.el"     # Future support
}

# IDE-specific ignore file paths
IDE_IGNORE_FILES = {
    "windsurf": ".codeiumignore",
    "cursor": ".cursorignore"
}

def load_policy(policy_file: str) -> Dict[str, Any]:
    """Load an ARIA policy file."""
    try:
        with open(policy_file, 'r') as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        print(f"Error loading policy file: {e}", file=sys.stderr)
        sys.exit(1)

def policy_to_rules(policy: Dict[str, Any]) -> List[str]:
    """Convert an ARIA policy to IDE rules."""
    rules = []
    
    # Add header
    rules.append(f"# ARIA Policy: {policy.get('name', 'Unnamed Policy')}")
    rules.append(f"# {policy.get('description', 'No description provided')}")
    rules.append("")
    
    # Add model-based rule
    model = policy.get('model', 'assistant').lower()
    if model == 'guardian':
        rules.append("1. AI assistants must not modify any files without explicit permission")
        rules.append("2. AI assistants must not generate code that could harm the system")
        rules.append("3. AI assistants must always explain their reasoning before making changes")
        rules.append("4. AI assistants must prioritize security and safety over functionality")
    elif model == 'observer':
        rules.append("1. AI assistants must not modify any files under any circumstances")
        rules.append("2. AI assistants may only provide information and answer questions")
        rules.append("3. AI assistants must not suggest code changes directly")
    elif model == 'collaborator':
        rules.append("1. AI assistants may suggest changes but must get approval first")
        rules.append("2. AI assistants must explain the reasoning behind their suggestions")
        rules.append("3. AI assistants should prioritize code quality and maintainability")
    elif model == 'partner':
        rules.append("1. AI assistants may make changes to improve code quality")
        rules.append("2. AI assistants should follow project conventions and standards")
        rules.append("3. AI assistants should document significant changes they make")
    else:  # Default to assistant
        rules.append("1. AI assistants should follow project conventions and standards")
        rules.append("2. AI assistants should explain significant changes they suggest")
    
    # Add capability-based rules
    capabilities = policy.get('capabilities', {})
    for capability, allowed in capabilities.items():
        if not allowed:
            rules.append(f"AI assistants must not {capability}")
    
    # Add path-specific rules
    paths = policy.get('paths', {})
    for path, path_policy in paths.items():
        path_model = path_policy.get('model', '').lower()
        if path_model == 'guardian':
            rules.append(f"AI assistants must not modify files in {path} without explicit permission")
        elif path_model == 'observer':
            rules.append(f"AI assistants must not modify files in {path} under any circumstances")
    
    return rules

def policy_to_ignore_patterns(policy: Dict[str, Any]) -> List[str]:
    """Convert an ARIA policy to IDE ignore patterns."""
    ignore_patterns = []
    
    # Add header with disclaimer about current limitations
    ignore_patterns.append(f"# ARIA Policy: {policy.get('name', 'Unnamed Policy')}")
    ignore_patterns.append(f"# {policy.get('description', 'No description provided')}")
    ignore_patterns.append("#")
    ignore_patterns.append("# DISCLAIMER: This is a basic implementation of ARIA policy enforcement.")
    ignore_patterns.append("# Full enforcement requires IDE plugins that are currently in development.")
    ignore_patterns.append("# This ignore file provides only basic protection by preventing AI access to sensitive files.")
    ignore_patterns.append("")
    
    # Add standard patterns for policy files
    ignore_patterns.append("# Protect ARIA policy files")
    ignore_patterns.append("*.aria.yaml")
    ignore_patterns.append("*.aria.yml")
    ignore_patterns.append("aria_policy.yml")  # Explicitly protect the main policy file
    ignore_patterns.append(".aria/")
    ignore_patterns.append("")
    
    # Do NOT add IDE rule files to the ignore patterns
    # We want AI to be able to read them, just not modify them
    # This is handled by the rules themselves
    
    # Add path-specific patterns only for guardian model or explicitly denied paths
    paths = policy.get('paths', {})
    protected_paths = []
    
    for path, path_policy in paths.items():
        # Only completely exclude paths with guardian model or explicit deny: ["read"]
        path_model = path_policy.get('model', '').lower()
        deny_actions = path_policy.get('deny', [])
        
        if path_model == 'guardian' or 'read' in deny_actions:
            protected_paths.append(path)
    
    if protected_paths:
        ignore_patterns.append("# Protected paths from ARIA policy")
        for path in protected_paths:
            # Ensure the path has the correct format for ignore files
            if path.endswith('/'):
                ignore_patterns.append(path)
            elif os.path.isdir(path):
                ignore_patterns.append(f"{path}/")
            else:
                ignore_patterns.append(path)
    
    return ignore_patterns

def read_existing_file(file_path: str) -> Tuple[List[str], List[str], List[str]]:
    """Read an existing file and extract ARIA section."""
    try:
        if not os.path.exists(file_path):
            return [], [], []
        
        with open(file_path, 'r') as f:
            lines = f.read().splitlines()
        
        aria_start = None
        aria_end = None
        
        for i, line in enumerate(lines):
            if line.strip() == "# BEGIN ARIA POLICY":
                aria_start = i
            elif line.strip() == "# END ARIA POLICY":
                aria_end = i
                break
        
        if aria_start is not None and aria_end is not None:
            before_aria = lines[:aria_start]
            aria_section = lines[aria_start:aria_end+1]
            after_aria = lines[aria_end+1:]
            return before_aria, aria_section, after_aria
        else:
            return lines, [], []
    except Exception as e:
        print(f"Warning: Could not read existing file {file_path}: {e}", file=sys.stderr)
        return [], [], []

def update_rules_file(rules: List[str], output_file: str) -> None:
    """Update an IDE rules file with ARIA policy rules."""
    try:
        before_aria, _, after_aria = read_existing_file(output_file)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
        
        # Wrap rules in ARIA section markers
        aria_section = ["# BEGIN ARIA POLICY"]
        aria_section.extend(rules)
        aria_section.append("# END ARIA POLICY")
        
        # Combine sections
        combined_rules = before_aria + aria_section + after_aria
        
        with open(output_file, 'w') as f:
            for rule in combined_rules:
                f.write(f"{rule}\n")
        
        print(f"Rules updated in {output_file}")
    except Exception as e:
        print(f"Error writing rules: {e}", file=sys.stderr)
        sys.exit(1)

def update_ignore_file(patterns: List[str], output_file: str) -> None:
    """Update an IDE ignore file with ARIA policy patterns."""
    try:
        before_aria, _, after_aria = read_existing_file(output_file)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
        
        # Wrap patterns in ARIA section markers
        aria_section = ["# BEGIN ARIA POLICY"]
        aria_section.extend(patterns)
        aria_section.append("# END ARIA POLICY")
        
        # Combine sections
        combined_patterns = before_aria + aria_section + after_aria
        
        with open(output_file, 'w') as f:
            for pattern in combined_patterns:
                f.write(f"{pattern}\n")
        
        print(f"Ignore patterns updated in {output_file}")
    except Exception as e:
        print(f"Error writing ignore patterns: {e}", file=sys.stderr)
        sys.exit(1)

def main() -> None:
    parser = argparse.ArgumentParser(description="Convert ARIA policy to IDE rules and ignore files")
    parser.add_argument("policy_file", help="Path to ARIA policy file")
    parser.add_argument("-o", "--output", help="Output file for rules (default depends on IDE)")
    parser.add_argument("-i", "--ide", choices=IDE_RULE_FILES.keys(), default="windsurf",
                        help="Target IDE (default: windsurf)")
    parser.add_argument("--ignore", action="store_true", help="Also generate IDE ignore file")
    parser.add_argument("--ignore-output", help="Output file for ignore patterns (default depends on IDE)")
    
    args = parser.parse_args()
    
    # Determine output files
    rules_output_file = args.output
    if not rules_output_file:
        rules_output_file = IDE_RULE_FILES[args.ide]
    
    ignore_output_file = args.ignore_output
    if not ignore_output_file and args.ide in IDE_IGNORE_FILES:
        ignore_output_file = IDE_IGNORE_FILES[args.ide]
    
    # Load policy and generate rules
    policy = load_policy(args.policy_file)
    rules = policy_to_rules(policy)
    update_rules_file(rules, rules_output_file)
    
    # Generate ignore file if requested
    if args.ignore and ignore_output_file:
        ignore_patterns = policy_to_ignore_patterns(policy)
        update_ignore_file(ignore_patterns, ignore_output_file)

if __name__ == "__main__":
    main()
