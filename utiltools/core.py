"""
Core plugin system for UtilTools
"""
import importlib
import inspect
import os
from typing import Dict, List, Any, Callable
from pathlib import Path


class Plugin:
    """Base class for all plugins"""
    
    def __init__(self):
        self.name = self.__class__.__name__
        self.description = self.__doc__ or "No description available"
        
    def execute(self, *args, **kwargs):
        """Execute the plugin functionality"""
        raise NotImplementedError("Plugins must implement execute method")
    
    def get_help(self):
        """Return help text for the plugin"""
        return self.description


class PluginManager:
    """Manages plugin registration and execution"""
    
    def __init__(self):
        self._plugins: Dict[str, Plugin] = {}
        self._categories: Dict[str, List[str]] = {}
        
    def register(self, plugin: Plugin, category: str = "general"):
        """Register a plugin"""
        plugin_name = plugin.name.lower()
        self._plugins[plugin_name] = plugin
        
        if category not in self._categories:
            self._categories[category] = []
        self._categories[category].append(plugin_name)
        
    def get_plugin(self, name: str) -> Plugin:
        """Get a plugin by name"""
        return self._plugins.get(name.lower())
    
    def list_plugins(self, category: str = None) -> List[str]:
        """List all plugins, optionally filtered by category"""
        if category:
            return self._categories.get(category, [])
        return list(self._plugins.keys())
    
    def list_categories(self) -> List[str]:
        """List all plugin categories"""
        return list(self._categories.keys())
    
    def execute(self, plugin_name: str, *args, **kwargs):
        """Execute a plugin by name"""
        plugin = self.get_plugin(plugin_name)
        if not plugin:
            raise ValueError(f"Plugin '{plugin_name}' not found")
        return plugin.execute(*args, **kwargs)
    
    def discover_plugins(self, plugin_dir: str = None):
        """Automatically discover and load plugins from a directory"""
        if plugin_dir is None:
            plugin_dir = os.path.join(os.path.dirname(__file__), "plugins")
        
        plugin_path = Path(plugin_dir)
        if not plugin_path.exists():
            return
        
        for file in plugin_path.glob("*.py"):
            if file.name.startswith("_"):
                continue
                
            module_name = f"utiltools.plugins.{file.stem}"
            try:
                module = importlib.import_module(module_name)
                # Auto-register plugins that are marked for registration
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and 
                        issubclass(obj, Plugin) and 
                        obj is not Plugin and
                        hasattr(obj, '_auto_register')):
                        instance = obj()
                        category = getattr(obj, '_category', 'general')
                        self.register(instance, category)
            except Exception as e:
                print(f"Warning: Failed to load plugin {file.name}: {e}")


# Global plugin manager instance
_plugin_manager = None


def get_plugin_manager() -> PluginManager:
    """Get the global plugin manager instance"""
    global _plugin_manager
    if _plugin_manager is None:
        _plugin_manager = PluginManager()
    return _plugin_manager


def register_plugin(category: str = "general"):
    """Decorator to auto-register a plugin"""
    def decorator(cls):
        cls._auto_register = True
        cls._category = category
        return cls
    return decorator
