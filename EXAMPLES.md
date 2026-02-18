# UtilTools Examples

This document provides practical examples of using UtilTools for common automation tasks.

## File Management Examples

### Example 1: Find and Organize Large Files

```python
from utiltools import PluginManager

pm = PluginManager()
pm.discover_plugins()

# Find large files
disk_analyzer = pm.get_plugin('diskanalyzerplugin')
large_files = disk_analyzer.execute(
    path='/home/user/Downloads',
    action='large_files'
)

print(f"Found {len(large_files)} large files")
for file_info in large_files:
    print(f"{file_info['path']}: {file_info['size'] / (1024**2):.2f} MB")
```

### Example 2: Backup and Compress Directories

```python
from utiltools import PluginManager
from datetime import datetime

pm = PluginManager()
pm.discover_plugins()

# Create timestamped backup
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
compression = pm.get_plugin('compressionplugin')

result = compression.execute(
    action='compress',
    source='/home/user/projects',
    destination=f'backup_{timestamp}.tar.gz',
    format='tar.gz'
)

print(f"Backup created: {result}")
```

### Example 3: Clean Up Duplicate Files

```python
from utiltools import PluginManager
import os

pm = PluginManager()
pm.discover_plugins()

# Find duplicates
finder = pm.get_plugin('duplicatefinderplugin')
duplicates = finder.execute(path='/home/user/Photos', recursive=True)

# Keep only the first file, delete the rest
for file_hash, files in duplicates.items():
    print(f"\nDuplicate set with {len(files)} files:")
    for i, file_path in enumerate(files):
        if i == 0:
            print(f"  KEEP: {file_path}")
        else:
            print(f"  DELETE: {file_path}")
            # Uncomment to actually delete:
            # os.remove(file_path)
```

## Text Processing Examples

### Example 4: Batch Process CSV Files

```python
from utiltools import PluginManager

pm = PluginManager()
pm.discover_plugins()

csv_processor = pm.get_plugin('csvprocessorplugin')

# Filter CSV rows
filtered_count = csv_processor.execute(
    action='filter',
    input_file='employees.csv',
    output_file='senior_employees.csv',
    column='years_experience',
    value='5',
    operator='contains'
)

print(f"Filtered {filtered_count} rows")

# Transform column values
transformed = csv_processor.execute(
    action='transform',
    input_file='names.csv',
    output_file='names_upper.csv',
    column='name',
    operation='upper'
)

print(f"Transformed {transformed} rows")
```

### Example 5: JSON Data Processing

```python
from utiltools import PluginManager

pm = PluginManager()
pm.discover_plugins()

json_processor = pm.get_plugin('jsonprocessorplugin')

# Prettify JSON
json_processor.execute(
    action='prettify',
    file_path='config.json',
    output='config_formatted.json'
)

# Query JSON data
result = json_processor.execute(
    action='query',
    file_path='data.json',
    path='users.0.name'  # Get first user's name
)

print(f"First user: {result}")
```

## Network Automation Examples

### Example 6: Monitor Website Availability

```python
from utiltools import PluginManager
import time

pm = PluginManager()
pm.discover_plugins()

url_validator = pm.get_plugin('urlvalidatorplugin')
websites = [
    'https://example.com',
    'https://github.com',
    'https://python.org'
]

while True:
    print("\n=== Website Status Check ===")
    for url in websites:
        result = url_validator.execute(url, check_reachable=True)
        status = "✓ UP" if result.get('reachable') else "✗ DOWN"
        print(f"{url}: {status} (Status: {result.get('status_code', 'N/A')})")
    
    time.sleep(300)  # Check every 5 minutes
```

### Example 7: Bulk Download Files

```python
from utiltools import PluginManager

pm = PluginManager()
pm.discover_plugins()

downloader = pm.get_plugin('downloadmanagerplugin')

files_to_download = [
    ('https://example.com/file1.pdf', 'downloads/file1.pdf'),
    ('https://example.com/file2.zip', 'downloads/file2.zip'),
    ('https://example.com/file3.jpg', 'downloads/file3.jpg'),
]

for url, destination in files_to_download:
    result = downloader.execute(url, destination)
    if result['success']:
        print(f"✓ Downloaded {url} -> {destination}")
    else:
        print(f"✗ Failed to download {url}: {result['error']}")
```

## System Monitoring Examples

### Example 8: Resource Monitoring Dashboard

```python
from utiltools import PluginManager
import time

pm = PluginManager()
pm.discover_plugins()

system_info = pm.get_plugin('systeminfoplugin')
process_monitor = pm.get_plugin('processmonitorplugin')

while True:
    # Get system stats
    info = system_info.execute()
    
    print("\n=== System Dashboard ===")
    print(f"CPU Usage: {info['cpu']['usage_percent']}%")
    print(f"Memory Usage: {info['memory']['percent']}%")
    print(f"Disk Usage: {info['disk']['percent']}%")
    
    # Top processes
    print("\nTop 5 Processes by Memory:")
    processes = process_monitor.execute('list', sort_by='memory', limit=5)
    for proc in processes:
        print(f"  {proc['name']}: {proc['memory_percent']:.1f}%")
    
    time.sleep(10)  # Update every 10 seconds
```

## Automation Examples

### Example 9: Automated File Organization Workflow

