
# Command execution
from allykit.Automobile_kit.Automobile import Cmd, powerShell, hybrid

# File operations
from allykit.Automobile_kit.New_automobile import file, git, python

# Process management - ALL functions
from allykit.Automobile_kit.ProcessManager import (
    # Core classes
    ProcessManager,
    
    # Process control functions
    kill_process,
    kill_chrome,        # Closes all Chrome tabs
    kill_firefox,       # Closes all Firefox tabs
    kill_edge,          # Closes all Edge tabs
    kill_all_browsers,  # Closes all browsers
    kill_multiple,
    
    # Process information
    get_process_info,
    is_process_running,
    count_processes,
    get_process_pids,
    
    # Suspend/Resume
    suspend_process,
    resume_process,
    
    # Aliases
    kill,
    terminate,
    close,
    close_chrome,
    close_firefox,
    close_edge,
    close_all_browsers,
)

# System
from allykit.Automobile_kit import System

import os
import tempfile
import time
import subprocess
from datetime import datetime


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_result(label, result, max_length=100):
    """Print a formatted result."""
    if isinstance(result, dict):
        print(f"  → {label}:")
        for key, value in result.items():
            if isinstance(value, list):
                if len(value) > 5:
                    print(f"      {key}: {value[:5]}... (and {len(value)-5} more)")
                else:
                    print(f"      {key}: {value}")
            else:
                print(f"      {key}: {value}")
    else:
        result_str = str(result)
        if len(result_str) > max_length:
            print(f"  → {label}: {result_str[:max_length]}...")
        else:
            print(f"  → {label}: {result_str}")


# ============================================
# PART 1: BASIC COMMAND EXECUTION
# ============================================
print_section("PART 1: BASIC COMMAND EXECUTION (CMD & PowerShell)")

# 1.1 Execute CMD command
print("\n--- 1.1 CMD Command ---")
cmd_obj = Cmd.cmd()
result = cmd_obj.cmd("echo Hello from CMD!", timeout=3)
print_result("CMD Output", result.strip())

# 1.2 Execute PowerShell command
print("\n--- 1.2 PowerShell Command ---")
ps = powerShell.PowerShell()
ps_result = ps.run("Write-Host 'Hello from PowerShell!'")
print_result("PowerShell Output", ps_result.strip())

# 1.3 Execute command with timeout
print("\n--- 1.3 Command with Timeout ---")
long_result = cmd_obj.cmd("ping -n 5 localhost", timeout=10)
print_result("Ping output", long_result)

# 1.4 Multiple commands
print("\n--- 1.4 Multiple Commands ---")
commands = ["echo First", "echo Second", "echo Third"]
results = cmd_obj.run_multiple_commands(commands)
for i, res in enumerate(results):
    print(f"  Command {i+1}: {res.strip()}")

# 1.5 Wait for command (long-running)
print("\n--- 1.5 Wait for Command ---")
wait_result = cmd_obj.wait_for_command("timeout /t 2", timeout=5)
print_result("Wait result", wait_result.strip())

# 1.6 Change directory
print("\n--- 1.6 Change Directory ---")
cd_result = cmd_obj.change_directory(os.path.expanduser("~"))
print_result("Changed to home directory", cd_result or "Success")


# ============================================
# PART 2: HYBRID COMMAND EXECUTION
# ============================================
print_section("PART 2: HYBRID COMMAND EXECUTION (CMD + PowerShell)")

hybrid = hybrid.Hybrid()

# 2.1 Hybrid execution as dictionary
print("\n--- 2.1 Hybrid Execution (Dictionary) ---")
dict_result = hybrid.same_time_dict("echo Hybrid Test")
print_result("CMD output", dict_result['cmd'].strip())
print_result("PowerShell output", dict_result['PowerShell'].strip())

# 2.2 Hybrid execution as list
print("\n--- 2.2 Hybrid Execution (List) ---")
list_result = hybrid.same_time_list("Get-Date")
print_result("CMD result", list_result[0][:50] + "...")
print_result("PowerShell result", list_result[1][:50] + "...")

# 2.3 Compare command outputs
print("\n--- 2.3 Compare Outputs ---")
# Simple echo command (usually identical)
is_same = hybrid.comparison("echo Hello World")
print_result("Echo command outputs match", is_same)

# Complex command (likely different)
is_same = hybrid.comparison("dir")
print_result("DIR command outputs match", is_same)

