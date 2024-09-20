import subprocess

def lightdm_configure():
    # Backup the LightDM configuration file
    try:
        subprocess.run(["sudo", "cp", "/etc/lightdm/lightdm.conf", "/etc/lightdm/lightdm.conf.bak"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error creating a backup: {e}")
        return

    # Modify the LightDM configuration file to disallow guest sessions
    with open("/etc/lightdm/lightdm.conf", "a") as f:
        f.write("\nallow-guest=false\n")

    # Restart LightDM to apply the changes
    try:
        subprocess.run(["sudo", "systemctl", "restart", "lightdm"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error restarting LightDM: {e}")

if __name__ == "__main__":
    lightdm_configure()
