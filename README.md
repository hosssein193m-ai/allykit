# allykit Library Documentation (Full & Updated Version)

The `allykit` library is a comprehensive toolkit designed for security engineers, backend developers, DevOps engineers, system administrators, and digital forensics specialists. It integrates advanced cryptographic operations, automated web interaction, intelligent filesystem auditing, command-line automation, robust password management, language and geographic data, and cookie management into a unified framework.
In this version, the data kit has been significantly updated for your use.

**Important Note**: Versions prior to 1.1.0 do not meet our standards, so please use the newer versions and enjoy.

---

## Modules Overview

### 1. Password Generation & Security Kit (Security Kit)

A high-level suite for managing credentials. It supports the generation of complex, randomized strings and time-sensitive passwords with expiration logic.

**Core Capabilities**:
- Customizable password generation (length, character constraints, prefixes/suffixes)
- Time-based validity (GTP/WPWT)
- Granular security auditing (Complexity Scoring and validation engines)
- **`Time_Password` class** for complete time-based password management
- **`Review_Password` class** for password validation and scoring
- Secure hashing, integrity verification, and authentication utilities

**Usage Examples**:
- Basic and strong password generation
- Password generation with prefix/suffix
- Time-limited password generation (with `generating_password` function)
- Password complexity validation (character checks, length, repetition)
- Entropy scoring (strength evaluation)
- Hashing with various algorithms (SHA256, SHA512, SHA3, BLAKE2)
- Salted hashing (for secure storage)
- Double hashing (Hash-in-Hash) for increased difficulty
- Hash algorithm detection
- Hash comparison
- **Professional time-based password management with `Time_Password` class** (expiry check, remaining time, full status report)

**Use Cases**: Automated credential management, secure token generation, password auditing, integrity verification, security strength evaluation, and one-time password authentication systems.

---

### 2. Web Kit & Scrapers (Web Kit)

A specialized module for seamless web interaction, data extraction, cookie management, and web monitoring.

**Core Capabilities**:
- **Web Interaction**: Advanced HTML fetching (mimicking real browsers to bypass detection), DOM traversal via BeautifulSoup integration, Selenium automation, intelligent HTTP requests, and memory-efficient streaming for large remote file downloads.
- **Cookie Management**: Saving, loading, managing expired cookies, switching between cookie files, and integration with WebAutomation.
- **Caching**: Disk-based caching with TTL support for HTML and JavaScript content.
- **Web Monitoring**: Change detection, data caching, and monitoring of web pages.

**Usage Examples**:
- URL normalization and validation
- HTTP requests with retry logic
- Extracting links, images, and text from HTML
- JavaScript rendering with headless browsers
- Web automation (form filling, clicking, screenshots)
- Single and bulk file downloads
- HTML comparison and change detection
- Cookie management (save, load, clear expired)
- Caching web pages for reuse
- Monitoring web page changes

**Use Cases**: Web scraping, data mining, automated browser interaction, website analysis, media/asset acquisition, user session management, and website change monitoring.

---

### 3. Cryptographic Hashing & Integrity Verification

A robust cryptographic engine providing multi-algorithm support and advanced protection mechanisms.

**Core Capabilities**: Support for the SHA family (SHA-1 through SHAKE-256), intelligent hash detection, Salt management to prevent rainbow table attacks, "Hash-in-Hash" (HH) double-hashing for increased computational difficulty, and integrity verification.

**Usage Examples**:
- String and file hashing
- Salt generation
- Salted hashing and password verification
- Automatic hash algorithm detection

**Use Cases**: Digital forensics (DFIR), data integrity verification, secure authentication, password protection, and digital evidence validation.

---

### 4. Filesystem Management & Metadata Mapping (Security Kit - File)

An advanced exploration engine for deep filesystem analysis and auditing.

**Core Capabilities**: Recursive directory crawling, hierarchical metadata mapping (size, ownership, timestamps), structured filesystem inventory generation, metadata extraction, and filesystem auditing.

**New Security Features**:
- **Create Snapshot** (`create_snapshot`): Capture a complete image of file system state for later use.
- **Verify Snapshot** (`verify_snapshot`): Compare current state with previous snapshot to detect changes, new files, or deletions.
- **Security Mapping** (`dict_files_in_directory`, `map_directory_metadata`)

**Usage Examples**:
- Taking a snapshot of a project folder to detect future changes
- Getting detailed file statistics and information
- Mapping complete directory metadata (recursively)
- Generating file dictionaries with hashes
- Saving dictionaries to JSON files
- Retrieving file permission strings
- Bulk file deletion

**Use Cases**: Digital forensics (DFIR), system auditing, integrity-based backup solutions, file analysis, and filesystem inspection.

---

### 5. Language & Geography Data (Data Kit)

A comprehensive dataset for language detection, country information, and Iranian geographic data.