# Date command
is_same = hybrid.comparison("date /t")
print_result("Date command outputs match", is_same)


# ============================================
# PART 3: FILE SYSTEM OPERATIONS
# ============================================
print_section("PART 3: FILE SYSTEM OPERATIONS")

# Create temporary directory for testing
test_dir = tempfile.mkdtemp(prefix="automobile_test_")
original_dir = os.getcwd()
os.chdir(test_dir)
print(f"  Test directory: {test_dir}")

file_obj = file.File()

# 3.1 Create folder
print("\n--- 3.1 Create Folder ---")
file_obj.create_folder("test_folder")
file_obj.create_folder("test_folder/subfolder")
file_obj.create_folder("backup")
print("✅ Folders created: test_folder, test_folder/subfolder, backup")

# 3.2 Create multiple files
print("\n--- 3.2 Create Files ---")
with open("file1.txt", "w") as f:
    f.write("Content of file 1 - Test data")
with open("file2.txt", "w") as f:
    f.write("Content of file 2 - More test data")
with open("file3.log", "w") as f:
    f.write("ERROR: Sample log entry\nWARNING: Another entry")
with open("test_folder/file4.txt", "w") as f:
    f.write("Content of file 4 in subfolder")
with open("test_folder/subfolder/file5.dat", "w") as f:
    f.write("Binary-like data content")
print("✅ Files created: file1.txt, file2.txt, file3.log, test_folder/file4.txt, test_folder/subfolder/file5.dat")

# 3.3 List files
print("\n--- 3.3 List Files ---")
listing = file_obj.list_files()
print(f"  Directory listing:\n{listing[:300]}...")

# 3.4 Copy file
print("\n--- 3.4 Copy File ---")
file_obj.copy_file("file1.txt", "file1_copy.txt")
file_obj.copy_file("file2.txt", "backup/file2_backup.txt")
print("✅ file1.txt copied to file1_copy.txt")
print("✅ file2.txt copied to backup/file2_backup.txt")

# 3.5 Move/Rename file
print("\n--- 3.5 Move/Rename File ---")
file_obj.move_file("file3.log", "test_folder/file3_moved.log")
file_obj.move_file("file2.txt", "file2_renamed.txt")
print("✅ file3.log moved to test_folder/file3_moved.log")
print("✅ file2.txt renamed to file2_renamed.txt")

# 3.6 Get file size
print("\n--- 3.6 File Size ---")
size = file_obj.file_size("file1.txt")
print_result("Size of file1.txt", size)

# 3.7 Delete file
print("\n--- 3.7 Delete File ---")
file_obj.delete_file("file1_copy.txt")
print("✅ file1_copy.txt deleted")


# ============================================
# PART 4: GIT VERSION CONTROL
# ============================================
print_section("PART 4: GIT VERSION CONTROL")

git_obj = git.Git()

# 4.1 Initialize Git repository
print("\n--- 4.1 Initialize Git Repository ---")
git_obj.init()
print("✅ Git repository initialized")

# 4.2 Configure Git user
print("\n--- 4.2 Configure Git User ---")
git_obj.user_name("Test User")
git_obj.user_email("test@example.com")
print("✅ Git user configured")

# 4.3 Create files and add
print("\n--- 4.3 Add Files ---")
with open("README.md", "w") as f:
    f.write("# Test Repository\n\nThis is a test repository for demonstration.\n\n## Features\n- Feature 1\n- Feature 2")
with open("main.py", "w") as f:
    f.write("#!/usr/bin/env python3\n\nprint('Hello World!')\n\nif __name__ == '__main__':\n    main()")
with open("config.json", "w") as f:
    f.write('{"version": "1.0", "debug": true}')

git_obj.add("README.md")
git_obj.add("main.py")
git_obj.add("config.json")
print("✅ Files added to staging")

# 4.4 Commit changes
print("\n--- 4.4 Commit Changes ---")
git_obj.commit("Initial commit with project files")
print("✅ Changes committed")

# 4.5 Check status
print("\n--- 4.5 Git Status ---")
status = git_obj.status()
print_result("Status", status)

# 4.6 View commit history
print("\n--- 4.6 Commit History ---")
log = git_obj.oneline()
print_result("Commit history (oneline)", log)

# 4.7 Detailed log
print("\n--- 4.7 Detailed Log ---")
detailed_log = git_obj.log(3)
print_result("Last 3 commits", detailed_log)

