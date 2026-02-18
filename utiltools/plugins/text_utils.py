"""
Text processing utility plugins
"""
import re
import json
import csv
from pathlib import Path
from typing import List, Dict, Any
from ..core import Plugin, register_plugin


@register_plugin(category="text")
class TextSearchReplacePlugin(Plugin):
    """Search and replace text in files"""
    
    def execute(self, file_path: str, search: str, replace: str, 
                regex: bool = False, dry_run: bool = True) -> Dict[str, Any]:
        """
        Search and replace text in a file
        
        Args:
            file_path: Path to the file
            search: Text or pattern to search for
            replace: Replacement text
            regex: Use regular expressions
            dry_run: If True, only show what would be replaced
        
        Returns:
            Dictionary with match count and preview
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if regex:
            matches = len(re.findall(search, content))
            new_content = re.sub(search, replace, content)
        else:
            matches = content.count(search)
            new_content = content.replace(search, replace)
        
        result = {
            "file": file_path,
            "matches": matches,
            "changed": content != new_content
        }
        
        if not dry_run and result["changed"]:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
        
        return result


@register_plugin(category="text")
class TextFormatterPlugin(Plugin):
    """Format text files (trim, case conversion, line endings)"""
    
    def execute(self, file_path: str, operation: str, **kwargs) -> str:
        """
        Format text file
        
        Args:
            file_path: Path to the file
            operation: Operation to perform (upper, lower, title, trim, unix_newlines, windows_newlines)
            **kwargs: Additional operation-specific arguments
        
        Returns:
            Formatted text
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if operation == "upper":
            result = content.upper()
        elif operation == "lower":
            result = content.lower()
        elif operation == "title":
            result = content.title()
        elif operation == "trim":
            result = '\n'.join(line.strip() for line in content.splitlines())
        elif operation == "unix_newlines":
            result = content.replace('\r\n', '\n')
        elif operation == "windows_newlines":
            result = content.replace('\n', '\r\n').replace('\r\r\n', '\r\n')
        else:
            raise ValueError(f"Unknown operation: {operation}")
        
        return result


@register_plugin(category="text")
class CSVProcessorPlugin(Plugin):
    """Process CSV files (filter, transform, merge)"""
    
    def execute(self, action: str, input_file: str, output_file: str = None, **kwargs) -> Any:
        """
        Process CSV files
        
        Args:
            action: Action to perform (filter, transform, merge, stats)
            input_file: Input CSV file path
            output_file: Output CSV file path (if applicable)
            **kwargs: Action-specific arguments
        
        Returns:
            Result depends on action
        """
        if action == "filter":
            return self._filter_csv(input_file, output_file, **kwargs)
        elif action == "transform":
            return self._transform_csv(input_file, output_file, **kwargs)
        elif action == "stats":
            return self._csv_stats(input_file)
        else:
            raise ValueError(f"Unknown action: {action}")
    
    def _filter_csv(self, input_file: str, output_file: str, 
                    column: str, value: str, operator: str = "equals") -> int:
        """Filter CSV rows based on column value"""
        filtered_count = 0
        
        with open(input_file, 'r', encoding='utf-8') as inf:
            reader = csv.DictReader(inf)
            fieldnames = reader.fieldnames
            
            filtered_rows = []
            for row in reader:
                if column not in row:
                    continue
                
                match = False
                if operator == "equals":
                    match = row[column] == value
                elif operator == "contains":
                    match = value in row[column]
                elif operator == "startswith":
                    match = row[column].startswith(value)
                elif operator == "endswith":
                    match = row[column].endswith(value)
                
                if match:
                    filtered_rows.append(row)
                    filtered_count += 1
            
            if output_file:
                with open(output_file, 'w', encoding='utf-8', newline='') as outf:
                    writer = csv.DictWriter(outf, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(filtered_rows)
        
        return filtered_count
    
    def _transform_csv(self, input_file: str, output_file: str, 
                       column: str, operation: str) -> int:
        """Transform CSV column values"""
        transformed_count = 0
        
        with open(input_file, 'r', encoding='utf-8') as inf:
            reader = csv.DictReader(inf)
            fieldnames = reader.fieldnames
            
            transformed_rows = []
            for row in reader:
                if column in row:
                    if operation == "upper":
                        row[column] = row[column].upper()
                    elif operation == "lower":
                        row[column] = row[column].lower()
                    elif operation == "strip":
                        row[column] = row[column].strip()
                    transformed_count += 1
                
                transformed_rows.append(row)
            
            with open(output_file, 'w', encoding='utf-8', newline='') as outf:
                writer = csv.DictWriter(outf, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(transformed_rows)
        
        return transformed_count
    
    def _csv_stats(self, input_file: str) -> Dict[str, Any]:
        """Get statistics about a CSV file"""
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
            return {
                "total_rows": len(rows),
                "columns": reader.fieldnames,
                "column_count": len(reader.fieldnames) if reader.fieldnames else 0
            }


@register_plugin(category="text")
class JSONProcessorPlugin(Plugin):
    """Process JSON files (query, transform, validate)"""
    
    def execute(self, action: str, file_path: str, **kwargs) -> Any:
        """
        Process JSON files
        
        Args:
            action: Action to perform (query, prettify, minify, validate)
            file_path: JSON file path
            **kwargs: Action-specific arguments
        
        Returns:
            Result depends on action
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if action == "prettify":
            output = kwargs.get('output', file_path)
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, sort_keys=True)
            return output
        
        elif action == "minify":
            output = kwargs.get('output', file_path)
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(data, f, separators=(',', ':'))
            return output
        
        elif action == "validate":
            return {"valid": True, "type": type(data).__name__}
        
        elif action == "query":
            # Simple key path query (e.g., "user.name")
            path = kwargs.get('path', '')
            result = data
            for key in path.split('.'):
                if key:
                    if isinstance(result, dict):
                        result = result.get(key)
                    elif isinstance(result, list) and key.isdigit():
                        result = result[int(key)]
                    else:
                        return None
            return result
        
        return data


@register_plugin(category="text")
class RegexToolPlugin(Plugin):
    """Test and apply regular expressions"""
    
    def execute(self, pattern: str, text: str, action: str = "findall", **kwargs) -> Any:
        """
        Work with regular expressions
        
        Args:
            pattern: Regular expression pattern
            text: Text to search/match
            action: Action to perform (findall, match, search, split, sub)
            **kwargs: Additional arguments (e.g., replacement for sub)
        
        Returns:
            Result depends on action
        """
        flags = kwargs.get('flags', 0)
        
        if action == "findall":
            return re.findall(pattern, text, flags)
        elif action == "match":
            match = re.match(pattern, text, flags)
            return match.group() if match else None
        elif action == "search":
            match = re.search(pattern, text, flags)
            return match.group() if match else None
        elif action == "split":
            return re.split(pattern, text, flags=flags)
        elif action == "sub":
            replacement = kwargs.get('replacement', '')
            return re.sub(pattern, replacement, text, flags=flags)
        else:
            raise ValueError(f"Unknown action: {action}")
