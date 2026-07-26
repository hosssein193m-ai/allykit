from typing import Dict, Any, Tuple, List
from functools import wraps
import time
try:
    from selenium.webdriver.remote.webdriver import WebDriver
    from selenium.common.exceptions import JavascriptException
except ImportError:
    raise("pip install selenium")

def scroll_decorator(func):
    """
    Decorator for executing scroll scripts in Selenium.
    
    This decorator automatically executes JavaScript scroll scripts generated 
    by the wrapped functions in the browser.
    
    Args:
        func (callable): The function that generates the scroll script.
            Should return either:
            - A tuple (script_string, driver)
            - A string (script) while driver is found in arguments
    
    Returns:
        callable: Wrapped function that executes the script
    
    Raises:
        Exception: Any exception from driver.execute_script()
    
    Example:
        >>> @scroll_decorator
        ... def my_scroll_func(driver):
        ...     return 'window.scrollTo(0, 500)', driver
        >>> my_scroll_func(driver)  # Executes the script automatically
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        Wrapper function that receives and executes the script.
        
        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
            
        Returns:
            Any: Result from driver.execute_script() or original result
        """
        result = func(*args, **kwargs)
        
        # Case 1: Function returns a tuple (script, driver)
        if isinstance(result, tuple) and len(result) == 2:
            script, driver = result
            if isinstance(driver, WebDriver):
                return driver.execute_script(script)
        
        # Case 2: Function returns just the script string
        elif isinstance(result, str):
            driver = None
            # Search for driver in positional arguments
            for arg in args:
                if isinstance(arg, WebDriver):
                    driver = arg
                    break
            
            # Search for driver in keyword arguments
            if not driver:
                for key, value in kwargs.items():
                    if isinstance(value, WebDriver):
                        driver = value
                        break
            
            if driver:
                return driver.execute_script(result)
        
        # Return result unchanged if no driver or script found
        return result
    return wrapper


def py_scroll(driver: WebDriver, timeout: int = 2, max_scrolls: int = 50, smooth: bool = False) -> int:
    """
    Scroll to the bottom of the page to load dynamic content.
    
    Continuously scrolls down until no new content is loaded or max scrolls reached.
    Useful for infinite-scroll pages (social media, galleries, etc.).
    
    Args:
        driver: Selenium WebDriver instance
        timeout: Wait time between scrolls in seconds (default: 2)
        max_scrolls: Maximum number of scroll attempts (default: 50)
        smooth: Use smooth scrolling animation (default: False)
    
    Returns:
        Number of scroll attempts made
    
    Example:
        >>> attempts = py_scroll(driver, timeout=1.5, max_scrolls=30)
        >>> print(f"Scrolled {attempts} times to load all content")
    """
    scroll_count = 0
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while scroll_count < max_scrolls:
        if smooth:
            driver.execute_script("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'})")
        else:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        
        time.sleep(timeout)
        
        try:
            new_height = driver.execute_script("return document.body.scrollHeight")
        except JavascriptException:
            print("JS execution error")
            break
        
        if new_height == last_height:
            print(f"Reached bottom after {scroll_count + 1} scrolls")
            break
            
        last_height = new_height
        scroll_count += 1
        
        if scroll_count % 10 == 0:
            print(f"Scroll {scroll_count}: new height = {new_height}px")
    
    if scroll_count >= max_scrolls:
        print(f"Reached maximum scrolls ({max_scrolls})")
    
    return scroll_count

   
@scroll_decorator
def window_scrollTo(driver: WebDriver, x: int = 0, y: int = 0, return_value: bool = False) -> Any:
    """
    Scroll to specific coordinates on the page.
    
    Scrolls the page to the specified (x, y) coordinates. This is the most
    basic scroll function that provides precise control over scroll position.
    
    Args:
        driver (WebDriver): Selenium WebDriver instance
        x (int): Horizontal position in pixels (default: 0)
        y (int): Vertical position in pixels (default: 0)
        return_value (bool): If True, returns the script's output (default: False)
    
    Returns:
        Any: If return_value=True, returns the script's output; otherwise None
    
    Example:
        >>> window_scrollTo(driver, 0, 500)  # Scroll down 500px
        >>> window_scrollTo(driver, 100, 200)  # Scroll to (100, 200)
        >>> pos = window_scrollTo(driver, 0, 0, True)  # Scroll to top and return
    """
    if return_value:
        return f'return window.scrollTo({x}, {y})', driver
    return f'window.scrollTo({x}, {y})', driver


