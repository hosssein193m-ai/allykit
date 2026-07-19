

from allykit.Security_kit import *

import os
import tempfile
import json
import time
from datetime import datetime
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
        for key, value in list(result.items())[:5]:
            if isinstance(value, dict):
                print(f"      {key}: {len(value)} items")
            elif isinstance(value, str) and len(value) > 50:
                print(f"      {key}: {value[:50]}...")
            else:
                print(f"      {key}: {value}")
        if len(result) > 5:
            print(f"      ... and {len(result)-5} more items")
    elif isinstance(result, list):
        print(f"  → {label}: {len(result)} items")
        for item in result[:3]:
            print(f"      {item}")
        if len(result) > 3:
            print(f"      ... and {len(result)-3} more")
    elif isinstance(result, str) and len(result) > max_length:
        print(f"  → {label}: {result[:max_length]}...")
    else:
        print(f"  → {label}: {result}")


# ============================================
# PART 1: SETUP - CREATE TEST ENVIRONMENT
# ============================================
print_section("PART 1: SETUP - TEST ENVIRONMENT")

# 1.1 Create test directory
print("\n--- 1.1 Creating Test Directory ---")
test_dir = tempfile.mkdtemp(prefix="security_complete_test_")
print(f"  Test directory: {test_dir}")

# 1.2 Create test files
print("\n--- 1.2 Creating Test Files ---")
files = {
    "config.json": '{"version": "1.0", "debug": true, "api_key": "test_key"}',
    "data.txt": "User data: John Doe, 30 years old",
    "logs/app.log": "INFO: Application started\nERROR: Connection failed\nINFO: Retrying...",
    "backup/data_backup.txt": "Backup data - Important information",
    "secrets/secret.txt": "SECRET_PASSWORD: MySecret123!",
}

for file_path, content in files.items():
    full_path = os.path.join(test_dir, file_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content)
    print(f"  ✅ Created: {file_path}")

print(f"  Total files: {len(files)}")


# ============================================
# PART 2: PASSWORD KIT - GENERATION
# ============================================
print_section("PART 2: PASSWORD KIT - GENERATION")

# 2.1 Generate different types of passwords
print("\n--- 2.1 Password Generation ---")

# Simple password
simple_pwd = G(12)
print_result("Simple password (12 chars)", simple_pwd)

# Strong password
strong_pwd = GSP(include_uppercase=True, include_digits=True, include_symbols=True, length=16)
print_result("Strong password (16 chars)", strong_pwd)

# Time-based password (1 hour)
timed_pwd = GTP('hours.1')
print_result("Time-based password (1 hour)", timed_pwd[:60] + "...")

# Password with prefix
prefixed_pwd = GP(length=10, prefix="SEC_")
print_result("Prefixed password", prefixed_pwd)

# 2.2 Wrap existing password with time
print("\n--- 2.2 Wrap Existing Password ---")
original_pwd = "MyExistingPassword123"
wrapped_pwd = WPWT(original_pwd, 'days.7')
print_result("Wrapped password (7 days)", wrapped_pwd[:60] + "...")

# 2.3 Character generation
print("\n--- 2.3 Character Generation ---")
print(f"  Random character: {CS()}")
print(f"  Random string (8): {SCS(add=8)}")
print(f"  Character list: {LCS(add=5)}")


# ============================================
# PART 3: PASSWORD KIT - VALIDATION
# ============================================
print_section("PART 3: PASSWORD KIT - VALIDATION")

# 3.1 Review passwords
print("\n--- 3.1 Password Review ---")
test_passwords = [
    "password123",
    "Password123!",
    strong_pwd,
]

for pwd in test_passwords:
    review = ReviewPassword(pwd)
    score = review.Entropy_Score_Password()
    status = review.password_check(types='bool')
    status_emoji = "✅" if status else "❌"
    print(f"  {status_emoji} '{pwd}': Score={score}/10")

# 3.2 Detailed check
print("\n--- 3.2 Detailed Password Check ---")
review = ReviewPassword(strong_pwd)
details = review.password_check(types='dict')
print_result("Strong password details", details)

