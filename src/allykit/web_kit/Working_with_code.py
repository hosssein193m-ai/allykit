import logging
import json
from urllib.parse import urljoin
from typing import Dict
import difflib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from bs4 import BeautifulSoup
except ImportError:
    logger.error("pip install bs4")
    raise

try:
    import requests
except ImportError:
    logger.error("pip install requests")
    raise

try:
    from allykit.Security_kit.password_kit import str_choice_string
except ImportError:
    raise ImportError("allykit Not fully installed")


def extract_text_from_tags(soup: BeautifulSoup, tags: list[str] | str) -> list[str]:
    """
    Extracts text from specific HTML tags.
    
    Args:
        soup (BeautifulSoup): Parsed BeautifulSoup object.
        tags (list | str): HTML tag name(s) to extract text from (e.g., "p" or ["h1", "h2"]).
    
    Returns:
        list: List of extracted text strings, stripped of whitespace.
    
    Examples:
        >>> from bs4 import BeautifulSoup
        >>> soup = BeautifulSoup("<p>Hello</p><p>World</p>", "html.parser")
        >>> extract_text_from_tags(soup, "p")
        ['Hello', 'World']
    """
    return [tag.get_text(strip=True) for tag in soup.find_all(tags)]

def extract_all_links(soup: BeautifulSoup, base_url: str = None, check_lazy: bool = False) -> list[str]:
    """
    Extracts all unique hyperlinks, including optional support for lazy-loaded attributes.
    
    Args:
        soup (BeautifulSoup): Parsed BeautifulSoup object.
        base_url (str, optional): Base str for resolving relative links. Defaults to None.
        check_lazy (bool): Whether to also check for lazy-load attributes like 'data-lazy'. Defaults to False.
    
    Returns:
        list: Unique list of extracted hyperlink URLs.
    
    Examples:
        >>> from bs4 import BeautifulSoup
        >>> html = '<a href="/page1">Link</a><a href="https://example.com">External</a>'
        >>> soup = BeautifulSoup(html, "html.parser")
        >>> extract_all_links(soup, base_url="https://mysite.com")
        ['https://mysite.com/page1', 'https://example.com']
    """
    links = set()     
    for a in soup.find_all('a', href=True):
        href = a['href']
        if base_url:
            href = urljoin(base_url, href)
        links.add(href)
        if check_lazy:
            lazy_href = a.get('data-lazy')
            if lazy_href:
                if base_url:
                    lazy_href = urljoin(base_url, lazy_href)
                links.add(lazy_href)
    return list(links)

def extract_images(soup: BeautifulSoup, base_url: str = None, check_lazy: bool = False) -> list[str]:
    """
    Extracts all unique image source URLs, including lazy-loading attributes.
    
    Args:
        soup (BeautifulSoup): Parsed BeautifulSoup object.
        base_url (str, optional): Base str for resolving relative image paths. Defaults to None.
        check_lazy (bool): Whether to also check common lazy-load attributes (data-src, data-lazy, lazy-src). Defaults to False.
    
    Returns:
        list: Unique list of extracted image URLs.
    
    Examples:
        >>> from bs4 import BeautifulSoup
        >>> html = '<img src="image.jpg"><img data-src="lazy.jpg">'
        >>> soup = BeautifulSoup(html, "html.parser")
        >>> extract_images(soup, base_url="https://example.com", check_lazy=True)
        ['https://example.com/image.jpg', 'https://example.com/lazy.jpg']
    """
    image_urls = set()    
    for img in soup.find_all('img'):
        src = img.get('src')
        if src:
            if base_url: src = urljoin(base_url, src)
            image_urls.add(src)
        
        if check_lazy:
            for attr in ['data-src', 'data-lazy', 'lazy-src']:
                lazy_val = img.get(attr)
                if lazy_val:
                    if base_url:
                        lazy_val = urljoin(base_url, lazy_val)
                    image_urls.add(lazy_val)
    return list(image_urls)

def save_links(links: list[str], name_file: str, size: int = 8192,add: int = 8) -> bool:
    """
    Downloads multiple files using streaming with unique filenames.
    
    Args:
        links (list): List of URLs to download.
        name_file (str): Base filename (a unique suffix will be appended).
        size (int): Chunk size in bytes for streaming. Defaults to 8192.
        add (int): Complexity parameter for filename generation. Defaults to 8.
    
    Returns:
        bool: True if all downloads succeeded, False otherwise.
    
    Examples:
        >>> success = save_links(["https://example.com/file1.pdf", "https://example.com/file2.pdf"], "document")
        >>> # Creates files like "document_aB3.pdf", "document_xY9.pdf"
    """    
    success_count = 0
    for link in links:
        try:
            string = str_choice_string(add=add)
            with requests.get(link, stream=True) as r:
                r.raise_for_status() 
                with open(name_file + string, "wb") as f:
                    for chunk in r.iter_content(chunk_size=size):
                        if chunk: 
                            f.write(chunk)
            success_count += 1
        except requests.exceptions.RequestException as e:
            logger.error(f"Error downloading {link}: {e}")
            continue  
    return success_count == len(links)
    
