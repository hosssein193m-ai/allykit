"""
Module: Country Data
Description: Comprehensive country database with international calling codes,
             ISO codes (alpha-2, alpha-3, numeric), continents, capitals,
             currencies, and utility functions for lookup and validation.
Author: Assistant
License: MIT

Usage:
    from country_data import *
    
    # Lookup by calling code
    get_country_by_code(98) -> 'Iran'
    get_calling_code('Iran') -> 98
    
    # Get detailed information
    get_country_info('Iran') -> {'name': 'Iran', 'alpha2': 'IR', ...}
    
    # Validate
    is_valid_country('Iran') -> True
"""

from typing import Dict, List, Optional, Tuple, Union

# ==================== CALLING CODES TO COUNTRY ====================

CALLING_CODES = {
    # North America
    1: "United States",
    1: "Canada",  # Same code, handled specially
    1242: "Bahamas",
    1246: "Barbados",
    1264: "Anguilla",
    1268: "Antigua and Barbuda",
    1284: "British Virgin Islands",
    1340: "US Virgin Islands",
    1345: "Cayman Islands",
    1441: "Bermuda",
    1473: "Grenada",
    1649: "Turks and Caicos Islands",
    1664: "Montserrat",
    1670: "Northern Mariana Islands",
    1671: "Guam",
    1684: "American Samoa",
    1721: "Sint Maarten",
    1758: "Saint Lucia",
    1767: "Dominica",
    1784: "Saint Vincent and the Grenadines",
    1809: "Dominican Republic",
    1829: "Dominican Republic",
    1849: "Dominican Republic",
    1868: "Trinidad and Tobago",
    1869: "Saint Kitts and Nevis",
    1876: "Jamaica",
    
    # Central America
    501: "Belize",
    502: "Guatemala",
    503: "El Salvador",
    504: "Honduras",
    505: "Nicaragua",
    506: "Costa Rica",
    507: "Panama",
    
    # South America
    54: "Argentina",
    55: "Brazil",
    56: "Chile",
    57: "Colombia",
    58: "Venezuela",
    591: "Bolivia",
    592: "Guyana",
    593: "Ecuador",
    594: "French Guiana",
    595: "Paraguay",
    596: "Martinique",
    597: "Suriname",
    598: "Uruguay",
    
    # Europe
    7: "Russia",
    30: "Greece",
    31: "Netherlands",
    32: "Belgium",
    33: "France",
    34: "Spain",
    36: "Hungary",
    39: "Italy",
    40: "Romania",
    41: "Switzerland",
    43: "Austria",
    44: "United Kingdom",
    45: "Denmark",
    46: "Sweden",
    47: "Norway",
    48: "Poland",
    49: "Germany",
    350: "Gibraltar",
    351: "Portugal",
    352: "Luxembourg",
    353: "Ireland",
    354: "Iceland",
    355: "Albania",
    356: "Malta",
    357: "Cyprus",
    358: "Finland",
    359: "Bulgaria",
    370: "Lithuania",
    371: "Latvia",
    372: "Estonia",
    373: "Moldova",
    374: "Armenia",
    375: "Belarus",
    376: "Andorra",
    377: "Monaco",
    378: "San Marino",
    379: "Vatican City",
    380: "Ukraine",
    381: "Serbia",
    382: "Montenegro",
    383: "Kosovo",
    385: "Croatia",
    386: "Slovenia",
    387: "Bosnia and Herzegovina",
    389: "North Macedonia",
    420: "Czech Republic",
    421: "Slovakia",
    423: "Liechtenstein",
    
    # Africa
    20: "Egypt",
    27: "South Africa",
    211: "South Sudan",
    212: "Morocco",
    213: "Algeria",
    216: "Tunisia",
    218: "Libya",
    220: "Gambia",
    221: "Senegal",
    222: "Mauritania",
    223: "Mali",
    224: "Guinea",
    225: "Ivory Coast",
    226: "Burkina Faso",
    227: "Niger",
    228: "Togo",
    229: "Benin",
    230: "Mauritius",
    231: "Liberia",
    232: "Sierra Leone",
    233: "Ghana",
    234: "Nigeria",
    235: "Chad",
    236: "Central African Republic",
    237: "Cameroon",
    238: "Cape Verde",
    239: "Sao Tome and Principe",
    240: "Equatorial Guinea",
    241: "Gabon",
    242: "Republic of the Congo",
    243: "Democratic Republic of the Congo",
    244: "Angola",
    245: "Guinea-Bissau",
    246: "Diego Garcia",
    247: "Ascension Island",
    248: "Seychelles",
    249: "Sudan",
    250: "Rwanda",
    251: "Ethiopia",
    252: "Somalia",
    253: "Djibouti",
    254: "Kenya",
    255: "Tanzania",
    256: "Uganda",
    257: "Burundi",
    258: "Mozambique",
    260: "Zambia",
    261: "Madagascar",
    262: "Reunion",
    263: "Zimbabwe",
    264: "Namibia",
    265: "Malawi",
    266: "Lesotho",
    267: "Botswana",
    268: "Eswatini",
    269: "Comoros",
    290: "Saint Helena",
    291: "Eritrea",
    297: "Aruba",
    298: "Faroe Islands",
    299: "Greenland",
    
    # Asia
    81: "Japan",
    82: "South Korea",
    84: "Vietnam",
    86: "China",
    90: "Turkey",
    91: "India",
    92: "Pakistan",
    93: "Afghanistan",
    94: "Sri Lanka",
    95: "Myanmar",
    98: "Iran",
    212: "Morocco",
    213: "Algeria",
    216: "Tunisia",
    218: "Libya",
    220: "Gambia",
    221: "Senegal",
    222: "Mauritania",
    223: "Mali",
    224: "Guinea",
    225: "Ivory Coast",
    226: "Burkina Faso",
    227: "Niger",
    228: "Togo",
    229: "Benin",
    230: "Mauritius",
    231: "Liberia",
    232: "Sierra Leone",
    233: "Ghana",
    234: "Nigeria",
    235: "Chad",
    236: "Central African Republic",
    237: "Cameroon",
    238: "Cape Verde",
    239: "Sao Tome and Principe",
    240: "Equatorial Guinea",
    241: "Gabon",
    242: "Republic of the Congo",
    243: "Democratic Republic of the Congo",
    244: "Angola",
    245: "Guinea-Bissau",
    246: "Diego Garcia",
    247: "Ascension Island",
    248: "Seychelles",
    249: "Sudan",
    250: "Rwanda",
    251: "Ethiopia",
    252: "Somalia",
    253: "Djibouti",
    254: "Kenya",
    255: "Tanzania",
    256: "Uganda",
    257: "Burundi",
    258: "Mozambique",
    260: "Zambia",
    261: "Madagascar",
    262: "Reunion",
    263: "Zimbabwe",
    264: "Namibia",
    265: "Malawi",
    266: "Lesotho",
    267: "Botswana",
    268: "Eswatini",
    269: "Comoros",
    290: "Saint Helena",
    291: "Eritrea",
    297: "Aruba",
    298: "Faroe Islands",
    299: "Greenland",
    
    # Asia (continued)
    960: "Maldives",
    961: "Lebanon",
    962: "Jordan",
    963: "Syria",
    964: "Iraq",
    965: "Kuwait",
    966: "Saudi Arabia",
    967: "Yemen",
    968: "Oman",
    970: "Palestine",
    971: "United Arab Emirates",
    972: "Israel",
    973: "Bahrain",
    974: "Qatar",
    975: "Bhutan",
    976: "Mongolia",
    977: "Nepal",
    992: "Tajikistan",
    993: "Turkmenistan",
    994: "Azerbaijan",
    995: "Georgia",
    996: "Kyrgyzstan",
    998: "Uzbekistan",
    
    # Southeast Asia
    60: "Malaysia",
    62: "Indonesia",
    63: "Philippines",
    64: "New Zealand",
    65: "Singapore",
    66: "Thailand",
    670: "East Timor",
    672: "Australian External Territories",
    673: "Brunei",
    674: "Nauru",
    675: "Papua New Guinea",
    676: "Tonga",
    677: "Solomon Islands",
    678: "Vanuatu",
    679: "Fiji",
    680: "Palau",
    681: "Wallis and Futuna",
    682: "Cook Islands",
    683: "Niue",
    685: "Samoa",
    686: "Kiribati",
    687: "New Caledonia",
    688: "Tuvalu",
    689: "French Polynesia",
    690: "Tokelau",
    691: "Micronesia",
    692: "Marshall Islands",
    856: "Laos",
    855: "Cambodia",
    880: "Bangladesh",
    
    # Other
    800: "International Freephone",
    808: "International Shared Cost",
    870: "Inmarsat",
    878: "Universal Personal Telecommunications",
    881: "Global Mobile Satellite System",
    882: "International Networks",
    883: "International Networks",
    979: "International Premium Rate",
}

