
from allykit.data_kit.Language import LANGUAGE_CHARS
from allykit.data_kit.country import COUNTRY_LIST, get_iso_numeric

from allykit import (
    # Language utilities
    detect_language,
    filter_by_language,
    normalize_digits,
    is_rtl_char,
    char_type,
    to_ascii_approx,
    is_persian,
    is_arabic,
    is_english,
    
    # Country utilities
    get_country_by_code,
    get_calling_code,
    get_country_info,
    search_country,
    format_phone_number,
    get_iso_alpha2,
    get_iso_alpha3,
    get_continent,
    get_capital,
    get_currency,
    
    # Iran utilities
    get_city_full_info,
    get_province_of_city,
    get_city_coords,
    get_sim_operator,
    get_car_plate_codes,
    get_city_population,
    get_city_phone_code,
    search_city,
    get_provinces_by_region,
)

import json


# ============================================
# PART 1: LANGUAGE DETECTION & CHARACTER CLASSIFICATION
# ============================================
print("=" * 70)
print("PART 1: LANGUAGE DETECTION & CHARACTER CLASSIFICATION")
print("=" * 70)

# 1.1 Detect language of text
print("\n--- 1.1 Language Detection ---")
texts = [
    "Hello, how are you?",
    "سلام، چطوری؟",
    "مرحبا، كيف حالك؟",
    "Привет, как дела?",
    "今日は、お元気ですか？",
    "नमस्ते, आप कैसे हैं?"
]

for text in texts:
    lang = detect_language(text)
    print(f"Text: {text[:20]}... -> Language: {lang}")

# 1.2 Filter by language
print("\n--- 1.2 Filter by Language ---")
mixed_text = "Hello سلام World دنیا"
persian_only = filter_by_language(mixed_text, "persian")
english_only = filter_by_language(mixed_text, "english")
print(f"Original: {mixed_text}")
print(f"Persian only: {persian_only}")
print(f"English only: {english_only}")

# 1.3 Normalize digits (convert any script digits to ASCII)
print("\n--- 1.3 Normalize Digits ---")
digit_samples = [
    "۱۲۳۴۵",  # Persian
    "१२३४५",  # Devanagari
    "๑๒๓๔๕",  # Thai
    "12345"    # ASCII
]
for sample in digit_samples:
    normalized = normalize_digits(sample)
    print(f"Original: {sample} -> Normalized: {normalized}")

# 1.4 Character type classification
print("\n--- 1.4 Character Type Classification ---")
chars = ["a", "5", "ا", " ", "!", "A", "۱"]
for char in chars:
    ctype = char_type(char)
    print(f"Character: '{char}' -> Type: {ctype}")

# 1.5 RTL character detection
print("\n--- 1.5 RTL Character Detection ---")
rtl_samples = ["ا", "ب", "א", "a", "1"]
for char in rtl_samples:
    is_rtl = is_rtl_char(char)
    print(f"Character: '{char}' -> RTL: {is_rtl}")

# 1.6 Language-specific checks
print("\n--- 1.6 Language-Specific Checks ---")
test_strings = [
    ("سلام", is_persian),
    ("Hello", is_english),
    ("مرحبا", is_arabic),
    ("123", is_english)
]
for text, func in test_strings:
    result = func(text)
    print(f"'{text}' -> {func.__name__}: {result}")

# 1.7 ASCII approximation (transliteration)
print("\n--- 1.7 ASCII Approximation ---")
persian_text = "سلام دنیا"
approx = to_ascii_approx(persian_text)
print(f"Persian: {persian_text} -> ASCII: {approx}")

german_text = "München"
approx_german = to_ascii_approx(german_text)
print(f"German: {german_text} -> ASCII: {approx_german}")


# ============================================
# PART 2: COUNTRY DATA
# ============================================
print("\n" + "=" * 70)
print("PART 2: COUNTRY DATA")
print("=" * 70)

# 2.1 Get country by calling code
print("\n--- 2.1 Country by Calling Code ---")
codes = [98, 44, 1, 91, 86]
for code in codes:
    country = get_country_by_code(code)
    print(f"Code +{code} -> {country}")

# 2.2 Get calling code by country
print("\n--- 2.2 Calling Code by Country ---")
countries = ["Iran", "United Kingdom", "Japan", "Brazil"]
for country in countries:
    code = get_calling_code(country)
    print(f"{country} -> +{code}")

# 2.3 Get country information (comprehensive)
print("\n--- 2.3 Country Information ---")
target_country = "Iran"
info = get_country_info(target_country)
print(f"Information for {target_country}:")
for key, value in info.items():
    print(f"  - {key}: {value}")

# 2.4 Search countries
print("\n--- 2.4 Search Countries ---")
query = "uni"
results = search_country(query)
print(f"Countries containing '{query}': {results}")