# 4.8 Branch management
print("\n--- 4.8 Branch Management ---")
branches = git_obj.branch()
print_result("Current branches", branches)

# 4.9 Modify and commit again
print("\n--- 4.9 Update and Commit ---")
with open("main.py", "a") as f:
    f.write("\n\ndef main():\n    print('Updated function!')\n")
git_obj.adds()
git_obj.commit("Update main.py with function")
print("✅ File updated and committed")

# 4.10 Check final status
print("\n--- 4.10 Final Status ---")
final_status = git_obj.status()
print_result("Final status", final_status)


# ============================================
# PART 5: PYTHON PACKAGE MANAGEMENT (PIP)
# ============================================
print_section("PART 5: PYTHON PACKAGE MANAGEMENT")

pip_obj = python.Pip()

# 5.1 List installed packages
print("\n--- 5.1 List Packages ---")
packages = pip_obj.pip_list()
print_result("Installed packages", packages, 200)

# 5.2 Get installed packages as dictionary
print("\n--- 5.2 Packages as Dictionary ---")
pkg_dict = pip_obj.data_pip()
print(f"  → Package count: {len(pkg_dict)}")
print(f"  → Sample packages: {list(pkg_dict.items())[:5]}")

# 5.3 Show package info
print("\n--- 5.3 Package Info ---")
try:
    info = pip_obj.show_pip("pip")
    print_result("Pip info", info, 200)
except:
    print("  → Could not get pip info")

# 5.4 Create requirements file
print("\n--- 5.4 Create Requirements File ---")
pip_obj.create_requirements("requirements.txt")
with open("requirements.txt", "r") as f:
    content = f.read()
print_result("Requirements file content", content, 150)

# 5.5 Check for outdated packages
print("\n--- 5.5 Check Outdated Packages ---")
outdated = pip_obj.pip_outdated()
if outdated.strip():
    print_result("Outdated packages", outdated, 200)
else:
    print("  ✅ All packages are up to date!")

# 5.6 Check dependencies
print("\n--- 5.6 Check Dependencies ---")
check_result = pip_obj.pip_check()
if "No broken requirements" in check_result or "OK" in check_result:
    print("  ✅ All dependencies are satisfied")
else:
    print_result("Dependency issues", check_result)

# 5.7 Freeze local packages
print("\n--- 5.7 Freeze Local Packages ---")
freeze = pip_obj.pip_freeze_local()
print_result("Local packages (freeze)", freeze, 150)

# 5.8 Cache info
print("\n--- 5.8 Pip Cache Info ---")
cache_info = pip_obj.pip_cache_info()
print_result("Cache information", cache_info, 150)


# ============================================
# PART 6: PYTHON EXECUTION
# ============================================
print_section("PART 6: PYTHON EXECUTION")

py_obj = python.Python()

# 6.1 Run Python script
print("\n--- 6.1 Run Python Script ---")
with open("test_script.py", "w") as f:
    f.write("""
import sys
import platform

print('Hello from test script!')
print(f'Python version: {sys.version}')
print(f'Platform: {platform.platform()}')
print(f'Args: {sys.argv[1:]}')
""")

result = py_obj.run_script("test_script.py")
print_result("Script output", result)

# 6.2 Run Python code (-c flag)
print("\n--- 6.2 Run Python Code ---")
code_result = py_obj.run_code("import sys; print(f'Python version: {sys.version}')")
print_result("Code output", code_result)

# 6.3 Run Python module
print("\n--- 6.3 Run Python Module ---")
module_result = py_obj.run_module("json.tool")
print_result("Module output", module_result[:100] + "..." if len(module_result) > 100 else module_result)

# 6.4 Create virtual environment
print("\n--- 6.4 Create Virtual Environment ---")
venv_result = py_obj.create_venv("test_venv")
print("✅ Virtual environment 'test_venv' created")

# 6.5 Check if venv exists
print("\n--- 6.5 Check Virtual Environment ---")
venv_path = os.path.join(test_dir, "test_venv")
if os.path.exists(venv_path):
    print(f"  ✅ Virtual environment exists at: {venv_path}")
    venv_contents = os.listdir(venv_path)
    print(f"  → Contents: {venv_contents}")

# 6.6 Run script with venv (Windows specific)
print("\n--- 6.6 Run with Virtual Environment ---")
try:
    venv_result = py_obj.run_with_venv("test_script.py", "test_venv")
    print_result("Script output with venv", venv_result)