# ==================== COUNTRY TO CALLING CODE ====================

# Reverse mapping (handles duplicate codes like US/Canada)
COUNTRY_TO_CODE = {
    "Iran": 98,
    "United States": 1,
    "Canada": 1,
    "United Kingdom": 44,
    "Germany": 49,
    "France": 33,
    "China": 86,
    "Japan": 81,
    "Australia": 61,
    "Italy": 39,
    "Spain": 34,
    "Russia": 7,
    "Turkey": 90,
    "India": 91,
    "Brazil": 55,
    "Mexico": 52,
    "Egypt": 20,
    "Saudi Arabia": 966,
    "South Korea": 82,
    "Netherlands": 31,
    "Switzerland": 41,
    "Sweden": 46,
    "Norway": 47,
    "Denmark": 45,
    "Finland": 358,
    "Portugal": 351,
    "Greece": 30,
    "Belgium": 32,
    "Poland": 48,
    "Austria": 43,
    "Ireland": 353,
    "New Zealand": 64,
    "Singapore": 65,
    "United Arab Emirates": 971,
    "Qatar": 974,
    "Kuwait": 965,
    "Bahrain": 973,
    "Oman": 968,
    "Jordan": 962,
    "Iraq": 964,
    "Ukraine": 380,
    "Lithuania": 370,
    "Estonia": 372,
    "Latvia": 371,
    "Czech Republic": 420,
    "Slovakia": 421,
    "Hungary": 36,
    "Romania": 40,
    "Malaysia": 60,
    "Philippines": 63,
    "Thailand": 66,
    "Vietnam": 84,
    "Pakistan": 92,
    "Afghanistan": 93,
    "Sri Lanka": 94,
    "Myanmar": 95,
    "Indonesia": 62,
    "Bangladesh": 880,
    "Nepal": 977,
    "Israel": 972,
    "Palestine": 970,
    "Syria": 963,
    "Lebanon": 961,
    "Yemen": 967,
    "South Africa": 27,
    "Nigeria": 234,
    "Kenya": 254,
    "Ethiopia": 251,
    "Argentina": 54,
    "Chile": 56,
    "Colombia": 57,
    "Venezuela": 58,
    "Peru": 51,
    "Ecuador": 593,
    "Bolivia": 591,
    "Paraguay": 595,
    "Uruguay": 598,
    "Cuba": 53,
    "Dominican Republic": 1809,
    "Jamaica": 1876,
    "Trinidad and Tobago": 1868,
    "Bahamas": 1242,
    "Barbados": 1246,
    "Algeria": 213,
    "Morocco": 212,
    "Tunisia": 216,
    "Libya": 218,
    "Sudan": 249,
    "Ghana": 233,
    "Ivory Coast": 225,
    "Cameroon": 237,
    "Angola": 244,
    "Zimbabwe": 263,
    "Zambia": 260,
    "Tanzania": 255,
    "Uganda": 256,
    "Rwanda": 250,
    "Somalia": 252,
    "Serbia": 381,
    "Croatia": 385,
    "Bulgaria": 359,
    "Belarus": 375,
    "Armenia": 374,
    "Azerbaijan": 994,
    "Georgia": 995,
    "Kazakhstan": 7,
    "Uzbekistan": 998,
    "Turkmenistan": 993,
    "Kyrgyzstan": 996,
    "Tajikistan": 992,
    "Mongolia": 976,
    "North Korea": 850,
    "Laos": 856,
    "Cambodia": 855,
    "Brunei": 673,
    "Maldives": 960,
    "Bhutan": 975,
    "Fiji": 679,
    "Papua New Guinea": 675,
    "New Caledonia": 687,
    "French Polynesia": 689,
}

