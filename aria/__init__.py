"""
ARIA Framework

A framework for managing AI participation in software projects.

Copyright 2024 ARIA Team
Licensed under the Apache License, Version 2.0
"""

from aria.core.policy import (
    AIAction,
    AIPolicy,
    PathPolicy,
    PolicyEffect,
    PolicyModel,
    PolicyStatement,
    PolicyManager
)

__version__ = "0.1.0"

__all__ = [
    'AIAction',
    'AIPolicy',
    'PathPolicy',
    'PolicyEffect',
    'PolicyModel',
    'PolicyStatement',
    'PolicyManager',
    '__version__'
]