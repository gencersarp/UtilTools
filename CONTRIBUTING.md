# Contributing to UtilTools

Thank you for your interest in contributing to UtilTools! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:

- A clear, descriptive title
- Steps to reproduce the bug
- Expected vs actual behavior
- System information (OS, Python version)
- Any relevant logs or error messages

### Suggesting Features

We welcome feature suggestions! Please:

- Check if the feature has already been requested
- Provide a clear use case
- Explain why this feature would be useful
- Consider submitting a PR if you can implement it

### Pull Requests

1. **Fork the repository** and create a new branch from `main`
2. **Write clear commit messages** explaining what and why
3. **Add tests** for new functionality
4. **Update documentation** as needed
5. **Ensure tests pass** before submitting
6. **Submit the PR** with a clear description

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/UtilTools.git
cd UtilTools

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .

# Run tests
python -m pytest tests/
```

## Creating a New Plugin

Plugins are the heart of UtilTools. Here's how to create one:

### 1. Choose the Right Category

- `file` - File system operations
- `text` - Text processing
- `network` - Network operations
- `system` - System monitoring
- `automation` - Automation tasks

### 2. Create Your Plugin File

Create a new file in `utiltools/plugins/` or extend an existing one:

```python
"""
My custom utilities
"""
from ..core import Plugin, register_plugin

@register_plugin(category="custom")
class MyCustomPlugin(Plugin):
    """Brief description of what this plugin does"""
    
    def execute(self, param1: str, param2: int = 0) -> dict:
        """
        Execute the plugin functionality
        
        Args:
            param1: Description of param1
            param2: Description of param2 (default: 0)
        
        Returns:
            Dictionary with results
        """
        # Your implementation here
        result = {
            "success": True,
            "data": f"Processed {param1} with {param2}"
        }
        return result
```

### 3. Add CLI Commands (Optional)

If your plugin should be accessible via CLI, add commands in `utiltools/cli.py`:

```python
@main.group()
def custom():
    """Custom operations"""
    pass

@custom.command()
@click.argument('param1')
@click.option('--param2', '-p', default=0, help='Parameter 2')
def my_command(param1, param2):
    """Execute my custom plugin"""
    pm = get_plugin_manager()
    plugin = pm.get_plugin('mycustomplugin')
    
    result = plugin.execute(param1=param1, param2=param2)
    console.print(f"[green]✓[/green] Success: {result['data']}")
```

### 4. Write Tests

Create tests in `tests/test_custom.py`:

```python
import unittest
from utiltools.core import PluginManager

class TestMyCustomPlugin(unittest.TestCase):
    def setUp(self):
        self.pm = PluginManager()
        self.pm.discover_plugins()
    
    def test_basic_functionality(self):
        plugin = self.pm.get_plugin('mycustomplugin')
        result = plugin.execute(param1="test", param2=5)
        
        self.assertTrue(result['success'])
        self.assertIn("test", result['data'])
```

### 5. Document Your Plugin

Update documentation:

- Add to plugin list in README.md
- Create examples in EXAMPLES.md
- Add docstrings to all methods

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write descriptive variable names
- Keep functions focused and small
- Comment complex logic

### Example:

```python
def process_data(input_data: List[str], filter_empty: bool = True) -> Dict[str, Any]:
    """
    Process input data and return structured results.
    
    Args:
        input_data: List of strings to process
        filter_empty: Whether to filter empty strings
    
    Returns:
        Dictionary containing processed results
    """
    if filter_empty:
        input_data = [item for item in input_data if item.strip()]
    
    return {
        "count": len(input_data),
        "items": input_data
    }
```

## Testing

We use Python's unittest framework. Tests should:

- Be isolated (use setUp/tearDown)
- Test one thing at a time
- Use descriptive test names
- Clean up resources

Run tests:

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_core.py

# Run with coverage
python -m pytest --cov=utiltools tests/
```

## Documentation

Good documentation is crucial:

- **Docstrings**: All classes and methods must have docstrings
- **Type hints**: Use type hints for parameters and return values
- **Examples**: Provide usage examples for complex features
- **README**: Keep the main README up to date

## Review Process

1. All PRs require at least one review
2. All tests must pass
3. Code coverage should not decrease
4. Documentation must be updated
5. Commit history should be clean

## Plugin Guidelines

### Best Practices

1. **Error Handling**: Always handle exceptions gracefully
   ```python
   try:
       result = risky_operation()
   except SpecificException as e:
       return {"success": False, "error": str(e)}
   ```

2. **Return Consistent Structures**: Use dictionaries with clear keys
   ```python
   return {
       "success": True,
       "data": result,
       "metadata": {"count": len(result)}
   }
   ```

3. **Validate Inputs**: Check and validate all inputs
   ```python
   if not os.path.exists(file_path):
       raise ValueError(f"File not found: {file_path}")
   ```

4. **Provide Progress Feedback**: For long operations, provide feedback
   ```python
   for i, item in enumerate(large_list):
       if i % 100 == 0:
           print(f"Processed {i}/{len(large_list)}")
   ```

5. **Resource Cleanup**: Always clean up resources
   ```python
   with open(file_path, 'r') as f:
       content = f.read()
   # File automatically closed
   ```

## Questions?

If you have questions:

- Check existing issues and discussions
- Open a new issue with the "question" label
- Reach out to maintainers

Thank you for contributing to UtilTools! 🎉
