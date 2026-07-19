"""
Process Management Utility for Python

A comprehensive process management class for system process operations
including killing, terminating, suspending, and monitoring processes.
"""

import psutil
from typing import List, Dict, Optional, Union
import time
import logging
from datetime import datetime


class ProcessManager:
    """
    Manage and control system processes with comprehensive monitoring and control capabilities.
    
    This class provides a robust interface for managing system processes including
    killing, terminating, suspending, resuming, and gathering detailed information
    about running processes.
    
    Attributes:
        process_name (str): Name of the target process to manage
        logger (logging.Logger): Logger instance for the class
        
    Examples:
        >>> manager = ProcessManager("chrome.exe")
        >>> if manager.is_running():
        ...     result = manager.kill_all(timeout=5)
        ...     print(f"Killed {result['success_count']} processes")
    """
    
    def __init__(self, process_name: str, enable_logging: bool = True):
        """
        Initialize ProcessManager with a target process name.
        
        Args:
            process_name: Name of the process to manage (e.g., 'chrome.exe')
            enable_logging: Enable logging output (default: True)
            
        Examples:
            >>> manager = ProcessManager("notepad.exe")
            >>> manager = ProcessManager("python.exe", enable_logging=False)
        """
        self.process_name = process_name
        self._cache = None
        self._cache_time = 0
        self._cache_duration = 1  # seconds
        self._logger = logging.getLogger(f"ProcessManager.{process_name}")
        if not enable_logging:
            self._logger.disabled = True
            
    def _get_processes(self, use_cache: bool = True) -> List[Dict]:
        """
        Retrieve list of all processes with caching mechanism.
        
        Args:
            use_cache: Use cached results if available (default: True)
            
        Returns:
            List of process dictionaries containing 'pid' and 'name'
            
        Note:
            Cache is invalidated after 1 second to ensure fresh data when needed
        """
        if use_cache and self._cache and (time.time() - self._cache_time < self._cache_duration):
            return self._cache
            
        processes = []
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
        self._cache = processes
        self._cache_time = time.time()
        return processes
    
    def get_pids(self) -> List[int]:
        """
        Get all process IDs matching the target process name.
        
        Returns:
            List of process IDs (PIDs)
            
        Examples:
            >>> manager = ProcessManager("chrome.exe")
            >>> pids = manager.get_pids()
            >>> print(f"Found {len(pids)} Chrome processes")
        """
        pids = []
        for proc_info in self._get_processes():
            if proc_info.get("name") == self.process_name:
                pid = proc_info.get("pid")
                if pid:
                    pids.append(pid)
        return pids
    
    @property
    def count(self) -> int:
        """
        Get the number of running processes matching the target name.
        
        Returns:
            Number of running processes
            
        Examples:
            >>> manager = ProcessManager("firefox.exe")
            >>> print(f"Firefox has {manager.count} running instances")
        """
        return len(self.get_pids())
    
    def is_running(self) -> bool:
        """
        Check if any process with the target name is running.
        
        Returns:
            True if at least one process is running, False otherwise
            
        Examples:
            >>> manager = ProcessManager("explorer.exe")
            >>> if manager.is_running():
            ...     print("Explorer is running")
        """
        return self.count > 0
    
    def kill_all(self, timeout: int = 5, force: bool = False) -> Dict[str, Union[str, List[int], int]]:
        """
        Terminate or kill all processes matching the target name.
        
        This method attempts to gracefully terminate processes first. If force is True
        or if processes don't terminate within the timeout, they will be killed forcefully.
        
        Args:
            timeout: Maximum time to wait for graceful termination (seconds)
            force: If True, use kill() instead of terminate() (default: False)
            
        Returns:
            Dictionary containing operation results with keys:
            - status: Operation status ('completed', 'no_process')
            - process_name: Name of the target process
            - killed: List of successfully killed PIDs
            - failed: List of PIDs that failed to kill
            - total: Total number of processes found
            - success_count: Number of successfully killed processes
            - failed_count: Number of failed kills
            
        Examples:
            >>> manager = ProcessManager("chrome.exe")
            >>> result = manager.kill_all(timeout=3, force=False)
            >>> if result['success_count'] > 0:
            ...     print(f"Successfully killed {result['success_count']} processes")
        """
        if not self.is_running():
            return {
                'status': 'no_process',
                'process_name': self.process_name,
                'killed': [],
                'failed': [],
                'total': 0,
                'success_count': 0,
                'failed_count': 0,
                'message': f'Process {self.process_name} not found'
            }
            
        pids = self.get_pids()
        killed = []
        failed = []
        
        for pid in pids:
            try:
                proc = psutil.Process(pid)
                
                # Choose termination method
                if force:
                    proc.kill()
                    method = 'kill'
                else:
                    proc.terminate()
                    method = 'terminate'
                
                # Wait for process to terminate
                try:
                    proc.wait(timeout)
                    killed.append(pid)
                    self._logger.info(f"✅ Process {pid} {method}ed successfully")
                except psutil.TimeoutExpired:
                    # Force kill if graceful termination timed out
                    if not force:
                        self._logger.warning(f"⏰ Timeout for PID {pid}, forcing kill")
                        proc.kill()
                        try:
                            proc.wait(2)
                            killed.append(pid)
                            self._logger.info(f"✅ Process {pid} killed after timeout")
                        except:
                            failed.append(pid)
                            self._logger.error(f"❌ Failed to force kill PID {pid}")
                    else:
                        failed.append(pid)
                        self._logger.warning(f"⏰ Timeout waiting for process {pid}")
                        
            except psutil.NoSuchProcess:
                self._logger.info(f"ℹ️ Process {pid} already terminated")
                killed.append(pid)
            except psutil.AccessDenied:
                failed.append(pid)
                self._logger.error(f"⛔ Access denied for process {pid}")
            except Exception as e:
                failed.append(pid)
                self._logger.error(f"❌ Error killing process {pid}: {e}")
                
        return {
            'status': 'completed',
            'process_name': self.process_name,
            'killed': killed,
            'failed': failed,
            'total': len(pids),
            'success_count': len(killed),
            'failed_count': len(failed)
        }
    
    def get_detailed_info(self) -> List[Dict]:
        """
        Get comprehensive information about all matching processes.
        
        Returns:
            List of dictionaries containing detailed process information including:
            - pid: Process ID
            - name: Process name
            - exe: Executable path
            - cmdline: Command line arguments
            - cwd: Current working directory
            - username: Process owner
            - create_time: Creation timestamp (ISO format)
            - cpu_percent: CPU usage percentage
            - memory_percent: Memory usage percentage
            - memory_mb: Memory usage in megabytes
            - status: Process status (running, sleeping, etc.)
            - num_threads: Number of threads
            - connections: Number of network connections
            - open_files: Number of open files
            - ppid: Parent process ID
            
        Examples:
            >>> manager = ProcessManager("python.exe")
            >>> info = manager.get_detailed_info()
            >>> for proc in info:
            ...     print(f"PID {proc['pid']}: {proc['memory_mb']:.2f} MB")
        """
        info_list = []
        for pid in self.get_pids():
            try:
                proc = psutil.Process(pid)
                info = {
                    'pid': pid,
                    'name': proc.name(),
                    'exe': proc.exe(),
                    'cmdline': ' '.join(proc.cmdline()),
                    'cwd': proc.cwd(),
                    'username': proc.username(),
                    'create_time': datetime.fromtimestamp(proc.create_time()).isoformat(),
                    'cpu_percent': proc.cpu_percent(interval=0.1),
                    'memory_percent': proc.memory_percent(),
                    'memory_mb': round(proc.memory_info().rss / 1024 / 1024, 2),
                    'status': proc.status(),
                    'num_threads': proc.num_threads(),
                    'connections': len(proc.connections()),
                    'open_files': len(proc.open_files()),
                    'ppid': proc.ppid()
                }
                info_list.append(info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return info_list
    
    def suspend_all(self) -> List[int]:
        """
        Suspend all matching processes.
        
        Suspended processes will not consume CPU time until resumed.
        
        Returns:
            List of successfully suspended PIDs
            
        Examples:
            >>> manager = ProcessManager("heavy_task.exe")
            >>> suspended = manager.suspend_all()
            >>> print(f"Suspended {len(suspended)} processes")
        """
        suspended = []
        for pid in self.get_pids():
            try:
                proc = psutil.Process(pid)
                proc.suspend()
                suspended.append(pid)
                self._logger.info(f"⏸️ Process {pid} suspended")
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                self._logger.error(f"Failed to suspend PID {pid}: {e}")
                continue
        return suspended
    
    def resume_all(self) -> List[int]:
        """
        Resume all suspended processes.
        
        Returns:
            List of successfully resumed PIDs
            
        Examples:
            >>> manager = ProcessManager("heavy_task.exe")
            >>> resumed = manager.resume_all()
            >>> print(f"Resumed {len(resumed)} processes")
        """
        resumed = []
        for pid in self.get_pids():
            try:
                proc = psutil.Process(pid)
                proc.resume()
                resumed.append(pid)
                self._logger.info(f"▶️ Process {pid} resumed")
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                self._logger.error(f"Failed to resume PID {pid}: {e}")
                continue
        return resumed
    
    def get_parent_process(self) -> Optional[Dict]:
        """
        Get information about the parent process.
        
        Returns:
            Dictionary with parent process info or None if not found:
            - pid: Parent process ID
            - name: Parent process name
            - cmdline: Parent command line
            
        Examples:
            >>> manager = ProcessManager("child_process.exe")
            >>> parent = manager.get_parent_process()
            >>> if parent:
            ...     print(f"Parent: {parent['name']} (PID: {parent['pid']})")
        """
        pids = self.get_pids()
        if not pids:
            return None
            
        try:
            proc = psutil.Process(pids[0])
            parent = proc.parent()
            if parent:
                return {
                    'pid': parent.pid,
                    'name': parent.name(),
                    'cmdline': ' '.join(parent.cmdline())
                }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
        return None
    
    def get_process_tree(self) -> List[Dict]:
        """
        Get the process tree including child processes.
        
        Returns:
            List of dictionaries containing process hierarchy:
            - pid: Process ID
            - name: Process name
            - children: List of child processes with pid and name
            
        Examples:
            >>> manager = ProcessManager("chrome.exe")
            >>> tree = manager.get_process_tree()
            >>> for proc in tree:
            ...     print(f"Process {proc['pid']} has {len(proc['children'])} children")
        """
        tree = []
        for pid in self.get_pids():
            try:
                proc = psutil.Process(pid)
                children = proc.children(recursive=True)
                tree.append({
                    'pid': pid,
                    'name': proc.name(),
                    'children': [
                        {'pid': child.pid, 'name': child.name()}
                        for child in children
                    ]
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return tree
    
    def wait_for_exit(self, timeout: int = 30, check_interval: float = 0.5) -> bool:
        """
        Wait for all matching processes to exit.
        
        Args:
            timeout: Maximum time to wait (seconds)
            check_interval: Time between checks (seconds)
            
        Returns:
            True if all processes exited within timeout, False otherwise
            
        Examples:
            >>> manager = ProcessManager("temp_process.exe")
            >>> if manager.wait_for_exit(timeout=10):
            ...     print("All processes exited gracefully")
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            if not self.is_running():
                return True
            time.sleep(check_interval)
        return False
    
    def clear_cache(self) -> None:
        """Clear the process cache to force fresh data retrieval."""
        self._cache = None
        self._cache_time = 0


