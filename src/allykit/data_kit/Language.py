# ==================== WHITESPACE CHARACTERS ====================
WHITESPACE = '\t\n\r\v\f\x0c\x1c\x1d\x1e\x1f\x85\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a\u2028\u2029\u205f\u3000\u00a0\u1680\u202f'
WHITESPACE_STANDARD = '\t\n\r\v\f '
WHITESPACE_LIST = list(WHITESPACE_STANDARD)
WHITESPACE_EXTRA = '\u200b\u200c\u200d\u200e\u200f\u2060\ufeff'
WHITESPACE_ALL = WHITESPACE + WHITESPACE_EXTRA

# ==================== PUNCTUATION ====================
PUNCTUATION_ASCII = r'''!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~'''
PUNCTUATION_UNICODE = '«»“”‘’‒–—―… ′″‹›¡¿‽※·¨¸ˆˇˉ˘˙˚˛˜˝—―‖‗‘’‚‛“”„‟†‡•‣․‥…‧‰‱′″‴‵‶‷‸‹›‼‾‿⁀⁁⁂⁃⁄⁅⁆⁇⁈⁉⁊⁋⁌⁍⁎⁏⁐⁑⁒⁓⁔⁕⁖⁗⁘⁙⁚⁛⁜⁝⁞'
PUNCTUATION_EXTRA = '❛❜❝❞❟❠❡❢❣❤❥❦❧➔➘➙➚➛➜➝➞➟➠➡➢➣➤➥➦➧➨➩➪➫➬➭➮➯➰➱➲➳➴➵➶➷➸➹➺➻➼➽➾➿'
PUNCTUATION = PUNCTUATION_ASCII + PUNCTUATION_UNICODE + PUNCTUATION_EXTRA
PUNCTUATION_LIST = list(PUNCTUATION)

# ==================== NUMERIC SYSTEMS ====================
BINARY_DIGITS = '01'
OCTAL_DIGITS = '01234567'
DECIMAL_DIGITS = '0123456789'
HEX_DIGITS = DECIMAL_DIGITS + 'abcdefABCDEF'

PERSIAN_DIGITS = '۰۱۲۳۴۵۶۷۸۹'
PERSIAN_DIGITS_MAP = {p: d for p, d in zip(PERSIAN_DIGITS, DECIMAL_DIGITS)}
EASTERN_ARABIC_DIGITS = PERSIAN_DIGITS

DEVANAGARI_DIGITS = '०१२३४५६७८९'
BENGALI_DIGITS = '০১২৩৪৫৬৭৮৯'
THAI_DIGITS = '๐๑๒๓๔๕๖๗๘๙'
TAMIL_DIGITS = '௦௧௨௩௪௫௬௭௮௯'
TELUGU_DIGITS = '౦౧౨౩౪౫౬౭౮౯'
KANNADA_DIGITS = '೦೧೨೩೪೫೬೭೮೯'
MALAYALAM_DIGITS = '൦൧൨൩൪൫൬൭൮൯'
GURMUKHI_DIGITS = '੦੧੨੩੪੫੬੭੮੯'
GUJARATI_DIGITS = '૦૧૨૩૪૫૬૭૮૯'
ORIYA_DIGITS = '୦୧୨୩୪୫୬୭୮୯'
TIBETAN_DIGITS = '༠༡༢༣༤༥༦༧༨༩'
MYANMAR_DIGITS = '၀၁၂၃၄၅၆၇၈၉'
KHMER_DIGITS = '០១២៣៤៥៦៧៨៩'
LAO_DIGITS = '໐໑໒໓໔໕໖໗໘໙'
MONGOLIAN_DIGITS = '᠐᠑᠒᠓᠔᠕᠖᠗᠘᠙'
JAVANESE_DIGITS = '꧐꧑꧒꧓꧔꧕꧖꧗꧘꧙'
BALINESE_DIGITS = '᭐᭑᭒᭓᭔᭕᭖᭗᭘᭙'
SUNDANESE_DIGITS = '᮰᮱᮲᮳᮴᮵᮶᮷᮸᮹'
LEPCHA_DIGITS = 'ᰰᰱᰲᰳᰴᰵᰶ᰷'
OL_CHIKI_DIGITS = '᱐᱑᱒᱓᱔᱕᱖᱗᱘᱙'
SAURASHTRA_DIGITS = '꣐꣑꣒꣓꣔꣕꣖꣗꣘꣙'
WARANG_CITI_DIGITS = '꣰꣱ꣲꣳꣴꣵꣶꣷ꣸꣹'
MAHAJANI_DIGITS = '𑁦𑁧𑁨𑁩𑁪𑁫𑁬𑁭𑁮𑁯'
MODI_DIGITS = '𑙐𑙑𑙒𑙓𑙔𑙕𑙖𑙗𑙘𑙙'
NANDINAGARI_DIGITS = '𑦠𑦡𑦢𑦣𑦤𑦥𑦦𑦧𑦨𑦩'
TAKRI_DIGITS = '𑛀𑛁𑛂𑛃𑛄𑛅𑛆𑛇𑛈𑛉'
DOGRA_DIGITS = '𑠰𑠱𑠲𑠳𑠴𑠵𑠶𑠷𑠸𑠹'

CIRCLED_NUMBERS = '①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳'
PARENTHESIZED_NUMBERS = '⑴⑵⑶⑷⑸⑹⑺⑻⑼⑽⑾⑿⒀⒁⒂⒃⒄⒅⒆⒇'
ROMAN_NUMERALS_UPPER = 'ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫ'
ROMAN_NUMERALS_LOWER = 'ⅰⅱⅲⅳⅴⅵⅶⅷⅸⅹⅺⅻ'
CHINESE_NUMBERS = '〇一二三四五六七八九十百千万亿兆'

ALL_DIGITS = (DECIMAL_DIGITS + PERSIAN_DIGITS + DEVANAGARI_DIGITS + 
              BENGALI_DIGITS + THAI_DIGITS + TAMIL_DIGITS + TELUGU_DIGITS +
              KANNADA_DIGITS + MALAYALAM_DIGITS + GURMUKHI_DIGITS + 
              GUJARATI_DIGITS + ORIYA_DIGITS + TIBETAN_DIGITS + 
              MYANMAR_DIGITS + KHMER_DIGITS + LAO_DIGITS + MONGOLIAN_DIGITS +
              JAVANESE_DIGITS + BALINESE_DIGITS + SUNDANESE_DIGITS +
              LEPCHA_DIGITS + OL_CHIKI_DIGITS + SAURASHTRA_DIGITS +
              WARANG_CITI_DIGITS + MAHAJANI_DIGITS + MODI_DIGITS +
              NANDINAGARI_DIGITS + TAKRI_DIGITS + DOGRA_DIGITS +
              CIRCLED_NUMBERS + PARENTHESIZED_NUMBERS + ROMAN_NUMERALS_UPPER +
              ROMAN_NUMERALS_LOWER + CHINESE_NUMBERS)

# ==================== LATIN-BASED ALPHABETS (40+ LANGUAGES) ====================

# Western European
ASCII_LOWERCASE = 'abcdefghijklmnopqrstuvwxyz'
ASCII_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ASCII_LETTERS = ASCII_LOWERCASE + ASCII_UPPERCASE

# 1. German
GERMAN_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzäöüß'
GERMAN_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜẞ'

# 2. French
FRENCH_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzàâæçéèêëîïôœùûüÿ'
FRENCH_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÂÆÇÉÈÊËÎÏÔŒÙÛÜŸ'

# 3. Spanish
SPANISH_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzáéíñóúü'
SPANISH_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÑÓÚÜ'

# 4. Italian
ITALIAN_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzàáèéìíîòóùú'
ITALIAN_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÁÈÉÌÍÎÒÓÙÚ'

# 5. Portuguese
PORTUGUESE_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzàáâãçéêíóôõúü'
PORTUGUESE_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÁÂÃÇÉÊÍÓÔÕÚÜ'

# 6. Dutch
DUTCH_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzàáâäéèêëíìîïóòôöúùûüÿ'
DUTCH_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÁÂÄÉÈÊËÍÌÎÏÓÒÔÖÚÙÛÜŸ'

# 7. Romanian
ROMANIAN_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzăâîșț'
ROMANIAN_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZĂÂÎȘȚ'

# 8. Polish
POLISH_LOWERCASE = 'abcdefghijklmnopqrstuvwxyząćęłńóśźż'
POLISH_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZĄĆĘŁŃÓŚŹŻ'

# 9. Czech
CZECH_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzáčďéěíňóřšťúůýž'
CZECH_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ'

# 10. Slovak
SLOVAK_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzáäčďéíĺľňóôŕšťúýž'
SLOVAK_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÄČĎÉÍĹĽŇÓÔŔŠŤÚÝŽ'