**Core Capabilities**:
- **Language**: Language detection, filtering by language, digit normalization, RTL character detection, character classification, and ASCII approximation (transliteration).
- **Countries**: Complete country information (calling codes, ISO codes, capitals, currencies, continents), country search, and phone number formatting.
- **Iran**: Province and city information (coordinates, population, phone codes, car plate codes), SIM card operator detection, city search, and region-based province lookup.

**Usage Examples**:
- Detecting the language of a text (Persian, English, Arabic, ...)
- Filtering Persian characters from a text
- Normalizing digits (converting Persian digits to ASCII)
- Getting complete information for a country (calling code, capital, currency)
- Searching for countries by name
- Getting the province and full information for an Iranian city
- Detecting the SIM card operator based on the prefix
- Getting the phone code and car plate code for a city

**Use Cases**: Internationalization (i18n), localization (l10n), phone number validation, text analysis, Geographic Information Systems (GIS), and location-based applications.

---

### 6. Core Automation Toolkit (Automobile Kit)

A unified automation layer for developers and system administrators that simplifies interaction with the operating system, terminal, Git, Python, package management, PowerShell, filesystem utilities, and process management.

**Core Capabilities**:
- **CMD**: Execute Command Prompt commands with timeout and multiple command support.
- **PowerShell**: Execute PowerShell commands with structured execution and output capture.
- **Hybrid**: Execute commands simultaneously in CMD and PowerShell and compare outputs.
- **Git**: Full Git automation (clone, init, add, commit, push, pull, branch, status, log).
- **Python**: Execute scripts, modules, and inline code, create virtual environments, and manage packages with Pip.
- **Filesystem**: Common file and folder operations (create, copy, move, delete, list).
- **Process Management**: Check, count, get info, suspend, resume, and kill processes, with special support for browsers.
- **System Class**: A unified interface to access all automation capabilities.

**Usage Examples**:
- Developer automation (code management, testing)
- DevOps workflows (deployment, monitoring)
- Windows automation (system management)
- New project initialization (init, venv)
- Command-line utilities
- Git automation (commit, push, branch)
- Python environment management (venv, pip)
- Process management (monitoring, closing browsers)
- System auditing and cleanup

**Use Cases**: Developer automation, DevOps workflows, Windows automation, project initialization, command-line utilities, Git automation, Python environment management, process management, and system administration.

---

### 7. General Tools Kit (Tools Kit) ** NEW **

A foundational layer providing common, reusable utilities for other modules and developers.

**Core Capabilities**:

* **File Tools (`file_tools.py`)**:
    * Basic file and folder operations (create, read, write, delete)
    * JSON file handling (`dump_file`, `load_file`)
    * File permission management (`get_permission`, `change_permission`)
    * Complete file metadata extraction (`information_files_dict`)

* **String Tools (`string_tools.py`)**:
    * Secure random string generation with `secrets`
    * Helper functions for random character generation
    * **Random character generation source for `password_kit` module**

* **Use Cases**: Developer automation, DevOps workflows, Windows automation, project initialization, command-line utilities, Git automation, Python environment management, process management, and system administration.

---

## Technical Requirements

### Environment
* Python 3.9+

### Dependencies
```bash
pip install requests beautifulsoup4 selenium tenacity deepdiff pyautogui pyperclip
```

### Standard Libraries
`hashlib`, `os`, `pathlib`, `datetime`, `json`, `shutil`, `string`, `random`, `re`, `typing`, `subprocess`, `time`, `pickle`

---

## Package Structure

```
src/allykit/
├── __init__.py
├── Security_kit/
│   ├── __init__.py
│   ├── file_kit.py
│   ├── password_kit.py
│   └── hash_kit.py
├── web_kit/
│   ├── __init__.py
│   ├── CChrome.py
│   ├── Communications.py
│   ├── WebAutomation.py
│   ├── Working_with_code.py
│   ├── Elastic_bands.py
│   ├── Get_Code.py
│   └── Cookie.py
├── data_kit/
│   ├── __init__.py
│   ├── IRAN/
│   │   └── __init__.py
│   │   └── education.py
│   │   └── geography.py
│   │   └── historical.py
│   │   └── telecom.py
│   ├── Language.py
│   └── country.py
└── Automobile_kit/
    ├── __init__.py
    ├── ProcessManager.py
    ├── Automobile/
    │   ├── __init__.py
    │   ├── Cmd.py
    │   ├── powershell.py
    │   └── hybrid.py
    └── New_automobile/
        ├── __init__.py
        ├── file.py
        ├── python.py
        └── git.py
```
## Version Summary

This version represents a significant step forward with the addition of Tools_kit and the modular rewrite of password_kit. The Security_kit modules now benefit from a foundational layer (Tools_kit), greatly improving code reusability and maintainability.

**Key Changes**:
- Added Tools_kit with file_tools and string_tools
- Complete modular rewrite of password_kit with Time_Password and Review_Password classes
- Added snapshot and integrity verification capabilities to file_kit