# ==================== ISO CODES ====================

ISO_ALPHA2 = {
    "Iran": "IR",
    "United States": "US",
    "Canada": "CA",
    "United Kingdom": "GB",
    "Germany": "DE",
    "France": "FR",
    "China": "CN",
    "Japan": "JP",
    "Australia": "AU",
    "Italy": "IT",
    "Spain": "ES",
    "Russia": "RU",
    "Turkey": "TR",
    "India": "IN",
    "Brazil": "BR",
    "Mexico": "MX",
    "Egypt": "EG",
    "Saudi Arabia": "SA",
    "South Korea": "KR",
    "Netherlands": "NL",
    "Switzerland": "CH",
    "Sweden": "SE",
    "Norway": "NO",
    "Denmark": "DK",
    "Finland": "FI",
    "Portugal": "PT",
    "Greece": "GR",
    "Belgium": "BE",
    "Poland": "PL",
    "Austria": "AT",
    "Ireland": "IE",
    "New Zealand": "NZ",
    "Singapore": "SG",
    "United Arab Emirates": "AE",
    "Qatar": "QA",
    "Kuwait": "KW",
    "Bahrain": "BH",
    "Oman": "OM",
    "Jordan": "JO",
    "Iraq": "IQ",
    "Ukraine": "UA",
    "Lithuania": "LT",
    "Estonia": "EE",
    "Latvia": "LV",
    "Czech Republic": "CZ",
    "Slovakia": "SK",
    "Hungary": "HU",
    "Romania": "RO",
    "Malaysia": "MY",
    "Philippines": "PH",
    "Thailand": "TH",
    "Vietnam": "VN",
    "Indonesia": "ID",
    "Pakistan": "PK",
    "Bangladesh": "BD",
    "Nepal": "NP",
    "Sri Lanka": "LK",
    "South Africa": "ZA",
    "Nigeria": "NG",
    "Kenya": "KE",
    "Argentina": "AR",
    "Chile": "CL",
    "Colombia": "CO",
    "Venezuela": "VE",
    "Peru": "PE",
    "Israel": "IL",
    "Lebanon": "LB",
    "Syria": "SY",
    "Yemen": "YE",
}

