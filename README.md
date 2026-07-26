# 📘 Complete Documentation for allykit Package

**allykit** is a versatile and powerful toolkit for Python developers that brings together a collection of essential tools in the fields of security, web interaction, system automation, and data processing, all within a unified and Pythonic interface.

---

## 🚀 Quick Start

### Installation

```bash
pip install allykit
```

**Note:** To use all features of the web module, install the following dependencies:

```bash
pip install selenium beautifulsoup4 requests tenacity psutil pyperclip
```

### First Example

```python
import allykit as ak

# Hashing a password
hashed = ak.hash_password("my_password", algorithm="sha256")

# Getting country information
iran_code = ak.COUNTRY_TO_CODE.get("Iran")  # 98

# Fetching web page content
soup = ak.soup_url("https://example.com")
print(soup.find_all("div"))
```

---

## 🏛️ Architecture & Structure

The allykit package consists of 6 main modules, each responsible for a specialized domain:

| Module | Path | Responsibility |
|--------|------|----------------|
| Security_kit | `allykit.Security_kit` | Cryptography, hashing, password generation, file security |
| web_kit | `allykit.web_kit` | HTTP requests, JS rendering, browser automation, cookies, caching, scroll management |
| data_kit | `allykit.data_kit` | Language data, country data, and geographic information |
| Automobile_kit | `allykit.Automobile_kit` | System automation, command line, Git, Python, filesystem |
| Tools_kit | `allykit.Tools_kit` | Basic file, JSON, and string utilities |
| core | `allykit` | Unified entry point and main configuration |

---

## 📦 Modules & Features

### 1. Security Module (`Security_kit`)

This module is the specialized core of allykit in the security domain.

#### `hash_kit.py` Submodule

- Data and file hashing: with algorithms `md5`, `sha1`, `sha224`, `sha256`, `sha384`, `sha512`, `sha3-*`, `blake2b`, `blake2s`
- Salted hashing: secure salt generation with `generate_salt`, hashing with `hash_with_salt`, and verification with `verify_password`
- Advanced security: `double_hash` for re-hashing
- Detection and comparison: automatic hash algorithm detection (`smart_hash_detector`) and hash comparison

```python
from allykit import hash_password, generate_salt, hash_with_salt, verify_password

# Simple hashing
hashed = hash_password("my_password", algorithm="sha256")

# Salted hashing
salt = generate_salt()
salted_hash = hash_with_salt("my_password", salt)
is_valid = verify_password("my_password", salted_hash, salt)
```

#### `password_kit` Submodule

- Strong password generation: `generate_password` and `generate_strong_password` functions
- Timed passwords: creating passwords with expiration dates using `generate_timed_password` and `generating_password`
- Timed password management: `Time_Password` class for validity checking, remaining time, and extracting the main password
- Security scoring: `Review_Password` class for checking security criteria and calculating entropy scores

```python
from allykit import generate_password, generate_strong_password, generate_timed_password, Time_Password, Review_Password

# Generate strong password
pwd = generate_strong_password(length=16)

# Timed password (valid for 24 hours)
timed_pwd = generate_timed_password(time='hours.24')
tp = Time_Password(timed_pwd)
print(f"Valid: {tp.is_password_valid()}")
print(f"Remaining: {tp.time_remaining()}")

# Check password strength
reviewer = Review_Password(pwd)
print(f"Entropy score: {reviewer.Entropy_Score_Password()}")
```

#### `file_kit.py` Submodule

- File hashing: `hash_file` with Salt capability for enhanced security
- Security snapshot: `create_snapshot` for taking a complete image of a folder's status
- Integrity verification: `verify_snapshot` for detecting changes (additions, deletions, content or permission changes)

```python
from allykit import hash_file, create_snapshot, verify_snapshot

# Hash a file
file_hash = hash_file("document.pdf", algorithm="sha256")

# Create a snapshot of a directory
snapshot = create_snapshot("./important_data")

# Later, verify the snapshot
is_clean = verify_snapshot("./important_data", snapshot)
if not is_clean:
    print("Changes detected in the directory!")
```

