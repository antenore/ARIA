"""
Output formatting for ARIA.

This module handles formatting of output using Rich.
"""
from __future__ import annotations

from typing import Any, Dict, Union, List, Sequence

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree

from aria.core.validator import ValidationResult

console = Console()

def format_validation_results(results: Union[ValidationResult, Dict[str, Any]]) -> Panel:
    """Format validation results.
    
    Args:
        results: Validation results
        
    Returns:
        Formatted panel
    """
    if isinstance(results, ValidationResult):
        results = results.as_dict()
    
    # Create tree structure
    tree = Tree("Validation Results")
    
    # Add status
    status = "✓ Valid" if results["valid"] else "✗ Invalid"
    status_style = "green" if results["valid"] else "red"
    tree.add(f"[{status_style}]{status}[/]")
    
    # Add errors if any
    if results.get("errors"):
        error_branch = tree.add("[red]Errors[/]")
        for error in results["errors"]:
            error_branch.add(f"[red]• {error}[/]")
    
    # Add warnings if any
    if results.get("warnings"):
        warning_branch = tree.add("[yellow]Warnings[/]")
        for warning in results["warnings"]:
            warning_branch.add(f"[yellow]• {warning}[/]")
    
    # Add checked files if any
    if results.get("checked_files"):
        files_branch = tree.add("Checked Files")
        for file in results["checked_files"]:
            files_branch.add(file)
    
    return Panel(
        tree,
        title="ARIA Validation",
        border_style=status_style
    )

def format_table(
    title: str,
    headers: Sequence[str],
    rows: Sequence[Sequence[str]],
    style: str = "default"
) -> Table:
    """Create a formatted table.
    
    Args:
        title: Table title
        headers: Column headers
        rows: Table rows
        style: Table style
        
    Returns:
        Formatted table
    """
    table = Table(title=title, style=style)
    
    # Add headers
    for header in headers:
        table.add_column(header)
    
    # Add rows
    for row in rows:
        table.add_row(*row)
    
    return table

def format_error(message: str) -> Panel:
    """Format error message.
    
    Args:
        message: Error message
        
    Returns:
        Formatted panel
    """
    return Panel(
        f"[red]Error:[/] {message}",
        border_style="red",
        title="Error"
    )

def format_success(message: str) -> Panel:
    """Format success message.
    
    Args:
        message: Success message
        
    Returns:
        Formatted panel
    """
    return Panel(
        f"[green]✓[/] {message}",
        border_style="green",
        title="Success"
    )

def format_warning(message: str) -> Panel:
    """Format warning message.
    
    Args:
        message: Warning message
        
    Returns:
        Formatted panel
    """
    return Panel(
        f"[yellow]⚠[/] {message}",
        border_style="yellow",
        title="Warning"
    )