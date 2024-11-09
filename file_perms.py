import os
import stat

directories = ["/etc", "/var", "/usr/local"]

incorrect_permissions_files = []
skipped_files = []

def check_and_fix_ownership_permissions(directory):
    for root, _, files in os.walk(directory):
        for name in files:
            filepath = os.path.join(root, name)
            try:

                file_stat = os.stat(filepath)
                file_uid = file_stat.st_uid
                file_gid = file_stat.st_gid
                file_mode = file_stat.st_mode

                if file_uid != 0 or file_gid != 0:
                    incorrect_permissions_files.append((filepath, "Incorrect ownership"))
                    os.chown(filepath, 0, 0)  

                expected_modes = [stat.S_IRUSR | stat.S_IWUSR, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP]
                if file_mode & 0o777 not in expected_modes:
                    incorrect_permissions_files.append((filepath, "Incorrect permissions"))
                    os.chmod(filepath, expected_modes[1])  

            except FileNotFoundError:

                continue
            except PermissionError:

                skipped_files.append(filepath)

print("Checking for incorrect ownership and permissions in specified directories...")

for directory in directories:
    if os.path.exists(directory):
        check_and_fix_ownership_permissions(directory)
    else:
        print(f"Directory {directory} does not exist, skipping...")

if not incorrect_permissions_files:
    print("All files in the specified directories have correct ownership and permissions.")
else:
    print("The following files had incorrect ownership or permissions and were fixed:")
    for file, issue in incorrect_permissions_files:
        print(f"{file}: {issue}")

if skipped_files:
    print("\nThe following files could not be modified due to permissions restrictions:")
    for file in skipped_files:
        print(file)
