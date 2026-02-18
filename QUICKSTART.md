# Quick Start Guide

Get started with UtilTools in minutes!

## Installation

```bash
# Clone the repository
git clone https://github.com/gencersarp/UtilTools.git
cd UtilTools

# Install
pip install -e .
```

## First Steps

### 1. Verify Installation

```bash
utiltools --version
utiltools --help
```

### 2. List Available Plugins

```bash
utiltools list-plugins
```

### 3. Try Basic Commands

#### Get System Information

```bash
utiltools system info
```

#### Search for Files

```bash
# Search for Python files
utiltools file search --path . --pattern "*.py"

# Search for files containing specific text
utiltools file search --path . --pattern "*.txt" --content "TODO"
```

#### Monitor Processes

```bash
utiltools system processes --limit 10
```

#### Network Operations

```bash
# Validate a URL
utiltools network validate-url https://github.com --check-reachable

# Scan ports
utiltools network scan-ports localhost --ports 80,443,22
```

## Quick Examples

### Example 1: Find and Backup Important Files

```bash
# Find all Python files
utiltools file search --path ./project --pattern "*.py" > files.txt

# Create a backup archive
utiltools file compress ./project project_backup.tar.gz --format tar.gz
```

### Example 2: Clean Up Duplicates

```bash
# Find duplicate files
utiltools file find-duplicates --path ~/Downloads
```

### Example 3: Process JSON Data

```bash
# Prettify JSON
utiltools text json-process data.json --action prettify --output formatted.json

# Query JSON data
utiltools text json-process data.json --action query --query "users.0.name"
```

### Example 4: Monitor System Resources

```bash
# Get disk usage
utiltools system disk --path /home --action usage

# Find large files
utiltools system disk --path /home --action large_files
```

## Using as a Python Library

```python
from utiltools import PluginManager

# Initialize
pm = PluginManager()
pm.discover_plugins()

# Use a plugin
file_search = pm.get_plugin('filesearchplugin')
results = file_search.execute(path='.', pattern='*.py', recursive=True)

for file_path in results:
    print(file_path)
```

## Creating Your First Plugin

```python
# myplugin.py
from utiltools.core import Plugin, register_plugin

@register_plugin(category="custom")
class MyPlugin(Plugin):
    """My custom utility"""
    
    def execute(self, name: str):
        return f"Hello, {name}!"

# Save in utiltools/plugins/
```

## Configuration

```bash
# View configuration
utiltools config show

# Set a value
utiltools config set logging.level DEBUG

# Get a value
utiltools config get logging.level
```

## Next Steps

- Read [EXAMPLES.md](EXAMPLES.md) for detailed examples
- Check [CONTRIBUTING.md](CONTRIBUTING.md) to add your own plugins
- Explore the full [README.md](README.md) for all features

## Common Use Cases

### Automated Backups
```bash
utiltools file compress ~/Documents backup_$(date +%Y%m%d).tar.gz --format tar.gz
```

### Code Analysis
```bash
utiltools file search --path ./src --pattern "*.py" --content "TODO" > todos.txt
```

### System Monitoring
```bash
watch -n 5 utiltools system info
```

### Batch File Operations
```python
from utiltools import PluginManager

pm = PluginManager()
pm.discover_plugins()

batch = pm.get_plugin('batchoperationplugin')
batch.execute(
    operation='copy',
    files=['file1.txt', 'file2.txt'],
    destination='/backup'
)
```

## Getting Help

- Run any command with `--help` flag
- Check the documentation in the docs/ folder
- Open an issue on GitHub for bugs or questions

Happy automating! 🚀
