

from allykit import *

# ===== LANGUAGE =====
lang = detect_language("Hello")                     # Detect language
persian = filter_by_language("Hello سلام", "persian")  # Filter by language
normalized = normalize_digits("۱۲۳")               # Convert to ASCII digits
is_rtl = is_rtl_char("ا")                          # Check RTL character
ctype = char_type("a")                             # Classify character
ascii_approx = to_ascii_approx("سلام")            # Transliterate to ASCII

# ===== COUNTRY =====
country = get_country_by_code(98)                  # Country by calling code
code = get_calling_code("Iran")                    # Calling code by country
info = get_country_info("Iran")                    # Complete country info
search = search_country("uni")                     # Search countries
phone = format_phone_number(98, "2112345678")      # Format phone number
alpha2 = get_iso_alpha2("Iran")                    # ISO alpha-2 code
capital = get_capital("France")                    # Capital city
currency = get_currency("Japan")                   # Currency name

# ===== IRAN =====
province = get_province_of_city("تهران")           # Province of city
coords = get_city_coords("اصفهان")                 # City coordinates
population = get_city_population("مشهد")           # City population
operator = get_sim_operator("0912")                # SIM operator
area_code = get_city_phone_code("شیراز")           # Area code
plate_codes = get_car_plate_codes("تهران")         # Car plate codes
full_info = get_city_full_info("تهران")            # Complete city info
cities = search_city("آب")                         # Search cities
provinces = get_provinces_by_region("مرکز")        # Provinces in region