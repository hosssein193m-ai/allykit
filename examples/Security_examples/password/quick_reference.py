
from allykit.Security_kit.password_kit import (
    # Generation
    generate_password, G,
    generate_strong_password, GSP,
    generate_timed_password, GTP,
    wrap_password_with_time, WPWT,
    generate_password_with_prefix_suffix,
    
    # Character generation
    choice_string, CS,
    str_choice_string, SCS,
    list_choice_string, LCS,
    
    # Classes
    Review_Password, ReviewPassword,
    Time_Password, TimePassword,
)


# ============================================
# 1. QUICK PASSWORD GENERATION
# ============================================
print("=" * 60)
print("1. QUICK PASSWORD GENERATION")
print("=" * 60)

# 1-liner passwords
print(f"Simple:     {G(12)}")
print(f"Strong:     {GSP(include_uppercase=True, include_digits=True, length=16)}")
print(f"Digits:     {generate_password(6, charset='0123456789')}")
print(f"Prefix:     {generate_password_with_prefix_suffix(8, prefix='PWD_')}")

# Character generation
print(f"Character:  {CS()}")
print(f"String:     {SCS(add=8)}")
print(f"List:       {LCS(add=4)}")


# ============================================
# 2. TIME-BASED PASSWORDS
# ============================================
print("\n" + "=" * 60)
print("2. TIME-BASED PASSWORDS")
print("=" * 60)

# Generate timed passwords
timed = GTP('days.1')
print(f"1-day token: {timed[:50]}...")

timed_hours = GTP('hours.2')
print(f"2-hour token: {timed_hours[:50]}...")

# Wrap existing password
wrapped = WPWT("MySecret", 'minutes.30')
print(f"Wrapped (30min): {wrapped[:50]}...")


# ============================================
# 3. PASSWORD VALIDATION
# ============================================
print("\n" + "=" * 60)
print("3. PASSWORD VALIDATION")
print("=" * 60)

# Check if timed password is valid
tp = TimePassword(timed)
print(f"Is valid? {tp.is_password_valid()}")
print(f"Remaining: {tp.time_remaining().total_seconds():.0f}s" if tp.is_password_valid() else "Expired!")

# Get status
status = tp.status_password()
print(f"Score: {status['Password security']['score']}/10")


# ============================================
# 4. PASSWORD STRENGTH
# ============================================
print("\n" + "=" * 60)
print("4. PASSWORD STRENGTH")
print("=" * 60)

# Test passwords
weak = "password123"
strong = "K#9mP$2vL!qR@7xZ9"

review = ReviewPassword(weak)
print(f"Weak password '{weak}':")
print(f"  - Meets all criteria? {review.password_check(types='bool')}")
print(f"  - Entropy score: {review.Entropy_Score_Password()}/10")

review = ReviewPassword(strong)
print(f"Strong password '{strong}':")
print(f"  - Meets all criteria? {review.password_check(types='bool')}")
print(f"  - Entropy score: {review.Entropy_Score_Password()}/10")

# Detailed check
details = review.password_check(types='dict')
print(f"  - Details: {details}")


# ============================================
# 5. REAL-WORLD USE CASES
# ============================================
print("\n" + "=" * 60)
print("5. REAL-WORLD USE CASES")
print("=" * 60)

# API Key with 24-hour expiry
api_key = GTP('hours.24', charset="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
print(f"API Key: {api_key[:40]}...")
api = TimePassword(api_key)
print(f"Expires: {api.end_time()}")

# Generate strong user password
user_pwd = GSP(include_uppercase=True, include_digits=True, include_symbols=True, length=16)
score = ReviewPassword(user_pwd).Entropy_Score_Password()
print(f"User password: {user_pwd} (Score: {score}/10)")

# Password rotation
old = "old_password"
rotated = WPWT(old, 'days.7')
print(f"Rotated: {rotated[:40]}...")


# ============================================
# 6. QUICK REFERENCE TABLE
# ============================================
print("\n" + "=" * 60)
print("6. QUICK REFERENCE TABLE")
print("=" * 60)

print("\nGENERATION:")
print("  G(length)                  → Simple password")
print("  GSP(...)                   → Strong password")
print("  GTP(time, charset)         → Timed password")
print("  WPWT(password, time)       → Wrap password")
print("  CS()                       → Random character")
print("  SCS(add)                   → Random string")
print("  LCS(add)                   → Character list")

print("\nCLASSES:")
print("  TimePassword(pwd)          → Manage timed password")
print("    .is_password_valid()     → Check if valid")
print("    .time_remaining()        → Get remaining time")
print("    .status_password()       → Get full status")
print("    .to_dict()               → Export as dict")

print("\n  ReviewPassword(pwd)        → Validate password")
print("    .password_check()        → Check criteria")
print("    .Entropy_Score_Password()→ Get score (0-10)")

print("\n" + "=" * 60)
print("✅ QUICK REFERENCE COMPLETE!")
print("=" * 60)