---

### 2. Web Module (`web_kit`)

This module provides comprehensive tools for web interaction.

#### Base Communications (`Communications.py`)

- `fetch_url`: GET request with automatic retry (up to 5 times)
- `execute_request`: GET/POST request with headers, proxy, and authentication
- `get_rate_limit_info`: Extracting rate limit information from response headers

```python
from allykit import fetch_url, execute_request, get_rate_limit_info

# Simple GET request with retry
response = fetch_url("https://api.example.com/data")

# Advanced request with headers and auth
response = execute_request(
    "https://api.example.com/data",
    method="POST",
    headers={"Content-Type": "application/json"},
    auth=("username", "password"),
    data={"key": "value"}
)

# Get rate limit info
rate_info = get_rate_limit_info(response)
print(f"Remaining requests: {rate_info.get('remaining')}")
```

#### Code Retrieval (`Get_Code.py`)

- `soup_url`: Fetching and converting a page to BeautifulSoup using requests
- `javascript`, `javascript_pro`: Fetching pages with full JavaScript rendering (Selenium) with advanced features like scrolling and script execution

```python
from allykit import soup_url, javascript, javascript_pro

# Simple BeautifulSoup fetch
soup = soup_url("https://example.com")
titles = soup.find_all("h1")

# JavaScript rendering with Selenium
html = javascript("https://example.com", wait_time=5)

# Advanced JavaScript rendering with scrolling
html = javascript_pro(
    "https://example.com",
    scroll_to_bottom=True,
    execute_script="document.querySelector('#load-more').click();"
)
```

#### Browser Automation (`CChrome.py`, `WebAutomation.py`)

- `chrome`: Launching a browser with advanced settings (incognito mode, proxy, User-Agent)
- `WebAutomation` class: Unified interface for clicking, typing, scrolling, hovering, and interacting with elements
- Cookie management (`Cookie.py`): Saving, loading, and clearing expired cookies

```python
from allykit import chrome, WebAutomation

# Launch browser
driver = chrome(incognito=True, headless=False)

# Create automation instance
auto = WebAutomation(driver)

# Navigate and interact
auto.open("https://example.com")
auto.click("#login-button")
auto.send_keys("#username", "myuser")
auto.send_keys("#password", "mypass")


# Cookie management
from allykit import Cookie

cookie = Cookie(driver, "cookies.pkl")

cookie.save_cookies()
cookie.load_cookies()
```

#### Scroll Management (`scroll_manager.py`) 🆕

A powerful and comprehensive scroll management system for Selenium WebDriver that handles all scrolling needs:

- Basic Scrolling: `window_scrollTo`, `window_scrollTo_bottom`, `window_scrollTo_top`, `window_scrollTo_right`
- Advanced Scrolling: `scroll_smooth_to`, `scroll_to_element`, `scroll_to_percentage`, `scroll_to_text`
- Infinite Scroll: `py_scroll` and `scroll_infinite_loader` for dynamic content loading
- Smart Detection: `get_scroll_info` for comprehensive scroll state information
- Visual Effects: `scroll_animated_spiral` for creative scrolling animations
- Element Management: `scroll_until_element_visible`, `highlight_and_scroll`, `get_element_position`
- `ScrollManager` Class: Unified interface with 20+ methods for all scroll operations