# 11. Hungarian
HUNGARIAN_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzáéíóöőúüű'
HUNGARIAN_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÖŐÚÜŰ'

# 12. Croatian
CROATIAN_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzćčđšž'
CROATIAN_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZĆČĐŠŽ'

# 13. Slovene
SLOVENE_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzčšž'
SLOVENE_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZČŠŽ'

# 14. Lithuanian
LITHUANIAN_LOWERCASE = 'abcdefghijklmnopqrstuvwxyząčęėįšųūž'
LITHUANIAN_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZĄČĘĖĮŠŲŪŽ'

# 15. Latvian
LATVIAN_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzāčēģīķļņōŗšūž'
LATVIAN_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZĀČĒĢĪĶĻŅŌŖŠŪŽ'

# 16. Estonian
ESTONIAN_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzäöüõšž'
ESTONIAN_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜÕŠŽ'

# 17. Finnish
FINNISH_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzäöåšž'
FINNISH_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÅŠŽ'

# 18. Swedish
SWEDISH_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzåäö'
SWEDISH_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ'

# 19. Norwegian
NORWEGIAN_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzæøå'
NORWEGIAN_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ'

# 20. Danish
DANISH_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzæøå'
DANISH_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ'

# 21. Icelandic
ICELANDIC_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzáðéíóúýþæö'
ICELANDIC_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÐÉÍÓÚÝÞÆÖ'

# 22. Faroese
FAROESE_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzáðíóúýæø'
FAROESE_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÐÍÓÚÝÆØ'

# 23. Turkish
TURKISH_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzâçğıiîöşüû'
TURKISH_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÂÇĞIİÎÖŞÜÛ'

# 24. Azerbaijani
AZERBAIJANI_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzçəğışöü'
AZERBAIJANI_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÇƏĞIŞÖÜ'

# 25. Vietnamese
VIETNAMESE_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ'
VIETNAMESE_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ'

# 26. Catalan
CATALAN_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzàéèíïóòúüç'
CATALAN_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÉÈÍÏÓÒÚÜÇ'

# 27. Welsh
WELSH_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzâêîôûŵŷáéíóúýäëïöüÿ'
WELSH_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÂÊÎÔÛŴŶÁÉÍÓÚÝÄËÏÖÜŸ'

# 28. Maltese
MALTESE_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzàċèéìíîòóùúġħż'
MALTESE_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀĊÈÉÌÍÎÒÓÙÚĠĦŻ'

# 29. Irish
IRISH_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzáéíóú'
IRISH_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚ'

# 30. Scots Gaelic
SCOTS_GAELIC_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzàèìòù'
SCOTS_GAELIC_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÈÌÒÙ'

# 31. Basque
BASQUE_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzñü'
BASQUE_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÑÜ'

# 32. Galician
GALICIAN_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzáéíñóúü'
GALICIAN_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÑÓÚÜ'

# 33. Esperanto
ESPERANTO_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzĉĝĥĵŝŭ'
ESPERANTO_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZĈĜĤĴŜŬ'

# 34. Albanian
ALBANIAN_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzëç'
ALBANIAN_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZËÇ'

# 35. Bosnian
BOSNIAN_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzćčđšž'
BOSNIAN_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZĆČĐŠŽ'

# 36. Serbian (Latin)
SERBIAN_LATIN_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzćčđšž'
SERBIAN_LATIN_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZĆČĐŠŽ'

# 37. Montenegrin (Latin)
MONTENEGRIN_LATIN_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzćčđšž'
MONTENEGRIN_LATIN_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZĆČĐŠŽ'

# 38. Macedonian (Latin)
MACEDONIAN_LATIN_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzčćđšžǵ'
MACEDONIAN_LATIN_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZČĆĐŠŽǴ'

# 39. Turkmen (Latin)
TURKMEN_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzáçýöşüň'
TURKMEN_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÇÝÖŞÜŇ'

# 40. Crimean Tatar (Latin)
CRIMEAN_TATAR_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzâçğıñöşü'
CRIMEAN_TATAR_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÂÇĞIÑÖŞÜ'

# 41. Breton
BRETON_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzâêîôûùüñ'
BRETON_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÂÊÎÔÛÙÜÑ'

# 42. Friulian
FRIULIAN_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzàâçèéìîôòùû'
FRIULIAN_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÂÇÈÉÌÎÔÒÙÛ'

# 43. Romansh
ROMSH_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzàèìòùéê'
ROMSH_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÈÌÒÙÉÊ'

# 44. Luxembourgish
LUXEMBOURGISH_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzäëé'
LUXEMBOURGISH_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÄËÉ'

# 45. Corsican
CORSICAN_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzàèìòù'
CORSICAN_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÈÌÒÙ'

# 46. Sardinian
SARDINIAN_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzàèìòù'
SARDINIAN_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÈÌÒÙ'

# 47. Sicilian
SICILIAN_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzàèìòù'
SICILIAN_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÈÌÒÙ'

# 48. Neapolitan
NEAPOLITAN_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzàèìòù'
NEAPOLITAN_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÈÌÒÙ'

# 49. Asturian
ASTURIAN_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzáéíóúüñ'
ASTURIAN_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚÜÑ'

# 50. Aragonese
ARAGONESE_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzáéíóúñü'
ARAGONESE_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚÑÜ'

# 51. Occitan
OCCITAN_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzàáèéíïòóúü'
OCCITAN_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÁÈÉÍÏÒÓÚÜ'

# 52. Walloon
WALLOON_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzåâêîôû'
WALLOON_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÅÂÊÎÔÛ'

# 53. Ladin
LADIN_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzàéèìóòù'
LADIN_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÉÈÌÓÒÙ'

# 54. Mirandese
MIRANDESE_LOWERCASE = 'abcdefghijklmnopqrstuvwxyzáéíóú'
MIRANDESE_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚ'

# ==================== CYRILLIC ALPHABETS (15+ LANGUAGES) ====================

# 55. Russian
RUSSIAN_LOWERCASE = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
RUSSIAN_UPPERCASE = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'

# 56. Ukrainian
UKRAINIAN_LOWERCASE = 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'
UKRAINIAN_UPPERCASE = 'АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ'

# 57. Bulgarian
BULGARIAN_LOWERCASE = 'абвгдежзийклмнопрстуфхцчшщъьюя'
BULGARIAN_UPPERCASE = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЬЮЯ'

# 58. Serbian (Cyrillic)
SERBIAN_CYRILLIC_LOWERCASE = 'абвгдђежзијклљмнњопрстћуфхцчџш'
SERBIAN_CYRILLIC_UPPERCASE = 'АБВГДЂЕЖЗИЈКЛЉМНЊОПРСТЋУФХЦЧЏШ'

# 59. Macedonian
MACEDONIAN_CYRILLIC_LOWERCASE = 'абвгдѓежзѕијклљмнњопрстќуфхцчџш'
MACEDONIAN_CYRILLIC_UPPERCASE = 'АБВГДЃЕЖЗЅИЈКЛЉМНЊОПРСТЌУФХЦЧЏШ'

# 60. Belarusian
BELARUSIAN_LOWERCASE = 'абвгдежзйклмнопрстуфхцчшыьэюяёіў'
BELARUSIAN_UPPERCASE = 'АБВГДЕЖЗЙКЛМНОПРСТУФХЦЧШЫЬЭЮЯЁІЎ'

# 61. Mongolian (Cyrillic)
MONGOLIAN_CYRILLIC_LOWERCASE = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяөү'
MONGOLIAN_CYRILLIC_UPPERCASE = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯӨҮ'

# 62. Kazakh
KAZAKH_CYRILLIC_LOWERCASE = 'абвгдеёжзийклмнопрстуфхцчшщъыіьэюяғқңөұүһ'
KAZAKH_CYRILLIC_UPPERCASE = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫІЬЭЮЯҒҚҢӨҰҮҺ'

# 63. Kyrgyz
KYRGYZ_CYRILLIC_LOWERCASE = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяңөү'
KYRGYZ_CYRILLIC_UPPERCASE = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯҢӨҮ'

# 64. Tajik
TAJIK_CYRILLIC_LOWERCASE = 'абвгдеёжзийклмнопрстуфхцчшъыьэюяғӣқӯҳҷ'
TAJIK_CYRILLIC_UPPERCASE = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЪЫЬЭЮЯҒӢҚӮҲҶ'

# 65. Tatar
TATAR_CYRILLIC_LOWERCASE = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяәөүҗңһ'
TATAR_CYRILLIC_UPPERCASE = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯӘӨҮҖҢҺ'

