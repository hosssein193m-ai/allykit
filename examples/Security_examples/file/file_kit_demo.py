

from allykit.Security_kit.file_kit import (
    # Hashing
    hash_file,
    find_file,
    ph_S384,
    
    # Directory mapping
    dict_files_in_directory,
    dict_files_in_directory_bool,
    save_dict_and_expected,
    
    # Snapshots
    create_snapshot,
    verify_snapshot,
    
    # Security constants
    DANGEROUS_PERMISSIONS,
    HIGH_RISK_PERMISSIONS,
    MEDIUM_RISK_PERMISSIONS,
)

import os
import tempfile
import json
import time
from pathlib import Path
from datetime import datetime


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_result(label, result, max_length=100):
    """Print a formatted result."""
    if isinstance(result, dict):
        print(f"  → {label}:")
        for key, value in list(result.items())[:5]:  # Show first 5 items
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
# PART 1: SETUP
# ============================================
print_section("PART 1: SETUP & TEST DIRECTORY CREATION")

# 1.1 Create test directory structure
print("\n--- 1.1 Creating Test Directory ---")
test_dir = tempfile.mkdtemp(prefix="file_kit_test_")
print(f"  Test directory: {test_dir}")

# Create subdirectories
sub_dir1 = os.path.join(test_dir, "subdir1")
sub_dir2 = os.path.join(test_dir, "subdir2")
os.makedirs(sub_dir1, exist_ok=True)
os.makedirs(sub_dir2, exist_ok=True)

# Create files with different content
files = {
    "file1.txt": "This is file 1 with some content",
    "file2.txt": "This is file 2 with different content",
    "subdir1/file3.log": "ERROR: Sample log entry\nWARNING: Another entry",
    "subdir1/file4.json": '{"name": "test", "value": 42}',
    "subdir2/file5.dat": "Binary-like data content for testing",
    "subdir2/file6.txt": "More test data in subdir2",
}

for file_path, content in files.items():
    full_path = os.path.join(test_dir, file_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content)
    print(f"  ✅ Created: {file_path}")

# 1.2 Set different permissions (on Unix-like systems)
print("\n--- 1.2 Setting Permissions ---")
try:
    # Only works on Unix-like systems
    os.chmod(os.path.join(test_dir, "file1.txt"), 0o644)
    os.chmod(os.path.join(test_dir, "file2.txt"), 0o755)
    os.chmod(os.path.join(test_dir, "subdir1/file3.log"), 0o600)
    print("  ✅ Permissions set")
except Exception as e:
    print(f"  ℹ️ Permission setting note: {e} (Windows may not support)")


# ============================================
# PART 2: FILE HASHING
# ============================================
print_section("PART 2: FILE HASHING")

# 2.1 Hash single file (with salt)
print("\n--- 2.1 Hash File (with salt) ---")
file_path = os.path.join(test_dir, "file1.txt")
hash_with_salt = hash_file(file_path, salt=True)
print_result("Hash with salt", hash_with_salt)

# 2.2 Hash single file (without salt)
print("\n--- 2.2 Hash File (without salt) ---")
hash_no_salt = hash_file(file_path, salt=False)
print_result("Hash without salt", hash_no_salt)

# 2.3 Compare hashes
print("\n--- 2.3 Compare Hashes ---")
print(f"  With salt:  {hash_with_salt[:20]}...")
print(f"  Without salt: {hash_no_salt[:20]}...")
print(f"  Same? {hash_with_salt == hash_no_salt} (Expected: False due to salt)")

# 2.4 Hash different files
print("\n--- 2.4 Hash Different Files ---")
file_paths = [
    os.path.join(test_dir, "file1.txt"),
    os.path.join(test_dir, "file2.txt"),
    os.path.join(test_dir, "subdir1/file3.log"),
]

for fpath in file_paths:
    h = hash_file(fpath, salt=True)
    print(f"  {os.path.basename(fpath)}: {h[:30]}...")

# 2.5 Non-existent file
print("\n--- 2.5 Non-existent File ---")
result = hash_file(os.path.join(test_dir, "nonexistent.txt"))
print_result("Hash of non-existent file", result)

# 2.6 Using ph_S384 lambda directly
print("\n--- 2.6 ph_S384 Lambda ---")
test_text = "Hello World"
hash_direct = ph_S384(test_text)
print_result("ph_S384('Hello World')", hash_direct)


# ============================================
# PART 3: FIND FILE
# ============================================
print_section("PART 3: FIND FILE")