def save_link(link: str, name_file: str, size: int = 8192) -> bool:
    """
    Downloads a single file using streaming to prevent high memory consumption.
    
    Args:
        link (str): The str of the file to download.
        name_file (str): Destination filename for the downloaded file.
        size (int): Chunk size in bytes for streaming. Defaults to 8192.
    
    Returns:
        bool: True if download succeeded, False otherwise.
    
    Examples:
        >>> success = save_link("https://example.com/image.jpg", "local_image.jpg")
        >>> success
        True
    """
    try:
        with requests.get(link, stream=True) as r:
            r.raise_for_status() 
            with open(name_file, "wb") as f:
                for chunk in r.iter_content(chunk_size=size):
                    if chunk: 
                        f.write(chunk)
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to download {link}: {e}")
        return False

def extract_structured_data(soup: BeautifulSoup) -> dict:
    """
    Extracts structured data (JSON-LD) from a BeautifulSoup object.

    This function searches the provided HTML soup for all <script> tags 
    with the type 'application/ld+json', parses the JSON content within 
    them, and aggregates the results into a dictionary.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object parsed from the target HTML.

    Returns:
        dict: A dictionary containing the extracted JSON-LD data. 
              The key 'json_ld' will store the data. 
              If multiple scripts are found, the last valid one will overwrite 
              previous entries in the 'json_ld' key.

    Raises:
        None: The function handles parsing errors internally using a 
              try-except block, skipping invalid JSON segments.
    """
    structured_data = {}
    
    json_ld = soup.find_all('script', type='application/ld+json')
    for script in json_ld:
        try:
            data = json.loads(script.string)
            structured_data['json_ld'] = data
        except (json.JSONDecodeError, TypeError):
            continue
        
    return structured_data