query = "stan"
results = search_country(query)
print(f"Countries containing '{query}': {results}")

# 2.5 ISO codes
print("\n--- 2.5 ISO Codes ---")
for country in ["Iran", "Germany", "Japan"]:
    alpha2 = get_iso_alpha2(country)
    alpha3 = get_iso_alpha3(country)
    numeric = get_iso_numeric(country)
    print(f"{country}: Alpha-2: {alpha2}, Alpha-3: {alpha3}, Numeric: {numeric}")

# 2.6 Continent, capital, currency
print("\n--- 2.6 Continent, Capital, Currency ---")
for country in ["Iran", "France", "Australia"]:
    continent = get_continent(country)
    capital = get_capital(country)
    currency = get_currency(country)
    print(f"{country}: Continent: {continent}, Capital: {capital}, Currency: {currency}")

# 2.7 Format phone number
print("\n--- 2.7 Format Phone Number ---")
phone_number = format_phone_number(98, "21 12345678")
print(f"Formatted: {phone_number}")

# 2.8 Parse phone number (utility demonstration)
print("\n--- 2.8 Phone Number Parse ---")
from allykit.data_kit.country import parse_phone_number  # Not in __init__ but available

test_numbers = ["+982112345678", "+442079460958", "+919876543210"]
for num in test_numbers:
    code, rest = parse_phone_number(num)
    if code:
        country = get_country_by_code(code)
        print(f"{num} -> Country: {country}, Code: +{code}, Number: {rest}")
    else:
        print(f"{num} -> Could not parse")


# ============================================
# PART 3: IRAN GEOGRAPHIC DATA
# ============================================
print("\n" + "=" * 70)
print("PART 3: IRAN GEOGRAPHIC DATA")
print("=" * 70)

# 3.1 Get province of a city
print("\n--- 3.1 Province of City ---")
cities = ["تهران", "اصفهان", "مشهد", "شیراز", "تبریز"]
for city in cities:
    province = get_province_of_city(city)
    print(f"{city} -> {province}")

# 3.2 Get city coordinates
print("\n--- 3.2 City Coordinates ---")
for city in cities[:3]:
    coords = get_city_coords(city)
    if coords:
        print(f"{city}: Latitude {coords[0]:.4f}, Longitude {coords[1]:.4f}")
    else:
        print(f"{city}: Coordinates not found")

# 3.3 Get full city information
print("\n--- 3.3 Full City Information ---")
city = "تهران"
full_info = get_city_full_info(city)
print(f"Full info for {city}:")
if full_info:
    for key, value in full_info.items():
        print(f"  - {key}: {value}")

# 3.4 Search cities
print("\n--- 3.4 Search Cities ---")
query = "آب"
results = search_city(query)
print(f"Cities containing '{query}': {results[:5]}... (showing first 5)")

# 3.5 Get city population
print("\n--- 3.5 City Population ---")
major_cities = ["تهران", "مشهد", "اصفهان", "کرج", "شیراز"]
for city in major_cities:
    population = get_city_population(city)
    print(f"{city}: {population:,} people")

# 3.6 Get SIM card operator
print("\n--- 3.6 SIM Card Operator Detection ---")
prefixes = ["0912", "0935", "0920", "0990", "0910"]
for prefix in prefixes:
    operator = get_sim_operator(prefix)
    print(f"Prefix {prefix} -> {operator}")

# 3.7 Get city phone code
print("\n--- 3.7 City Phone Code ---")
for city in ["تهران", "اصفهان", "شیراز", "مشهد"]:
    code = get_city_phone_code(city)
    print(f"{city}: Area code {code}")

# 3.8 Get car plate codes
print("\n--- 3.8 Car Plate Codes by Province ---")
provinces = ["تهران", "اصفهان", "فارس"]
for province in provinces:
    codes = get_car_plate_codes(province)
    print(f"{province}: Plate codes {codes}")

# 3.9 Get provinces by region
print("\n--- 3.9 Provinces by Region ---")
regions = ["مرکز", "شمال", "جنوب", "غرب"]
for region in regions:
    provinces = get_provinces_by_region(region)
    print(f"Region {region}: {provinces}")


# ============================================
# PART 4: IRAN - COMPREHENSIVE DEMO
# ============================================
print("\n" + "=" * 70)
print("PART 4: IRAN - COMPREHENSIVE DATA EXPLORATION")
print("=" * 70)

# 4.1 List all provinces with metadata_kit
print("\n--- 4.1 Province Metadata_kit ---")
from allykit.data_kit.IRAN import province_metadata_kit, iran_provinces

