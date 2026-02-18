"""
UtilTools - A comprehensive utility toolkit for automation and productivity
"""

__version__ = "1.0.0"
__author__ = "UtilTools Contributors"

from .core import PluginManager, register_plugin
from .config import Config

__all__ = ["PluginManager", "register_plugin", "Config", "__version__"]
