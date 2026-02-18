"""
System monitoring and management utility plugins
"""
import psutil
import platform
import time
from datetime import datetime
from typing import Dict, List, Any
from ..core import Plugin, register_plugin


@register_plugin(category="system")
class SystemInfoPlugin(Plugin):
    """Get comprehensive system information"""
    
    def execute(self) -> Dict[str, Any]:
        """
        Get system information
        
        Returns:
            Dictionary with system details
        """
        return {
            "platform": {
                "system": platform.system(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
                "processor": platform.processor(),
                "python_version": platform.python_version()
            },
            "cpu": {
                "physical_cores": psutil.cpu_count(logical=False),
                "logical_cores": psutil.cpu_count(logical=True),
                "frequency": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
                "usage_percent": psutil.cpu_percent(interval=1)
            },
            "memory": {
                "total": psutil.virtual_memory().total,
                "available": psutil.virtual_memory().available,
                "used": psutil.virtual_memory().used,
                "percent": psutil.virtual_memory().percent
            },
            "disk": {
                "total": psutil.disk_usage('/').total,
                "used": psutil.disk_usage('/').used,
                "free": psutil.disk_usage('/').free,
                "percent": psutil.disk_usage('/').percent
            },
            "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat()
        }


@register_plugin(category="system")
class ProcessMonitorPlugin(Plugin):
    """Monitor and manage system processes"""
    
    def execute(self, action: str = "list", **kwargs) -> Any:
        """
        Monitor or manage processes
        
        Args:
            action: Action to perform (list, info, kill)
            **kwargs: Action-specific arguments
        
        Returns:
            Result depends on action
        """
        if action == "list":
            return self._list_processes(**kwargs)
        elif action == "info":
            return self._process_info(kwargs.get('pid'))
        elif action == "kill":
            return self._kill_process(kwargs.get('pid'))
        else:
            raise ValueError(f"Unknown action: {action}")
    
    def _list_processes(self, sort_by: str = "memory", limit: int = 10) -> List[Dict[str, Any]]:
        """List top processes"""
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
            try:
                processes.append({
                    "pid": proc.info['pid'],
                    "name": proc.info['name'],
                    "cpu_percent": proc.info['cpu_percent'],
                    "memory_percent": proc.info['memory_percent'],
                    "status": proc.info['status']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Sort processes
        if sort_by == "memory":
            processes.sort(key=lambda x: x['memory_percent'], reverse=True)
        elif sort_by == "cpu":
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
        
        return processes[:limit]
    
    def _process_info(self, pid: int) -> Dict[str, Any]:
        """Get detailed process information"""
        try:
            proc = psutil.Process(pid)
            return {
                "pid": proc.pid,
                "name": proc.name(),
                "status": proc.status(),
                "cpu_percent": proc.cpu_percent(interval=0.1),
                "memory_percent": proc.memory_percent(),
                "create_time": datetime.fromtimestamp(proc.create_time()).isoformat(),
                "num_threads": proc.num_threads(),
                "cmdline": proc.cmdline()
            }
        except psutil.NoSuchProcess:
            return {"error": f"Process {pid} not found"}
    
    def _kill_process(self, pid: int) -> Dict[str, Any]:
        """Kill a process"""
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            proc.wait(timeout=3)
            return {"success": True, "pid": pid}
        except psutil.NoSuchProcess:
            return {"success": False, "error": f"Process {pid} not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}


@register_plugin(category="system")
class DiskAnalyzerPlugin(Plugin):
    """Analyze disk usage and find large files"""
    
    def execute(self, path: str = ".", action: str = "usage") -> Any:
        """
        Analyze disk usage
        
        Args:
            path: Path to analyze
            action: Action to perform (usage, large_files, directory_sizes)
        
        Returns:
            Result depends on action
        """
        if action == "usage":
            return self._disk_usage(path)
        elif action == "large_files":
            return self._find_large_files(path)
        elif action == "directory_sizes":
            return self._directory_sizes(path)
        else:
            raise ValueError(f"Unknown action: {action}")
    
    def _disk_usage(self, path: str) -> Dict[str, Any]:
        """Get disk usage for a path"""
        usage = psutil.disk_usage(path)
        return {
            "path": path,
            "total": usage.total,
            "used": usage.used,
            "free": usage.free,
            "percent": usage.percent
        }
    
    def _find_large_files(self, path: str, min_size: int = 10*1024*1024, limit: int = 10) -> List[Dict[str, Any]]:
        """Find large files in a directory"""
        from pathlib import Path
        
        large_files = []
        
        try:
            for file_path in Path(path).rglob('*'):
                if file_path.is_file():
                    try:
                        size = file_path.stat().st_size
                        if size >= min_size:
                            large_files.append({
                                "path": str(file_path),
                                "size": size,
                                "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                            })
                    except (OSError, PermissionError):
                        pass
        except (OSError, PermissionError):
            pass
        
        large_files.sort(key=lambda x: x['size'], reverse=True)
        return large_files[:limit]
    
    def _directory_sizes(self, path: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get sizes of subdirectories"""
        from pathlib import Path
        
        dir_sizes = []
        
        try:
            for item in Path(path).iterdir():
                if item.is_dir():
                    try:
                        size = sum(f.stat().st_size for f in item.rglob('*') if f.is_file())
                        dir_sizes.append({
                            "path": str(item),
                            "size": size
                        })
                    except:
                        pass
        except PermissionError:
            pass
        
        dir_sizes.sort(key=lambda x: x['size'], reverse=True)
        return dir_sizes[:limit]


@register_plugin(category="system")
class NetworkMonitorPlugin(Plugin):
    """Monitor network connections and statistics"""
    
    def execute(self, action: str = "connections") -> Any:
        """
        Monitor network activity
        
        Args:
            action: Action to perform (connections, stats, interfaces)
        
        Returns:
            Result depends on action
        """
        if action == "connections":
            return self._list_connections()
        elif action == "stats":
            return self._network_stats()
        elif action == "interfaces":
            return self._network_interfaces()
        else:
            raise ValueError(f"Unknown action: {action}")
    
    def _list_connections(self, limit: int = 20) -> List[Dict[str, Any]]:
        """List active network connections"""
        connections = []
        
        for conn in psutil.net_connections():
            try:
                connections.append({
                    "fd": conn.fd,
                    "family": str(conn.family),
                    "type": str(conn.type),
                    "local_address": f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else None,
                    "remote_address": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
                    "status": conn.status,
                    "pid": conn.pid
                })
            except (psutil.Error, AttributeError):
                pass
        
        return connections[:limit]
    
    def _network_stats(self) -> Dict[str, Any]:
        """Get network I/O statistics"""
        stats = psutil.net_io_counters()
        return {
            "bytes_sent": stats.bytes_sent,
            "bytes_recv": stats.bytes_recv,
            "packets_sent": stats.packets_sent,
            "packets_recv": stats.packets_recv,
            "errors_in": stats.errin,
            "errors_out": stats.errout,
            "drop_in": stats.dropin,
            "drop_out": stats.dropout
        }
    
    def _network_interfaces(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get network interface information"""
        interfaces = {}
        
        for interface, addrs in psutil.net_if_addrs().items():
            interfaces[interface] = []
            for addr in addrs:
                interfaces[interface].append({
                    "family": str(addr.family),
                    "address": addr.address,
                    "netmask": addr.netmask,
                    "broadcast": addr.broadcast
                })
        
        return interfaces
