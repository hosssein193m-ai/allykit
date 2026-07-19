
from allykit.web_kit import fix_url
from allykit.web_kit.CChrome import chrome, browser_context , wait_for_element , get_headless_driver
from allykit.web_kit.Communications import fetch_url , execute_request , validate_links, get_rate_limit_info ,is_link_alive 
from allykit.web_kit.Elastic_bands import Monitoring , DiskCache
from allykit.web_kit.Get_Code import soup_url, javascript, javascript_driver , javascript_pro
from allykit.web_kit.WebAutomation import WebAutomation, By
from allykit.web_kit.Working_with_code import extract_all_links, extract_images, extract_text_from_tags, save_links ,save_link , SoupToDict, extract_structured_data


import os
import tempfile
import json
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


# ============================================
# PART 1: URL NORMALIZATION & VALIDATION
# ============================================
print("=" * 70)
print("PART 1: URL NORMALIZATION & VALIDATION")
print("=" * 70)

# 1.1 Basic URL fix
print("\n--- 1.1 Fix URL ---")
urls = [
    "Example.COM//API//Users",
    "www.google.com",
    "localhost:8000",
    "https://SITE.com/Path//With//Slashes"
]

for raw_url in urls:
    fixed = fix_url(raw_url)
    print(f"Raw: {raw_url:30} -> Fixed: {fixed}")

# 1.2 Force HTTP (for local development)
print("\n--- 1.2 Force HTTP ---")
http_url = fix_url("localhost:8000/api", HTTP=False)
print(f"Force HTTP: {http_url}")

# 1.3 Remove URL fragments
print("\n--- 1.3 Remove Fragments ---")
with_fragment = fix_url("https://example.com/page#section", remove_fragment=True)
print(f"Without fragment: {with_fragment}")

# 1.4 Test URL availability
print("\n--- 1.4 Test URL Availability ---")
test_url = "https://google.com"
is_available = fix_url(test_url, test=True)
print(f"Is {test_url} available? {is_available}")

# 1.5 Invalid URL handling
print("\n--- 1.5 Invalid URL ---")
try:
    invalid = fix_url("")
except ValueError as e:
    print(f"Error: {e}")


# ============================================
# PART 2: HTTP COMMUNICATIONS
# ============================================
print("\n" + "=" * 70)
print("PART 2: HTTP COMMUNICATIONS")
print("=" * 70)

# 2.1 Basic fetch with retry
print("\n--- 2.1 Fetch URL (with retry) ---")
try:
    response = fetch_url("https://httpbin.org/get")
    print(f"Status: {response.status_code}")
    print(f"Content length: {len(response.text)} chars")
except Exception as e:
    print(f"Error: {e}")

# 2.2 Execute request (GET/POST)
print("\n--- 2.2 Execute Request ---")
# GET request
get_response = execute_request("https://httpbin.org/get", method="GET")
print(f"GET status: {get_response.status_code}")

# POST request with data
post_response = execute_request(
    "https://httpbin.org/post",
    method="POST",
    data={"key": "value", "name": "AllyKit"}
)
print(f"POST status: {post_response.status_code}")

# 2.3 Validate links (filter working URLs)
print("\n--- 2.3 Validate Links ---")
test_links = [
    "https://google.com",
    "https://invalid-domain-12345.com",
    "https://github.com"
]
valid = validate_links(test_links, timeout=3)
print(f"Valid links: {valid}")

# 2.4 Check if link is alive
print("\n--- 2.4 Link Alive Check ---")
alive = is_link_alive("https://google.com")
print(f"Is google.com alive? {alive}")

# 2.5 Rate limit information
print("\n--- 2.5 Rate Limit Info ---")
try:
    rate_info = get_rate_limit_info("https://api.github.com/users/octocat")
    print(f"Rate limit info:")
    for key, value in rate_info.items():
        print(f"  - {key}: {value}")
except Exception as e:
    print(f"Rate limit not available: {e}")


# ============================================
# PART 3: HTML PARSING & EXTRACTION
# ============================================
print("\n" + "=" * 70)
print("PART 3: HTML PARSING & EXTRACTION")
print("=" * 70)

