"""
Command-line interface for ARIA.

This module provides the command-line interface for managing AI participation
policies. It includes commands for initializing new policies, applying templates,
and validating existing policies.

Commands:
    init: Initialize a new policy
    template: Manage policy templates
    policy: Manage ARIA policies
    ide: Manage IDE integration for ARIA policies

Example:
    >>> # Initialize a new policy
    >>> aria init --model assistant --output my_policy.yml
    >>> 
    >>> # List available templates
    >>> aria template list
    >>> 
    >>> # Apply a template
    >>> aria template apply chat_assistant --output my_policy.yml
    >>> 
    >>> # Validate policy
    >>> aria policy validate policy.yml
    >>> 
    >>> # Generate IDE rules from policy
    >>> aria ide rules my_policy.yml
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Callable, TypeVar, cast, Union, Any
import sys
import logging
import time
from functools import wraps
import json
import yaml
import os

import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from aria.core.policy import AIPolicy, PolicyModel
from aria.core.templates import Template, TemplateManager
from aria.logger import get_logger

logger = get_logger(__name__)
console = Console()

F = TypeVar('F', bound=Callable[..., Any])

def handle_error(func: F) -> F:
    """Decorator to handle errors in CLI commands with improved context."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except click.UsageError as e:
            console.print(f"[red]Usage Error: {str(e)}[/red]")
            console.print("[yellow]Run with --help for usage information[/yellow]")
            sys.exit(1)
        except ValueError as e:
            console.print(f"[red]Validation Error: {str(e)}[/red]")
            logger.debug("Validation failed", exc_info=True)
            sys.exit(1)
        except FileNotFoundError as e:
            console.print(f"[red]File Not Found: {str(e)}[/red]")
            logger.debug("File not found", exc_info=True)
            sys.exit(1)
        except yaml.YAMLError as e:
            console.print(f"[red]Invalid YAML: {str(e)}[/red]")
            logger.debug("YAML parsing failed", exc_info=True)
            sys.exit(1)
        except Exception as e:
            console.print(f"[red]Error: An unexpected error occurred[/red]")
            console.print(f"[red]Details: {str(e)}[/red]")
            logger.exception("Command failed with unexpected error")
            sys.exit(1)
    return cast(F, wrapper)

def with_progress(description: str) -> Callable[[F], F]:
    """Decorator to add progress indicator for long-running operations.
    
    Args:
        description: Progress description to display
        
    Returns:
        Decorator function
    """
    def decorator(func: F) -> F:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task(description, total=None)
                result = func(*args, **kwargs)
                progress.remove_task(task)
                return result
        wrapper.__name__ = func.__name__
        return cast(F, wrapper)
    return decorator

@click.group()
def cli() -> None:
    """ARIA - Artificial Intelligence Regulation Interface & Agreements.
    
    A framework for defining and enforcing AI participation policies.
    """
    pass

@cli.group()
def ide() -> None:
    """Manage IDE integration for ARIA policies."""
    pass


@ide.command("rules")
@click.argument("policy_file", type=click.Path(exists=True), required=False)
@click.option("-i", "--ide", type=click.Choice(["windsurf", "cursor", "vscode", "nvim", "emacs"]),
              default="windsurf", help="Target IDE (default: windsurf)")
@click.option("-o", "--output", type=click.Path(), help="Output file (default depends on IDE)")
def ide_rules(policy_file: Optional[str], ide: str, output: Optional[str]) -> None:
    """Generate IDE rules from an ARIA policy.
    
    If POLICY_FILE is not specified, uses the default aria.yml in the current directory.
    """
    from aria.tools.policy_to_iderules import load_policy, policy_to_rules, update_rules_file, IDE_RULE_FILES
    
    try:
        # Use default policy file if not specified
        if not policy_file:
            policy_file = "aria.yml"
            if not os.path.exists(policy_file):
                console.print(f"[red]Error: Default policy file '{policy_file}' not found.[/red]")
                sys.exit(1)
        
        # Determine output file
        rules_output_file = output
        if not rules_output_file:
            rules_output_file = IDE_RULE_FILES[ide]
        
        # Generate rules
        policy = load_policy(policy_file)
        rules = policy_to_rules(policy)
        update_rules_file(rules, rules_output_file)
        
        console.print(f"[green]Successfully generated {ide} rules in {rules_output_file}[/green]")
    except Exception as e:
        logger.error(f"Failed to generate IDE rules: {e}")
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@ide.command("ignore")
@click.argument("policy_file", type=click.Path(exists=True), required=False)
@click.option("-i", "--ide", type=click.Choice(["windsurf", "cursor"]),
              default="windsurf", help="Target IDE (default: windsurf)")
