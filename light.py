import subprocess
import os

def create_lightdm_config():
    # Check if the script is running as root
    if os.geteuid() != 0:
        print("This script must be run as root.")
        return

    # Define the new configuration content
    config_content = """
[Seat:*]
# Disable guest sessions for security
allow-guest=false

# Set the default user session (update to your desktop environment)
user-session=ubuntu

# Set greeter session (can be adjusted to your installed greeter)
greeter-session=lightdm-gtk-greeter

# X server configuration for better security (restrict remote access)
xserver-command=X -nolisten tcp

# Hide user list for better security (optional)
greeter-hide-users=true
"""

    # Create a backup of the existing configuration file
    try:
        if os.path.exists("/etc/lightdm/lightdm.conf"):
            subprocess.run(["cp", "/etc/lightdm/lightdm.conf", "/etc/lightdm/lightdm.conf.bak"], check=True)
            print("Backup of lightdm.conf created successfully.")
        else:
            print("No existing lightdm.conf found. Proceeding without a backup.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating a backup: {e}")
        return

    # Write the new configuration to the lightdm.conf file
    try:
        with open("/etc/lightdm/lightdm.conf", "w") as f:
            f.write(config_content)
        print("New lightdm.conf created successfully.")
    except Exception as e:
        print(f"Error writing lightdm.conf: {e}")
        return

    # Check the configuration for syntax errors
    try:
        result = subprocess.run(["lightdm", "--test-mode"], capture_output=True, text=True)
        if result.returncode != 0:
            print("Configuration test failed. Restoring the backup.")
            subprocess.run(["cp", "/etc/lightdm/lightdm.conf.bak", "/etc/lightdm/lightdm.conf"], check=True)
            print("Restored the backup configuration due to errors.")
            print(f"Error details:\n{result.stderr}")
            return
        else:
            print("Configuration test passed. Proceeding with applying changes.")
    except subprocess.CalledProcessError as e:
        print(f"Error testing the configuration: {e}")
        return

    # Reload LightDM to apply the changes safely without interrupting the current session
    try:
        subprocess.run(["systemctl", "reload", "lightdm"], check=True)
        print("LightDM configuration reloaded successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error reloading LightDM: {e}")
        return

    # Prompt the user before proceeding with a full restart
    restart = input("Configuration reload successful. Do you want to restart LightDM now to fully apply changes? (yes/no): ").strip().lower()
    if restart == 'yes':
        try:
            subprocess.run(["systemctl", "restart", "lightdm"], check=True)
            print("LightDM restarted successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error restarting LightDM: {e}")
            print("It is recommended to check the system status and revert to the backup if necessary.")

if __name__ == "__main__":
    create_lightdm_config()
