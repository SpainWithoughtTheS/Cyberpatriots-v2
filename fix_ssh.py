import subprocess
import os

# Define the SSH settings to be set
ssh_settings = {
    "Protocol": "2",
    "PermitRootLogin": "no",
    "X11Forwarding": "no",
    "PermitEmptyPasswords": "no",
    "UsePAM": "yes",
    "PasswordAuthentication": "no"
}

# Path to sshd_config
ssh_config_path = '/etc/ssh/sshd_config'

# Function to set SSH parameters
def set_ssh_parameters(settings):
    try:
        # Read current settings
        with open(ssh_config_path, 'r') as file:
            lines = file.readlines()
        
        with open(ssh_config_path, 'w') as file:
            for key, value in settings.items():
                line = f"{key} {value}\n"
                # Check if the setting already exists and update it
                if any(line.strip().startswith(key) for line in lines):
                    print(f"Updating {key} in {ssh_config_path}.")
                    # Remove any existing line that starts with this key
                    lines = [line for line in lines if not line.strip().startswith(key)]
                file.write(line)
            # Write the remaining lines back to the file
            file.writelines(lines)
            print(f"Added/Updated settings in {ssh_config_path}.")
    except PermissionError:
        print("Permission denied. Please run the script with sudo.")
    except FileNotFoundError:
        print(f"{ssh_config_path} not found. Please check the path.")
    except Exception as e:
        print(f"An error occurred while writing to {ssh_config_path}: {e}")

# Function to restart SSH service
def restart_ssh_service():
    try:
        subprocess.run(["sudo", "systemctl", "restart", "ssh"], check=True)
        print("SSH service restarted.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to restart SSH service: {e}")

# Run the functions
set_ssh_parameters(ssh_settings)
restart_ssh_service()