@scroll_decorator
def window_scrollTo_bottom(driver: WebDriver, return_value: bool = False) -> Any:
    """
    Scroll to the bottom of the page.
    
    Scrolls the page to the absolute bottom by using document.body.scrollHeight.
    Useful for loading dynamically loaded content (infinite scroll).
    
    Args:
        driver (WebDriver): Selenium WebDriver instance
        return_value (bool): If True, returns the script's output (default: False)
    
    Returns:
        Any: If return_value=True, returns the script's output; otherwise None
    
    Example:
        >>> window_scrollTo_bottom(driver)  # Scroll to bottom
        >>> # For infinite scroll pages:
        >>> for i in range(5):
        ...     window_scrollTo_bottom(driver)
        ...     time.sleep(2)
    """
    if return_value:
        return 'return window.scrollTo(0, document.body.scrollHeight)', driver
    return 'window.scrollTo(0, document.body.scrollHeight)', driver


@scroll_decorator
def window_scrollTo_top(driver: WebDriver, return_value: bool = False) -> Any:
    """
    Scroll to the top of the page.
    
    Scrolls the page to the very top (origin). Useful for resetting scroll
    position or navigating back to the beginning of a page.
    
    Args:
        driver (WebDriver): Selenium WebDriver instance
        return_value (bool): If True, returns the script's output (default: False)
    
    Returns:
        Any: If return_value=True, returns the script's output; otherwise None
    
    Example:
        >>> window_scrollTo_top(driver)  # Scroll to top
        >>> # After scrolling to bottom:
        >>> window_scrollTo_bottom(driver)
        >>> time.sleep(1)
        >>> window_scrollTo_top(driver)  # Go back to top
    """
    if return_value:
        return 'return window.scrollTo(0, 0)', driver
    return 'window.scrollTo(0, 0)', driver


@scroll_decorator
def window_scrollTo_right(driver: WebDriver, return_value: bool = False) -> Any:
    """
    Scroll to the rightmost edge of the page.
    
    Scrolls horizontally to the far right edge of the page. Useful for
    wide pages or horizontal scrolling scenarios.
    
    Args:
        driver (WebDriver): Selenium WebDriver instance
        return_value (bool): If True, returns the script's output (default: False)
    
    Returns:
        Any: If return_value=True, returns the script's output; otherwise None
    
    Example:
        >>> window_scrollTo_right(driver)  # Scroll to far right
    """
    if return_value:
        return 'return window.scrollTo(document.body.scrollWidth, 0)', driver
    return 'window.scrollTo(document.body.scrollWidth, 0)', driver


@scroll_decorator
def scroll_smooth_to(driver: WebDriver, x: int = 0, y: int = 0) -> None:
    """
    Smooth scroll to specific coordinates.
    
    Scrolls to the specified coordinates with a smooth animation effect.
    Provides better user experience for visible scrolling operations.
    
    Args:
        driver (WebDriver): Selenium WebDriver instance
        x (int): Horizontal position in pixels (default: 0)
        y (int): Vertical position in pixels (default: 0)
    
    Returns:
        None
    
    Example:
        >>> scroll_smooth_to(driver, 0, 500)  # Smooth scroll down 500px
        >>> scroll_smooth_to(driver, 100, 200)  # Smooth scroll to (100, 200)
    """
    return f'window.scrollTo({{top: {y}, left: {x}, behavior: "smooth"}})', driver


