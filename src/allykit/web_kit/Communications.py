import logging
from typing import Union, Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    import requests
except ImportError:
    logger.error("pip install requests")
    raise

try:
    from tenacity import retry, stop_after_attempt, wait_exponential
except ImportError:
    logger.error("pip install tenacity")



@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def fetch_url(url: str, header: bool = False, 
              headers: dict | None = None,
            ) -> requests.Response:
    """
    Performs an HTTP GET request to a specified str with error handling.
    
    Args:
        url (str): The target str to fetch.
        header (bool): Whether to use custom headers. Defaults to False.
        headers (dict): Custom HTTP headers. Defaults to a standard Chrome User-Agent.
    
    Returns:
        requests.Response: The response object on successful request.
    
    Raises:
        requests.exceptions.RequestException: If the request fails.
    
    Examples:
        >>> response = fetch_url("https://api.example.com/data")
        >>> response.status_code
        200
    """
    from allykit.web_kit import fix_url    
    url = fix_url(url)
    default_headers  = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    try:
        if not header:
            request = requests.get(url)
        else:
            if headers is None:
                headers = default_headers
                request = requests.get(url, headers=headers)
        request.raise_for_status() 
    except requests.exceptions.RequestException as e: 
        raise requests.RequestException(f"Failed to retrieve str: {e}") from e
    return request

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def execute_request(url: str, method: str = "GET", headers: dict = None, 
                    proxies: dict = None, auth: tuple = None, data: dict = None) -> requests.Response:
    """
    Executes an HTTP request (GET or POST) with customizable configurations.
    
    Args:
        url (str): The target str.
        method (str): HTTP method, either "GET" or "POST". Defaults to "GET".
        headers (dict, optional): Custom HTTP headers. Defaults to None.
        proxies (dict, optional): Proxy configuration. Defaults to None.
        auth (tuple, optional): Basic authentication as (username, password). Defaults to None.
        data (dict, optional): POST data payload. Defaults to None.
    
    Returns:
        requests.Response: The response object on successful request.
    
    Raises:
        requests.exceptions.RequestException: If the request fails.
    
    Examples:
        >>> response = execute_request("https://httpbin.org/post", method="POST", data={"key": "value"})
        >>> response.status_code
        200
    """
    from allykit.web_kit import fix_url    
    url = fix_url(url)
    session = requests.Session()
    
    if headers: session.headers.update(headers)
    if proxies: session.proxies = proxies
    if auth: session.auth = auth

    try:
        if method.upper() == "POST":
            response = session.post(url, data=data)
        else:
            response = session.get(url) 
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"Failed to execute {method} request: {e}") from e

def validate_links(links: list[str], timeout: int = 5) -> list[str]:
    """
    Filters a list of URLs, returning only those that return a 200 OK status.
    
    Args:
        links (list): List of str strings to validate.
        timeout (int): Request timeout in seconds. Defaults to 5.
    
    Returns:
        list: Filtered list containing only responsive URLs.
    
    Examples:
        >>> validate_links(["https://google.com", "https://invalid.domain"], timeout=3)
        ['https://google.com']
    """
    from allykit.web_kit import fix_url
    valid_links = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    for link in links:
        link = fix_url(link)
        try:
            r = requests.head(link, timeout=timeout, allow_redirects=True, headers=headers)
            if r.status_code == 200:
                valid_links.append(link)
        except requests.RequestException:
            continue
    return valid_links

def is_link_alive(link: str, timeout: int = 5) -> bool:
    """
    Checks if a str is accessible and returns a 200 OK status.
    
    Args:
        link (str): The str to check.
        timeout (int): Request timeout in seconds. Defaults to 5.
    
    Returns:
        bool: True if str returns 200 OK, False otherwise.
    
    Examples:
        >>> is_link_alive("https://google.com")
        True
        >>> is_link_alive("https://invalid.domain")
        False
    """
    from allykit.web_kit import fix_url    
    link = fix_url(link)
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.head(link, timeout=timeout, allow_redirects=True, headers=headers)
        return r.status_code == 200
    except requests.RequestException:
        return False

