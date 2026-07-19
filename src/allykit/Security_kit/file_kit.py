"""
Module: Security & Integrity Tools
===================================
File hashing, integrity verification, snapshots, and security auditing.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Union, List
from allykit.Security_kit.hash_kit import HP
# از جعبه ابزار عمومی وارد می‌کنیم
from allykit.Tools_kit.file_tools import information_files_dict, get_permission

ph_S384 = lambda password: HP(password=str(password), algorithm="sha384")

# ==================== SECURITY CONSTANTS ====================
DANGEROUS_PERMISSIONS = [
    "rwxrwxrwx", "drwxrwxrwx", "rw-rw-rw-", "drwxrwxrw-",
    "rwxrwxrw-", "rwxrwxrwt", "rwxrwxr-x", "drwxrwxr-x",
    "rwxrwx--x", "drwxrwx--x", "rwxrwx--w", "drwxrwx--w",
    "rwxrwx-wx", "drwxrwx-wx", "rwxrwx-w-", "drwxrwx-w-",
    "rw-rw-rwx",
]

HIGH_RISK_PERMISSIONS = [
    "rwxrwxrwx", "drwxrwxrwx", "rw-rw-rw-",
    "rwxrwxrw-", "rwxrwx-wx", "rwxrwx--w",
]

MEDIUM_RISK_PERMISSIONS = [
    "rwxr-xr-x", "rw-r--r--", "rwxr-x---",
    "rw-r-----", "rwx------",
]

# ==================== HASH & INTEGRITY ====================
def hash_file(file: str, salt: bool = True) -> str:
    """
    Generates a unique SHA384 hex hash for a file.
    
    Args:
        file (str): The path to the file.
        salt (bool): If True, combines content, metadata, and path.
    
    Returns:
        str: The SHA384 hex string, or FILE_ERROR if inaccessible.
    """
    list_hash_file = []
    try:
        with open(file, 'rb') as f:
            text_dir = f.read()
        password = ph_S384(text_dir)
        list_hash_file.append(password)
        
        if salt:
            file_data = information_files_dict(file)["Information_file"]
            for value in file_data.values():
                if isinstance(value, (str, int, float, datetime)):
                    list_hash_file.append(ph_S384(str(value)))
            list_hash_file.append(ph_S384(str(file)))
    except (FileNotFoundError, PermissionError):
        return "FILE_ERROR"
    
    if salt:
        return ph_S384(''.join(list_hash_file))
    return list_hash_file[0]

def find_file(directory: str, filename: str) -> Path | None:
    """Searches for a specific filename within a directory and all subdirectories."""
    directory_path = Path(directory)
    for path in directory_path.rglob(filename):
        if path.is_file():
            return path
    return None

# ==================== DIRECTORY MAPPING ====================
def dict_files_in_directory(directory: str) -> dict:
    """
    Creates a dictionary of all files and folders inside a specified path.
    Includes PERMISSION_MASKS and file hash for each item.
    """
    directory = Path(directory)
    dict_files = {}
    for item in directory.iterdir():
        if item.is_dir():
            dict_files[item.name] = dict_files_in_directory(item)
        else:
            password = hash_file(item)
            dict_files[item.name] = [password, "file"]
    return dict_files

def dict_files_in_directory_bool(directory: str,
                                 reachs: bool = True,
                                 passwords: bool = True,
                                 f: bool = True) -> dict:
    """
    Similar to dict_files_in_directory but with control over included information.
    
    Args:
        reachs: Include permission information
        passwords: Include file hashes
        f: Include file type information
    """
    directory = Path(directory)
    dict_files = {}
    
    for item in directory.iterdir():
        reach = get_permission(str(item))
        
        if item.is_dir():
            dict_files[item.name] = dict_files_in_directory_bool(
                item, reachs, passwords, f
            )
        else:
            chdir = find_file(directory, item.name)
            password = hash_file(chdir) if passwords else None
            
            result = []
            if reachs:
                result.append(reach)
            if passwords:
                result.append(password)
            if f:
                result.append("file")
            
            dict_files[item.name] = result if len(result) > 1 else (result[0] if result else {})
    
    return dict_files

def save_dict_and_expected(filename: str, directory: str) -> None:
    """Saves the dictionary from dict_files_in_directory into a JSON file."""
    if not filename:
        raise ValueError("filename cannot be empty")
    
    text = dict_files_in_directory(directory)
    with open(filename, 'w') as f:
        json.dump(text, f, indent=4)

# ==================== SNAPSHOTS ====================
def create_snapshot(directory: str) -> dict:
    """
    Create a security snapshot of all files in a directory and its subdirectories.
    
    The snapshot includes for each file:
    - relative path
    - file hash (with salt for integrity)
    - file size in bytes
    - last modification time (mtime)
    - permission information
    """
    directory = Path(directory)
    if not directory.exists():
        raise FileNotFoundError(f"Directory '{directory}' does not exist.")
    
    snapshot = {}
    for item in directory.rglob('*'):
        if item.is_file():
            rel_path = str(item.relative_to(directory))
            snapshot[rel_path] = {
                'hash': hash_file(item, salt=True),
                'size': item.stat().st_size,
                'mtime': item.stat().st_mtime,
                'permissions': get_permission(str(item)),
            }
    return snapshot

def verify_snapshot(directory: str, snapshot: dict) -> Dict[str, str]:
    """
    Verifies a directory against a previously taken snapshot.
    
    Returns a dictionary of changes detected.
    """
    current_snapshot = create_snapshot(directory)
    changes = {}
    
    for file_path, current_data in current_snapshot.items():
        if file_path not in snapshot:
            changes[file_path] = "NEW_FILE"
        elif current_data['hash'] != snapshot[file_path]['hash']:
            changes[file_path] = "MODIFIED"
        elif current_data['permissions'] != snapshot[file_path]['permissions']:
            changes[file_path] = "PERMISSION_CHANGED"
    
    # Check for deleted files
    for file_path in snapshot:
        if file_path not in current_snapshot:
            changes[file_path] = "DELETED"
    
    return changes