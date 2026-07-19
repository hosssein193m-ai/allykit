

from allykit.Security_kit.hash_kit import (
    # Core hashing
    hash_password,
    hash_file,
    
    # Detection
    detect_hash_algorithm,
    smart_hash_detector,
    
    # Salted hashing
    generate_salt,
    hash_with_salt,
    verify_password,
    
    # Advanced
    double_hash,
    compare_hash,
    find_matching_hashes,
    calculate_file_hashes,
    hash_url,
    
    # Aliases
    HP, HF, DHA, HWS, VP, DH, CH, FMH, CFH, HU, SHD,
    
    # Constants
    hash_algorithms,
)

import os
import tempfile
import time
from pathlib import Path


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_result(label, result, max_length=80):
    """Print a formatted result."""
    if isinstance(result, dict):
        print(f"  → {label}:")
        for key, value in result.items():
            if isinstance(value, str) and len(value) > 50:
                print(f"      {key}: {value[:50]}...")
            else:
                print(f"      {key}: {value}")
    elif isinstance(result, list):
        print(f"  → {label}: {len(result)} items")
        for item in result[:3]:
            if isinstance(item, (list, tuple)):
                print(f"      {item}")
            else:
                print(f"      {item}")
        if len(result) > 3:
            print(f"      ... and {len(result)-3} more")
    elif isinstance(result, str) and len(result) > max_length:
        print(f"  → {label}: {result[:max_length]}...")
    else:
        print(f"  → {label}: {result}")


# ============================================
# PART 1: CORE HASHING
# ============================================
print_section("PART 1: CORE HASHING")

# 1.1 Basic password hashing
print("\n--- 1.1 Basic Password Hashing ---")
password = "MySecurePassword123!"
hash_sha256 = hash_password(password, "sha256")
hash_sha512 = hash_password(password, "sha512")
hash_sha3 = hash_password(password, "sha3_256")

print_result("SHA-256", hash_sha256)
print_result("SHA-512", hash_sha512)
print_result("SHA3-256", hash_sha3)

# 1.2 Multiple algorithms
print("\n--- 1.2 Multiple Algorithms ---")
algorithms = ["md5", "sha1", "sha224", "sha256", "sha384", "sha512", "sha3_256", "sha3_512", "blake2b"]
for alg in algorithms[:5]:  # Show first 5 for brevity
    try:
        h = hash_password(password, alg)
        print(f"  {alg.upper():<12}: {h[:30]}...")
    except ValueError as e:
        print(f"  {alg.upper():<12}: ❌ {e}")

# 1.3 Using HP alias
print("\n--- 1.3 Using HP Alias ---")
hash_alias = HP(password, "sha384")
print_result("HP alias (SHA-384)", hash_alias[:40] + "...")


# ============================================
# PART 2: FILE HASHING
# ============================================
print_section("PART 2: FILE HASHING")

# 2.1 Create test file
print("\n--- 2.1 Create Test File ---")
test_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
test_file.write("This is sample content for file hashing.\nLine 2\nLine 3")
test_file.close()
print(f"  Test file: {test_file.name}")

# 2.2 Hash file with different algorithms
print("\n--- 2.2 Hash File ---")
hash_md5 = hash_file(test_file.name, "md5")
hash_sha256 = hash_file(test_file.name, "sha256")
hash_sha384 = hash_file(test_file.name, "sha384")
hash_sha512 = hash_file(test_file.name, "sha512")

print_result("MD5", hash_md5)
print_result("SHA-256", hash_sha256)
print_result("SHA-384", hash_sha384)
print_result("SHA-512", hash_sha512)

# 2.3 Using HF alias
print("\n--- 2.3 HF Alias ---")
hash_alias_file = HF(test_file.name, "sha256")
print_result("HF alias", hash_alias_file)

# 2.4 Non-existent file
print("\n--- 2.4 Non-existent File ---")
result = hash_file("/non/existent/file.txt")
print_result("Hash of non-existent file", result)

# 2.5 Permission denied (simulated)
print("\n--- 2.5 Permission Handling ---")
# Create a file and try to read without permission (Windows may not support)
try:
    import stat
    os.chmod(test_file.name, 0o000)  # Remove all permissions
    result = hash_file(test_file.name)
    print_result("Permission test", result)
    os.chmod(test_file.name, 0o644)  # Restore
except Exception as e:
    print(f"  ℹ️ Permission test skipped: {e}")


