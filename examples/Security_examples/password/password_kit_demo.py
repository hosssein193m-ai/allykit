
from allykit.Security_kit.password_kit import (
    # Password generation
    generate_password,
    generate_strong_password,
    generate_timed_password,
    wrap_password_with_time,
    generate_password_with_prefix_suffix,
    
    # Character generation
    choice_string,
    choice_string_yield,
    str_choice_string,
    list_choice_string,
    
    # Classes
    Review_Password,
    Time_Password,
    
    # Aliases
    WPWT, GTP, GP, GSP, G,
    CS, CSY, SCS, LCS,
    ReviewPassword,
    TimePassword,
)

from datetime import datetime, timedelta
import json


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_result(label, result, max_length=100):
    """Print a formatted result."""
    if isinstance(result, dict):
        print(f"  → {label}:")
        for key, value in result.items():
            if isinstance(value, dict):
                print(f"      {key}:")
                for k, v in value.items():
                    if isinstance(v, (int, float, str, bool)):
                        print(f"        {k}: {v}")
                    else:
                        print(f"        {k}: {str(v)[:50]}...")
            elif isinstance(value, list):
                print(f"      {key}: {len(value)} items")
            else:
                print(f"      {key}: {value}")
    elif isinstance(result, str) and len(result) > max_length:
        print(f"  → {label}: {result[:max_length]}...")
    else:
        print(f"  → {label}: {result}")


# ============================================
# PART 1: BASIC PASSWORD GENERATION
# ============================================
print_section("PART 1: BASIC PASSWORD GENERATION")

# 1.1 Simple password
print("\n--- 1.1 Simple Password ---")
simple_pwd = generate_password(length=12)
print_result("Simple password (12 chars)", simple_pwd)

# 1.2 Custom charset
print("\n--- 1.2 Custom Charset Password ---")
digit_only = generate_password(length=8, charset="0123456789")
print_result("Digits only", digit_only)

# 1.3 Password with prefix/suffix
print("\n--- 1.3 Password with Prefix/Suffix ---")
prefixed = generate_password_with_prefix_suffix(
    length=10,
    prefix="SEC_",
    suffix=False
)
print_result("With prefix", prefixed)

suffixed = generate_password_with_prefix_suffix(
    length=10,
    prefix="_END",
    suffix=True
)
print_result("With suffix", suffixed)

# 1.4 Strong password
print("\n--- 1.4 Strong Password ---")
strong_pwd = generate_strong_password(
    include_uppercase=True,
    include_digits=True,
    include_symbols=True,
    length=20
)
print_result("Strong password", strong_pwd)

# 1.5 Using aliases
print("\n--- 1.5 Using Aliases ---")
pwd_g = G(length=12)
pwd_gsp = GSP(include_uppercase=True, include_digits=True, length=15)
print_result("G() alias", pwd_g)
print_result("GSP() alias", pwd_gsp)


# ============================================
# PART 2: CHARACTER GENERATION
# ============================================
print_section("PART 2: CHARACTER GENERATION")

# 2.1 Single character
print("\n--- 2.1 Single Character ---")
char = CS()
print_result("Random character", char)

# 2.2 String of characters
print("\n--- 2.2 String of Characters ---")
str_chars = SCS(add=10)
print_result("Random string (10 chars)", str_chars)

# 2.3 List of characters
print("\n--- 2.3 List of Characters ---")
char_list = LCS(add=5)
print_result("Character list", char_list)

# 2.4 Custom charset
print("\n--- 2.4 Custom Charset ---")
custom_chars = SCS(charset="ABC123", add=8)
print_result("Custom charset (ABC123, 8 chars)", custom_chars)

# 2.5 Using aliases
print("\n--- 2.5 Character Aliases ---")
print(f"  CS() → {CS()}")
print(f"  SCS(add=5) → {SCS(add=5)}")
print(f"  LCS(add=3) → {LCS(add=3)}")


# ============================================
# PART 3: TIME-BASED PASSWORDS
# ============================================
print_section("PART 3: TIME-BASED PASSWORDS")

# 3.1 Generate timed password (default 10 days)
print("\n--- 3.1 Generate Timed Password (Default) ---")
timed_pwd = generate_timed_password()
print_result("Timed password (10 days)", timed_pwd, 80)

# 3.2 Generate timed password with custom duration
print("\n--- 3.2 Generate Timed Password (Custom) ---")
pwd_1hour = generate_timed_password('hours.1')
print_result("Valid for 1 hour", pwd_1hour, 80)

pwd_5min = generate_timed_password('minutes.5')
print_result("Valid for 5 minutes", pwd_5min, 80)

