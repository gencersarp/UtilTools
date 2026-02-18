"""
Command-line interface for UtilTools
"""
import click
import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint
from .core import get_plugin_manager
from .config import get_config

console = Console()


@click.group()
@click.version_option(version="1.0.0")
def main():
    """UtilTools - A comprehensive utility toolkit for automation and productivity"""
    # Initialize plugin manager and discover plugins
    pm = get_plugin_manager()
    pm.discover_plugins()


@main.command()
def list_plugins():
    """List all available plugins"""
    pm = get_plugin_manager()
    categories = pm.list_categories()
    
    table = Table(title="Available Plugins")
    table.add_column("Category", style="cyan")
    table.add_column("Plugin Name", style="green")
    table.add_column("Description", style="white")
    
    for category in sorted(categories):
        plugins = pm.list_plugins(category)
        for plugin_name in sorted(plugins):
            plugin = pm.get_plugin(plugin_name)
            description = plugin.description.split('\n')[0][:60]
            table.add_row(category, plugin_name, description)
    
    console.print(table)


@main.group()
def file():
    """File system operations"""
    pass


@file.command()
@click.option('--path', '-p', default='.', help='Directory to search in')
@click.option('--pattern', '-pt', default='*', help='File name pattern')
@click.option('--content', '-c', help='Search for files containing this text')
@click.option('--recursive/--no-recursive', '-r', default=True, help='Search recursively')
def search(path, pattern, content, recursive):
    """Search for files by name or content"""
    pm = get_plugin_manager()
    plugin = pm.get_plugin('filesearchplugin')
    
    results = plugin.execute(path=path, pattern=pattern, content=content, recursive=recursive)
    
    if results:
        console.print(f"\n[green]Found {len(results)} file(s):[/green]\n")
        for file_path in results:
            console.print(f"  • {file_path}")
    else:
        console.print("[yellow]No files found.[/yellow]")


@file.command()
@click.argument('source')
@click.argument('destination', required=False)
@click.option('--format', '-f', default='zip', type=click.Choice(['zip', 'tar', 'tar.gz']), help='Compression format')
def compress(source, destination, format):
    """Compress files or directories"""
    pm = get_plugin_manager()
    plugin = pm.get_plugin('compressionplugin')
    
    result = plugin.execute('compress', source, destination, format)
    console.print(f"[green]✓[/green] Created archive: {result}")


@file.command()
@click.argument('source')
@click.argument('destination', required=False)
def extract(source, destination):
    """Extract compressed files"""
    pm = get_plugin_manager()
    plugin = pm.get_plugin('compressionplugin')
    
    result = plugin.execute('extract', source, destination)
    console.print(f"[green]✓[/green] Extracted to: {result}")


@file.command()
@click.option('--path', '-p', default='.', help='Directory to search in')
@click.option('--recursive/--no-recursive', '-r', default=True, help='Search recursively')
def find_duplicates(path, recursive):
    """Find duplicate files by content"""
    pm = get_plugin_manager()
    plugin = pm.get_plugin('duplicatefinderplugin')
    
    with console.status("[bold green]Scanning for duplicates..."):
        duplicates = plugin.execute(path=path, recursive=recursive)
    
    if duplicates:
        console.print(f"\n[yellow]Found {len(duplicates)} set(s) of duplicates:[/yellow]\n")
        for file_hash, files in duplicates.items():
            console.print(f"[cyan]Duplicate set ({len(files)} files):[/cyan]")
            for file_path in files:
                console.print(f"  • {file_path}")
            console.print()
    else:
        console.print("[green]No duplicate files found.[/green]")


@main.group()
def text():
    """Text processing operations"""
    pass


@text.command()
@click.argument('file_path')
@click.option('--search', '-s', required=True, help='Text to search for')
@click.option('--replace', '-r', required=True, help='Replacement text')
@click.option('--regex', is_flag=True, help='Use regular expressions')
@click.option('--dry-run/--no-dry-run', default=True, help='Preview changes without modifying file')
def replace(file_path, search, replace, regex, dry_run):
    """Search and replace text in files"""
    pm = get_plugin_manager()
    plugin = pm.get_plugin('textsearchreplaceplugin')
    
    result = plugin.execute(file_path, search, replace, regex=regex, dry_run=dry_run)
    
    if result['changed']:
        status = "[yellow]Would replace[/yellow]" if dry_run else "[green]Replaced[/green]"
        console.print(f"{status} {result['matches']} occurrence(s) in {file_path}")
    else:
        console.print(f"[yellow]No matches found in {file_path}[/yellow]")


