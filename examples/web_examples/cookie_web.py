
from allykit.web_kit.Cookie import Cookie
from allykit.web_kit.WebAutomation import WebAutomation
from allykit.web_kit.CChrome import chrome, get_headless_driver
from selenium.webdriver.common.by import By
import os
import time
import tempfile
import pickle


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_result(label, result):
    """Print a formatted result."""
    if isinstance(result, list):
        print(f"  → {label}: {len(result)} items")
        if result and len(result) > 0:
            for item in result[:3]:
                if isinstance(item, dict):
                    print(f"      {item.get('name', 'Unknown')}: {item.get('value', '')[:20]}...")
                else:
                    print(f"      {item}")
            if len(result) > 3:
                print(f"      ... and {len(result)-3} more")
    else:
        print(f"  → {label}: {result}")


# ============================================
# PART 1: SETUP
# ============================================
print_section("PART 1: SETUP & CONFIGURATION")

# 1.1 Create temporary directory for cookies
print("\n--- 1.1 Create Cookie Directory ---")
cookie_dir = tempfile.mkdtemp(prefix="cookies_")
cookie_file = os.path.join(cookie_dir, "cookies.pkl")
cookie_file2 = os.path.join(cookie_dir, "cookies_backup.pkl")
print(f"  Cookie directory: {cookie_dir}")
print(f"  Main cookie file: {cookie_file}")
print(f"  Backup cookie file: {cookie_file2}")

# 1.2 Initialize WebAutomation with headless browser
print("\n--- 1.2 Initialize WebAutomation ---")
try:
    # Create headless driver
    driver = get_headless_driver()
    print("✅ Headless Chrome driver initialized")
except Exception as e:
    print(f"⚠️ Headless failed, trying regular: {e}")
    driver = chrome(criterion=False, incognito=True)
    print("✅ Regular Chrome driver initialized")

# 1.3 Navigate to test URL
print("\n--- 1.3 Navigate to Test URL ---")
test_url = "https://example.com"
driver.get(test_url)
print(f"  Navigated to: {test_url}")
print(f"  Page title: {driver.title}")


# ============================================
# PART 2: BASIC COOKIE OPERATIONS
# ============================================
print_section("PART 2: BASIC COOKIE OPERATIONS")

# 2.1 Create Cookie instance
print("\n--- 2.1 Create Cookie Instance ---")
cookie_manager = Cookie(driver=driver, cookie_file=cookie_file)
print("✅ Cookie manager created")
print(f"  Cookie file: {cookie_manager.cookie_file}")

# 2.2 Get initial cookies
print("\n--- 2.2 Get Initial Cookies ---")
initial_cookies = driver.get_cookies()
print_result("Initial cookies", initial_cookies)

# 2.3 Add custom cookies
print("\n--- 2.3 Add Custom Cookies ---")
test_cookies = [
    {
        'name': 'user_session',
        'value': 'abc123def456',
        'domain': 'example.com',
        'path': '/',
        'secure': False,
        'httpOnly': False
    },
    {
        'name': 'preferences',
        'value': 'dark_mode=on;language=en',
        'domain': 'example.com',
        'path': '/'
    },
    {
        'name': 'analytics_id',
        'value': 'UA-123456-1',
        'domain': 'example.com',
        'path': '/'
    }
]

for cookie in test_cookies:
    try:
        driver.add_cookie(cookie)
        print(f"  ✅ Added cookie: {cookie['name']}")
    except Exception as e:
        print(f"  ❌ Failed to add cookie {cookie['name']}: {e}")

# 2.4 Verify cookies added
print("\n--- 2.4 Verify Cookies ---")
all_cookies = driver.get_cookies()
print_result("All cookies after adding", all_cookies)

# 2.5 Save cookies to file
print("\n--- 2.5 Save Cookies to File ---")
save_result = cookie_manager.save_cookies()
print_result("Save cookies result", "✅ Success" if save_result else "❌ Failed")

# 2.6 Check if file exists
print("\n--- 2.6 Check Cookie File ---")
file_exists = os.path.exists(cookie_file)
print_result("Cookie file exists", file_exists)