# 66. Bashkir
BASHKIR_CYRILLIC_LOWERCASE = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяәөүҡңҫһ'
BASHKIR_CYRILLIC_UPPERCASE = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯӘӨҮҠҢҪҺ'

# 67. Chuvash
CHUVASH_CYRILLIC_LOWERCASE = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяӑӗ'
CHUVASH_CYRILLIC_UPPERCASE = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯӐӖ'

# 68. Ossetian
OSSETIAN_CYRILLIC_LOWERCASE = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяæӕ'
OSSETIAN_CYRILLIC_UPPERCASE = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯÆӔ'

# 69. Mari
MARI_CYRILLIC_LOWERCASE = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяӧӱ'
MARI_CYRILLIC_UPPERCASE = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯӦӰ'

# 70. Udmurt
UDMURT_CYRILLIC_LOWERCASE = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяӥӧ'
UDMURT_CYRILLIC_UPPERCASE = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯӤӦ'

# ==================== ARABIC-BASED SCRIPTS (10+ LANGUAGES) ====================

# 71. Arabic
ARABIC_LETTERS = 'ءآأؤإئابةتثجحخدذرزسشصضطظعغفقكلمنهويى'
ARABIC_LETTERS_LIST = list(ARABIC_LETTERS)
ARABIC_ALL_FORMS = ARABIC_LETTERS + 'ۀةكىًٌٍَُِّْٰٕٓٔٱٹپچڈڑژکگںھہۃیے'

# 72. Persian/Farsi
PERSIAN_LETTERS = 'آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی'
PERSIAN_LETTERS_LIST = list(PERSIAN_LETTERS)
PERSIAN_FULL = PERSIAN_LETTERS + 'ءأؤإئۀةك'

# 73. Urdu
URDU_LETTERS = 'آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیٹڈڑںھے'
URDU_LETTERS_LIST = list(URDU_LETTERS)

# 74. Pashto
PASHTO_LETTERS = 'آابپتټثجځچڅحخدډذرړزژږسشښصضطظعغفقکګلمنڼوهیې'
PASHTO_LETTERS_LIST = list(PASHTO_LETTERS)

# 75. Kurdish (Arabic)
KURDISH_ARABIC = 'ئابپتجچحخدرزژسشعغفڤقکگلڵمنهوەێ'
KURDISH_ARABIC_LIST = list(KURDISH_ARABIC)

# 76. Sindhi
SINDHI_LETTERS = 'آابٻتثپجڄچحخدڌڏرزسشصضطظعغفڦقڪکگڱلمنڻوهءي'
SINDHI_LETTERS_LIST = list(SINDHI_LETTERS)

# 77. Uyghur
UYGHUR_ARABIC = 'ئابپتجچخدرزژسشغفقكگڭلمنھوۇۆۈۋېى'
UYGHUR_ARABIC_LIST = list(UYGHUR_ARABIC)

# 78. Jawi/Malay
JAWI_LETTERS = 'ابجچدرفغهيحکلمنڤوقسرتوءيڠ'
JAWI_LETTERS_LIST = list(JAWI_LETTERS)

# 79. Balochi
BALOCHI_ARABIC = 'آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیءے'
BALOCHI_ARABIC_LIST = list(BALOCHI_ARABIC)

# 80. Kashmiri
KASHMIRI_ARABIC = 'آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیٹڈڑں'
KASHMIRI_ARABIC_LIST = list(KASHMIRI_ARABIC)

# ==================== SOUTH ASIAN SCRIPTS (12+ LANGUAGES) ====================

# 81. Devanagari (Hindi, Marathi, Nepali, Sanskrit)
DEVANAGARI_VOWELS = 'अआइईउऊऋएऐओऔअंअः'
DEVANAGARI_CONSONANTS = 'कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसह'
DEVANAGARI_LETTERS = DEVANAGARI_VOWELS + DEVANAGARI_CONSONANTS + 'क्षत्रज्ञश्र'
DEVANAGARI_LETTERS_LIST = list(DEVANAGARI_LETTERS)

# 82. Bengali
BENGALI_VOWELS = 'অআইঈউঊঋএঐওঔ'
BENGALI_CONSONANTS = 'কখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহড়ঢ়য়ৎ'
BENGALI_LETTERS = BENGALI_VOWELS + BENGALI_CONSONANTS
BENGALI_LETTERS_LIST = list(BENGALI_LETTERS)

# 83. Gurmukhi (Punjabi)
GURMUKHI_VOWELS = 'ਅਆਇਈਉਊਏਐਓਔ'
GURMUKHI_CONSONANTS = 'ਕਖਗਘਙਚਛਜਝਞਟਠਡਢਣਤਥਦਧਨਪਫਬਭਮਯਰਲਵਸਹ'
GURMUKHI_LETTERS = GURMUKHI_VOWELS + GURMUKHI_CONSONANTS + 'ੜਸ਼ਖ਼ਗ਼ਜ਼ਫ਼'

# 84. Gujarati
GUJARATI_VOWELS = 'અઆઇઈઉઊઋએઐઓઔ'
GUJARATI_CONSONANTS = 'કખગઘઙચછજઝઞટઠડઢણતથદધનપફબભમયરલવશષસહ'
GUJARATI_LETTERS = GUJARATI_VOWELS + GUJARATI_CONSONANTS + 'ળક્ષજ્ઞ'

# 85. Odia
ODIA_VOWELS = 'ଅଆଇଈଉଊଋଏଐଓଔ'
ODIA_CONSONANTS = 'କଖଗଘଙଚଛଜଝଞଟଠଡଢଣତଥଦଧନପଫବଭମଯରଲଵଶଷସହ'
ODIA_LETTERS = ODIA_VOWELS + ODIA_CONSONANTS + 'ଡ଼ଢ଼ୟୱ'

# 86. Tamil
TAMIL_VOWELS = 'அஆஇஈஉஊஎஏஐஒஓஔ'
TAMIL_CONSONANTS = 'கஙசஞடணதநபமயரலவழளறன'
TAMIL_LETTERS = TAMIL_VOWELS + TAMIL_CONSONANTS + 'ஜஷஸஹக்ஷஶ'

# 87. Telugu
TELUGU_VOWELS = 'అఆఇఈఉఊఋఎఏఐఒఓఔ'
TELUGU_CONSONANTS = 'కఖగఘఙచఛజఝఞటఠడఢణతథదధనపఫబభమయరఱలళవశషసహ'
TELUGU_LETTERS = TELUGU_VOWELS + TELUGU_CONSONANTS

# 88. Kannada
KANNADA_VOWELS = 'ಅಆಇಈಉಊಋಎಏಐಒಓಔ'
KANNADA_CONSONANTS = 'ಕಖಗಘಙಚಛಜಝಞಟಠಡಢಣತಥದಧನಪಫಬಭಮಯರಲಳವಶಷಸಹ'
KANNADA_LETTERS = KANNADA_VOWELS + KANNADA_CONSONANTS + 'ಱೞ'

# 89. Malayalam
MALAYALAM_VOWELS = 'അആഇഈഉഊഋഎഏഐഒഓഔ'
MALAYALAM_CONSONANTS = 'കഖഗഘങചഛജഝഞടഠഡഢണതഥദധനപഫബഭമയരലളവശഷസഹ'
MALAYALAM_LETTERS = MALAYALAM_VOWELS + MALAYALAM_CONSONANTS + 'റ്റന്റ'

# 90. Sinhala
SINHALA_VOWELS = 'අආඇඈඉඊඋඌඍඎඏඐඑඒඓඔඕඖ'
SINHALA_CONSONANTS = 'කඛගඝඞචඡජඣඤටඨඩඪණතථදධනපඵබභමයරලවශෂසහ'
SINHALA_LETTERS = SINHALA_VOWELS + SINHALA_CONSONANTS + 'ළෆ'

# 91. Marathi (additional Devanagari)
MARATHI_EXTRA = 'ऍऎऑऒऴ'

# ==================== SOUTHEAST ASIAN SCRIPTS ====================

# 92. Thai
THAI_CONSONANTS = 'กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรฤลวศษสหฬอฮ'
THAI_VOWELS = 'ะัาำิีึืุูเแโใไๆ'
THAI_TONES = '่้๊๋'
THAI_LETTERS = THAI_CONSONANTS + THAI_VOWELS + THAI_TONES

# 93. Lao
LAO_CONSONANTS = 'ກຂຄງຈຊຍດຕຖທນບປຜຝພຟມຢຣລວສຫອຮ'
LAO_VOWELS = 'ະັາິີຶືຸູເແໂໃໄ'
LAO_LETTERS = LAO_CONSONANTS + LAO_VOWELS + '່້໊໋'

