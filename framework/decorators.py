import functools
import inspect
from typing import List, Callable, Optional, Dict, Any, Set

# Global registry to store all modules and their metadata
_MODULE_REGISTRY: Dict[str, Dict[str, Any]] = {}

# Track modules that have been validated
_VALIDATED_MODULES: Set[str] = set()


def module(dependencies: Optional[List[str]] = None, difficulty: str = "medium"):
    """
    Decorator to mark a function as a learning module in the framework.
    
    Args:
        dependencies: List of function names (as strings) that this module depends on
        difficulty: Difficulty level (easy, medium, hard)
    
    Example:
        @module(dependencies=["create_database"], difficulty="easy")
        def get_user_data(user_id: int):
            # Implementation here
            pass
    """
    dependencies = [] if dependencies is None else dependencies

    def decorator_to_module(func: Callable):
        # Get module information
        module_name = func.__name__
        module_file = inspect.getfile(func)
        
        # Store module metadata in registry
        _MODULE_REGISTRY[module_name] = {
            "function": func,
            "dependencies": dependencies,
            "description": func.__doc__ or "",
            "difficulty": difficulty,
            "file": module_file,
            "qualified_name": f"{func.__module__}.{func.__name__}"
        }
        
        # Add metadata as attributes to the function
        func._is_learning_module = True
        func._module_name = module_name
        func._dependencies = dependencies
        func._difficulty = difficulty
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator_to_module

def get_module_registry() -> Dict[str, Dict[str, Any]]:
    """Return the global module registry."""
    return _MODULE_REGISTRY

def get_module_info(module_name: str) -> Optional[Dict[str, Any]]:
    """Get metadata for a specific module."""
    return _MODULE_REGISTRY.get(module_name)

def validate_all_modules_have_tests():
    """
    Validate that all registered modules have associated tests.
    Should be called after test collection.
    
    Raises:
        RuntimeError: If any module lacks a corresponding test
    """
    # Import here to avoid circular dependency
    from _pytest.config import get_config
    
    try:
        config = get_config()
        if config is None:
            # Not in pytest context, skip validation
            return
            
        # Get all collected test items
        session = getattr(config, '_session', None)
        if session is None:
            return
            
        # Find all modules that have tests
        module_with_tests = set()
        for item in session.items:
            for marker in item.iter_markers('tests_module'):
                if marker.args:
                    module_with_tests.add(marker.args[0])
        
        # Check if any registered modules lack tests
        missing_tests = []
        for module_name in _MODULE_REGISTRY.keys():
            if module_name not in module_with_tests:
                missing_tests.append(module_name)
        
        if missing_tests:
            raise RuntimeError(
                f"The following modules are missing tests:\n" +
                "\n".join(f"  - {name}" for name in sorted(missing_tests)) +
                f"\n\nEvery @module must have a corresponding test marked with "
                f"@pytest.mark.tests_module('module_name')"
            )
    except RuntimeError:
        # Some modules are missing tests, code cannot be continued
        raise
    except Exception:
        # If we can't validate (e.g., not in pytest), just skip
        pass

def get_modules_without_tests() -> List[str]:
    """
    Get list of modules that don't have associated tests.
    Used for validation and reporting.
    
    Returns:
        List of module names that lack tests
    """
    # This will be populated by conftest.py during test collection
    return list(set(_MODULE_REGISTRY.keys()) - _VALIDATED_MODULES)

def mark_module_as_tested(module_name: str):
    """Mark a module as having a test (called during test collection)."""
    _VALIDATED_MODULES.add(module_name)