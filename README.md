# UtilTools 🛠️

A comprehensive, plugin-based utility toolkit for automation and productivity. UtilTools provides a powerful collection of utilities for file operations, text processing, network tasks, system monitoring, and automation - all accessible through an intuitive command-line interface.

## ✨ Features

### 🗂️ File System Utilities
- **File Search**: Search files by name patterns or content
- **Batch Rename**: Rename multiple files with pattern replacement
- **Compression**: Create and extract ZIP, TAR, and TAR.GZ archives
- **Duplicate Finder**: Find duplicate files based on content hash
- **Directory Sync**: Synchronize directories with smart copying

### 📝 Text Processing
- **Search & Replace**: Find and replace text with regex support
- **Text Formatter**: Convert case, trim whitespace, normalize line endings
- **CSV Processor**: Filter, transform, and analyze CSV files
- **JSON Processor**: Prettify, minify, query, and validate JSON files
- **Regex Tool**: Test and apply regular expressions

### 🌐 Network Utilities
- **Port Scanner**: Scan network ports on any host
- **URL Validator**: Validate and parse URLs with reachability checks
- **HTTP Client**: Make HTTP requests with custom headers and data
- **Download Manager**: Download files from URLs with progress tracking
- **DNS Lookup**: Perform forward and reverse DNS lookups

### 💻 System Monitoring
- **System Info**: Get comprehensive system information (CPU, memory, disk)
- **Process Monitor**: List, monitor, and manage system processes
- **Disk Analyzer**: Analyze disk usage and find large files
- **Network Monitor**: Monitor network connections and statistics

### 🤖 Automation
- **Task Scheduler**: Schedule tasks to run automatically
- **File Watcher**: Watch files/directories for changes
- **Batch Operations**: Execute operations on multiple files
- **Workflow Engine**: Create and execute multi-step workflows

### 🔌 Plugin Architecture
- Extensible plugin system for adding custom utilities
- Auto-discovery of plugins
- Category-based organization
- Easy integration of third-party plugins

## 🚀 Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/gencersarp/UtilTools.git
cd UtilTools

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Using pip (when published)

```bash
pip install utiltools
```

## 📖 Usage

### Command-Line Interface

UtilTools provides a comprehensive CLI with intuitive commands:

```bash
# List all available plugins
utiltools list-plugins

# File operations
utiltools file search --path . --pattern "*.py" --content "TODO"
utiltools file compress source_dir output.zip --format zip
utiltools file extract archive.zip destination/
utiltools file find-duplicates --path /home/user/Documents

# Text processing
utiltools text replace file.txt --search "old" --replace "new" --dry-run
utiltools text json-process data.json --action prettify --output formatted.json

# Network operations
utiltools network scan-ports example.com --ports 80,443,8080
utiltools network validate-url https://example.com --check-reachable
utiltools network download https://example.com/file.zip --output local.zip

# System monitoring
utiltools system info
utiltools system processes --sort-by memory --limit 10
utiltools system disk --path /home --action large_files

# Configuration
utiltools config set logging.level DEBUG
utiltools config get logging.level
utiltools config show
```

### Python API

You can also use UtilTools as a Python library:

```python
from utiltools import PluginManager, get_config

# Initialize plugin manager
pm = PluginManager()
pm.discover_plugins()

# Use file search plugin
file_search = pm.get_plugin('filesearchplugin')
results = file_search.execute(path='/home/user', pattern='*.txt', recursive=True)

# Use system info plugin
system_info = pm.get_plugin('systeminfoplugin')
info = system_info.execute()
print(f"CPU Usage: {info['cpu']['usage_percent']}%")

# Configure UtilTools
config = get_config()
config.set('network.timeout', 60)
config.save()
```

### Creating Custom Plugins

Extend UtilTools with your own plugins:

```python
from utiltools.core import Plugin, register_plugin

@register_plugin(category="custom")
class MyCustomPlugin(Plugin):
    """My custom utility plugin"""
    
    def execute(self, **kwargs):
        """Execute plugin functionality"""
        # Your custom logic here
        return {"success": True, "message": "Custom operation completed"}
```

## 🏗️ Project Structure

```
UtilTools/
├── utiltools/
│   ├── __init__.py          # Package initialization
│   ├── core.py              # Plugin system core
│   ├── config.py            # Configuration management
│   ├── cli.py               # Command-line interface
│   └── plugins/
│       ├── file_utils.py    # File system plugins
│       ├── text_utils.py    # Text processing plugins
│       ├── network_utils.py # Network plugins
│       ├── system_utils.py  # System monitoring plugins
│       └── automation_utils.py # Automation plugins
├── tests/                   # Test suite
├── setup.py                 # Package setup
├── requirements.txt         # Dependencies
└── README.md               # Documentation
```

## 🧪 Available Plugins

### File System (Category: file)
- `FileSearchPlugin` - Search files by name or content
- `BatchRenamePlugin` - Batch rename files
- `CompressionPlugin` - Compress and extract archives
- `DuplicateFinderPlugin` - Find duplicate files
- `DirectorySyncPlugin` - Synchronize directories

### Text Processing (Category: text)
- `TextSearchReplacePlugin` - Search and replace in files
- `TextFormatterPlugin` - Format text files
- `CSVProcessorPlugin` - Process CSV files
- `JSONProcessorPlugin` - Process JSON files
- `RegexToolPlugin` - Work with regular expressions

### Network (Category: network)
- `PortScannerPlugin` - Scan network ports
- `URLValidatorPlugin` - Validate and parse URLs
- `HTTPRequestPlugin` - Make HTTP requests
- `DownloadManagerPlugin` - Download files
- `DNSLookupPlugin` - DNS lookups

### System (Category: system)
- `SystemInfoPlugin` - Get system information
- `ProcessMonitorPlugin` - Monitor processes
- `DiskAnalyzerPlugin` - Analyze disk usage
- `NetworkMonitorPlugin` - Monitor network activity

### Automation (Category: automation)
- `TaskSchedulerPlugin` - Schedule automated tasks
- `FileWatcherPlugin` - Watch for file changes
- `BatchOperationPlugin` - Batch file operations
- `WorkflowPlugin` - Execute multi-step workflows

## 📋 Requirements

- Python 3.7+
- click >= 8.0.0
- colorama >= 0.4.4
- requests >= 2.26.0
- psutil >= 5.8.0
- pyyaml >= 5.4.1
- watchdog >= 2.1.0
- schedule >= 1.1.0
- rich >= 10.0.0

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Adding New Plugins

To add a new plugin:

1. Create a new file in `utiltools/plugins/`
2. Import the base classes: `from utiltools.core import Plugin, register_plugin`
3. Define your plugin class with the `@register_plugin()` decorator
4. Implement the `execute()` method
5. Add CLI commands in `cli.py` if needed

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [Click](https://click.palletsprojects.com/) for CLI
- UI powered by [Rich](https://rich.readthedocs.io/)
- System monitoring via [psutil](https://github.com/giampaolo/psutil)
- File watching with [watchdog](https://github.com/gorakhargosh/watchdog)

## 📧 Contact

For questions, issues, or suggestions, please open an issue on GitHub.

---

Made with ❤️ by UtilTools Contributors
