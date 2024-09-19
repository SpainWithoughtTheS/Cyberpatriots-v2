import subprocess
import os

CRITICAL_USERS = ['root', 'sys', 'bin', 'daemon', 'nobody', 'systemd-network', 'systemd-resolve', 'messagebus', 
                  'systemd-timesync', 'syslog', '_apt', 'tss', 'uuidd', 'systemd-oom', 'tcpdump', 'avahi-autoipd', 
                  'usbmux', 'dnsmasq', 'kernoops', 'avahi', 'cups-pk-helper', 'rtkit', 'whoopsie', 'sssd', 
                  'speech-dispatcher', 'fwupd-refresh', 'nm-openvpn', 'saned', 'colord', 'geoclue', 'pulse', 
                  'gnome-initial-setup', 'hplip', 'gdm', 'mysql', 'memcache', 'sshd']  # Add more as needed

def get_system_users():
    """Get the list of system users."""
    try:
        with open('/etc/passwd', 'r') as passwd_file:
            users = [line.split(':')[0] for line in passwd_file.readlines()]
        return users
    except FileNotFoundError:
        print("Could not read the /etc/passwd file.")
        return []

def remove_user(user):
    """Remove the user from the system."""
    try:
        subprocess.run(["sudo", "userdel", user], check=True)
        print(f"User {user} removed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to remove user {user}: {e}")

def confirm_removal(user):
    """Ask the user for confirmation to remove a user."""
    response = input(f"Do you want to remove user {user}? (yes/no): ").strip().lower()
    return response == 'yes'

def read_allowed_users(file_path):
    """Read allowed users from a file."""
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return []
    
    with open(file_path, 'r') as f:
        allowed_users = [line.strip() for line in f.readlines()]
    
    return allowed_users

def main():
    file_path = 'allowed_users.txt'  # You can modify the file name or path here
    allowed_users = read_allowed_users(file_path)

    if not allowed_users:
        print("No allowed users found or file is empty.")
        return

    # Get the list of system users
    system_users = get_system_users()

    # Iterate through system users and remove any that are not in the allowed list and not critical
    for user in system_users:
        if user not in allowed_users and user not in CRITICAL_USERS:
            if confirm_removal(user):
                remove_user(user)
        elif user in CRITICAL_USERS:
            print(f"Skipping critical user: {user}")

if __name__ == "__main__":
    main()
