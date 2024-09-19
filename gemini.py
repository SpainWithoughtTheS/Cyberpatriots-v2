import subprocess
import os
import time
import logging

# Configure logging
logging.basicConfig(filename='hardening_log.txt', level=logging.INFO)

def run_command(command):
    """Runs a system command and logs the output."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        logging.info(f"Command executed: {command}")
        logging.info(f"Output: {result.stdout}")
        if result.stderr:
            logging.warning(f"Error: {result.stderr}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error executing command: {command}")
        logging.error(f"Error message: {e}")

# Function to check installed services
def check_services():
    logging.info("Checking installed services...")
    run_command("service --status-all | grep -E '\[ \+ \]|\[ - \]' > installed_services.txt")

# Function to disable unnecessary services
def disable_unnecessary_services():
    logging.info("Disabling unnecessary services...")
    services = ["bluetooth", "cups", "avahi-daemon", "rpcbind"]
    for service in services:
        run_command(f"sudo systemctl disable {service}")
        run_command(f"sudo systemctl stop {service}")

# Function to secure file permissions for sensitive files
def secure_file_permissions():
    logging.info("Securing permissions for /etc/passwd and /etc/shadow...")
    run_command("sudo chmod 644 /etc/passwd")
    run_command("sudo chmod 600 /etc/shadow")

# Function to check password expiration policy
def check_password_expiration():
    logging.info("Checking password expiration settings...")
    run_command("grep PASS_MAX_DAYS /etc/login.defs")
    run_command("grep PASS_MIN_DAYS /etc/login.defs")
    run_command("grep PASS_WARN_AGE /etc/login.defs")

# Function to audit SUID/SGID binaries
def audit_suid_sgid():
    logging.info("Auditing SUID/SGID binaries...")
    run_command("find / -perm /6000 -type f -exec ls -lh {} \\; 2>/dev/null > suid_sgid_audit.txt")

# Function to check for open ports
def check_open_ports():
    logging.info("Checking for open ports...")
    run_command("sudo netstat -tuln > open_ports.txt")

# Function to audit user accounts and sudo privileges
def audit_users():
    logging.info("Auditing user accounts and sudo privileges...")
    run_command("awk -F: '$3 >= 1000 {print $1}' /etc/passwd")
    run_command("getent group sudo")

# Function to update and patch the system
def update_system():
    logging.info("Updating and upgrading the system...")
    run_command("sudo apt update && sudo apt upgrade -y")

# Function to configure firewall
def configure_firewall():
    logging.info("Configuring firewall...")
    run_command("sudo ufw enable")
    run_command("sudo ufw default deny incoming")
    run_command("sudo ufw default allow outgoing")
    run_command("sudo ufw allow ssh")
    run_command("sudo ufw allow http")
    run_command("sudo ufw allow https")

# Function to monitor logs for suspicious activity
def monitor_logs():
    logging.info("Monitoring /var/log/auth.log for unusual activity...")
    try:
        # Tail the log file in real-time
        subprocess.run(['tail', '-f', '/var/log/auth.log'])
    except KeyboardInterrupt:
        logging.info("Monitoring interrupted by user.")
    except Exception as e:
        logging.error(f"Error while monitoring logs: {e}")

# Function to check for weak passwords (using a dictionary)

def check_weak_passwords():
    logging.info("Checking for weak passwords...")
    # Load weak password dictionary
    weak_passwords = set()
    try:
        with open('weak_passwords.txt', 'r') as file:
            weak_passwords = {line.strip() for line in file}
    except FileNotFoundError:
        logging.error("Weak password dictionary not found.")
        return

    # Iterate over users and check their passwords
    with open('/etc/shadow', 'r') as shadow_file:
        for line in shadow_file:
            user_data = line.split(':')
            user, password_hash = user_data[0], user_data[1]
            if password_hash in weak_passwords:
                logging.warning(f"Weak password detected for user: {user}")

# Function to check for outdated packages
def check_outdated_packages():
    logging.info("Checking for outdated packages...")
    run_command("sudo apt update && sudo apt upgrade -y")

# Function to check for root logins
def check_root_logins():
    logging.info("Checking for root logins...")
    run_command("grep 'root' /var/log/auth.log | grep 'login'")

# Function to check for SSH brute force attempts
def check_ssh_brute_force():
    logging.info("Checking for SSH brute force attempts...")
    run_command("grep 'Failed password for root' /var/log/auth.log")

# Function to check for cron job security
def check_cron_job_security():
    logging.info("Checking cron job security...")
    run_command("grep -v '^#.*' /etc/crontab | grep -v 'root'")

# Function to check for file system integrity
def check_file_system_integrity():
    logging.info("Checking file system integrity...")
    run_command("fsck -f /dev/sda1")

# Main menu
def main():
    while True:
        print("\nSecurity Master Script")
        print("1. Check installed services")
        print("2. Disable unnecessary services")
        print("3. Secure file permissions")
        print("4. Check password expiration policy")
        print("5. Audit SUID/SGID binaries")
        print("6. Check for open ports")
        print("7. Audit user accounts and sudo privileges")
        print("8. Update and patch system")
        print("9. Configure firewall")
        print("10. Monitor logs")
        print("11. Check for weak passwords")
        print("12. Check for outdated packages")
        print("13. Check for root logins")
        print("14. Check for SSH brute force attempts")
        print("15. Check for cron job security")
        print("16. Check for file system integrity")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            check_services()
        elif choice == "2":
            disable_unnecessary_services()
        elif choice == "3":
            secure_file_permissions()
        elif choice == "4":
            check_password_expiration()
        elif choice == "5":
            audit_suid_sgid()
        elif choice == "6":
            check_open_ports()
        elif choice == "7":
            audit_users()
        elif choice == "8":
            update_system()
        elif choice == "9":
            configure_firewall()
        elif choice == "10":
            monitor_logs()
        elif choice == "11":
            check_weak_passwords()
        elif choice == "12":
            check_outdated_packages()
        elif choice == "13":
            check_root_logins()
        elif choice == "14":
            check_ssh_brute_force()
        elif choice == "15":
            check_cron_job_security()
        elif choice == "16":
            check_file_system_integrity()
        elif choice == "0":
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
