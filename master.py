import os
import subprocess

# Function to remove unauthorized users
def remove_unauthorized_users():
    print("Removing unauthorized users...")
    users_to_remove = ["user1", "user2"]  # Add users to remove here
    for user in users_to_remove:
        subprocess.run(["sudo", "userdel", user])
    print("Unauthorized users removed.")

# Function to remove certain admin users
def remove_admin_users():
    print("Removing certain admin users...")
    admins_to_remove = ["admin1", "admin2"]  # Add admin users to remove here
    for admin in admins_to_remove:
        subprocess.run(["sudo", "deluser", admin, "sudo"])
    print("Certain admin users removed.")

# Function to spot root impostors
def spot_root_impostors():
    print("Spotting root impostors...")
    # Checking for users with UID 0 except root
    subprocess.run(["awk", "-F:", '($3 == "0" && $1 != "root") {print}', "/etc/passwd"])
    print("Root impostors spotted.")

# Function to configure secure default password hashing algorithm
def configure_password_hashing():
    print("Configuring secure password hashing...")
    subprocess.run(["sudo", "sed", "-i", 's/^PASS_MAX_DAYS.*/PASS_MAX_DAYS 90/', "/etc/login.defs"])
    # subprocess.run(["sudo", "sed", "-i", 's/^password\s\+\[success=2 default=ignore\]\s\+pam_unix.so/password        [success=2 default=ignore]      pam_unix.so crypt_blowfish minlen=10/', "/etc/pam.d/common-password"])
    # print("Password hashing algorithm secured using bcrypt.")

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
    subprocess.run(["sudo", "echo", "greeter-show-manual-login=false", ">>", "/etc/gdm3/custom.conf"])
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
        elif choice == "0":
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