# 3.1 Fetch and parse HTML
print("\n--- 3.1 Soup URL ---")
soup = soup_url("https://example.com")
print(f"Page title: {soup.title.string if soup.title else 'N/A'}")
print(f"Found {len(soup.find_all('p'))} paragraphs")

# 3.2 Extract text from specific tags
print("\n--- 3.2 Extract Text from Tags ---")
paragraphs = extract_text_from_tags(soup, "p")
print(f"First paragraph: {paragraphs[0][:50]}..." if paragraphs else "No paragraphs")

# 3.3 Extract all links
print("\n--- 3.3 Extract All Links ---")
links = extract_all_links(soup, base_url="https://example.com")
print(f"Found {len(links)} links")
for link in links[:3]:
    print(f"  - {link}")

# 3.4 Extract images
print("\n--- 3.4 Extract Images ---")
images = extract_images(soup, base_url="https://example.com")
print(f"Found {len(images)} images")
for img in images[:3]:
    print(f"  - {img}")

# 3.5 Extract structured data (JSON-LD)
print("\n--- 3.5 Extract Structured Data ---")
structured = extract_structured_data(soup)
if structured:
    print(f"Found JSON-LD data: {json.dumps(structured, indent=2)[:200]}...")
else:
    print("No structured data found")

# 3.6 HTML Comparison (SoupToDict)
print("\n--- 3.6 HTML Comparison ---")
html1 = "<html><body><h1>Hello</h1><p>World</p></body></html>"
html2 = "<html><body><h1>Hello</h1><p>Changed</p></body></html>"
soup1 = BeautifulSoup(html1, "html.parser")
soup2 = BeautifulSoup(html2, "html.parser")

comparator = SoupToDict(soup1, soup2)
changes = comparator.get_changes()

print(f"Changes detected:")
print(f"  - Added: {changes['summary']['added']}")
print(f"  - Removed: {changes['summary']['removed']}")
print(f"  - Unchanged: {changes['summary']['unchanged']}")
print(f"  - Total changes: {changes['summary']['total_changes']}")

# Check specific element
status = comparator.has_item_changed("<p>World</p>")
print(f"Element '<p>World</p>' status: {status}")

# Export to JSON
json_output = comparator.to_json(indent=2)
print(f"JSON output (first 200 chars): {json_output[:200]}...")


# ============================================
# PART 4: JAVASCRIPT RENDERING
# ============================================
print("\n" + "=" * 70)
print("PART 4: JAVASCRIPT RENDERING")
print("=" * 70)

# 4.1 Basic JavaScript rendering (simple)
print("\n--- 4.1 Basic JavaScript ---")
try:
    js_soup = javascript("https://example.com")
    print(f"JS rendered title: {js_soup.title.string if js_soup.title else 'N/A'}")
except Exception as e:
    print(f"JavaScript rendering failed (may need Chrome): {e}")

# 4.2 Advanced JavaScript rendering (with options)
print("\n--- 4.2 Advanced JavaScript (pro) ---")
try:
    pro_soup = javascript_pro(
        url="https://example.com",
        wait_for_load=True,
        timeout=10,
        scroll_to_bottom=False,
        headless=True,
        viewport_size=(1920, 1080)
    )
    print(f"Pro rendering successful: {len(pro_soup.text)} chars")
except Exception as e:
    print(f"Pro rendering failed: {e}")

# 4.3 JavaScript with custom scripts and element waiting
print("\n--- 4.3 JavaScript with Custom Scripts ---")
try:
    from selenium.webdriver.common.by import By
    
    custom_soup = javascript_pro(
        url="https://example.com",
        wait_for_element=(By.TAG_NAME, "h1"),
        custom_scripts=[
            "document.querySelector('h1').style.color = 'red';"
        ],
        headless=True,
        scroll_to_bottom=True
    )
    print(f"Custom script executed successfully")
except Exception as e:
    print(f"Custom script failed: {e}")


# ============================================
# PART 5: DISK CACHE SYSTEM
# ============================================
print("\n" + "=" * 70)
print("PART 5: DISK CACHE SYSTEM")
print("=" * 70)

# 5.1 Initialize cache
print("\n--- 5.1 Initialize Cache ---")
cache_dir = tempfile.mkdtemp(prefix="allykit_cache_")
cache = DiskCache(cache_dir=cache_dir, ttl_hours=24)
print(f"Cache directory: {cache_dir}")
print(f"TTL: {cache.ttl}")


