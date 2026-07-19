"""
Module: Character Classification & Language Sets
Description: Defines comprehensive character sets for classification (ctype-style),
             including whitespace, punctuation, digits, and multiple language alphabets.
             Supports Persian, Arabic, English, German, French, Russian, Chinese, Japanese,
             Korean, Turkish, Urdu, Hindi, Spanish, Italian, and more.
Author: Assistant
License: MIT

Usage:
    from char_classifier import *
    
    # Check character types
    is_digit('5') -> True
    char_type('ا') -> 'persian'
    
    # Get language of a string
    detect_language("Hello") -> 'english'
    
    # Filter by language
    filter_by_lang("Hello سلام", "persian") -> "سلام"
"""

import re
import unicodedata

# ==================== BASIC CHARACTER SETS ====================

# Whitespace characters (all Unicode whitespace)
WHITESPACE = '\t\n\r\v\f\x0c\x1c\x1d\x1e\x1f\x85\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a\u2028\u2029\u205f\u3000'
WHITESPACE_STANDARD = '\t\n\r\v\f'
WHITESPACE_LIST = list(WHITESPACE_STANDARD)

# Punctuation (ASCII + common Unicode)
PUNCTUATION_ASCII = r'''!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~'''
PUNCTUATION_UNICODE = '«»“”‘’‒–—―… ′″‹›¡¿‽※' + PUNCTUATION_ASCII
PUNCTUATION = PUNCTUATION_UNICODE
PUNCTUATION_LIST = list(PUNCTUATION)

# ==================== NUMERIC SYSTEMS ====================

# Binary
BINARY_DIGITS = '01'
BINARY_LIST = ['0', '1']

# Octal
OCTAL_DIGITS = '01234567'
OCTAL_LIST = list(OCTAL_DIGITS)

# Decimal (ASCII)
DECIMAL_DIGITS = '0123456789'
DECIMAL_LIST = list(DECIMAL_DIGITS)

# Hexadecimal
HEX_DIGITS = DECIMAL_DIGITS + 'abcdefABCDEF'
HEX_LIST = list(HEX_DIGITS)

# Persian/Arabic-Indic digits (۰۱۲۳۴۵۶۷۸۹)
PERSIAN_DIGITS = '۰۱۲۳۴۵۶۷۸۹'
PERSIAN_DIGITS_MAP = {p: d for p, d in zip(PERSIAN_DIGITS, DECIMAL_DIGITS)}

# Eastern Arabic digits (same as Persian)
EASTERN_ARABIC_DIGITS = PERSIAN_DIGITS

# Devanagari digits (०१२३४५६७८९) - Hindi/Marathi/Nepali
DEVANAGARI_DIGITS = '०१२३४५६७८९'

# Bengali digits (০১২৩৪৫৬৭৮৯)
BENGALI_DIGITS = '০১২৩৪৫৬৭৮৯'

# Thai digits (๐๑๒๓๔๕๖๗๘๙)
THAI_DIGITS = '๐๑๒๓๔๕๖๗๘๙'

ALL_DIGITS = DECIMAL_DIGITS + PERSIAN_DIGITS + DEVANAGARI_DIGITS + BENGALI_DIGITS + THAI_DIGITS

# ==================== LATIN ALPHABETS ====================

# Basic English
ASCII_LOWERCASE = 'abcdefghijklmnopqrstuvwxyz'
ASCII_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ASCII_LETTERS = ASCII_LOWERCASE + ASCII_UPPERCASE
ASCII_LOWERCASE_LIST = list(ASCII_LOWERCASE)
ASCII_UPPERCASE_LIST = list(ASCII_UPPERCASE)

# German (Deutsch)
GERMAN_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzäöüß'
GERMAN_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ'
GERMAN_LETTERS = GERMAN_LOWERCASE + GERMAN_UPPERCASE

# French (Français)
FRENCH_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzàâæçéèêëîïôœùûüÿ'
FRENCH_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÂÆÇÉÈÊËÎÏÔŒÙÛÜŸ'
FRENCH_LETTERS = FRENCH_LOWERCASE + FRENCH_UPPERCASE