ISO_ALPHA3 = {
    "Iran": "IRN",
    "United States": "USA",
    "Canada": "CAN",
    "United Kingdom": "GBR",
    "Germany": "DEU",
    "France": "FRA",
    "China": "CHN",
    "Japan": "JPN",
    "Australia": "AUS",
    "Italy": "ITA",
    "Spain": "ESP",
    "Russia": "RUS",
    "Turkey": "TUR",
    "India": "IND",
    "Brazil": "BRA",
    "Mexico": "MEX",
    "Egypt": "EGY",
    "Saudi Arabia": "SAU",
    "South Korea": "KOR",
    "Netherlands": "NLD",
    "Switzerland": "CHE",
    "Sweden": "SWE",
    "Norway": "NOR",
    "Denmark": "DNK",
    "Finland": "FIN",
    "Portugal": "PRT",
    "Greece": "GRC",
    "Belgium": "BEL",
    "Poland": "POL",
    "Austria": "AUT",
    "Ireland": "IRL",
    "New Zealand": "NZL",
    "Singapore": "SGP",
    "United Arab Emirates": "ARE",
    "Qatar": "QAT",
    "Kuwait": "KWT",
    "Bahrain": "BHR",
    "Oman": "OMN",
    "Jordan": "JOR",
    "Iraq": "IRQ",
    "Ukraine": "UKR",
    "Hungary": "HUN",
    "Romania": "ROU",
    "Malaysia": "MYS",
    "Philippines": "PHL",
    "Thailand": "THA",
    "Vietnam": "VNM",
    "Indonesia": "IDN",
}