# 5.2 Cache HTML content
print("\n--- 5.2 Cache HTML ---")
cached_soup = cache.html("https://example.com")
print(f"Cached HTML title: {cached_soup.title.string}")
print(f"Cache file: {cache.create_filename('https://example.com', 'html')}")

# 5.3 Cache JavaScript content
print("\n--- 5.3 Cache JavaScript ---")
try:
    js_cached = cache.javascript("https://example.com")
    print(f"Cached JS content length: {len(js_cached.text)} chars")
except Exception as e:
    print(f"JS cache failed: {e}")

# 5.4 Cache advanced JavaScript
print("\n--- 5.4 Cache Advanced JavaScript ---")
try:
    pro_cached = cache.javascript_pro(
        "https://example.com",
        scroll_to_bottom=True,
        headless=True
    )
    print(f"Cached Pro content length: {len(pro_cached.text)} chars")
except Exception as e:
    print(f"Pro cache failed: {e}")

# 5.5 Cache statistics
print("\n--- 5.5 Cache Statistics ---")
files = os.listdir(cache_dir)
print(f"Cache files: {len(files)}")
for f in files:
    print(f"  - {f}")

# 5.6 Clear expired cache
print("\n--- 5.6 Clear Expired ---")
removed = cache.clear_expired()
print(f"Removed {removed} expired files")

# 5.7 Clear all cache
print("\n--- 5.7 Clear All ---")
cache.clear_all()
print(f"All cache files cleared")


# ============================================
# PART 6: WEB AUTOMATION (Selenium Wrapper)
# ============================================
print("\n" + "=" * 70)
print("PART 6: WEB AUTOMATION")
print("=" * 70)

# 6.1 Initialize WebAutomation
print("\n--- 6.1 Initialize Automation ---")
try:
    automation = WebAutomation(timeout=10)
    print("WebAutomation initialized successfully")
    
    # 6.2 Open URL
    print("\n--- 6.2 Open URL ---")
    automation.open("https://example.com")
    print(f"Current URL: {automation.driver.current_url}")
    
    # 6.3 Find element
    print("\n--- 6.3 Find Element ---")
    from selenium.webdriver.common.by import By
    h1_element = automation.find((By.TAG_NAME, "h1"))
    print(f"Found element: {h1_element.text}")
    
    # 6.4 Get text
    print("\n--- 6.4 Get Text ---")
    text = automation.get_text((By.TAG_NAME, "h1"))
    print(f"Text: {text}")
    
    # 6.5 Get attribute
    print("\n--- 6.5 Get Attribute ---")
    href = automation.get_attribute((By.TAG_NAME, "a"), "href")
    print(f"First link href: {href}")
    
    # 6.6 Check visibility
    print("\n--- 6.6 Check Visibility ---")
    visible = automation.is_visible((By.TAG_NAME, "h1"))
    print(f"H1 visible? {visible}")
    
    # 6.7 Screenshot
    print("\n--- 6.7 Screenshot ---")
    screenshot_path = os.path.join(tempfile.gettempdir(), "allykit_screenshot.png")
    automation.screenshot(screenshot_path)
    print(f"Screenshot saved: {screenshot_path}")
    
    # 6.8 Quit browser
    print("\n--- 6.8 Quit ---")
    automation.quit()
    print("Browser closed")
    
except Exception as e:
    print(f"Automation test failed (may need ChromeDriver): {e}")


# ============================================
# PART 7: CHROME BROWSER MANAGEMENT
# ============================================
print("\n" + "=" * 70)
print("PART 7: CHROME BROWSER MANAGEMENT")
print("=" * 70)

# 7.1 Headless driver
print("\n--- 7.1 Headless Driver ---")
try:
    headless_driver = get_headless_driver()
    headless_driver.get("https://example.com")
    print(f"Headless page title: {headless_driver.title}")
    headless_driver.quit()
except Exception as e:
    print(f"Headless driver failed: {e}")

# 7.2 Custom Chrome configuration
print("\n--- 7.2 Custom Chrome ---")
try:
    custom_driver = chrome(
        criterion=False,  # Not headless
        proxy=None,
        user_agent="Mozilla/5.0 (Custom) Chrome/120.0",
        incognito=True,
        lang="en-US",
        disable_images=True,
        disable=True
    )
    custom_driver.get("https://example.com")
    print(f"Custom Chrome title: {custom_driver.title}")
    custom_driver.quit()