# Spanish (Español)
SPANISH_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzáéíñóúü'
SPANISH_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÑÓÚÜ'
SPANISH_LETTERS = SPANISH_LOWERCASE + SPANISH_UPPERCASE

# Italian (Italiano)
ITALIAN_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzàáèéìíîòóùú'
ITALIAN_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÁÈÉÌÍÎÒÓÙÚ'
ITALIAN_LETTERS = ITALIAN_LOWERCASE + ITALIAN_UPPERCASE

# Portuguese (Português)
PORTUGUESE_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzàáâãçéêíóôõúü'
PORTUGUESE_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÁÂÃÇÉÊÍÓÔÕÚÜ'
PORTUGUESE_LETTERS = PORTUGUESE_LOWERCASE + PORTUGUESE_UPPERCASE

# Dutch (Nederlands)
DUTCH_LETTERS = ASCII_LETTERS + 'äëïöüÿáéíóú'  # Simplified

# ==================== CYRILLIC ALPHABETS ====================

# Russian (Русский)
RUSSIAN_LOWERCASE = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
RUSSIAN_UPPERCASE = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
RUSSIAN_LETTERS = RUSSIAN_LOWERCASE + RUSSIAN_UPPERCASE

# Ukrainian (Українська)
UKRAINIAN_LOWERCASE = 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'
UKRAINIAN_UPPERCASE = 'АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ'
UKRAINIAN_LETTERS = UKRAINIAN_LOWERCASE + UKRAINIAN_UPPERCASE

# Bulgarian (Български) - same as Russian without Ё, Ы, Э
BULGARIAN_LETTERS = RUSSIAN_LETTERS.replace('Ё', '').replace('ё', '').replace('Ы', '').replace('ы', '').replace('Э', '').replace('э', '')

# Serbian (Српски) - Latin + Cyrillic
SERBIAN_CYRILLIC_LOWERCASE = 'абвгдђежзијклљмнњопрстћуфхцчџш'
SERBIAN_CYRILLIC_UPPERCASE = 'АБВГДЂЕЖЗИЈКЛЉМНЊОПРСТЋУФХЦЧЏШ'
SERBIAN_CYRILLIC = SERBIAN_CYRILLIC_LOWERCASE + SERBIAN_CYRILLIC_UPPERCASE

# ==================== MIDDLE EASTERN SCRIPTS ====================

# Persian (فارسی) - Complete with all letters
PERSIAN_LETTERS = "آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی"
PERSIAN_LETTERS_LIST = list(PERSIAN_LETTERS)

# Arabic (العربية)
ARABIC_LETTERS = "ءآأؤإئابةتثجحخدذرزسشصضطظعغفقكلمنهويى"
ARABIC_LETTERS_LIST = list(ARABIC_LETTERS)

# Urdu (اردو) - Persian/Arabic + additional letters
URDU_LETTERS = PERSIAN_LETTERS + "ٹڈڑھے"  # Additional Urdu-specific letters
URDU_LETTERS_LIST = list(set(URDU_LETTERS))

# Kurdish (Kurdî) - Arabic script + Latin
KURDISH_ARABIC = PERSIAN_LETTERS + "ڤڕڵگ"  # Kurdish-specific letters in Arabic script

# Pashto (پښتو)
PASHTO_LETTERS = PERSIAN_LETTERS + "ځڅډړږښڼګڵګ"  # Pashto-specific letters

# ==================== SOUTH ASIAN SCRIPTS ====================

# Devanagari (देवनागरी) - Hindi, Marathi, Nepali, Sanskrit
DEVANAGARI_LETTERS = "अआइईउऊऋएऐओऔकखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसहक्षत्रज्ञ"
DEVANAGARI_LETTERS_LIST = list(DEVANAGARI_LETTERS)

# Bengali (বাংলা)
BENGALI_LETTERS = "অআইঈউঊঋএঐওঔকখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহড়ঢ়য়ৎ"
BENGALI_LETTERS_LIST = list(BENGALI_LETTERS)

# Gurmukhi (ਗੁਰਮੁਖੀ) - Punjabi
GURMUKHI_LETTERS = "ਅਆਇਈਉਊਏਐਓਔਕਖਗਘਙਚਛਜਝਞਟਠਡਢਣਤਥਦਧਨਪਫਬਭਮਯਰਲਵਸਹ"

