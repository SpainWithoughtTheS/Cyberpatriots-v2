import subprocess

CRITICAL_USERS = [
    'root', 'sys', 'bin', 'daemon', 'nobody', 'systemd-network', 'systemd-resolve',
    'messagebus', 'systemd-timesync', 'syslog', '_apt', 'tss', 'uuidd', 'systemd-oom',
    'tcpdump', 'avahi-autoipd', 'usbmux', 'dnsmasq', 'kernoops', 'avahi', 'cups-pk-helper',
    'rtkit', 'whoopsie', 'sssd', 'speech-dispatcher', 'fwupd-refresh', 'nm-openvpn',
    'saned', 'colord', 'geoclue', 'pulse', 'gnome-initial-setup', 'hplip', 'gdm', 'mysql',
    'memcache', 'sshd', 'sync', 'games', 'man', 'lp', 'mail', 'news', 'uucp', 'proxy', 'www-data', 'backup',
    'list', 'irc', 'gnats'
]


def get_system_users():
    """Get a list of current system users."""
    with open('/etc/passwd', 'r') as passwd_file:
        return [line.split(':')[0] for line in passwd_file.readlines()]

def remove_user(user):
    """Remove a user from the system."""
    subprocess.run(['sudo', 'userdel', '-r', user], check=False)

def add_user(user, is_admin=False):
    """Add a user to the system, optionally adding to sudo group."""
    subprocess.run(['sudo', 'useradd', '-m', user], check=False)
    if is_admin:
        subprocess.run(['sudo', 'usermod', '-aG', 'sudo', user], check=False)

def set_password(user, password="CyberPatriot@24"):
    """Set the password for a user."""
    subprocess.run(['sudo', 'chpasswd'], input=f"{user}:{password}".encode(), check=False)

def ensure_group_membership(user, is_admin):
    """Ensure the user has the correct group membership."""
    if is_admin:
        subprocess.run(['sudo', 'usermod', '-aG', 'sudo', user], check=False)
    else:
        subprocess.run(['sudo', 'gpasswd', '-d', user, 'sudo'], check=False)

def change_password_policy(user):
    """Change the password policy for the given user."""
    subprocess.run(['sudo', 'chage', '-m', '7', '-M', '90', '-W', '14', '-I', '30', user], check=True)

def read_authorized_users(file_path):
    """Read authorized admins and users from the users.txt file."""
    authorized_admins = []
    authorized_users = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        is_admin_section = False
        is_user_section = False
        
        for line in lines:
            line = line.strip()
            if line == "Authorized Administrators:":
                is_admin_section = True
                is_user_section = False
            elif line == "Authorized Users:":
                is_admin_section = False
                is_user_section = True
            elif line and is_admin_section:
                authorized_admins.append(line)
            elif line and is_user_section:
                authorized_users.append(line)
                
    return authorized_admins, authorized_users

def confirm_removal(user):
    """Ask for confirmation to remove a user."""
    response = input(f"Do you want to remove unauthorized user {user}? (y/n): ").strip().lower()
    return response == 'y'

def main():
    # Read the list of authorized admins and users from users.txt
    file_path = 'users.txt'
    authorized_admins, authorized_users = read_authorized_users(file_path)
    all_authorized_users = authorized_admins + authorized_users

    # Fetch current system users
    system_users = get_system_users()

    # Step 1: Prompt to remove users not in the authorized list and not critical
    for user in system_users:
        if user not in all_authorized_users and user not in CRITICAL_USERS:
            if confirm_removal(user):
                remove_user(user)
                print(f"Removed unauthorized user: {user}")

    # Step 2: Add missing users and set up admin or regular user permissions
    for user in all_authorized_users:
        if user not in system_users:
            is_admin = user in authorized_admins
            add_user(user, is_admin)
            print(f"Added missing user: {user} {'(admin)' if is_admin else '(user)'}")

    # Step 3: Ensure each authorized user's role is correct
    for user in authorized_admins:
        ensure_group_membership(user, is_admin=True)

    for user in authorized_users:
        ensure_group_membership(user, is_admin=False)

    # Step 4: Set passwords for all authorized users
    for user in all_authorized_users:
        set_password(user)

    # Step 5: Change password policies for all users
    for user in all_authorized_users:
        change_password_policy(user)

if __name__ == "__main__":
    main()