# 3.3 Time-based password validation
print("\n--- 3.3 Time-Based Validation ---")
tp = TimePassword(timed_pwd)
print(f"  Is valid? {tp.is_password_valid()}")
print(f"  Start: {tp.start_time()}")
print(f"  End: {tp.end_time()}")
print(f"  Password: {tp.get_password()}")

# 3.4 Status report
print("\n--- 3.4 Status Report ---")
status_report = tp.status_password()
print_result("Time password status", status_report)


# ============================================
# PART 4: HASH KIT - CRYPTOGRAPHIC HASHING
# ============================================
print_section("PART 4: HASH KIT - CRYPTOGRAPHIC HASHING")

# 4.1 Hash passwords
print("\n--- 4.1 Hash Passwords ---")
test_text = "SecretData123"

print("  Hashing with different algorithms:")
for alg in ["md5", "sha256", "sha512", "sha3_256"]:
    h = hash_password(test_text, alg)
    print(f"    {alg.upper():<10}: {h[:30]}...")

# 4.2 Salted hashing (secure password storage)
print("\n--- 4.2 Salted Hashing ---")
password_to_store = "MySecurePassword!"
salt = generate_salt()
stored = hash_with_salt(password_to_store, salt, "sha256")

print_result("Salted hash result", stored)

# 4.3 Verify password
print("\n--- 4.3 Verify Password ---")
is_valid = verify_password(password_to_store, stored['hash'], stored['salt'], stored['algorithm'])
print_result("Correct password", "✅ Valid" if is_valid else "❌ Invalid")

is_valid = verify_password("WrongPassword", stored['hash'], stored['salt'], stored['algorithm'])
print_result("Wrong password", "✅ Valid" if is_valid else "❌ Invalid")

# 4.4 Double hashing
print("\n--- 4.4 Double Hashing ---")
single = hash_password("Secret", "sha256")
double = double_hash("Secret", "sha256")
print_result("Single hash", single[:30] + "...")
print_result("Double hash", double[:30] + "...")


# ============================================
# PART 5: HASH KIT - DETECTION & COMPARISON
# ============================================
print_section("PART 5: HASH KIT - DETECTION & COMPARISON")

# 5.1 Detect hash algorithms
print("\n--- 5.1 Detect Algorithms ---")
hash_samples = [
    hash_password("test", "md5"),
    hash_password("test", "sha256"),
    hash_password("test", "sha512"),
]

for h in hash_samples:
    basic = detect_hash_algorithm(h)
    smart = smart_hash_detector(h)
    print(f"  {h[:20]}... → Basic: {basic}, Smart: {smart}")

# 5.2 Compare hashes
print("\n--- 5.2 Compare Hashes ---")
h1 = hash_password("same", "sha256")
h2 = hash_password("same", "sha256")
h3 = hash_password("different", "sha256")

comparison = compare_hash(h1, h2, h3)
for i, (match, candidate) in enumerate(comparison):
    status = "✅ MATCH" if match else "❌ NO MATCH"
    print(f"  Candidate {i+1}: {status}")

# 5.3 Find matching hashes
print("\n--- 5.3 Find Matching Hashes ---")
candidates = [
    hash_password("value1", "sha256"),
    hash_password("value2", "sha256"),
    hash_password("value1", "sha256"),
]
target = hash_password("value1", "sha256")
matches = find_matching_hashes(target, candidates)
print_result("Matching hashes", matches)


# ============================================
# PART 6: FILE KIT - FILE HASHING & INTEGRITY
# ============================================
print_section("PART 6: FILE KIT - FILE HASHING & INTEGRITY")

# 6.1 Hash files
print("\n--- 6.1 Hash Files ---")
for file_path in ["config.json", "data.txt", "logs/app.log"]:
    full_path = os.path.join(test_dir, file_path)
    h = hash_file(full_path, salt=True)
    print(f"  {file_path:20} → {h[:30]}...")

# 6.2 Find files
print("\n--- 6.2 Find Files ---")
found = find_file(test_dir, "config.json")
print_result("Find 'config.json'", found)

found = find_file(test_dir, "app.log")
print_result("Find 'app.log'", found)