# Tamil (தமிழ்)
TAMIL_LETTERS = "அஆஇஈஉஊஎஏஐஒஓஔகஙசஜஞடணதநனபமயரலளவழற"

# Telugu (తెలుగు)
TELUGU_LETTERS = "అఆఇఈఉఊఋఎఏఐఒఓఔకఖగఘఙచఛజఝఞటఠడఢణతథదధనపఫబభమయరఱలళవశషసహ"

# ==================== EAST ASIAN SCRIPTS ====================

# Chinese (中文) - Common characters (CJK Unified Ideographs)
# This is a small subset. Complete set has over 20,000 characters
CHINESE_COMMON = "的一是不了人我在有他这中大来上国个到说们为子和你地出道也时年得就那要下以生会自着去之过家学对可里后小"
CHINESE_LETTERS_LIST = list(CHINESE_COMMON)

# Japanese (日本語) - Hiragana + Katakana + Common Kanji
HIRAGANA = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽっぁぃぅぇぉゃゅょゎ"
KATAKANA = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポッァィゥェォャュョヮ"
JAPANESE_COMMON_KANJI = "日本人年月大小山川田目上下左右東西南北出入学先生社員会社長話語"
JAPANESE_LETTERS = HIRAGANA + KATAKANA + JAPANESE_COMMON_KANJI

# Korean (한국어) - Hangul Syllables (basic jamo)
HANGUL_JAMO = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ"
HANGUL_LETTERS = HANGUL_JAMO

# Thai (ไทย)
THAI_LETTERS = "กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรฤลวศษสหฬอฮ"

# ==================== OTHER SCRIPTS ====================

# Greek (Ελληνικά)
GREEK_LOWERCASE = "αβγδεζηθικλμνξοπρστυφχψω"
GREEK_UPPERCASE = "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ"
GREEK_LETTERS = GREEK_LOWERCASE + GREEK_UPPERCASE

# Hebrew (עברית)
HEBREW_LETTERS = "אבגדהוזחטיכלמנסעפצקרשת"

# Armenian (Հայերեն)
ARMENIAN_LOWERCASE = "աբգդեզէըթժիլխծկհձղճմյնշոչպջռսվտրցւփքօֆ"
ARMENIAN_UPPERCASE = "ԱԲԳԴԵԶԷԸԹԺԻԼԽԾԿՀՁՂՃՄՅՆՇՈՉՊՋՌՍՎՏՐՑՒՓՔՕՖ"
ARMENIAN_LETTERS = ARMENIAN_LOWERCASE + ARMENIAN_UPPERCASE

# Georgian (ქართული)
GEORGIAN_LETTERS = "აბგდევზთიკლმნოპჟრსტუფქღყშჩცძწჭხჯჰ"

# ==================== PRINTABLE STRINGS ====================

def make_printable(charset: str, include_digits: bool = True, 
                   include_punct: bool = True, include_space: bool = True,
                   include_whitespace: bool = True) -> str:
    """
    Create a printable string from a character set.
    
    Args:
        charset: Base character set (e.g., letters)
        include_digits: Include numeric digits
        include_punct: Include punctuation
        include_space: Include space character
        include_whitespace: Include all whitespace characters
    
    Returns:
        Combined printable string
    """
    result = charset
    if include_digits:
        result += DECIMAL_DIGITS
    if include_punct:
        result += PUNCTUATION
    if include_space:
        result += ' '
    if include_whitespace:
        result += WHITESPACE_STANDARD
    return result