```python
from allykit import chrome, ScrollManager

# Launch browser
driver = chrome()
scroll = ScrollManager(driver)

# Navigate to a page
driver.get("https://example.com")

# Scroll to the bottom
scroll.to_bottom()

# Get scroll information
info = scroll.get_info()
print(f"Scrolled: {info['percentageScrolled']}%")

# Scroll to a specific element
scroll.to_element("#my-element", by="css")

# Load infinite scroll content
result = scroll.load_infinite_content(max_scrolls=5)
print(f"Loaded {result['height_increase']}px of new content")

# Highlight an element and scroll to it
scroll.highlight_and_scroll(".important-section", duration=3)

# Smart scroll to bottom with content detection
if scroll.smart_scroll_to_bottom():
    print("All content loaded successfully")

# Scroll smoothly to text
scroll.to_text("Important News!", smooth=True)

# Get element position
pos = scroll.get_element_position("#post-123")
print(f"Post at: ({pos['x']}, {pos['y']})")

# Reset to top
scroll.reset()

# Print debugging info
scroll.print_info()
```

#### Caching & Monitoring (`Elastic_bands.py`)

- `DiskCache` class: Disk-based caching with automatic expiration (TTL) for web requests
- `Monitoring` class: Monitoring web page changes and detecting changes in content, headers, and metadata

```python
from allykit import DiskCache, Monitoring

# Cache with 1-hour TTL
cache = DiskCache(ttl_hours=1)

# Fetch with caching
html = cache.fetch("https://example.com")
cached_html = cache.get("https://example.com")

# Monitor a page for changes
monitor = Monitoring("https://example.com", cache_dir="./cache")
if monitor.update_all():
    print("Page has been updated!")
```

#### Code Processing (`Working_with_code.py`)

- Data extraction: `extract_all_links`, `extract_images`, `extract_text_from_tags` functions
- `SoupToDict` class: Comparing two HTML pages and detecting line-by-line changes with JSON output

```python
from allykit import extract_all_links, extract_images, extract_text_from_tags, SoupToDict

# Extract data from BeautifulSoup
links = extract_all_links(soup)
images = extract_images(soup)
texts = extract_text_from_tags(soup, ["p", "h1", "h2"])

# Compare two HTML pages
comparator = SoupToDict(soup_old, soup_new)
changes = comparator.get_changes()
print(f"Found {len(changes)} changes")
```

---

### 3. Data Module (`data_kit`)

This module provides a rich data source.

- `Language.py`: Encyclopedia of characters from various languages (Latin, Cyrillic, Persian, Chinese, etc.) for text detection and processing
- `country.py`: Complete country information including calling codes (`CALLING_CODES`), ISO codes (`ISO_ALPHA2`), continent (`COUNTRY_CONTINENT`), official language (`COUNTRY_LANGUAGE`), and internet TLD (`COUNTRY_TLD`)
- `IRAN/`: Comprehensive data on Iranian provinces and cities (including phone codes, license plates, population, and mobile carrier detection)

```python
from allykit import (
    CALLING_CODES, ISO_ALPHA2, COUNTRY_CONTINENT,
    COUNTRY_LANGUAGE, COUNTRY_TLD, COUNTRY_TO_CODE
)

# Get country information
iran_code = COUNTRY_TO_CODE.get("Iran")  # 98
iran_iso = ISO_ALPHA2.get("Iran")  # "IR"
iran_continent = COUNTRY_CONTINENT.get("Iran")  # "Asia"

```

---

### 4. System Automation Module (`Automobile_kit`)

This module brings command-line power and system management to Python.

#### Process Management (`ProcessManager`)

- `ProcessManager` class and high-level functions: `kill_process`, `kill_chrome`, `kill_all_browsers`, `suspend_process`, `resume_process`
- Detailed process information retrieval (`get_process_info`), counting and checking process existence

```python
from allykit import (
    ProcessManager, kill_process, kill_chrome,
    suspend_process, resume_process, get_process_info
)

# Kill a specific process
kill_process("notepad.exe")

# Kill all Chrome processes
kill_chrome()

# Suspend and resume
suspend_process(1234)
resume_process(1234)

# Get process info
info = get_process_info(1234)
print(f"Name: {info['name']}, CPU: {info['cpu']}%")

# Process manager class
pm = ProcessManager(process_name = "chrome")
processes = pm.kill_all()
chrome_processes = pm.is_running()
```