@text.command()
@click.argument('file_path')
@click.option('--action', '-a', required=True, 
              type=click.Choice(['prettify', 'minify', 'validate', 'query']),
              help='Action to perform')
@click.option('--query', '-q', help='JSON path query (for query action)')
@click.option('--output', '-o', help='Output file path')
def json_process(file_path, action, query, output):
    """Process JSON files"""
    pm = get_plugin_manager()
    plugin = pm.get_plugin('jsonprocessorplugin')
    
    kwargs = {'output': output} if output else {}
    if action == 'query' and query:
        kwargs['path'] = query
    
    result = plugin.execute(action, file_path, **kwargs)
    
    if action == 'query':
        console.print(json.dumps(result, indent=2))
    elif action in ['prettify', 'minify']:
        console.print(f"[green]✓[/green] Processed: {result}")
    elif action == 'validate':
        console.print(f"[green]✓[/green] Valid JSON ({result['type']})")


@main.group()
def network():
    """Network operations"""
    pass


@network.command()
@click.argument('host')
@click.option('--ports', '-p', help='Comma-separated list of ports to scan')
@click.option('--timeout', '-t', default=1.0, help='Connection timeout in seconds')
def scan_ports(host, ports, timeout):
    """Scan network ports on a host"""
    pm = get_plugin_manager()
    plugin = pm.get_plugin('portscannerplugin')
    
    port_list = [int(p) for p in ports.split(',')] if ports else None
    
    with console.status(f"[bold green]Scanning {host}..."):
        results = plugin.execute(host, port_list, timeout)
    
    table = Table(title=f"Port Scan Results for {host}")
    table.add_column("Port", style="cyan")
    table.add_column("Status", style="white")
    
    for port, is_open in sorted(results.items()):
        status = "[green]OPEN[/green]" if is_open else "[red]CLOSED[/red]"
        table.add_row(str(port), status)
    
    console.print(table)


@network.command()
@click.argument('url')
@click.option('--check-reachable', '-c', is_flag=True, help='Check if URL is reachable')
def validate_url(url, check_reachable):
    """Validate and parse a URL"""
    pm = get_plugin_manager()
    plugin = pm.get_plugin('urlvalidatorplugin')
    
    result = plugin.execute(url, check_reachable=check_reachable)
    
    if result.get('valid'):
        console.print(Panel.fit(
            f"[green]Valid URL[/green]\n\n"
            f"Scheme: {result['scheme']}\n"
            f"Domain: {result['netloc']}\n"
            f"Path: {result['path']}\n"
            f"Query: {result['query']}\n"
            + (f"Status: {result.get('status_code')}\n" if check_reachable else ""),
            title="URL Analysis"
        ))
    else:
        console.print(f"[red]Invalid URL: {result.get('error', 'Unknown error')}[/red]")


@network.command()
@click.argument('url')
@click.option('--output', '-o', help='Output file path')
def download(url, output):
    """Download a file from a URL"""
    pm = get_plugin_manager()
    plugin = pm.get_plugin('downloadmanagerplugin')
    
    with console.status(f"[bold green]Downloading {url}..."):
        result = plugin.execute(url, output)
    
    if result.get('success'):
        console.print(f"[green]✓[/green] Downloaded to: {result['destination']} ({result['size']} bytes)")
    else:
        console.print(f"[red]✗ Download failed: {result.get('error')}[/red]")


@main.group()
def system():
    """System monitoring and management"""
    pass


