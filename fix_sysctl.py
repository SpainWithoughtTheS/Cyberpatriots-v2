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
            print(f"An error occurred while setting {key}: {e}")

# Function to ensure settings are in sysctl.conf
def ensure_sysctl_in_conf(settings, path):
    try:
        # Read current settings
        with open(path, 'r') as file:
            lines = file.readlines()
        
        with open(path, 'w') as file:
            for key, value in settings.items():
                line = f"{key} = {value}\n"
                # Check if the setting already exists and update it
                if any(line.strip().startswith(key) for line in lines):
                    print(f"Updating {key} in {path}.")
                    # Remove any existing line that starts with this key
                    lines = [line for line in lines if not line.strip().startswith(key)]
                file.write(line)
            # Write the remaining lines back to the file
            file.writelines(lines)
            print(f"Added to {path}: {line.strip()}")
    except PermissionError:
        print("Permission denied. Please run the script with sudo.")
    except FileNotFoundError:
        print(f"{path} not found. Please check the path.")
    except Exception as e:
        print(f"An error occurred while writing to {path}: {e}")

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