def get_rate_limit_info(url: str) -> Dict[str, Union[int, str, None]]:
    """
    Extract rate limit information from HTTP response headers.

    This function sends a GET request to the specified URL and parses the response
    headers to extract rate limiting information. It's particularly useful when
    working with APIs that implement rate limiting to track remaining requests
    and plan request schedules accordingly.

    The function extracts standard rate limit headers and calculates how many
    requests have been made in the current rate limit window.

    Parameters:
        url (str): The target URL to check for rate limit information.
                   This should be the API endpoint you're querying.

    Returns:
        Dict[str, Union[int, str, None]]: A dictionary containing the following keys:
            - 'retry_after' (str | None): Time in seconds to wait before retrying
              (only present when rate limit is exceeded). Typically a string value
              that can be converted to integer.
            - 'remaining' (int | None): Number of requests remaining in the current
              rate limit window.
            - 'limit' (int | None): Total number of requests allowed in the rate
              limit window.
            - 'reset' (str | None): Timestamp or time in seconds until the rate
              limit resets.
            - 'Requests made' (int): Number of requests used in the current window,
              calculated as (limit - remaining). Returns 0 if limit or remaining
              are None.

    Raises:
        requests.exceptions.RequestException: If the request fails.
        ValueError: If the URL is invalid.
        TypeError: If limit or remaining headers cannot be converted to integers.

    Examples:
        >>> # Check rate limits for a public API
        >>> rate_info = get_rate_limit_info("https://api.github.com/users/octocat")
        >>> print(f"Requests remaining: {rate_info['remaining']}")
        >>> print(f"Total limit: {rate_info['limit']}")
        >>> print(f"Requests made: {rate_info['Requests made']}")
        
        >>> # Handle rate limiting in a loop
        >>> while True:
        ...     rate_info = get_rate_limit_info(api_url)
        ...     if rate_info['remaining'] == 0:
        ...         print(f"Rate limit exceeded. Waiting {rate_info['retry_after']} seconds...")
        ...         time.sleep(int(rate_info['retry_after']))
        ...         continue
        ...     # Make your API request
        ...     response = fetch_url(api_url)
        ...     # Process response...

        >>> # Check if you're approaching rate limits
        >>> rate_info = get_rate_limit_info("https://api.example.com/data")
        >>> remaining = rate_info['remaining']
        >>> if remaining and remaining < 10:
        ...     print(f"Warning: Only {remaining} requests remaining!")
        ...     print(f"Reset time: {rate_info['reset']}")
        ...     print(f"Requests used: {rate_info['Requests made']} of {rate_info['limit']}")

    Notes:
        - This function looks for common rate limit headers including:
          'retry-after', 'x-ratelimit-remaining', 'x-ratelimit-limit', 'x-ratelimit-reset'
        - Not all APIs use these standard headers. For custom APIs, you may need
          to modify the header names in the function.
        - The 'Requests made' calculation assumes that the 'limit' and 'remaining'
          headers are present and valid integers.
        - If rate limit headers are not found, all values except 'Requests made'
          will be None, and 'Requests made' will be 0.
        - This function uses fetch_url() which includes automatic retry logic.

    See Also:
        fetch_url: The underlying function used to make the request.
        is_link_alive: Check if a URL is accessible.
        validate_links: Filter valid URLs from a list.
    """
    response = fetch_url(url) 
    data = {}
    rate_limit_headers = ['retry-after', 'x-ratelimit-remaining', 'x-ratelimit-limit', 'x-ratelimit-reset']
    header_name = ['retry_after','remaining','limit','reset']
    for i, header in enumerate(rate_limit_headers):
        value = response.headers.get(header)
        data[header_name[i]] = value
    
    if data["limit"] is not None and data["remaining"] is not None:
        try:
            data['Requests made'] = int(data["limit"]) - int(data["remaining"])
        except (ValueError, TypeError):
            data['Requests made'] = 0
    else:
        data['Requests made'] = 0
    
    return data

def session_manager(headers: Optional[dict] = None, cookies: Optional[dict] = None):
    """
    Context manager for requests Session with custom headers and cookies.
    
    Creates a requests Session that automatically handles connection pooling,
    cookie persistence, and resource cleanup.
    
    Parameters
    ----------
    headers : Optional[dict], default=None
        HTTP headers to include in all requests (e.g., User-Agent, Authorization).
    
    cookies : Optional[dict], default=None
        Cookies to persist across all requests in the session.
    
    Yields
    ------
    requests.Session
        Configured Session object that automatically closes on context exit.
    
    Examples
    --------
    >>> with session_manager(headers={'User-Agent': 'MyBot/1.0'}) as session:
    ...     response = session.get('https://api.example.com/data')
    ...     print(response.json())
    
    >>> with session_manager(cookies={'session_id': 'abc123'}) as session:
    ...     session.get('https://example.com/login')
    ...     data = session.get('https://example.com/dashboard')
    
    Notes
    -----
    - Use with 'with' statement for automatic session cleanup
    - Session maintains cookies across multiple requests
    - More efficient than creating new requests for each call
    """
    session = requests.Session()
    if headers:
        session.headers.update(headers)
    if cookies:
        session.cookies.update(cookies)
    try:
        yield session
    finally:
        session.close()