except Exception as e:
    print(f"Custom Chrome failed: {e}")

# 7.3 Browser context manager
print("\n--- 7.3 Browser Context ---")
try:
    with browser_context(headless=True) as driver:
        driver.get("https://example.com")
        print(f"Context title: {driver.title}")
    print("Browser auto-closed via context manager")
except Exception as e:
    print(f"Context manager failed: {e}")


# ============================================
# PART 8: FILE DOWNLOADS
# ============================================
print("\n" + "=" * 70)
print("PART 8: FILE DOWNLOADS")
print("=" * 70)

# 8.1 Download single file
print("\n--- 8.1 Save Single Link ---")
download_file = os.path.join(tempfile.gettempdir(), "allykit_download.txt")
try:
    success = save_link(
        "https://raw.githubusercontent.com/hosssein193m-ai/allykit/main/README.md",
        download_file
    )
    if success:
        print(f"Downloaded to: {download_file}")
        print(f"File size: {os.path.getsize(download_file)} bytes")
        os.remove(download_file)
    else:
        print("Download failed")
except Exception as e:
    print(f"Download error: {e}")

# 8.2 Download multiple files
print("\n--- 8.2 Save Multiple Links ---")
multi_files = [
    "https://raw.githubusercontent.com/hosssein193m-ai/allykit/main/requirements.txt",
    "https://raw.githubusercontent.com/hosssein193m-ai/allykit/main/setup.py"
]
try:
    base_name = os.path.join(tempfile.gettempdir(), "allykit_multi_")
    all_success = save_links(multi_files, base_name, add=4)
    print(f"All downloads successful? {all_success}")
    
    # Cleanup
    for f in os.listdir(tempfile.gettempdir()):
        if f.startswith("allykit_multi_"):
            os.remove(os.path.join(tempfile.gettempdir(), f))
    print("Cleanup complete")
except Exception as e:
    print(f"Multi-download error: {e}")

# ============================================
# PART 9: MONITORING CLASS DEMONSTRATION
# ============================================
print("\n" + "=" * 70)
print("PART 9: MONITORING CLASS - ADVANCED WEB MONITORING")
print("=" * 70)

# ============================================
# 9.1 Basic Initialization & Setup
# ============================================
print("\n--- 9.1 Initialization ---")

# Create a temporary cache directory
monitor_cache_dir = tempfile.mkdtemp(prefix="monitoring_cache_")
print(f"Cache directory: {monitor_cache_dir}")

# Initialize monitoring for a test URL
test_url = "https://httpbin.org/html"  # A page that changes
monitor = Monitoring(test_url, cache_dir=monitor_cache_dir)
print(f"✅ Monitoring initialized for: {test_url}")
print(f"   Cache path: {monitor.cache_dir}")

# ============================================
# 9.2 Data Extraction (data() method)
# ============================================
print("\n--- 9.2 Data Extraction ---")

# Get all data
all_data = monitor.data()
print(f"All data keys: {list(all_data.keys())}")
print(f"  - Status code: {all_data['Short-form content']['status_code']}")
print(f"  - Content length: {len(all_data['text'])} chars")

# Get specific items
html_content = monitor.data("text")
print(f"  - HTML length: {len(html_content)} chars")

headers = monitor.data("headers")
print(f"  - Content-Type: {headers.get('content-type', 'N/A')}")

metadata = monitor.data("Short-form content")
print(f"  - Encoding: {metadata.get('encoding', 'N/A')}")
print(f"  - Elapsed: {metadata.get('elapsed', 'N/A')}")

# ============================================
# 9.3 Caching Data (set_all(), set())
# ============================================
print("\n--- 9.3 Caching Data ---")

# Cache all data
monitor.set_all()
print("✅ All data cached")

# Cache specific items with custom names
monitor.set("text", "page_content")
print("✅ HTML cached as 'page_content.html'")

monitor.set("headers", "response_headers")
print("✅ Headers cached as 'response_headers.json'")

# Get cache info
cache_info = monitor.get_cache_info()
print(f"Cache files: {cache_info['file_count']}")
for file in cache_info['files']:
    print(f"  - {file}")

