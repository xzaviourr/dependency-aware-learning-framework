import json
from pathlib import Path
from typing import Dict, Set, Optional
from datetime import datetime


class TestTracker:
    """Manages test results and completion status for learning modules."""
    
    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize the test tracker.
        
        Args:
            project_root: Root directory of the project. If None, uses current directory.
        """
        if project_root is None:
            project_root = Path.cwd()
        self.project_root = Path(project_root)
        self.results_file = self.project_root / ".learning_framework" / "test_results.json"
        self._ensure_results_directory()
        self._results: Dict[str, Dict] = self._load_results()
    
    def _ensure_results_directory(self):
        """Create the results directory if it doesn't exist."""
        self.results_file.parent.mkdir(parents=True, exist_ok=True)
    
    def _load_results(self) -> Dict[str, Dict]:
        """Load test results from the JSON file."""
        if self.results_file.exists():
            try:
                with open(self.results_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def _save_results(self):
        """Save test results to the JSON file."""
        with open(self.results_file, 'w') as f:
            json.dump(self._results, f, indent=2)
    
    def mark_passed(self, module_name: str, test_file: str = ""):
        """
        Mark a module test as passed.
        
        Args:
            module_name: Name of the module
            test_file: Path to the test file
        """
        self._results[module_name] = {
            "status": "passed",
            "timestamp": datetime.now().isoformat(),
            "test_file": test_file
        }
        self._save_results()
    
    def mark_failed(self, module_name: str, error_message: str = "", test_file: str = ""):
        """
        Mark a module test as failed.
        
        Args:
            module_name: Name of the module
            error_message: Error message from the test
            test_file: Path to the test file
        """
        self._results[module_name] = {
            "status": "failed",
            "timestamp": datetime.now().isoformat(),
            "test_file": test_file,
            "error": error_message
        }
        self._save_results()
    
    def is_passed(self, module_name: str) -> bool:
        """
        Check if a module test has passed.
        
        Args:
            module_name: Name of the module
            
        Returns:
            True if the module test has passed, False otherwise
        """
        return self._results.get(module_name, {}).get("status") == "passed"
    
    def get_passed_modules(self) -> Set[str]:
        """Get set of all modules that have passed their tests."""
        return {
            name for name, data in self._results.items()
            if data.get("status") == "passed"
        }
    
    def get_failed_modules(self) -> Set[str]:
        """Get set of all modules that have failed their tests."""
        return {
            name for name, data in self._results.items()
            if data.get("status") == "failed"
        }
    
    def get_module_status(self, module_name: str) -> Optional[str]:
        """
        Get the status of a module.
        
        Args:
            module_name: Name of the module
            
        Returns:
            'passed', 'failed', or None if not tested yet
        """
        return self._results.get(module_name, {}).get("status")
    
    def get_all_results(self) -> Dict[str, Dict]:
        """Get all test results."""
        return self._results.copy()
    
    def reset(self):
        """Clear all test results."""
        self._results = {}
        self._save_results()
    
    def reset_module(self, module_name: str):
        """
        Reset test results for a specific module.
        
        Args:
            module_name: Name of the module to reset
        """
        if module_name in self._results:
            del self._results[module_name]
            self._save_results()

# Global instance for easy access
_global_tracker: Optional[TestTracker] = None

def get_tracker(project_root: Optional[Path] = None) -> TestTracker:
    """
    Get the global test tracker instance.
    
    Args:
        project_root: Root directory of the project
        
    Returns:
        TestTracker instance
    """
    global _global_tracker
    if _global_tracker is None:
        _global_tracker = TestTracker(project_root)
    return _global_tracker
