from datetime import datetime
from typing import Optional, List
from pathlib import Path
import networkx as nx
from framework.decorators import get_module_registry
from framework.test_tracker import get_tracker


class DependencyGraph:
    """Builds and visualizes the dependency graph for learning modules."""
    
    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize the dependency graph.
        
        Args:
            project_root: Root directory of the project
        """
        self.project_root = project_root or Path.cwd()
        self.tracker = get_tracker(project_root)
        self.graph = nx.DiGraph()
        self._build_graph()
    
    def _build_graph(self):
        """Build the dependency graph from the module registry."""
        module_registry = get_module_registry()
        
        # Add all modules as nodes
        for module_name, module_info in module_registry.items():
            self.graph.add_node(
                module_name,
                description=module_info.get('description', ''),
                difficulty=module_info.get('difficulty', 'medium'),
                file=module_info.get('file', '')
            )
        
        # Add edges for dependencies
        for module_name, module_info in module_registry.items():
            for dependency in module_info.get('dependencies', []):
                if dependency in module_registry:
                    # Edge goes FROM dependency TO module (dependency -> module)
                    self.graph.add_edge(dependency, module_name)
    
    def get_module_status(self, module_name: str) -> str:
        """
        Determine the status of a module.
        
        Returns:
            'completed': Module test has passed (GREEN)
            'available': Dependencies met, can be attempted (ORANGE)
            'locked': Dependencies not met (RED)
        """
        # Check if module test has passed
        if self.tracker.is_passed(module_name):
            return 'completed'
        
        # Check if all dependencies are satisfied
        module_registry = get_module_registry()
        if module_name not in module_registry:
            return 'locked'
        
        dependencies = module_registry[module_name].get('dependencies', [])
        
        # Check if all dependencies have passed
        for dep in dependencies:
            if not self.tracker.is_passed(dep):
                return 'locked'
        
        return 'available'
    
    def get_available_modules(self) -> List[str]:
        """Get list of modules that can be attempted now (dependencies met)."""
        return [
            module for module in self.graph.nodes()
            if self.get_module_status(module) == 'available'
        ]
    
    def get_completed_modules(self) -> List[str]:
        """Get list of modules that have been completed."""
        return [
            module for module in self.graph.nodes()
            if self.get_module_status(module) == 'completed'
        ]
    
    def get_locked_modules(self) -> List[str]:
        """Get list of modules that are locked (dependencies not met)."""
        return [
            module for module in self.graph.nodes()
            if self.get_module_status(module) == 'locked'
        ]
    
    def get_next_modules(self) -> List[str]:
        """Get suggested next modules to work on (available, sorted by difficulty)."""
        available = self.get_available_modules()
        module_registry = get_module_registry()
        
        # Sort by difficulty: easy first, then medium, then hard
        difficulty_order = {'easy': 0, 'medium': 1, 'hard': 2}
        
        return sorted(
            available,
            key=lambda m: difficulty_order.get(
                module_registry[m].get('difficulty', 'medium'), 1
            )
        )
    
    def visualize(self, output_file: Optional[Path] = None) -> Optional[Path]:
        """
        Create a visual representation of the dependency graph in Markdown.
        
        Args:
            output_file: Path to save the visualization. If None, auto-detects project directory
            
        Returns:
            Path to the generated visualization file
        """
        # Determine output path
        if output_file is None:
            # Auto-detect project directory from module files
            output_file = self._get_project_progress_path()
        else:
            output_file = Path(output_file)
            if not output_file.suffix:
                output_file = output_file.with_suffix('.md')
        
        # Generate markdown content
        markdown = self._generate_markdown()
        
        # Ensure output directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Write to file
        with open(output_file, 'w') as f:
            f.write(markdown)
        
        return output_file
    
    def _get_project_progress_path(self) -> Path:
        """Determine the project directory path for progress.md."""
        module_registry = get_module_registry()
        
        if not module_registry:
            return self.project_root / 'progress.md'
        
        # Get the first module's file path to determine project directory
        for _, module_info in module_registry.items():
            file_path = Path(module_info.get('file', ''))
            
            # Look for 'projects/<project_name>' pattern
            try:
                if 'projects' in file_path.parts:
                    projects_idx = file_path.parts.index('projects')
                    # Get path up to projects/<project_name>/
                    if len(file_path.parts) > projects_idx + 1:
                        project_name = file_path.parts[projects_idx + 1]
                        project_dir = self.project_root / 'projects' / project_name
                        return project_dir / 'progress.md'
            except (ValueError, IndexError):
                pass
        
        # Fallback to project root if pattern not found
        return self.project_root / 'progress.md'
    
    def _generate_markdown(self) -> str:
        """Generate markdown content for the dependency graph."""
        module_registry = get_module_registry()
        
        # Group modules by their file/folder
        modules_by_folder = {}
        for module_name, module_info in module_registry.items():
            file_path = Path(module_info.get('file', ''))
            
            # Extract folder structure from file path
            try:
                # Get path relative to project root
                if 'projects' in file_path.parts:
                    projects_idx = file_path.parts.index('projects')
                    # Skip 'projects' and project name, get the actual module folder
                    if len(file_path.parts) > projects_idx + 2:
                        # Use the file name (without .py) as category
                        folder = file_path.stem  # e.g., 'database', 'similarity', 'api'
                    else:
                        folder = "main"
                else:
                    folder = "main"
            except (ValueError, IndexError):
                folder = "main"
            
            if folder not in modules_by_folder:
                modules_by_folder[folder] = []
            
            modules_by_folder[folder].append({
                'name': module_name,
                'info': module_info,
                'status': self.get_module_status(module_name)
            })
        
        # Build markdown
        lines = []
        lines.append("# 📚 Learning Framework Progress\n")
        
        # Overall progress
        completed = self.get_completed_modules()
        total = len(self.graph.nodes())
        progress_pct = (len(completed) / total * 100) if total > 0 else 0
        
        lines.append(f"**Overall Progress:** {len(completed)}/{total} modules completed ({progress_pct:.1f}%)\n")
        lines.append(f"**Last Updated:** {self._get_timestamp()}\n")
        
        # Progress bar
        bar_length = 30
        filled = int(bar_length * progress_pct / 100)
        bar = '█' * filled + '░' * (bar_length - filled)
        lines.append(f"```\n{bar} {progress_pct:.1f}%\n```\n")
        
        # Legend
        lines.append("## Legend\n")
        lines.append("- 🟢 **Completed** - Test passed, module is complete\n")
        lines.append("- 🟧 **Available** - Dependencies met, ready to implement\n")
        lines.append("- 🔴 **Locked** - Dependencies not met yet\n")
        
        # Modules by folder
        for folder in sorted(modules_by_folder.keys()):
            modules = modules_by_folder[folder]
            
            # Folder header
            lines.append(f"\n## 📁 {folder.replace('_', ' ').title()}\n")
            
            # Count statuses in this folder
            folder_stats = {'completed': 0, 'available': 0, 'locked': 0}
            for mod in modules:
                folder_stats[mod['status']] += 1
            
            lines.append(f"*Completed: {folder_stats['completed']}, Available: {folder_stats['available']}, Locked: {folder_stats['locked']}*\n")
            
            # Module table
            lines.append("\n| Status | Module | Difficulty | Dependencies |\n")
            lines.append("|--------|--------|------------|-------------|\n")
            
            # Sort by status (completed first, then available, then locked)
            status_order = {'completed': 0, 'available': 1, 'locked': 2}
            sorted_modules = sorted(modules, key=lambda m: (status_order[m['status']], m['name']))
            
            for mod in sorted_modules:
                status_icon = {'completed': '🟢', 'available': '🟧', 'locked': '🔴'}[mod['status']]
                difficulty = mod['info'].get('difficulty', 'medium')
                dependencies = mod['info'].get('dependencies', [])
                deps_str = ', '.join(dependencies) if dependencies else 'None'
                
                # Truncate long dependency lists
                if len(deps_str) > 40:
                    deps_str = deps_str[:37] + '...'
                
                lines.append(f"| {status_icon} | `{mod['name']}` | {difficulty} | {deps_str} |\n")
        
        # Dependency graph section
        lines.append("\n## 🔗 Dependency Graph\n")
        lines.append("\n```mermaid\n")
        lines.append("graph TD\n")
        
        # Add nodes with colors
        for module_name in self.graph.nodes():
            status = self.get_module_status(module_name)
            # Mermaid color styling
            style_class = {'completed': 'completed', 'available': 'available', 'locked': 'locked'}[status]
            lines.append(f"    {module_name}[{module_name}]:::{style_class}\n")
        
        # Add edges
        for source, target in self.graph.edges():
            lines.append(f"    {source} --> {target}\n")
        
        # Add styling
        lines.append("\n    classDef completed fill:#90EE90,stroke:#333,stroke-width:2px\n")
        lines.append("    classDef available fill:#FFB366,stroke:#333,stroke-width:2px\n")
        lines.append("    classDef locked fill:#FFB6C1,stroke:#333,stroke-width:2px\n")
        lines.append("```\n")
        
        # Next steps
        next_modules = self.get_next_modules()
        if next_modules:
            lines.append("\n## 🎯 Suggested Next Steps\n")
            for i, module in enumerate(next_modules[:5], 1):
                module_info = module_registry[module]
                difficulty = module_info.get('difficulty', 'medium')
                description = module_info.get('description', '').split('\n')[0]  # First line
                lines.append(f"{i}. **`{module}`** ({difficulty})")
                if description:
                    lines.append(f" - {description}")
                lines.append("\n")
        
        return ''.join(lines)
    
    def _get_timestamp(self) -> str:
        """Get current timestamp as string."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def print_status(self):
        """Print a text-based status summary."""
        print("\n" + "="*60)
        print("LEARNING FRAMEWORK - MODULE STATUS")
        print("="*60)
        
        completed = self.get_completed_modules()
        available = self.get_available_modules()
        locked = self.get_locked_modules()
        
        total = len(self.graph.nodes())
        completed_count = len(completed)
        progress = (completed_count / total * 100) if total > 0 else 0
        
        print(f"\nProgress: {completed_count}/{total} modules completed ({progress:.1f}%)")
        
        if completed:
            print(f"\n✅ COMPLETED ({len(completed)}):")
            for module in sorted(completed):
                print(f"   • {module}")
        
        if available:
            print(f"\n🟧 AVAILABLE - Ready to implement ({len(available)}):")
            next_modules = self.get_next_modules()
            for module in next_modules:
                module_registry = get_module_registry()
                difficulty = module_registry[module].get('difficulty', 'medium')
                description = module_registry[module].get('description', '')
                print(f"   • {module} ({difficulty})")
                if description:
                    print(f"     {description}")
        
        if locked:
            print(f"\n🔒 LOCKED - Dependencies not met ({len(locked)}):")
            for module in sorted(locked):
                module_registry = get_module_registry()
                deps = module_registry[module].get('dependencies', [])
                unmet = [d for d in deps if not self.tracker.is_passed(d)]
                if unmet:
                    print(f"   • {module} (needs: {', '.join(unmet)})")
        
        print("\n" + "="*60 + "\n")
    
    def get_learning_path(self) -> List[str]:
        """
        Get a recommended learning path (topological sort of the DAG).
        
        Returns:
            List of module names in recommended order
        """
        try:
            return list(nx.topological_sort(self.graph))
        except nx.NetworkXError:
            # Graph has cycles, return best effort
            return list(self.graph.nodes())
    
    def check_cycles(self) -> List[List[str]]:
        """
        Check for circular dependencies.
        
        Returns:
            List of cycles found (empty if no cycles)
        """
        try:
            cycles = list(nx.simple_cycles(self.graph))
            return cycles
        except:
            return []


def create_progress_visualization(project_root: Optional[Path] = None) -> Optional[Path]:
    """
    Convenience function to create the progress markdown file.
    
    Args:
        project_root: Root directory of the project
        
    Returns:
        Path to the generated progress.md file
    """
    graph = DependencyGraph(project_root)
    graph.print_status()
    return graph.visualize()