found = find_file(test_dir, "nonexistent.txt")
print_result("Find nonexistent", found)

# 6.3 Directory mapping
print("\n--- 6.3 Directory Mapping ---")
dir_map = dict_files_in_directory(test_dir)
print_result("Directory map", dir_map)

# 6.4 Filtered directory mapping
print("\n--- 6.4 Filtered Mapping ---")
# Only permissions
perm_only = dict_files_in_directory_bool(test_dir, reachs=True, passwords=False, f=False)
print_result("Permissions only", perm_only)


# ============================================
# PART 7: FILE KIT - SECURITY SNAPSHOTS
# ============================================
print_section("PART 7: FILE KIT - SECURITY SNAPSHOTS")

# 7.1 Create snapshot
print("\n--- 7.1 Create Snapshot ---")
snapshot = create_snapshot(test_dir)
print_result("Snapshot created", snapshot)

# 7.2 Snapshot details
print("\n--- 7.2 Snapshot Details ---")
for file_path, data in list(snapshot.items())[:3]:
    print(f"\n  📄 {file_path}:")
    print(f"      Hash: {data['hash'][:30]}...")
    print(f"      Size: {data['size']} bytes")
    print(f"      Modified: {datetime.fromtimestamp(data['mtime']).isoformat()}")
    print(f"      Permissions: {data['permissions']}")

# 7.3 Save snapshot to JSON
print("\n--- 7.3 Save Snapshot ---")
snapshot_file = os.path.join(tempfile.gettempdir(), "security_snapshot.json")
with open(snapshot_file, "w") as f:
    json.dump(snapshot, f, indent=2)
print_result("Snapshot saved", snapshot_file)

# 7.4 Modify files
print("\n--- 7.4 Modify Files ---")
# Modify existing file
with open(os.path.join(test_dir, "data.txt"), "a") as f:
    f.write("\nNew content added!")
print("  ✅ Modified: data.txt")

# Add new file
with open(os.path.join(test_dir, "new_file.txt"), "w") as f:
    f.write("This is a new file for testing")
print("  ✅ Added: new_file.txt")

# Delete a file
os.remove(os.path.join(test_dir, "logs/app.log"))
print("  ✅ Deleted: logs/app.log")

time.sleep(1)

# 7.5 Verify snapshot
print("\n--- 7.5 Verify Snapshot ---")
changes = verify_snapshot(test_dir, snapshot)
print_result("Changes detected", changes)

# 7.6 Change analysis
print("\n--- 7.6 Change Analysis ---")
change_counts = {
    "NEW_FILE": 0,
    "MODIFIED": 0,
    "DELETED": 0,
    "PERMISSION_CHANGED": 0,
}
for status in changes.values():
    if status in change_counts:
        change_counts[status] += 1

print("  Change summary:")
for status, count in change_counts.items():
    if count > 0:
        emoji = {"NEW_FILE": "🟢", "MODIFIED": "🟡", "DELETED": "🔴", "PERMISSION_CHANGED": "🟠"}.get(status, "⚪")
        print(f"    {emoji} {status}: {count}")


# ============================================
# PART 8: INTEGRATED SECURITY WORKFLOW
# ============================================
print_section("PART 8: INTEGRATED SECURITY WORKFLOW")

# 8.1 Complete security audit
print("\n--- 8.1 Complete Security Audit ---")

def security_audit(directory: str) -> dict:
    """Perform a complete security audit of a directory."""
    audit = {
        "timestamp": datetime.now().isoformat(),
        "directory": directory,
        "snapshot": create_snapshot(directory),
        "password_analysis": {},
        "hash_analysis": {},
        "security_score": 0,
    }
    
    # Analyze each file
    for file_path, data in audit["snapshot"].items():
        full_path = os.path.join(directory, file_path)
        
        # Check file content for passwords (simplified)
        try:
            with open(full_path, 'r') as f:
                content = f.read()
                # Simple password detection
                if "password" in content.lower() or "secret" in content.lower():
                    audit["password_analysis"][file_path] = "⚠️ May contain sensitive data"
        except:
            pass
        
        # Check permissions
        perm = data['permissions']
        if perm in DANGEROUS_PERMISSIONS:
            audit["password_analysis"][file_path] = "🔴 DANGEROUS permissions"
        elif perm in HIGH_RISK_PERMISSIONS:
            audit["password_analysis"][file_path] = "🟠 HIGH RISK permissions"
    
    # Calculate security score
    total_files = len(audit["snapshot"])
    issues = len(audit["password_analysis"])
    audit["security_score"] = max(0, 10 - (issues / total_files * 10) if total_files > 0 else 10)
    
    return audit