# 2.7 Get cookie file size
if file_exists:
    file_size = os.path.getsize(cookie_file)
    print_result("Cookie file size", f"{file_size} bytes")


# ============================================
# PART 3: LOADING COOKIES
# ============================================
print_section("PART 3: LOADING COOKIES")

# 3.1 Clear all cookies
print("\n--- 3.1 Clear All Cookies ---")
driver.delete_all_cookies()
print("✅ All cookies cleared")
print_result("Current cookies after clear", driver.get_cookies())

# 3.2 Load cookies from file
print("\n--- 3.2 Load Cookies from File ---")
load_result = cookie_manager.load_cookies(loaded=True)
print_result("Load cookies result", "✅ Success" if load_result else "❌ Failed")

# 3.3 Verify loaded cookies
print("\n--- 3.3 Verify Loaded Cookies ---")
loaded_cookies = driver.get_cookies()
print_result("Loaded cookies count", loaded_cookies)
for cookie in loaded_cookies[:3]:
    print(f"  → {cookie['name']}: {cookie['value'][:20]}...")
if len(loaded_cookies) > 3:
    print(f"  → ... and {len(loaded_cookies)-3} more")

# 3.4 Load cookies from different file
print("\n--- 3.4 Load Cookies from Different File ---")
# Save current cookies to backup
cookie_manager.switch_cookie_file(cookie_file2)
cookie_manager.save_cookies()
print(f"  ✅ Cookies saved to backup: {cookie_file2}")

# Clear and load from backup
driver.delete_all_cookies()
load_from_file = cookie_manager.load_cookies_from_file(cookie_file2)
print_result("Load from backup", "✅ Success" if load_from_file else "❌ Failed")


# ============================================
# PART 4: COOKIE MANAGEMENT
# ============================================
print_section("PART 4: COOKIE MANAGEMENT")

# 4.1 Load cookies if needed
print("\n--- 4.1 Load Cookies If Needed ---")
# Clear cookies first
driver.delete_all_cookies()
print("  ✅ Cookies cleared")

# Try to load if needed
result = cookie_manager.load_cookies_if_needed()
print_result("Load if needed result", "✅ Success" if result else "❌ Failed")

# 4.2 Get expired cookies
print("\n--- 4.2 Get Expired Cookies ---")
expired = cookie_manager.get_expired_cookies()
print_result("Expired cookies", expired)

# 4.3 Create expired cookie for testing
print("\n--- 4.3 Create Expired Cookie ---")
import time as time_module
expired_cookie = {
    'name': 'expired_session',
    'value': 'expired123',
    'domain': 'example.com',
    'path': '/',
    'expiry': int(time_module.time() - 3600)  # Expired 1 hour ago
}
try:
    driver.add_cookie(expired_cookie)
    print("  ✅ Added expired cookie for testing")
except Exception as e:
    print(f"  ❌ Could not add expired cookie: {e}")

# 4.4 Check expired cookies again
print("\n--- 4.4 Check Expired Cookies ---")
expired_after = cookie_manager.get_expired_cookies()
print_result("Expired cookies after adding test cookie", expired_after)

# 4.5 Clear expired cookies
print("\n--- 4.5 Clear Expired Cookies ---")
cookie_manager.clear_expired_cookies()
print("  ✅ Expired cookies cleared")

# 4.6 Verify expired cookies removed
print("\n--- 4.6 Verify Expired Removed ---")
expired_final = cookie_manager.get_expired_cookies()
print_result("Expired cookies after clearing", expired_final)


# ============================================
# PART 5: COOKIE FILE MANAGEMENT
# ============================================
print_section("PART 5: COOKIE FILE MANAGEMENT")

# 5.1 Switch cookie file
print("\n--- 5.1 Switch Cookie File ---")
print(f"  Current cookie file: {cookie_manager.cookie_file}")
cookie_manager.switch_cookie_file(cookie_file2)
print(f"  New cookie file: {cookie_manager.cookie_file}")

# 5.2 Save to new file
print("\n--- 5.2 Save to New File ---")
save_new = cookie_manager.save_cookies()
print_result("Save to new file", "✅ Success" if save_new else "❌ Failed")

