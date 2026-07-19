
from allykit.Security_kit.hash_kit import (
    hash_password, HP,
    hash_file, HF,
    generate_salt,
    hash_with_salt, HWS,
    verify_password, VP,
    double_hash, DH,
    detect_hash_algorithm, DHA,
    smart_hash_detector, SHD,
    hash_url, HU,
    compare_hash, CH,
    find_matching_hashes, FMH,
)

import os
import tempfile


def print_result(label, result):
    """Print a formatted result."""
    if isinstance(result, dict):
        print(f"  {label}:")
        for k, v in result.items():
            if isinstance(v, str) and len(v) > 30:
                print(f"    {k}: {v[:30]}...")
            else:
                print(f"    {k}: {v}")
    elif isinstance(result, str) and len(result) > 50:
        print(f"  {label}: {result[:50]}...")
    else:
        print(f"  {label}: {result}")


# ============================================
# 1. QUICK HASHING
# ============================================
print("=" * 60)
print("1. QUICK HASHING")
print("=" * 60)

# 1-liner hash
print(f"MD5:     {hash_password('test', 'md5')}")
print(f"SHA256:  {hash_password('test', 'sha256')}")
print(f"SHA512:  {hash_password('test', 'sha512')}")

# Using alias
print(f"HP:      {HP('test', 'sha256')[:30]}...")


# ============================================
# 2. FILE HASHING
# ============================================
print("\n" + "=" * 60)
print("2. FILE HASHING")
print("=" * 60)

# Create test file
with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
    f.write("Hello World")
    filepath = f.name

print(f"File: {filepath}")
print(f"SHA256: {hash_file(filepath, 'sha256')}")
print(f"HF:     {HF(filepath, 'sha256')}")

os.remove(filepath)


# ============================================
# 3. SALTED HASHING
# ============================================
print("\n" + "=" * 60)
print("3. SALTED HASHING")
print("=" * 60)

# Generate salt
salt = generate_salt()
print(f"Salt: {salt}")

# Hash with salt
salted = hash_with_salt("MyPassword", salt)
print_result("Hash with salt", salted)

# Verify
is_valid = verify_password("MyPassword", salted['hash'], salted['salt'])
print(f"Verify correct: {is_valid}")
is_valid = verify_password("Wrong", salted['hash'], salted['salt'])
print(f"Verify wrong:   {is_valid}")


# ============================================
# 4. ALGORITHM DETECTION
# ============================================
print("\n" + "=" * 60)
print("4. ALGORITHM DETECTION")
print("=" * 60)

hash_example = hash_password("test", "sha256")
print(f"Hash: {hash_example}")
print(f"DHA:  {detect_hash_algorithm(hash_example)}")
print(f"SHD:  {smart_hash_detector(hash_example)}")


# ============================================
# 5. DOUBLE HASHING
# ============================================
print("\n" + "=" * 60)
print("5. DOUBLE HASHING")
print("=" * 60)

single = hash_password("secret", "sha256")
double = double_hash("secret", "sha256")
print(f"Single: {single[:30]}...")
print(f"Double: {double[:30]}...")


# ============================================
# 6. COMPARE HASHES
# ============================================
print("\n" + "=" * 60)
print("6. COMPARE HASHES")
print("=" * 60)

h1 = hash_password("abc", "sha256")
h2 = hash_password("abc", "sha256")
h3 = hash_password("xyz", "sha256")

comparison = compare_hash(h1, h2, h3)
for i, (match, candidate) in enumerate(comparison):
    print(f"  Candidate {i+1}: {'✅ MATCH' if match else '❌ NO MATCH'}")


# ============================================
# 7. URL HASHING
# ============================================
print("\n" + "=" * 60)
print("7. URL HASHING")
print("=" * 60)

url = "https://example.com/api/data"
print(f"URL:  {url}")
print(f"Hash: {hash_url(url)}")


# ============================================
# 8. REAL-WORLD USE
# ============================================
print("\n" + "=" * 60)
print("8. REAL-WORLD USE")
print("=" * 60)

# Store password
password = "SecurePassword123!"
stored = hash_with_salt(password)
print("✅ Password stored")

# Login simulation
def login(input_password):
    return verify_password(input_password, stored['hash'], stored['salt'])

print(f"Login with correct: {login(password)}")
print(f"Login with wrong:   {login('WrongPassword')}")


# ============================================
# 9. QUICK REFERENCE
# ============================================
print("\n" + "=" * 60)
print("9. QUICK REFERENCE")
print("=" * 60)

print("""
HASHING:
  hash_password(text, alg)     - Hash text
  HP(text, alg)                - Alias for hash_password
  hash_file(file, alg)         - Hash file
  HF(file, alg)                - Alias for hash_file

SALTED:
  generate_salt(len)           - Generate salt
  hash_with_salt(pwd, salt)    - Salted hash
  HWS(pwd, salt)               - Alias
  verify_password(pwd, hash)   - Verify password
  VP(pwd, hash)                - Alias

ADVANCED:
  double_hash(pwd, alg)        - Double hash
  DH(pwd, alg)                 - Alias
  detect_hash_algorithm(hash)  - Detect algorithm
  DHA(hash)                    - Alias
  smart_hash_detector(hash)    - Smart detection
  SHD(hash)                    - Alias

COMPARE:
  compare_hash(target, *candidates) - Compare hashes
  CH(target, *candidates)           - Alias
  find_matching_hashes(target, list)- Find matches
  FMH(target, list)                 - Alias

UTILITY:
  hash_url(url)                - Hash URL
  HU(url)                      - Alias
""")

print("=" * 60)
print("✅ QUICK REFERENCE COMPLETE!")
print("=" * 60)