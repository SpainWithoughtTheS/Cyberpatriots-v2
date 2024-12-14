import os
import subprocess

# Function to remove unauthorized users
def remove_unauthorized_users():
    print("Removing unauthorized users...")
    users_to_remove = ["user1", "user2"]  # Add users to remove here
    for user in users_to_remove:
        confirm = input(f"Are you sure you want to remove the user '{user}'? (yes/no): ").strip().lower()
        if confirm == "yes":
            subprocess.run(["sudo", "userdel", user])
            print(f"User '{user}' removed.")
        else:
            print(f"Skipped removing user '{user}'.")
    print("Unauthorized users removal process completed.")

# Function to remove certain admin users
def remove_admin_users():
    print("Removing certain admin users...")
    admins_to_remove = ["admin1", "admin2"]  # Add admin users to remove here
    for admin in admins_to_remove:
        confirm = input(f"Are you sure you want to remove admin privileges for '{admin}'? (yes/no): ").strip().lower()
        if confirm == "yes":
            subprocess.run(["sudo", "deluser", admin, "sudo"])
            print(f"Admin privileges removed for '{admin}'.")
        else:
            print(f"Skipped removing admin privileges for '{admin}'.")
    print("Admin users removal process completed.")

# Function to spot root impostors
def spot_root_impostors():
    print("Spotting root impostors...")
    subprocess.run(["awk", "-F:", '($3 == "0" && $1 != "root") {print}', "/etc/passwd"])
    print("Root impostors spotting completed.")

# Function to configure secure default password hashing algorithm
def configure_password_hashing():
    print("Configuring secure password hashing...")
    subprocess.run(["sudo", "sed", "-i", 's/^PASS_MAX_DAYS.*/PASS_MAX_DAYS 90/', "/etc/login.defs"])
    print("Password hashing configuration updated.")

# Function to enable extra dictionary-based password strength checks
def enable_dictionary_password_checks():
    print("Enabling dictionary-based password strength checks...")
    subprocess.run(["sudo", "apt-get", "install", "-y", "cracklib-runtime"])
    subprocess.run(["sudo", "sed", "-i", 's/# dictcheck/dictcheck/', "/etc/pam.d/common-password"])
    print("Password strength checks enabled.")

# Function to enforce password length
def enforce_min_password_length():
    print("Enforcing minimum password length...")
    subprocess.run(["sudo", "sed", "-i", 's/pam_unix.so.*/pam_unix.so minlen=12/', "/etc/pam.d/common-password"])
    print("Minimum password length enforced.")

# Function to disable IP forwarding
def disable_ipv_forwarding():
    print("Disabling IPv forwarding...")
    subprocess.run(["sudo", "sysctl", "-w", "net.ipv4.ip_forward=0"])
    print("IPv forwarding disabled.")

# Function to enable Address Space Layout Randomization (ASLR)
def enable_aslr():
    print("Enabling ASLR...")
    subprocess.run(["sudo", "sysctl", "-w", "kernel.randomize_va_space=2"])
    print("ASLR enabled.")

# Function to disable new kernels from booting alongside the current one
def disable_new_kernel_boot():
    print("Disabling new kernel boot...")
    subprocess.run(["sudo", "grub-editenv", "/boot/grub/grubenv", "set", "boot_once=true"])
    print("New kernel boot disabled.")

# Function to restrict perf_event_open to processes with CAP_PERFMON
def restrict_perf_event_open():
    print("Restricting access to CPU performance events...")
    subprocess.run(["sudo", "sysctl", "-w", "kernel.perf_event_paranoid=3"])
    print("perf_event_open restricted.")

# Function to disable GDM greeter root login
def disable_gdm_root_login():
    print("Disabling GDM greeter root login...")
    subprocess.run(["sudo", "sh", "-c", "echo -e '\\n[security]\\nAllowRoot=false' >> /etc/gdm3/custom.conf"], check=True)
    print("GDM root login disabled.")