# Common printable sets
PRINTABLE_ASCII = DECIMAL_DIGITS + ASCII_LETTERS + PUNCTUATION_ASCII + WHITESPACE_STANDARD
PRINTABLE_PERSIAN = make_printable(PERSIAN_LETTERS)
PRINTABLE_ARABIC = make_printable(ARABIC_LETTERS)
PRINTABLE_URDU = make_printable(URDU_LETTERS)
PRINTABLE_GERMAN = make_printable(GERMAN_LETTERS)
PRINTABLE_FRENCH = make_printable(FRENCH_LETTERS)
PRINTABLE_SPANISH = make_printable(SPANISH_LETTERS)
PRINTABLE_RUSSIAN = make_printable(RUSSIAN_LETTERS)
PRINTABLE_CHINESE = make_printable(CHINESE_COMMON)
PRINTABLE_JAPANESE = make_printable(JAPANESE_LETTERS)
PRINTABLE_KOREAN = make_printable(HANGUL_LETTERS)
PRINTABLE_GREEK = make_printable(GREEK_LETTERS)
PRINTABLE_HEBREW = make_printable(HEBREW_LETTERS)
PRINTABLE_DEVANAGARI = make_printable(DEVANAGARI_LETTERS)

# Alphanumeric only (no punctuation, no whitespace)
PRINTABLE_ALNUM = DECIMAL_DIGITS + ASCII_LETTERS

# ==================== COMPREHENSIVE SETS ====================

# All letters from all supported languages
ALL_LETTERS = ''.join(set(
    ASCII_LETTERS + GERMAN_LETTERS + FRENCH_LETTERS + SPANISH_LETTERS + ITALIAN_LETTERS +
    RUSSIAN_LETTERS + UKRAINIAN_LETTERS + PERSIAN_LETTERS + ARABIC_LETTERS + URDU_LETTERS +
    DEVANAGARI_LETTERS + BENGALI_LETTERS + GURMUKHI_LETTERS + TAMIL_LETTERS +
    CHINESE_COMMON + JAPANESE_LETTERS + HANGUL_LETTERS + THAI_LETTERS +
    GREEK_LETTERS + HEBREW_LETTERS + ARMENIAN_LETTERS + GEORGIAN_LETTERS
))
ALL_LETTERS_LIST = list(ALL_LETTERS)

# All characters (letters + digits + punctuation + whitespace)
ALL_CHARS = ALL_LETTERS + ALL_DIGITS + PUNCTUATION + WHITESPACE_STANDARD
ALL_CHARS_LIST = list(set(ALL_CHARS))

# ==================== LANGUAGE DETECTION ====================

# Define character ranges for each script (Unicode blocks)
SCRIPT_RANGES = {
    'latin': (('0041', '005A'), ('0061', '007A'), ('00C0', '00FF'), ('0100', '017F')),
    'cyrillic': (('0400', '04FF'),),
    'arabic': (('0600', '06FF'), ('0750', '077F'), ('08A0', '08FF'), ('FB50', 'FDFF'), ('FE70', 'FEFF')),
    'persian': (('0600', '06FF'),),  # Same Unicode block as Arabic
    'hebrew': (('0590', '05FF'),),
    'devanagari': (('0900', '097F'),),
    'bengali': (('0980', '09FF'),),
    'gurmukhi': (('0A00', '0A7F'),),
    'tamil': (('0B80', '0BFF'),),
    'telugu': (('0C00', '0C7F'),),
    'thai': (('0E00', '0E7F'),),
    'greek': (('0370', '03FF'),),
    'armenian': (('0530', '058F'),),
    'georgian': (('10A0', '10FF'),),
    'hangul': (('1100', '11FF'), ('3130', '318F'), ('AC00', 'D7AF')),
    'hiragana': (('3040', '309F'),),
    'katakana': (('30A0', '30FF'),),
    'cjk': (('4E00', '9FFF'), ('3400', '4DBF')),
}

# Language to character set mapping
LANGUAGE_CHARS = {
    'english': ASCII_LETTERS,
    'german': GERMAN_LETTERS,
    'french': FRENCH_LETTERS,
    'spanish': SPANISH_LETTERS,
    'italian': ITALIAN_LETTERS,
    'portuguese': PORTUGUESE_LETTERS,
    'russian': RUSSIAN_LETTERS,
    'ukrainian': UKRAINIAN_LETTERS,
    'persian': PERSIAN_LETTERS,
    'arabic': ARABIC_LETTERS,
    'urdu': URDU_LETTERS,
    'hebrew': HEBREW_LETTERS,
    'greek': GREEK_LETTERS,
    'armenian': ARMENIAN_LETTERS,
    'georgian': GEORGIAN_LETTERS,
    'hindi': DEVANAGARI_LETTERS,
    'bengali': BENGALI_LETTERS,
    'punjabi': GURMUKHI_LETTERS,
    'tamil': TAMIL_LETTERS,
    'telugu': TELUGU_LETTERS,
    'thai': THAI_LETTERS,
    'chinese': CHINESE_COMMON,
    'japanese': JAPANESE_LETTERS,
    'korean': HANGUL_LETTERS,
    'turkish': ASCII_LETTERS + 'çğıöşüÇĞİÖŞÜ',
    'vietnamese': ASCII_LETTERS + 'ăâđêôơưĂÂĐÊÔƠƯ',
    'polish': ASCII_LETTERS + 'ąćęłńóśźżĄĆĘŁŃÓŚŹŻ',
}

