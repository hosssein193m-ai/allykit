"""
PowerShell Command Execution Utility Module

This module provides a comprehensive interface for executing PowerShell
commands and scripts from Python, with support for error handling,
timeout management, and specialized file operations.
"""

import os
import subprocess

class PowerShell:
    """
    A utility class for executing PowerShell commands and managing PowerShell windows.
    
    This class provides both simple and advanced methods for running PowerShell
    commands, with features like timeout control, error handling, and specialized
    file operations. It serves as a bridge between Python and PowerShell's
    powerful scripting capabilities.
    """
    
    @staticmethod    
    def open():
        """
        Open a new PowerShell window using the system command.
        
        Returns:
            int: Exit code from the system call (0 typically indicates success).
        
        Note:
            This method uses os.system to launch PowerShell, which will
            appear as a new window in the operating system.
        
        Example:
            >>> PowerShell.open()
            0  # PowerShell window opens
        """
        return os.system("start powershell")

    @staticmethod    
    def run(ps_command) -> str:
        """
        Execute a PowerShell command and return its combined output.
        
        This is a simple method for running PowerShell commands with minimal
        configuration. It captures both stdout and stderr as a single string.
        
        Args:
            ps_command (str): The PowerShell command to execute.
        
        Returns:
            str: Combined stdout and stderr output from the command.
                 Empty string if no output is produced.
        
        Example:
            >>> output = PowerShell.run("Get-Process -Name explorer")
            >>> print(output[:100])  # Show first 100 characters
            'Handles  NPM(K)    PM(K)      WS(K)     CPU(s)     Id  SI ProcessName'
        """
        result = subprocess.run(
            ["powershell.exe", "-Command", ps_command],
            capture_output=True,
            text=True
        )
        return result.stdout + result.stderr

    @staticmethod
    def execute(command: str, timeout: int = 60) -> dict:
        """
        Execute a PowerShell command with advanced features and structured output.
        
        This method provides comprehensive execution control including:
        - Timeout management for long-running commands
        - UTF-8 encoding support for international characters
        - Structured dictionary output with success status
        - Separate output and error streams
        
        Args:
            command (str): The PowerShell command to execute.
            timeout (int, optional): Maximum execution time in seconds.
                                    Defaults to 60 seconds.
        
        Returns:
            dict: A structured response containing:
                - success (bool): Whether the command executed successfully
                - output (str): The command's standard output
                - error (str): The command's standard error (if any)
                - returncode (int): The process's exit code
        
        Raises:
            subprocess.TimeoutExpired: Automatically handled, returns error dict.
            Exception: Automatically caught and wrapped in error dict.
        
        Example:
            >>> result = PowerShell.execute("Get-Service -Name Spooler", timeout=30)
            >>> if result["success"]:
            ...     print(f"Service status: {result['output']}")
            ... else:
            ...     print(f"Error: {result['error']}")
        """
        try:
            result = subprocess.run(
                ["powershell.exe", "-Command", command],
                capture_output=True,
                text=True,
                encoding='utf-8',  # Support Unicode/UTF-8 characters
                timeout=timeout
            )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout.strip(),
                "error": result.stderr.strip(),
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False, 
                "error": "Execution time expired", 
                "output": ""
            }
        except Exception as e:
            return {
                "success": False, 
                "error": str(e), 
                "output": ""
            }

    @staticmethod    
    def size_file(name: str) -> float:
        """
        Calculate the total size of a file or directory in gigabytes (GB).
        
        This method recursively calculates the total size of a specified file
        or directory using PowerShell's Get-ChildItem and Measure-Object cmdlets.
        
        Args:
            name (str): The path to the file or directory to measure.
        
        Returns:
            float: The size in gigabytes (GB) as a floating-point number.
                  Returns a string error message if the operation fails.
        
        Note:
            - The method searches recursively (-Recurse flag)
            - Returns 0 if the path doesn't exist
            - Handles both files and directories
            - Returns size in GB for practical large-file operations
        
        Example:
            >>> size = PowerShell.size_file("C:\\Users\\Documents")
            >>> print(f"Folder size: {size:.2f} GB")
            Folder size: 15.34 GB
            
            >>> file_size = PowerShell.size_file("C:\\largefile.iso")
            >>> print(f"File size: {file_size:.2f} GB")
            File size: 2.45 GB
        
        PowerShell Command Used:
            Get-ChildItem "{name}" -Recurse -ErrorAction SilentlyContinue |
            Measure-Object -Property Length -Sum |
            Select-Object -ExpandProperty Sum / 1GB
        """
        ps_command = f'(Get-ChildItem "{name}" -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1GB'
        
        try:
            result = subprocess.run(
                ["powershell.exe", "-Command", ps_command],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if result.returncode == 0:
                output = result.stdout.strip()
                if output:
                    size_gb = float(output)
                    return size_gb
        except Exception as e:
            return f"Execution error: {str(e)}"