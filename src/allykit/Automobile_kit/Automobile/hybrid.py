"""
Hybrid Command Execution Utility Module

This module provides a hybrid command execution class that combines
both CMD and PowerShell capabilities, allowing parallel execution
and comparison of command outputs across both shells.
"""

from allykit.Security_kit.hash_kit import hash_password
from allykit.Automobile_kit.Automobile import powerShell
from allykit.Automobile_kit.Automobile import Cmd

class Hybrid(Cmd.cmd, powerShell.PowerShell):
    """
    A hybrid command execution class that inherits from both CMD and PowerShell utilities.
    
    This class combines the functionality of both command-line interfaces,
    allowing users to execute the same command in both environments simultaneously.
    It also provides comparison functionality to verify if both shells produce
    identical outputs.
    
    Inheritance:
        - Cmd.cmd: Provides Windows CMD command execution capabilities
        - powerShell.PowerShell: Provides PowerShell command execution capabilities
    
    Features:
        - Parallel execution of commands in both CMD and PowerShell
        - Output comparison using hash verification
        - Flexible output formats (dictionary and list)
        - Inherited methods from both parent classes
    """
    
    def same_time_dict(self, text: str) -> dict:
        """
        Execute a command in both CMD and PowerShell simultaneously and return results as a dictionary.
        
        This method runs the same command in both command-line environments
        and organizes the outputs into a structured dictionary format.
        
        Args:
            text (str): The command to execute in both CMD and PowerShell.
        
        Returns:
            dict: A dictionary containing:
                - "cmd" (str): Output from the CMD execution
                - "PowerShell" (str): Output from the PowerShell execution
        
        Note:
            - Uses self.cmd() from Cmd.cmd parent class
            - Uses self.run() from powerShell.PowerShell parent class
            - Both commands are executed independently
        
        Example:
            >>> hybrid = Hybrid()
            >>> result = hybrid.same_time_dict("echo Hello World")
            >>> print(result)
            {
                "cmd": "Hello World\\n",
                "PowerShell": "Hello World\\n"
            }
        """
        cmd = self.cmd(text)
        powerShell = self.run(text)
        return {
            "cmd": cmd,
            "PowerShell": powerShell
        }
    
    def same_time_list(self, text: str) -> list:
        """
        Execute a command in both CMD and PowerShell simultaneously and return results as a list.
        
        This method runs the same command in both command-line environments
        and returns the outputs as a list in a predictable order.
        
        Args:
            text (str): The command to execute in both CMD and PowerShell.
        
        Returns:
            list: A list containing [CMD_output, PowerShell_output] in that order.
        
        Example:
            >>> hybrid = Hybrid()
            >>> result = hybrid.same_time_list("dir")
            >>> print(f"CMD: {result[0]}")
            >>> print(f"PowerShell: {result[1]}")
        """
        cmd = self.cmd(text)
        powerShell = self.run(text)
        return [cmd, powerShell]
   
    def comparison(self, text: str) -> bool:
        """
        Compare the outputs of a command executed in both CMD and PowerShell.
        
        This method executes the same command in both environments and compares
        their outputs using cryptographic hashing to determine if they are identical.
        
        Args:
            text (str): The command to execute and compare across both shells.
        
        Returns:
            bool: True if the outputs from CMD and PowerShell are identical,
                  False if they differ.
        
        Note:
            - Uses hash_password() for secure output comparison
            - Converts outputs to strings before hashing
            - Useful for testing command compatibility across shells
            - Handles commands that may have different output formats
        
        Example:
            >>> hybrid = Hybrid()
            >>> # Commands with identical outputs
            >>> is_same = hybrid.comparison("echo Hello")
            >>> print(f"Outputs match: {is_same}")  # True
            
            >>> # Commands with different outputs
            >>> is_same = hybrid.comparison("dir")
            >>> print(f"Outputs match: {is_same}")  # False (different formatting)
        
        Use Cases:
            - Testing command compatibility between CMD and PowerShell
            - Validating that commands produce consistent results
            - Debugging differences in command outputs
            - Ensuring cross-shell script compatibility
        """
        data = self.same_time_list(text)
        return hash_password(str(data[0])) == hash_password(str(data[1]))