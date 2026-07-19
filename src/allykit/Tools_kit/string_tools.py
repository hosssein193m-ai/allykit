from allykit.data_kit.Language import ASCII_LOWERCASE
import secrets
from typing import Optional, Union


def choice_string(charset=ASCII_LOWERCASE) -> str:
    """Return one cryptographically secure random character from charset."""
    return secrets.choice(charset)


def choice_string_yield(prefix: str = False, add: int = 3):
    """Yield random characters. If prefix provided, use it as charset, else use ASCII_LOWERCASE."""
    if prefix:
        for _ in range(add):
            yield secrets.choice(prefix)
    if not prefix:
        for _ in range(add):
            yield secrets.choice(ASCII_LOWERCASE)


def str_choice_string(charset: Optional[str] = None, add: int = 1) -> str:
    """Generate and return a string of random characters. Whitespace is stripped."""
    list_string = []
    if charset is None:   
        for item in choice_string_yield(prefix=False, add=add):
            list_string.append(item)
    if charset:    
        for item in choice_string_yield(prefix=charset, add=add):
            list_string.append(item)
    text =  ''.join(list_string)
    result = "".join(text.split())
    return result


def list_choice_string(add=3):
    """Return a list of random characters."""
    list_string= []
    for item in choice_string_yield(prefix=False, add=add):
        list_string.append(item)
    return list_string  


def truncate(text: str, max_len: int = 100, suffix: str = "") -> str:
    """Truncate text to max_len, preserving word boundaries, and append suffix."""
    if len(text) <= max_len:
        return text
    truncated = text[:max_len].rsplit(' ', 1)[0]
    return truncated + suffix


def format_thousands(number: Union[int, float]) -> str:
    """Format number with thousand separators (e.g., 1234567 -> '1,234,567')."""
    return f"{number:,}"