@scroll_decorator
def scroll_to_element(driver: WebDriver, selector: str, by: str = 'css', smooth: bool = True) -> bool:
    """
    Scroll to a specific element on the page.
    
    Finds an element using the provided selector and scrolls to it.
    The element will be centered in the viewport after scrolling.
    
    Args:
        driver (WebDriver): Selenium WebDriver instance
        selector (str): Element selector (e.g., "#id", ".class", "div")
        by (str): Selector type - 'css' or 'id' (default: 'css')
        smooth (bool): Use smooth scroll animation (default: True)
    
    Returns:
        bool: True if the element was found and scrolled to, False otherwise
    
    Raises:
        ValueError: If 'by' parameter is not 'css' or 'id'
    
    Example:
        >>> # Scroll to a button using CSS selector
        >>> scroll_to_element(driver, "#submit-btn")
        >>> # Scroll to an element using ID
        >>> scroll_to_element(driver, "my-element", by="id")
        >>> # Scroll without animation
        >>> scroll_to_element(driver, ".header", smooth=False)
    """
    behavior = '"smooth"' if smooth else '"auto"'
    
    if by.lower() == 'css':
        return f'''
            var element = document.querySelector("{selector}");
            if(element) {{
                element.scrollIntoView({{behavior: {behavior}, block: "center"}});
                return true;
            }}
            return false;
        ''', driver
    
    elif by.lower() == 'id':
        return f'''
            var element = document.getElementById("{selector}");
            if(element) {{
                element.scrollIntoView({{behavior: {behavior}, block: "center"}});
                return true;
            }}
            return false;
        ''', driver
    
    else:
        raise ValueError(f"Invalid 'by' value: {by}. Use 'css' or 'id'")


@scroll_decorator
def get_scroll_info(driver: WebDriver) -> Dict[str, Any]:
    """
    Get comprehensive scroll position information.
    
    Returns detailed information about the current scroll state and
    page dimensions. Useful for debugging and conditional logic.
    
    Args:
        driver (WebDriver): Selenium WebDriver instance
    
    Returns:
        Dict[str, Any]: Dictionary containing:
            - scrollX (int): Current horizontal scroll position
            - scrollY (int): Current vertical scroll position
            - scrollWidth (int): Total page width
            - scrollHeight (int): Total page height
            - clientWidth (int): Visible viewport width
            - clientHeight (int): Visible viewport height
            - maxScrollX (int): Maximum horizontal scroll possible
            - maxScrollY (int): Maximum vertical scroll possible
            - isAtBottom (bool): Whether at bottom of page
            - isAtTop (bool): Whether at top of page
            - isAtRight (bool): Whether at rightmost edge
            - isAtLeft (bool): Whether at leftmost edge
            - percentageScrolled (str): Percentage of page scrolled
    
    Example:
        >>> info = get_scroll_info(driver)
        >>> print(f"Scrolled: {info['percentageScrolled']}%")
        >>> if info['isAtBottom']:
        ...     print("At bottom of page")
        >>> print(f"Page height: {info['scrollHeight']}px")
    """
    return '''
        return {
            scrollX: window.pageXOffset,
            scrollY: window.pageYOffset,
            scrollWidth: document.documentElement.scrollWidth,
            scrollHeight: document.documentElement.scrollHeight,
            clientWidth: document.documentElement.clientWidth,
            clientHeight: document.documentElement.clientHeight,
            maxScrollX: document.documentElement.scrollWidth - document.documentElement.clientWidth,
            maxScrollY: document.documentElement.scrollHeight - document.documentElement.clientHeight,
            isAtBottom: (window.innerHeight + window.pageYOffset) >= document.documentElement.scrollHeight - 10,
            isAtTop: window.pageYOffset === 0,
            isAtRight: (window.innerWidth + window.pageXOffset) >= document.documentElement.scrollWidth - 10,
            isAtLeft: window.pageXOffset === 0,
            percentageScrolled: ((window.pageYOffset / (document.documentElement.scrollHeight - window.innerHeight)) * 100).toFixed(2)
        };
    ''', driver


@scroll_decorator
def scroll_to_percentage(driver: WebDriver, percentage: int) -> int:
    """
    Scroll to a specific percentage of the page.
    
    Scrolls to a percentage point between 0% (top) and 100% (bottom)
    of the total scrollable height.
    
    Args:
        driver (WebDriver): Selenium WebDriver instance
        percentage (int): Target percentage (0 to 100)
    
    Returns:
        int: The actual pixel position scrolled to
    
    Raises:
        ValueError: If percentage is not between 0 and 100
    
    Example:
        >>> scroll_to_percentage(driver, 50)  # Scroll to middle of page
        >>> scroll_to_percentage(driver, 75)  # Scroll to 75% down
        >>> scroll_to_percentage(driver, 0)   # Scroll to top
        >>> scroll_to_percentage(driver, 100) # Scroll to bottom
    """
    if not 0 <= percentage <= 100:
        raise ValueError(f"Percentage must be between 0 and 100, got {percentage}")
    
    return f'''
        var scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
        var scrollTo = (scrollHeight * {percentage}) / 100;
        window.scrollTo({{top: scrollTo, behavior: "smooth"}});
        return scrollTo;
    ''', driver


