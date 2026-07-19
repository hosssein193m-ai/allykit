"""
web_allykit Member of the allykit module and web expert

A comprehensive web automation and scraping toolkit providing robust string manipulation, 
HTTP requests with retry mechanisms, HTML parsing, intelligent caching, and headless 
browser automation capabilities.

This module is designed for developers and data engineers requiring enterprise-grade 
web scraping solutions with production-ready features including:
- Automatic retry with exponential backoff
- Disk-based caching with TTL expiration
- JavaScript rendering via headless Chrome
- Lazy-load content extraction
- Bulk file downloads with collision prevention
- String normalization and validation
- Link validation and availability checking
- Multi-format data extraction (text, images, links)
- Advanced web monitoring with change detection
- HTML comparison and diff analysis
- Structured data extraction (JSON-LD)

Dependencies:
    - requests: HTTP client library
    - beautifulsoup4: HTML parsing
    - selenium: Browser automation
    - tenacity: Retry logic
    - pickle: Serialization for caching
    - hashlib: Cache key generation

TABLE OF CONTENTS:
    1. String Utilities
        - fix_url: Normalize and validate URLs
    2. HTTP Request Utilities
        - fetch_url: GET requests with retry
        - execute_request: Advanced HTTP requests (GET/POST with auth, proxies)
    3. Parsing & Extraction Utilities
        - soup_url: Fetch and parse HTML
        - extract_all_links: Extract hyperlinks with lazy-load support
        - extract_images: Extract image URLs with lazy-load support
        - extract_text_from_tags: Extract text from specific HTML tags
        - validate_links: Filter valid URLs
        - is_link_alive: Check URL accessibility
        - extract_structured_data: Extract JSON-LD structured data
    4. File Download Utilities
        - save_link: Download single file with streaming
        - save_links: Download multiple files with unique names
    5. Browser Automation Utilities
        - chrome: Configurable Chrome driver with extensive options
        - get_headless_driver: Headless Chrome driver
        - wait_for_element: Selenium explicit wait helper
        - browser_context: Context manager for automatic driver management
        - javascript: Basic JavaScript rendering
        - javascript_pro: Advanced JavaScript rendering with full interaction options
        - javascript_driver: Fetch content using existing WebDriver
    6. Disk Cache System
        - DiskCache: Persistent caching with TTL expiration
            - html: Cache static HTML pages
            - javascript: Cache basic JS-rendered pages
            - javascript_pro: Cache advanced JS-rendered pages with interactions
            - javascript_driver: Cache content from existing driver
            - update: Intelligent cache update with change detection
    7. HTML Comparison Utilities
        - SoupToDict: Compare two BeautifulSoup objects
            - get_changes: Analyze all differences
            - get_full_review: Get change status or detailed review
            - to_json: Export results as JSON
            - save_to_file: Save comparison results to file
            - has_item_changed: Check specific element changes
    8. Web Monitoring System
        - Monitoring: Advanced web monitoring with automatic caching
            - data: Extract and return data from request
            - set_all: Cache all data components
            - set: Cache specific data item
            - load: Load cached data from disk
            - update_all: Check changes and update cache
            - update: Selective update of changed components
            - status: Detailed change detection per component
            - refresh: Force complete refresh
            - remove: Remove cached files
            - remove_all: Remove cache directory
            - search: Search nested data with dot notation
            - get_cache_info: Get cache statistics
            - is_cached: Check if component is cached
            - get_cache_age: Get cache age in seconds
    9. Utility Aliases
        - EI, EAL, VL, ILA, ETFT, ER, NOC, ec, ESD, JP, JD: Shortcut functions

USAGE EXAMPLES:
    >>> # Basic page fetching and parsing
    >>> soup = soup_url("https://example.com")
    >>> links = extract_all_links(soup)
    
    >>> # Using cache for performance
    >>> cache = DiskCache(ttl_hours=48)
    >>> cached_soup = cache.get("https://example.com")
    
    >>> # JavaScript rendering for SPAs
    >>> dynamic_soup = javascript("https://react-app.com")
    
    >>> # Advanced JavaScript rendering with interactions
    >>> from selenium.webdriver.common.by import By
    >>> soup = javascript_pro(
    ...     "https://example.com/product",
    ...     scroll_to_bottom=True,
    ...     wait_for_element=(By.CSS_SELECTOR, ".price"),
    ...     headless=True
    ... )
    
    >>> # Bulk downloads
    >>> urls = ["https://site.com/file1.pdf", "https://site.com/file2.pdf"]
    >>> save_links(urls, "document")
    
    >>> # HTML comparison
    >>> comparator = SoupToDict(soup1, soup2)
    >>> changes = comparator.get_changes()
    >>> print(f"Total changes: {changes['summary']['total_changes']}")
    
    >>> # Web monitoring with automatic caching
    >>> monitor = Monitoring("https://example.com", ".cache")
    >>> monitor.set_all()  # Cache all data
    >>> if monitor.update_all():
    ...     print("No changes detected")
    ... else:
    ...     print("Content updated!")
    >>> 
    >>> # Search nested data
    >>> status_code = monitor.search("Short-form content.status_code")
    >>> print(f"Status: {status_code}")
"""
import logging
import re
from urllib.parse import urlparse, urlunparse


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    import requests
except ImportError:
    logger.error("pip install requests")
    raise


