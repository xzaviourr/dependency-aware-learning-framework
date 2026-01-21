"""
Pytest configuration and hooks for the learning framework.
This enforces dependency checking before running tests.
"""
import pytest
from pathlib import Path
from framework.decorators import get_module_registry, mark_module_as_tested
from framework.test_tracker import get_tracker
from framework.project_discovery import discover_and_import_projects

def pytest_configure(config):
    """Initialize the learning framework when pytest starts."""
    # Register custom marker
    config.addinivalue_line(
        "markers",
        "tests_module(name): mark test as testing a specific learning module"
    )
    
    # Get project root
    project_root = Path(config.rootdir)
    
    # Automatically discover and import all projects
    discover_and_import_projects(project_root)
    
    # Initialize tracker
    global tracker
    tracker = get_tracker(project_root)
    
    # Store in config for access in other hooks
    config.tracker = tracker

def pytest_collection_modifyitems(config, items):
    """
    Modify test collection to add dependency information.
    This runs after all tests are collected but before they run.
    """
    tracker = getattr(config, 'tracker', None)
    if tracker is None:
        return
    
    module_registry = get_module_registry()
    
    # Track which modules have tests
    modules_with_tests = set()
    
    # Map test items to their corresponding modules
    for item in items:
        # Try to extract module name from test function name
        # Convention: test_<module_name> or test_<module_name>_*
        test_name = item.name
        
        # Store original test for potential dependency checking
        if hasattr(item, 'function'):
            # Check if the test function has a marker indicating which module it tests
            module_name = None
            
            # Look for @pytest.mark.tests_module("module_name") marker
            for marker in item.iter_markers('tests_module'):
                if marker.args:
                    module_name = marker.args[0]
                    break
            
            # If no marker, try to infer from test name
            if module_name is None and test_name.startswith('test_'):
                # Remove 'test_' prefix and any trailing parts after another underscore
                potential_name = test_name[5:]  # Remove 'test_'
                if potential_name in module_registry:
                    module_name = potential_name
            
            if module_name:
                item._learning_module_name = module_name
                modules_with_tests.add(module_name)
                mark_module_as_tested(module_name)
    
    # Validate that all modules have tests
    missing_tests = []
    for module_name in module_registry.keys():
        if module_name not in modules_with_tests:
            missing_tests.append(module_name)
    
    if missing_tests:
        # Fail the test collection with clear error message
        raise pytest.UsageError(
            f"\n{'='*70}\n"
            f"ERROR: The following modules are missing tests:\n\n" +
            "\n".join(f"  ❌ {name}" for name in sorted(missing_tests)) +
            f"\n\nEvery function decorated with @module must have a corresponding test\n"
            f"marked with @pytest.mark.tests_module('module_name')\n"
            f"\nExample:\n"
            f"  @pytest.mark.tests_module('{missing_tests[0]}')\n"
            f"  def test_{missing_tests[0]}():\n"
            f"      # Test implementation\n"
            f"      pass\n"
            f"{'='*70}"
        )

def pytest_runtest_setup(item):
    """
    Run before each test to check if dependencies are met.
    Skip test if dependencies haven't passed.
    """
    module_name = getattr(item, '_learning_module_name', None)
    if module_name is None:
        return  # Not a learning framework test
    
    tracker = item.config.tracker
    module_registry = get_module_registry()
    
    if module_name not in module_registry:
        return  # Module not in registry, let test run normally
    
    module_info = module_registry[module_name]
    dependencies = module_info.get('dependencies', [])
    
    # Check if all dependencies have passed
    unmet_dependencies = []
    for dep in dependencies:
        if not tracker.is_passed(dep):
            unmet_dependencies.append(dep)
    
    if unmet_dependencies:
        pytest.skip(
            f"Dependencies not met for '{module_name}': {', '.join(unmet_dependencies)}\n"
            f"Please complete and pass tests for these modules first."
        )

def pytest_runtest_makereport(item, call):
    """
    Create test report and track results.
    Called after test execution to create the report.
    """
    # This is called for setup, call, and teardown phases
    # We only care about the 'call' phase (actual test execution)
    if call.when != "call":
        return
    
    module_name = getattr(item, '_learning_module_name', None)
    if module_name is None:
        return
    
    tracker = item.config.tracker
    
    # Check test outcome
    if call.excinfo is None:
        # Test passed
        test_file = str(item.fspath)
        tracker.mark_passed(module_name, test_file)
    else:
        # Test failed
        error_msg = str(call.excinfo.value) if call.excinfo else "Unknown error"
        test_file = str(item.fspath)
        tracker.mark_failed(module_name, error_msg, test_file)

@pytest.fixture
def learning_tracker():
    """Fixture to provide access to the test tracker in tests."""
    return tracker if 'tracker' in globals() else get_tracker()

def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test session finishes.
    Update the progress.md file with latest results.
    """
    from framework.visualization import DependencyGraph
    from pathlib import Path
    
    try:
        project_root = Path(session.config.rootdir)
        graph = DependencyGraph(project_root)
        progress_file = graph.visualize()
        
        if progress_file:
            # Show relative path from project root
            try:
                rel_path = progress_file.relative_to(project_root)
                print(f"\n✅ Progress updated: {rel_path}")
            except ValueError:
                print(f"\n✅ Progress updated: {progress_file}")
    except Exception:
        # Don't fail the test session if visualization fails
        pass