#### Command Line (`Automobile/Cmd.py`, `powerShell.py`)

- `cmd` class: Executing CMD commands, opening windows, auto-typing commands
- `PowerShell` class: Executing PowerShell commands with Unicode support and special `size_file` function for calculating file/folder size

```python
from allykit import cmd, PowerShell

# CMD operations
cmd.cmd("dir")
cmd.open_cmd()
cmd.type_text("echo Hello World")

# PowerShell operations
ps = PowerShell()
result = ps.run("Get-Process")
file_size = ps.size_file("C:\\MyFolder")
```

#### Specialized Automation (`New_automobile/`)

- `git.py`: `Git` class for full Git automation (clone, init, add, commit, push, pull, branch, log)
- `python.py`: `Pip` (package management) and `Python` (script execution, venv creation, code execution) classes
- `file.py`: `File` class for cross-platform filesystem operations (create, delete, copy, move, rename)

```python
from allykit import Git, Pip, Python, File

# Git automation
git = Git()
git.clone("https://github.com/user/project.git")
git.add(".")
git.commit("Initial commit")
git.push()

# Python automation
py = Python()
py.create_venv("venv")
py.run_script("app.py")

# File operations
file = File()
file.copy_file("source.txt", "dest.txt")
file.move_file("old.txt", "new.txt")
file.delete_file("temp.txt")
```

---

### 5. General Utilities Module (`Tools_kit`)

This module provides a reusable foundation layer for other components.

- `file_tools.py`: Basic file functions (read, write, delete, get metadata, and permission management)
- `string_tools.py`: Secure random string generation (`str_choice_string`) and text processing utilities (truncate, format_thousands)
- `WorkFileJson.py`: `WorkFileJson` class for complete JSON file management with CRUD operations, search, merge, and file management

```python
from allykit import (
    read_file, write_file, remove_file,
    str_choice_string, truncate, format_thousands,
    WorkFileJson
)

# File operations
content = read_file("data.txt")
write_file("output.txt", "Hello World")

# String utilities
random_string = str_choice_string(length=10)
formatted = format_thousands(1234567)  # "1,234,567"

# JSON file management
json_file = WorkFileJson("data.json")
json_file.save({"name": "John", "age": 30})
json_file.update_dict({"name": "Jane"})
data = json_file.search_in_dict({"age": 30})
json_file.save()
```

---

## 💡 Advanced Examples

### 1. Full Deployment Pipeline Automation

```python
from allykit import Git, Pip, Python, File

# 1. Clone repository
git = Git()
git.clone("https://github.com/user/project.git")

# 2. Install dependencies
pip = Pip()
pip.pip_install_requirements("requirements.txt")

# 3. Run tests
py = Python()
test_output = py.run_script("run_tests.py")

# 4. Build package
py.run_module("build")

# 5. Archive results
file = File()
file.copy_file("logs/test_results.log", "archive/")
```

### 2. Building a Secure Web Monitoring Bot

```python
from allykit import DiskCache, Monitoring, SoupToDict, create_snapshot, verify_snapshot

# Cache with 1-hour TTL
cache = DiskCache(ttl_hours=1)

# Fetch target page
soup_old = cache.javascript("https://example.com/dashboard")

# Create security snapshot
snapshot = create_snapshot("./data")

# ... after some time ...
# Check for page changes
monitor = Monitoring("https://example.com/dashboard", "./cache")
if not monitor.update_all():
    # Fetch new page and perform detailed comparison
    soup_new = cache.javascript("https://example.com/dashboard")
    comparator = SoupToDict(soup_old, soup_new)
    changes = comparator.get_changes()
    
    # Verify file integrity
    if verify_snapshot("./data", snapshot):
        print("Website changes detected and file integrity verified.")
```

### 3. Enterprise Password Management

