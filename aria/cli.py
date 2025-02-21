"""
Command-line interface for ARIA.

This module provides the command-line interface for managing AI participation
policies. It includes commands for initializing new policies, applying templates,
and validating existing policies.

Commands:
    init: Initialize a new policy
    template: Manage policy templates
    policy: Manage ARIA policies

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
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Callable, TypeVar, cast, Union, Any
import sys
import logging
import time
from functools import wraps

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
    """Decorator to handle errors in CLI commands."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except click.UsageError as e:
            console.print(f"[red]Error: {str(e)}[/red]")
            sys.exit(1)
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")
            logger.exception("Command failed")
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
def cli():
    """ARIA - AI Participation Manager.

    Command-line tool for managing AI participation policies. Supports creating,
    applying templates to, and validating policies.
    """
    pass

@cli.command()
@click.option('--model', type=click.Choice(['assistant', 'tool']), required=True,
              help='Policy model type')
@click.option('--output', '-o', type=str, required=True,
              help='Output file path')
@click.option('--templates-dir', type=str,
              help='Custom templates directory')
@handle_error
@with_progress("Initializing new policy...")
def init(model: str, output: str, templates_dir: Optional[str]):
    """Initialize a new policy."""
    try:
        logger.info(f"Initializing new policy with model '{model}' at '{output}'")
        manager = TemplateManager(templates_dir)
        policy_model = PolicyModel(model)
        
        # Create output directory if it doesn't exist
        output_path = Path(output)
        if not output_path.parent.exists():
            raise click.UsageError(f"Directory does not exist: {output_path.parent}")
        
        template = manager.get_template(f"base_{model}")
        policy = template.apply()
        policy.save(output)
        
        logger.info(f"Created new policy at '{output}'")
        console.print(f"[green]Created new policy at {output}[/green]")
    except Exception as e:
        raise click.UsageError(str(e))

@cli.group()
def template():
    """Manage policy templates."""
    pass

@template.command(name='list')
@click.option('--templates-dir', type=str,
              help='Custom templates directory')
@handle_error
@with_progress("Loading templates...")
def list_templates(templates_dir: Optional[str]):
    """List available templates."""
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

@template.command(name='apply')
@click.argument('name')
@click.option('--templates-dir', type=str,
              help='Custom templates directory')
@click.option('--output', '-o', type=str,
              help='Output file path')
@handle_error
@with_progress("Applying template...")
def apply(name: str, templates_dir: Optional[str], output: Optional[str]):
    """Apply a template to create/update policy."""
    logger.info(f"Applying template '{name}'")
    manager = TemplateManager(templates_dir)
    
    try:
        policy_model = PolicyModel(name)
        name = policy_model.value
    except ValueError:
        pass  # Not a policy model name, use as-is
    
    template = manager.get_template(name)
    policy = template.apply()
    
    if output:
        logger.info(f"Writing policy to '{output}'")
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        policy.save(output)
        console.print(f"[green]Created new policy at {output}[/green]")
    else:
        console.print(policy.to_yaml())

@cli.group()
def policy():
    """Manage ARIA policies."""
    pass

@policy.command(name='validate')
@click.argument('policy_file')
@handle_error
@with_progress("Validating policy...")
def validate(policy_file: str):
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

if __name__ == '__main__':
    cli()