# Command execution
from allykit.Automobile_kit.Automobile import Cmd, powerShell, hybrid
from  allykit.Automobile_kit.New_automobile import (
    # file operations
    file,
    
    # git operations
    git,
    
    # Package management
    python,
)
from allykit.Automobile_kit.ProcessManager import ( 
    # Process management
    ProcessManager,
    kill_process,
    kill_chrome, # It closes all open Chrome tabs. # kill_chrome()
    kill_firefox, # It closes all open firefox tabs.
    kill_edge, # It closes all open edge tabs.
    kill_all_browsers, # Closes all browsers.
    get_process_info,
    is_process_running,
    count_processes,
    suspend_process,
    resume_process,
    get_process_pids
)
from allykit.Automobile_kit import System
import os
import tempfile
import time
from datetime import datetime


# ============================================
# PART 1: BASIC COMMAND EXECUTION
# ============================================
print("=" * 70)
print("PART 1: BASIC COMMAND EXECUTION (CMD & PowerShell)")
print("=" * 70)

# 1.1 Execute CMD command
print("\n--- 1.1 CMD Command ---")
cmd_obj = Cmd.cmd()
result = cmd_obj.cmd("echo Hello from CMD!", timeout=3)
print(f"CMD Output: {result.strip()}")

# 1.2 Execute PowerShell command
print("\n--- 1.2 PowerShell Command ---")
ps_result = powerShell.PowerShell.run("Write-Host 'Hello from PowerShell!'")
print(f"PowerShell Output: {ps_result.strip()}")

# 1.3 Execute command with timeout
print("\n--- 1.3 Command with Timeout ---")
long_result = cmd_obj.cmd("ping -n 5 localhost", timeout=10)
print(f"Ping output (first 100 chars): {long_result[:100]}...")

# 1.4 Multiple commands
print("\n--- 1.4 Multiple Commands ---")
commands = ["echo First", "echo Second", "echo Third"]
results = cmd_obj.run_multiple_commands(commands)
for i, res in enumerate(results):
    print(f"Command {i+1}: {res.strip()}")

# 1.5 Wait for command (long-running)
print("\n--- 1.5 Wait for Command ---")
wait_result = cmd_obj.wait_for_command("timeout /t 2", timeout=5)
print(f"Wait result: {wait_result.strip()}")


# ============================================
# PART 2: HYBRID COMMAND EXECUTION
# ============================================
print("\n" + "=" * 70)
print("PART 2: HYBRID COMMAND EXECUTION (CMD + PowerShell)")
print("=" * 70)

# 2.1 hybrid execution as dictionary
print("\n--- 2.1 hybrid Execution (Dictionary) ---")
hybrid = hybrid.Hybrid()
dict_result = hybrid.same_time_dict("echo hybrid Test")
print(f"CMD output: {dict_result['cmd'].strip()}")
print(f"PowerShell output: {dict_result['PowerShell'].strip()}")

# 2.2 hybrid execution as list
print("\n--- 2.2 hybrid Execution (List) ---")
list_result = hybrid.same_time_list("Get-Date")
print(f"CMD result: {list_result[0][:50]}...")
print(f"PowerShell result: {list_result[1][:50]}...")

# 2.3 Compare command outputs
print("\n--- 2.3 Compare Outputs ---")
# Simple echo command (usually identical)
is_same = hybrid.comparison("echo Hello World")
print(f"Echo command outputs match? {is_same}")

# Complex command (likely different)
is_same = hybrid.comparison("dir")
print(f"DIR command outputs match? {is_same}")


# ============================================
# PART 3: FILE SYSTEM OPERATIONS
# ============================================
print("\n" + "=" * 70)
print("PART 3: FILE SYSTEM OPERATIONS")
print("=" * 70)

# Create temporary directory for testing
test_dir = tempfile.mkdtemp(prefix="automobile_test_")
os.chdir(test_dir)
print(f"Test directory: {test_dir}")