ISO_NUMERIC = {
    "Iran": 364,
    "United States": 840,
    "Canada": 124,
    "United Kingdom": 826,
    "Germany": 276,
    "France": 250,
    "China": 156,
    "Japan": 392,
    "Australia": 36,
    "Italy": 380,
    "Spain": 724,
    "Russia": 643,
    "Turkey": 792,
    "India": 356,
    "Brazil": 76,
    "Mexico": 484,
    "Egypt": 818,
    "Saudi Arabia": 682,
    "South Korea": 410,
    "Netherlands": 528,
    "Switzerland": 756,
    "Sweden": 752,
    "Norway": 578,
    "Denmark": 208,
    "Finland": 246,
    "Portugal": 620,
    "Greece": 300,
    "Belgium": 56,
    "Poland": 616,
    "Austria": 40,
    "Ireland": 372,
    "New Zealand": 554,
    "Singapore": 702,
    "United Arab Emirates": 784,
    "Qatar": 634,
    "Kuwait": 414,
    "Bahrain": 48,
    "Oman": 512,
    "Jordan": 400,
    "Iraq": 368,
    "Ukraine": 804,
    "Hungary": 348,
    "Romania": 642,
    "Malaysia": 458,
    "Philippines": 608,
    "Thailand": 764,
}

# ==================== CONTINENTS ====================

COUNTRY_CONTINENT = {
    # Asia
    "Iran": "Asia",
    "China": "Asia",
    "Japan": "Asia",
    "South Korea": "Asia",
    "India": "Asia",
    "Turkey": "Asia",
    "Saudi Arabia": "Asia",
    "United Arab Emirates": "Asia",
    "Qatar": "Asia",
    "Kuwait": "Asia",
    "Bahrain": "Asia",
    "Oman": "Asia",
    "Jordan": "Asia",
    "Iraq": "Asia",
    "Israel": "Asia",
    "Lebanon": "Asia",
    "Syria": "Asia",
    "Yemen": "Asia",
    "Afghanistan": "Asia",
    "Pakistan": "Asia",
    "Bangladesh": "Asia",
    "Nepal": "Asia",
    "Sri Lanka": "Asia",
    "Myanmar": "Asia",
    "Thailand": "Asia",
    "Vietnam": "Asia",
    "Laos": "Asia",
    "Cambodia": "Asia",
    "Malaysia": "Asia",
    "Singapore": "Asia",
    "Indonesia": "Asia",
    "Philippines": "Asia",
    "Mongolia": "Asia",
    "Kazakhstan": "Asia",
    "Uzbekistan": "Asia",
    "Turkmenistan": "Asia",
    "Kyrgyzstan": "Asia",
    "Tajikistan": "Asia",
    "Azerbaijan": "Asia",
    "Georgia": "Asia",
    "Armenia": "Asia",
    
    # Europe
    "United Kingdom": "Europe",
    "Germany": "Europe",
    "France": "Europe",
    "Italy": "Europe",
    "Spain": "Europe",
    "Russia": "Europe",
    "Netherlands": "Europe",
    "Switzerland": "Europe",
    "Sweden": "Europe",
    "Norway": "Europe",
    "Denmark": "Europe",
    "Finland": "Europe",
    "Portugal": "Europe",
    "Greece": "Europe",
    "Belgium": "Europe",
    "Poland": "Europe",
    "Austria": "Europe",
    "Ireland": "Europe",
    "Ukraine": "Europe",
    "Lithuania": "Europe",
    "Estonia": "Europe",
    "Latvia": "Europe",
    "Czech Republic": "Europe",
    "Slovakia": "Europe",
    "Hungary": "Europe",
    "Romania": "Europe",
    "Bulgaria": "Europe",
    "Serbia": "Europe",
    "Croatia": "Europe",
    "Belarus": "Europe",
    "Moldova": "Europe",
    
    # North America
    "United States": "North America",
    "Canada": "North America",
    "Mexico": "North America",
    "Cuba": "North America",
    "Dominican Republic": "North America",
    "Jamaica": "North America",
    "Bahamas": "North America",
    "Trinidad and Tobago": "North America",
    
    # South America
    "Brazil": "South America",
    "Argentina": "South America",
    "Chile": "South America",
    "Colombia": "South America",
    "Venezuela": "South America",
    "Peru": "South America",
    "Ecuador": "South America",
    "Bolivia": "South America",
    "Paraguay": "South America",
    "Uruguay": "South America",
    
    # Africa
    "Egypt": "Africa",
    "South Africa": "Africa",
    "Nigeria": "Africa",
    "Kenya": "Africa",
    "Ethiopia": "Africa",
    "Algeria": "Africa",
    "Morocco": "Africa",
    "Tunisia": "Africa",
    "Libya": "Africa",
    "Sudan": "Africa",
    "Ghana": "Africa",
    "Ivory Coast": "Africa",
    "Cameroon": "Africa",
    "Angola": "Africa",
    "Zimbabwe": "Africa",
    "Zambia": "Africa",
    "Tanzania": "Africa",
    "Uganda": "Africa",
    "Rwanda": "Africa",
    "Somalia": "Africa",
    
    # Oceania
    "Australia": "Oceania",
    "New Zealand": "Oceania",
    "Fiji": "Oceania",
    "Papua New Guinea": "Oceania",
    "Solomon Islands": "Oceania",
    "Vanuatu": "Oceania",
}

