import subprocess

def change_all_passwords(new_password):
    try:
        # Get all system users
        with open('/etc/passwd', 'r') as passwd_file:
            users = [line.split(':')[0] for line in passwd_file if int(line.split(':')[2]) >= 1000]

        for user in users:
            result = subprocess.run(['sudo', 'chpasswd'], input=f"{user}:{new_password}", text=True)
            if result.returncode == 0:
                print(f"Password changed for user: {user}")
            else:
                print(f"Failed to change password for user: {user}")

    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    # Set all users' password to !password123Aa
    change_all_passwords("!password123Aa")