@scroll_decorator
def scroll_until_element_visible(driver: WebDriver, selector: str, max_attempts: int = 30) -> str:
    """
    Scroll progressively until an element becomes visible.
    
    Performs multiple scroll attempts until the specified element
    becomes visible in the viewport or max attempts are reached.
    
    Args:
        driver (WebDriver): Selenium WebDriver instance
        selector (str): Element selector (e.g., "#id", ".class")
        max_attempts (int): Maximum scroll attempts (default: 30)
    
    Returns:
        str: Status message indicating success or failure
    
    Example:
        >>> result = scroll_until_element_visible(driver, ".lazy-load")
        >>> print(result)  # "Element is visible!" or error message
        >>> 
        >>> # For elements that load lazily:
        >>> result = scroll_until_element_visible(driver, "#dynamic-content", max_attempts=20)
        >>> if "visible" in result:
        ...     # Element found, proceed with actions
    """
    return f'''
        var selector = "{selector}";
        var attempts = 0;
        var maxAttempts = {max_attempts};
        var found = false;
        
        function checkAndScroll() {{
            var element = document.querySelector(selector);
            if(element) {{
                var rect = element.getBoundingClientRect();
                if(rect.top >= 0 && rect.bottom <= window.innerHeight) {{
                    found = true;
                    element.scrollIntoView({{behavior: "smooth", block: "center"}});
                    return "Element is visible!";
                }}
            }}
            
            if(attempts >= maxAttempts) {{
                return "Element not found or not visible after " + maxAttempts + " attempts";
            }}
            
            window.scrollBy(0, window.innerHeight * 0.7);
            attempts++;
            
            setTimeout(checkAndScroll, 300);
        }}
        
        return checkAndScroll();
    ''', driver


@scroll_decorator
def scroll_infinite_loader(driver: WebDriver, max_scrolls: int = 10, check_interval: float = 1.5) -> Dict[str, Any]:
    """
    Scroll down repeatedly to load infinite scroll content.
    
    Continuously scrolls down until no new content is loaded or max_scrolls is reached.
    Useful for loading all content in infinite scroll pages like social media feeds.
    
    Args:
        driver (WebDriver): Selenium WebDriver instance
        max_scrolls (int): Maximum number of scroll attempts (default: 10)
        check_interval (float): Time to wait between scrolls in seconds (default: 1.5)
    
    Returns:
        Dict[str, Any]: Dictionary containing:
            - total_scrolls (int): Number of scrolls performed
            - initial_height (int): Height before scrolling
            - final_height (int): Height after scrolling
            - height_increase (int): Total height increase
            - stopped_reason (str): Reason for stopping 
                ('max_scrolls', 'no_new_content', or 'page_bottom')
    
    Example:
        >>> result = scroll_infinite_loader(driver, max_scrolls=5)
        >>> print(f"Loaded {result['height_increase']}px of new content")
        >>> if result['stopped_reason'] == 'no_new_content':
        ...     print("All content loaded!")
    """
    return f'''
        var maxScrolls = {max_scrolls};
        var checkInterval = {check_interval} * 1000;
        var scrollCount = 0;
        var initialHeight = document.documentElement.scrollHeight;
        var lastHeight = initialHeight;
        var newHeight = initialHeight;
        var result = null;
        var finished = false;
        
        function checkContent() {{
            if (finished) return;
            
            if (scrollCount >= maxScrolls) {{
                result = {{
                    total_scrolls: scrollCount,
                    initial_height: initialHeight,
                    final_height: document.documentElement.scrollHeight,
                    height_increase: document.documentElement.scrollHeight - initialHeight,
                    stopped_reason: 'max_scrolls'
                }};
                finished = true;
                return;
            }}
            
            // Scroll to bottom
            window.scrollTo(0, document.documentElement.scrollHeight);
            scrollCount++;
            
            // Check if new content loaded
            setTimeout(function() {{
                newHeight = document.documentElement.scrollHeight;
                if (newHeight > lastHeight) {{
                    lastHeight = newHeight;
                    // Continue scrolling
                    checkContent();
                }} else {{
                    result = {{
                        total_scrolls: scrollCount,
                        initial_height: initialHeight,
                        final_height: document.documentElement.scrollHeight,
                        height_increase: document.documentElement.scrollHeight - initialHeight,
                        stopped_reason: 'no_new_content'
                    }};
                    finished = true;
                }}
            }}, checkInterval);
        }}
        
        // Start the scrolling process
        checkContent();
        
        // Wait for completion (Selenium needs synchronous return)
        var startTime = Date.now();
        var timeout = (maxScrolls * {check_interval} * 1000) + 5000;
        
        while (!finished && (Date.now() - startTime) < timeout) {{
            // Busy wait (not ideal but necessary for Selenium)
        }}
        
        if (!finished) {{
            result = {{
                total_scrolls: scrollCount,
                initial_height: initialHeight,
                final_height: document.documentElement.scrollHeight,
                height_increase: document.documentElement.scrollHeight - initialHeight,
                stopped_reason: 'timeout'
            }};
        }}
        
        return result;
    ''', driver