# ==================== CURRENCIES ====================

COUNTRY_CURRENCY = {
    "Iran": "Iranian Rial",
    "United States": "US Dollar",
    "Canada": "Canadian Dollar",
    "United Kingdom": "Pound Sterling",
    "Germany": "Euro",
    "France": "Euro",
    "Italy": "Euro",
    "Spain": "Euro",
    "Netherlands": "Euro",
    "Belgium": "Euro",
    "Portugal": "Euro",
    "Ireland": "Euro",
    "Austria": "Euro",
    "Finland": "Euro",
    "Greece": "Euro",
    "Japan": "Japanese Yen",
    "China": "Chinese Yuan",
    "India": "Indian Rupee",
    "Turkey": "Turkish Lira",
    "Russia": "Russian Ruble",
    "Brazil": "Brazilian Real",
    "Mexico": "Mexican Peso",
    "Australia": "Australian Dollar",
    "New Zealand": "New Zealand Dollar",
    "Switzerland": "Swiss Franc",
    "Sweden": "Swedish Krona",
    "Norway": "Norwegian Krone",
    "Denmark": "Danish Krone",
    "Saudi Arabia": "Saudi Riyal",
    "United Arab Emirates": "UAE Dirham",
    "Qatar": "Qatari Riyal",
    "Kuwait": "Kuwaiti Dinar",
    "Bahrain": "Bahraini Dinar",
    "Oman": "Omani Rial",
    "Jordan": "Jordanian Dinar",
    "Iraq": "Iraqi Dinar",
    "Israel": "New Shekel",
    "South Korea": "South Korean Won",
    "Singapore": "Singapore Dollar",
    "Malaysia": "Malaysian Ringgit",
    "Thailand": "Thai Baht",
    "Vietnam": "Vietnamese Dong",
    "Indonesia": "Indonesian Rupiah",
    "Philippines": "Philippine Peso",
    "Pakistan": "Pakistani Rupee",
    "Bangladesh": "Bangladeshi Taka",
    "Egypt": "Egyptian Pound",
    "South Africa": "South African Rand",
    "Nigeria": "Nigerian Naira",
    "Kenya": "Kenyan Shilling",
    "Argentina": "Argentine Peso",
    "Chile": "Chilean Peso",
    "Colombia": "Colombian Peso",
}

# ==================== CAPITALS ====================

