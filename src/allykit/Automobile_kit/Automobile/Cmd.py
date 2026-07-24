"""
Command Execution Utility Module

This module provides a comprehensive interface for executing system commands,
managing command-line windows, and handling command output. It combines
subprocess execution with GUI automation capabilities for enhanced control.
"""

import os
import pyautogui as ui
import subprocess
import pyperclip
from time import sleep
from allykit.Automobile_kit.ProcessManager import kill_process

class cmd:
    """
    A utility class for executing and managing system commands.
    
    This class provides static and instance methods for command execution,
    terminal management, and output handling. It supports both background
    execution and interactive GUI-based command entry.
    """
    
    @staticmethod
    def cmd(text: str, timeout: int = 5) -> str:
        """
        Execute a system command and capture its output.
        
        Args:
            text (str): The command to execute in the system shell.
            timeout (int, optional): Maximum execution time in seconds. 
                                    Defaults to 5.
        
        Returns:
            str: The combined stdout and stderr output of the command.
                 Returns an error message if the command times out or fails.
        
        Raises:
            subprocess.TimeoutExpired: When command execution exceeds timeout.
            Exception: For any other execution errors.
        
        Example:
            >>> cmd.cmd("dir", timeout=3)
            'Volume in drive C is Windows\\nVolume Serial Number is XXXX-XXXX\\n...'
        """
        try:
            result = subprocess.run(
                text,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            output = result.stdout + result.stderr
            pyperclip.copy(output)  # Copy output to clipboard for easy access
            
            return output
            
        except subprocess.TimeoutExpired:
            return f"Error: The command did not complete after {timeout} seconds"
        except Exception as e:
            return f"Error executing command: {e}"

    @staticmethod
    def open_cmd():
        """
        Open a new Command Prompt window using the default method.
        
        Returns:
            bool or int: Result of os.startfile operation.
                         True if successful, raises exception otherwise.
        
        Note:
            This method uses os.startfile which opens the command prompt
            using Windows' default file association for .exe files.
        """
        return os.startfile("cmd")
    
    @staticmethod    
    def open_terminal():
        """
        Open a new Command Prompt window using system command.
        
        Returns:
            int: Exit code from the system call (0 for success).
        
        Note:
            This method uses os.system to execute 'start cmd',
            which may provide more control over the window behavior.
        """
        return os.system("start cmd")    
    
    def run_multiple_commands(self, commands: list[str]) -> list[str]:
        """
        Execute multiple commands sequentially and collect their outputs.
        
        Args:
            commands (list[str]): A list of command strings to execute.
        
        Returns:
            list[str]: A list containing the output of each command
                       in the same order as the input list.
        
        Example:
            >>> cmd_obj = cmd()
            >>> results = cmd_obj.run_multiple_commands(["echo Hello", "echo World"])
            >>> print(results)
            ['Hello\\n', 'World\\n']
        """
        results = []
        for cmd_text in commands:
            results.append(self.cmd(cmd_text))
        return results
    
    def type_text(self, text: str, address: tuple = (600, 300), time: int = 5):
        """
        Open a command prompt and automatically type the specified command.
        
        This method combines GUI automation with command execution to simulate
        user typing in a command prompt window.
        
        Args:
            text (str): The text/command to type into the command prompt.
            address (tuple, optional): Screen coordinates (x, y) where the 
                                      command prompt window is located. 
                                      Defaults to (600, 300).
            time (int, optional): Time to wait after opening the command prompt
                                  before typing. Defaults to 5 seconds.
        
        Returns:
            None: This method performs GUI actions and doesn't return a value.
        
        Note:
            - Requires the command prompt window to be visible at the specified address
            - The method will click at the specified coordinates to focus the window
            - Adjust the delay time based on system performance
        
        Example:
            >>> cmd_obj = cmd()
            >>> cmd_obj.type_text("ipconfig", (500, 200), 3)
            # Opens cmd, waits 3 seconds, types "ipconfig", and presses Enter
        """
        self.open_cmd()
        sleep(time)
        ui.click(*address)  # Click to focus the command prompt window
        ui.typewrite(text)  # Type the command
        ui.press("enter")   # Execute the command

    def change_directory(self, path: str) -> str:
        """
        Change the current working directory using the 'cd' command.
        
        Args:
            path (str): The target directory path to change to.
        
        Returns:
            str: The output from the 'cd' command execution.
        
        Example:
            >>> cmd_obj = cmd()
            >>> result = cmd_obj.change_directory("C:\\Users\\Documents")
            >>> print(result)
            ''  # Empty output on success
        """
        return self.cmd(f"cd {path}")

    def wait_for_command(self, command: str, timeout: int = 30) -> str:
        """
        Execute a command with extended timeout for long-running operations.
        
        This method is specifically designed for commands that require more
        time to complete, such as system scans, file operations, or network
        commands.
        
        Args:
            command (str): The command to execute.
            timeout (int, optional): Maximum execution time in seconds.
                                    Defaults to 30 seconds.
        
        Returns:
            str: The output of the command execution, or an error message
                 if the command times out.
        
        Example:
            >>> cmd_obj = cmd()
            >>> output = cmd_obj.wait_for_command("ping google.com -n 10", 60)
            >>> print(output)
            'Pinging google.com...\\nReply from ...'
        """
        return self.cmd(command, timeout=timeout)
    
    @staticmethod       
    def kill_cmd():
        return kill_process("cmd.exe")

