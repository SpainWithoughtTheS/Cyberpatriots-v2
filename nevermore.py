import os
import subprocess

def remove_local_user(username):
    """Remove unauthorized local users."""
    try:
        subprocess.run(["sudo", "deluser", "--remove-home", username], check=True)
        print(f"Unauthorized local user {username} has been removed.")
    except subprocess.CalledProcessError:
        print(f"Failed to remove user {username}.")

def demote_admin_user(username):
    """Demote unauthorized users from the sudo/admin group."""
    try:
        subprocess.run(["sudo", "deluser", username, "sudo"], check=True)
        print(f"Local user {username} is no longer an administrator.")
    except subprocess.CalledProcessError:
        print(f"Failed to demote user {username}.")

def configure_password_policy():
    """Configure secure password policies."""
    try:
        # Set secure password hashing algorithm
        with open("/etc/login.defs", "a") as f:
            f.write("ENCRYPT_METHOD SHA512\n")
        print("A secure default password hashing algorithm configured.")

        # Enable dictionary-based password strength checks
        with open("/etc/pam.d/common-password", "a") as f:
            f.write("password requisite pam_pwquality.so retry=3\n")
        print("Dictionary-based password strength checks enabled.")

        # Set minimum password length and remember previous passwords
        with open("/etc/security/pwquality.conf", "a") as f:
            f.write("minlen = 12\nretry = 3\n")
        print("A minimum password length is enforced.")

        with open("/etc/pam.d/common-password", "a") as f:
            f.write("password requisite pam_unix.so remember=5\n")
        print("Previous passwords are remembered.")
    except Exception as e:
        print(f"Error configuring password policies: {e}")

def disable_ipv4_forwarding():
    """Disable IPv4 forwarding."""
    try:
        subprocess.run(["sudo", "sysctl", "-w", "net.ipv4.ip_forward=0"], check=True)
        print("IPv4 forwarding disabled.")
    except subprocess.CalledProcessError:
        print("Failed to disable IPv4 forwarding.")

def enable_aslr():
    """Enable Address Space Layout Randomization (ASLR)."""
    try:
        with open("/proc/sys/kernel/randomize_va_space", "w") as f:
            f.write("2")
        print("Address space layout randomization enabled.")
    except Exception as e:
        print(f"Failed to enable ASLR: {e}")

def restrict_perf_event():
    """Restrict access to CPU performance events."""
    try:
        with open("/proc/sys/kernel/perf_event_paranoid", "w") as f:
            f.write("3")
        print("perf_event_open() is restricted to processes with CAP_PERFMON.")
    except Exception as e:
        print(f"Failed to restrict perf_event: {e}")

def configure_ssh():
    """Secure SSH configuration."""
    try:
        ssh_config_path = "/etc/ssh/sshd_config"
        changes = {
            "PermitRootLogin": "no",
            "PasswordAuthentication": "no",
            "PermitEmptyPasswords": "no",
            "LogLevel": "INFO",
            "AllowTcpForwarding": "no",
            "X11Forwarding": "no"
        }
        for key, value in changes.items():
            subprocess.run(["sudo", "sed", "-i", f"s/^#?{key}.*/{key} {value}/", ssh_config_path], check=True)
        subprocess.run(["sudo", "systemctl", "restart", "ssh"], check=True)
        print("SSH configuration secured.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to configure SSH: {e}")

def remove_unwanted_packages(packages):
    """Remove prohibited or malicious software."""
    try:
        for package in packages:
            subprocess.run(["sudo", "apt-get", "purge", "-y", package], check=True)
            print(f"Prohibited software {package} removed.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to remove software: {e}")

def enable_firewall():
    """Enable UFW and configure it to start on boot."""
    try:
        subprocess.run(["sudo", "ufw", "enable"], check=True)
        subprocess.run(["sudo", "ufw", "logging", "on"], check=True)
        print("UFW is enabled, active on startup, and logging.")
    except subprocess.CalledProcessError:
        print("Failed to enable UFW.")

def configure_apparmor():
    """Enable and start AppArmor."""
    try:
        subprocess.run(["sudo", "systemctl", "enable", "apparmor"], check=True)
        subprocess.run(["sudo", "systemctl", "start", "apparmor"], check=True)
        print("AppArmor service enabled and started.")
    except subprocess.CalledProcessError:
        print("Failed to configure AppArmor.")

def harden_miscellaneous():
    """Handle miscellaneous security tasks."""
    try:
        # Disable root login for GDM
        subprocess.run(["sudo", "sed", "-i", "s/^#?AllowRoot.*/AllowRoot=false/", "/etc/gdm3/custom.conf"], check=True)
        print("GDM greeter root login disabled.")

        # Restrict preload environment variables with sudo
        subprocess.run(["sudo", "sed", "-i", "s/^#?Defaults\s+env_reset.*/Defaults env_reset/", "/etc/sudoers"], check=True)
        print("Environment variable defining preloaded libraries is not kept with sudo.")
    except subprocess.CalledProcessError:
        print("Failed to harden miscellaneous security settings.")

def main():
    # Perform each task
    remove_local_user("rowan")
    remove_local_user("mmouse")
    demote_admin_user("vkinbott")
    remove_local_user("lgates")
    configure_password_policy()
    disable_ipv4_forwarding()
    enable_aslr()
    restrict_perf_event()
    configure_ssh()
    remove_unwanted_packages(["apache2", "pvpgn", "sucrack", "changeme", "unworkable"])
    enable_firewall()
    configure_apparmor()
    harden_miscellaneous()

if __name__ == "__main__":
    main()