class SoupToDict:
    """
    Compare two BeautifulSoup objects and detect differences between them.
    
    This class provides comprehensive HTML comparison functionality by computing
    the difference between two parsed HTML documents. It identifies added,
    removed, and unchanged elements, generates a summary of changes, and allows
    exporting results in various formats including JSON.
    
    Features:
    - Computes hash of both HTML documents for quick equality check
    - Line-by-line difference analysis using difflib
    - Categorization of changes (added, removed, unchanged)
    - Summary statistics of changes
    - JSON export capability
    - File saving functionality
    - Individual element change detection
    
    Attributes:
        soup1 (BeautifulSoup): First HTML document for comparison
        soup2 (BeautifulSoup): Second HTML document for comparison
        hash_soup1 (str): MD5 hash of the first HTML document
        hash_soup2 (str): MD5 hash of the second HTML document
        lines1 (list): Lines from prettified first HTML document
        lines2 (list): Lines from prettified second HTML document
        changes (dict): Dictionary containing all detected changes
    
    Example:
        >>> from bs4 import BeautifulSoup
        >>> html1 = "<html><body><h1>Hello</h1></body></html>"
        >>> html2 = "<html><body><h1>World</h1></body></html>"
        >>> soup1 = BeautifulSoup(html1, "html.parser")
        >>> soup2 = BeautifulSoup(html2, "html.parser")
        >>> 
        >>> comparator = SoupToDict(soup1, soup2)
        >>> changes = comparator.get_changes()
        >>> print(changes['summary']['total_changes'])
        2
        >>> 
        >>> # Check if specific element changed
        >>> status = comparator.has_item_changed("<h1>Hello</h1>")
        >>> print(status)
        {'added': False, 'removed': True, 'unchanged': False}
        >>> 
        >>> # Export to JSON
        >>> json_output = comparator.to_json()
        >>> print(json_output)
    """
    
    def __init__(self, html1: BeautifulSoup, html2: BeautifulSoup):
        """
        Initialize the SoupToDict comparator with two BeautifulSoup objects.
        
        Args:
            html1 (BeautifulSoup): First parsed HTML document
            html2 (BeautifulSoup): Second parsed HTML document
            
        Example:
            >>> comparator = SoupToDict(soup1, soup2)
        """
        self.soup1 = html1
        self.soup2 = html2
        self.hash_soup1 = self._hash(html1)
        self.hash_soup2 = self._hash(html2)
        self.lines1 = self.soup1.prettify().splitlines()
        self.lines2 = self.soup2.prettify().splitlines()
        self.changes = self.get_changes()

    def _hash(self, soup: BeautifulSoup) -> str:
        """
        Generate MD5 hash of a BeautifulSoup object.
        
        Internal method used to compute hash fingerprints of HTML documents
        for quick equality comparisons.
        
        Args:
            soup (BeautifulSoup): The BeautifulSoup object to hash
            
        Returns:
            str: MD5 hash hex digest of the HTML content
        """
        from hashlib import md5
        return md5(str(soup).encode()).hexdigest()

    def get_changes(self) -> Dict[str, list]:
        """
        Analyze and categorize all differences between the two HTML documents.
        
        Uses Python's difflib to perform line-by-line comparison and categorizes
        each line as added, removed, or unchanged. Also generates a summary
        with change statistics.
        
        Returns:
            Dict[str, list]: Dictionary containing:
                - 'added': List of lines added in second document
                - 'removed': List of lines removed from first document
                - 'unchanged': List of lines present in both documents
                - 'summary': Statistics including counts of changes
                - 'hash soup': MD5 hashes of both documents
        
        Example:
            >>> changes = comparator.get_changes()
            >>> print(f"Added: {changes['summary']['added']}")
            >>> print(f"Removed: {changes['summary']['removed']}")
        """
        diff = difflib.ndiff(self.lines1, self.lines2)
        result = {'added': [], 'removed': [], 'unchanged': []}
        for line in diff:
            if line.startswith('+ '):
                result['added'].append(line[2:].strip())
            elif line.startswith('- '):
                result['removed'].append(line[2:].strip())
            elif line.startswith('  '):
                result['unchanged'].append(line[2:].strip())
        result['summary'] = {
            'added': len(result['added']),
            'removed': len(result['removed']),
            'unchanged': len(result['unchanged']),
            'total_changes': len(result['added']) + len(result['removed'])
        }
        result['hash soup'] = {"html1": self.hash_soup1, 'html2': self.hash_soup2}
        return result
        
    def get_full_review(self, output: bool | dict = True) -> dict | bool:
        """
        Get a comprehensive review of changes or just a change status.
        
        If HTML documents are identical, returns empty dict or False based on
        the output parameter. If different, returns changes or True.
        
        Args:
            output (bool | dict): If True (default), returns boolean status.
                                  If dict, returns the changes dictionary.
        
        Returns:
            dict | bool: If output=True: True if changes exist, False otherwise.
                        If output=dict: Changes dictionary if different,
                        empty dict if identical.
        
        Example:
            >>> # Get boolean status
            >>> has_changes = comparator.get_full_review()
            >>> 
            >>> # Get detailed changes
            >>> changes = comparator.get_full_review({})
        """
        if self.hash_soup1 == self.hash_soup2:
            return {} if isinstance(output, dict) else False
        return self.changes if isinstance(output, dict) else True
    
    def to_json(self, method: str = 'get_changes', **kwargs) -> str:
        """
        Export comparison results as JSON string.
        
        Args:
            method (str): Which method to use for data extraction.
                         Options: 'get_changes', 'get_full_review.bool',
                         'get_full_review.dict'. Default: 'get_changes'
            **kwargs: Additional arguments passed to json.dumps()
                     (e.g., indent, ensure_ascii)
        
        Returns:
            str: JSON formatted string of the comparison results
        
        Raises:
            ValueError: If an unsupported method is specified
        
        Example:
            >>> # Export full changes with pretty formatting
            >>> json_data = comparator.to_json(indent=4)
            >>> 
            >>> # Export as boolean status
            >>> status_json = comparator.to_json('get_full_review.bool')
        """
        if method == 'get_changes':
            data = self.changes
        elif method == 'get_full_review.bool':
            data = self.get_full_review()
        elif method == 'get_full_review.dict':
            data = self.get_full_review({})
        else:
            raise ValueError(f"Method '{method}' not supported. Use: get_changes, get_full_review.bool, get_full_review.dict")
        
        json_args = {
            'ensure_ascii': False,
            'indent': 2,
            **kwargs
        }
        return json.dumps(data, **json_args)

    def save_to_file(self, namefile: str) -> bool:
        """
        Save comparison results to a JSON file.
        
        Args:
            namefile (str): Path and name of the output file
            
        Returns:
            bool: True if save successful, False otherwise
        
        Example:
            >>> success = comparator.save_to_file("comparison_result.json")
            >>> if success:
            ...     print("File saved successfully")
        """
        text = self.changes
        try:
            with open(namefile, 'w', encoding='utf-8') as f:
                json.dump(text, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving file: {e}")
            return False

    def has_item_changed(self, item: str) -> Dict[str, bool]:
        """
        Check if a specific HTML element has changed in either document.
        
        Searches through added, removed, and unchanged lists to determine
        the status of a specific element.
        
        Args:
            item (str): The HTML element string to check
            
        Returns:
            Dict[str, bool]: Dictionary with three keys:
                - 'added': True if item was added in second document
                - 'removed': True if item was removed from first document
                - 'unchanged': True if item exists in both documents
        
        Example:
            >>> status = comparator.has_item_changed("<div class='main'>")
            >>> if status['removed']:
            ...     print("Element was removed")
        """
        data = self.changes
        added = data["added"]
        removed = data["removed"]
        unchanged = data['unchanged']
        return {
            "added": True if item in added else False,
            "removed": True if item in removed else False,
            "unchanged": True if item in unchanged else False
        }
    