# ============================================
# PART 3: HASH ALGORITHM DETECTION
# ============================================
print_section("PART 3: HASH ALGORITHM DETECTION")

# 3.1 Basic detection
print("\n--- 3.1 Basic Detection ---")
test_hashes = [
    hash_password("test", "md5"),
    hash_password("test", "sha1"),
    hash_password("test", "sha256"),
    hash_password("test", "sha384"),
    hash_password("test", "sha512"),
]

for h in test_hashes:
    detected = detect_hash_algorithm(h)
    print(f"  {h[:20]}... → {detected}")

# 3.2 Smart detection
print("\n--- 3.2 Smart Detection ---")
for h in test_hashes:
    smart = smart_hash_detector(h)
    print(f"  {h[:20]}... → {smart}")

# 3.3 Complex patterns
print("\n--- 3.3 Complex Patterns ---")
complex_hashes = [
    "$2a$12$R9h/cIPz0gi.URNNX3kh2OPST9/PgBkqquzi.Ss7KIUgO2t0jWMUW",  # Bcrypt
    "$1$rasmusle$rISCgZzpwk3UhDidwXvin0",  # MD5 (Unix)
    "$sha1$40000$JTJyXhD2$LUqI2iqHxZzHmnQq6T5hYqHp1L0=",  # SHA-1 (Unix)
]

for h in complex_hashes:
    smart = smart_hash_detector(h)
    print(f"  {h[:30]}... → {smart}")

# 3.4 Using DHA and SHD aliases
print("\n--- 3.4 Aliases ---")
hash_example = hash_password("test", "sha256")
print_result("DHA", DHA(hash_example))
print_result("SHD", SHD(hash_example))


# ============================================
# PART 4: SALTED HASHING
# ============================================
print_section("PART 4: SALTED HASHING")

# 4.1 Generate salt
print("\n--- 4.1 Generate Salt ---")
salt_default = generate_salt()
salt_custom = generate_salt(length=32)
salt_short = generate_salt(length=8)

print_result("Default salt (16)", salt_default)
print_result("Custom salt (32)", salt_custom)
print_result("Short salt (8)", salt_short)

# 4.2 Hash with salt
print("\n--- 4.2 Hash with Salt ---")
password = "MySecretPassword"
salt = generate_salt()

salted_result = hash_with_salt(password, salt, "sha256")
print_result("Salted hash result", salted_result)

# 4.3 Auto-generate salt
print("\n--- 4.3 Auto-generate Salt ---")
auto_salted = hash_with_salt(password, algorithm="sha512")
print_result("Auto-salted hash", auto_salted)

# 4.4 Different algorithms with salt
print("\n--- 4.4 Multiple Algorithms with Salt ---")
for alg in ["sha256", "sha512", "sha3_256"]:
    result = hash_with_salt(password, algorithm=alg)
    print(f"  {alg.upper():<12}: {result['hash'][:30]}... (salt: {result['salt'][:8]}...)")

# 4.5 Using HWS alias
print("\n--- 4.5 HWS Alias ---")
hws_result = HWS(password, algorithm="sha384")
print_result("HWS alias", hws_result)


# ============================================
# PART 5: PASSWORD VERIFICATION
# ============================================
print_section("PART 5: PASSWORD VERIFICATION")

# 5.1 Store password
print("\n--- 5.1 Store Password ---")
original_password = "MySecurePassword123!"
stored = hash_with_salt(original_password, algorithm="sha256")
print("  ✅ Password stored:")
print_result("  Hash", stored['hash'][:40] + "...")
print_result("  Salt", stored['salt'])
print_result("  Algorithm", stored['algorithm'])

# 5.2 Verify correct password
print("\n--- 5.2 Verify Correct Password ---")
is_valid = verify_password(
    original_password,
    stored['hash'],
    stored['salt'],
    stored['algorithm']
)
print_result("Correct password verification", "✅ Valid" if is_valid else "❌ Invalid")

# 5.3 Verify wrong password
print("\n--- 5.3 Verify Wrong Password ---")
is_valid = verify_password(
    "WrongPassword",
    stored['hash'],
    stored['salt'],
    stored['algorithm']
)
print_result("Wrong password verification", "✅ Valid" if is_valid else "❌ Invalid")

# 5.4 Verify with different algorithm
print("\n--- 5.4 Verify with Different Algorithm ---")
# Store with SHA-512
stored_sha512 = hash_with_salt(original_password, algorithm="sha512")