@click.option("-o", "--output", type=click.Path(), help="Output file (default depends on IDE)")
def ide_ignore(policy_file: Optional[str], ide: str, output: Optional[str]) -> None:
    """Generate IDE ignore files from an ARIA policy.
    
    If POLICY_FILE is not specified, uses the default aria.yml in the current directory.
    """
    from aria.tools.policy_to_iderules import (
        load_policy, policy_to_ignore_patterns, update_ignore_file, IDE_IGNORE_FILES
    )
    
    try:
        # Use default policy file if not specified
        if not policy_file:
            policy_file = "aria.yml"
            if not os.path.exists(policy_file):
                console.print(f"[red]Error: Default policy file '{policy_file}' not found.[/red]")
                sys.exit(1)
        
        # Determine output file
        ignore_output_file = output
        if not ignore_output_file and ide in IDE_IGNORE_FILES:
            ignore_output_file = IDE_IGNORE_FILES[ide]
        
        if not ignore_output_file:
            console.print("[red]Error: No output file specified and no default for selected IDE[/red]")
            sys.exit(1)
            
        # Generate ignore patterns
        policy = load_policy(policy_file)
        ignore_patterns = policy_to_ignore_patterns(policy)
        update_ignore_file(ignore_patterns, ignore_output_file)
        
        console.print(f"[green]Successfully generated {ide} ignore file in {ignore_output_file}[/green]")
    except Exception as e:
        logger.error(f"Failed to generate IDE ignore file: {e}")
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


@ide.command("generate")
@click.argument("policy_file", type=click.Path(exists=True), required=False)
@click.option("-i", "--ide", type=click.Choice(["windsurf", "cursor", "vscode", "nvim", "emacs"]),
              default="windsurf", help="Target IDE (default: windsurf)")
@click.option("--rules-output", type=click.Path(), help="Output file for rules (default depends on IDE)")
@click.option("--ignore-output", type=click.Path(), help="Output file for ignore patterns (default depends on IDE)")
@click.option("--no-ignore", is_flag=True, help="Skip generating ignore file")
def ide_generate(
    policy_file: Optional[str], 
    ide: str, 
    rules_output: Optional[str], 
    ignore_output: Optional[str],
    no_ignore: bool
) -> None:
    """Generate both IDE rules and ignore files from an ARIA policy.
    
    If POLICY_FILE is not specified, uses the default aria.yml in the current directory.
    """
    from aria.tools.policy_to_iderules import (
        load_policy, policy_to_rules, update_rules_file, IDE_RULE_FILES,
        policy_to_ignore_patterns, update_ignore_file, IDE_IGNORE_FILES
    )
    
    try:
        # Use default policy file if not specified
        if not policy_file:
            policy_file = "aria.yml"
            if not os.path.exists(policy_file):
                console.print(f"[red]Error: Default policy file '{policy_file}' not found.[/red]")
                sys.exit(1)
        
        # Load policy
        policy = load_policy(policy_file)
        
        # Determine output files
        rules_file = rules_output
        if not rules_file:
            rules_file = IDE_RULE_FILES[ide]
        
        # Generate rules
        rules = policy_to_rules(policy)
        update_rules_file(rules, rules_file)
        console.print(f"[green]Successfully generated {ide} rules in {rules_file}[/green]")
        
        # Generate ignore file if applicable
        if not no_ignore and ide in IDE_IGNORE_FILES:
            ignore_file = ignore_output
            if not ignore_file:
                ignore_file = IDE_IGNORE_FILES[ide]
            
            if not ignore_file:
                console.print("[red]Error: No output file specified and no default for selected IDE[/red]")
                sys.exit(1)
                
            ignore_patterns = policy_to_ignore_patterns(policy)
            update_ignore_file(ignore_patterns, ignore_file)
            console.print(f"[green]Successfully generated {ide} ignore file in {ignore_file}[/green]")
    
    except Exception as e:
        logger.error(f"Failed to generate IDE files: {e}")
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)