pwd_30sec = generate_timed_password('seconds.30')
print_result("Valid for 30 seconds", pwd_30sec, 80)

# 3.3 Generate timed password with custom charset
print("\n--- 3.3 Timed Password with Custom Charset ---")
pwd_digits = generate_timed_password('days.1', charset="0123456789")
print_result("Digits only, 1 day", pwd_digits, 80)

# 3.4 Using GTP alias
print("\n--- 3.4 Using GTP Alias ---")
pwd_alias = GTP('days.7')
print_result("GTP alias (7 days)", pwd_alias, 80)

# 3.5 Wrap existing password
print("\n--- 3.5 Wrap Existing Password ---")
original = "MySecretPassword123!"
wrapped = wrap_password_with_time(original, 'hours.2')
print_result("Wrapped password (2 hours)", wrapped, 80)

# 3.6 Wrap with WPWT alias
print("\n--- 3.6 WPWT Alias ---")
wrapped_alias = WPWT("API_KEY_12345", 'days.30')
print_result("WPWT alias (30 days)", wrapped_alias, 80)

# 3.7 Generating function (auto-detect)
print("\n--- 3.7 Generating Function ---")
from allykit.Security_kit.password_kit.Time_based_password import generating_password

new_pwd = generating_password(time='hours.3')
print_result("generating_password() - new", new_pwd, 80)

wrapped_pwd = generating_password(password="MyToken", time='days.5')
print_result("generating_password() - wrapped", wrapped_pwd, 80)


# ============================================
# PART 4: TIME_PASSWORD CLASS
# ============================================
print_section("PART 4: TIME_PASSWORD CLASS")

# 4.1 Create Time_Password instance
print("\n--- 4.1 Create Time_Password ---")
time_pwd = Time_Password(timed_pwd)
print_result("Time_Password created", time_pwd)

# 4.2 Get password components
print("\n--- 4.2 Get Components ---")
print_result("Start time", time_pwd.start_time())
print_result("End time", time_pwd.end_time())
print_result("Actual password", time_pwd.get_password())

# 4.3 Check validity
print("\n--- 4.3 Check Validity ---")
print_result("Is password valid?", time_pwd.is_password_valid())
print_result("Is password expired?", time_pwd.is_expired())

# 4.4 Time remaining
print("\n--- 4.4 Time Remaining ---")
remaining = time_pwd.time_remaining()
if isinstance(remaining, timedelta):
    print(f"  → Time remaining: {remaining.total_seconds():.0f} seconds")
    print(f"  → Days: {remaining.days}, Hours: {remaining.seconds // 3600}")
else:
    print_result("Time remaining", remaining)

# 4.5 Status dictionary
print("\n--- 4.5 Status Dictionary ---")
status = time_pwd.status_password()
print_result("Full status", status)

# 4.6 to_dict() method
print("\n--- 4.6 to_dict() Method ---")
# With security (hashed)
dict_secure = time_pwd.to_dict(security=True)
print_result("Secure dict (hashed)", dict_secure)

# Without security (plain)
dict_plain = time_pwd.to_dict(security=False)
print_result("Plain dict (unhashed)", dict_plain)

# 4.7 String representation
print("\n--- 4.7 String Representation ---")
print(f"  str(): {time_pwd}")
print(f"  repr(): {repr(time_pwd)}")

# 4.8 Create Time_Password from wrapped password
print("\n--- 4.8 From Wrapped Password ---")
wrapped_time_pwd = Time_Password(wrapped)
print_result("Time_Password from wrapped", wrapped_time_pwd)
print_result("Wrapped password valid?", wrapped_time_pwd.is_password_valid())

# 4.9 Using TimePassword alias
print("\n--- 4.9 TimePassword Alias ---")
tp_alias = TimePassword(timed_pwd)
print_result("TimePassword alias", tp_alias)
print_result("Valid?", tp_alias.is_password_valid())


# ============================================
# PART 5: REVIEW_PASSWORD CLASS
# ============================================
print_section("PART 5: REVIEW_PASSWORD CLASS")

# 5.1 Create Review_Password instance
print("\n--- 5.1 Create Review_Password ---")
weak_pwd = "password123"
strong_pwd = "K#9mP$2vL!qR@7xZ9"

review_weak = Review_Password(weak_pwd)
review_strong = Review_Password(strong_pwd)

print_result("Weak password review created", review_weak)
print_result("Strong password review created", review_strong)