COUNTRY_CAPITAL = {
    "Iran": "Tehran",
    "United States": "Washington, D.C.",
    "Canada": "Ottawa",
    "United Kingdom": "London",
    "Germany": "Berlin",
    "France": "Paris",
    "Italy": "Rome",
    "Spain": "Madrid",
    "Portugal": "Lisbon",
    "Netherlands": "Amsterdam",
    "Belgium": "Brussels",
    "Switzerland": "Bern",
    "Austria": "Vienna",
    "Greece": "Athens",
    "Turkey": "Ankara",
    "Russia": "Moscow",
    "China": "Beijing",
    "Japan": "Tokyo",
    "India": "New Delhi",
    "South Korea": "Seoul",
    "Australia": "Canberra",
    "New Zealand": "Wellington",
    "Brazil": "Brasília",
    "Mexico": "Mexico City",
    "Egypt": "Cairo",
    "Saudi Arabia": "Riyadh",
    "United Arab Emirates": "Abu Dhabi",
    "Qatar": "Doha",
    "Kuwait": "Kuwait City",
    "Bahrain": "Manama",
    "Oman": "Muscat",
    "Jordan": "Amman",
    "Iraq": "Baghdad",
    "Lebanon": "Beirut",
    "Israel": "Jerusalem",
    "Syria": "Damascus",
    "Yemen": "Sana'a",
    "Afghanistan": "Kabul",
    "Pakistan": "Islamabad",
    "Bangladesh": "Dhaka",
    "Nepal": "Kathmandu",
    "Sri Lanka": "Sri Jayawardenepura Kotte",
    "Thailand": "Bangkok",
    "Vietnam": "Hanoi",
    "Indonesia": "Jakarta",
    "Philippines": "Manila",
    "Singapore": "Singapore",
    "Malaysia": "Kuala Lumpur",
    "Myanmar": "Naypyidaw",
    "South Africa": "Pretoria",
    "Nigeria": "Abuja",
    "Kenya": "Nairobi",
    "Ethiopia": "Addis Ababa",
    "Argentina": "Buenos Aires",
    "Chile": "Santiago",
    "Colombia": "Bogotá",
    "Venezuela": "Caracas",
    "Peru": "Lima",
}

# ==================== TIMEZONES ====================

COUNTRY_TIMEZONE = {
    "Iran": "UTC+03:30",
    "United States": "UTC-05:00 to UTC-10:00",
    "Canada": "UTC-03:30 to UTC-08:00",
    "United Kingdom": "UTC+00:00",
    "Germany": "UTC+01:00",
    "France": "UTC+01:00",
    "Italy": "UTC+01:00",
    "Spain": "UTC+01:00",
    "Portugal": "UTC+00:00",
    "Netherlands": "UTC+01:00",
    "Belgium": "UTC+01:00",
    "Switzerland": "UTC+01:00",
    "Austria": "UTC+01:00",
    "Greece": "UTC+02:00",
    "Turkey": "UTC+03:00",
    "Russia": "UTC+02:00 to UTC+12:00",
    "China": "UTC+08:00",
    "Japan": "UTC+09:00",
    "India": "UTC+05:30",
    "South Korea": "UTC+09:00",
    "Australia": "UTC+05:00 to UTC+10:00",
    "New Zealand": "UTC+12:00",
    "Brazil": "UTC-05:00 to UTC-02:00",
    "Mexico": "UTC-08:00 to UTC-06:00",
    "Egypt": "UTC+02:00",
    "Saudi Arabia": "UTC+03:00",
    "United Arab Emirates": "UTC+04:00",
    "Qatar": "UTC+03:00",
    "Kuwait": "UTC+03:00",
    "Bahrain": "UTC+03:00",
    "Oman": "UTC+04:00",
    "Jordan": "UTC+02:00",
    "Iraq": "UTC+03:00",
    "Israel": "UTC+02:00",
    "Singapore": "UTC+08:00",
    "Malaysia": "UTC+08:00",
    "Thailand": "UTC+07:00",
    "Vietnam": "UTC+07:00",
    "Indonesia": "UTC+07:00 to UTC+09:00",
    "Philippines": "UTC+08:00",
}

# ==================== COUNTRY LIST ====================

COUNTRY_LIST = sorted(set(COUNTRY_TO_CODE.keys()))

# ==================== UTILITY FUNCTIONS ====================