# 3.1 Find existing file
print("\n--- 3.1 Find Existing File ---")
found = find_file(test_dir, "file1.txt")
print_result("Found file1.txt", found)

# 3.2 Find file in subdirectory
print("\n--- 3.2 Find File in Subdirectory ---")
found = find_file(test_dir, "file4.json")
print_result("Found file4.json", found)

# 3.3 Find non-existent file
print("\n--- 3.3 Find Non-existent File ---")
found = find_file(test_dir, "nonexistent.txt")
print_result("Found nonexistent.txt", found)


# ============================================
# PART 4: DIRECTORY MAPPING
# ============================================
print_section("PART 4: DIRECTORY MAPPING")

# 4.1 Full directory mapping
print("\n--- 4.1 Full Directory Mapping ---")
full_map = dict_files_in_directory(test_dir)
print_result("Full directory map", full_map)

# 4.2 Directory mapping with options
print("\n--- 4.2 Directory Mapping (with options) ---")
# Only permissions
perm_only = dict_files_in_directory_bool(test_dir, reachs=True, passwords=False, f=False)
print_result("Permissions only", perm_only)

# Only hashes
hash_only = dict_files_in_directory_bool(test_dir, reachs=False, passwords=True, f=False)
print_result("Hashes only", hash_only)

# Permissions and hashes (no file type)
perm_hash = dict_files_in_directory_bool(test_dir, reachs=True, passwords=True, f=False)
print_result("Permissions + Hashes", perm_hash)

# Permissions and file type (no hashes)
perm_type = dict_files_in_directory_bool(test_dir, reachs=True, passwords=False, f=True)
print_result("Permissions + File type", perm_type)

# 4.3 Save dictionary to JSON
print("\n--- 4.3 Save Dictionary to JSON ---")
json_file = os.path.join(tempfile.gettempdir(), "file_map.json")
save_dict_and_expected(json_file, test_dir)
print_result("JSON file saved", json_file)

# Load and verify JSON
if os.path.exists(json_file):
    with open(json_file, "r") as f:
        json_data = json.load(f)
    print_result("JSON content", json_data)


# ============================================
# PART 5: SECURITY SNAPSHOTS
# ============================================
print_section("PART 5: SECURITY SNAPSHOTS")

# 5.1 Create initial snapshot
print("\n--- 5.1 Create Snapshot ---")
snapshot = create_snapshot(test_dir)
print_result("Snapshot created", snapshot)

# 5.2 Snapshot details
print("\n--- 5.2 Snapshot Details ---")
for file_path, data in list(snapshot.items())[:3]:
    print(f"\n  📄 {file_path}:")
    print(f"      Hash: {data['hash'][:30]}...")
    print(f"      Size: {data['size']} bytes")
    print(f"      Modified: {datetime.fromtimestamp(data['mtime']).isoformat()}")
    print(f"      Permissions: {data['permissions']}")

# 5.3 Save snapshot to file
print("\n--- 5.3 Save Snapshot to File ---")
snapshot_file = os.path.join(tempfile.gettempdir(), "snapshot.json")
with open(snapshot_file, "w") as f:
    json.dump(snapshot, f, indent=2)
print_result("Snapshot saved", snapshot_file)

# 5.4 Modify files
print("\n--- 5.4 Modifying Files ---")
# Modify existing file
with open(os.path.join(test_dir, "file1.txt"), "a") as f:
    f.write("\nNew content added!")
print("  ✅ Modified file1.txt")

# Add new file
with open(os.path.join(test_dir, "new_file.txt"), "w") as f:
    f.write("This is a new file")
print("  ✅ Added new_file.txt")

# Change permissions (if possible)
try:
    os.chmod(os.path.join(test_dir, "file2.txt"), 0o600)
    print("  ✅ Changed permissions on file2.txt")
except Exception:
    print("  ℹ️ Could not change permissions (Windows)")

# Delete a file
os.remove(os.path.join(test_dir, "subdir1/file4.json"))
print("  ✅ Deleted subdir1/file4.json")

time.sleep(1)  # Ensure timestamp changes


# ============================================
# PART 6: SNAPSHOT VERIFICATION
# ============================================
print_section("PART 6: SNAPSHOT VERIFICATION")

# 6.1 Verify snapshot
print("\n--- 6.1 Verify Snapshot ---")
changes = verify_snapshot(test_dir, snapshot)
print_result("Changes detected", changes)