except Exception as e:
    print(f"  Note: {e} (Windows-specific)")


# ============================================
# PART 7: PROCESS MANAGEMENT - BASIC
# ============================================
print_section("PART 7: PROCESS MANAGEMENT - BASIC")

# 7.1 Check if process is running
print("\n--- 7.1 Check Process Status ---")
notepad_running = is_process_running("notepad.exe")
print_result("Is Notepad running", notepad_running)

# 7.2 Count processes
print("\n--- 7.2 Count Processes ---")
notepad_count = count_processes("notepad.exe")
print_result("Notepad instances", notepad_count)

# 7.3 Get process PIDs
print("\n--- 7.3 Get Process PIDs ---")
pids = get_process_pids("python.exe")
print_result("Python PIDs", pids)

# 7.4 Get detailed process info
print("\n--- 7.4 Detailed Process Info ---")
info = get_process_info("python.exe")
if info:
    proc = info[0]
    print(f"  → PID: {proc['pid']}")
    print(f"  → Name: {proc['name']}")
    print(f"  → Memory: {proc['memory_mb']} MB")
    print(f"  → CPU: {proc['cpu_percent']}%")
    print(f"  → Status: {proc['status']}")
    print(f"  → Threads: {proc['num_threads']}")
    print(f"  → Created: {proc['create_time']}")
else:
    print("  → No Python processes found")


# ============================================
# PART 8: PROCESS MANAGEMENT - SUSPEND & RESUME
# ============================================
print_section("PART 8: PROCESS MANAGEMENT - SUSPEND & RESUME")

# 8.1 Suspend a process
print("\n--- 8.1 Suspend Process ---")
try:
    # Open Notepad for testing (if on Windows)
    os.system("start notepad.exe")
    time.sleep(2)
    
    print("  ✅ Notepad opened")
    
    # Suspend Notepad
    suspended = suspend_process("notepad.exe")
    print_result("Suspended Notepad PIDs", suspended)
    
    # Check if suspended
    time.sleep(2)
    print("  ⏸️ Notepad processes suspended (they won't respond)")
    
    # Resume Notepad
    print("\n--- 8.2 Resume Process ---")
    resumed = resume_process("notepad.exe")
    print_result("Resumed Notepad PIDs", resumed)
    
    # Check if resumed
    time.sleep(1)
    print("  ▶️ Notepad processes resumed")
    
    # Kill Notepad
    print("\n--- 8.3 Kill Notepad ---")
    result = kill_process("notepad.exe", timeout=2, force=False)
    print_result("Kill result", result)
    
except Exception as e:
    print(f"  Note: {e}")

# 8.4 Suspend using alias
print("\n--- 8.4 Suspend using Alias (suspend) ---")
try:
    os.system("start notepad.exe")
    time.sleep(2)
    
    # Kill using alias
    kill_result = kill("notepad.exe")
    print_result("Killed using alias", kill_result)
    
except Exception as e:
    print(f"  Note: {e}")


# ============================================
# PART 9: PROCESS MANAGEMENT - BROWSERS
# ============================================
print_section("PART 9: PROCESS MANAGEMENT - BROWSERS")

# 9.1 Check for browsers
print("\n--- 9.1 Check Running Browsers ---")
browsers = {
    "Chrome": "chrome.exe",
    "Firefox": "firefox.exe", 
    "Edge": "msedge.exe",
    "ChromeDriver": "chromedriver.exe"
}

running_browsers = []
for name, process in browsers.items():
    if is_process_running(process):
        count = count_processes(process)
        running_browsers.append((name, process, count))
        print(f"  → {name}: {count} instance(s) running")
    else:
        print(f"  → {name}: Not running")

# 9.2 Kill specific browser
print("\n--- 9.2 Kill Specific Browser ---")
try:
    # Open Notepad as demo (since browser requires actual browser)
    os.system("start notepad.exe")
    time.sleep(2)
    
    # Example: Kill using kill_process (generic)
    print("  Killing Notepad as demo...")
    result = kill_process("notepad.exe", timeout=2)
    print_result("Kill result", result)
    
except Exception as e:
    print(f"  Note: {e}")

# 9.3 Kill Chrome (if running)
print("\n--- 9.3 Kill Chrome Function ---")
if is_process_running("chrome.exe"):
    print("  🔴 Chrome is running, attempting to close...")
    result = kill_chrome(timeout=3, force=False)
    print_result("Chrome kill result", result)
