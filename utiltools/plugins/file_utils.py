"""
File system utility plugins
"""
import os
import shutil
import zipfile
import tarfile
import glob
from pathlib import Path
from typing import List, Dict
from ..core import Plugin, register_plugin


@register_plugin(category="file")
class FileSearchPlugin(Plugin):
    """Search for files by name pattern or content"""
    
    def execute(self, path: str = ".", pattern: str = "*", content: str = None, recursive: bool = True) -> List[str]:
        """
        Search for files matching a pattern or containing specific content
        
        Args:
            path: Directory to search in
            pattern: File name pattern (supports wildcards)
            content: Search for files containing this text
            recursive: Search recursively in subdirectories
        
        Returns:
            List of matching file paths
        """
        results = []
        search_pattern = f"**/{pattern}" if recursive else pattern
        
        for file_path in Path(path).glob(search_pattern):
            if file_path.is_file():
                if content is None:
                    results.append(str(file_path))
                else:
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            if content in f.read():
                                results.append(str(file_path))
                    except:
                        pass
        
        return results


@register_plugin(category="file")
class BatchRenamePlugin(Plugin):
    """Batch rename files with pattern replacement"""
    
    def execute(self, path: str, pattern: str, replacement: str, dry_run: bool = True) -> Dict[str, str]:
        """
        Batch rename files by replacing pattern in filenames
        
        Args:
            path: Directory containing files to rename
            pattern: Pattern to search for in filenames
            replacement: Replacement text
            dry_run: If True, only show what would be renamed
        
        Returns:
            Dictionary mapping old names to new names
        """
        renamed = {}
        path_obj = Path(path)
        
        for file_path in path_obj.iterdir():
            if file_path.is_file() and pattern in file_path.name:
                new_name = file_path.name.replace(pattern, replacement)
                new_path = file_path.parent / new_name
                renamed[str(file_path)] = str(new_path)
                
                if not dry_run:
                    file_path.rename(new_path)
        
        return renamed


@register_plugin(category="file")
class CompressionPlugin(Plugin):
    """Compress and extract files (zip, tar, tar.gz)"""
    
    def execute(self, action: str, source: str, destination: str = None, format: str = "zip") -> str:
        """
        Compress or extract files
        
        Args:
            action: 'compress' or 'extract'
            source: Source file or directory
            destination: Destination path
            format: Compression format (zip, tar, tar.gz)
        
        Returns:
            Path to the created archive or extracted directory
        """
        if action == "compress":
            return self._compress(source, destination, format)
        elif action == "extract":
            return self._extract(source, destination, format)
        else:
            raise ValueError(f"Invalid action: {action}")
    
    def _compress(self, source: str, destination: str, format: str) -> str:
        """Compress files or directories"""
        source_path = Path(source)
        
        if destination is None:
            destination = f"{source}.{format}"
        
        if format == "zip":
            with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as zipf:
                if source_path.is_file():
                    zipf.write(source, source_path.name)
                else:
                    for file in source_path.rglob('*'):
                        if file.is_file():
                            zipf.write(file, file.relative_to(source_path.parent))
        
        elif format in ["tar", "tar.gz"]:
            mode = "w:gz" if format == "tar.gz" else "w"
            with tarfile.open(destination, mode) as tar:
                tar.add(source, arcname=source_path.name)
        
        return destination
    
    def _extract(self, source: str, destination: str, format: str = None) -> str:
        """Extract compressed files"""
        if destination is None:
            destination = Path(source).stem
        
        Path(destination).mkdir(parents=True, exist_ok=True)
        
        # Auto-detect format if not specified
        if format is None:
            if source.endswith('.zip'):
                format = 'zip'
            elif source.endswith('.tar.gz') or source.endswith('.tgz'):
                format = 'tar.gz'
            elif source.endswith('.tar'):
                format = 'tar'
        
        if format == "zip":
            with zipfile.ZipFile(source, 'r') as zipf:
                zipf.extractall(destination)
        elif format in ["tar", "tar.gz"]:
            with tarfile.open(source, 'r:*') as tar:
                tar.extractall(destination)
        
        return destination


@register_plugin(category="file")
class DuplicateFinderPlugin(Plugin):
    """Find duplicate files based on content hash"""
    
    def execute(self, path: str = ".", recursive: bool = True) -> Dict[str, List[str]]:
        """
        Find duplicate files by comparing their content
        
        Args:
            path: Directory to search in
            recursive: Search recursively in subdirectories
        
        Returns:
            Dictionary mapping file hashes to lists of duplicate file paths
        """
        import hashlib
        
        file_hashes = {}
        duplicates = {}
        
        search_pattern = "**/*" if recursive else "*"
        
        for file_path in Path(path).glob(search_pattern):
            if file_path.is_file():
                try:
                    # Calculate file hash using SHA-256 for better collision resistance
                    hasher = hashlib.sha256()
                    with open(file_path, 'rb') as f:
                        for chunk in iter(lambda: f.read(4096), b""):
                            hasher.update(chunk)
                    
                    file_hash = hasher.hexdigest()
                    
                    if file_hash in file_hashes:
                        if file_hash not in duplicates:
                            duplicates[file_hash] = [file_hashes[file_hash]]
                        duplicates[file_hash].append(str(file_path))
                    else:
                        file_hashes[file_hash] = str(file_path)
                
                except Exception:
                    pass
        
        return duplicates


@register_plugin(category="file")
class DirectorySyncPlugin(Plugin):
    """Synchronize directories (copy new and modified files)"""
    
    def execute(self, source: str, destination: str, delete: bool = False, dry_run: bool = True) -> Dict[str, List[str]]:
        """
        Synchronize source directory to destination
        
        Args:
            source: Source directory
            destination: Destination directory
            delete: Delete files in destination that don't exist in source
            dry_run: If True, only show what would be synced
        
        Returns:
            Dictionary with lists of copied, updated, and deleted files
        """
        result = {
            "copied": [],
            "updated": [],
            "deleted": []
        }
        
        source_path = Path(source)
        dest_path = Path(destination)
        
        # Create destination if it doesn't exist
        if not dry_run:
            dest_path.mkdir(parents=True, exist_ok=True)
        
        # Copy/update files
        for src_file in source_path.rglob('*'):
            if src_file.is_file():
                rel_path = src_file.relative_to(source_path)
                dst_file = dest_path / rel_path
                
                if not dst_file.exists():
                    result["copied"].append(str(rel_path))
                    if not dry_run:
                        dst_file.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(src_file, dst_file)
                elif src_file.stat().st_mtime > dst_file.stat().st_mtime:
                    result["updated"].append(str(rel_path))
                    if not dry_run:
                        shutil.copy2(src_file, dst_file)
        
        # Delete files not in source
        if delete:
            for dst_file in dest_path.rglob('*'):
                if dst_file.is_file():
                    rel_path = dst_file.relative_to(dest_path)
                    src_file = source_path / rel_path
                    
                    if not src_file.exists():
                        result["deleted"].append(str(rel_path))
                        if not dry_run:
                            dst_file.unlink()
        
        return result