def fix_url(url: str,
            HTTP: bool = True,
            remove_fragment: bool = False,
            replaces: bool = True,
            verbal_ability: bool = True,
            test: bool = False
            ) -> str | bool:
    """
    Normalize and optionally validate a str.
    
    Args:
        url (str): Raw str string to normalize.
        HTTP (bool): If True, use HTTPS (except for localhost and local network IPs where HTTP is used). 
                     If False, force HTTP protocol.
        remove_fragment (bool): If True, remove everything after the '#' character.
        replaces (bool): If True, remove all whitespace characters from the str.
        verbal_ability (bool): If True, convert the domain to lowercase and normalize the path 
                               (e.g., remove duplicate slashes).
        test (bool): If True, test if the str is reachable and return a boolean.
    
    Returns:
        str: The normalized str string (if test=False).
        bool: True if the str is reachable, False otherwise (if test=True).
    
    Raises:
        TypeError: If input types are incorrect.
        ValueError: If the str is empty or becomes invalid after processing.
    
    Examples:
        >>> fix_url("Example.COM//API//Users")
        'https://example.com/API/Users'
        
        >>> fix_url("example.com", test=True)
        True  # If the site is available
        
        >>> fix_url("localhost:8000", HTTP=True)
        'http://localhost:8000' # Note: HTTP is used for localhost
        
        >>> fix_url("www.google.com", HTTP=False)
        'http://www.google.com'
    """
    if not isinstance(HTTP, bool):
        raise TypeError(f"HTTP must be bool (True/False), got {type(HTTP).__name__}")
    
    if not url or not url.strip():
        raise ValueError("str cannot be empty")
    
    url = url.strip()

    if url.startswith(("ftp://", "file://", "ws://", "wss://", "mailto:")):
        return url
    
    while url.startswith(("http://", "https://")):
        if url.startswith("http://"):
            url = url[7:]
        else:
            url = url[8:]
        
    if remove_fragment and '#' in url:
        url = url.split("#")[0] 
    
    if HTTP:
        local_prefixes = ("localhost", "127.", "192.168.", "10.", "172.", "::1")
        if any(url.startswith(p) for p in local_prefixes):
            url = "http://" + url
        else:
            url = "https://" + url
    
    else:
        url = "https://" + url 
    
    if replaces:
        url = url.replace(" ", "")
    
    if verbal_ability:
        parsed = urlparse(url)
        
        normalized_dict = {
            'scheme': parsed.scheme.lower(),
            'netloc': parsed.netloc.lower(),
            'path': '/' + '/'.join([p for p in parsed.path.split('/') if p]), 
            'params': parsed.params,
            'query': parsed.query,
            'fragment': parsed.fragment
        }
        
        url = urlunparse((normalized_dict['scheme'], normalized_dict['netloc'], 
                        normalized_dict['path'], normalized_dict['params'], 
                        normalized_dict['query'], normalized_dict['fragment']))

    
    if test:
        try:
            request = requests.get(url)
            if request.raise_for_status():
                return False
        except requests.exceptions.ConnectionError:
            return False
        return True
        
    url_pattern = re.compile(r'^https?://[a-zA-Z0-9.-]+(:[0-9]+)?(/[^#?]*)?(\?[^#]*)?(#.*)?$')

    if not url_pattern.match(url):
        raise ValueError(f"Generated invalid str: {url}")
    
    return str(url)