# ============================================
# 9.4 Loading Cached Data (load() method)
# ============================================
print("\n--- 9.4 Loading Cached Data ---")

# Load JSON data
cached_headers = monitor.load("headers")
print(f"Loaded headers: {list(cached_headers.keys())[:3]}...")

# Load HTML data
cached_html = monitor.load("text", "html")
print(f"Loaded HTML length: {len(cached_html)} chars")

# Load custom named file
custom_headers = monitor.load("response_headers")
print(f"Custom headers loaded: {custom_headers.get('content-type', 'N/A')}")

# ============================================
# 9.5 Change Detection (status(), update_all())
# ============================================
print("\n--- 9.5 Change Detection ---")

# First, let's check the current status
status = monitor.status()
print("Initial status comparison:")
for component, is_same in status.items():
    status_text = "✅ Same" if is_same else "🔄 Changed"
    print(f"  - {component}: {status_text}")

# Perform update check
if monitor.update_all():
    print("✅ No changes detected - cache is up to date")
else:
    print("🔄 Changes detected - cache updated")

# Get detailed status after update
status_after = monitor.status()
print("\nStatus after update:")
for component, is_same in status_after.items():
    status_text = "✅ Same" if is_same else "🔄 Changed"
    print(f"  - {component}: {status_text}")

# ============================================
# 9.6 Selective Cache Updates (update())
# ============================================
print("\n--- 9.6 Selective Cache Updates ---")

# Force some changes by making a second request with different data
# (Simulate changes by creating a new monitor instance)
monitor2 = Monitoring(test_url, cache_dir=monitor_cache_dir)

# Perform selective update
print("Performing selective update...")
monitor2.update()

# Check what was updated
cache_info_after = monitor2.get_cache_info()
print(f"Cache files after selective update: {cache_info_after['file_count']}")

# ============================================
# 9.7 Search Functionality (search() method)
# ============================================
print("\n--- 9.7 Search Functionality ---")

# Search for nested data
status_code = monitor.search("Short-form content.status_code")
print(f"Status code: {status_code}")

connection_info = monitor.search("Short-form content.connection")
print(f"Connection: {connection_info}")

# Search for top-level data
html_search = monitor.search("text")
print(f"HTML found: {len(html_search)} chars")

# Search for non-existent data
missing = monitor.search("nonexistent.key")
print(f"Non-existent search: {missing}")

# ============================================
# 9.8 Cache Management
# ============================================
print("\n--- 9.8 Cache Management ---")

# Check if files are cached
print(f"Is 'headers' cached? {monitor.is_cached('headers')}")
print(f"Is 'text' cached? {monitor.is_cached('text', 'html')}")
print(f"Is 'nonexistent' cached? {monitor.is_cached('nonexistent')}")

# Get cache age
age = monitor.get_cache_age("headers")
if age is not None:
    print(f"Headers cache age: {age:.2f} seconds")

age_html = monitor.get_cache_age("text", "html")
if age_html is not None:
    print(f"HTML cache age: {age_html:.2f} seconds")

# Get detailed cache info
info = monitor.get_cache_info()
print(f"\nDetailed cache information:")
print(f"  - Directory: {info['cache_dir']}")
print(f"  - File count: {info['file_count']}")
print(f"  - Total size: {info['total_size']} bytes ({info['total_size']/1024:.2f} KB)")
print(f"  - Files: {', '.join(info['files'])}")

# ============================================
# 9.9 Cache Removal Operations
# ============================================
print("\n--- 9.9 Cache Removal Operations ---")

# Remove specific file
monitor.remove_name("text.html")
print("Removed text.html")

# Check after removal
info_after_remove = monitor.get_cache_info()
print(f"Files after removal: {info_after_remove['file_count']}")

# Remove all files (keep directory)
monitor.remove()
print("Removed all cache files")

info_after_remove_all = monitor.get_cache_info()
print(f"Files after remove(): {info_after_remove_all['file_count']}")

# ============================================
# 9.10 Complete Refresh
# ============================================
print("\n--- 9.10 Complete Refresh ---")

# Cache some data again
monitor.set_all()
print("Data re-cached")

# Force a complete refresh
print("Forcing refresh...")
monitor.refresh()
print("Refresh complete")

