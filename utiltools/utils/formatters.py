"""
Common utility functions for formatting and display
"""
from typing import Any, Dict
import json


def format_json(data: Any, indent: int = 2) -> str:
    """
    Format data as pretty JSON
    
    Args:
        data: Data to format
        indent: Indentation level
    
    Returns:
        Formatted JSON string
    """
    return json.dumps(data, indent=indent, sort_keys=True, default=str)


def format_table_row(columns: list, widths: list) -> str:
    """
    Format a table row with fixed column widths
    
    Args:
        columns: List of column values
        widths: List of column widths
    
    Returns:
        Formatted row string
    """
    formatted = []
    for col, width in zip(columns, widths):
        col_str = str(col)
        if len(col_str) > width:
            col_str = col_str[:width-3] + "..."
        formatted.append(col_str.ljust(width))
    return " | ".join(formatted)


def truncate_string(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Truncate a string to a maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add when truncated
    
    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def format_bytes(bytes_value: int) -> str:
    """
    Format bytes as human-readable string
    
    Args:
        bytes_value: Value in bytes
    
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"


def format_duration(seconds: float) -> str:
    """
    Format duration in seconds as human-readable string
    
    Args:
        seconds: Duration in seconds
    
    Returns:
        Formatted string (e.g., "2h 30m 15s")
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    
    minutes = int(seconds // 60)
    seconds = seconds % 60
    
    if minutes < 60:
        return f"{minutes}m {seconds:.0f}s"
    
    hours = minutes // 60
    minutes = minutes % 60
    
    return f"{hours}h {minutes}m"
