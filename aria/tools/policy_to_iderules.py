#!/usr/bin/env python3
"""
ARIA Policy to IDE Rules Converter

This tool converts ARIA policy files to various IDE rules formats,
including Windsurf (.windsurfrules) and Cursor (.cursorrules).
"""

import argparse
import os
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional

# Define supported IDEs and their rule file names
IDE_RULE_FILES = {
    "windsurf": ".windsurfrules",
    "cursor": ".cursorrules",
    "vscode": ".vscode/aria-rules.json",  # Future support
    "nvim": ".nvim/aria-rules.lua",       # Future support
    "emacs": ".emacs.d/aria-rules.el"     # Future support
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
    elif model == 'observer':
        rules.append("1. AI assistants may only analyze and review code, not modify it")
    elif model == 'assistant':
        rules.append("1. AI assistants may suggest and generate code with human review")
    elif model == 'collaborator':
        rules.append("1. AI assistants may contribute to specific project areas with appropriate permissions")
    elif model == 'partner':
        rules.append("1. AI assistants may participate fully with safety guardrails")
    
    # Add default rules
    defaults = policy.get('defaults', {})
    default_allow = defaults.get('allow', [])
    default_require = defaults.get('require', [])
    
    if not default_allow:
        rules.append("2. AI assistants must not modify files by default")
    else:
        allowed = ", ".join(default_allow)
        rules.append(f"2. AI assistants may {allowed} by default")
    
    if default_require:
        requirements = ", ".join(default_require)
        rules.append(f"3. All AI contributions require {requirements}")
    
    # Add path-specific rules
    rule_index = 4
    paths = policy.get('paths', {})
    for path_pattern, path_policy in paths.items():
        allow = path_policy.get('allow', [])
        require = path_policy.get('require', [])
        effect = path_policy.get('effect', 'allow')
        
        if effect == 'deny' or not allow:
            rules.append(f"{rule_index}. AI assistants must not modify files in {path_pattern}")
        else:
            allowed = ", ".join(allow)
            rules.append(f"{rule_index}. AI assistants may {allowed} files in {path_pattern}")
        
        rule_index += 1
        
        if require:
            requirements = ", ".join(require)
            rules.append(f"{rule_index}. Changes to {path_pattern} require {requirements}")
            rule_index += 1
    
    return rules

def update_rules_file(rules: List[str], output_file: str) -> None:
    """Update rules file without overwriting existing content."""
    try:
        # Create directory if it doesn't exist (for nested paths like .vscode/)
        if os.path.dirname(output_file):
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        existing_rules = []
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                existing_rules = f.readlines()
                # Remove trailing newlines
                existing_rules = [line.rstrip() for line in existing_rules]
        
        # Add separator if file exists and doesn't end with empty lines
        if existing_rules and existing_rules[-1].strip():
            existing_rules.append("")
            existing_rules.append("# ===== ARIA Policy Rules (Auto-generated) =====")
        
        # Combine existing rules with new rules
        combined_rules = existing_rules if existing_rules else []
        if not combined_rules:
            combined_rules = rules
        else:
            # Only add new rules if they don't exist
            aria_section_start = -1
            for i, line in enumerate(combined_rules):
                if "ARIA Policy Rules (Auto-generated)" in line:
                    aria_section_start = i
                    break
            
            if aria_section_start >= 0:
                # Replace existing ARIA rules
                combined_rules = combined_rules[:aria_section_start+1] + rules
            else:
                # Append new rules
                combined_rules.extend(rules)
        
        with open(output_file, 'w') as f:
            for rule in combined_rules:
                f.write(f"{rule}\n")
        
        print(f"Rules updated in {output_file}")
    except Exception as e:
        print(f"Error writing rules: {e}", file=sys.stderr)
        sys.exit(1)

def main() -> None:
    parser = argparse.ArgumentParser(description="Convert ARIA policy to IDE rules")
    parser.add_argument("policy_file", help="Path to ARIA policy file")
    parser.add_argument("-o", "--output", help="Output file (default depends on IDE)")
    parser.add_argument("-i", "--ide", choices=IDE_RULE_FILES.keys(), default="windsurf",
                        help="Target IDE (default: windsurf)")
    
    args = parser.parse_args()
    
    # Determine output file
    output_file = args.output
    if not output_file:
        output_file = IDE_RULE_FILES[args.ide]
    
    policy = load_policy(args.policy_file)
    rules = policy_to_rules(policy)
    update_rules_file(rules, output_file)

if __name__ == "__main__":
    main()