```python
from allykit import generate_timed_password, Time_Password, Review_Password

# Generate one-time password for user (24-hour validity)
temp_pwd = generate_timed_password(time='hours.24')
tp = Time_Password(temp_pwd)

# Check password security
reviewer = Review_Password(tp.get_password())
if reviewer.Entropy_Score_Password() < 8:
    print("Password is weak, regenerate!")
else:
    # Store password hash in database
    hashed_data = tp.to_dict(security=True)
    print(f"Password securely stored: {hashed_data['password']}")
```

### 4. Advanced Scroll Management for Web Automation 🆕

```python
from allykit import chrome, ScrollManager

# Launch browser
driver = chrome()

# Create scroll manager
scroll = ScrollManager(driver)

# Navigate to a page
driver.get("https://example.com")

# Scroll to the bottom
scroll.to_bottom()

# Get scroll information
info = scroll.get_info()
print(f"Scrolled: {info['percentageScrolled']}%")

# Scroll to a specific element
scroll.to_element("#my-element", by="css")

# Load infinite scroll content
result = scroll.load_infinite_content(max_scrolls=5)
print(f"Loaded {result['height_increase']}px of new content")

# Highlight an element and scroll to it
scroll.highlight_and_scroll(".important-section", duration=3)

# Smart scroll to bottom with content detection
if scroll.smart_scroll_to_bottom():
    print("All content loaded successfully")
```

### 5. Web Automation with Scroll Management

```python
from allykit import chrome, ScrollManager, WebAutomation
import time

# Setup
driver = chrome()
scroll = ScrollManager(driver)
automation = WebAutomation(driver)

# Navigate to social media feed
driver.get("https://social-media-site.com/feed")

# Load content with infinite scroll
for i in range(3):
    scroll.to_bottom()
    time.sleep(2)
    
    # Extract visible posts
    visible_text = scroll.get_visible_elements('div')
    print(f"Visible elements: {len(visible_text)}")

# Scroll to a specific post
scroll.to_text("Exciting news!", smooth=True)

# Get element position
pos = scroll.get_element_position("#post-123")
print(f"Post at position: ({pos['x']}, {pos['y']})")

# Reset to top
scroll.reset()

# Print debugging info
scroll.print_info()
```

---

## ⚙️ Configuration & Dependencies

### Core Dependencies (Required)

- Python >= 3.9
- `hashlib`, `os`, `pathlib`, `datetime`, `json`, `shutil`, `string`, `random`, `re`, `typing`, `subprocess`, `time`, `pickle` (all standard)
- `secrets` (standard)

### Optional Dependencies (For Specific Features)

- **Web:** `requests`, `beautifulsoup4`, `selenium`, `tenacity`, `deepdiff`
- **System Automation:** `psutil`, `pyautogui`, `pyperclip`

---

## 🤝 Contributing

The allykit package is developed as Open Source under the MIT license. For contributions, bug reports, or feature suggestions, please visit the main repository on GitHub.

---

## 📄 License

This package is released under the MIT License.

**Developed by:** allykit Development Team  
**Last Updated:** As of version 1.4.0

---

## 🤝 Corporate Sponsorship

allykit is a comprehensive toolkit that is already being used by individual developers and small teams. We are looking for corporate partners to help sustain and accelerate its development.

### Why Sponsor allykit?

- **Reduce Development Time:** Your team can save hundreds of development hours by leveraging allykit's pre-built modules for security, web automation, and system tasks.
- **Support Open Source:** Help maintain a high-quality, free tool that benefits the entire Python community.
- **Gain Visibility:** Your company logo and link will be prominently displayed in the project's README and documentation, reaching thousands of developers.
- **Feature Prioritization:** Sponsors at the corporate level can have a say in the roadmap and prioritization of new features.

### Contact Us

For corporate sponsorship inquiries, please contact us at:  
📧 **@Hossein_12_mm** (My Telegram ID)

---

> **One final point:** I am the sole creator of this module—it was built exclusively by me—so please beware of scams. ✔  
> **Thank you for your support.** 🙏💝