# 6.2 Analyze changes
print("\n--- 6.2 Change Analysis ---")
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
        print(f"    {status}: {count}")

# 6.3 Detailed changes
print("\n--- 6.3 Detailed Changes ---")
for file_path, status in changes.items():
    emoji = {
        "NEW_FILE": "🟢",
        "MODIFIED": "🟡",
        "DELETED": "🔴",
        "PERMISSION_CHANGED": "🟠"
    }.get(status, "⚪")
    print(f"    {emoji} {file_path}: {status}")

# 6.4 Create new snapshot
print("\n--- 6.4 Create New Snapshot ---")
new_snapshot = create_snapshot(test_dir)
print_result("New snapshot created", new_snapshot)

# Compare snapshots
print("\n--- 6.5 Compare Old vs New ---")
print(f"  Old snapshot files: {len(snapshot)}")
print(f"  New snapshot files: {len(new_snapshot)}")


# ============================================
# PART 7: PERMISSION SECURITY AUDIT
# ============================================
print_section("PART 7: PERMISSION SECURITY AUDIT")

# 7.1 Check permissions
print("\n--- 7.1 Check Permissions ---")
for file_path, data in snapshot.items():
    perm = data['permissions']
    risk = "✅ Safe"
    if perm in DANGEROUS_PERMISSIONS:
        risk = "🔴 DANGEROUS"
    elif perm in HIGH_RISK_PERMISSIONS:
        risk = "🟠 HIGH RISK"
    elif perm in MEDIUM_RISK_PERMISSIONS:
        risk = "🟡 MEDIUM"
    print(f"    {risk}: {file_path} ({perm})")

# 7.2 Find dangerous permissions
print("\n--- 7.2 Find Dangerous Permissions ---")
dangerous_files = []
for file_path, data in snapshot.items():
    if data['permissions'] in DANGEROUS_PERMISSIONS:
        dangerous_files.append(file_path)

if dangerous_files:
    print("  ⚠️ Files with DANGEROUS permissions:")
    for f in dangerous_files:
        print(f"    🔴 {f}")
else:
    print("  ✅ No dangerous permissions found")

# 7.3 Find high-risk permissions
print("\n--- 7.3 Find High-Risk Permissions ---")
high_risk_files = []
for file_path, data in snapshot.items():
    if data['permissions'] in HIGH_RISK_PERMISSIONS:
        high_risk_files.append(file_path)

if high_risk_files:
    print("  ⚠️ Files with HIGH-RISK permissions:")
    for f in high_risk_files:
        print(f"    🟠 {f}")
else:
    print("  ✅ No high-risk permissions found")


# ============================================
# PART 8: INTEGRITY MONITORING
# ============================================
print_section("PART 8: INTEGRITY MONITORING")

# 8.1 Monitor specific files
print("\n--- 8.1 Monitor Specific Files ---")
monitor_files = ["file1.txt", "file2.txt"]
for filename in monitor_files:
    fpath = os.path.join(test_dir, filename)
    if os.path.exists(fpath):
        hash_val = hash_file(fpath, salt=True)
        print(f"  {filename}: {hash_val[:30]}...")

# 8.2 Check file integrity
print("\n--- 8.2 Check File Integrity ---")
for filename in monitor_files:
    fpath = os.path.join(test_dir, filename)
    if os.path.exists(fpath):
        current_hash = hash_file(fpath, salt=True)
        # Check against snapshot
        rel_path = filename
        if rel_path in snapshot:
            original_hash = snapshot[rel_path]['hash']
            if current_hash == original_hash:
                print(f"  ✅ {filename}: INTACT")
            else:
                print(f"  ⚠️ {filename}: MODIFIED")
        else:
            print(f"  🟢 {filename}: NEW FILE")


# ============================================
# PART 9: REAL-WORLD USE CASES
# ============================================
print_section("PART 9: REAL-WORLD USE CASES")

# 9.1 Security Audit Report
print("\n--- 9.1 Security Audit Report ---")
print("  🔍 Generating security audit report...")

audit_report = {
    "timestamp": datetime.now().isoformat(),
    "directory": test_dir,
    "total_files": len(snapshot),
    "dangerous_permissions": len(dangerous_files),
    "high_risk_permissions": len(high_risk_files),
    "changes_detected": len(changes),
    "change_summary": change_counts,
    "files": snapshot
}

print_result("Audit report", audit_report)

