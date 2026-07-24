import json
from typing import Union, Optional, List, Dict
import os
import shutil

# Type aliases for better readability
JsonData = Union[Dict, List, str]
JsonContainer = Union[Dict, List]


def dump_file(file: str, text: JsonContainer) -> bool:
    """
    Serializes a Python object to a JSON file with UTF-8 encoding.
    
    Args:
        file (str): Path to the target JSON file
        text (JsonContainer): Data to serialize (dict or list)
        
    Returns:
        bool: True if successful, False otherwise
        
    Raises:
        Prints error messages but does not raise exceptions
    """
    try:
        with open(file, "w", encoding='utf-8') as f:
            json.dump(text, f, ensure_ascii=False, indent=4)
        return True
    except (FileNotFoundError, IOError) as e:
        print(f"File error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


def load_file(file: str, return_list: bool = False) -> JsonContainer:
    """
    Loads JSON data from a file. Creates empty file if it doesn't exist.
    
    Args:
        file (str): Path to the JSON file
        return_list (bool): If True, returns empty list; otherwise empty dict
        
    Returns:
        JsonContainer: Loaded data or empty container
        
    Note:
        - Creates file with empty JSON if not found
        - Returns empty container on JSON decode errors
        - Handles all exceptions gracefully
    """
    try:
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Create empty file with appropriate container type
        with open(file, 'w', encoding='utf-8') as f:
            json.dump({} if not return_list else [], f, ensure_ascii=False, indent=4)
        return [] if return_list else {}
    except json.JSONDecodeError:
        print(f"Warning: {file} contains invalid JSON. Returning empty container.")
        return [] if return_list else {}
    except Exception as e:
        print(f"Error loading {file}: {e}")
        return [] if return_list else {}


class WorkFileJson:
    """
    A comprehensive JSON file handler with CRUD operations and utility methods.
    
    This class provides a clean interface for managing JSON data with support for:
    - Dictionary and list data structures
    - CRUD operations (Create, Read, Update, Delete)
    - File management (rename, delete, backup, restore)
    - Data manipulation (search, merge, clear)
    - Information retrieval (size, keys, values)
    
    Attributes:
        namefile (str): Path to the JSON file being managed
    """
    
    def __init__(self, namefile: str):
        """
        Initialize the JSON file handler.
        
        Args:
            namefile (str): Path to the JSON file to manage
        """
        self.namefile = namefile

    # ==================== CORE OPERATIONS ====================
    
    def load(self, output: bool = False) -> JsonContainer:
        """
        Load data from the JSON file.
        
        Args:
            output (bool): If True, returns list; otherwise returns dict
            
        Returns:
            JsonContainer: Loaded data (dict or list)
        """
        return load_file(self.namefile, output)
    
    def save(self, data: JsonContainer) -> bool:
        """
        Save data to the JSON file.
        
        Args:
            data (JsonContainer): Data to save (dict or list)
            
        Returns:
            bool: True if successful, False otherwise
        """
        return dump_file(self.namefile, data)
    
    def exists(self) -> bool:
        """
        Check if the file exists on disk.
        
        Returns:
            bool: True if file exists, False otherwise
        """
        return os.path.exists(self.namefile)
    
    # ==================== UPDATE OPERATIONS ====================
    
    def update_dict(self, key: str, value: JsonData, data: Optional[dict] = None) -> bool:
        """
        Update a dictionary with a new key-value pair.
        
        Args:
            key (str): Key to add/update
            value (JsonData): Value to associate with key
            data (Optional[dict]): Optional data to update instead of loading
            
        Returns:
            bool: True if successful, False otherwise
            
        Note:
            If data is provided, it will be updated directly without loading from file
        """
        if data is None:
            data = self.load()
            if not isinstance(data, dict):
                print("Error: Data is not a dictionary")
                return False
        
        data[key] = value
        return self.save(data)
    
    def update_list(self, value: JsonData, data: Optional[list] = None) -> bool:
        """
        Append a value to a list.
        
        Args:
            value (JsonData): Value to append
            data (Optional[list]): Optional data to update instead of loading
            
        Returns:
            bool: True if successful, False otherwise
        """
        if data is None:
            data = self.load(output=True)
            if not isinstance(data, list):
                print("Error: Data is not a list")
                return False
        
        data.append(value)
        return self.save(data)
    
    # ==================== REMOVE OPERATIONS ====================
    
    def remove_from_dict(self, key: str, data: Optional[dict] = None) -> bool:
        """
        Remove a key from a dictionary.
        
        Args:
            key (str): Key to remove
            data (Optional[dict]): Optional data to update instead of loading
            
        Returns:
            bool: True if successful, False otherwise
        """
        if data is None:
            data = self.load()
            if not isinstance(data, dict):
                print("Error: Data is not a dictionary")
                return False
        
        if key in data:
            del data[key]
            return self.save(data)
        print(f"Key '{key}' not found")
        return False

    def remove_from_list(self, index: int = -1, data: Optional[list] = None) -> bool:
        """
        Remove item from a list by index.
        
        Args:
            index (int): Index to remove (default: -1 removes last item)
            data (Optional[list]): Optional data to update instead of loading
            
        Returns:
            bool: True if successful, False otherwise
        """
        if data is None:
            data = self.load(output=True)
            if not isinstance(data, list):
                print("Error: Data is not a list")
                return False
        
        if not data:
            print("List is empty")
            return False
        
        try:
            data.pop(index)
            return self.save(data)
        except IndexError:
            print(f"Index {index} out of range")
            return False

    def remove_from_list_by_value(self, value: JsonData, data: Optional[list] = None) -> bool:
        """
        Remove all occurrences of a value from a list.
        
        Args:
            value (JsonData): Value to remove
            data (Optional[list]): Optional data to update instead of loading
            
        Returns:
            bool: True if successful, False otherwise
        """
        if data is None:
            data = self.load(output=True)
            if not isinstance(data, list):
                print("Error: Data is not a list")
                return False
        
        if value not in data:
            print(f"Value '{value}' not found")
            return False
        
        data = [item for item in data if item != value]
        return self.save(data)
    
    # ==================== SEARCH OPERATIONS ====================
    
    def search_in_dict(self, key: str) -> Optional[JsonData]:
        """
        Search for a key in the dictionary data.
        
        Args:
            key (str): Key to search for
            
        Returns:
            Optional[JsonData]: Value if found, None otherwise
        """
        data = self.load()
        if isinstance(data, dict):
            return data.get(key, None)
        return None

    def search_in_list(self, value: JsonData) -> List[int]:
        """
        Find all indices of a value in a list.
        
        Args:
            value (JsonData): Value to search for
            
        Returns:
            List[int]: List of indices where the value appears
        """
        data = self.load(output=True)
        if isinstance(data, list):
            return [i for i, item in enumerate(data) if item == value]
        return []

    # ==================== INFORMATION OPERATIONS ====================
    
    def info(self) -> dict:
        """
        Get comprehensive information about the current data.
        
        Returns:
            dict: Information including type, size, file info, etc.
            
        Example:
            {
                "type": "dict",
                "file": "data.json",
                "exists": True,
                "file_size": 1024,
                "length": 5,
                "keys": ["key1", "key2"],
                "is_empty": False
            }
        """
        data = self.load()
        info_dict = {
            "type": type(data).__name__,
            "file": self.namefile,
            "exists": self.exists(),
            "file_size": os.path.getsize(self.namefile) if self.exists() else 0,
        }
        
        if isinstance(data, dict):
            info_dict.update({
                "length": len(data),
                "keys": list(data.keys())[:10],  # Limit to first 10 keys
                "is_empty": len(data) == 0
            })
        elif isinstance(data, list):
            info_dict.update({
                "length": len(data),
                "first_items": data[:5] if data else [],
                "is_empty": len(data) == 0
            })
        
        return info_dict

    def size(self) -> int:
        """
        Get the number of items in the data container.
        
        Returns:
            int: Length of dict/list, 0 for other types
        """
        data = self.load()
        if isinstance(data, (dict, list)):
            return len(data)
        return 0

    # ==================== FILE MANAGEMENT OPERATIONS ====================
    
    def clear(self, output: bool = False) -> bool:
        """
        Clear all data and save an empty container.
        
        Args:
            output (bool): If True, save empty list; otherwise empty dict
            
        Returns:
            bool: True if successful, False otherwise
        """
        empty_data = [] if output else {}
        return self.save(empty_data)

    def delete_file(self) -> bool:
        """
        Delete the JSON file permanently from disk.
        
        Returns:
            bool: True if successful, False otherwise
            
        Note:
            Prints confirmation message on success, error message on failure
        """
        try:
            if not self.exists():
                print(f"File '{self.namefile}' does not exist.")
                return False
            os.remove(self.namefile)
            print(f"✅ File '{self.namefile}' deleted successfully.")
            return True
        except PermissionError:
            print(f"❌ Permission denied: Cannot delete '{self.namefile}'")
            return False
        except Exception as e:
            print(f"❌ Error deleting file: {e}")
            return False

    def rename(self, new_name: str) -> bool:
        """
        Rename the JSON file.
        
        Args:
            new_name (str): New filename/path
            
        Returns:
            bool: True if successful, False otherwise
            
        Note:
            Updates self.namefile to the new name on success
        """
        try:
            if not self.exists():
                print(f"File '{self.namefile}' does not exist.")
                return False
            
            if os.path.exists(new_name):
                print(f"File '{new_name}' already exists.")
                return False
            
            os.rename(self.namefile, new_name)
            old_name = self.namefile
            self.namefile = new_name
            print(f"✅ File renamed from '{old_name}' to '{new_name}'.")
            return True
        except PermissionError:
            print(f"❌ Permission denied: Cannot rename '{self.namefile}'")
            return False
        except Exception as e:
            print(f"❌ Error renaming file: {e}")
            return False

    def restore(self, backup_file: str) -> bool:
        """
        Restore data from a backup file.
        
        Args:
            backup_file (str): Path to the backup file
            
        Returns:
            bool: True if successful, False otherwise
            
        Note:
            Uses shutil.copy2 which preserves metadata
        """
        try:
            if not os.path.exists(backup_file):
                print(f"❌ Backup file '{backup_file}' not found.")
                return False
            
            shutil.copy2(backup_file, self.namefile)
            print(f"✅ Restored from: {backup_file}")
            return True
        except Exception as e:
            print(f"❌ Restore failed: {e}")
            return False

    # ==================== DATA EXTRACTION OPERATIONS ====================

    def get_keys(self) -> List[str]:
        """
        Get all keys from dictionary data.
        
        Returns:
            List[str]: List of keys, empty list if not a dictionary
        """
        data = self.load()
        if isinstance(data, dict):
            return list(data.keys())
        return []

    def get_values(self) -> List:
        """
        Get all values from dictionary data.
        
        Returns:
            List: List of values, empty list if not a dictionary
        """
        data = self.load()
        if isinstance(data, dict):
            return list(data.values())
        return []

    # ==================== MERGE OPERATIONS ====================
    
    def merge(self, other_data: JsonContainer) -> bool:
        """
        Merge another dictionary/list into the current data.
        
        Args:
            other_data (JsonContainer): Data to merge (must match current type)
            
        Returns:
            bool: True if successful, False otherwise
            
        Note:
            - For dicts: uses update() to merge keys
            - For lists: uses extend() to append items
            - Types must match exactly
        """
        data = self.load()
        
        if isinstance(data, dict) and isinstance(other_data, dict):
            data.update(other_data)
            return self.save(data)
        elif isinstance(data, list) and isinstance(other_data, list):
            data.extend(other_data)
            return self.save(data)
        else:
            print("❌ Error: Data types must match")
            return False

    # ==================== MAGIC METHODS ====================
    
    def __len__(self) -> int:
        """
        Support len() function.
        
        Returns:
            int: Number of items in the data container
        """
        return self.size()

    def __str__(self) -> str:
        """
        String representation for printing.
        
        Returns:
            str: Human-readable representation
        """
        return f"WorkFileJson(file='{self.namefile}', items={self.size()})"

    def __repr__(self) -> str:
        """
        Representation for debugging.
        
        Returns:
            str: Debug-friendly representation
        """
        return f"WorkFileJson('{self.namefile}')"


# ==================== USAGE EXAMPLES ====================
"""
Example usage:
    
    # Create a new file handler
    handler = WorkFileJson("data.json")
    
    # Save dictionary data
    handler.save({"name": "John", "age": 30})
    
    # Update data
    handler.update_dict("email", "john@example.com")
    
    # Load data
    data = handler.load()
    print(data)  # {"name": "John", "age": 30, "email": "john@example.com"}
    
    # Get info
    info = handler.info()
    print(info)
    
    # List operations
    list_handler = WorkFileJson("list.json")
    list_handler.save(["apple", "banana", "orange"])
    list_handler.update_list("grape")
    
    # Search operations
    indices = list_handler.search_in_list("banana")
    print(indices)  # [1]
    
    # File management
    handler.restore("backup.json")
    handler.delete_file()
"""