print(f"Total provinces: {len(iran_provinces)}")
print("First 5 provinces with metadata_kit:")
for province in iran_provinces[:5]:
    meta = province_metadata_kit.get(province, {})
    print(f"  - {province}: Code {meta.get('code')}, "
          f"Region {meta.get('region')}, "
          f"Population {meta.get('population', 0):,}")

# 4.2 List cities in a province
print("\n--- 4.2 Cities in Province ---")
from allykit.data_kit.IRAN import provinces_and_cities

province = "تهران"
cities = provinces_and_cities.get(province, [])
print(f"Cities in {province}:")
for city in cities[:10]:  # Show first 10
    print(f"  - {city}")

# 4.3 City coordinates mapping
print("\n--- 4.3 City Coordinates Sample ---")
from allykit.data_kit.IRAN import city_coordinates

print("Sample city coordinates:")
sample_cities = ["تهران", "اصفهان", "مشهد", "شیراز"]
for city in sample_cities:
    coords = city_coordinates.get(city)
    if coords:
        print(f"  - {city}: ({coords[0]:.4f}, {coords[1]:.4f})")

# 4.4 SIM card prefix operators
print("\n--- 4.4 SIM Card Operators ---")
from allykit.data_kit.IRAN import sim_card_prefixes

operators = ["همراه اول", "ایرانسل", "رایتل", "آپتل"]
for operator in operators:
    prefixes = sim_card_prefixes.get(operator, [])
    print(f"{operator}: {len(prefixes)} prefixes, e.g., {prefixes[:3]}")

# 4.5 City populations (sorted)
print("\n--- 4.5 Top 10 Cities by Population ---")
from allykit.data_kit.IRAN import city_population

top_cities = sorted(city_population.items(), key=lambda x: x[1], reverse=True)[:10]
print("Top 10 cities by population:")
for rank, (city, population) in enumerate(top_cities, 1):
    print(f"  {rank}. {city}: {population:,} people")


# ============================================
# PART 5: LANGUAGE & GEOGRAPHY COMBINED
# ============================================
print("\n" + "=" * 70)
print("PART 5: LANGUAGE & GEOGRAPHY COMBINED")
print("=" * 70)

# 5.1 Multi-language country name detection
print("\n--- 5.1 Country Names in Different Scripts ---")
country_names = [
    ("ایران", "Iran"),
    ("مصر", "Egypt"),
    ("المان", "Germany"),
    ("هند", "India")
]

for persian_name, english_name in country_names:
    # Detect language
    lang = detect_language(persian_name)
    # Get country info
    info = get_country_info(english_name)
    print(f"{persian_name} ({lang}): {english_name}, Code +{info['calling_code']}")

# 5.2 Format phone numbers with country detection
print("\n--- 5.2 Format Phone Numbers ---")
phone_numbers = [
    "+982112345678",
    "+442079460958",
    "+919876543210"
]

for phone in phone_numbers:
    code, rest = parse_phone_number(phone)
    if code:
        country = get_country_by_code(code)
        formatted = format_phone_number(code, rest)
        print(f"{phone} -> {formatted} ({country})")
    else:
        print(f"{phone} -> Could not parse")

# 5.3 Persian text with geographic data_kit
print("\n--- 5.3 Persian Geographic Query ---")
query_city = "اصفهان"
province = get_province_of_city(query_city)
population = get_city_population(query_city)
coords = get_city_coords(query_city)
phone_code = get_city_phone_code(query_city)

print(f"City: {query_city}")
print(f"  Province: {province}")
print(f"  Population: {population:,}")
print(f"  Coordinates: {coords}")
print(f"  Area code: {phone_code}")
print(f"  English name: {to_ascii_approx(query_city)}")

# 5.4 Multi-language text analysis
print("\n--- 5.4 Multi-language Analysis ---")
sample_text = "Hello, ایران is a beautiful country with many cities like تهران and اصفهان."

print(f"Original: {sample_text}")
print(f"Languages detected: {detect_language(sample_text)}")
print(f"Persian characters: {filter_by_language(sample_text, 'persian')}")
print(f"English characters: {filter_by_language(sample_text, 'english')}")

# ============================================
# CLEANUP & SUMMARY
# ============================================
print("\n" + "=" * 70)
print("✅ ALL DEMONSTRATIONS COMPLETED SUCCESSFULLY!")
print("=" * 70)
print("\nSummary of available data_kit:")
print(f"  - Countries: {len(COUNTRY_LIST) if 'COUNTRY_LIST' in dir() else 'N/A'}")
print(f"  - Iran provinces: {len(iran_provinces)}")
print(f"  - Iran cities: {len(city_population)} with population data_kit")
print(f"  - SIM operators: {len(sim_card_prefixes)}")
print(f"  - Language sets: {len(LANGUAGE_CHARS) if 'LANGUAGE_CHARS' in dir() else 'N/A'}")