# Verify with SHA-512
is_valid = verify_password(
    original_password,
    stored_sha512['hash'],
    stored_sha512['salt'],
    "sha512"
)
print_result("SHA-512 verification", "✅ Valid" if is_valid else "❌ Invalid")

# 5.5 Using VP alias
print("\n--- 5.5 VP Alias ---")
is_valid = VP(original_password, stored['hash'], stored['salt'], stored['algorithm'])
print_result("VP alias verification", "✅ Valid" if is_valid else "❌ Invalid")


# ============================================
# PART 6: DOUBLE HASHING
# ============================================
print_section("PART 6: DOUBLE HASHING")

# 6.1 Double hash with SHA-256
print("\n--- 6.1 Double Hash (SHA-256) ---")
password = "SuperSecret"
single_hash = hash_password(password, "sha256")
double_hash_result = double_hash(password, "sha256")

print_result("Single hash", single_hash[:30] + "...")
print_result("Double hash", double_hash_result[:30] + "...")
print(f"  Same? {single_hash == double_hash_result}")

# 6.2 Double hash with different algorithms
print("\n--- 6.2 Multiple Algorithms ---")
for alg in ["sha256", "sha512", "sha3_256"]:
    try:
        dh = double_hash(password, alg)
        print(f"  {alg.upper():<12}: {dh[:30]}...")
    except Exception as e:
        print(f"  {alg.upper():<12}: ❌ {e}")

# 6.3 Using DH alias
print("\n--- 6.3 DH Alias ---")
dh_alias = DH(password, "sha512")
print_result("DH alias", dh_alias[:30] + "...")


# ============================================
# PART 7: HASH COMPARISON
# ============================================
print_section("PART 7: HASH COMPARISON")

# 7.1 Compare hashes
print("\n--- 7.1 Compare Hashes ---")
hash1 = hash_password("test123", "sha256")
hash2 = hash_password("test123", "sha256")
hash3 = hash_password("different", "sha256")

comparison = compare_hash(hash1, hash2, hash3)
print("  Comparison results:")
for i, (match, candidate) in enumerate(comparison):
    status = "✅ MATCH" if match else "❌ NO MATCH"
    print(f"    Candidate {i+1}: {status} ({candidate[:20]}...)")

# 7.2 Find matching hashes
print("\n--- 7.2 Find Matching Hashes ---")
candidates = [
    hash_password("test1", "sha256"),
    hash_password("test2", "sha256"),
    hash_password("test1", "sha256"),
    hash_password("test3", "sha256"),
]
target_hash = hash_password("test1", "sha256")

matches = find_matching_hashes(target_hash, candidates)
print_result("Matches found", len(matches))
for i, match in enumerate(matches):
    print(f"  Match {i+1}: {match[:20]}...")

# 7.3 Using CH and FMH aliases
print("\n--- 7.3 Aliases ---")
ch_result = CH(hash1, hash2, hash3)
print_result("CH alias results", ch_result)

fmh_result = FMH(hash1, [hash1, hash2, hash3])
print_result("FMH alias matches", fmh_result)


# ============================================
# PART 8: BULK FILE HASHING
# ============================================
print_section("PART 8: BULK FILE HASHING")

# 8.1 Create test files
print("\n--- 8.1 Create Test Files ---")
test_dir = tempfile.mkdtemp(prefix="hash_bulk_")
files = ["file1.txt", "file2.txt", "file3.txt", "subdir/"]
os.makedirs(os.path.join(test_dir, "subdir"), exist_ok=True)

for filename in files:
    if filename.endswith('/'):
        continue
    filepath = os.path.join(test_dir, filename)
    with open(filepath, "w") as f:
        f.write(f"Content of {filename}\nLine 2\nLine 3")
    print(f"  ✅ Created: {filename}")

# 8.2 Calculate hashes
print("\n--- 8.2 Calculate Bulk Hashes ---")
file_list = ["file1.txt", "file2.txt", "file3.txt", "subdir"]
print("  Hashing files:")
for filepath, hash_value in calculate_file_hashes(file_list, test_dir):
    filename = os.path.basename(filepath)
    if hash_value.startswith("error:") or hash_value in ["not_found", "is_directory"]:
        print(f"    {filename}: {hash_value}")
    else:
        print(f"    {filename}: {hash_value[:30]}...")