# Function to disable SSH root login
def disable_ssh_root_login():
    print("Disabling SSH root login...")
    subprocess.run(["sudo", "sed", "-i", 's/PermitRootLogin yes/PermitRootLogin no/', "/etc/ssh/sshd_config"])
    subprocess.run(["sudo", "systemctl", "restart", "ssh"])
    print("SSH root login disabled.")

# Function to ensure SSH does not allow empty passwords
def disable_empty_ssh_passwords():
    print("Disabling empty SSH passwords...")
    subprocess.run(["sudo", "sed", "-i", 's/PermitEmptyPasswords yes/PermitEmptyPasswords no/', "/etc/ssh/sshd_config"])
    subprocess.run(["sudo", "systemctl", "restart", "ssh"])
    print("Empty SSH passwords disabled.")

# Function to disable guest user login
def disable_guest_users():
    print("Disabling guest users...")
    try:
        # Check if LightDM is the active display manager
        lightdm_status = subprocess.run(["sudo", "systemctl", "is-active", "lightdm"], capture_output=True, text=True)
        if lightdm_status.stdout.strip() == "active":
            subprocess.run(["sudo", "sh", "-c", "echo '[SeatDefaults]' >> /etc/lightdm/lightdm.conf"])
            subprocess.run(["sudo", "sh", "-c", "echo 'allow-guest=false' >> /etc/lightdm/lightdm.conf"])
            print("Guest user login disabled in LightDM.")
        
        # Check if GDM is the active display manager
        gdm_status = subprocess.run(["sudo", "systemctl", "is-active", "gdm"], capture_output=True, text=True)
        if gdm_status.stdout.strip() == "active":
            subprocess.run(["sudo", "sh", "-c", "echo -e '\\n[security]\\nAllowGuest=false' >> /etc/gdm3/custom.conf"])
            print("Guest user login disabled in GDM.")
        
        # Check if SDDM is the active display manager
        sddm_status = subprocess.run(["sudo", "systemctl", "is-active", "sddm"], capture_output=True, text=True)
        if sddm_status.stdout.strip() == "active":
            subprocess.run(["sudo", "sh", "-c", "echo -e '[General]\\nEnableGuest=false' >> /etc/sddm.conf"])
            print("Guest user login disabled in SDDM.")
        
        # If none of the above display managers are active
        if lightdm_status.stdout.strip() != "active" and gdm_status.stdout.strip() != "active" and sddm_status.stdout.strip() != "active":
            print("No supported display manager is currently active. Please manually configure guest login settings for your display manager.")
    
    except Exception as e:
        print(f"An error occurred while disabling guest users: {e}")

# Main menu
def main():
    while True:
        print("\nSecurity Master Script")
        print("1. Remove Unauthorized Users")
        print("2. Remove Certain Admin Users")
        print("3. Spot Root Impostors")
        print("4. Configure Secure Password Hashing")
        print("5. Enable Dictionary Password Strength Checks")
        print("6. Enforce Minimum Password Length")
        print("7. Disable IPv Forwarding")
        print("8. Enable ASLR")
        print("9. Disable New Kernel Boot")
        print("10. Restrict perf_event_open to CAP_PERFMON")
        print("11. Disable GDM Root Login")
        print("12. Disable SSH Root Login")
        print("13. Disable Empty SSH Passwords")
        print("14. Disable Guest Users")
        print("0. Exit")
        
        choice = input("Enter your choice: ")

        if choice == "1":
            remove_unauthorized_users()
        elif choice == "2":
            remove_admin_users()
        elif choice == "3":
            spot_root_impostors()
        elif choice == "4":
            configure_password_hashing()
        elif choice == "5":
            enable_dictionary_password_checks()
        elif choice == "6":
            enforce_min_password_length()
        elif choice == "7":
            disable_ipv_forwarding()
        elif choice == "8":
            enable_aslr()
        elif choice == "9":
            disable_new_kernel_boot()
        elif choice == "10":
            restrict_perf_event_open()
        elif choice == "11":
            disable_gdm_root_login()
        elif choice == "12":
            disable_ssh_root_login()
        elif choice == "13":
            disable_empty_ssh_passwords()
        elif choice == "14":
            disable_guest_users()
        elif choice == "0":
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