# 3.1 Create folder
print("\n--- 3.1 Create Folder ---")
file_obj = file.File()
file_obj.create_folder("test_folder")
print("✅ Folder 'test_folder' created")

# 3.2 Create multiple files
print("\n--- 3.2 Create files ---")
with open("file1.txt", "w") as f:
    f.write("Content of file 1")
with open("file2.txt", "w") as f:
    f.write("Content of file 2")
with open("test_folder/file3.txt", "w") as f:
    f.write("Content of file 3")
print("✅ files created: file1.txt, file2.txt, test_folder/file3.txt")

# 3.3 List files
print("\n--- 3.3 List files ---")
listing = file_obj.list_files()
print(f"Directory listing:\n{listing[:200]}...")

# 3.4 Copy file
print("\n--- 3.4 Copy file ---")
file_obj.copy_file("file1.txt", "file1_copy.txt")
print("✅ file1.txt copied to file1_copy.txt")

# 3.5 Move/Rename file
print("\n--- 3.5 Move/Rename file ---")
file_obj.move_file("file2.txt", "test_folder/file2_moved.txt")
print("✅ file2.txt moved to test_folder/file2_moved.txt")

# 3.6 Get file size
print("\n--- 3.6 file Size ---")
size = file_obj.file_size("file1.txt")
print(f"Size of file1.txt: {size}")

# 3.7 Delete file
print("\n--- 3.7 Delete file ---")
file_obj.delete_file("file1_copy.txt")
print("✅ file1_copy.txt deleted")


# ============================================
# PART 4: GIT VERSION CONTROL
# ============================================
print("\n" + "=" * 70)
print("PART 4: GIT VERSION CONTROL")
print("=" * 70)

# 4.1 Initialize git repository
print("\n--- 4.1 Initialize git Repository ---")
git = git.Git()
git.init()
print("✅ git repository initialized")

# 4.2 Configure git user
print("\n--- 4.2 Configure git User ---")
git.user_name("Test User")
git.user_email("test@example.com")
print("✅ git user configured")

# 4.3 Create files and add
print("\n--- 4.3 Add files ---")
with open("README.md", "w") as f:
    f.write("# Test Repository\n\nThis is a test repository for demonstration.")
with open("main.py", "w") as f:
    f.write("print('Hello World!')")

git.add("README.md")
git.add("main.py")
print("✅ files added to staging")

# 4.4 Commit changes
print("\n--- 4.4 Commit Changes ---")
git.commit("Initial commit")
print("✅ Changes committed")

# 4.5 Check status
print("\n--- 4.5 git Status ---")
status = git.status()
print(f"Status:\n{status}")

# 4.6 View commit history
print("\n--- 4.6 Commit History ---")
log = git.oneline()
print(f"Commit history:\n{log}")

# 4.7 Create and switch branch
print("\n--- 4.7 Branch Management ---")
branches = git.branch()
print(f"Current branches:\n{branches}")

# 4.8 Modify file and commit
print("\n--- 4.8 Update file ---")
with open("main.py", "a") as f:
    f.write("\nprint('Updated!')")
git.adds()
git.commit("Update main.py")
print("✅ file updated and committed")


# ============================================
# PART 5: PYTHON PACKAGE MANAGEMENT (PIP)
# ============================================
print("\n" + "=" * 70)
print("PART 5: PYTHON PACKAGE MANAGEMENT")
print("=" * 70)

# 5.1 List installed packages
print("\n--- 5.1 List Packages ---")
pip = python.Pip()
packages = pip.pip_list()
print(f"Installed packages (first 10):\n{packages[:200]}...")

# 5.2 Get installed packages as dictionary
print("\n--- 5.2 Packages as Dictionary ---")
pkg_dict = pip.data_pip()
print(f"Package count: {len(pkg_dict)}")
print(f"Sample packages: {list(pkg_dict.items())[:5]}")

