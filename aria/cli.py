"""
Command-line interface for ARIA.

This module provides the command-line interface for managing AI participation
policies. It includes commands for initializing new policies, applying templates,
and validating existing policies.

Commands:
    init: Initialize a new policy
    apply: Apply a template to create/update policy
    validate: Validate an existing policy
    list-templates: List available templates

Example:
    >>> # Initialize a new policy
    >>> aria init --model assistant
    >>> 
    >>> # Apply a template
    >>> aria apply --template chat_assistant
    >>> 
    >>> # Validate policy
    >>> aria validate policy.yml
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Callable, TypeVar, cast, Union, Any
import sys
import logging
import time

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
    """Decorator to handle errors in CLI commands.
    
    Args:
        func: Function to wrap
        
    Returns:
        Wrapped function that handles errors
    """
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Command failed: {error_msg}")
            console.print(f"[red]Error: {error_msg}[/red]")
            sys.exit(1)
    wrapper.__name__ = func.__name__
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
    """ARIA - AI Participation Policy Management.
    
    Command-line tool for managing AI participation policies. Supports creating,
    applying templates to, and validating policies.
    """
    pass

@cli.command()
@click.option('--model', '-m', type=click.Choice([m.value for m in PolicyModel]), default='assistant',
              help='Policy model type')
@click.option('--output', '-o', type=click.Path(), default='aria.yml',
              help='Output policy file')
@click.option('--templates-dir', '-t', type=click.Path(exists=False), help='Directory containing templates')
@handle_error
@with_progress("Initializing new policy...")
def init(model: str, output: str, templates_dir: Optional[str]) -> None:
    """Initialize a new policy.
    
    Creates a new policy file with basic structure for the specified model.
    
    Args:
        model: Policy model type ('assistant' or 'tool')
        output: Output file path for the policy
        
    Example:
        $ aria init --model assistant --output my_policy.yml
    """
    logger.info(f"Initializing new policy with model '{model}' at '{output}'")
    manager = TemplateManager(templates_dir)
    policy_model = PolicyModel(model)  # Convert string to enum
    template = manager.get_template(policy_model.value)
    policy = manager.create_policy(template)
    
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(policy.to_yaml())
    logger.info(f"Created new policy at '{output}'")
    console.print(f"[green]Created new policy at {output}[/green]")

@cli.command()
@click.argument('name', type=str)
@click.option('--templates-dir', '-t', type=click.Path(exists=False), help='Directory containing templates')
@click.option('--output', '-o', type=click.Path(), help='Output policy file')
@handle_error
@with_progress("Applying template...")
def apply(name: str, templates_dir: Optional[str], output: Optional[str]) -> None:
    """Apply a template to create/update policy.
    
    Creates a new policy or updates existing one using the specified template.
    
    Args:
        name: Name of template to apply
        output: Output file path for the policy
        
    Example:
        $ aria apply --template chat_assistant --output my_policy.yml
    """
    logger.info(f"Applying template '{name}'")
    manager = TemplateManager(templates_dir)
    
    # Try to convert name to PolicyModel if it matches an enum value
    try:
        policy_model = PolicyModel(name)
        name = policy_model.value
    except ValueError:
        pass  # Not a policy model name, use as-is
    
    template = manager.get_template(name)
    policy = manager.create_policy(template)
    
    if output:
        logger.info(f"Writing policy to '{output}'")
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(policy.to_yaml())
        console.print(f"[green]Created new policy at {output}[/green]")
    else:
        console.print(policy.to_yaml())

@cli.group()
def policy() -> None:
    """Manage ARIA policies."""
    pass

@policy.command()
@click.argument('policy_file', type=click.Path(exists=True))
@handle_error
@with_progress("Validating policy...")
def validate(policy_file: str) -> None:
    """Validate a policy file.
    
    Checks if policy file meets all requirements and constraints.
    
    Args:
        policy_file: Path to policy file to validate
        
    Example:
        $ aria validate policy.yml
    """
    logger.info(f"Validating policy file '{policy_file}'")
    try:
        policy = AIPolicy.from_yaml_file(policy_file)
        if policy.validate():
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

@cli.command(name='list-templates')
@click.option('--templates-dir', '-t', type=click.Path(exists=False), help='Directory containing templates')
@handle_error
@with_progress("Loading templates...")
def list_templates(templates_dir: Optional[str]) -> None:
    """List available templates.
    
    Displays a table of available templates with their descriptions.
    
    Example:
        $ aria list-templates
    """
    logger.info("Listing available templates")
    manager = TemplateManager(templates_dir)
    templates = manager.list_templates()
    
    table = Table(title="Available Templates")
    table.add_column("Name", style="cyan")
    table.add_column("Description")
    table.add_column("Model", style="magenta")
    table.add_column("Tags", style="green")
    
    for t in templates:
        table.add_row(
            t.name,
            t.description,
            t.model.value,
            ", ".join(t.tags) if t.tags else "-"
        )
    
    console.print(table)

if __name__ == '__main__':
    cli()