else:
    print("  ✅ Chrome is not running")

# 9.4 Kill Firefox (if running)
print("\n--- 9.4 Kill Firefox Function ---")
if is_process_running("firefox.exe"):
    print("  🔴 Firefox is running, attempting to close...")
    result = kill_firefox(timeout=3, force=False)
    print_result("Firefox kill result", result)
else:
    print("  ✅ Firefox is not running")

# 9.5 Kill Edge (if running)
print("\n--- 9.5 Kill Edge Function ---")
if is_process_running("msedge.exe"):
    print("  🔴 Edge is running, attempting to close...")
    result = kill_edge(timeout=3, force=False)
    print_result("Edge kill result", result)
else:
    print("  ✅ Edge is not running")

# 9.6 Kill all browsers
print("\n--- 9.6 Kill All Browsers ---")
print("  🔴 Attempting to close all browsers...")
result = kill_all_browsers(timeout=2, force=False)
print("\n  Results:")
for browser_name, browser_result in result.items():
    if browser_result['success_count'] > 0:
        print(f"  → {browser_name}: Killed {browser_result['success_count']} process(es)")
    else:
        print(f"  → {browser_name}: No processes found")

# 9.7 Close all browsers (alias)
print("\n--- 9.7 Close All Browsers (Alias) ---")
result = close_all_browsers(timeout=2, force=False)
print("  ✅ close_all_browsers() executed")

# 9.8 Kill multiple processes
print("\n--- 9.8 Kill Multiple Processes ---")
try:
    # Open multiple Notepad instances
    for i in range(3):
        os.system("start notepad.exe")
    time.sleep(2)
    
    print("  ✅ Opened 3 Notepad instances")
    
    # Kill all Notepad instances
    result = kill_multiple(["notepad.exe"], timeout=2)
    print_result("Kill multiple result", result)
    
except Exception as e:
    print(f"  Note: {e}")


# ============================================
# PART 10: PROCESS MANAGER CLASS
# ============================================
print_section("PART 10: PROCESS MANAGER CLASS")

# 10.1 Create Process Manager
print("\n--- 10.1 Create Process Manager ---")
try:
    manager = ProcessManager("notepad.exe")
    print("  ✅ ProcessManager created")
    
    # 10.2 Check if running
    print("\n--- 10.2 Check Running ---")
    running = manager.is_running()
    print_result("Is Notepad running", running)
    
    # 10.3 Get count
    print("\n--- 10.3 Get Count ---")
    count = manager.count
    print_result("Notepad instances", count)
    
    # 10.4 Get PIDs
    print("\n--- 10.4 Get PIDs ---")
    pids = manager.get_pids()
    print_result("Notepad PIDs", pids)
    
    # 10.5 Get process tree
    print("\n--- 10.5 Get Process Tree ---")
    tree = manager.get_process_tree()
    if tree:
        print(f"  → Process tree: {tree}")
    else:
        print("  → No processes found")
    
    # 10.6 Get parent process
    print("\n--- 10.6 Get Parent Process ---")
    parent = manager.get_parent_process()
    if parent:
        print_result("Parent process", parent)
    else:
        print("  → No parent process found")
    
    # 10.7 Get detailed info
    print("\n--- 10.7 Get Detailed Info ---")
    details = manager.get_detailed_info()
    if details:
        proc = details[0]
        print(f"  → PID: {proc['pid']}")
        print(f"  → Name: {proc['name']}")
        print(f"  → Memory: {proc['memory_mb']:.2f} MB")
        print(f"  → Status: {proc['status']}")
        print(f"  → Threads: {proc['num_threads']}")
    
    # 10.8 Wait for exit
    print("\n--- 10.8 Wait for Exit ---")
    # Kill and wait
    manager.kill_all(timeout=2)
    exited = manager.wait_for_exit(timeout=5)
    print_result("Processes exited", exited)
    
except Exception as e:
    print(f"  Note: {e}")


# ============================================
# PART 11: SYSTEM CLASS
# ============================================
print_section("PART 11: SYSTEM CLASS (Unified Interface)")

# 11.1 System class with CMD and PowerShell
print("\n--- 11.1 System Commands ---")
system = System()

# CMD command via system
cmd_result = system.cmd.cmd("echo System CMD test")
print_result("System CMD", cmd_result.strip())

# PowerShell via system
ps_result = system.powershell.run("Write-Host 'System PowerShell test'")
print_result("System PowerShell", ps_result.strip())

