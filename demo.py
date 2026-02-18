#!/usr/bin/env python3
"""
Demo script showing UtilTools capabilities
"""
from utiltools import PluginManager
import tempfile
import os
from pathlib import Path

def main():
    print("=" * 60)
    print("UtilTools - Comprehensive Demo")
    print("=" * 60)
    
    # Initialize plugin manager
    pm = PluginManager()
    pm.discover_plugins()
    
    print(f"\n✓ Loaded {len(pm.list_plugins())} plugins")
    print(f"  Categories: {', '.join(pm.list_categories())}")
    
    # Create temporary directory for demo
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"\n✓ Created temporary directory: {temp_dir}")
        
        # Demo 1: File operations
        print("\n" + "=" * 60)
        print("DEMO 1: File System Operations")
        print("=" * 60)
        
        # Create some test files
        for i in range(5):
            Path(temp_dir, f"file_{i}.txt").write_text(f"Content {i}")
        Path(temp_dir, f"duplicate.txt").write_text("Same content")
        Path(temp_dir, f"duplicate2.txt").write_text("Same content")
        
        print(f"\n✓ Created test files")
        
        # Search for files
        file_search = pm.get_plugin('filesearchplugin')
        results = file_search.execute(path=temp_dir, pattern="*.txt", recursive=False)
        print(f"\n✓ Found {len(results)} text files")
        
        # Find duplicates
        dup_finder = pm.get_plugin('duplicatefinderplugin')
        duplicates = dup_finder.execute(path=temp_dir, recursive=False)
        print(f"✓ Found {len(duplicates)} sets of duplicate files")
        
        # Demo 2: Text processing
        print("\n" + "=" * 60)
        print("DEMO 2: Text Processing")
        print("=" * 60)
        
        test_file = Path(temp_dir, "test.txt")
        test_file.write_text("Hello world, this is a test file.")
        
        # Search and replace
        text_replace = pm.get_plugin('textsearchreplaceplugin')
        result = text_replace.execute(
            str(test_file),
            search="test",
            replace="demo",
            dry_run=False
        )
        print(f"\n✓ Replaced {result['matches']} occurrences")
        print(f"  New content: {test_file.read_text()}")
        
        # Demo 3: System monitoring
        print("\n" + "=" * 60)
        print("DEMO 3: System Monitoring")
        print("=" * 60)
        
        sys_info = pm.get_plugin('systeminfoplugin')
        info = sys_info.execute()
        
        print(f"\n✓ System Information:")
        print(f"  Platform: {info['platform']['system']} {info['platform']['release']}")
        print(f"  CPU Cores: {info['cpu']['physical_cores']} physical, {info['cpu']['logical_cores']} logical")
        print(f"  CPU Usage: {info['cpu']['usage_percent']}%")
        print(f"  Memory Usage: {info['memory']['percent']}%")
        print(f"  Disk Usage: {info['disk']['percent']}%")
        
        # Demo 4: Network utilities
        print("\n" + "=" * 60)
        print("DEMO 4: Network Utilities")
        print("=" * 60)
        
        # URL validation
        url_validator = pm.get_plugin('urlvalidatorplugin')
        result = url_validator.execute("https://github.com", check_reachable=False)
        print(f"\n✓ URL Validation:")
        print(f"  Valid: {result['valid']}")
        print(f"  Scheme: {result['scheme']}")
        print(f"  Domain: {result['netloc']}")
        
        # Demo 5: Automation
        print("\n" + "=" * 60)
        print("DEMO 5: Workflow Automation")
        print("=" * 60)
        
        workflow = pm.get_plugin('workflowplugin')
        workflow_steps = [
            {
                'plugin': 'filesearchplugin',
                'args': {
                    'path': temp_dir,
                    'pattern': '*.txt',
                    'recursive': False
                }
            }
        ]
        
        result = workflow.execute(workflow=workflow_steps, stop_on_error=True)
        print(f"\n✓ Workflow Execution:")
        print(f"  Total steps: {result['total_steps']}")
        print(f"  Successful: {result['successful_steps']}")
        print(f"  Failed: {result['failed_steps']}")
    
    print("\n" + "=" * 60)
    print("Demo completed successfully!")
    print("=" * 60)
    print("\nTry the CLI: utiltools --help")

if __name__ == '__main__':
    main()
