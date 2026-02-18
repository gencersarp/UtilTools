"""
Automation and scheduling utility plugins
"""
import schedule
import time
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Callable
from ..core import Plugin, register_plugin, get_plugin_manager


@register_plugin(category="automation")
class TaskSchedulerPlugin(Plugin):
    """Schedule tasks to run automatically"""
    
    def __init__(self):
        super().__init__()
        self.scheduled_tasks = []
    
    def execute(self, action: str, **kwargs) -> Any:
        """
        Manage scheduled tasks
        
        Args:
            action: Action to perform (add, remove, list, run)
            **kwargs: Action-specific arguments
        
        Returns:
            Result depends on action
        """
        if action == "add":
            return self._add_task(**kwargs)
        elif action == "remove":
            return self._remove_task(kwargs.get('task_id'))
        elif action == "list":
            return self._list_tasks()
        elif action == "run":
            return self._run_scheduler(kwargs.get('duration', 60))
        else:
            raise ValueError(f"Unknown action: {action}")
    
    def _add_task(self, plugin_name: str, schedule_time: str, 
                  schedule_type: str = "once", **plugin_kwargs) -> Dict[str, Any]:
        """
        Add a scheduled task
        
        Args:
            plugin_name: Name of plugin to execute
            schedule_time: When to run (e.g., "10:30", "5" for minutes)
            schedule_type: Type of schedule (once, daily, hourly, every_n_minutes)
            **plugin_kwargs: Arguments to pass to the plugin
        """
        task_id = len(self.scheduled_tasks)
        
        task = {
            "id": task_id,
            "plugin": plugin_name,
            "schedule_time": schedule_time,
            "schedule_type": schedule_type,
            "plugin_kwargs": plugin_kwargs,
            "created_at": datetime.now().isoformat(),
            "last_run": None,
            "run_count": 0
        }
        
        self.scheduled_tasks.append(task)
        
        # Set up the schedule
        self._setup_schedule(task)
        
        return task
    
    def _setup_schedule(self, task: Dict[str, Any]):
        """Set up a schedule for a task"""
        pm = get_plugin_manager()
        
        def job():
            try:
                plugin = pm.get_plugin(task["plugin"])
                if plugin:
                    plugin.execute(**task["plugin_kwargs"])
                    task["last_run"] = datetime.now().isoformat()
                    task["run_count"] += 1
            except Exception as e:
                print(f"Error running scheduled task {task['id']}: {e}")
        
        schedule_type = task["schedule_type"]
        schedule_time = task["schedule_time"]
        
        if schedule_type == "daily":
            schedule.every().day.at(schedule_time).do(job)
        elif schedule_type == "hourly":
            schedule.every().hour.at(f":{schedule_time}").do(job)
        elif schedule_type == "every_n_minutes":
            schedule.every(int(schedule_time)).minutes.do(job)
        elif schedule_type == "once":
            # For "once", we'll use a daily schedule but mark it for removal after first run
            schedule.every().day.at(schedule_time).do(job)
            task["remove_after_run"] = True
    
    def _remove_task(self, task_id: int) -> Dict[str, Any]:
        """Remove a scheduled task"""
        for i, task in enumerate(self.scheduled_tasks):
            if task["id"] == task_id:
                self.scheduled_tasks.pop(i)
                return {"success": True, "task_id": task_id}
        
        return {"success": False, "error": "Task not found"}
    
    def _list_tasks(self) -> List[Dict[str, Any]]:
        """List all scheduled tasks"""
        return self.scheduled_tasks
    
    def _run_scheduler(self, duration: int = 60) -> Dict[str, Any]:
        """
        Run the scheduler for a specified duration
        
        Args:
            duration: How long to run in seconds (0 for indefinite)
        """
        start_time = time.time()
        
        while True:
            schedule.run_pending()
            time.sleep(1)
            
            if duration > 0 and (time.time() - start_time) >= duration:
                break
        
        return {"success": True, "duration": time.time() - start_time}


