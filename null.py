import os
import subprocess

# PAM configuration directory
PAM_CONFIG_DIR = "/usr/share/pam-configs"
FAILLOCK_PATH = os.path.join(PAM_CONFIG_DIR, "faillock")
FAILLOCK_NOTIFY_PATH = os.path.join(PAM_CONFIG_DIR, "faillock_notify")

# Ensure script is run with sudo/root privileges
if os.geteuid() != 0:
    print("Please run this script with sudo/root privileges.")
    exit()

# Function to write configuration to a file
def create_pam_file(file_path, content):
    try:
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"{os.path.basename(file_path)} configuration file created successfully.")
    except Exception as e:
        print(f"Failed to create {file_path}: {e}")

# Task 1: Create and configure the 'faillock' file
faillock_content = """Name: Enforce failed login attempt counter
Default: no
Priority: 0
Auth-Type: Primary
Auth: [default=die] pam_faillock.so authfail
Auth: sufficient pam_faillock.so authsucc
"""
create_pam_file(FAILLOCK_PATH, faillock_content)

# Task 2: Create and configure the 'faillock_notify' file
faillock_notify_content = """Name: Notify on failed login attempts
Default: no
Priority: 1024
Auth-Type: Primary
Auth: requisite pam_faillock.so preauth
"""
create_pam_file(FAILLOCK_NOTIFY_PATH, faillock_notify_content)

# Task 3: Update PAM configuration to apply changes
try:
    print("Updating PAM configuration to apply changes...")
    subprocess.run(["pam-auth-update", "--package"], check=True)
    print("Select 'Notify on failed login attempts' and 'Enforce failed login attempt counter' using the spacebar, then press <Ok>.")
except subprocess.CalledProcessError as e:
    print(f"Failed to update PAM configuration: {e}")

print("Script execution completed. Account lockout policies are now enforced.")