# 8.3 Using CFH alias
print("\n--- 8.3 CFH Alias ---")
print("  Using CFH alias:")
for filepath, hash_value in CFH(["file1.txt", "nonexistent.txt"], test_dir):
    print(f"    {os.path.basename(filepath)}: {hash_value[:30] if len(hash_value) > 30 else hash_value}...")


# ============================================
# PART 9: URL HASHING
# ============================================
print_section("PART 9: URL HASHING")

# 9.1 Hash URLs
print("\n--- 9.1 Hash URLs ---")
urls = [
    "https://example.com",
    "https://example.com/page",
    "https://example.com/page?q=test",
    "https://google.com",
]

for url in urls:
    url_hash = hash_url(url)
    print(f"  {url:40} → {url_hash}")

# 9.2 Cache key usage
print("\n--- 9.2 Cache Key Example ---")
cache_data = {
    hash_url("https://api.example.com/data"): {"data": "cached_response", "timestamp": time.time()},
    hash_url("https://api.example.com/users"): {"data": "user_list", "timestamp": time.time()},
}

print("  Cache keys:")
for key, value in cache_data.items():
    print(f"    {key}: {value['data']}")

# 9.3 Using HU alias
print("\n--- 9.3 HU Alias ---")
url_hash_alias = HU("https://example.com")
print_result("HU alias", url_hash_alias)


# ============================================
# PART 10: REAL-WORLD USE CASES
# ============================================
print_section("PART 10: REAL-WORLD USE CASES")

# 10.1 User Registration
print("\n--- 10.1 User Registration ---")
def register_user(username: str, password: str) -> dict:
    """Simulate user registration with salted hash."""
    salt = generate_salt()
    password_hash = hash_with_salt(password, salt, "sha256")
    return {
        "username": username,
        "hash": password_hash['hash'],
        "salt": password_hash['salt'],
        "algorithm": password_hash['algorithm']
    }

user = register_user("alice", "AlicePassword123!")
print("  User registered:")
for key, value in user.items():
    if key == "hash":
        print(f"    {key}: {value[:30]}...")
    else:
        print(f"    {key}: {value}")

# 10.2 User Login
print("\n--- 10.2 User Login ---")
def login_user(username: str, password: str, stored: dict) -> bool:
    """Simulate user login verification."""
    return verify_password(password, stored['hash'], stored['salt'], stored['algorithm'])

is_logged_in = login_user("alice", "AlicePassword123!", user)
print_result(f"Login for 'alice'", "✅ Success" if is_logged_in else "❌ Failed")

is_logged_in = login_user("alice", "WrongPassword", user)
print_result(f"Login with wrong password", "✅ Success" if is_logged_in else "❌ Failed")

# 10.3 File Integrity Check
print("\n--- 10.3 File Integrity Check ---")
def check_file_integrity(filepath: str, expected_hash: str) -> bool:
    """Check if file hash matches expected hash."""
    current_hash = hash_file(filepath, "sha256")
    return current_hash == expected_hash

# Calculate and store hash
file_path = os.path.join(test_dir, "file1.txt")
original_hash = hash_file(file_path, "sha256")
print(f"  Original hash: {original_hash[:30]}...")

# Modify file
with open(file_path, "a") as f:
    f.write("\nModified content!")

# Check integrity
is_intact = check_file_integrity(file_path, original_hash)
print_result("File integrity", "✅ Intact" if is_intact else "❌ Modified")

# 10.4 Duplicate File Detection
print("\n--- 10.4 Duplicate File Detection ---")
# Create duplicate files
with open(os.path.join(test_dir, "duplicate1.txt"), "w") as f:
    f.write("Duplicate content")
with open(os.path.join(test_dir, "duplicate2.txt"), "w") as f:
    f.write("Duplicate content")
with open(os.path.join(test_dir, "different.txt"), "w") as f:
    f.write("Different content")

# Group by hash
hash_groups = {}
for filename in ["duplicate1.txt", "duplicate2.txt", "different.txt"]:
    filepath = os.path.join(test_dir, filename)
    file_hash = hash_file(filepath, "sha256")
    if file_hash not in hash_groups:
        hash_groups[file_hash] = []
    hash_groups[file_hash].append(filename)

print("  Duplicate groups:")
for file_hash, filenames in hash_groups.items():
    if len(filenames) > 1:
        print(f"    {' '.join(filenames)}: DUPLICATES")
    else:
        print(f"    {filenames[0]}: UNIQUE")

# 10.5 Password Strength with Hashing
print("\n--- 10.5 Password Strength ---")
test_passwords = ["123456", "password", "Password123!", "K#9mP$2vL!qR@7xZ9"]

