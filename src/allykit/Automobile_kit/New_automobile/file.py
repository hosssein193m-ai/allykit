"""
Cross-Platform File System Operations Utility Module

This module provides a comprehensive interface for file system operations
that works across Windows, Linux, and macOS. It abstracts platform-specific
commands behind a unified Python API.
"""

from allykit.Automobile_kit.Automobile import Cmd
import os

class File(Cmd.cmd):
    """
    A cross-platform file system operations utility class.
    
    This class provides a platform-agnostic interface for common file system
    operations including creating, deleting, copying, moving, and listing
    files and directories. It automatically detects the operating system
    and uses the appropriate system commands.
    
    Features:
        - Cross-platform compatibility (Windows, Linux, macOS)
        - Automatic command selection based on OS
        - File and directory operations
        - File information retrieval
        - Path manipulation
    
    Inheritance:
        - Cmd.cmd: Provides command execution capabilities
    
    Platform Support:
        - Windows: Uses cmd.exe commands (mkdir, del, copy, move, dir, ren)
        - Linux/macOS: Uses bash commands (mkdir, rm, cp, mv, ls -la, du)
    """
    
    def create_folder(self, folder_name: str) -> str:
        """
        Create a new directory/folder.
        
        Args:
            folder_name (str): The name or path of the folder to create.
        
        Returns:
            str: Output from the directory creation command.
        
        Platform Commands:
            - Windows: mkdir {folder_name}
            - Linux/macOS: mkdir {folder_name}
        
        Example:
            >>> file = File()
            >>> result = file.create_folder("new_project")
            >>> result = file.create_folder("src/utils")
        """
        return self.cmd(f"mkdir {folder_name}")
    
    def delete_file(self, file_path: str) -> str:
        """
        Delete a file from the file system.
        
        Args:
            file_path (str): The path to the file to delete.
        
        Returns:
            str: Output from the file deletion command.
        
        Platform Commands:
            - Windows: del {file_path}
            - Linux/macOS: rm {file_path}
        
        Warning:
            This operation is permanent and cannot be undone.
            Files are not moved to the recycle bin.
        
        Example:
            >>> file = File()
            >>> result = file.delete_file("temp.txt")
            >>> result = file.delete_file("./cache/old_data.json")
        """
        if os.name == 'nt':
            return self.cmd(f"del {file_path}")
        else:
            return self.cmd(f"rm {file_path}")

    def copy_file(self, source: str, destination: str) -> str:
        """
        Copy a file from source to destination.
        
        Args:
            source (str): The path to the source file.
            destination (str): The path where the file should be copied.
        
        Returns:
            str: Output from the file copy command.
        
        Platform Commands:
            - Windows: copy {source} {destination}
            - Linux/macOS: cp {source} {destination}
        
        Note:
            - Destination can be a file path or directory path
            - If destination is a directory, the file will be copied into it
            - Overwrites existing files at the destination
        
        Example:
            >>> file = File()
            >>> # Copy to new file name
            >>> file.copy_file("original.txt", "backup.txt")
            >>> # Copy to directory
            >>> file.copy_file("data.csv", "./backup/data.csv")
        """
        if os.name == 'nt':
            return self.cmd(f"copy {source} {destination}")
        else:
            return self.cmd(f"cp {source} {destination}")

    def move_file(self, source: str, destination: str) -> str:
        """
        Move or rename a file from source to destination.
        
        Args:
            source (str): The current path of the file.
            destination (str): The new path for the file.
        
        Returns:
            str: Output from the file move command.
        
        Platform Commands:
            - Windows: move {source} {destination}
            - Linux/macOS: mv {source} {destination}
        
        Example:
            >>> file = File()
            >>> # Move to another directory
            >>> file.move_file("data.txt", "archive/data.txt")
            >>> # Rename file
            >>> file.move_file("old_name.txt", "new_name.txt")
        """
        if os.name == 'nt':
            return self.cmd(f"move {source} {destination}")
        else:
            return self.cmd(f"mv {source} {destination}")

    def list_files(self, path: str = ".") -> str:
        """
        List files and directories at the specified path.
        
        Args:
            path (str, optional): The directory path to list.
                                 Defaults to current directory (".").
        
        Returns:
            str: A detailed listing of files and directories.
        
        Platform Commands:
            - Windows: dir {path}
            - Linux/macOS: ls -la {path}
        
        Note:
            - Windows: Shows file sizes, dates, and attributes
            - Linux/macOS: Shows permissions, owners, sizes, and dates
        
        Example:
            >>> file = File()
            >>> # List current directory
            >>> print(file.list_files())
            >>> # List specific directory
            >>> print(file.list_files("/home/user/documents"))
        """
        if os.name == 'nt':
            return self.cmd(f"dir {path}")
        else:
            return self.cmd(f"ls -la {path}")

    def rename_file(self, old_name: str, new_name: str) -> str:
        """
        Rename a file or directory.
        
        Args:
            old_name (str): The current name/path of the file.
            new_name (str): The new name/path for the file.
        
        Returns:
            str: Output from the rename command.
        
        Platform Commands:
            - Windows: ren {old_name} {new_name}
            - Linux/macOS: mv {old_name} {new_name}
        
        Note:
            - On Linux/macOS, this is an alias for move_file()
            - The destination can include a different directory path
            - The source and destination must be in the same filesystem
        
        Example:
            >>> file = File()
            >>> file.rename_file("report.txt", "final_report.txt")
            >>> file.rename_file("old_project", "new_project")
        """
        if os.name == 'nt':
            return self.cmd(f"ren {old_name} {new_name}")
        else:
            return self.cmd(f"mv {old_name} {new_name}")

    def file_size(self, file_path: str) -> str:
        """
        Get the size of a file or directory.
        
        Args:
            file_path (str): The path to the file or directory.
        
        Returns:
            str: Size information for the specified path.
        
        Platform Commands:
            - Windows: dir {file_path} | findstr {file_path}
            - Linux/macOS: du -sh {file_path}
        
        Note:
            - Windows: Shows file size in bytes with other file information
            - Linux/macOS: Shows human-readable size (KB, MB, GB)
            - For directories, displays total size (Linux/macOS only)
        
        Example:
            >>> file = File()
            >>> # Get file size
            >>> size = file.file_size("large_video.mp4")
            >>> print(size)
            '2.5G    large_video.mp4'
            >>> # Get directory size
            >>> size = file.file_size("./project_folder")
            >>> print(size)
            '156M    ./project_folder'
        """
        if os.name == 'nt':
            return self.cmd(f"dir {file_path} | findstr {file_path}")
        else:
            return self.cmd(f"du -sh {file_path}")