# 94. Khmer
KHMER_CONSONANTS = 'កខគឃងចឆជឈញដឋឌឍណតថទធនបផពភមយរលវឝឞសហឡអ'
KHMER_VOWELS = 'ឣឤឥឦឧឨឩឪឫឬឭឮឯឰឱឲឳ'
KHMER_LETTERS = KHMER_CONSONANTS + KHMER_VOWELS

# 95. Myanmar
MYANMAR_CONSONANTS = 'ကခဂဃငစဆဇဈဉတထဒဓနပဖဗဘမယရလဝသဟဠအ'
MYANMAR_VOWELS = 'အအာဣဤဥဦဧဩဪ'
MYANMAR_LETTERS = MYANMAR_CONSONANTS + MYANMAR_VOWELS

# 96. Javanese
JAVANESE_LETTERS = 'ꦲꦤꦕꦫꦏꦢꦠꦱꦮꦭꦥꦝꦗꦪꦚꦩꦒꦧꦛꦔ'
JAVANESE_VOWELS = 'ꦄꦅꦆꦇꦈꦉꦊꦋꦌꦍ'

# 97. Balinese
BALINESE_LETTERS = 'ᬳᬦᬘᬭᬓᬤᬢᬲᬯᬮᬧᬥᬚᬬᬜᬫᬕᬩᬛᬗ'
BALINESE_VOWELS = 'ᬅᬆᬇᬈᬉᬊᬋᬌᬍᬎᬏᬐᬑᬒ'

# ==================== EAST ASIAN SCRIPTS ====================

# 98. Chinese (Extended)
CHINESE_COMMON = ("的一是不了人我在有他这中大来上国个到说们为子和你地道也"
                  "时年得就那要下以生会自着去之过家学对可里后小"
                  "天日身心意事明月水火山石木金土田禾米竹车舟门"
                  "花鸟虫鱼马牛羊龙风云雨电气光色"
                  "你我他她它我们你们他们自己大家所有很多一些"
                  "因为所以但是虽然然而如果而且或者并且由于"
                  "可以应该需要能够希望觉得知道认为想说要")
CHINESE_LETTERS_LIST = list(CHINESE_COMMON)

# 99. Japanese
HIRAGANA = ("あいうえおかきくけこさしすせそたちつてと"
            "なにぬねのはひふへほまみむめもやゆよ"
            "らりるれろわをん"
            "がぎぐげござじずぜぞだぢづでど"
            "ばびぶべぼぱぴぷぺぽ"
            "っゃゅょぁぃぅぇぉ")
KATAKANA = ("アイウエオカキクケコサシスセソタチツテト"
            "ナニヌネノハヒフヘホマミムメモヤユヨ"
            "ラリルレロワヲン"
            "ガギグゲゴザジズゼゾダヂヅデド"
            "バビブベボパピプペポ"
            "ッャュョァィゥェォ")
JAPANESE_LETTERS = HIRAGANA + KATAKANA

# 100. Korean
HANGUL_INITIAL = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
HANGUL_MEDIAL = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
HANGUL_FINAL = 'ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ'
HANGUL_SYLLABLES = '가나다라마바사아자차카타파하'
HANGUL_LETTERS = HANGUL_INITIAL + HANGUL_MEDIAL + HANGUL_FINAL + HANGUL_SYLLABLES

# ==================== OTHER SCRIPTS ====================

# Greek
GREEK_LOWERCASE = 'αβγδεζηθικλμνξοπρστυφχψω'
GREEK_UPPERCASE = 'ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ'
GREEK_LETTERS = GREEK_LOWERCASE + GREEK_UPPERCASE + 'άέήίόύώϊϋΐΰΆΈΉΊΌΎΏΪΫ'

# Hebrew
HEBREW_LETTERS = 'אבגדהוזחטיכלמנסעפצקרשת'
HEBREW_FULL = HEBREW_LETTERS + 'םןףץך'

# Armenian
ARMENIAN_LOWERCASE = 'աբգդեզէըթժիլխծկհձղճմյնշոչպջռսվտրցւփքօֆ'
ARMENIAN_UPPERCASE = 'ԱԲԳԴԵԶԷԸԹԺԻԼԽԾԿՀՁՂՃՄՅՆՇՈՉՊՋՌՍՎՏՐՑՒՓՔՕՖ'
ARMENIAN_LETTERS = ARMENIAN_LOWERCASE + ARMENIAN_UPPERCASE

# Georgian
GEORGIAN_MKHEDRULI = 'აბგდევზთიკლმნოპჟრსტუფქღყშჩცძწჭხჯჰ'
GEORGIAN_ASOMTAVRULI = 'ႠႡႢႣႤႥႦႧႨႩႪႫႬႭႮႯႰႱႲႳႴႵႶႷႸႹႺႻႼႽႾႿჀ'
GEORGIAN_LETTERS = GEORGIAN_MKHEDRULI + GEORGIAN_ASOMTAVRULI

# Amharic
AMHARIC_LETTERS = ('ሀሁሂሃሄህሆለሉሊላሌልሎሐሑሒሓሔሕሖመሙሚማሜምሞ'
                   'ሠሡሢሣሤሥሦረሩሪራሬርሮሰሱሲሳሴስሶሸሹሺሻሼሽሾ'
                   'ቀቁቂቃቄቅቆበቡቢባቤብቦተቱቲታቴትቶቸቹቺቻቼችቾ'
                   'ኀኁኂኃኄኅኆነኑኒናኔንኖአኡኢኣኤእኦከኩኪካኬክኮ'
                   'ወዉዊዋዌውዎዐዑዒዓዔዕዖዘዙዚዛዜዝዞዠዡዢዣዤዥዦ'
                   'የዩዪያዬይዮደዱዲዳዴድዶጀጁጂጃጄጅጆገጉጊጋጌግጎ'
                   'ጠጡጢጣጤጥጦጰጱጲጳጴጵጶፀፁፂፃፄፅፆፈፉፊፋፌፍፎ'
                   'ፐፑፒፓፔፕፖ')

# Tibetan
TIBETAN_CONSONANTS = 'ཀཁགངཅཆཇཉཏཐདནཔཕབམཙཚཛཝཞཟའཡརལཤསཧ'
TIBETAN_VOWELS = 'ཨཨིཨུཨེཨོ'
TIBETAN_LETTERS = TIBETAN_CONSONANTS + TIBETAN_VOWELS

# Syriac
SYRIAC_LETTERS = 'ܐܒܓܕܗܘܙܚܛܝܟܠܡܢܣܥܦܨܩܪܫܬ'
SYRIAC_LETTERS_LIST = list(SYRIAC_LETTERS)

# Thaana (Maldivian)
THAANA_LETTERS = 'ހށނރބޅކއވމފދތލގޏސޑޒޓޔޕޖޗ'

# Cherokee
CHEROKEE_LETTERS = ('ᎠᎡᎢᎣᎤᎥᎦᎧᎨᎩᎪᎫᎬᎭᎮᎯᎰᎱᎲᎳᎴᎵᎶᎷᎸᎹᎺᎻᎼᎽᎾᎿ'
                     'ᏀᏁᏂᏃᏄᏅᏆᏇᏈᏉᏊᏋᏌᏍᏎᏏᏐᏑᏒᏓᏔᏕᏖᏗᏘᏙᏚᏛᏜᏝᏞᏟ'
                     'ᏠᏡᏢᏣᏤᏥᏦᏧᏨᏩᏪᏫᏬᏭᏮᏯᏰᏱᏲᏳᏴ')

# IPA
IPA_CONSONANTS = 'ɐɑɒɓɔɕɖɗɘəɚɛɜɝɞɟɠɡɢɣɤɥɦɧɨɩɪɫɬɭɮɯɰɱɲɳɴɵɶɸɹɺɻɼɽɾɿʀʁʂʃʄʅʆʇʈʉʊʋʌʍʎʏʐʑʒʓʔʕʖʗʘʙʚʛʜʝʞʟʠʡʢʣʤʥʦʧʨʩʪʫʬʭʮʯ'
IPA_VOWELS = 'æɑɒʌɜəɪʊɔɛɵɨʉ'

# Ancient scripts
PHOENICIAN = '𐤀𐤁𐤂𐤃𐤄𐤅𐤆𐤇𐤈𐤉𐤊𐤋𐤌𐤍𐤎𐤏𐤐𐤑𐤒𐤓𐤔𐤕'
CUNEIFORM_SAMPLE = '𒀀𒀁𒀂𒀃𒀄𒀅𒀆𒀇𒀈𒀉𒀊𒀋𒀌𒀍𒀎𒀏'

# ==================== SYMBOLS AND SPECIAL CHARACTERS ====================

# Currency Symbols
CURRENCY_SYMBOLS = '₳฿₵¢₡₢₣₤₥₦₧₨₩₪₫€₭₮₯₰₱₲₳₴₵₶₷₸₹₺₻₼₽₾₿﷼¥$£€©®™'

