"""
Secure Hashing Library - A comprehensive collection of cryptographic hashing utilities.

This module provides functions for hashing passwords, files, and text using various 
algorithms (SHA256, SHA512, SHA3, BLAKE2, etc.). It includes salted hashing for 
secure password storage, double hashing for additional security, hash comparison 
utilities, and batch file processing capabilities.

Core Features:
    - Password hashing with multiple algorithms
    - File hashing with chunked reading for large files
    - Automatic hash algorithm detection
    - Cryptographically secure salt generation
    - Salted password hashing and verification
    - Double hashing (hash-in-hash) for increased security
    - Hash comparison utilities
    - Batch file hashing with error handling
    - URL hashing for caching purposes
    - Convenience aliases for all functions

Security Notes:
    - Always use hash_with_salt() for password storage
    - Avoid MD5 and SHA-1 for security-critical applications
    - Default salt length of 16 is sufficient for most use cases
    - Double hashing is computationally expensive

Dependencies:
    - hashlib (standard library)
    - os (standard library)
    - secrets (standard library)
    - typing (standard library)
    - .Language (custom module providing ASCII_LOWERCASE and PRINTABLE_ASCII constants)

Author: Generated Code
Version: 1.0
License: Open Source

Example:
    >>> from hashing_lib import hash_with_salt, verify_password
    >>> 
    >>> # Store a password securely
    >>> result = hash_with_salt("my_secure_password", algorithm="sha256")
    >>> stored_hash = result['hash']
    >>> salt = result['salt']
    >>> 
    >>> # Verify later
    >>> is_valid = verify_password("my_secure_password", stored_hash, salt)
    >>> print(is_valid)
    True
"""
import hashlib
import os
import secrets
from typing import Union, List, Tuple, Generator
try:
    from allykit.data_kit.Language import  PRINTABLE_ASCII
except ImportError:
    raise ImportError("utile Not fully installed")
import re


hash_algorithms = [
    "md5", "sha1", "sha224", "sha256", "sha384", "sha512",
    "sha3-224", "sha3-256", "sha3-384", "sha3-512",
    "bcrypt", "scrypt", "argon2", "ntlm"
]

# ============== CORE HASHING FUNCTIONS ==============

def hash_password(password: str, algorithm: str = "sha256") -> str:
    """
    Hash a password using the specified algorithm.
    
    Args:
        password: The password to hash
        algorithm: Hashing algorithm (sha256, sha512, sha3_256, blake2b, etc.)
        algorithm == md5,sha1,sha224,sha256,sha384,sha512,sha3_224,sha3_256,sha3_384,sha3_512
    
    Returns:
        Hexadecimal digest of the hash
    
    Examples:
        >>> hash_password("mypassword", "sha256")
        '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'
    """
    try:
        hasher = hashlib.new(algorithm)
        hasher.update(password.encode('utf-8'))
        return hasher.hexdigest()
    except ValueError:
        raise ValueError(f"Unsupported algorithm: {algorithm}")


def hash_file(filepath: str, algorithm: str = "sha256") -> str:
    """
    Calculate hash of a file's contents.
    
    Args:
        filepath: Path to the file
        algorithm: Hashing algorithm to use
        algorithm == md5,sha1,sha224,sha256,sha384,sha512,sha3_224,sha3_256,sha3_384,sha3_512

    
    Returns:
        Hexadecimal digest of the file
    
    Raises:
        FileNotFoundError: If file doesn't exist
        PermissionError: If can't read the file
    """
    hasher = hashlib.new(algorithm)
    try:
        with open(filepath, 'rb') as f:
            # Read in chunks to handle large files
            for chunk in iter(lambda: f.read(8192), b''):
                hasher.update(chunk)
    except PermissionError:
        return "PermissionError"
    except FileNotFoundError:
        return "FileNotFoundError"
    return hasher.hexdigest()


def detect_hash_algorithm(hash_string: hashlib) -> Union[str, bool]:
    """
    Detect the hashing algorithm based on the hash length.
    
    Args:
        hash_string: The hash digest to analyze
        
    Returns:
        Algorithm name or False if unknown
    """
    length_map = {
        32: "md5",
        40: "sha1",
        56: "sha224",
        64: "sha256",
        96: "sha384",
        128: "sha512"
    }
    return length_map.get(len(hash_string), False)


def smart_hash_detector(hash_string: hashlib) -> str:
    """
    Detects the cryptographic hash algorithm of a given string.

    This function performs a two-tier analysis:
    1. Checks for common structured hash formats (e.g., Bcrypt, Unix-style hashes)
       using regular expressions.
    2. Validates hexadecimal-based hashes by analyzing their character set 
       (0-9, a-f) and their exact character length.

    Args:
        hash_string (hashlib): The raw hash string to be identified. 

    Returns:
        str: The name of the detected algorithm (e.g., 'MD5', 'Bcrypt') 
             or 'Unknown Format' if no match is found.
    """
    if not isinstance(hash_string, str):
        return "Invalid Input (Not a string)"

    hash_string = hash_string.strip()

    complex_patterns = {
        "Bcrypt": r'^\$2[ayb]\$.{56}$',
        "MD5 (Unix)": r'^\$1\$[a-zA-Z0-9./]+\$',
        "SHA-1 (Unix)": r'^\$sha1\$[a-zA-Z0-9./]+\$',
    }

    for name, pattern in complex_patterns.items():
        if re.match(pattern, hash_string):
            return name

    if re.fullmatch(r'[0-9a-fA-F]+', hash_string):
        length_map = {
            32: "MD5",
            40: "sha1",
            56: "sha224",
            64: "sha256",
            96: "sha384",
            128: "sha512"
        }
        return length_map.get(len(hash_string), "Unknown Hex Length")

    return "Unknown Format"

