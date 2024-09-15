import os
import subprocess
import sys

# Helper function to run system commands
def run_command(command, exit_on_fail=True):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"Command succeeded: {command}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.stderr}")
        if exit_on_fail:
            sys.exit(1)
        return None

# Disable Unauthorized Users
def remove_unauthorized_users(users_to_remove):
    """Remove unauthorized users"""
    for user in users_to_remove:
        print(f"Removing unauthorized user: {user}")
        run_command(f"sudo userdel -r {user}")
        run_command(f"sudo groupdel {user}")

# Enforce password policies (length, complexity, etc.)
def enforce_password_policy():
    print("Enforcing password policies...")
    # Ensure password hashing algorithm is secure
    run_command("sudo sed -i '/pam_unix.so/ s/$/ sha512/' /etc/pam.d/common-password")
    
    # Enforce minimum password length and password complexity
    run_command("sudo sed -i '/pam_unix.so/ s/$/ minlen=10/' /etc/pam.d/common-password")
    run_command("sudo apt-get install -y libpam-cracklib")
    run_command("sudo sed -i '/pam_cracklib.so/ s/$/ ucredit=-1 lcredit=-1 dcredit=-1 ocredit=-1/' /etc/pam.d/common-password")
    
    # Remember previous passwords
    run_command("sudo sed -i '/pam_unix.so/ s/$/ remember=5/' /etc/pam.d/common-password")

# Disable root login in SSH and secure SSH settings
def secure_ssh_config():
    print("Securing SSH configuration...")
    # Disable root login
    run_command("sudo sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config")
    
    # Disable key-based authentication (if required)
    run_command("sudo sed -i 's/#PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config")
    
    # Ensure LogLevel is not set to QUIET
    run_command("sudo sed -i 's/#LogLevel INFO/LogLevel VERBOSE/' /etc/ssh/sshd_config")
    
    # Disallow empty passwords
    run_command("sudo sed -i 's/#PermitEmptyPasswords yes/PermitEmptyPasswords no/' /etc/ssh/sshd_config")
    
    # Disable processing of client environment variables
    run_command("sudo sed -i 's/#PermitUserEnvironment yes/PermitUserEnvironment no/' /etc/ssh/sshd_config")
    
    run_command("sudo systemctl restart sshd")

# Disable IPv4 forwarding and enable Address Space Layout Randomization (ASLR)
def network_security_hardening():
    print("Disabling IPv4 forwarding and enabling ASLR...")
    # Disable IPv4 forwarding
    run_command("echo 0 | sudo tee /proc/sys/net/ipv4/ip_forward")
    
    # Enable Address Space Layout Randomization
    run_command("sudo sysctl -w kernel.randomize_va_space=2")

# Enable UFW and AppArmor services
def enable_firewall_apparmor():
    print("Enabling UFW and AppArmor...")
    # Enable UFW
    run_command("sudo ufw enable")
    run_command("sudo ufw logging on")
    
    # Enable AppArmor
    run_command("sudo systemctl enable apparmor")
    run_command("sudo systemctl start apparmor")

# Configure Seafile services (if installed)
def configure_seafile():
    print("Configuring Seafile services...")
    # Secure Seahub password policies
    seafile_settings = [
        'SECURE_CookiesHttpOnly = True',
        'SECURE_CookiesSecure = True',
        'PASSWORD_MIN_LENGTH = 10',
        'PASSWORD_MIN_DIGITS = 1',
        'PASSWORD_MIN_UPPER = 1',
        'PASSWORD_MIN_LOWER = 1',
        'PASSWORD_MIN_SYMBOLS = 1',
        'SESSION_EXPIRE_AT_BROWSER_CLOSE = True',
        'LOG_FILES_ACCESS = True',
    ]
    seafile_conf = "/path/to/seahub/settings.py"  # Replace with actual path
    for setting in seafile_settings:
        run_command(f"echo '{setting}' | sudo tee -a {seafile_conf}")

# Disable unnecessary services and remove prohibited software
def remove_unnecessary_services_and_software():
    print("Removing unnecessary services and prohibited software...")
    prohibited_software = ['sucrack', 'changeme', 'unworkable', 'apache2', 'pvpgn']
    for software in prohibited_software:
        run_command(f"sudo apt-get purge -y {software}")

# Apply additional system hardening (disabling SUID, coredumps, etc.)
def additional_system_hardening():
    print("Applying additional system hardening...")
    # Ensure no SUID on binaries like 'date'
    run_command("sudo chmod -s /bin/date")
    
    # Disable coredumps for sudo
    run_command("echo 'CoredumpDisable=yes' | sudo tee -a /etc/systemd/system.conf")
    
    # Restrict perf_event_open()
    run_command("echo 'kernel.perf_event_paranoid=3' | sudo tee -a /etc/sysctl.conf")
    run_command("sysctl -p")

# Run daily updates
def enable_daily_updates():
    print("Enabling daily updates...")
    run_command("sudo sed -i 's/^APT::Periodic::Update-Package-Lists.*/APT::Periodic::Update-Package-Lists \"1\";/' /etc/apt/apt.conf.d/10periodic")

# Main function to orchestrate the hardening process
def main():
    # Remove unauthorized users
    unauthorized_users = ['rowan', 'mmouse', 'lgates', 'vkinbott']  # Modify based on your setup
    remove_unauthorized_users(unauthorized_users)
    
    # Enforce password policies
    enforce_password_policy()
    
    # Secure SSH
    secure_ssh_config()
    
    # Network security hardening
    network_security_hardening()
    
    # Enable firewall and AppArmor
    enable_firewall_apparmor()
    
    # Configure Seafile (if installed)
    configure_seafile()
    
    # Remove unnecessary services and prohibited software
    remove_unnecessary_services_and_software()
    
    # Apply additional hardening
    additional_system_hardening()
    
    # Enable daily updates
    enable_daily_updates()
    
    print("System hardening completed.")

if __name__ == "__main__":
    main()
