# 📘 Complete Documentation for `allykit` Package

**`allykit`** is a versatile and powerful toolkit for Python developers that brings together a collection of essential tools in the fields of security, web interaction, system automation, and data processing, all within a unified and Pythonic interface.

---

## 🚀 Quick Start

### Installation
```bash
pip install allykit
```

Note: To use all features of the web module, install the following dependencies:

```bash
pip install selenium beautifulsoup4 requests tenacity deepdiff
```

First Example

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

The `allykit` package consists of 6 main modules, each responsible for a specialized domain:

| Module | Path | Responsibility |
|--------|------|----------------|
| Security_kit | allykit.Security_kit | Cryptography, hashing, password generation, file security |
| web_kit | allykit.web_kit | HTTP requests, JS rendering, browser automation, cookies, caching |
| data_kit | allykit.data_kit | Language data, country data, and geographic information |
| Automobile_kit | allykit.Automobile_kit | System automation, command line, Git, Python, filesystem |
| Tools_kit | allykit.Tools_kit | Basic file, JSON, and string utilities |
| core | allykit | Unified entry point and main configuration |

---

## 📦 Modules & Features

### 1. Security Module (Security_kit)

This module is the specialized core of allykit in the security domain.

**hash_kit.py Submodule**

- Data and file hashing: with algorithms md5, sha1, sha224, sha256, sha384, sha512, sha3-*, blake2b, blake2s
- Salted hashing: secure salt generation with `generate_salt`, hashing with `hash_with_salt`, and verification with `verify_password`
- Advanced security: `double_hash` for re-hashing
- Detection and comparison: automatic hash algorithm detection (`smart_hash_detector`) and hash comparison

**password_kit Submodule**

- Strong password generation: `generate_password` and `generate_strong_password` functions
- Timed passwords: creating passwords with expiration dates using `generate_timed_password` and `generating_password`
- Timed password management: `Time_Password` class for validity checking, remaining time, and extracting the main password
- Security scoring: `Review_Password` class for checking security criteria and calculating entropy scores

**file_kit.py Submodule**

- File hashing: `hash_file` with Salt capability for enhanced security
- Security snapshot: `create_snapshot` for taking a complete image of a folder's status
- Integrity verification: `verify_snapshot` for detecting changes (additions, deletions, content or permission changes)

---

### 2. Web Module (web_kit)

This module provides comprehensive tools for web interaction.

**Base Communications (Communications.py)**

- `fetch_url`: GET request with automatic retry (up to 5 times)
- `execute_request`: GET/POST request with headers, proxy, and authentication
- `get_rate_limit_info`: Extracting rate limit information from response headers

**Code Retrieval (Get_Code.py)**

- `soup_url`: Fetching and converting a page to BeautifulSoup using requests
- `javascript`, `javascript_pro`: Fetching pages with full JavaScript rendering (Selenium) with advanced features like scrolling and script execution

**Browser Automation (CChrome.py, WebAutomation.py)**

- `chrome`: Launching a browser with advanced settings (incognito mode, proxy, User-Agent)
- `WebAutomation` class: Unified interface for clicking, typing, scrolling, hovering, and interacting with elements
- Cookie management (`Cookie.py`): Saving, loading, and clearing expired cookies

**Caching & Monitoring (Elastic_bands.py)**

- `DiskCache` class: Disk-based caching with automatic expiration (TTL) for web requests
- `Monitoring` class: Monitoring web page changes and detecting changes in content, headers, and metadata

**Code Processing (Working_with_code.py)**

- Data extraction: `extract_all_links`, `extract_images`, `extract_text_from_tags` functions
- `SoupToDict` class: Comparing two HTML pages and detecting line-by-line changes with JSON output

---

### 3. Data Module (data_kit)

This module provides a rich data source.

- `Language.py`: Encyclopedia of characters from various languages (Latin, Cyrillic, Persian, Chinese, etc.) for text detection and processing
- `country.py`: Complete country information including calling codes (`CALLING_CODES`), ISO codes (`ISO_ALPHA2`), continent (`COUNTRY_CONTINENT`), official language (`COUNTRY_LANGUAGE`), and internet TLD (`COUNTRY_TLD`)
- `IRAN/`: Comprehensive data on Iranian provinces and cities (including phone codes, license plates, population, and mobile carrier detection)

---

### 4. System Automation Module (Automobile_kit)

This module brings command-line power and system management to Python.

**Process Management (ProcessManager)**

- `ProcessManager` class and high-level functions: `kill_process`, `kill_chrome`, `kill_all_browsers`, `suspend_process`, `resume_process`
- Detailed process information retrieval (`get_process_info`), counting and checking process existence

**Command Line (Automobile/Cmd.py, powerShell.py)**

- `cmd` class: Executing CMD commands, opening windows, auto-typing commands
- `PowerShell` class: Executing PowerShell commands with Unicode support and special `size_file` function for calculating file/folder size

**Specialized Automation (New_automobile/)**

- `git.py`: `Git` class for full Git automation (clone, init, add, commit, push, pull, branch, log)
- `python.py`: `Pip` (package management) and `Python` (script execution, venv creation, code execution) classes
- `file.py`: `File` class for cross-platform filesystem operations (create, delete, copy, move, rename)

---

### 5. General Utilities Module (Tools_kit)

This module provides a reusable foundation layer for other components.

- `file_tools.py`: Basic file functions (read, write, delete, get metadata, and permission management)
- `string_tools.py`: Secure random string generation (`str_choice_string`) and text processing utilities (truncate, format_thousands)
- `WorkFileJson.py`: `WorkFileJson` class for complete JSON file management with CRUD operations, search, merge, and file management

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

---

## ⚙️ Configuration & Dependencies

**Core Dependencies (Required)**

- Python >= 3.9
- hashlib, os, pathlib, datetime, json, shutil, string, random, re, typing, subprocess, time, pickle (all standard)
- secrets (standard)

**Optional Dependencies (For Specific Features)**

- Web: requests, beautifulsoup4, selenium, tenacity, deepdiff
- System Automation: psutil, pyautogui, pyperclip

---

## 🤝 Contributing

The `allykit` package is developed as Open Source under the MIT license. For contributions, bug reports, or feature suggestions, please visit the main repository on GitHub.

---

## 📄 License

This package is released under the MIT License.

---

**Developed by:** allykit Development Team  
**Last Updated:** As of version 1.3.0