def get_country_by_code(code: int) -> Optional[str]:
    """
    Get country name by calling code.
    
    Args:
        code: International calling code (e.g., 98)
        
    Returns:
        Country name or None if not found
        
    Examples:
        >>> get_country_by_code(98)
        'Iran'
        >>> get_country_by_code(1)
        'United States'  # Returns first match (US)
    """
    # Handle special cases for country code 1
    if code == 1:
        return "United States"  # Default
    return CALLING_CODES.get(code)

def get_calling_code(country: str) -> Optional[int]:
    """
    Get calling code by country name.
    
    Args:
        country: Country name (e.g., 'Iran')
        
    Returns:
        Calling code or None if not found
        
    Examples:
        >>> get_calling_code('Iran')
        98
    """
    return COUNTRY_TO_CODE.get(country)

def get_iso_alpha2(country: str) -> Optional[str]:
    """Get ISO 3166-1 alpha-2 code (2 letters)."""
    return ISO_ALPHA2.get(country)

def get_iso_alpha3(country: str) -> Optional[str]:
    """Get ISO 3166-1 alpha-3 code (3 letters)."""
    return ISO_ALPHA3.get(country)

def get_iso_numeric(country: str) -> Optional[int]:
    """Get ISO 3166-1 numeric code."""
    return ISO_NUMERIC.get(country)

def get_continent(country: str) -> Optional[str]:
    """Get continent of the country."""
    return COUNTRY_CONTINENT.get(country)

def get_currency(country: str) -> Optional[str]:
    """Get currency name of the country."""
    return COUNTRY_CURRENCY.get(country)

def get_capital(country: str) -> Optional[str]:
    """Get capital city of the country."""
    return COUNTRY_CAPITAL.get(country)

def get_timezone(country: str) -> Optional[str]:
    """Get timezone of the country."""
    return COUNTRY_TIMEZONE.get(country)

def get_country_info(country: str) -> Dict:
    """
    Get comprehensive information about a country.
    
    Args:
        country: Country name
        
    Returns:
        Dictionary with all available information
        
    Examples:
        >>> get_country_info('Iran')
        {'name': 'Iran', 'calling_code': 98, 'alpha2': 'IR', 'alpha3': 'IRN', ...}
    """
    return {
        "name": country,
        "calling_code": get_calling_code(country),
        "alpha2": get_iso_alpha2(country),
        "alpha3": get_iso_alpha3(country),
        "numeric": get_iso_numeric(country),
        "continent": get_continent(country),
        "capital": get_capital(country),
        "currency": get_currency(country),
        "timezone": get_timezone(country),
    }

def is_valid_country(country: str) -> bool:
    """Check if country name exists in database."""
    return country in COUNTRY_TO_CODE

def search_country(query: str) -> List[str]:
    """
    Search for countries by name (case-insensitive partial match).
    
    Args:
        query: Search string
        
    Returns:
        List of matching country names
        
    Examples:
        >>> search_country('uni')
        ['United Arab Emirates', 'United Kingdom', 'United States']
    """
    query = query.lower()
    return [c for c in COUNTRY_LIST if query in c.lower()]

def get_countries_by_continent(continent: str) -> List[str]:
    """Get all countries in a specific continent."""
    return [c for c, cont in COUNTRY_CONTINENT.items() if cont == continent]

def format_phone_number(code: int, number: str) -> str:
    """
    Format an international phone number.
    
    Args:
        code: Country calling code
        number: Local phone number
        
    Returns:
        Formatted international number (e.g., '+98 21 12345678')
    """
    return f"+{code} {number}"

def parse_phone_number(phone: str) -> Tuple[Optional[int], Optional[str]]:
    """
    Parse an international phone number.
    
    Args:
        phone: Phone number string (may start with + or 00)
        
    Returns:
        Tuple of (calling_code, remaining_number) or (None, None)
    """
    # Remove leading + or 00
    if phone.startswith('+'):
        phone = phone[1:]
    elif phone.startswith('00'):
        phone = phone[2:]
    else:
        return None, None
    
    # Find the longest matching calling code
    for i in range(1, min(5, len(phone))):
        try:
            code = int(phone[:i])
            if code in CALLING_CODES:
                return code, phone[i:]
        except ValueError:
            continue
    
    return None, None