info_after_refresh = monitor.get_cache_info()
print(f"Files after refresh: {info_after_refresh['file_count']}")

# ============================================
# 9.11 Context Manager Usage
# ============================================
print("\n--- 9.11 Context Manager Usage ---")

# Use with statement for automatic updates
with Monitoring(test_url, cache_dir=monitor_cache_dir) as auto_monitor:
    print(f"Inside context manager: {auto_monitor.url}")
    auto_monitor.set_all()
    print("Data cached inside context")
    # Auto-update on exit (if no errors)

print("Context manager exited - cache updated")

# ============================================
# 9.12 Advanced Usage Examples
# ============================================
print("\n--- 9.12 Advanced Usage ---")

# Example: Monitor multiple URLs
print("Monitoring multiple URLs:")
urls_to_monitor = [
    "https://httpbin.org/html",
    "https://httpbin.org/status/200",
    "https://example.com"
]

monitors = {}
for url in urls_to_monitor:
    try:
        m = Monitoring(url, cache_dir=monitor_cache_dir)
        m.set_all()
        monitors[url] = m
        print(f"  ✅ {url} - monitored")
    except Exception as e:
        print(f"  ❌ {url} - failed: {e}")

# Example: Periodic monitoring simulation
print("\nSimulating periodic monitoring:")
for i in range(2):
    print(f"\nCheck #{i+1}")
    for url, m in monitors.items():
        try:
            if m.update_all():
                print(f"  - {url}: No changes")
            else:
                print(f"  - {url}: 🔄 UPDATED")
        except Exception as e:
            print(f"  - {url}: Error - {e}")

# ============================================
# 9.13 Error Handling Examples
# ============================================
print("\n--- 9.13 Error Handling ---")

# Invalid URL
try:
    invalid_monitor = Monitoring("not-a-url", cache_dir=monitor_cache_dir)
except Exception as e:
    print(f"✅ Caught invalid URL error: {type(e).__name__}")

# Loading non-existent cache
try:
    monitor.load("nonexistent_file")
except FileNotFoundError as e:
    print(f"✅ Caught missing file error: {e}")

# Removing non-existent file
try:
    monitor.remove_name("non_existent.html")
except FileNotFoundError as e:
    print(f"✅ Caught file not found error: {e}")

# Searching for invalid data
result = monitor.search("invalid.key.that.does.not.exist")
print(f"Invalid search returns: {result}")

# ============================================
# 9.14 String Representation
# ============================================
print("\n--- 9.14 String Representation ---")

print(f"repr(): {repr(monitor)}")
print(f"str(): {str(monitor)}")

# ============================================
# 9.15 Complete Cache Cleanup
# ============================================
print("\n--- 9.15 Complete Cleanup ---")

# Remove all cache data
monitor.remove_all()
print("All cache removed (including directory)")

# Verify directory is gone
if os.path.exists(monitor.cache_dir):
    print("⚠️ Cache directory still exists")
else:
    print("✅ Cache directory removed successfully")


# ============================================
# PART 10: UTILITY ALIASES & QUICK REFERENCE
# ============================================
print("\n" + "=" * 70)
print("PART 9: UTILITY ALIASES")
print("=" * 70)

# 9.1 Alias demonstrations
print("\n--- 9.1 Using Aliases ---")
print("Available aliases:")
aliases = [
    "EI = extract_images",
    "EAL = extract_all_links", 
    "VL = validate_links",
    "ILA = is_link_alive",
    "ETFT = extract_text_from_tags",
    "ER = execute_request",
    "NOC = chrome",
    "ec = expected_conditions",
    "ESD = extract_structured_data",
    "JP = javascript_pro",
    "JD = javascript_driver"
]

for alias in aliases:
    print(f"  - {alias}")



# ============================================
# CLEANUP
# ============================================
print("\n" + "=" * 70)
print("CLEANUP")
print("=" * 70)

# Remove cache directory
try:
    import shutil
    shutil.rmtree(cache_dir)
    print(f"Removed cache directory: {cache_dir}")
except Exception as e:
    print(f"Cleanup error: {e}")

print("\n" + "=" * 70)
print("✅ ALL DEMONSTRATIONS COMPLETED SUCCESSFULLY!")
print("=" * 70)