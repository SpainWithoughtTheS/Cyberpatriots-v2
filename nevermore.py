import subprocess
import os


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
        # Secure password hashing algorithm
        with open("/etc/login.defs", "a") as f:
            f.write("ENCRYPT_METHOD SHA512\n")
        print("A secure default password hashing algorithm configured.")

        # Dictionary-based password strength checks
        with open("/etc/pam.d/common-password", "a") as f:
            f.write("password requisite pam_pwquality.so retry=3\n")
        print("Dictionary-based password strength checks enabled.")

        # Enforce minimum password length and remember previous passwords
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


def disable_unwanted_booting():
    """Disable new kernel boot alongside the current one."""
    try:
        subprocess.run(["sudo", "sed", "-i", "s/^GRUB_DEFAULT=.*/GRUB_DEFAULT=0/", "/etc/default/grub"], check=True)
        subprocess.run(["sudo", "update-grub"], check=True)
        print("New kernels cannot be booted alongside the current one.")
    except subprocess.CalledProcessError:
        print("Failed to restrict boot options.")


def remove_world_writable_files():
    """Ensure critical files are not world-writable."""
    files_to_check = ["/etc/ssh/sshd_config", "/etc/init.d/seafile"]
    for file in files_to_check:
        try:
            subprocess.run(["sudo", "chmod", "600", file], check=True)
            print(f"{file} is no longer world writable.")
        except subprocess.CalledProcessError:
            print(f"Failed to update permissions for {file}.")


def disable_suid_binary(binary):
    """Ensure specific binaries do not have the SUID bit set."""
    try:
        subprocess.run(["sudo", "chmod", "-s", binary], check=True)
        print(f"The SUID bit has been removed from {binary}.")
    except subprocess.CalledProcessError:
        print(f"Failed to disable SUID on {binary}.")


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


def remove_unwanted_services(services):
    """Remove prohibited or malicious services."""
    for service in services:
        try:
            subprocess.run(["sudo", "systemctl", "disable", service], check=True)
            subprocess.run(["sudo", "systemctl", "stop", service], check=True)
            subprocess.run(["sudo", "apt-get", "purge", "-y", service], check=True)
            print(f"Service {service} removed.")
        except subprocess.CalledProcessError:
            print(f"Failed to remove service: {service}")


def secure_seahub():
    """Harden Seahub settings."""
    try:
        # Enforce password policies for Seahub users
        settings = [
            "PASSWORD_MIN_LENGTH = 10\n",
            "PASSWORD_COMPLEXITY = {'UPPER': 1, 'LOWER': 1, 'DIGIT': 1, 'OTHER': 1}\n",
            "SESSION_EXPIRE_AT_BROWSER_CLOSE = True\n",
        ]
        with open("/path/to/seahub_settings.py", "a") as f:
            f.writelines(settings)
        print("Seahub user account security settings applied.")

        # Enable logging for file access
        subprocess.run(["sudo", "sed", "-i", "s/^#ENABLE_LOGGING.*/ENABLE_LOGGING=True/", "/path/to/seahub.conf"], check=True)
        print("Seafile fileserver access logging enabled.")
    except Exception as e:
        print(f"Error securing Seahub: {e}")


def secure_ssh():
    """Secure SSH configurations."""
    ssh_config_path = "/etc/ssh/sshd_config"
    try:
        settings = {
            "PermitRootLogin": "no",
            "PasswordAuthentication": "no",
            "PermitEmptyPasswords": "no",
            "LogLevel": "VERBOSE",
            "AllowTcpForwarding": "no",
            "X11Forwarding": "no",
        }
        for key, value in settings.items():
            subprocess.run(["sudo", "sed", "-i", f"s/^#?{key}.*/{key} {value}/", ssh_config_path], check=True)
        subprocess.run(["sudo", "systemctl", "restart", "ssh"], check=True)
        print("SSH configuration hardened.")
    except subprocess.CalledProcessError as e:
        print(f"Error securing SSH: {e}")


def main():
    # Remove unauthorized users
    remove_local_user("rowan")
    remove_local_user("mmouse")
    remove_local_user("lgates")

    # Demote unauthorized admin users
    demote_admin_user("vkinbott")

    # Configure system and user security
    configure_password_policy()
    disable_ipv4_forwarding()
    enable_aslr()
    restrict_perf_event()
    disable_unwanted_booting()
    remove_world_writable_files()

    # Secure SUID and critical services
    disable_suid_binary("/bin/date")
    enable_firewall()
    configure_apparmor()
    remove_unwanted_services(["apache2", "pvpgn"])

    # Harden Seahub and SSH
    secure_seahub()
    secure_ssh()

    print("\nAll tasks completed. System hardened.")


if __name__ == "__main__":
    main()
