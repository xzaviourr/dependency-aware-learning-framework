import sys
import importlib
from pathlib import Path
from typing import List

def discover_and_import_projects(root_path: Path = None) -> List[str]:
    """
    Automatically discover and import all projects in the projects/ folder.
    
    Args:
        root_path: Root path of the framework. Defaults to current working directory.
        
    Returns:
        List of project names that were imported
    """
    if root_path is None:
        root_path = Path.cwd()
    
    projects_dir = root_path / "projects"
    if not projects_dir.exists():
        return []
    
    # Add root to sys.path if not already there
    root_str = str(root_path)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)
    
    imported_projects = []
    
    # Iterate through each project directory
    for project_dir in projects_dir.iterdir():
        if not project_dir.is_dir():
            continue
        
        # Skip special directories
        if project_dir.name.startswith('.') or project_dir.name == '__pycache__':
            continue
        
        project_name = project_dir.name
        
        try:
            # Import all Python modules in the project
            for module_file in project_dir.rglob("*.py"):
                # Skip test files and special files
                if module_file.name.startswith('test_') or module_file.name.startswith('_'):
                    continue
                
                # Skip files in tests directory
                if 'tests' in module_file.parts:
                    continue
                
                # Convert file path to module path
                relative_path = module_file.relative_to(root_path)
                module_parts = list(relative_path.parts[:-1]) + [relative_path.stem]
                module_name = '.'.join(module_parts)
                
                try:
                    importlib.import_module(module_name)
                except ImportError as e:
                    # Some modules might have import errors, that's okay
                    pass
            
            imported_projects.append(project_name)
            
        except Exception as e:
            # If a project fails to import, continue with others
            pass
    
    return imported_projects

def get_project_modules(project_name: str, root_path: Path = None) -> List[Path]:
    """
    Get all Python module files for a specific project.
    
    Args:
        project_name: Name of the project
        root_path: Root path of the framework
        
    Returns:
        List of Python file paths in the project
    """
    if root_path is None:
        root_path = Path.cwd()
    
    project_dir = root_path / "projects" / project_name
    if not project_dir.exists():
        return []
    
    modules = []
    for module_file in project_dir.rglob("*.py"):
        # Skip test files and special files
        if module_file.name.startswith('test_') or module_file.name.startswith('_'):
            continue
        
        # Skip files in tests directory
        if 'tests' in module_file.parts:
            continue
        
        modules.append(module_file)
    
    return modules