@system.command()
def info():
    """Get comprehensive system information"""
    pm = get_plugin_manager()
    plugin = pm.get_plugin('systeminfoplugin')
    
    info = plugin.execute()
    
    # Display system info in a nice format
    console.print(Panel.fit(
        f"[cyan]Platform:[/cyan] {info['platform']['system']} {info['platform']['release']}\n"
        f"[cyan]Machine:[/cyan] {info['platform']['machine']}\n"
        f"[cyan]Python:[/cyan] {info['platform']['python_version']}\n\n"
        f"[cyan]CPU Cores:[/cyan] {info['cpu']['physical_cores']} physical, {info['cpu']['logical_cores']} logical\n"
        f"[cyan]CPU Usage:[/cyan] {info['cpu']['usage_percent']}%\n\n"
        f"[cyan]Memory Total:[/cyan] {info['memory']['total'] / (1024**3):.2f} GB\n"
        f"[cyan]Memory Used:[/cyan] {info['memory']['percent']}%\n\n"
        f"[cyan]Disk Total:[/cyan] {info['disk']['total'] / (1024**3):.2f} GB\n"
        f"[cyan]Disk Used:[/cyan] {info['disk']['percent']}%",
        title="System Information"
    ))


@system.command()
@click.option('--sort-by', '-s', default='memory', type=click.Choice(['memory', 'cpu']), help='Sort by')
@click.option('--limit', '-l', default=10, help='Number of processes to show')
def processes(sort_by, limit):
    """List top system processes"""
    pm = get_plugin_manager()
    plugin = pm.get_plugin('processmonitorplugin')
    
    processes = plugin.execute('list', sort_by=sort_by, limit=limit)
    
    table = Table(title=f"Top {limit} Processes (by {sort_by})")
    table.add_column("PID", style="cyan")
    table.add_column("Name", style="white")
    table.add_column("CPU %", style="yellow")
    table.add_column("Memory %", style="green")
    table.add_column("Status", style="blue")
    
    for proc in processes:
        table.add_row(
            str(proc['pid']),
            proc['name'],
            f"{proc['cpu_percent']:.1f}",
            f"{proc['memory_percent']:.1f}",
            proc['status']
        )
    
    console.print(table)


@system.command()
@click.option('--path', '-p', default='.', help='Path to analyze')
@click.option('--action', '-a', default='usage', 
              type=click.Choice(['usage', 'large_files', 'directory_sizes']),
              help='Analysis type')
def disk(path, action):
    """Analyze disk usage"""
    pm = get_plugin_manager()
    plugin = pm.get_plugin('diskanalyzerplugin')
    
    result = plugin.execute(path, action)
    
    if action == 'usage':
        console.print(Panel.fit(
            f"[cyan]Path:[/cyan] {result['path']}\n"
            f"[cyan]Total:[/cyan] {result['total'] / (1024**3):.2f} GB\n"
            f"[cyan]Used:[/cyan] {result['used'] / (1024**3):.2f} GB\n"
            f"[cyan]Free:[/cyan] {result['free'] / (1024**3):.2f} GB\n"
            f"[cyan]Usage:[/cyan] {result['percent']}%",
            title="Disk Usage"
        ))
    elif action == 'large_files':
        table = Table(title="Large Files")
        table.add_column("Path", style="white")
        table.add_column("Size", style="yellow")
        
        for item in result:
            table.add_row(item['path'], f"{item['size'] / (1024**2):.2f} MB")
        
        console.print(table)
    elif action == 'directory_sizes':
        table = Table(title="Directory Sizes")
        table.add_column("Path", style="white")
        table.add_column("Size", style="yellow")
        
        for item in result:
            table.add_row(item['path'], f"{item['size'] / (1024**2):.2f} MB")
        
        console.print(table)


@main.group()
def config():
    """Configuration management"""
    pass


@config.command()
@click.argument('key')
@click.argument('value')
def set(key, value):
    """Set a configuration value"""
    cfg = get_config()
    cfg.set(key, value)
    cfg.save()
    console.print(f"[green]✓[/green] Set {key} = {value}")


@config.command()
@click.argument('key')
def get(key):
    """Get a configuration value"""
    cfg = get_config()
    value = cfg.get(key)
    console.print(f"{key} = {value}")


@config.command()
def show():
    """Show all configuration"""
    cfg = get_config()
    console.print(json.dumps(cfg._config, indent=2))


if __name__ == '__main__':
    main()