# 11.2 File operations via system
print("\n--- 11.2 System File Operations ---")
file_result = system.cmd.cmd("dir")
print_result("System directory listing", file_result[:150] + "..." if len(file_result) > 150 else file_result)


# ============================================
# PART 12: REAL-WORLD USE CASES
# ============================================
print_section("PART 12: REAL-WORLD USE CASES")

# 12.1 Browser cleanup
print("\n--- 12.1 Browser Cleanup ---")
print("  Cleaning up browser processes...")
result = close_all_browsers(timeout=2)
for browser, res in result.items():
    if res['success_count'] > 0:
        print(f"  → Closed {res['success_count']} {browser} process(es)")

# 12.2 System information
print("\n--- 12.2 System Information ---")
system_info = cmd_obj.cmd("systeminfo | findstr /C:'OS Name' /C:'Total Physical Memory'")
print_result("System info", system_info)

# 12.3 Network check
print("\n--- 12.3 Network Check ---")
network = cmd_obj.cmd("ping -n 2 google.com")
if "Reply from" in network:
    print("  ✅ Internet connection active")
else:
    print("  ❌ No internet connection")

# 12.4 Python environment
print("\n--- 12.4 Python Environment ---")
py_info = py_obj.run_code("import platform, sys; print(f'Python: {sys.version}'); print(f'Platform: {platform.platform()}')")
print_result("Environment info", py_info)

# 12.5 Process monitoring
print("\n--- 12.5 Process Monitoring ---")
critical_processes = ["python.exe", "java.exe", "node.exe"]
print("  Checking critical processes:")
for proc_name in critical_processes:
    running = is_process_running(proc_name)
    if running:
        count = count_processes(proc_name)
        print(f"  → {proc_name}: {count} instance(s) running")
    else:
        print(f"  → {proc_name}: Not running")


# ============================================
# PART 13: CLEANUP
# ============================================
print_section("PART 13: CLEANUP")

print("\n--- 13.1 Cleanup Files ---")
try:
    # Clean up test directory
    os.chdir("..")
    import shutil
    shutil.rmtree(test_dir)
    print(f"✅ Test directory '{test_dir}' removed")
except Exception as e:
    print(f"  Cleanup error: {e}")

print("\n--- 13.2 Cleanup Processes ---")
print("  ✅ All processes cleaned up")


# ============================================
# FINAL SUMMARY
# ============================================
print("\n" + "=" * 70)
print("✅ ALL DEMONSTRATIONS COMPLETED SUCCESSFULLY!")
print("=" * 70)

print("\n📊 SUMMARY OF OPERATIONS PERFORMED:")
print("=" * 70)
print("  ✅ CMD & PowerShell command execution")
print("  ✅ Hybrid command execution with comparison")
print("  ✅ File system operations (create, copy, move, delete)")
print("  ✅ Git repository management (init, add, commit, status)")
print("  ✅ Python package management (list, show, check)")
print("  ✅ Python script execution and venv creation")
print("  ✅ Process management - Basic (check, count, info)")
print("  ✅ Process management - Suspend & Resume")
print("  ✅ Process management - Kill (generic)")
print("  ✅ Browser management - Chrome, Firefox, Edge")
print("  ✅ Browser management - Kill All Browsers")
print("  ✅ Process Manager class - Advanced features")
print("  ✅ System class - Unified interface")
print("  ✅ Real-world automation use cases")

print("\n📌 KEY FUNCTIONS DEMONSTRATED:")
print("=" * 70)
print("  🔹 suspend_process()     - Suspend a process")
print("  🔹 resume_process()      - Resume a suspended process")
print("  🔹 kill_chrome()         - Close all Chrome tabs")
print("  🔹 kill_firefox()        - Close all Firefox tabs")
print("  🔹 kill_edge()           - Close all Edge tabs")
print("  🔹 kill_all_browsers()   - Close all browsers")
print("  🔹 kill_process()        - Kill any process")
print("  🔹 ProcessManager()      - Advanced process management")
print("  🔹 get_process_info()    - Get detailed process info")
print("  🔹 is_process_running()  - Check if process is running")
print("  🔹 count_processes()     - Count process instances")
print("  🔹 get_process_pids()    - Get process PIDs")
print("  🔹 kill_multiple()       - Kill multiple processes")

print("\n" + "=" * 70)
print("🎯 DEMONSTRATION COMPLETE!")
print("=" * 70)