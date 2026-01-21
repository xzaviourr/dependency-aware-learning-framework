import sys
import argparse
from pathlib import Path
from framework.visualization import DependencyGraph
from framework.test_tracker import get_tracker
from framework.project_discovery import discover_and_import_projects

# Automatically discover and import all projects
discover_and_import_projects()

def show_status(args):
    """Display the current status of all modules."""
    graph = DependencyGraph(Path.cwd())
    graph.print_status()
    
    if args.cycles:
        cycles = graph.check_cycles()
        if cycles:
            print("\n⚠️  WARNING: Circular dependencies detected!")
            for i, cycle in enumerate(cycles, 1):
                print(f"   Cycle {i}: {' → '.join(cycle + [cycle[0]])}")
        else:
            print("\n✅ No circular dependencies found.")

def reset(args):
    """Reset test results."""
    tracker = get_tracker(Path.cwd())
    
    if args.all:
        tracker.reset()
        print("✅ All test results have been reset.")
    elif args.module:
        tracker.reset_module(args.module)
        print(f"✅ Test results for '{args.module}' have been reset.")
    else:
        print("Please specify --all or --module <name>")

def next_modules(args):
    """Show suggested next modules to work on."""
    graph = DependencyGraph(Path.cwd())
    next_mods = graph.get_next_modules()
    
    if not next_mods:
        print("🎉 Congratulations! All modules are either completed or locked.")
        available = graph.get_available_modules()
        if available:
            print(f"\nYou can still work on: {', '.join(available)}")
        return
    
    print(f"\n📚 Suggested next modules ({len(next_mods)}):")
    from framework.decorators import get_module_registry
    module_registry = get_module_registry()
    
    for i, module in enumerate(next_mods[:5], 1):  # Show top 5
        info = module_registry.get(module, {})
        difficulty = info.get('difficulty', 'medium')
        description = info.get('description', '')
        print(f"\n{i}. {module} ({difficulty})")
        if description:
            print(f"   {description}")

def learning_path(args):
    """Show the recommended learning path."""
    graph = DependencyGraph(Path.cwd())
    path = graph.get_learning_path()
    
    print("\n📖 Recommended Learning Path:")
    print("="*60)
    
    for i, module in enumerate(path, 1):
        status = graph.get_module_status(module)
        status_icon = {
            'completed': '✅',
            'available': '🟧',
            'locked': '🔒'
        }[status]
        
        print(f"{i:2d}. {status_icon} {module}")
    print("="*60)

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Learning Framework - Manage your learning progress',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show module status')
    status_parser.add_argument('--cycles', action='store_true', help='Check for circular dependencies')
    status_parser.set_defaults(func=show_status)
    
    # Reset command
    reset_parser = subparsers.add_parser('reset', help='Reset test results')
    reset_parser.add_argument('--all', action='store_true', help='Reset all test results')
    reset_parser.add_argument('--module', help='Reset specific module')
    reset_parser.set_defaults(func=reset)
    
    # Next command
    next_parser = subparsers.add_parser('next', help='Show suggested next modules')
    next_parser.set_defaults(func=next_modules)
    
    # Path command
    path_parser = subparsers.add_parser('path', help='Show recommended learning path')
    path_parser.set_defaults(func=learning_path)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Execute the command
    args.func(args)
    return 0

if __name__ == '__main__':
    sys.exit(main())