# 5.2 Password check (various formats)
print("\n--- 5.2 Password Check (Boolean) ---")
result_bool = review_strong.password_check(types="bool")
print_result("Strong password meets all criteria?", result_bool)

print("\n--- 5.3 Password Check (Dictionary) ---")
result_dict = review_strong.password_check(types="dict")
print_result("Detailed check (dict)", result_dict)

print("\n--- 5.4 Password Check (List) ---")
result_list = review_strong.password_check(types="list")
print_result("Detailed check (list)", result_list)

print("\n--- 5.5 Password Check (String) ---")
result_str = review_strong.password_check(types="str")
print_result("Detailed check (string)", result_str)

# 5.6 Entropy score
print("\n--- 5.6 Entropy Score ---")
score_weak = review_weak.Entropy_Score_Password()
score_strong = review_strong.Entropy_Score_Password()

print_result("Weak password score (0-10)", score_weak)
print_result("Strong password score (0-10)", score_strong)

# 5.7 Compare weak vs strong
print("\n--- 5.7 Comparison: Weak vs Strong ---")
print("  Weak password analysis:")
weak_dict = review_weak.password_check(types="dict")
for key, value in weak_dict.items():
    if key != 'status' and isinstance(value, bool):
        print(f"    {key}: {'✅' if value else '❌'}")

print("\n  Strong password analysis:")
strong_dict = review_strong.password_check(types="dict")
for key, value in strong_dict.items():
    if key != 'status' and isinstance(value, bool):
        print(f"    {key}: {'✅' if value else '❌'}")

# 5.8 Using ReviewPassword alias
print("\n--- 5.8 ReviewPassword Alias ---")
review_alias = ReviewPassword("Test@123")
print_result("ReviewPassword alias", review_alias)
print_result("Score", review_alias.Entropy_Score_Password())


# ============================================
# PART 6: REAL-WORLD USE CASES
# ============================================
print_section("PART 6: REAL-WORLD USE CASES")

# 6.1 Temporary API Key
print("\n--- 6.1 Temporary API Key ---")
api_key = GTP('hours.24')
print(f"  API Key: {api_key[:50]}...")
api_time = Time_Password(api_key)
print(f"  Valid until: {api_time.end_time()}")
print(f"  Is valid now? {api_time.is_password_valid()}")

# 6.2 User Registration with Strong Password
print("\n--- 6.2 User Registration ---")
user_password = GSP(include_uppercase=True, include_digits=True, include_symbols=True, length=16)
review = Review_Password(user_password)
score = review.Entropy_Score_Password()

print(f"  Generated password: {user_password}")
print(f"  Entropy score: {score}/10")
print(f"  Meets requirements: {review.password_check(types='bool')}")

if score >= 7:
    print("  ✅ Password is strong enough")
else:
    print("  ⚠️ Password needs improvement")