# Mathematical Symbols
MATH_SYMBOLS = '±÷×≈≠≤≥∞∑∏∫∂∇√∛∜∝∞∠∡∢∥⊥∦∧∨∩∪⊂⊃⊄⊅⊆⊇⊈⊉⊊⊋⊕⊖⊗⊘⊙⊚⊛⊜⊝⊞⊟⊠⊡∀∃∄∈∉∌∋⊢⊣⊤⊥'

# Arrows
ARROWS = '←↑→↓↔↕↖↗↘↙↚↛↜↝↞↟↠↡↢↣↤↥↦↧↨↩↪↫↬↭↮↯↰↱↲↳↴↵↶↷↸↹↺↻↼↽↾↿⇀⇁⇂⇃⇄⇅⇆⇇⇈⇉⇊⇋⇌⇍⇎⇏⇐⇑⇒⇓⇔⇕⇖⇗⇘⇙⇚⇛⇜⇝⇞⇟⇠⇡⇢⇣⇤⇥⇦⇧⇨⇩⇪'

# Music Symbols
MUSIC_SYMBOLS = '♩♪♫♬♭♮♯𝄞𝄡𝄢𝄣𝄤𝄥𝄦𝄩𝄪𝄫'

# Chess and Games
CHESS_SYMBOLS = '♔♕♖♗♘♙♚♛♜♝♞♟'
CARDS_SYMBOLS = '♠♡♢♣♤♥♦♧'

# Zodiac and Astronomy
ZODIAC_SYMBOLS = '♈♉♊♋♌♍♎♏♐♑♒♓'
ASTRONOMY_SYMBOLS = '☉☿♀♂♁♃♄♅♆♇'

# Weather and Seasons
WEATHER_SYMBOLS = '☀☁☂☃☄❄❅❆❇❈❉❊❋☔☕❄🌟🌙🌞'

# Fraction characters
FRACTIONS = '¼½¾⅐⅑⅒⅓⅔⅕⅖⅗⅘⅙⅚⅛⅜⅝⅞⅟↉'

# Box Drawing
BOX_DRAWING = '┌┍┎┏┐┑┒┓└┕┖┗┘┙┚┛├┝┞┟┠┡┢┣┤┥┦┧┨┩┪┫┬┭┮┯┰┱┲┳┴┵┶┷┸┹┺┻┼┽┾┿╀╁╂╃╄╅╆╇╈╉╊╋═║╒╓╔╕╖╗╘╙╚╛╜╝╞╟╠╡╢╣╤╥╦╧╨╩╪╫╬'

# Common Emojis
COMMON_EMOJIS = '😀😂🤣😊😍🥰😘😜🤪😎🤩🥳😢😭😤😡🥵🥶😱🤯🤠💀👻👽🤖🎃😺❤️💔💕💖💗💘💝💟☮️✝️☪️🕉️☸️✡️🔯🕎☯️☦️'
EMOJI_FLAGS = '🇮🇷🇺🇸🇬🇧🇩🇪🇫🇷🇷🇺🇨🇳🇯🇵🇰🇷🇹🇷🇦🇪🇸🇦🇮🇳🇵🇰🇦🇫🇧🇷🇦🇷🇲🇽🇮🇹🇪🇸🇨🇦🇦🇺🇩🇪🇫🇷'

# Persian/Arabic diacritics
PERSIAN_HARAKAT = 'ًٌٍَُِّْ'
PERSIAN_PUNCTUATION = '،؛؟٪٬٫٭ٰ'
ARABIC_DIACRITICS = 'ًٌٍَُِّْٰٕٓٔ'

# ==================== COMPREHENSIVE COLLECTIONS ====================

# All Latin-based alphabets combined
ALL_LATIN_LOWERCASE = ''.join(set(
    ASCII_LOWERCASE + GERMAN_LOWERCASE + FRENCH_LOWERCASE + SPANISH_LOWERCASE +
    ITALIAN_LOWERCASE + PORTUGUESE_LOWERCASE + DUTCH_LOWERCASE + 
    ROMANIAN_LOWERCASE + POLISH_LOWERCASE + CZECH_LOWERCASE +
    SLOVAK_LOWERCASE + HUNGARIAN_LOWERCASE + CROATIAN_LOWERCASE +
    SLOVENE_LOWERCASE + LITHUANIAN_LOWERCASE + LATVIAN_LOWERCASE +
    ESTONIAN_LOWERCASE + FINNISH_LOWERCASE + SWEDISH_LOWERCASE +
    NORWEGIAN_LOWERCASE + DANISH_LOWERCASE + ICELANDIC_LOWERCASE +
    FAROESE_LOWERCASE + TURKISH_LOWERCASE + AZERBAIJANI_LOWERCASE +
    VIETNAMESE_LOWERCASE + CATALAN_LOWERCASE + WELSH_LOWERCASE +
    MALTESE_LOWERCASE + IRISH_LOWERCASE + SCOTS_GAELIC_LOWERCASE +
    BASQUE_LOWERCASE + GALICIAN_LOWERCASE + ESPERANTO_LOWERCASE +
    ALBANIAN_LOWERCASE + BOSNIAN_LOWERCASE + SERBIAN_LATIN_LOWERCASE +
    MONTENEGRIN_LATIN_LOWERCASE + MACEDONIAN_LATIN_LOWERCASE +
    TURKMEN_LOWERCASE + CRIMEAN_TATAR_LOWERCASE + BRETON_LOWERCASE +
    FRIULIAN_LOWERCASE + ROMSH_LOWERCASE + LUXEMBOURGISH_LOWERCASE +
    CORSICAN_LOWERCASE + SARDINIAN_LOWERCASE + SICILIAN_LOWERCASE +
    NEAPOLITAN_LOWERCASE + ASTURIAN_LOWERCASE + ARAGONESE_LOWERCASE +
    OCCITAN_LOWERCASE + WALLOON_LOWERCASE + LADIN_LOWERCASE +
    MIRANDESE_LOWERCASE
))

ALL_LATIN_UPPERCASE = ''.join(set(
    ASCII_UPPERCASE + GERMAN_UPPERCASE + FRENCH_UPPERCASE + SPANISH_UPPERCASE +
    ITALIAN_UPPERCASE + PORTUGUESE_UPPERCASE + DUTCH_UPPERCASE + 
    ROMANIAN_UPPERCASE + POLISH_UPPERCASE + CZECH_UPPERCASE +
    SLOVAK_UPPERCASE + HUNGARIAN_UPPERCASE + CROATIAN_UPPERCASE +
    SLOVENE_UPPERCASE + LITHUANIAN_UPPERCASE + LATVIAN_UPPERCASE +
    ESTONIAN_UPPERCASE + FINNISH_UPPERCASE + SWEDISH_UPPERCASE +
    NORWEGIAN_UPPERCASE + DANISH_UPPERCASE + ICELANDIC_UPPERCASE +
    FAROESE_UPPERCASE + TURKISH_UPPERCASE + AZERBAIJANI_UPPERCASE +
    VIETNAMESE_UPPERCASE + CATALAN_UPPERCASE + WELSH_UPPERCASE +
    MALTESE_UPPERCASE + IRISH_UPPERCASE + SCOTS_GAELIC_UPPERCASE +
    BASQUE_UPPERCASE + GALICIAN_UPPERCASE + ESPERANTO_UPPERCASE +
    ALBANIAN_UPPERCASE + BOSNIAN_UPPERCASE + SERBIAN_LATIN_UPPERCASE +
    MONTENEGRIN_LATIN_UPPERCASE + MACEDONIAN_LATIN_UPPERCASE +
    TURKMEN_UPPERCASE + CRIMEAN_TATAR_UPPERCASE + BRETON_UPPERCASE +
    FRIULIAN_UPPERCASE + ROMSH_UPPERCASE + LUXEMBOURGISH_UPPERCASE +
    CORSICAN_UPPERCASE + SARDINIAN_UPPERCASE + SICILIAN_UPPERCASE +
    NEAPOLITAN_UPPERCASE + ASTURIAN_UPPERCASE + ARAGONESE_UPPERCASE +
    OCCITAN_UPPERCASE + WALLOON_UPPERCASE + LADIN_UPPERCASE +
    MIRANDESE_UPPERCASE
))

ALL_LATIN_LETTERS = ALL_LATIN_LOWERCASE + ALL_LATIN_UPPERCASE