# 5.3 Show package info
print("\n--- 5.3 Package Info ---")
try:
    info = pip.show_pip("pip")
    print(f"Pip info:\n{info[:200]}...")
except:
    print("Could not get pip info")

# 5.4 Create requirements file
print("\n--- 5.4 Create Requirements file ---")
pip.create_requirements("requirements.txt")
print("✅ requirements.txt created")

# 5.5 Check for outdated packages
print("\n--- 5.5 Check Outdated Packages ---")
outdated = pip.pip_outdated()
if outdated.strip():
    print(f"Outdated packages:\n{outdated[:200]}...")
else:
    print("All packages are up to date!")

# 5.6 Check dependencies
print("\n--- 5.6 Check Dependencies ---")
check_result = pip.pip_check()
if "No broken requirements" in check_result:
    print("✅ All dependencies are satisfied")
else:
    print(f"Dependency issues found:\n{check_result[:200]}...")


# ============================================
# PART 6: PYTHON EXECUTION
# ============================================
print("\n" + "=" * 70)
print("PART 6: PYTHON EXECUTION")
print("=" * 70)

# 6.1 Run python script
print("\n--- 6.1 Run python Script ---")
py = python.Python()
with open("test_script.py", "w") as f:
    f.write("print('Hello from test script!')\nprint('Version:', __import__('sys').version)")

result = py.run_script("test_script.py")
print(f"Script output:\n{result}")

# 6.2 Run python code (-c flag)
print("\n--- 6.2 Run python Code ---")
code_result = py.run_code("import sys; print(f'python version: {sys.version}')")
print(f"Code output: {code_result}")

# 6.3 Run python module
print("\n--- 6.3 Run python Module ---")
module_result = py.run_module("json.tool")
print(f"Module output (first 100 chars): {module_result[:100]}...")

# 6.4 Create virtual environment
print("\n--- 6.4 Create Virtual Environment ---")
venv_result = py.create_venv("test_venv")
print("✅ Virtual environment 'test_venv' created")

# 6.5 Run script with venv (Windows specific)
print("\n--- 6.5 Run with Virtual Environment ---")
try:
    venv_result = py.run_with_venv("test_script.py", "test_venv")
    print(f"Script output with venv:\n{venv_result}")
except Exception as e:
    print(f"Note: {e}")


# ============================================
# PART 7: PROCESS MANAGEMENT
# ============================================
print("\n" + "=" * 70)
print("PART 7: PROCESS MANAGEMENT")
print("=" * 70)

# 7.1 Check if process is running
print("\n--- 7.1 Check Process Status ---")
chrome_running = is_process_running("notepad.exe")
print(f"Is Notepad running? {chrome_running}")

# 7.2 Count processes
print("\n--- 7.2 Count Processes ---")
notepad_count = count_processes("notepad.exe")
print(f"Notepad instances: {notepad_count}")

# 7.3 Get process PIDs
print("\n--- 7.3 Get Process PIDs ---")
pids = get_process_pids("python.exe")
print(f"python PIDs: {pids}")

# 7.4 Get detailed process info
print("\n--- 7.4 Detailed Process Info ---")
info = get_process_info("python.exe")
if info:
    proc = info[0]
    print(f"PID: {proc['pid']}")
    print(f"Name: {proc['name']}")
    print(f"Memory: {proc['memory_mb']} MB")
    print(f"CPU: {proc['cpu_percent']}%")
    print(f"Status: {proc['status']}")
    print(f"Threads: {proc['num_threads']}")
else:
    print("No python processes found")

# 7.5 Process Manager class
print("\n--- 7.5 Process Manager ---")
# Open Notepad for testing (if on Windows)
try:
    os.system("start notepad.exe")
    time.sleep(2)
    
    manager = ProcessManager("notepad.exe")
    print(f"Notepad running: {manager.is_running()}")
    print(f"Notepad instances: {manager.count}")
    
    # Get parent process
    parent = manager.get_parent_process()
    if parent:
        print(f"Parent process: {parent['name']} (PID: {parent['pid']})")
    
    # Kill Notepad
    result = manager.kill_all(timeout=2, force=False)
    print(f"Killed {result['success_count']} Notepad processes")
