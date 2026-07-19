

from allykit.web_kit import fix_url
from allykit.web_kit.CChrome import chrome, browser_context , wait_for_element , get_headless_driver
from allykit.web_kit.Communications import fetch_url , execute_request , validate_links, get_rate_limit_info ,is_link_alive 
from allykit.web_kit.Elastic_bands import Monitoring , DiskCache
from allykit.web_kit.Get_Code import soup_url, javascript, javascript_driver , javascript_pro
from allykit.web_kit.WebAutomation import WebAutomation, By
from allykit.web_kit.Working_with_code import extract_all_links, extract_images, extract_text_from_tags, save_links ,save_link , SoupToDict, extract_structured_data

# ===== URL NORMALIZATION =====
fixed = fix_url("Example.COM//API//Users")              # Normalize URL
alive = fix_url("https://google.com", test=True)        # Check availability

url = fixed
# ===== HTTP REQUESTS =====
response = fetch_url("https://api.example.com/data")    # GET with retry
post_resp = execute_request(url, method="POST", data={"key": "value"})

# ===== HTML PARSING =====
soup = soup_url("https://example.com")                  # Fetch and parse
links = extract_all_links(soup)                         # Extract all links
images = extract_images(soup)                           # Extract images
text = extract_text_from_tags(soup, "p")                # Extract paragraphs

# ===== JAVASCRIPT RENDERING =====
js_soup = javascript("https://spa-site.com")            # Basic JS rendering
pro_soup = javascript_pro(                              # Advanced rendering
    "https://spa-site.com",
    scroll_to_bottom=True,
    headless=True
)

# ===== CACHING =====
cache = DiskCache(ttl_hours=48)                         # Initialize cache
cached = cache.html("https://example.com")              # Fetch with cache
js_cached = cache.javascript("https://example.com")     # JS with cache

# ===== WEB AUTOMATION =====
automation = WebAutomation()                            # Initialize
automation.open("https://example.com")                  # Navigate
automation.click((By.ID, "submit"))                     # Click element
automation.write((By.NAME, "email"), "user@example.com") # Fill form

# ===== HTML COMPARISON =====
soup1 = ''
soup2 = ''
comparator = SoupToDict(soup1, soup2)                   # Compare HTML
changes = comparator.get_changes()                      # Get changes
json_out = comparator.to_json(indent=2)                 # Export as JSON

# ===== FILE DOWNLOADS =====
save_link("https://example.com/file.pdf", "local.pdf")  # Download single
save_links(["url1", "url2"], "base_name")               # Download multiple