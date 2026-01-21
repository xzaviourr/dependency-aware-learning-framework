"""
Learning Framework - Educational project-based learning with dependency tracking.
"""

from framework.decorators import (
    module, 
    get_module_registry, 
    get_module_info,
    get_modules_without_tests,
    mark_module_as_tested
)
from framework.test_tracker import TestTracker, get_tracker
from framework.visualization import DependencyGraph, create_progress_visualization
from framework.project_discovery import discover_and_import_projects

__version__ = "0.1.0"

__all__ = [
    'module',
    'get_module_registry',
    'get_module_info',
    'get_modules_without_tests',
    'mark_module_as_tested',
    'TestTracker',
    'get_tracker',
    'DependencyGraph',
    'create_progress_visualization',
    'discover_and_import_projects',
]