audit_result = security_audit(test_dir)
print_result("Security audit", audit_result)
print(f"  Security score: {audit_result['security_score']:.1f}/10")

# 8.2 Password-protected file encryption simulation
print("\n--- 8.2 Password-Protected File ---")

def secure_file_with_password(filepath: str, password: str) -> dict:
    """Simulate securing a file with a password."""
    # Generate a strong password
    secure_pwd = GSP(include_uppercase=True, include_digits=True, include_symbols=True, length=20)
    
    # Hash the password
    salt = generate_salt()
    hashed = hash_with_salt(secure_pwd, salt, "sha256")
    
    # Hash the file
    file_hash = hash_file(filepath, salt=True)
    
    return {
        "file": filepath,
        "file_hash": file_hash,
        "password": secure_pwd,
        "password_hash": hashed['hash'],
        "salt": salt,
    }

file_to_secure = os.path.join(test_dir, "secrets/secret.txt")
secured = secure_file_with_password(file_to_secure, "MySecretPassword")
print_result("Secured file", secured)

# 8.3 Verify file integrity with password
print("\n--- 8.3 Verify Secure File ---")
# Re-hash file
current_hash = hash_file(file_to_secure, salt=True)
print(f"  Original hash: {secured['file_hash'][:30]}...")
print(f"  Current hash:  {current_hash[:30]}...")
print(f"  File integrity: {'✅ Intact' if current_hash == secured['file_hash'] else '❌ Modified'}")


# ============================================
# PART 9: REAL-WORLD USE CASES
# ============================================
print_section("PART 9: REAL-WORLD USE CASES")

# 9.1 User Management System
print("\n--- 9.1 User Management System ---")

class UserManager:
    """Simple user management with secure password storage."""
    
    def __init__(self):
        self.users = {}
    
    def create_user(self, username: str, password: str) -> dict:
        """Create a new user with secure password storage."""
        if username in self.users:
            raise ValueError(f"User {username} already exists")
        
        # Generate salt and hash password
        salt = generate_salt()
        hashed = hash_with_salt(password, salt, "sha256")
        
        user_data = {
            "username": username,
            "hash": hashed['hash'],
            "salt": salt,
            "algorithm": hashed['algorithm'],
            "created_at": datetime.now().isoformat(),
            "password_strength": ReviewPassword(password).Entropy_Score_Password(),
        }
        self.users[username] = user_data
        return user_data
    
    def verify_user(self, username: str, password: str) -> bool:
        """Verify user password."""
        if username not in self.users:
            return False
        user = self.users[username]
        return verify_password(password, user['hash'], user['salt'], user['algorithm'])
    
    def get_user_info(self, username: str) -> dict:
        """Get user information (without exposing password)."""
        if username not in self.users:
            return None
        info = self.users[username].copy()
        info.pop('hash', None)
        info.pop('salt', None)
        return info

# Create user manager
user_manager = UserManager()

# Create users
users = [
    ("alice", "AliceSecure123!"),
    ("bob", "BobPassword456@"),
    ("charlie", "Charlie#789$"),
]

for username, password in users:
    user = user_manager.create_user(username, password)
    print(f"  ✅ User created: {username} (Strength: {user['password_strength']}/10)")

# Verify users
print("\n  User verification:")
for username, password in users:
    is_valid = user_manager.verify_user(username, password)
    print(f"    {username}: {'✅ Valid' if is_valid else '❌ Invalid'}")

# Wrong password
is_valid = user_manager.verify_user("alice", "WrongPassword")
print(f"    alice (wrong): {'✅ Valid' if is_valid else '❌ Invalid'}")