@scroll_decorator
def scroll_animated_spiral(driver: WebDriver, target_y: int = 500) -> None:
    """
    Scroll with a spiral animation effect.
    
    Performs a unique spiral-like scrolling animation for visual effect.
    Useful for demonstration or creative purposes.
    
    Args:
        driver (WebDriver): Selenium WebDriver instance
        target_y (int): Target vertical position (default: 500)
    
    Example:
        >>> scroll_animated_spiral(driver, 800)  # Spiral scroll to 800px
    """
    return f'''
        var targetY = {target_y};
        var startY = window.pageYOffset;
        var duration = 1500;
        var startTime = null;
        var amplitude = 30;
        var frequency = 0.05;
        
        function animateScroll(timestamp) {{
            if (!startTime) startTime = timestamp;
            var progress = Math.min((timestamp - startTime) / duration, 1);
            var easeProgress = 1 - Math.pow(1 - progress, 3);
            var currentY = startY + (targetY - startY) * easeProgress;
            var offsetX = amplitude * Math.sin(progress * Math.PI * frequency * 1000);
            
            window.scrollTo(offsetX, currentY);
            
            if (progress < 1) {{
                requestAnimationFrame(animateScroll);
            }} else {{
                window.scrollTo(0, targetY);
            }}
        }}
        
        requestAnimationFrame(animateScroll);
    ''', driver


@scroll_decorator
def scroll_to_text(driver: WebDriver, text: str, smooth: bool = True) -> bool:
    """
    Scroll to the first element containing specific text.
    
    Finds and scrolls to the first element that contains the given text.
    Useful for navigating to specific content without knowing the selector.
    
    Args:
        driver (WebDriver): Selenium WebDriver instance
        text (str): Text to search for
        smooth (bool): Use smooth scroll animation (default: True)
    
    Returns:
        bool: True if text was found and scrolled to, False otherwise
    
    Example:
        >>> scroll_to_text(driver, "Contact Us")  # Scroll to "Contact Us" section
        >>> scroll_to_text(driver, "Pricing", smooth=False)
    """
    behavior = '"smooth"' if smooth else '"auto"'
    
    return f'''
        var text = "{text}";
        var elements = document.getElementsByTagName('*');
        var found = false;
        
        for (var i = 0; i < elements.length; i++) {{
            if (elements[i].textContent.includes(text)) {{
                elements[i].scrollIntoView({{behavior: {behavior}, block: "center"}});
                found = true;
                break;
            }}
        }}
        
        return found;
    ''', driver