# 6.3 Session Token with Expiration
print("\n--- 6.3 Session Token ---")
session_token = GTP('hours.2', charset="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
print(f"  Session token: {session_token[:60]}...")
token = Time_Password(session_token)
print(f"  Created: {token.start_time()}")
print(f"  Expires: {token.end_time()}")
remaining = token.time_remaining()
if isinstance(remaining, timedelta):
    print(f"  Time remaining: {remaining.total_seconds()/60:.0f} minutes")

# 6.4 Password Rotation
print("\n--- 6.4 Password Rotation ---")
old_password = "OldPassword123!"
print(f"  Old password: {old_password}")

# Wrap old password with expiration
rotated = WPWT(old_password, 'days.7')
print(f"  Rotated password (valid 7 days): {rotated[:60]}...")
rotated_obj = Time_Password(rotated)
print(f"  New expiry: {rotated_obj.end_time()}")
print(f"  Is valid? {rotated_obj.is_password_valid()}")

# 6.5 Bulk Password Generation
print("\n--- 6.5 Bulk Password Generation ---")
print("  Generating 5 strong passwords:")
for i in range(5):
    pwd = GSP(include_uppercase=True, include_digits=True, include_symbols=True, length=12)
    score = Review_Password(pwd).Entropy_Score_Password()
    print(f"    {i+1}: {pwd} (Score: {score}/10)")

# 6.6 Password Audit
print("\n--- 6.6 Password Audit ---")
test_passwords = [
    "123456",
    "password",
    "Password123!",
    "K#9mP$2vL!qR@7xZ9",
    "hello_world",
    "MySecureP@ssw0rd2024!"
]

print("  Auditing passwords:")
for pwd in test_passwords:
    review = Review_Password(pwd)
    score = review.Entropy_Score_Password()
    status = review.password_check(types='bool')
    status_text = "✅" if status else "❌"
    print(f"    {status_text} '{pwd}': Score={score}/10")


# ============================================
# PART 7: ERROR HANDLING
# ============================================
print_section("PART 7: ERROR HANDLING")

# 7.1 Invalid Time_Password
print("\n--- 7.1 Invalid Time_Password ---")
try:
    invalid = Time_Password("invalid_password")
except ValueError as e:
    print(f"  ✅ Caught error: {e}")

# 7.2 Invalid time format
print("\n--- 7.2 Invalid Time Format ---")
try:
    invalid_time = GTP('invalid.10')
except (ValueError, AttributeError) as e:
    print(f"  ✅ Caught error: {e}")

# 7.3 Invalid charset
print("\n--- 7.3 Invalid Charset ---")
try:
    empty_pwd = generate_password(length=10, charset="")
except ValueError as e:
    print(f"  ✅ Caught error: {e}")

# 7.4 add > length
print("\n--- 7.4 add > length ---")
try:
    pwd = generate_password(length=5, add=10)
except ValueError as e:
    print(f"  ✅ Caught error: {e}")

# 7.5 Invalid types in password_check
print("\n--- 7.5 Invalid types ---")
try:
    review = Review_Password("test")
    review.password_check(types="invalid")
except TypeError as e:
    print(f"  ✅ Caught error: {e}")


# ============================================
# PART 8: PERFORMANCE & BENCHMARKING
# ============================================
print_section("PART 8: PERFORMANCE & BENCHMARKING")

import time as time_module

# 8.1 Generation speed
print("\n--- 8.1 Generation Speed ---")
start = time_module.time()
for _ in range(100):
    G(length=10)
end = time_module.time()
print(f"  100 simple passwords: {end-start:.4f} seconds")

start = time_module.time()
for _ in range(50):
    GSP(include_uppercase=True, include_digits=True, include_symbols=True)
end = time_module.time()
print(f"  50 strong passwords: {end-start:.4f} seconds")

# 8.2 Validation speed
print("\n--- 8.2 Validation Speed ---")
test_pwd = GSP(include_uppercase=True, include_digits=True, include_symbols=True)
start = time_module.time()
for _ in range(100):
    Review_Password(test_pwd).password_check(types='bool')
end = time_module.time()
print(f"  100 validations: {end-start:.4f} seconds")


# ============================================
# PART 9: CLEANUP
# ============================================
print_section("PART 9: SUMMARY")

print("\n  ✅ ALL DEMONSTRATIONS COMPLETED SUCCESSFULLY!")

print("\n📊 SUMMARY OF OPERATIONS:")
print("=" * 70)
print("  ✅ Basic password generation")
print("  ✅ Strong password generation")
print("  ✅ Custom charset passwords")
print("  ✅ Password with prefix/suffix")
print("  ✅ Character generation (single, string, list)")
print("  ✅ Time-based password generation")
print("  ✅ Password wrapping with timestamps")
print("  ✅ Time_Password class (validation, expiry, status)")
print("  ✅ Review_Password class (validation, scoring)")
print("  ✅ Entropy scoring (0-10 scale)")
print("  ✅ Multiple output formats (bool, dict, list, str)")
print("  ✅ Real-world use cases (API keys, sessions, rotation)")
print("  ✅ Error handling")
print("  ✅ Performance benchmarking")

print("\n📌 KEY FUNCTIONS & CLASSES:")
print("=" * 70)
print("  🔹 generate_password()        - Simple password")
print("  🔹 generate_strong_password() - Strong password")
print("  🔹 generate_timed_password()  - Time-limited password")
print("  🔹 wrap_password_with_time()  - Wrap existing password")
print("  🔹 Time_Password              - Manage timed passwords")
print("  🔹 Review_Password            - Validate & score passwords")
print("  🔹 choice_string()            - Random character")
print("  🔹 str_choice_string()        - Random string")
print("  🔹 list_choice_string()       - Character list")

print("\n📌 ALIASES AVAILABLE:")
print("=" * 70)
print("  🔸 G   → generate_password")
print("  🔸 GSP → generate_strong_password")
print("  🔸 GTP → generate_timed_password")
print("  🔸 WPWT → wrap_password_with_time")
print("  🔸 CS  → choice_string")
print("  🔸 SCS → str_choice_string")
print("  🔸 LCS → list_choice_string")
print("  🔸 ReviewPassword → Review_Password")
print("  🔸 TimePassword → Time_Password")

print("\n" + "=" * 70)
print("🎯 DEMONSTRATION COMPLETE!")
print("=" * 70)