# 5.3 Load from new file
print("\n--- 5.3 Load from New File ---")
driver.delete_all_cookies()
load_new = cookie_manager.load_cookies()
print_result("Load from new file", "✅ Success" if load_new else "❌ Failed")

# 5.4 Switch back to original
print("\n--- 5.4 Switch Back to Original ---")
cookie_manager.switch_cookie_file(cookie_file)
print(f"  Switched back to: {cookie_manager.cookie_file}")


# ============================================
# PART 6: WEB AUTOMATION WITH COOKIES
# ============================================
print_section("PART 6: WEB AUTOMATION WITH COOKIES")

# 6.1 Create WebAutomation instance
print("\n--- 6.1 Create WebAutomation ---")
automation = WebAutomation(timeout=10)
print("  ✅ WebAutomation created")

# 6.2 Navigate and set cookies
print("\n--- 6.2 Navigate and Set Cookies ---")
automation.open("https://example.com")
print(f"  Current URL: {automation.driver.current_url}")

# Create cookie manager for automation
cookie_auto = Cookie(
    driver=automation.driver,
    cookie_file=os.path.join(cookie_dir, "automation_cookies.pkl")
)

# Add automation-specific cookies
auto_cookies = [
    {'name': 'automation_session', 'value': 'auto_12345', 'domain': 'example.com', 'path': '/'},
    {'name': 'test_mode', 'value': 'true', 'domain': 'example.com', 'path': '/'}
]

for cookie in auto_cookies:
    try:
        automation.driver.add_cookie(cookie)
        print(f"  ✅ Added: {cookie['name']}")
    except Exception as e:
        print(f"  ❌ Failed: {e}")

# Save automation cookies
cookie_auto.save_cookies()
print("  ✅ Automation cookies saved")

# 6.3 Clear and reload
print("\n--- 6.3 Clear and Reload ---")
automation.driver.delete_all_cookies()
print("  ✅ Cookies cleared")

# Reload cookies
cookie_auto.load_cookies(loaded=True)
print("  ✅ Cookies reloaded")

# 6.4 Get page with cookies
print("\n--- 6.4 Page with Cookies ---")
automation.open("https://example.com")
print("  ✅ Page loaded with cookies")


# ============================================
# PART 7: REAL-WORLD AUTOMATION SCENARIOS
# ============================================
print_section("PART 7: REAL-WORLD AUTOMATION SCENARIOS")

# 7.1 Scenario: Login session management
print("\n--- 7.1 Login Session Management ---")
print("  🎯 Simulating login session with cookies...")

# Create session cookies
session_cookies = [
    {
        'name': 'auth_token',
        'value': 'abcdef1234567890',
        'domain': 'example.com',
        'path': '/',
        'secure': False,
        'expiry': int(time_module.time() + 86400)  # 24 hours
    },
    {
        'name': 'user_id',
        'value': 'user_12345',
        'domain': 'example.com',
        'path': '/'
    },
    {
        'name': 'session_id',
        'value': 'sess_987654321',
        'domain': 'example.com',
        'path': '/'
    }
]

driver.delete_all_cookies()
for cookie in session_cookies:
    try:
        driver.add_cookie(cookie)
        print(f"  ✅ Added session cookie: {cookie['name']}")
    except Exception as e:
        print(f"  ❌ Failed: {e}")

# Save session
session_file = os.path.join(cookie_dir, "session_cookies.pkl")
cookie_manager.switch_cookie_file(session_file)
cookie_manager.save_cookies()
print(f"  ✅ Session cookies saved to: {session_file}")

# 7.2 Scenario: Cookie rotation
print("\n--- 7.2 Cookie Rotation ---")
print("  🔄 Rotating cookies...")

# Save current cookies
rotation_file = os.path.join(cookie_dir, "rotation_1.pkl")
cookie_manager.switch_cookie_file(rotation_file)
cookie_manager.save_cookies()
print(f"  ✅ Cookies saved to: {rotation_file}")

# Generate new cookies
new_cookies = [
    {
        'name': 'new_session',
        'value': 'new_token_123',
        'domain': 'example.com',
        'path': '/'
    }
]
for cookie in new_cookies:
    driver.add_cookie(cookie)

