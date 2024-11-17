import os
import subprocess

def disable_ftp_write_commands():
    """
    Check if vsftpd is installed and disable write commands in the vsftpd configuration file.
    """
    try:
        # Check if vsftpd is installed
        result = subprocess.run(['dpkg', '-l', 'vsftpd'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print("FTP service (vsftpd) is not installed.")
            return
    except FileNotFoundError:
        print("dpkg command not found. Ensure you are using a Debian-based system.")
        return

    # Disable write commands in the vsftpd configuration file
    config_path = '/etc/vsftpd.conf'
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as file:
                config_lines = file.readlines()

            # Modify or add the following lines to disable write commands.
            new_config_lines = []
            for line in config_lines:
                if line.startswith('write_enable='):
                    new_config_lines.append('write_enable=NO\n')
                else:
                    new_config_lines.append(line)

            if 'write_enable=NO\n' not in new_config_lines:
                new_config_lines.append('write_enable=NO\n')

            with open(config_path, 'w') as file:
                file.writelines(new_config_lines)

            print("FTP write commands have been disabled.")
        except PermissionError:
            print("Permission denied: Run the script with elevated privileges.")
    else:
        print(f"Configuration file {config_path} not found.")

if __name__ == "__main__":
    disable_ftp_write_commands()