for pwd in test_passwords:
    hashed = hash_password(pwd, "sha256")
    print(f"  {pwd:20} → {hashed[:30]}...")


# ============================================
# PART 11: PERFORMANCE
# ============================================
print_section("PART 11: PERFORMANCE")

# 11.1 Hash speed
print("\n--- 11.1 Hash Speed ---")
test_text = "x" * 1000

print("  Time to hash 10000 times:")
for alg in ["md5", "sha256", "sha512"]:
    start = time.time()
    for _ in range(1000):
        hash_password(test_text, alg)
    elapsed = time.time() - start
    print(f"    {alg.upper():<8}: {elapsed:.3f}s")

# 11.2 File hash speed
print("\n--- 11.2 File Hash Speed ---")
large_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
large_file.write("x" * 100000)  # 100KB
large_file.close()

for alg in ["md5", "sha256", "sha512"]:
    start = time.time()
    hash_file(large_file.name, alg)
    elapsed = time.time() - start
    print(f"    {alg.upper():<8}: {elapsed:.3f}s")


# ============================================
# PART 12: CLEANUP
# ============================================
print_section("PART 12: CLEANUP")

# 12.1 Remove test files
print("\n--- 12.1 Cleanup ---")
try:
    # Remove test file
    if os.path.exists(test_file.name):
        os.remove(test_file.name)
        print(f"  ✅ Removed: {test_file.name}")
    
    # Remove large file
    if os.path.exists(large_file.name):
        os.remove(large_file.name)
        print(f"  ✅ Removed: {large_file.name}")
    
    # Remove test directory
    import shutil
    shutil.rmtree(test_dir)
    print(f"  ✅ Removed: {test_dir}")
except Exception as e:
    print(f"  Cleanup error: {e}")


# ============================================
# FINAL SUMMARY
# ============================================
print("\n" + "=" * 70)
print("✅ ALL DEMONSTRATIONS COMPLETED SUCCESSFULLY!")
print("=" * 70)

print("\n📊 SUMMARY OF OPERATIONS:")
print("=" * 70)
print("  ✅ Password hashing (multiple algorithms)")
print("  ✅ File hashing (chunked reading)")
print("  ✅ Hash algorithm detection (basic & smart)")
print("  ✅ Salt generation")
print("  ✅ Salted hashing and verification")
print("  ✅ Double hashing")
print("  ✅ Hash comparison")
print("  ✅ Bulk file hashing")
print("  ✅ URL hashing")
print("  ✅ Real-world use cases")
print("  ✅ Performance testing")

print("\n📌 KEY FUNCTIONS:")
print("=" * 70)
print("  🔹 hash_password()        - Hash text/password")
print("  🔹 hash_file()            - Hash file content")
print("  🔹 generate_salt()        - Generate cryptographic salt")
print("  🔹 hash_with_salt()       - Salted hashing")
print("  🔹 verify_password()      - Verify salted password")
print("  🔹 double_hash()          - Double hashing")
print("  🔹 detect_hash_algorithm() - Basic algorithm detection")
print("  🔹 smart_hash_detector()  - Advanced algorithm detection")
print("  🔹 compare_hash()         - Compare multiple hashes")
print("  🔹 find_matching_hashes() - Find matching hashes")
print("  🔹 calculate_file_hashes() - Bulk file hashing")
print("  🔹 hash_url()             - URL hashing for caching")

print("\n📌 ALIASES:")
print("=" * 70)
print("  🔸 HP  = hash_password")
print("  🔸 HF  = hash_file")
print("  🔸 DHA = detect_hash_algorithm")
print("  🔸 HWS = hash_with_salt")
print("  🔸 VP  = verify_password")
print("  🔸 DH  = double_hash")
print("  🔸 CH  = compare_hash")
print("  🔸 FMH = find_matching_hashes")
print("  🔸 CFH = calculate_file_hashes")
print("  🔸 HU  = hash_url")
print("  🔸 SHD = smart_hash_detector")

print("\n📌 SUPPORTED ALGORITHMS:")
print("=" * 70)
print("  md5, sha1, sha224, sha256, sha384, sha512")
print("  sha3-224, sha3-256, sha3-384, sha3-512")
print("  bcrypt, scrypt, argon2, ntlm, blake2b")

print("\n" + "=" * 70)
print("🎯 DEMONSTRATION COMPLETE!")
print("=" * 70)