# ============== SECURE HASHING WITH SALT ==============

def generate_salt(length: int = 16) -> str:
    """Generate a cryptographically secure salt."""
    alphabet = PRINTABLE_ASCII
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def hash_with_salt(password: str, salt: str = None, algorithm: str = "sha256") -> dict:
    """
    Hash a password with a salt.
    
    Args:
        password: The password to hash
        salt: Optional salt (generated if not provided)
        algorithm: Hashing algorithm
        algorithm == md5,sha1,sha224,sha256,sha384,sha512,bcrypt,scrypt,argon2,ntlm,sha3_224,sha3_256,sha3_384,sha3_512        
    
    Returns:
        Dictionary containing hash, salt, and algorithm
    """
    if salt is None:
        salt = generate_salt()
    
    salted_password = password + salt
    hash_value = hash_password(salted_password, algorithm)
    
    return {
        'hash': hash_value,
        'salt': salt,
        'algorithm': algorithm
    }


def verify_password(password: str, stored_hash: str, salt: str, algorithm: str = "sha256") -> bool:
    """
    Verify a password against a stored hash and salt.
    
    Args:
        password: The password to verify
        stored_hash: The previously stored hash
        salt: The salt used when hashing
        algorithm: The algorithm used
        algorithm == md5,sha1,sha224,sha256,sha384,sha512,bcrypt,scrypt,argon2,ntlm,sha3_224,sha3_256,sha3_384,sha3_512
    
    Returns:
        True if password matches, False otherwise
    """
    result = hash_with_salt(password, salt, algorithm)
    return result['hash'] == stored_hash


# ============== DOUBLE HASHING (Hash-in-Hash) ==============

def double_hash(password: str, algorithm: str = "sha256") -> str:
    """
    Apply hashing twice for additional security (computationally expensive).
    
    Args:
        password: The password to hash
        algorithm: Hashing algorithm to use
        algorithm == md5,sha1,sha224,sha256,sha384,sha512,bcrypt,scrypt,argon2,ntlm,sha3_224,sha3_256,sha3_384,sha3_512
    
    Returns:
        Double-hashed value
    """
    first_hash = hash_password(password, algorithm)
    return hash_password(first_hash, algorithm)


# ============== HASH COMPARISON UTILITIES ==============

def compare_hash(hash_value: hashlib, *candidates: hashlib) -> List[Tuple[bool, str]]:
    """
    Compare a hash against multiple candidate values.
    
    Args:
        hash_value: The hash to compare
        hash_string == md5,sha1,sha224,sha256,sha384,sha512,bcrypt,scrypt,argon2,ntlm,sha3_224,sha3_256,sha3_384,sha3_512
        candidates: One or more hash values to compare against
    
    Returns:
        List of [is_match, candidate] pairs
    
    Examples:
        >>> compare_hash("abc123", "abc123", "def456", "xyz789")
        [[True, 'abc123'], [False, 'def456'], [False, 'xyz789']]
    """
    return [[hash_value == candidate, candidate] for candidate in candidates]


def find_matching_hashes(hash_value: hashlib, candidates: List[str]) -> List[str]:
    """
    Find all matches of a hash in a list of candidates.
    
    Args:
        hash_value: The hash to match
        hash_string == md5,sha1,sha224,sha256,sha384,sha512,bcrypt,scrypt,argon2,ntlm,sha3_224,sha3_256,sha3_384,sha3_512
        candidates: List of hash values to search
    
    Returns:
        List of matching hash values
    """
    return [h for h in candidates if h == hash_value]


# ============== BULK FILE HASHING ==============

def calculate_file_hashes(files: List[str], directory: str) -> Generator[Tuple[str, str], None, None]:
    """
    Generate SHA256 hashes for multiple files.
    
    Args:
        files: List of file names
        directory: Working directory path
    
    Yields:
        Tuple of (file_path, hash_value or error_message)
    
    Examples:
        >>> for path, hash_val in calculate_file_hashes(["a.txt", "b.txt"], "./"):
        ...     print(f"{path}: {hash_val}")
    """
    for file in files:
        filepath = os.path.join(directory, file)
        
        try:
            if os.path.isdir(filepath):
                yield filepath, "is_directory"
                continue
                
            hash_value = hash_file(filepath, "sha256")
            yield filepath, hash_value
            
        except FileNotFoundError:
            yield filepath, "not_found"
        except PermissionError:
            yield filepath, "permission_denied"
        except IsADirectoryError:
            yield filepath, "is_directory"
        except Exception as e:
            print(f"Error hashing {filepath}: {e}")
            yield filepath, f"error: {str(e)}"


# ============== URL HASHING ==============

def hash_url(url: str) -> str:
    """Create an MD5 hash of a URL (useful for caching)."""
    return hashlib.md5(url.encode()).hexdigest()

# ============== ALIASES ==============

HP = hash_password
HF = hash_file
DHA = detect_hash_algorithm
HWS = hash_with_salt
VP = verify_password
DH = double_hash
CH = compare_hash
FMH = find_matching_hashes
CFH = calculate_file_hashes
HU = hash_url
SHD = smart_hash_detector