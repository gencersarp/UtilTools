"""
Common utility functions for file operations
"""
import os
from pathlib import Path
from typing import List, Optional


def ensure_directory(path: str) -> Path:
    """
    Ensure a directory exists, creating it if necessary
    
    Args:
        path: Directory path
    
    Returns:
        Path object for the directory
    """
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def get_file_size_human(size_bytes: int) -> str:
    """
    Convert bytes to human-readable format
    
    Args:
        size_bytes: Size in bytes
    
    Returns:
        Human-readable size string
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def find_files_by_extension(directory: str, extensions: List[str], 
                            recursive: bool = True) -> List[str]:
    """
    Find all files with specific extensions
    
    Args:
        directory: Directory to search
        extensions: List of extensions (e.g., ['.txt', '.py'])
        recursive: Search recursively
    
    Returns:
        List of file paths
    """
    files = []
    path = Path(directory)
    
    pattern = "**/*" if recursive else "*"
    
    for file_path in path.glob(pattern):
        if file_path.is_file() and file_path.suffix in extensions:
            files.append(str(file_path))
    
    return files


def safe_file_write(file_path: str, content: str, backup: bool = True) -> bool:
    """
    Safely write to a file with optional backup
    
    Args:
        file_path: Path to file
        content: Content to write
        backup: Create backup of existing file
    
    Returns:
        True if successful
    """
    try:
        path = Path(file_path)
        
        # Create backup if file exists and backup is enabled
        if backup and path.exists():
            backup_path = path.with_suffix(path.suffix + '.bak')
            path.rename(backup_path)
        
        # Write new content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception:
        return False