except Exception as e:
    print(f"Note: {e}")

# 7.6 Kill multiple processes
print("\n--- 7.6 Kill Multiple Processes ---")
browsers = ["chrome.exe", "firefox.exe", "msedge.exe"]
for browser in browsers:
    if is_process_running(browser):
        result = kill_process(browser, timeout=2, force=False)
        if result['success_count'] > 0:
            print(f"Killed {result['success_count']} {browser} processes")


# ============================================
# PART 8: SYSTEM CLASS
# ============================================
print("\n" + "=" * 70)
print("PART 8: SYSTEM CLASS (Unified Interface)")
print("=" * 70)

# 8.1 System class with CMD and PowerShell
print("\n--- 8.1 System Commands ---")
system = System()

# CMD command via system
cmd_result = system.cmd.cmd("echo System CMD test")
print(f"System CMD: {cmd_result.strip()}")

# PowerShell via system
ps_result = system.powershell.run("Write-Host 'System PowerShell test'")
print(f"System PowerShell: {ps_result.strip()}")

# 8.2 file operations via system
print("\n--- 8.2 System file Operations ---")
file_result = system.cmd.cmd("dir")
print(f"System directory listing (first 100 chars):\n{file_result[:100]}...")


# ============================================
# PART 9: REAL-WORLD USE CASES
# ============================================
print("\n" + "=" * 70)
print("PART 9: REAL-WORLD USE CASES")
print("=" * 70)

# 9.1 Find large files
print("\n--- 9.1 Find Large files (PowerShell) ---")
ps = powerShell.PowerShell()
large_files = ps.run("Get-ChildItem -Recurse | Where-Object { $_.Length -gt 100MB } | Select-Object Name, Length")
print(f"Large files (first 200 chars):\n{large_files[:200]}...")

# 9.2 Get system information
print("\n--- 9.2 System Information (CMD) ---")
system_info = cmd_obj.cmd("systeminfo | findstr /C:'OS Name' /C:'Total Physical Memory'")
print(f"System info:\n{system_info}")

# 9.3 Check network connectivity
print("\n--- 9.3 Network Check ---")
network = cmd_obj.cmd("ping -n 2 google.com")
if "Reply from" in network:
    print("✅ Internet connection active")
else:
    print("❌ No internet connection")

# 9.4 python environment info
print("\n--- 9.4 python Environment ---")
py_info = py.run_code("import platform, sys; print(f'python: {sys.version}'); print(f'Platform: {platform.platform()}')")
print(f"Environment info:\n{py_info}")


# ============================================
# PART 10: CLEANUP
# ============================================
print("\n" + "=" * 70)
print("PART 10: CLEANUP")
print("=" * 70)

print("\n--- 10.1 Cleanup files ---")
try:
    # Clean up test directory
    os.chdir("..")
    import shutil
    shutil.rmtree(test_dir)
    print(f"✅ Test directory '{test_dir}' removed")
except Exception as e:
    print(f"Cleanup error: {e}")

print("\n" + "=" * 70)
print("✅ ALL DEMONSTRATIONS COMPLETED SUCCESSFULLY!")
print("=" * 70)
print("\nSummary of operations performed:")
print("- ✅ CMD & PowerShell command execution")
print("- ✅ hybrid command execution with comparison")
print("- ✅ file system operations (create, copy, move, delete)")
print("- ✅ git repository management (init, add, commit, status)")
print("- ✅ python package management (list, show, check)")
print("- ✅ python script execution and venv creation")
print("- ✅ Process management (check, kill, suspend, resume)")
print("- ✅ System information and network checks")
print("- ✅ Real-world automation use cases")