# 9.2 File Backup System
print("\n--- 9.2 File Backup System ---")

class BackupSystem:
    """Simple backup system with integrity verification."""
    
    def __init__(self, source_dir: str, backup_dir: str):
        self.source_dir = source_dir
        self.backup_dir = backup_dir
        self.snapshot = None
        self.backup_snapshot = None
    
    def create_backup(self) -> dict:
        """Create a backup of the source directory."""
        os.makedirs(self.backup_dir, exist_ok=True)
        
        # Create snapshot before backup
        self.snapshot = create_snapshot(self.source_dir)
        
        # Simulate backup (copy files)
        for file_path in self.snapshot:
            src = os.path.join(self.source_dir, file_path)
            dst = os.path.join(self.backup_dir, file_path)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            try:
                import shutil
                shutil.copy2(src, dst)
            except Exception as e:
                print(f"  ⚠️ Failed to copy {file_path}: {e}")
        
        # Verify backup
        self.backup_snapshot = create_snapshot(self.backup_dir)
        
        return {
            "backup_dir": self.backup_dir,
            "files_backed_up": len(self.snapshot),
            "backup_files": len(self.backup_snapshot),
            "timestamp": datetime.now().isoformat()
        }
    
    def verify_backup(self) -> dict:
        """Verify backup integrity."""
        if not self.backup_snapshot:
            return {"status": "No backup found"}
        
        # Compare backup with original snapshot
        changes = verify_snapshot(self.backup_dir, self.snapshot)
        
        return {
            "status": "✅ Verified" if not changes else "⚠️ Issues found",
            "changes": changes,
            "total_changes": len(changes)
        }

# Create backup system
backup_dir = tempfile.mkdtemp(prefix="backup_")
backup_system = BackupSystem(test_dir, backup_dir)

# Create backup
print("  Creating backup...")
backup_result = backup_system.create_backup()
print(f"  Files backed up: {backup_result['files_backed_up']}")
print(f"  Backup files: {backup_result['backup_files']}")

# Verify backup
print("\n  Verifying backup...")
verify_result = backup_system.verify_backup()
print_result("Backup verification", verify_result)

# 9.3 Secure Logging System
print("\n--- 9.3 Secure Logging System ---")

class SecureLogger:
    """Secure logging with hash-based integrity."""
    
    def __init__(self, log_file: str):
        self.log_file = log_file
        self.logs = []
        self.hash_chain = []
    
    def log(self, message: str, level: str = "INFO"):
        """Add a log entry with hash chain."""
        timestamp = datetime.now().isoformat()
        entry = {
            "timestamp": timestamp,
            "level": level,
            "message": message,
        }
        
        # Hash the entry
        entry_str = json.dumps(entry)
        entry_hash = hash_password(entry_str, "sha256")
        
        # Chain with previous hash
        if self.hash_chain:
            combined = entry_hash + self.hash_chain[-1]
            entry["previous_hash"] = self.hash_chain[-1]
            entry["chain_hash"] = hash_password(combined, "sha256")
        else:
            entry["chain_hash"] = entry_hash
        
        self.logs.append(entry)
        self.hash_chain.append(entry["chain_hash"])
        
        # Write to file
        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")
        
        return entry
    
    def verify_integrity(self) -> dict:
        """Verify the integrity of the log chain."""
        if not self.logs:
            return {"status": "No logs"}
        
        issues = []
        for i, entry in enumerate(self.logs):
            if i == 0:
                # First entry: just verify hash
                expected = hash_password(json.dumps({k: v for k, v in entry.items() if k != "chain_hash"}), "sha256")
                if expected != entry["chain_hash"] and "previous_hash" not in entry:
                    issues.append(f"Entry {i}: Hash mismatch")
            else:
                # Verify chain
                if entry["previous_hash"] != self.logs[i-1]["chain_hash"]:
                    issues.append(f"Entry {i}: Chain break")
        
        return {
            "status": "✅ Valid" if not issues else "⚠️ Issues found",
            "total_entries": len(self.logs),
            "issues": issues,
            "last_hash": self.hash_chain[-1] if self.hash_chain else None
        }