```python
from utiltools import PluginManager

pm = PluginManager()
pm.discover_plugins()

workflow = pm.get_plugin('workflowplugin')

# Define a workflow to organize downloads
organization_workflow = [
    {
        'plugin': 'filesearchplugin',
        'args': {
            'path': '/home/user/Downloads',
            'pattern': '*.pdf',
            'recursive': False
        }
    },
    {
        'plugin': 'batchoperationplugin',
        'args': {
            'operation': 'move',
            'files': [],  # Will be populated from previous step
            'destination': '/home/user/Documents/PDFs'
        }
    }
]

result = workflow.execute(workflow=organization_workflow, stop_on_error=False)
print(f"Workflow completed: {result['successful_steps']}/{result['total_steps']} steps")
```

### Example 10: Scheduled Backup Task

```python
from utiltools import PluginManager

pm = PluginManager()
pm.discover_plugins()

scheduler = pm.get_plugin('taskschedulerplugin')

# Schedule daily backup at 2 AM
task = scheduler.execute(
    action='add',
    plugin_name='compressionplugin',
    schedule_type='daily',
    schedule_time='02:00',
    action='compress',
    source='/home/user/important_data',
    format='tar.gz'
)

print(f"Scheduled backup task: {task['id']}")

# Run scheduler (in production, this would run as a service)
# scheduler.execute(action='run', duration=0)  # Run indefinitely
```

### Example 11: File Change Monitor with Auto-Processing

```python
from utiltools import PluginManager

pm = PluginManager()
pm.discover_plugins()

file_watcher = pm.get_plugin('filewatcherplugin')

# Watch for new CSV files and auto-process them
result = file_watcher.execute(
    path='/home/user/data_inbox',
    callback_plugin='csvprocessorplugin',
    event_types=['created'],
    duration=3600  # Watch for 1 hour
)

print(f"Detected {result['events_detected']} file changes")
```

## Integration Examples

### Example 12: Complete Backup Solution

```python
from utiltools import PluginManager
from datetime import datetime
import os

pm = PluginManager()
pm.discover_plugins()

def create_smart_backup(source_dir, backup_dir):
    """Create a backup with deduplication and compression"""
    
    # Find duplicates to avoid backing up
    finder = pm.get_plugin('duplicatefinderplugin')
    duplicates = finder.execute(path=source_dir, recursive=True)
    
    files_to_exclude = set()
    for file_hash, files in duplicates.items():
        # Keep first file, exclude others
        files_to_exclude.update(files[1:])
    
    print(f"Found {len(files_to_exclude)} duplicate files to exclude")
    
    # Create timestamped backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"backup_{timestamp}.tar.gz"
    
    compression = pm.get_plugin('compressionplugin')
    result = compression.execute(
        action='compress',
        source=source_dir,
        destination=os.path.join(backup_dir, backup_name),
        format='tar.gz'
    )
    
    print(f"Backup created: {result}")
    
    # Get system info for logging
    system_info = pm.get_plugin('systeminfoplugin')
    info = system_info.execute()
    
    return {
        'backup_file': result,
        'duplicates_excluded': len(files_to_exclude),
        'timestamp': timestamp,
        'system_disk_usage': info['disk']['percent']
    }

# Execute backup
backup_info = create_smart_backup('/home/user/projects', '/backups')
print(f"Backup completed: {backup_info}")
```

### Example 13: Network Service Monitor

```python
from utiltools import PluginManager
import time

pm = PluginManager()
pm.discover_plugins()

def monitor_services(host, services, check_interval=60):
    """Monitor network services and alert on issues"""
    
    port_scanner = pm.get_plugin('portscannerplugin')
    
    while True:
        print(f"\n=== Monitoring {host} at {time.strftime('%Y-%m-%d %H:%M:%S')} ===")
        
        results = port_scanner.execute(
            host=host,
            ports=list(services.keys()),
            timeout=2.0
        )
        
        for port, service_name in services.items():
            is_up = results.get(port, False)
            status = "✓ UP" if is_up else "✗ DOWN"
            print(f"{service_name} (:{port}): {status}")
            
            if not is_up:
                # Alert logic here
                print(f"  ALERT: {service_name} is down!")
        
        time.sleep(check_interval)

# Monitor web services
services = {
    80: "HTTP",
    443: "HTTPS",
    22: "SSH",
    3306: "MySQL",
    5432: "PostgreSQL"
}

monitor_services('localhost', services, check_interval=30)
```

## CLI Examples

### Using the Command-Line Interface

```bash
# Find all Python files with TODO comments
utiltools file search --path ./src --pattern "*.py" --content "TODO"

# Create a compressed backup
utiltools file compress /home/user/documents backup_$(date +%Y%m%d).tar.gz --format tar.gz

# Find and list duplicate files
utiltools file find-duplicates --path /home/user/Downloads

# Replace text in all markdown files
find . -name "*.md" -exec utiltools text replace {} --search "old_term" --replace "new_term" --no-dry-run \;

# Check if websites are up
utiltools network validate-url https://example.com --check-reachable

# Monitor system resources
watch -n 5 utiltools system info

# Get top memory-consuming processes
utiltools system processes --sort-by memory --limit 20

# Find large files consuming disk space
utiltools system disk --path /home --action large_files

# Scan common ports on a server
utiltools network scan-ports example.com --ports 80,443,22,3306,5432
```