# 9.2 Automated Backup Verification
print("\n--- 9.2 Backup Verification ---")
backup_dir = tempfile.mkdtemp(prefix="backup_")
print(f"  Backup directory: {backup_dir}")

# Simulate backup
for file_path, data in snapshot.items():
    src = os.path.join(test_dir, file_path)
    dst = os.path.join(backup_dir, file_path)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    try:
        import shutil
        shutil.copy2(src, dst)
    except:
        pass

print("  ✅ Backup created")

# Verify backup
backup_snapshot = create_snapshot(backup_dir)
print(f"  Backup files: {len(backup_snapshot)}")
print(f"  Original files: {len(snapshot)}")

# Compare backup with original
backup_changes = verify_snapshot(backup_dir, snapshot)
if backup_changes:
    print("  ⚠️ Backup verification found issues:")
    for file_path, status in backup_changes.items():
        print(f"    {file_path}: {status}")
else:
    print("  ✅ Backup verified: All files match")

# 9.3 Integrity Check Before/After Deployment
print("\n--- 9.3 Deployment Integrity Check ---")
print("  📦 Simulating deployment...")

# Create pre-deployment snapshot
pre_deploy = create_snapshot(test_dir)

# Simulate deployment changes
with open(os.path.join(test_dir, "deployed.txt"), "w") as f:
    f.write("Deployment file")
print("  ✅ Deployment file added")

# Post-deployment verification
post_deploy = create_snapshot(test_dir)
deploy_changes = verify_snapshot(test_dir, pre_deploy)

print("  Changes after deployment:")
for file_path, status in deploy_changes.items():
    emoji = "🟢" if status == "NEW_FILE" else "⚠️"
    print(f"    {emoji} {file_path}: {status}")


# ============================================
# PART 10: CLEANUP
# ============================================
print_section("PART 10: CLEANUP")

# 10.1 Remove test directories
print("\n--- 10.1 Cleanup ---")
try:
    import shutil
    shutil.rmtree(test_dir)
    print(f"  ✅ Removed test directory: {test_dir}")
except Exception as e:
    print(f"  Cleanup error: {e}")

try:
    shutil.rmtree(backup_dir)
    print(f"  ✅ Removed backup directory: {backup_dir}")
except Exception as e:
    print(f"  Cleanup error: {e}")

# 10.2 Remove temporary files
print("\n--- 10.2 Remove Temporary Files ---")
temp_files = [json_file, snapshot_file]
for f in temp_files:
    if os.path.exists(f):
        os.remove(f)
        print(f"  ✅ Removed: {f}")


# ============================================
# FINAL SUMMARY
# ============================================
print("\n" + "=" * 70)
print("✅ ALL DEMONSTRATIONS COMPLETED SUCCESSFULLY!")
print("=" * 70)

print("\n📊 SUMMARY OF OPERATIONS:")
print("=" * 70)
print("  ✅ File hashing (with and without salt)")
print("  ✅ Find files in directory tree")
print("  ✅ Directory mapping (full and filtered)")
print("  ✅ Save directory maps to JSON")
print("  ✅ Create security snapshots")
print("  ✅ Verify snapshots")
print("  ✅ Detect changes (new, modified, deleted, permission)")
print("  ✅ Permission risk assessment")
print("  ✅ Security audit report")
print("  ✅ Backup verification")
print("  ✅ Deployment integrity check")

print("\n📌 KEY FUNCTIONS:")
print("=" * 70)
print("  🔹 hash_file()                 - Hash file with optional metadata salt")
print("  🔹 find_file()                 - Find file in directory tree")
print("  🔹 dict_files_in_directory()   - Map directory structure")
print("  🔹 dict_files_in_directory_bool() - Filtered directory mapping")
print("  🔹 save_dict_and_expected()    - Save map to JSON")
print("  🔹 create_snapshot()           - Create security snapshot")
print("  🔹 verify_snapshot()           - Verify against snapshot")
print("  🔹 ph_S384()                   - SHA384 hash lambda")

print("\n📌 SECURITY CONSTANTS:")
print("=" * 70)
print("  🔸 DANGEROUS_PERMISSIONS   - World-writable permissions")
print("  🔸 HIGH_RISK_PERMISSIONS   - Critical security issues")
print("  🔸 MEDIUM_RISK_PERMISSIONS - Permissions needing review")

print("\n" + "=" * 70)
print("🎯 DEMONSTRATION COMPLETE!")
print("=" * 70)