# All Cyrillic alphabets combined
ALL_CYRILLIC_LOWERCASE = ''.join(set(
    RUSSIAN_LOWERCASE + UKRAINIAN_LOWERCASE + BULGARIAN_LOWERCASE +
    SERBIAN_CYRILLIC_LOWERCASE + MACEDONIAN_CYRILLIC_LOWERCASE +
    BELARUSIAN_LOWERCASE + MONGOLIAN_CYRILLIC_LOWERCASE +
    KAZAKH_CYRILLIC_LOWERCASE + KYRGYZ_CYRILLIC_LOWERCASE +
    TAJIK_CYRILLIC_LOWERCASE + TATAR_CYRILLIC_LOWERCASE +
    BASHKIR_CYRILLIC_LOWERCASE + CHUVASH_CYRILLIC_LOWERCASE +
    OSSETIAN_CYRILLIC_LOWERCASE + MARI_CYRILLIC_LOWERCASE +
    UDMURT_CYRILLIC_LOWERCASE
))

ALL_CYRILLIC_UPPERCASE = ''.join(set(
    RUSSIAN_UPPERCASE + UKRAINIAN_UPPERCASE + BULGARIAN_UPPERCASE +
    SERBIAN_CYRILLIC_UPPERCASE + MACEDONIAN_CYRILLIC_UPPERCASE +
    BELARUSIAN_UPPERCASE + MONGOLIAN_CYRILLIC_UPPERCASE +
    KAZAKH_CYRILLIC_UPPERCASE + KYRGYZ_CYRILLIC_UPPERCASE +
    TAJIK_CYRILLIC_UPPERCASE + TATAR_CYRILLIC_UPPERCASE +
    BASHKIR_CYRILLIC_UPPERCASE + CHUVASH_CYRILLIC_UPPERCASE +
    OSSETIAN_CYRILLIC_UPPERCASE + MARI_CYRILLIC_UPPERCASE +
    UDMURT_CYRILLIC_UPPERCASE
))

ALL_CYRILLIC = ALL_CYRILLIC_LOWERCASE + ALL_CYRILLIC_UPPERCASE

# All Arabic-based scripts combined
ALL_ARABIC_SCRIPTS = ''.join(set(
    ARABIC_LETTERS + PERSIAN_LETTERS + URDU_LETTERS + 
    PASHTO_LETTERS + KURDISH_ARABIC + SINDHI_LETTERS +
    UYGHUR_ARABIC + JAWI_LETTERS + BALOCHI_ARABIC +
    KASHMIRI_ARABIC
))

# All South Asian scripts combined
ALL_SOUTH_ASIAN = ''.join(set(
    DEVANAGARI_LETTERS + BENGALI_LETTERS + GURMUKHI_LETTERS +
    GUJARATI_LETTERS + ODIA_LETTERS + TAMIL_LETTERS +
    TELUGU_LETTERS + KANNADA_LETTERS + MALAYALAM_LETTERS +
    SINHALA_LETTERS + MARATHI_EXTRA
))

# All scripts combined (mega collection)
ALL_CHARACTERS = (ALL_LATIN_LETTERS + ALL_CYRILLIC + ALL_ARABIC_SCRIPTS + 
                  ALL_SOUTH_ASIAN + THAI_LETTERS + LAO_LETTERS + 
                  KHMER_LETTERS + MYANMAR_LETTERS + JAVANESE_LETTERS +
                  JAVANESE_VOWELS + BALINESE_LETTERS + BALINESE_VOWELS +
                  HIRAGANA + KATAKANA + CHINESE_COMMON + HANGUL_LETTERS +
                  GREEK_LETTERS + HEBREW_FULL + ARMENIAN_LETTERS +
                  GEORGIAN_LETTERS + AMHARIC_LETTERS + TIBETAN_LETTERS +
                  SYRIAC_LETTERS + THAANA_LETTERS + CHEROKEE_LETTERS +
                  IPA_CONSONANTS + IPA_VOWELS + PHOENICIAN + CUNEIFORM_SAMPLE +
                  ALL_DIGITS + PUNCTUATION + CURRENCY_SYMBOLS + MATH_SYMBOLS +
                  ARROWS + MUSIC_SYMBOLS + CHESS_SYMBOLS + CARDS_SYMBOLS +
                  ZODIAC_SYMBOLS + ASTRONOMY_SYMBOLS + WEATHER_SYMBOLS +
                  FRACTIONS + BOX_DRAWING + COMMON_EMOJIS + EMOJI_FLAGS +
                  PERSIAN_HARAKAT + PERSIAN_PUNCTUATION + ARABIC_DIACRITICS
)

# ==================== PRINTABLE CHARACTER SETS ====================

PRINTABLE_ASCII = ASCII_LETTERS + PUNCTUATION_ASCII + DECIMAL_DIGITS
PRINTABLE_LATIN = ALL_LATIN_LETTERS + PUNCTUATION + DECIMAL_DIGITS
PRINTABLE_CYRILLIC = ALL_CYRILLIC + PUNCTUATION + DECIMAL_DIGITS
PRINTABLE_ARABIC = ALL_ARABIC_SCRIPTS + PUNCTUATION + PERSIAN_DIGITS + ARABIC_DIACRITICS + PERSIAN_HARAKAT + PERSIAN_PUNCTUATION
PRINTABLE_SOUTH_ASIAN = ALL_SOUTH_ASIAN + PUNCTUATION + DECIMAL_DIGITS + DEVANAGARI_DIGITS + BENGALI_DIGITS + TAMIL_DIGITS + TELUGU_DIGITS + KANNADA_DIGITS + MALAYALAM_DIGITS + GURMUKHI_DIGITS + GUJARATI_DIGITS + ORIYA_DIGITS
PRINTABLE_EAST_ASIAN = CHINESE_COMMON + HIRAGANA + KATAKANA + HANGUL_LETTERS + PUNCTUATION + DECIMAL_DIGITS
PRINTABLE_GREEK = GREEK_LETTERS + PUNCTUATION + DECIMAL_DIGITS
PRINTABLE_HEBREW = HEBREW_FULL + PUNCTUATION + DECIMAL_DIGITS
PRINTABLE_ARMENIAN = ARMENIAN_LETTERS + PUNCTUATION + DECIMAL_DIGITS
PRINTABLE_GEORGIAN = GEORGIAN_LETTERS + PUNCTUATION + DECIMAL_DIGITS
PRINTABLE_THAI = THAI_LETTERS + PUNCTUATION + THAI_DIGITS
PRINTABLE_LAO = LAO_LETTERS + PUNCTUATION + LAO_DIGITS
PRINTABLE_KHMER = KHMER_LETTERS + PUNCTUATION + KHMER_DIGITS
PRINTABLE_MYANMAR = MYANMAR_LETTERS + PUNCTUATION + MYANMAR_DIGITS
PRINTABLE_TIBETAN = TIBETAN_LETTERS + PUNCTUATION + TIBETAN_DIGITS
PRINTABLE_MONGOLIAN = MONGOLIAN_CYRILLIC_LOWERCASE + MONGOLIAN_CYRILLIC_UPPERCASE + PUNCTUATION + MONGOLIAN_DIGITS
PRINTABLE_CHEROKEE = CHEROKEE_LETTERS + PUNCTUATION + DECIMAL_DIGITS
PRINTABLE_ETHIOPIC = AMHARIC_LETTERS + PUNCTUATION + DECIMAL_DIGITS

# ==================== LANGUAGE-SPECIFIC PRINTABLE SETS ====================

