import subprocess

# Define the sysctl settings to be set
sysctl_settings = {
    "net.ipv4.tcp_rfc1337": 1,
    "net.ipv4.tcp_syncookies": 1,
    "net.ipv4.conf.all.rp_filter": 1,
    "net.ipv4.conf.default.rp_filter": 1,
    "kernel.randomize_va_space": 2,
    "net.ipv4.conf.all.accept_source_route": 0,
    "net.ipv4.conf.default.accept_source_route": 0,
    "net.ipv4.conf.all.send_redirects": 0,
    "net.ipv4.conf.default.send_redirects": 0,
    "net.ipv4.conf.all.log_martians": 1,
    "kernel.exec-shield": 1
}

# Function to set sysctl parameters
def set_sysctl_parameters(settings):
    for key, value in settings.items():
        try:
            subprocess.run(["sudo", "sysctl", "-w", f"{key}={value}"], check=True)
            print(f"Set {key} = {value}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to set {key}: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

# Run the function
set_sysctl_parameters(sysctl_settings)
