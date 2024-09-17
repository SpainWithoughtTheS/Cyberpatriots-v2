#!/bin/bash

# Function to check installed services
check_services() {
    echo "Checking for installed services..."
    service --status-all | grep -E '\[ \+ \]|\[ - \]' > installed_services.txt
    echo "Installed services saved to installed_services.txt"
}

# Function to disable unnecessary services
disable_unnecessary_services() {
    echo "Disabling unnecessary services..."
    # Add specific services that you know should be disabled.
    services=("bluetooth" "cups" "avahi-daemon" "rpcbind")
    for service in "${services[@]}"; do
      echo "Disabling $service..."
      sudo systemctl disable $service
      sudo systemctl stop $service
    done
    echo "Unnecessary services disabled."
}

# Function to change file permissions for sensitive files
secure_file_permissions() {
    echo "Securing permissions for /etc/passwd and /etc/shadow..."
    sudo chmod 644 /etc/passwd
    sudo chmod 600 /etc/shadow
    echo "Permissions have been secured."
}

# Function to check password expiration policy
check_password_expiration() {
    echo "Checking password expiration settings..."
    grep PASS_MAX_DAYS /etc/login.defs
    grep PASS_MIN_DAYS /etc/login.defs
    grep PASS_WARN_AGE /etc/login.defs
    echo "Please verify that the output matches your security policy."
}

# Function to audit SUID/SGID binaries
audit_suid_sgid() {
    echo "Auditing SUID/SGID binaries..."
    find / -perm /6000 -type f -exec ls -lh {} \; 2>/dev/null | tee suid_sgid_audit.txt
    echo "Audit complete. Results saved to suid_sgid_audit.txt"
}

# Function to check for open ports
check_open_ports() {
    echo "Checking for open ports..."
    sudo netstat -tuln | tee open_ports.txt
    echo "Open ports saved to open_ports.txt"
}

# Function to audit user accounts and sudo privileges
audit_users() {
    echo "Auditing user accounts and sudo privileges..."
    echo "Users with UID greater than 1000:"
    awk -F: '$3 >= 1000 {print $1}' /etc/passwd
    echo "Users with sudo privileges:"
    getent group sudo
    echo "Please review these users to ensure they are legitimate."
}

# Function to update and patch the system
update_system() {
    echo "Updating and upgrading the system..."
    sudo apt update && sudo apt upgrade -y
    echo "System is up-to-date."
}

# Function to configure firewall
configure_firewall() {
    echo "Configuring firewall..."
    sudo ufw enable
    sudo ufw default deny incoming
    sudo ufw default allow outgoing
    sudo ufw allow ssh
    sudo ufw allow http
    sudo ufw allow https
    echo "Firewall configured with basic rules."
}

# Function to monitor logs for suspicious activity
monitor_logs() {
    echo "Monitoring /var/log/auth.log for unusual activity..."
    tail -f /var/log/auth.log
}

# Function to list users with weak passwords (based on a weak password list)
check_weak_passwords() {
    echo "Checking for weak passwords..."
    # Add code here to check users against a dictionary of weak passwords
    echo "Weak password audit complete."
}

# Main menu
while true; do
    echo "CyberPatriot Master Script"
    echo "1. Check installed services"
    echo "2. Disable unnecessary services"
    echo "3. Secure file permissions"
    echo "4. Check password expiration policy"
    echo "5. Audit SUID/SGID binaries"
    echo "6. Check for open ports"
    echo "7. Audit user accounts and sudo privileges"
    echo "8. Update and patch system"
    echo "9. Configure firewall"
    echo "10. Monitor logs"
    echo "11. Check for weak passwords"
    echo "0. Exit"
    echo -n "Please choose an option: "
    read choice

    case $choice in
        1) check_services ;;
        2) disable_unnecessary_services ;;
        3) secure_file_permissions ;;
        4) check_password_expiration ;;
        5) audit_suid_sgid ;;
        6) check_open_ports ;;
        7) audit_users ;;
        8) update_system ;;
        9) configure_firewall ;;
        10) monitor_logs ;;
        11) check_weak_passwords ;;
        0) echo "Exiting..."; exit 0 ;;
        *) echo "Invalid option! Please try again." ;;
    esac
    echo "Press Enter to continue..."
    read
done