# Save rotation
rotation_file2 = os.path.join(cookie_dir, "rotation_2.pkl")
cookie_manager.switch_cookie_file(rotation_file2)
cookie_manager.save_cookies()
print(f"  ✅ Rotation cookies saved to: {rotation_file2}")

# Switch back
cookie_manager.switch_cookie_file(cookie_file)
print("  ✅ Switched back to original cookie file")

# 7.3 Scenario: Cookie expiration monitoring
print("\n--- 7.3 Cookie Expiration Monitoring ---")
print("  📊 Monitoring cookie expiration...")

# Add cookies with different expiration times
expiry_cookies = [
    {
        'name': 'short_lived',
        'value': 'expires_soon',
        'domain': 'example.com',
        'path': '/',
        'expiry': int(time_module.time() + 300)  # 5 minutes
    },
    {
        'name': 'medium_lived',
        'value': 'expires_later',
        'domain': 'example.com',
        'path': '/',
        'expiry': int(time_module.time() + 3600)  # 1 hour
    },
    {
        'name': 'long_lived',
        'value': 'expires_far',
        'domain': 'example.com',
        'path': '/',
        'expiry': int(time_module.time() + 86400)  # 24 hours
    }
]

for cookie in expiry_cookies:
    try:
        driver.add_cookie(cookie)
        minutes = int((cookie['expiry'] - time_module.time()) / 60)
        print(f"  ✅ Added cookie: {cookie['name']} (expires in {minutes} minutes)")
    except Exception as e:
        print(f"  ❌ Failed: {e}")

# Check expired
expired = cookie_manager.get_expired_cookies()
if expired:
    print(f"  ⚠️ Found {len(expired)} expired cookies")
    for cookie in expired:
        print(f"    → {cookie['name']} expired")
else:
    print("  ✅ No expired cookies found")

# 7.4 Scenario: Multi-profile cookie management
print("\n--- 7.4 Multi-Profile Cookie Management ---")
profiles = ["profile_user1", "profile_user2", "profile_guest"]

for profile in profiles:
    profile_file = os.path.join(cookie_dir, f"{profile}.pkl")
    print(f"\n  📂 Profile: {profile}")
    print(f"    File: {profile_file}")
    
    # Switch to profile file
    cookie_manager.switch_cookie_file(profile_file)
    
    # Create profile-specific cookies
    profile_cookies = [
        {
            'name': 'profile',
            'value': profile,
            'domain': 'example.com',
            'path': '/'
        },
        {
            'name': f'{profile}_session',
            'value': f'token_{profile}_123',
            'domain': 'example.com',
            'path': '/'
        }
    ]
    
    for cookie in profile_cookies:
        try:
            driver.add_cookie(cookie)
        except Exception:
            pass
    
    # Save profile cookies
    cookie_manager.save_cookies()
    print(f"    ✅ {profile} cookies saved")

# 7.5 Scenario: Cookie backup and restore
print("\n--- 7.5 Cookie Backup and Restore ---")
backup_file = os.path.join(cookie_dir, "backup_all_cookies.pkl")

# Create backup
cookie_manager.switch_cookie_file(backup_file)
cookie_manager.save_cookies()
print(f"  ✅ Backup created: {backup_file}")

# Simulate cookie loss
driver.delete_all_cookies()
print("  ✅ Cookies cleared (simulating loss)")

# Restore from backup
cookie_manager.load_cookies()
print("  ✅ Cookies restored from backup")

# 7.6 Scenario: Cookie export/import
print("\n--- 7.6 Cookie Export/Import ---")
export_file = os.path.join(cookie_dir, "exported_cookies.json")

# Export cookies to JSON
current_cookies = driver.get_cookies()
import json
with open(export_file, "w") as f:
    json.dump(current_cookies, f, indent=2)
print(f"  ✅ Cookies exported to: {export_file}")

# Clear and import
driver.delete_all_cookies()
with open(export_file, "r") as f:
    imported_cookies = json.load(f)
    for cookie in imported_cookies:
        try:
            driver.add_cookie(cookie)
        except Exception:
            pass
