"""Configuration management module."""

import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class Config:
    """Game configuration manager."""
    
    DEFAULT_CONFIG = {
        "window": {
            "width": 1280,
            "height": 720,
            "title": "Japan City Builder",
            "fps": 60
        },
        "game": {
            "initial_budget": 10000,
            "difficulty": "normal",
            "autosave_interval": 30  # minutes
        },
        "debug": False
    }
    
    def __init__(self, config_data: Optional[Dict[str, Any]] = None):
        """Initialize configuration.
        
        Args:
            config_data: Dictionary containing configuration.
                        Defaults to DEFAULT_CONFIG if None.
        """
        self.data = config_data or self.DEFAULT_CONFIG.copy()
    
    @classmethod
    def from_file(cls, filepath: Optional[Path] = None) -> "Config":
        """Load configuration from file.
        
        Args:
            filepath: Path to configuration file.
                     Defaults to config/game.json
        
        Returns:
            Config instance.
        """
        if filepath is None:
            filepath = Path(__file__).parent.parent.parent / "config" / "game.json"
        
        if filepath.exists():
            try:
                with open(filepath, 'r') as f:
                    config_data = json.load(f)
                logger.info(f"Configuration loaded from {filepath}")
                return cls(config_data)
            except Exception as e:
                logger.warning(f"Failed to load config from {filepath}: {e}")
                logger.warning("Using default configuration.")
        else:
            logger.info(f"Config file not found at {filepath}, using defaults.")
        
        return cls()
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot-notation key.
        
        Args:
            key: Configuration key (e.g., 'window.width')
            default: Default value if key not found
        
        Returns:
            Configuration value.
        """
        keys = key.split('.')
        value = self.data
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value by dot-notation key.
        
        Args:
            key: Configuration key (e.g., 'window.width')
            value: Value to set
        """
        keys = key.split('.')
        config = self.data
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def __repr__(self) -> str:
        return f"Config({self.data})"
