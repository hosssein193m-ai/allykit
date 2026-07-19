"""
AllyKit File Kit - Quick Reference
====================================
Fast demonstrations of file security and integrity operations.

Author: AllyKit Team
Version: 1.0.0
"""

from allykit.Security_kit.file_kit import (
    hash_file,
    find_file,
    dict_files_in_directory,
    dict_files_in_directory_bool,
    save_dict_and_expected,
    create_snapshot,
    verify_snapshot,
    DANGEROUS_PERMISSIONS,
    HIGH_RISK_PERMISSIONS,
    ph_S384,
)

import os
import tempfile
import json


def print_result(label, result):
    """Print a formatted result."""
    if isinstance(result, dict):
        print(f"  {label}: {len(result)} items")
    else:
        print(f"  {label}: {result}")


# ============================================
# 1. SETUP TEST ENVIRONMENT
# ============================================
print("=" * 60)
print("1. SETUP TEST ENVIRONMENT")
print("=" * 60)

test_dir = tempfile.mkdtemp(prefix="file_kit_quick_")
os.makedirs(os.path.join(test_dir, "subdir"), exist_ok=True)

with open(os.path.join(test_dir, "file1.txt"), "w") as f:
    f.write("Hello World")
with open(os.path.join(test_dir, "file2.txt"), "w") as f:
    f.write("Goodbye World")
with open(os.path.join(test_dir, "subdir", "file3.log"), "w") as f:
    f.write("Log entry")

print(f"Test directory: {test_dir}")
print("✅ Test files created")


# ============================================
# 2. FILE HASHING
# ============================================
print("\n" + "=" * 60)
print("2. FILE HASHING")
print("=" * 60)

# 1-liner hash
file_path = os.path.join(test_dir, "file1.txt")
hash_val = hash_file(file_path, salt=True)
print_result("Hash (with salt)", hash_val[:30] + "...")

hash_no_salt = hash_file(file_path, salt=False)
print_result("Hash (no salt)", hash_no_salt[:30] + "...")

# Using lambda
print_result("ph_S384('test')", ph_S384("test")[:30] + "...")


# ============================================
# 3. FIND FILES
# ============================================
print("\n" + "=" * 60)
print("3. FIND FILES")
print("=" * 60)

found = find_file(test_dir, "file1.txt")
print_result("Find 'file1.txt'", found)

found = find_file(test_dir, "file3.log")
print_result("Find 'file3.log'", found)

found = find_file(test_dir, "nonexistent")
print_result("Find nonexistent", found)


# ============================================
# 4. DIRECTORY MAPPING
# ============================================
print("\n" + "=" * 60)
print("4. DIRECTORY MAPPING")
print("=" * 60)

# Full map
full_map = dict_files_in_directory(test_dir)
print_result("Full map", full_map)
print(f"  {json.dumps(full_map, indent=2)[:200]}...")

# Permissions only
perms = dict_files_in_directory_bool(test_dir, reachs=True, passwords=False, f=False)
print_result("Permissions only", perms)


# ============================================
# 5. SECURITY SNAPSHOTS
# ============================================
print("\n" + "=" * 60)
print("5. SECURITY SNAPSHOTS")
print("=" * 60)

# Create snapshot
snapshot = create_snapshot(test_dir)
print_result("Snapshot", snapshot)
for file_path, data in snapshot.items():
    print(f"  {file_path}: {data['hash'][:20]}... {data['permissions']}")

# Verify snapshot (should be identical)
changes = verify_snapshot(test_dir, snapshot)
print_result("Changes detected", changes)
print(f"  No changes: {len(changes) == 0}")


# ============================================
# 6. PERMISSION CHECK
# ============================================
print("\n" + "=" * 60)
print("6. PERMISSION CHECK")
print("=" * 60)

for file_path, data in snapshot.items():
    perm = data['permissions']
    status = "🔴 DANGEROUS" if perm in DANGEROUS_PERMISSIONS else \
             "🟠 HIGH RISK" if perm in HIGH_RISK_PERMISSIONS else \
             "✅ SAFE"
    print(f"  {status}: {file_path} ({perm})")


# ============================================
# 7. REAL-WORLD USE
# ============================================
print("\n" + "=" * 60)
print("7. REAL-WORLD USE")
print("=" * 60)

# Save snapshot to JSON
json_file = os.path.join(tempfile.gettempdir(), "quick_snapshot.json")
with open(json_file, "w") as f:
    json.dump(snapshot, f, indent=2)
print(f"Snapshot saved: {json_file}")

# Simulate file change
with open(os.path.join(test_dir, "file1.txt"), "w") as f:
    f.write("Modified content!")

# Verify changes
changes = verify_snapshot(test_dir, snapshot)
if changes:
    print("Changes detected:")
    for file_path, status in changes.items():
        print(f"  {file_path}: {status}")
else:
    print("No changes detected")


# ============================================
# 8. CLEANUP
# ============================================
print("\n" + "=" * 60)
print("8. CLEANUP")
print("=" * 60)

import shutil
shutil.rmtree(test_dir)
print(f"Removed: {test_dir}")

if os.path.exists(json_file):
    os.remove(json_file)
    print(f"Removed: {json_file}")

print("\n" + "=" * 60)
print("✅ QUICK REFERENCE COMPLETE!")
print("=" * 60)