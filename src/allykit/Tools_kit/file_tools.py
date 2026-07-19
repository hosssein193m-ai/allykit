"""
Module: General Filesystem Tools
=================================
Basic file operations, metadata extraction, and permission management.
"""

import os
import shutil
import stat
import json
from pathlib import Path
from datetime import datetime
from typing import Union, List, Dict

# ==================== PERMISSION CONSTANTS ====================
PERMISSION_MASKS = {
    "OWNER": 0o700,
    "GROUP": 0o070,
    "OTHER": 0o007,
    "ALL": 0o777,
    "OWNER_READ": 0o400,
    "OWNER_WRITE": 0o200,
    "OWNER_EXEC": 0o100,
    "GROUP_READ": 0o040,
    "GROUP_WRITE": 0o020,
    "GROUP_EXEC": 0o010,
    "OTHER_READ": 0o004,
    "OTHER_WRITE": 0o002,
    "OTHER_EXEC": 0o001,
    "SUID": 0o4000,
    "SGID": 0o2000,
    "STICKY": 0o1000,
}

PERMISSION_MASKS_SHORT = {
    "O": 0o700, "G": 0o070, "OT": 0o007,
    "OR": 0o400, "OW": 0o200, "OE": 0o100,
    "GR": 0o040, "GW": 0o020, "GE": 0o010,
    "OTR": 0o004, "OTW": 0o002, "OTE": 0o001,
    "SUID": 0o4000, "SGID": 0o2000, "STICKY": 0o1000,
}

PERMISSION_MASKS_LIST = [
    0o4000, 0o2000, 0o1000, 0o700, 0o070, 0o007,
    0o400, 0o200, 0o100, 0o040, 0o020, 0o010,
    0o004, 0o002, 0o001,
]

# ==================== FILE OPERATIONS ====================
def remove_file(file: str) -> None:
    """Remove file or folder if permission denied."""
    try:
        os.remove(file)
    except PermissionError:
        shutil.rmtree(file)
    except FileNotFoundError:
        raise FileNotFoundError(file)

def remove_files(path: str) -> None:
    """Deletes all files and directories within the specified path."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"The path '{path}' does not exist.")
    if os.path.isfile(path):
        raise NotADirectoryError(f"The path '{path}' is a file, not a directory.")
    
    for file in os.listdir(path):
        full_path = os.path.join(path, file)
        try:
            os.remove(full_path)
        except PermissionError:
            shutil.rmtree(full_path)

def is_dir(file: str) -> bool | str:
    """Check if object is folder (True) or file (False) or symlink."""
    if os.path.isdir(file):
        return True
    if os.path.isfile(file):
        return False
    return "symlink"

# ==================== FILE READ/WRITE OPERATIONS ====================
def write_file(file: str, text: str) -> bool:
    """Writes a plain text string to a specified file."""
    try:
        with open(file, "w", encoding='utf-8') as f:
            f.write(text)
        return True
    except FileNotFoundError:
        return False
    except IOError:
        print("Error: An error occurred while writing to the file.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

def dump_file(file: str, text: dict | list) -> bool:
    """Serializes a Python object to a JSON file."""
    try:
        with open(file, "w", encoding='utf-8') as f:
            json.dump(text, f, ensure_ascii=False, indent=4)
        return True
    except FileNotFoundError:
        return False
    except IOError:
        print("IOError: An error occurred while writing to the file.")
        return False
    except Exception as e:
        print(f"Exception: An unexpected error occurred: {e}")
        return False

def load_file(file: str, s: bool = False) -> dict | list:
    """Loads JSON data from a file. Creates empty file if missing."""
    try:
        with open(file, 'r', encoding='utf-8') as f:
            load = json.load(f)
    except FileNotFoundError:
        with open(file, 'w', encoding='utf-8') as f:
            pass
        load = load_file(file, s)
    except json.JSONDecodeError:
        return [] if s else {}
    except Exception as e:
        raise Exception(e)
    return load

def read_file(file: str) -> str:
    """Reads the entire content of a text file."""
    try:
        with open(file, 'r', encoding='utf-8') as f:
            read = f.read()
    except FileNotFoundError:
        with open(file, 'w', encoding='utf-8') as f:
            pass
        read = read_file(file)
    except Exception as e:
        raise Exception(e)
    return read

# ==================== METADATA EXTRACTION ====================
def get_permission(file: str) -> str:
    """Return file permission mode."""
    try:
        mode = os.stat(file).st_mode
        return stat.filemode(mode)
    except FileNotFoundError:
        raise FileNotFoundError(f"not file: {file}")
    except Exception as e:
        raise Exception(f"Error processing file {file}: {e}")

def change_permission(file: str, permission: Union[str, int]) -> None:
    """Updates the permission mode of a given file."""
    if permission in PERMISSION_MASKS_SHORT:
        os.chmod(file, PERMISSION_MASKS_SHORT[permission])
    elif permission in PERMISSION_MASKS:
        os.chmod(file, PERMISSION_MASKS[permission])
    elif permission in PERMISSION_MASKS_LIST:
        os.chmod(file, permission)
    else:
        raise TypeError(f"not permission: {permission}")

def get_stat_info(file: str) -> os.stat_result:
    """Retrieves the status information of a file."""
    return os.stat(file)

def datetime_file(stat_info: os.stat_result) -> list:
    """Extracts access, modification, and creation timestamps."""
    return [
        datetime.fromtimestamp(stat_info.st_atime),
        datetime.fromtimestamp(stat_info.st_mtime),
        datetime.fromtimestamp(stat_info.st_ctime),
    ]

def type_file(mode: int) -> str:
    """Determines the type of the file based on the mode bitmask."""
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "Directory"
    if stat.S_ISLNK(mode):
        return "Symbolic_link"
    return "Unknown"

def information_files(stat_info: os.stat_result) -> list:
    """Extracts core metadata including UID, Device ID, GID, Size, and Link count."""
    uid_file = stat_info.st_uid
    uid = "root" if uid_file == 0 else str(uid_file)
    return [uid, stat_info.st_dev, stat_info.st_gid, stat_info.st_size, stat_info.st_nlink]

def information_files_dict(filename: str) -> dict:
    """Gathers all file metadata and returns it in a structured dictionary."""
    stat_info = os.stat(filename)
    mode = stat_info.st_mode
    datetime_files = datetime_file(stat_info)
    information = information_files(stat_info)
    
    return {
        "Information_file": {
            "name_file": filename,
            "type_file": type_file(mode),
            "last_load_file": datetime_files[0],
            "last_change_file": datetime_files[1],
            "last_rename_file": datetime_files[2],
            "owner_uid": information[0],
            "place_file": information[1],
            "owner_gid": information[2],
            "size_file_byte": information[3],
            "nlink_file": information[4]
        }
    }