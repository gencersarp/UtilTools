"""
Configuration management for UtilTools
"""
import os
import yaml
from pathlib import Path
from typing import Any, Dict


class Config:
    """Configuration manager for UtilTools"""
    
    DEFAULT_CONFIG = {
        "logging": {
            "level": "INFO",
            "file": "utiltools.log"
        },
        "plugins": {
            "auto_discover": True,
            "plugin_dirs": []
        },
        "network": {
            "timeout": 30,
            "retries": 3
        },
        "file_operations": {
            "backup_enabled": True,
            "max_file_size": 104857600  # 100MB
        }
    }
    
    def __init__(self, config_path: str = None):
        self._config = self.DEFAULT_CONFIG.copy()
        self._config_path = config_path or self._get_default_config_path()
        self.load()
    
    def _get_default_config_path(self) -> str:
        """Get the default configuration file path"""
        home = Path.home()
        config_dir = home / ".utiltools"
        config_dir.mkdir(exist_ok=True)
        return str(config_dir / "config.yml")
    
    def load(self):
        """Load configuration from file"""
        if os.path.exists(self._config_path):
            try:
                with open(self._config_path, 'r') as f:
                    user_config = yaml.safe_load(f) or {}
                    self._merge_config(self._config, user_config)
            except Exception as e:
                print(f"Warning: Failed to load config: {e}")
    
    def save(self):
        """Save current configuration to file"""
        config_path = Path(self._config_path)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self._config_path, 'w') as f:
            yaml.dump(self._config, f, default_flow_style=False)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value using dot notation"""
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        return value
    
    def set(self, key: str, value: Any):
        """Set a configuration value using dot notation"""
        keys = key.split('.')
        config = self._config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
    
    def _merge_config(self, base: Dict, update: Dict):
        """Recursively merge configuration dictionaries"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
    
    def reset(self):
        """Reset configuration to defaults"""
        self._config = self.DEFAULT_CONFIG.copy()
        self.save()


# Global config instance
_config = None


def get_config() -> Config:
    """Get the global configuration instance"""
    global _config
    if _config is None:
        _config = Config()
    return _config