PRINTABLE_GERMAN = GERMAN_LOWERCASE + GERMAN_UPPERCASE + PUNCTUATION + DECIMAL_DIGITS + '€'
PRINTABLE_FRENCH = FRENCH_LOWERCASE + FRENCH_UPPERCASE + PUNCTUATION + DECIMAL_DIGITS + '€'
PRINTABLE_SPANISH = SPANISH_LOWERCASE + SPANISH_UPPERCASE + PUNCTUATION + DECIMAL_DIGITS + '€¿¡'
PRINTABLE_ITALIAN = ITALIAN_LOWERCASE + ITALIAN_UPPERCASE + PUNCTUATION + DECIMAL_DIGITS + '€'
PRINTABLE_PORTUGUESE = PORTUGUESE_LOWERCASE + PORTUGUESE_UPPERCASE + PUNCTUATION + DECIMAL_DIGITS + '€R$'
PRINTABLE_DUTCH = DUTCH_LOWERCASE + DUTCH_UPPERCASE + PUNCTUATION + DECIMAL_DIGITS + '€'
PRINTABLE_POLISH = POLISH_LOWERCASE + POLISH_UPPERCASE + PUNCTUATION + DECIMAL_DIGITS + 'zł'
PRINTABLE_CZECH = CZECH_LOWERCASE + CZECH_UPPERCASE + PUNCTUATION + DECIMAL_DIGITS + 'Kč'
PRINTABLE_TURKISH = TURKISH_LOWERCASE + TURKISH_UPPERCASE + PUNCTUATION + DECIMAL_DIGITS + '₺'
PRINTABLE_VIETNAMESE = VIETNAMESE_LOWERCASE + VIETNAMESE_UPPERCASE + PUNCTUATION + DECIMAL_DIGITS + '₫'
PRINTABLE_RUSSIAN = RUSSIAN_LOWERCASE + RUSSIAN_UPPERCASE + PUNCTUATION + DECIMAL_DIGITS + '₽'
PRINTABLE_UKRAINIAN = UKRAINIAN_LOWERCASE + UKRAINIAN_UPPERCASE + PUNCTUATION + DECIMAL_DIGITS + '₴'
PRINTABLE_ARABIC = ARABIC_ALL_FORMS + PUNCTUATION + PERSIAN_DIGITS + ARABIC_DIACRITICS + '﷼'
PRINTABLE_PERSIAN = PERSIAN_FULL + PUNCTUATION + PERSIAN_DIGITS + PERSIAN_HARAKAT + PERSIAN_PUNCTUATION + '﷼'
PRINTABLE_URDU = URDU_LETTERS + PUNCTUATION + PERSIAN_DIGITS + PERSIAN_HARAKAT + PERSIAN_PUNCTUATION + '₨'
PRINTABLE_HINDI = DEVANAGARI_LETTERS + PUNCTUATION + DEVANAGARI_DIGITS + '₹'
PRINTABLE_BENGALI = BENGALI_LETTERS + PUNCTUATION + BENGALI_DIGITS + '৳'
PRINTABLE_PUNJABI = GURMUKHI_LETTERS + PUNCTUATION + GURMUKHI_DIGITS + '₹'
PRINTABLE_GUJARATI = GUJARATI_LETTERS + PUNCTUATION + GUJARATI_DIGITS + '₹'
PRINTABLE_TAMIL = TAMIL_LETTERS + PUNCTUATION + TAMIL_DIGITS + '₹'
PRINTABLE_TELUGU = TELUGU_LETTERS + PUNCTUATION + TELUGU_DIGITS + '₹'
PRINTABLE_KANNADA = KANNADA_LETTERS + PUNCTUATION + KANNADA_DIGITS + '₹'
PRINTABLE_MALAYALAM = MALAYALAM_LETTERS + PUNCTUATION + MALAYALAM_DIGITS + '₹'
PRINTABLE_JAPANESE = HIRAGANA + KATAKANA + PUNCTUATION + DECIMAL_DIGITS + '¥'
PRINTABLE_CHINESE = CHINESE_COMMON + PUNCTUATION + DECIMAL_DIGITS + '¥'
PRINTABLE_KOREAN = HANGUL_LETTERS + PUNCTUATION + DECIMAL_DIGITS + '₩'

# ==================== FUNCTIONAL CHARACTER SETS ====================

# URL-safe characters
URL_SAFE = ASCII_LOWERCASE + ASCII_UPPERCASE + DECIMAL_DIGITS + '-._~'

# Base64 character set
BASE64_CHARS = ASCII_UPPERCASE + ASCII_LOWERCASE + DECIMAL_DIGITS + '+/='

# Hexadecimal character set
HEX_CHARS = DECIMAL_DIGITS + 'ABCDEF'

# Identifier-safe characters (for programming languages)
IDENTIFIER_CHARS = ASCII_LETTERS + DECIMAL_DIGITS + '_'

# Password-safe special characters (commonly accepted)
PASSWORD_SPECIAL = '!@#$%^&*()-_=+[]{}|;:,.<>?/~`'

# Email local-part allowed characters
EMAIL_LOCAL_CHARS = ASCII_LETTERS + DECIMAL_DIGITS + '!#$%&\'*+-/=?^_`{|}~.'

# Domain name allowed characters
DOMAIN_CHARS = ASCII_LOWERCASE + DECIMAL_DIGITS + '-.'

# ==================== LANGUAGE GROUP SETS ====================

# Germanic languages
GERMANIC_LANGUAGES_CHARS = ''.join(set(
    GERMAN_LOWERCASE + GERMAN_UPPERCASE +
    DUTCH_LOWERCASE + DUTCH_UPPERCASE +
    SWEDISH_LOWERCASE + SWEDISH_UPPERCASE +
    NORWEGIAN_LOWERCASE + NORWEGIAN_UPPERCASE +
    DANISH_LOWERCASE + DANISH_UPPERCASE +
    ICELANDIC_LOWERCASE + ICELANDIC_UPPERCASE +
    LUXEMBOURGISH_LOWERCASE + LUXEMBOURGISH_UPPERCASE
))

# Romance languages
ROMANCE_LANGUAGES_CHARS = ''.join(set(
    FRENCH_LOWERCASE + FRENCH_UPPERCASE +
    SPANISH_LOWERCASE + SPANISH_UPPERCASE +
    ITALIAN_LOWERCASE + ITALIAN_UPPERCASE +
    PORTUGUESE_LOWERCASE + PORTUGUESE_UPPERCASE +
    ROMANIAN_LOWERCASE + ROMANIAN_UPPERCASE +
    CATALAN_LOWERCASE + CATALAN_UPPERCASE +
    GALICIAN_LOWERCASE + GALICIAN_UPPERCASE
))

# Slavic languages (Latin script)
SLAVIC_LATIN_CHARS = ''.join(set(
    POLISH_LOWERCASE + POLISH_UPPERCASE +
    CZECH_LOWERCASE + CZECH_UPPERCASE +
    SLOVAK_LOWERCASE + SLOVAK_UPPERCASE +
    CROATIAN_LOWERCASE + CROATIAN_UPPERCASE +
    SLOVENE_LOWERCASE + SLOVENE_UPPERCASE +
    BOSNIAN_LOWERCASE + BOSNIAN_UPPERCASE +
    SERBIAN_LATIN_LOWERCASE + SERBIAN_LATIN_UPPERCASE +
    MONTENEGRIN_LATIN_LOWERCASE + MONTENEGRIN_LATIN_UPPERCASE
))

# Slavic languages (Cyrillic script)
SLAVIC_CYRILLIC_CHARS = ''.join(set(
    RUSSIAN_LOWERCASE + RUSSIAN_UPPERCASE +
    UKRAINIAN_LOWERCASE + UKRAINIAN_UPPERCASE +
    BULGARIAN_LOWERCASE + BULGARIAN_UPPERCASE +
    SERBIAN_CYRILLIC_LOWERCASE + SERBIAN_CYRILLIC_UPPERCASE +
    MACEDONIAN_CYRILLIC_LOWERCASE + MACEDONIAN_CYRILLIC_UPPERCASE +
    BELARUSIAN_LOWERCASE + BELARUSIAN_UPPERCASE
))

# Turkic languages
TURKIC_LANGUAGES_CHARS = ''.join(set(
    TURKISH_LOWERCASE + TURKISH_UPPERCASE +
    AZERBAIJANI_LOWERCASE + AZERBAIJANI_UPPERCASE +
    TURKMEN_LOWERCASE + TURKMEN_UPPERCASE +
    CRIMEAN_TATAR_LOWERCASE + CRIMEAN_TATAR_UPPERCASE
))

# ==================== TEXT CLASSIFICATION SETS ====================

# Characters that indicate bidirectional text
BIDI_CHARS = ALL_ARABIC_SCRIPTS + HEBREW_FULL + SYRIAC_LETTERS + PERSIAN_LETTERS + URDU_LETTERS

# Characters that are typically right-to-left
RTL_CHARS = ALL_ARABIC_SCRIPTS + HEBREW_FULL + SYRIAC_LETTERS + THAANA_LETTERS

# Characters that are typically left-to-right
LTR_CHARS = ALL_LATIN_LETTERS + ALL_CYRILLIC + GREEK_LETTERS

# Characters that are typically top-to-bottom (for reference, some Asian scripts)
TTB_CHARS = CHINESE_COMMON + JAPANESE_LETTERS + HANGUL_LETTERS

# ==================== USAGE CATEGORIES ====================

# Characters suitable for UI display
UI_SAFE_CHARS = (ALL_LATIN_LETTERS + ALL_CYRILLIC + DECIMAL_DIGITS + 
                 PUNCTUATION_ASCII + WHITESPACE_STANDARD + CURRENCY_SYMBOLS)

# Characters suitable for filenames (OS-dependent, conservative)
FILENAME_SAFE_CHARS = ASCII_LETTERS + DECIMAL_DIGITS + '._-'

# Characters suitable for XML/HTML content
XML_SAFE_CHARS = (ALL_CHARACTERS.replace('&', '').replace('<', '')
                  .replace('>', '').replace('"', '').replace("'", ""))

# Characters requiring escaping in HTML
HTML_ESCAPE_CHARS = '<>&"\''