# ==================== UTILITY FUNCTIONS ====================

def normalize_digit(char: str) -> str:
    """
    Convert any digit character to ASCII digit.
    
    Args:
        char: A single character
        
    Returns:
        ASCII digit or original character if not a digit
    """
    if char in PERSIAN_DIGITS:
        return PERSIAN_DIGITS_MAP[char]
    if char in DEVANAGARI_DIGITS:
        return DECIMAL_DIGITS[DEVANAGARI_DIGITS.index(char)]
    if char in BENGALI_DIGITS:
        return DECIMAL_DIGITS[BENGALI_DIGITS.index(char)]
    if char in THAI_DIGITS:
        return DECIMAL_DIGITS[THAI_DIGITS.index(char)]
    return char

def normalize_digits(text: str) -> str:
    """Convert all digits in text to ASCII digits."""
    return ''.join(normalize_digit(c) for c in text)

def is_binary(s: str) -> bool:
    """Check if string contains only binary digits (0 and 1)."""
    return all(c in BINARY_DIGITS for c in s)

def is_octal(s: str) -> bool:
    """Check if string contains only octal digits (0-7)."""
    return all(c in OCTAL_DIGITS for c in s)

def is_hex(s: str) -> bool:
    """Check if string contains only hexadecimal digits."""
    return all(c in HEX_DIGITS for c in s)

def is_digit(s: str) -> bool:
    """Check if string contains only ASCII digits."""
    return all(c in DECIMAL_DIGITS for c in s)

def is_digit_any(s: str) -> bool:
    """Check if string contains only digits (any script)."""
    return all(c in ALL_DIGITS for c in s)

def is_ascii(s: str) -> bool:
    """Check if string contains only ASCII characters."""
    return all(ord(c) < 128 for c in s)

def is_persian(s: str) -> bool:
    """Check if string contains only Persian characters, digits, punctuation, and whitespace."""
    return all(c in PRINTABLE_PERSIAN for c in s)

def is_persian_alpha(s: str) -> bool:
    """Check if string contains only Persian letters (no digits or punctuation)."""
    return all(c in PERSIAN_LETTERS for c in s)

def is_arabic(s: str) -> bool:
    """Check if string contains only Arabic characters."""
    return all(c in PRINTABLE_ARABIC for c in s)

def is_english(s: str) -> bool:
    """Check if string contains only English letters (no digits, only letters)."""
    return all(c in ASCII_LETTERS or c == ' ' for c in s)

def is_rtl_char(char: str) -> bool:
    """
    Check if a character is from a Right-to-Left script (Arabic, Persian, Hebrew, Urdu).
    
    Args:
        char: A single character
        
    Returns:
        True if character is RTL, False otherwise
    """
    rtl_scripts = (PERSIAN_LETTERS, ARABIC_LETTERS, URDU_LETTERS, HEBREW_LETTERS)
    return any(char in script for script in rtl_scripts)

def is_ltr_char(char: str) -> bool:
    """Check if a character is from a Left-to-Right script."""
    return not is_rtl_char(char) and char not in WHITESPACE

