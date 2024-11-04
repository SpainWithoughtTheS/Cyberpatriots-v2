import subprocess
import os

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

# Path to sysctl.conf
sysctl_conf_path = '/etc/sysctl.conf'

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

# Function to ensure settings are in sysctl.conf
def ensure_sysctl_in_conf(settings, path):
    try:
        with open(path, 'a') as file:
            for key, value in settings.items():
                # Check if the setting already exists in the file
                file.seek(0)
                if f"{key} = {value}" not in file.read():
                    file.write(f"{key} = {value}\n")
                    print(f"Added to {path}: {key} = {value}")
                else:
                    print(f"Already present in {path}: {key} = {value}")
    except PermissionError:
        print("Permission denied. Please run the script with sudo.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to refresh sysctl settings
def refresh_sysctl():
    try:
        subprocess.run(["sudo", "sysctl", "-p"], check=True)
        print("Sysctl settings refreshed.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to refresh sysctl settings: {e}")

# Run the functions
set_sysctl_parameters(sysctl_settings)
ensure_sysctl_in_conf(sysctl_settings, sysctl_conf_path)
refresh_sysctl()