@register_plugin(category="automation")
class FileWatcherPlugin(Plugin):
    """Watch files or directories for changes"""
    
    def execute(self, path: str, callback_plugin: str = None, 
                event_types: List[str] = None, duration: int = 60) -> Dict[str, Any]:
        """
        Watch a file or directory for changes
        
        Args:
            path: Path to watch
            callback_plugin: Plugin to execute on changes (optional)
            event_types: Types of events to watch (created, modified, deleted, moved)
            duration: How long to watch in seconds
        
        Returns:
            Dictionary with watch statistics
        """
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
        
        if event_types is None:
            event_types = ["created", "modified", "deleted", "moved"]
        
        events_detected = []
        
        class ChangeHandler(FileSystemEventHandler):
            def on_any_event(self, event):
                if event.event_type in event_types:
                    event_info = {
                        "type": event.event_type,
                        "path": event.src_path,
                        "is_directory": event.is_directory,
                        "timestamp": datetime.now().isoformat()
                    }
                    events_detected.append(event_info)
                    
                    if callback_plugin:
                        try:
                            pm = get_plugin_manager()
                            plugin = pm.get_plugin(callback_plugin)
                            if plugin:
                                plugin.execute(event=event_info)
                        except Exception as e:
                            print(f"Error executing callback: {e}")
        
        observer = Observer()
        observer.schedule(ChangeHandler(), path, recursive=True)
        observer.start()
        
        try:
            time.sleep(duration)
        finally:
            observer.stop()
            observer.join()
        
        return {
            "path": path,
            "duration": duration,
            "events_detected": len(events_detected),
            "events": events_detected
        }


@register_plugin(category="automation")
class BatchOperationPlugin(Plugin):
    """Execute operations on multiple files in batch"""
    
    def execute(self, operation: str, files: List[str], **kwargs) -> Dict[str, Any]:
        """
        Execute batch operations on files
        
        Args:
            operation: Operation to perform (copy, move, delete, rename)
            files: List of file paths
            **kwargs: Operation-specific arguments
        
        Returns:
            Dictionary with operation results
        """
        import shutil
        
        results = {
            "success": [],
            "failed": []
        }
        
        for file_path in files:
            try:
                if operation == "delete":
                    Path(file_path).unlink()
                    results["success"].append(file_path)
                
                elif operation == "copy":
                    destination = kwargs.get('destination')
                    if destination:
                        shutil.copy2(file_path, destination)
                        results["success"].append(file_path)
                
                elif operation == "move":
                    destination = kwargs.get('destination')
                    if destination:
                        shutil.move(file_path, destination)
                        results["success"].append(file_path)
                
                elif operation == "rename":
                    pattern = kwargs.get('pattern', '')
                    replacement = kwargs.get('replacement', '')
                    file_obj = Path(file_path)
                    new_name = file_obj.name.replace(pattern, replacement)
                    new_path = file_obj.parent / new_name
                    file_obj.rename(new_path)
                    results["success"].append(file_path)
                
            except Exception as e:
                results["failed"].append({"file": file_path, "error": str(e)})
        
        return results


@register_plugin(category="automation")
class WorkflowPlugin(Plugin):
    """Execute a series of plugin operations as a workflow"""
    
    def execute(self, workflow: List[Dict[str, Any]], stop_on_error: bool = True) -> Dict[str, Any]:
        """
        Execute a workflow of plugin operations
        
        Args:
            workflow: List of workflow steps, each with 'plugin' and 'args' keys
            stop_on_error: Stop workflow if a step fails
        
        Returns:
            Dictionary with workflow execution results
        """
        pm = get_plugin_manager()
        results = []
        
        for i, step in enumerate(workflow):
            plugin_name = step.get('plugin')
            args = step.get('args', {})
            
            try:
                plugin = pm.get_plugin(plugin_name)
                if not plugin:
                    raise ValueError(f"Plugin '{plugin_name}' not found")
                
                result = plugin.execute(**args)
                results.append({
                    "step": i,
                    "plugin": plugin_name,
                    "success": True,
                    "result": result
                })
            
            except Exception as e:
                results.append({
                    "step": i,
                    "plugin": plugin_name,
                    "success": False,
                    "error": str(e)
                })
                
                if stop_on_error:
                    break
        
        success_count = sum(1 for r in results if r.get('success', False))
        
        return {
            "total_steps": len(workflow),
            "completed_steps": len(results),
            "successful_steps": success_count,
            "failed_steps": len(results) - success_count,
            "results": results
        }
