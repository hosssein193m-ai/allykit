from allykit.data_kit.Language import (DECIMAL_DIGITS,
                PRINTABLE_ASCII, ASCII_UPPERCASE,
                ASCII_LOWERCASE,PUNCTUATION_ASCII)
import secrets
from allykit.Tools_kit.string_tools import *



def generate_password(length:int=10,charset=PRINTABLE_ASCII,add:int=2):# 
    """Generate a single password charset."""
    if add > length:
        raise ValueError("not :add > length")
    else:
        random_obj = secrets.randbelow(length - add + 1) + add
        password = str_choice_string(charset,add=random_obj)
    return password

def generate_password_with_prefix_suffix(password: str = None, length: int = 4, 
                                          prefix: str = '', suffix: bool = False,
                                          charset: str = PRINTABLE_ASCII, add: int = 3) -> str:
    if password is None:
        if add > length:
            raise ValueError("add cannot be greater than length")
        random_len = secrets.randbelow(length - add + 1) + add
        password = str_choice_string(charset, add=random_len)
    
    if not isinstance(suffix, bool):
        raise TypeError(f"suffix must be bool, got {type(suffix).__name__}")
    
    return f"{prefix}{password}" if not suffix else f"{password}{prefix}"

def list_password(length=10,charset=PRINTABLE_ASCII,add=3) -> list:
    """Return a list of passwords."""
    if add > length:
        raise TypeError("not :add > length")
    list_password = []
    for _ in range(length):
        random_obj = secrets.randbelow(length - add + 1) + add
        password = str_choice_string(charset,add=random_obj)
        list_password.append(password)
    return list_password

def str_password(length=10,charset=PRINTABLE_ASCII,add=3) -> str:
    """Return a concatenated charset of passwords."""
    if add > length:
        raise TypeError("not :add > length")
    list_password = []
    for _ in range(length):
        random_obj = secrets.randbelow(length - add + 1) + add
        password = str_choice_string(charset,add=random_obj)
        list_password.append(password)
    return ''.join(list_password)

def generate_strong_password(include_uppercase=False, include_digits=False, 
                              include_symbols=False, length=12) -> str:
    chars = ASCII_LOWERCASE
    if include_uppercase: chars += ASCII_UPPERCASE
    if include_digits: chars += DECIMAL_DIGITS
    if include_symbols: chars += PUNCTUATION_ASCII
    
    if not chars:
        raise ValueError("At least one character set must be selected")
    
    return ''.join(secrets.choice(chars) for _ in range(length))


