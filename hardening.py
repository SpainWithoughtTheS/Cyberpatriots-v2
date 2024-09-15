import os
import subprocess
import sys

def run_command(command, exit_on_fail=True):
    """Run a shell command and check for success."""
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"Command succeeded: {command}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.stderr}")
        if exit_on_fail:
            sys.exit(1)
        return None

def secure_root_login():
    """Secure SSH root login by setting PermitRootLogin to no."""
    print("Securing root login...")
    run_command("sed -i 's/^#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config")
    run_command("systemctl restart sshd")

def disable_guest_user():
    """Disable the guest user in LightDM."""
    print("Disabling guest user...")
    with open("/etc/lightdm/lightdm.conf", "a") as f:
        f.write("allow-guest=false\n")
    run_command("systemctl restart lightdm")

def check_uid_0_users():
    """Check for UID 0 users and log them."""
    print("Checking for UID 0 users...")
    uid_0_users = run_command("awk -F: '($3 == 0) {print $1}' /etc/passwd")
    with open("/root/uid_0_users.txt", "w") as f:
        f.write(uid_0_users)

def enforce_password_policy():
    """Enforce password policies for expiration, complexity, and lockout."""
    print("Enforcing password policies...")
    # Password expiration
    run_command("sed -i 's/^PASS_MIN_DAYS.*/PASS_MIN_DAYS 7/' /etc/login.defs")
    run_command("sed -i 's/^PASS_MAX_DAYS.*/PASS_MAX_DAYS 90/' /etc/login.defs")
    run_command("sed -i 's/^PASS_WARN_AGE.*/PASS_WARN_AGE 14/' /etc/login.defs")

    # Password complexity
    run_command("sed -i '/pam_unix.so/ s/$/ minlen=8 remember=5/' /etc/pam.d/common-password")
    if not run_command("grep -q 'pam_cracklib.so' /etc/pam.d/common-password", exit_on_fail=False):
        run_command("apt-get install -y libpam-cracklib")
        run_command("echo 'password requisite pam_cracklib.so ucredit=-1 lcredit=-1 dcredit=-1 ocredit=-1' >> /etc/pam.d/common-password")

    # Lockout policy
    if not run_command("grep -q 'pam_tally2.so' /etc/pam.d/common-auth", exit_on_fail=False):
        run_command("echo 'auth required pam_tally2.so deny=5 unlock_time=1800' >> /etc/pam.d/common-auth")

def secure_ports():
    """Check open ports and close unauthorized ones."""
    print("Checking and securing open ports...")
    open_ports = run_command("ss -ln")
    with open("/root/open_ports.txt", "w") as f:
        f.write(open_ports)
    ports_to_close = [line for line in open_ports.splitlines() if not "127.0.0.1" in line]
    for port in ports_to_close:
        port_num = port.split()[4].split(":")[-1]
        print(f"Closing port {port_num}...")
        process = run_command(f"lsof -i :{port_num} | awk '{{print $1}}' | tail -n 1")
        location = run_command(f"whereis {process.strip()} | awk '{{print $2}}'")
        package = run_command(f"dpkg -S {location.strip()} | cut -d: -f1")
        run_command(f"apt-get purge -y {package.strip()}")
        run_command("ss -l")

def enable_firewall():
    """Enable the UFW firewall."""
    print("Enabling firewall...")
    run_command("ufw enable")

def enable_syn_cookies():
    """Enable SYN cookies protection."""
    print("Enabling SYN cookies protection...")
    run_command("sysctl -w net.ipv4.tcp_syncookies=1")

def disable_ipv6():
    """Disable IPv6 (optional)."""
    print("Disabling IPv6...")
    run_command("echo 'net.ipv6.conf.all.disable_ipv6 = 1' >> /etc/sysctl.conf")
    run_command("sysctl -p")

def disable_ip_forwarding():
    """Disable IP forwarding."""
    print("Disabling IP forwarding...")
    run_command("echo '0' > /proc/sys/net/ipv4/ip_forward")

def prevent_ip_spoofing():
    """Prevent IP spoofing."""
    print("Preventing IP spoofing...")
    run_command("echo 'nospoof on' >> /etc/host.conf")

def update_system():
    """Run system updates and security patches."""
    print("Updating system...")
    run_command("apt-get update")
    run_command("apt-get upgrade -y")

def check_for_hacking_tools():
    """Check for hacking tools or suspicious packages."""
    print("Checking for hacking tools...")
    hacking_tools = run_command("dpkg --get-selections | grep -E 'john|hydra|medusa|ophcrack'")
    if hacking_tools:
        with open("/root/suspicious_tools.txt", "w") as f:
            f.write(hacking_tools)

def check_service_status():
    """Check the status of all services."""
    print("Checking service status...")
    services = run_command("service --status-all")
    with open("/root/service_status.txt", "w") as f:
        f.write(services)

# Main script execution
if __name__ == "__main__":
    secure_root_login()
    disable_guest_user()
    check_uid_0_users()
    enforce_password_policy()
    secure_ports()
    enable_firewall()
    enable_syn_cookies()
    disable_ipv6()
    disable_ip_forwarding()
    prevent_ip_spoofing()
    update_system()
    check_for_hacking_tools()
    check_service_status()
    print("Linux hardening completed successfully.")
