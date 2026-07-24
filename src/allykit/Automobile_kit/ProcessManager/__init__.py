from .ProcessManager import ProcessManager
from typing import List, Dict


def kill_process(process_name: str, timeout: int = 5, force: bool = False) -> Dict:
    """
    Kill or terminate a process by name.
    
    Args:
        process_name: Name of the process to kill
        timeout: Timeout for graceful termination
        force: Force kill if True
        
    Returns:
        Operation result dictionary
        
    Examples:
        >>> result = kill_process("notepad.exe", timeout=3)
        >>> print(f"Killed {result['success_count']} processes")
    """
    manager = ProcessManager(process_name)
    return manager.kill_all(timeout=timeout, force=force)


def kill_chrome(timeout: int = 5, force: bool = False) -> Dict:
    """Kill all Google Chrome processes."""
    return kill_process("chrome.exe", timeout, force)


def kill_chrome_driver(timeout: int = 5, force: bool = False) -> Dict:
    """Kill all ChromeDriver processes."""
    return kill_process("chromedriver.exe", timeout, force)


def kill_firefox(timeout: int = 5, force: bool = False) -> Dict:
    """Kill all Firefox processes."""
    return kill_process("firefox.exe", timeout, force)


def kill_edge(timeout: int = 5, force: bool = False) -> Dict:
    """Kill all Microsoft Edge processes."""
    return kill_process("msedge.exe", timeout, force)


def kill_multiple(process_names: List[str], timeout: int = 5, force: bool = False) -> Dict[str, Dict]:
    """
    Kill multiple processes by name.
    
    Args:
        process_names: List of process names to kill
        timeout: Timeout for graceful termination
        force: Force kill if True
        
    Returns:
        Dictionary mapping process names to their kill results
        
    Examples:
        >>> results = kill_multiple(["chrome.exe", "firefox.exe"], timeout=3)
        >>> for name, result in results.items():
        ...     print(f"{name}: {result['success_count']} killed")
    """
    results = {}
    for name in process_names:
        results[name] = kill_process(name, timeout, force)
    return results


def kill_all_browsers(timeout: int = 5, force: bool = False) -> Dict[str, Dict]:
    """
    Kill all common browser processes.
    
    Kills: Chrome, Firefox, Edge, and ChromeDriver processes.
    
    Args:
        timeout: Timeout for graceful termination
        force: Force kill if True
        
    Returns:
        Dictionary mapping browser names to their kill results
        
    Examples:
        >>> results = kill_all_browsers(timeout=2, force=True)
        >>> for browser, result in results.items():
        ...     print(f"{browser}: {result['success_count']} processes killed")
    """
    browsers = ["chrome.exe", "chromedriver.exe", "firefox.exe", "msedge.exe"]
    return kill_multiple(browsers, timeout, force)


def get_process_info(process_name: str) -> List[Dict]:
    """
    Get detailed information about a process.
    
    Args:
        process_name: Name of the process to inspect
        
    Returns:
        List of detailed process information dictionaries
        
    Examples:
        >>> info = get_process_info("python.exe")
        >>> for proc in info:
        ...     print(f"PID {proc['pid']} uses {proc['memory_mb']} MB")
    """
    manager = ProcessManager(process_name)
    return manager.get_detailed_info()


def is_process_running(process_name: str) -> bool:
    """
    Check if a process is currently running.
    
    Args:
        process_name: Name of the process to check
        
    Returns:
        True if the process is running, False otherwise
        
    Examples:
        >>> if is_process_running("chrome.exe"):
        ...     print("Chrome is running")
    """
    manager = ProcessManager(process_name)
    return manager.is_running()


def count_processes(process_name: str) -> int:
    """
    Count the number of running instances of a process.
    
    Args:
        process_name: Name of the process to count
        
    Returns:
        Number of running instances
        
    Examples:
        >>> count = count_processes("notepad.exe")
        >>> print(f"Notepad instances: {count}")
    """
    manager = ProcessManager(process_name)
    return manager.count


def get_process_pids(process_name: str) -> List[int]:
    """
    Get all PIDs for a process name.
    
    Args:
        process_name: Name of the process
        
    Returns:
        List of process IDs
        
    Examples:
        >>> pids = get_process_pids("chrome.exe")
        >>> print(f"Chrome PIDs: {pids}")
    """
    manager = ProcessManager(process_name)
    return manager.get_pids()


def suspend_process(process_name: str) -> List[int]:
    """
    Suspend all instances of a process.
    
    Args:
        process_name: Name of the process to suspend
        
    Returns:
        List of suspended PIDs
        
    Examples:
        >>> suspended = suspend_process("heavy_task.exe")
        >>> print(f"Suspended {len(suspended)} processes")
    """
    manager = ProcessManager(process_name)
    return manager.suspend_all()


def resume_process(process_name: str) -> List[int]:
    """
    Resume all suspended instances of a process.
    
    Args:
        process_name: Name of the process to resume
        
    Returns:
        List of resumed PIDs
        
    Examples:
        >>> resumed = resume_process("heavy_task.exe")
        >>> print(f"Resumed {len(resumed)} processes")
    """
    manager = ProcessManager(process_name)
    return manager.resume_all()


# Convenience aliases
kill = kill_process
terminate = kill_process
close = kill_process

# Browser-specific aliases
close_chrome = kill_chrome
close_firefox = kill_firefox
close_edge = kill_edge
close_chrome_driver = kill_chrome_driver
close_all_browsers = kill_all_browsers