print("  ✅ Cookies imported from JSON")


# ============================================
# PART 8: COOKIE CLASS PROPERTIES
# ============================================
print_section("PART 8: COOKIE CLASS PROPERTIES")

# 8.1 Test __str__ method
print("\n--- 8.1 String Representation ---")
print(f"  Cookie class: {cookie_manager}")
print(f"  repr: {repr(cookie_manager)}")

# 8.2 Cookie file operations
print("\n--- 8.2 File Operations ---")
print(f"  Current file: {cookie_manager.cookie_file}")
print(f"  File exists: {os.path.exists(cookie_manager.cookie_file)}")
print(f"  File size: {os.path.getsize(cookie_manager.cookie_file) if os.path.exists(cookie_manager.cookie_file) else 0} bytes")


# ============================================
# PART 9: ERROR HANDLING
# ============================================
print_section("PART 9: ERROR HANDLING")

# 9.1 Invalid cookie file
print("\n--- 9.1 Invalid Cookie File ---")
try:
    invalid_manager = Cookie(
        driver=driver,
        cookie_file="/invalid/path/cookies.pkl"
    )
    invalid_manager.load_cookies()
    print("  ⚠️ Should have failed but didn't")
except Exception as e:
    print(f"  ✅ Caught error: {type(e).__name__}")

# 9.2 Load from non-existent file
print("\n--- 9.2 Non-existent File ---")
result = cookie_manager.load_cookies_from_file("/non/existent/file.pkl")
print_result("Load from non-existent file", "✅ Failed gracefully" if not result else "❌ Unexpected success")

# 9.3 Save with invalid cookies
print("\n--- 9.3 Invalid Cookie Data ---")
try:
    # Try to save invalid data
    cookie_manager.save_cookies(cookies="invalid_data")
    print("  ⚠️ Should have failed but didn't")
except Exception as e:
    print(f"  ✅ Caught error: {type(e).__name__}")


# ============================================
# PART 10: CLEANUP
# ============================================
print_section("PART 10: CLEANUP")

# 10.1 Close browser
print("\n--- 10.1 Close Browser ---")
try:
    driver.quit()
    print("  ✅ Browser closed")
except Exception as e:
    print(f"  Browser close error: {e}")

# 10.2 Cleanup cookie directory
print("\n--- 10.2 Cleanup Cookie Directory ---")
try:
    import shutil
    shutil.rmtree(cookie_dir)
    print(f"  ✅ Removed cookie directory: {cookie_dir}")
except Exception as e:
    print(f"  Cleanup error: {e}")

print("\n" + "=" * 70)
print("✅ ALL DEMONSTRATIONS COMPLETED SUCCESSFULLY!")
print("=" * 70)

print("\n📊 SUMMARY OF COOKIE OPERATIONS:")
print("=" * 70)
print("  ✅ Cookie creation and management")
print("  ✅ Save cookies to file (pickle format)")
print("  ✅ Load cookies from file")
print("  ✅ Switch between cookie files")
print("  ✅ Load cookies from different file")
print("  ✅ Load cookies if needed")
print("  ✅ Get expired cookies")
print("  ✅ Clear expired cookies")
print("  ✅ WebAutomation integration")
print("  ✅ Real-world automation scenarios")
print("  ✅ Multi-profile cookie management")
print("  ✅ Cookie backup and restore")
print("  ✅ Cookie export/import (JSON)")
print("  ✅ Error handling")

print("\n📌 KEY COOKIE CLASS METHODS:")
print("=" * 70)
print("  🔹 save_cookies()          - Save cookies to file")
print("  🔹 load_cookies()          - Load cookies from file")
print("  🔹 load_cookies_from_file() - Load from specific file")
print("  🔹 load_cookies_if_needed() - Load if not already loaded")
print("  🔹 get_expired_cookies()   - Get expired cookies")
print("  🔹 clear_expired_cookies() - Remove expired cookies")
print("  🔹 switch_cookie_file()    - Change cookie file")
print("  🔹 __str__()               - String representation")
print("  🔹 __init__()              - Initialize with driver and file")

print("\n" + "=" * 70)