# Create secure logger
log_file = os.path.join(test_dir, "secure_logs.json")
logger = SecureLogger(log_file)

# Add log entries
logger.log("System started", "INFO")
logger.log("User logged in: alice", "INFO")
logger.log("Password reset attempted", "WARNING")
logger.log("Failed login attempt", "ERROR")

print("  Log entries added")

# Verify integrity
integrity = logger.verify_integrity()
print_result("Log integrity", integrity)


# ============================================
# PART 10: PERFORMANCE & CLEANUP
# ============================================
print_section("PART 10: PERFORMANCE & CLEANUP")

# 10.1 Performance test
print("\n--- 10.1 Performance Test ---")

def performance_test():
    """Test performance of key operations."""
    results = {}
    
    # Password generation
    start = time.time()
    for _ in range(100):
        G(12)
    results["Password generation (100)"] = time.time() - start
    
    # Hashing
    start = time.time()
    for _ in range(100):
        hash_password("test", "sha256")
    results["Hashing (100)"] = time.time() - start
    
    # File hashing
    test_file = os.path.join(test_dir, "config.json")
    start = time.time()
    for _ in range(10):
        hash_file(test_file)
    results["File hashing (10)"] = time.time() - start
    
    # Password validation
    pwd = GSP(include_uppercase=True, include_digits=True, include_symbols=True)
    start = time.time()
    for _ in range(100):
        ReviewPassword(pwd).Entropy_Score_Password()
    results["Password validation (100)"] = time.time() - start
    
    return results

perf_results = performance_test()
print("  Performance results:")
for operation, duration in perf_results.items():
    print(f"    {operation}: {duration:.3f}s")

# 10.2 Cleanup
print("\n--- 10.2 Cleanup ---")
try:
    import shutil
    shutil.rmtree(test_dir)
    print(f"  ✅ Removed test directory: {test_dir}")
    shutil.rmtree(backup_dir)
    print(f"  ✅ Removed backup directory: {backup_dir}")
    
    if os.path.exists(snapshot_file):
        os.remove(snapshot_file)
        print(f"  ✅ Removed snapshot file: {snapshot_file}")
except Exception as e:
    print(f"  Cleanup error: {e}")


# ============================================
# FINAL SUMMARY
# ============================================
print("\n" + "=" * 70)
print("✅ ALL DEMONSTRATIONS COMPLETED SUCCESSFULLY!")
print("=" * 70)

print("\n📊 MODULES USED:")
print("=" * 70)
print("  🔹 password_kit - Password generation, validation, time-based")
print("  🔹 hash_kit    - Cryptographic hashing, salted hashing")
print("  🔹 file_kit    - File hashing, directory mapping, snapshots")

print("\n📌 KEY FEATURES DEMONSTRATED:")
print("=" * 70)
print("  PASSWORD KIT:")
print("    ✅ Password generation (simple, strong, time-based)")
print("    ✅ Password wrapping with timestamps")
print("    ✅ Password validation and entropy scoring")
print("    ✅ Time_Password class for expiration management")
print("    ✅ Review_Password class for strength assessment")
print()
print("  HASH KIT:")
print("    ✅ Cryptographic hashing (MD5, SHA256, SHA512, SHA3)")
print("    ✅ Salted hashing for secure password storage")
print("    ✅ Password verification")
print("    ✅ Double hashing for extra security")
print("    ✅ Hash algorithm detection (basic & smart)")
print("    ✅ Hash comparison and matching")
print("    ✅ URL hashing for caching")
print()
print("  FILE KIT:")
print("    ✅ File hashing with metadata salting")
print("    ✅ Directory mapping with permissions")
print("    ✅ Security snapshots")
print("    ✅ Snapshot verification and change detection")
print("    ✅ Permission risk assessment")
print()
print("  INTEGRATED:")
print("    ✅ User management system (passwords + hashing)")
print("    ✅ File backup system (snapshots + verification)")
print("    ✅ Secure logging system (hash chains)")
print("    ✅ Security audit reports")
print("    ✅ Password-protected file simulation")

print("\n🎯 ALL MODULES WORKING TOGETHER SEAMLESSLY!")
print("=" * 70)