# Characters requiring escaping in XML
XML_ESCAPE_CHARS = '<>&"\''

# Characters requiring escaping in JSON
JSON_ESCAPE_CHARS = '"\\/\b\f\n\r\t'

# Characters requiring escaping in Python strings
PYTHON_ESCAPE_CHARS = '\n\r\t\\\'\"\a\b\f\v'

# ==================== METRICS AND STATISTICS ====================

# Count total unique characters in mega collection
UNIQUE_ALL_CHARACTERS = ''.join(set(ALL_CHARACTERS))
TOTAL_UNIQUE_CHARS = len(UNIQUE_ALL_CHARACTERS)

# Language coverage statistics
LATIN_LANGUAGES_COUNT = 54  # Number of Latin-based languages included
CYRILLIC_LANGUAGES_COUNT = 16  # Number of Cyrillic-based languages included
ARABIC_LANGUAGES_COUNT = 10  # Number of Arabic-based languages included
SOUTH_ASIAN_LANGUAGES_COUNT = 12  # Number of South Asian languages included
TOTAL_LANGUAGES_COVERED = (LATIN_LANGUAGES_COUNT + CYRILLIC_LANGUAGES_COUNT + 
                           ARABIC_LANGUAGES_COUNT + SOUTH_ASIAN_LANGUAGES_COUNT + 
                           10)  # +10 for additional scripts

# ==================== CHARACTER PROPERTY MAPPINGS ====================

# Mapping of common characters to their Unicode categories (simplified)
CHAR_CATEGORY_MAP = {
    'LETTERS': ALL_LATIN_LETTERS + ALL_CYRILLIC + ALL_ARABIC_SCRIPTS + ALL_SOUTH_ASIAN + 
               GREEK_LETTERS + HEBREW_FULL + ARMENIAN_LETTERS + GEORGIAN_LETTERS,
    'DIGITS': ALL_DIGITS,
    'PUNCTUATION': PUNCTUATION,
    'SYMBOLS': CURRENCY_SYMBOLS + MATH_SYMBOLS + ARROWS,
    'WHITESPACE': WHITESPACE_ALL,
    'EMOJI': COMMON_EMOJIS + EMOJI_FLAGS
}

# ASCII character type classification
ASCII_LETTER_CHARS = ASCII_LETTERS
ASCII_DIGIT_CHARS = DECIMAL_DIGITS
ASCII_PUNCT_CHARS = PUNCTUATION_ASCII
ASCII_WHITESPACE_CHARS = WHITESPACE_STANDARD
ASCII_CONTROL_CHARS = ''.join(chr(i) for i in range(32)) + chr(127)
ASCII_PRINTABLE_CHARS = ''.join(chr(i) for i in range(32, 127))

# ==================== STRING VALIDATION PATTERNS ====================

# Common character classes for regex-like validation
ALPHA_CHARS = ALL_LATIN_LETTERS + ALL_CYRILLIC + GREEK_LETTERS
ALPHANUMERIC_CHARS = ALPHA_CHARS + DECIMAL_DIGITS
ALPHANUMERIC_EXTENDED = ALPHANUMERIC_CHARS + '_-'
NUMERIC_CHARS = DECIMAL_DIGITS + '.-+eE'
INTEGER_CHARS = DECIMAL_DIGITS + '-'
FLOAT_CHARS = DECIMAL_DIGITS + '.-+eE'
HEX_NUMERIC_CHARS = HEX_DIGITS + 'xX'
OCTAL_NUMERIC_CHARS = OCTAL_DIGITS + 'oO'
BINARY_NUMERIC_CHARS = BINARY_DIGITS + 'bB'

# ==================== SPECIAL CHARACTER SUBSETS ====================

# Characters that appear as whitespace but aren't standard
INVISIBLE_CHARS = WHITESPACE_EXTRA + '\u200b\u200c\u200d\u200e\u200f\u2060\ufeff\u00ad'

# Characters that can be confused visually (homoglyphs)
HOMOGLYPH_LATIN_A = 'AΑАᎪ'
HOMOGLYPH_LATIN_B = 'BΒВᏴ'
HOMOGLYPH_LATIN_E = 'EΕЕ'
HOMOGLYPH_LATIN_H = 'HΗНᎻ'
HOMOGLYPH_LATIN_I = 'IΙІӀ'
HOMOGLYPH_LATIN_K = 'KΚКᏦ'
HOMOGLYPH_LATIN_M = 'MΜМᎷ'
HOMOGLYPH_LATIN_N = 'NΝΝᏁ'
HOMOGLYPH_LATIN_O = 'OΟОՕ'
HOMOGLYPH_LATIN_P = 'PΡРᏢ'
HOMOGLYPH_LATIN_T = 'TΤТᎢ'
HOMOGLYPH_LATIN_X = 'XΧХᚷ'
HOMOGLYPH_LATIN_Y = 'YΥҮ'

# Zero-width characters (security concern)
ZERO_WIDTH_CHARS = '\u200b\u200c\u200d\u200e\u200f\u2060\ufeff\u00ad\u034f\u061c\u2061\u2062\u2063\u2064'

# Characters that change text direction
DIRECTION_CHARS = '\u200e\u200f\u061c\u202a\u202b\u202c\u202d\u202e\u2066\u2067\u2068\u2069'

# ==================== DATABASE AND STORAGE ====================

# Characters safe for SQL identifiers (without quoting)
SQL_IDENTIFIER_CHARS = ASCII_LETTERS + DECIMAL_DIGITS + '_'

# Characters commonly used in Base32 encoding
BASE32_CHARS = ASCII_UPPERCASE + '234567='

# Characters used in Crockford's Base32
CROCKFORD_BASE32 = '0123456789ABCDEFGHJKMNPQRSTVWXYZ'

# ==================== DISPLAY AND RENDERING ====================

# Characters with descenders in Latin script
DESCENDER_CHARS = 'gjpqyQ'

# Characters with ascenders in Latin script
ASCENDER_CHARS = 'bdfhikltABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Monospace digit equivalents
MONOSPACE_DIGITS = DECIMAL_DIGITS  # All standard digits are typically monospace

# Variable-width characters (typical)
VARIABLE_WIDTH_CHARS = ALL_LATIN_LETTERS + ALL_CYRILLIC

# Full-width characters (East Asian)
FULLWIDTH_CHARS = 'ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ０１２３４５６７８９'

# Half-width characters
HALFWIDTH_CHARS = 'ｦｧｨｩｪｫｬｭｮｯｰｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝﾞﾟ'

# ==================== HISTORICAL AND RARE SCRIPTS ====================

# Runic
RUNIC_CHARS = 'ᚠᚡᚢᚣᚤᚥᚦᚧᚨᚩᚪᚫᚬᚭᚮᚯᚰᚱᚲᚳᚴᚵᚶᚷᚸᚹᚺᚻᚼᚽᚾᚿᛀᛁᛂᛃᛄᛅᛆᛇᛈᛉᛊᛋᛌᛍᛎᛏ'

# Ogham
OGHAM_CHARS = 'ᚁᚂᚃᚄᚅᚆᚇᚈᚉᚊᚋᚌᚍᚎᚏᚐᚑᚒᚓᚔᚕᚖᚗᚘᚙ'

# Gothic
GOTHIC_CHARS = '𐌰𐌱𐌲𐌳𐌴𐌵𐌶𐌷𐌸𐌹𐌺𐌻𐌼𐌽𐌾𐌿𐍀𐍁𐍂𐍃𐍄𐍅𐍆𐍇𐍈𐍉'

# Deseret
DESERET_CHARS = '𐐀𐐁𐐂𐐃𐐄𐐅𐐆𐐇𐐈𐐉𐐊𐐋𐐌𐐍𐐎𐐏𐐐𐐑𐐒𐐓𐐔𐐕𐐖𐐗𐐘𐐙𐐚𐐛𐐜𐐝𐐞𐐟𐐠𐐡𐐢𐐣𐐤𐐥𐐦𐐧'

# ==================== EXPORT CONFIGURATIONS ====================

# Character sets organized by encoding compatibility
ASCII_COMPATIBLE = PRINTABLE_ASCII
LATIN1_COMPATIBLE = ALL_LATIN_LETTERS + PUNCTUATION_ASCII + DECIMAL_DIGITS  # ISO 8859-1 approximate
UTF8_COMPATIBLE = ALL_CHARACTERS  # All characters are UTF-8 compatible
UTF16_COMPATIBLE = ALL_CHARACTERS  # All characters are UTF-16 compatible

# Byte order marks
BOM_UTF8 = '\ufeff'
BOM_UTF16_LE = '\ufffe'
BOM_UTF16_BE = '\ufeff'
BOM_UTF32_LE = '\ufffe'
BOM_UTF32_BE = '\ufeff'