def char_type(char: str) -> str:
    """
    Determine the type/category of a character.
    
    Args:
        char: A single character
        
    Returns:
        String describing the character type
    """
    if len(char) != 1:
        raise ValueError("Expected a single character")
    
    if char in WHITESPACE_STANDARD:
        return "whitespace"
    if char in PUNCTUATION:
        return "punctuation"
    if char in DECIMAL_DIGITS:
        return "digit_ascii"
    if char in PERSIAN_DIGITS:
        return "digit_persian"
    if char in ALL_DIGITS:
        return "digit_other"
    if char in ASCII_LETTERS:
        return "latin"
    if char in PERSIAN_LETTERS:
        return "persian"
    if char in ARABIC_LETTERS:
        return "arabic"
    if char in RUSSIAN_LETTERS:
        return "cyrillic"
    if char in GREEK_LETTERS:
        return "greek"
    if char in HEBREW_LETTERS:
        return "hebrew"
    if char in DEVANAGARI_LETTERS:
        return "devanagari"
    if char in CHINESE_COMMON or char in JAPANESE_LETTERS:
        return "cjk"
    if char in HANGUL_LETTERS:
        return "hangul"
    if char in THAI_LETTERS:
        return "thai"
    
    return "other"

def detect_language(text: str) -> str:
    """
    Detect the most likely language of a text.
    
    Args:
        text: Input string
        
    Returns:
        Language name or 'unknown'
    """
    if not text:
        return "unknown"
    
    scores = {}
    for lang, charset in LANGUAGE_CHARS.items():
        # Count matching characters
        score = sum(1 for c in text if c in charset)
        if score > 0:
            scores[lang] = score
    
    if not scores:
        return "unknown"
    
    return max(scores, key=scores.get)

def filter_by_language(text: str, language: str) -> str:
    """
    Keep only characters from a specific language.
    
    Args:
        text: Input string
        language: Language name (e.g., 'persian', 'english')
        
    Returns:
        Filtered string containing only characters from that language
    """
    charset = LANGUAGE_CHARS.get(language, '')
    return ''.join(c for c in text if c in charset)

def remove_punctuation(text: str, keep_ascii_only: bool = False) -> str:
    """
    Remove punctuation from text.
    
    Args:
        text: Input string
        keep_ascii_only: If True, only remove ASCII punctuation
        
    Returns:
        Text without punctuation
    """
    punct = PUNCTUATION_ASCII if keep_ascii_only else PUNCTUATION
    return ''.join(c for c in text if c not in punct)

def remove_whitespace(text: str) -> str:
    """Remove all whitespace characters from text."""
    return ''.join(c for c in text if c not in WHITESPACE_STANDARD)

def normalize_whitespace(text: str) -> str:
    """Normalize multiple whitespace characters to single spaces."""
    return re.sub(r'\s+', ' ', text).strip()

def to_ascii_approx(text: str) -> str:
    """
    Convert text to ASCII approximation (simple transliteration).
    
    Args:
        text: Input string with non-ASCII characters
        
    Returns:
        ASCII approximation
    """
    # Common Persian/Arabic to Latin mapping
    mapping = {
        'آ': 'a', 'ا': 'a', 'ب': 'b', 'پ': 'p', 'ت': 't', 'ث': 's',
        'ج': 'j', 'چ': 'ch', 'ح': 'h', 'خ': 'kh', 'د': 'd', 'ذ': 'z',
        'ر': 'r', 'ز': 'z', 'ژ': 'zh', 'س': 's', 'ش': 'sh', 'ص': 's',
        'ض': 'z', 'ط': 't', 'ظ': 'z', 'ع': 'a', 'غ': 'gh', 'ف': 'f',
        'ق': 'gh', 'ک': 'k', 'گ': 'g', 'ل': 'l', 'م': 'm', 'ن': 'n',
        'و': 'v', 'ه': 'h', 'ی': 'y',
        'أ': 'a', 'إ': 'e', 'ة': 'h', 'ى': 'a',
        'ü': 'u', 'ä': 'a', 'ö': 'o', 'ß': 'ss',
        'ç': 'c', 'ğ': 'g', 'ş': 's', 'ı': 'i',
    }
    
    result = []
    for c in text:
        if c in mapping:
            result.append(mapping[c])
        elif ord(c) < 128:
            result.append(c)
        else:
            # Try Unicode normalization
            normalized = unicodedata.normalize('NFKD', c)
            ascii_version = ''.join(ch for ch in normalized if ord(ch) < 128)
            result.append(ascii_version if ascii_version else '?')
    
    return ''.join(result)