@cli.command()
@click.option('--model', type=click.Choice(['guardian', 'observer', 'assistant', 'collaborator', 'partner']), required=True,
              help='Policy model type')
@click.option('-o', '--output', type=str, default='aria_policy.yml',
              help='Output file path')
@click.option('--templates-dir', type=str, help='Templates directory')
@click.option('--name', type=str, default='Default Policy',
              help='Policy name')
@click.option('--description', type=str,
              default='Default ARIA policy configuration',
              help='Policy description')
@handle_error
@with_progress("Initializing policy...")
def init(model: str, output: str, templates_dir: Optional[str], name: str, description: str) -> None:
    """Initialize a new policy."""
    logger.info(f"Initializing new policy with model '{model}' at '{output}'")
    
    try:
        # Convert model string to enum
        policy_model = PolicyModel[model.upper()]
        
        # Create initial policy
        policy = AIPolicy(
            name=name,
            description=description,
            model=policy_model,
            statements=[],
            path_policies=[]
        )
        
        # Save policy to file
        policy.to_yaml_file(output)
        logger.info(f"Policy initialized at {output}")
        console.print(f"[green]Created new policy '{name}' at {output}[/green]")
        
    except Exception as e:
        logger.error(f"Failed to initialize policy: {e}")
        console.print(f"[red]Error: Failed to initialize policy[/red]")
        console.print(f"[red]Details: {str(e)}[/red]")
        sys.exit(1)

@cli.group()
def template() -> None:
    """Manage policy templates."""
    pass

@template.command(name='list')
@click.option('--templates-dir', type=str, help='Templates directory')
@handle_error
def list_templates(templates_dir: Optional[str]) -> None:
    """List available templates."""
    manager = TemplateManager(templates_dir=templates_dir)
    templates = manager.list_templates()
    
    if not templates:
        click.echo("No templates found")
        return
        
    click.echo("\nAvailable Templates:")
    for template in templates:
        model_value = template.model.value if isinstance(template.model, PolicyModel) else template.model
        click.echo(f"\n{template.name}:")
        click.echo(f"  Description: {template.description}")
        click.echo(f"  Model: {model_value}")

@template.command(name='apply')
@click.argument('name')
@click.option('--templates-dir', type=str, help='Templates directory')
@click.option('-o', '--output', type=str, help='Output file path')
@handle_error
@with_progress("Applying template...")
def apply(name: str, templates_dir: Optional[str], output: Optional[str]) -> None:
    """Apply a template to create/update policy."""
    manager = TemplateManager(templates_dir=templates_dir)
    template = manager.get_template(name)
    if not template:
        raise click.UsageError(f"Template '{name}' not found")
    
    # Use the template's apply method to create a policy with proper fields
    policy = template.apply()
    
    if output:
        # Ensure parent directory exists
        output_dir = os.path.dirname(os.path.abspath(output))
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            
        # Save policy using its YAML methods
        policy.to_yaml_file(output)
        click.echo(f"Policy saved to {output}")
    else:
        # Print to stdout if no output file specified
        click.echo(policy.to_yaml())

@cli.group()
def policy() -> None:
    """Manage ARIA policies."""
    pass

@policy.command(name='validate')
@click.argument('policy_file')
@handle_error
@with_progress("Validating policy...")
def validate(policy_file: str) -> None:
    """Validate a policy file."""
    logger.info(f"Validating policy file '{policy_file}'")
    try:
        policy = AIPolicy.from_yaml_file(policy_file)
        if policy.validate_model():
            logger.info("Policy validation successful")
            console.print(f"[green]Policy is valid[/green]")
        else:
            logger.error("Policy validation failed")
            console.print(f"[red]Policy validation failed[/red]")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Failed to validate policy: {e}")
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)

def main() -> None:
    """Entry point for command-line execution."""
    cli()

if __name__ == '__main__':
    main()