class ScrollManager:
    """
    Scroll Manager class for Selenium WebDriver.
    
    Provides a unified, simple interface for all scroll operations.
    This is the recommended way to use the scroll functionality.
    
    Attributes:
        driver (WebDriver): Selenium WebDriver instance
    
    Example:
        >>> driver = WebDriver()
        >>> scroll = ScrollManager(driver)
        >>> scroll.to_bottom()  # Scroll to bottom
        >>> info = scroll.get_info()  # Get scroll information
        >>> scroll.to_element("#my-element")  # Scroll to element
    """
    
    def __init__(self, driver: WebDriver):
        """
        Initialize the ScrollManager.
        
        Args:
            driver (WebDriver): Selenium WebDriver instance
        """
        self.driver = driver
    
    def to(self, x: int = 0, y: int = 0) -> Any:
        """
        Scroll to specific coordinates.
        
        Args:
            x (int): Horizontal position
            y (int): Vertical position
        
        Returns:
            Any: Script execution result
        
        Example:
            >>> scroll.to(0, 500)  # Scroll down 500px
        """
        return window_scrollTo(self.driver, x, y)
    
    def to_bottom(self) -> Any:
        """
        Scroll to the bottom of the page.
        
        Returns:
            Any: Script execution result
        
        Example:
            >>> scroll.to_bottom()
        """
        return window_scrollTo_bottom(self.driver)
    
    def to_top(self) -> Any:
        """
        Scroll to the top of the page.
        
        Returns:
            Any: Script execution result
        
        Example:
            >>> scroll.to_top()
        """
        return window_scrollTo_top(self.driver)
    
    def to_right(self) -> Any:
        """
        Scroll to the rightmost edge of the page.
        
        Returns:
            Any: Script execution result
        
        Example:
            >>> scroll.to_right()
        """
        return window_scrollTo_right(self.driver)
    
    def smooth_to(self, x: int = 0, y: int = 0) -> None:
        """
        Smooth scroll to specific coordinates.
        
        Args:
            x (int): Horizontal position
            y (int): Vertical position
        
        Example:
            >>> scroll.smooth_to(0, 500)  # Smooth scroll down
        """
        return scroll_smooth_to(self.driver, x, y)
    
    def to_element(self, selector: str, by: str = 'css', smooth: bool = True) -> bool:
        """
        Scroll to a specific element.
        
        Args:
            selector (str): Element selector
            by (str): Selector type - 'css' or 'id'
            smooth (bool): Use smooth scroll animation
        
        Returns:
            bool: True if successful, False otherwise
        
        Example:
            >>> scroll.to_element("#submit-btn")
        """
        return scroll_to_element(self.driver, selector, by, smooth)
    
    def to_percentage(self, percentage: int) -> int:
        """
        Scroll to a percentage of the page.
        
        Args:
            percentage (int): Target percentage (0-100)
        
        Returns:
            int: The position scrolled to
        
        Example:
            >>> scroll.to_percentage(50)  # Scroll to middle
        """
        return scroll_to_percentage(self.driver, percentage)
    
    def get_info(self) -> Dict[str, Any]:
        """
        Get comprehensive scroll information.
        
        Returns:
            Dict[str, Any]: Scroll information dictionary
        
        Example:
            >>> info = scroll.get_info()
            >>> print(info['percentageScrolled'])
        """
        return get_scroll_info(self.driver)
    
    def py_scroll(self, timeout: int = 2, max_scrolls: int = 50, smooth: bool = False):
        return py_scroll(self.driver, timeout, max_scrolls , smooth)

    def until_element_visible(self, selector: str, max_attempts: int = 30) -> str:
        """
        Scroll until an element becomes visible.
        
        Args:
            selector (str): Element selector
            max_attempts (int): Maximum scroll attempts
        
        Returns:
            str: Status message
        
        Example:
            >>> result = scroll.until_element_visible(".lazy-load")
        """
        return scroll_until_element_visible(self.driver, selector, max_attempts)
    
    def wait_for_bottom(self, timeout: int = 10) -> bool:
        """
        Wait until the page reaches the bottom.
        
        Periodically checks scroll position until the bottom is reached
        or the timeout expires.
        
        Args:
            timeout (int): Maximum wait time in seconds (default: 10)
        
        Returns:
            bool: True if bottom reached, False if timeout
        
        Example:
            >>> scroll.to_bottom()
            >>> if scroll.wait_for_bottom(5):
            ...     print("Reached bottom!")
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            info = self.get_info()
            if info.get('isAtBottom'):
                return True
            time.sleep(0.5)
        
        return False
    
    def wait_for_top(self, timeout: int = 10) -> bool:
        """
        Wait until the page reaches the top.
        
        Args:
            timeout (int): Maximum wait time in seconds (default: 10)
        
        Returns:
            bool: True if top reached, False if timeout
        
        Example:
            >>> scroll.to_top()
            >>> if scroll.wait_for_top(3):
            ...     print("At top!")
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            info = self.get_info()
            if info.get('isAtTop'):
                return True
            time.sleep(0.5)

        return False
    
    def scroll_by(self, delta_x: int = 0, delta_y: int = 100) -> None:
        """
        Scroll relative by a specified amount.
        
        Args:
            delta_x (int): Horizontal scroll amount (default: 0)
            delta_y (int): Vertical scroll amount (default: 100)
        
        Example:
            >>> scroll.scroll_by(delta_y=200)  # Scroll down 200px
            >>> scroll.scroll_by(delta_y=-100)  # Scroll up 100px
            >>> scroll.scroll_by(delta_x=50)  # Scroll right 50px
        """
        script = f'window.scrollBy({delta_x}, {delta_y})'
        self.driver.execute_script(script)
    
    def scroll_to_element_and_wait(self, selector: str, timeout: int = 5) -> bool:
        """
        Scroll to an element and wait for it to load.
        
        Args:
            selector (str): Element selector
            timeout (int): Wait time in seconds (default: 5)
        
        Returns:
            bool: True if successful, False otherwise
        
        Example:
            >>> scroll.scroll_to_element_and_wait("#dynamic-content", 3)
        """
        result = self.to_element(selector)
        if result:
            time.sleep(timeout)
            return True
        return False
    
    def smooth_scroll_to_bottom(self) -> None:
        """
        Smoothly scroll to the bottom of the page.
        
        Example:
            >>> scroll.smooth_scroll_to_bottom()
        """
        self.driver.execute_script('window.scrollTo({top: document.body.scrollHeight, behavior: "smooth"})')
    
    def smooth_scroll_to_top(self) -> None:
        """
        Smoothly scroll to the top of the page.
        
        Example:
            >>> scroll.smooth_scroll_to_top()
        """
        self.driver.execute_script('window.scrollTo({top: 0, behavior: "smooth"})')
    
    def load_infinite_content(self, max_scrolls: int = 10) -> Dict[str, Any]:
        """
        Load all content in an infinite scroll page.
        
        Args:
            max_scrolls (int): Maximum number of scroll attempts
        
        Returns:
            Dict[str, Any]: Result dictionary from scroll_infinite_loader
        
        Example:
            >>> result = scroll.load_infinite_content(max_scrolls=8)
            >>> print(f"Loaded {result['height_increase']}px new content")
        """
        return scroll_infinite_loader(self.driver, max_scrolls)

    def to_text(self, text: str, smooth: bool = True) -> bool:
        """
        Scroll to the first element containing specific text.
        
        Args:
            text (str): Text to search for
            smooth (bool): Use smooth scroll animation
        
        Returns:
            bool: True if found and scrolled to
        
        Example:
            >>> scroll.to_text("Subscribe")  # Scroll to "Subscribe" text
        """
        return scroll_to_text(self.driver, text, smooth)

    def spiral_to(self, y: int = 500) -> None:
        """
        Scroll with a spiral animation effect.
        
        Args:
            y (int): Target vertical position
        
        Example:
            >>> scroll.spiral_to(1000)  # Spiral scroll to 1000px
        """
        return scroll_animated_spiral(self.driver, y)

    def smart_scroll_to_bottom(self, max_attempts: int = 5) -> bool:
        """
        Smart scroll to bottom with content loading detection.
        
        Combines scrolling with detection of new content loading.
        Waits for content to stabilize before returning.
        
        Args:
            max_attempts (int): Maximum scroll attempts
        
        Returns:
            bool: True if successfully reached bottom
        
        Example:
            >>> if scroll.smart_scroll_to_bottom():
            ...     print("All content loaded")
        """
        initial_height = self.driver.execute_script('return document.documentElement.scrollHeight')
        attempts = 0
        
        while attempts < max_attempts:
            self.to_bottom()
            time.sleep(1.5)  # Wait for content to load
            current_height = self.driver.execute_script('return document.documentElement.scrollHeight')
            
            if current_height == initial_height:
                return True
            
            initial_height = current_height
            attempts += 1
        
        return False

    def get_element_position(self, selector: str) -> Dict[str, int]:
        """
        Get the position of an element on the page.
        
        Args:
            selector (str): Element selector
        
        Returns:
            Dict[str, int]: Dictionary with 'x' and 'y' coordinates
        
        Example:
            >>> pos = scroll.get_element_position("#header")
            >>> print(f"Header at: ({pos['x']}, {pos['y']})")
        """
        script = f'''
            var element = document.querySelector("{selector}");
            if (!element) return null;
            var rect = element.getBoundingClientRect();
            return {{
                x: rect.left + window.pageXOffset,
                y: rect.top + window.pageYOffset,
                width: rect.width,
                height: rect.height
            }};
        '''
        return self.driver.execute_script(script)

    def highlight_and_scroll(self, selector: str, duration: int = 2) -> bool:
        """
        Scroll to an element and highlight it temporarily.
        
        Finds the element, scrolls to it, and changes its background color
        for visual feedback. Useful for debugging or demonstrations.
        
        Args:
            selector (str): Element selector
            duration (int): Highlight duration in seconds (default: 2)
        
        Returns:
            bool: True if successful, False otherwise
        
        Example:
            >>> scroll.highlight_and_scroll("#submit-btn", duration=3)
        """
        script = f'''
            var element = document.querySelector("{selector}");
            if (!element) return false;
            
            element.scrollIntoView({{behavior: "smooth", block: "center"}});
            var originalBg = element.style.backgroundColor;
            element.style.backgroundColor = "#ffff00";
            element.style.transition = "background-color 0.3s";
            
            setTimeout(function() {{
                element.style.backgroundColor = originalBg;
            }}, {duration * 1000});
            
            return true;
        '''
        return self.driver.execute_script(script)

    def get_visible_elements(self, tag: str = '*') -> List[str]:
        """
        Get all visible elements in the current viewport.
        
        Returns a list of text content from elements currently visible.
        Useful for content verification or scraping.
        
        Args:
            tag (str): HTML tag to filter (default: '*' for all)
        
        Returns:
            List[str]: List of text content from visible elements
        
        Example:
            >>> visible = scroll.get_visible_elements('h2')
            >>> print(f"Visible headings: {visible}")
        """
        script = f'''
            var elements = document.getElementsByTagName('{tag}');
            var visible = [];
            var viewportHeight = window.innerHeight;
            
            for (var i = 0; i < elements.length; i++) {{
                var rect = elements[i].getBoundingClientRect();
                if (rect.top >= 0 && rect.bottom <= viewportHeight) {{
                    var text = elements[i].textContent.trim();
                    if (text) {{
                        visible.push(text);
                    }}
                }}
            }}
            
            return visible;
        '''
        return self.driver.execute_script(script)

    def get_current_position(self) -> Tuple[int, int]:
        """
        Get the current scroll position.
        
        Returns:
            Tuple[int, int]: (x, y) current scroll position
        
        Example:
            >>> x, y = scroll.get_current_position()
            >>> print(f"Scrolled to ({x}, {y})")
        """
        info = self.get_info()
        return (info.get('scrollX', 0), info.get('scrollY', 0))
    
    def is_element_visible(self, selector: str) -> bool:
        """
        Check if an element is visible in the viewport.
        
        Args:
            selector (str): Element selector
        
        Returns:
            bool: True if visible, False otherwise
        
        Example:
            >>> if scroll.is_element_visible("#footer"):
            ...     print("Footer is visible")
        """
        script = f'''
            var element = document.querySelector("{selector}");
            if(!element) return false;
            var rect = element.getBoundingClientRect();
            return rect.top >= 0 && rect.bottom <= window.innerHeight;
        '''
        return self.driver.execute_script(script)
    
    def reset(self) -> None:
        """
        Reset scroll position to the top of the page.
        
        Example:
            >>> scroll.reset()  # Go to top
        """
        self.to_top()
    
    def print_info(self) -> None:
        """
        Print scroll information for debugging.
        
        Displays comprehensive scroll state information in a formatted
        manner for debugging purposes.
        
        Example:
            >>> scroll.print_info()
            ==================================================
            Scroll Information:
              Position: (0, 450)
              Page Size: (1920, 3200)
              Viewport: (1920, 1080)
              Percentage: 14.06%
              At Bottom: False
              At Top: False
            ==================================================
        """
        info = self.get_info()
        print("=" * 50)
        print("Scroll Information:")
        print(f"  Position: ({info['scrollX']}, {info['scrollY']})")
        print(f"  Page Size: ({info['scrollWidth']}, {info['scrollHeight']})")
        print(f"  Viewport: ({info['clientWidth']}, {info['clientHeight']})")
        print(f"  Percentage: {info['percentageScrolled']}%")
        print(f"  At Bottom: {info['isAtBottom']}")
        print(f"  At Top: {info['isAtTop']}")
        print("=" * 50)
    
    def __repr__(self) -> str:
        """
        String representation of the ScrollManager object.
        
        Returns:
            str: String representation
        
        Example:
            >>> scroll
            ScrollManager(driver=WebDriver(...))
        """
        return f"ScrollManager(driver={self.driver})"

