import subprocess

def list_crontabs():
    # Check the status of the cron service
    try:
        subprocess.run(["systemctl", "is-active", "--quiet", "cron"])
        print("Cron service status: Running")
    except subprocess.CalledProcessError:
        print("Cron service status: Stopped")
        return

    # Get a list of users
    with open("/etc/passwd") as f:
        users = [line.split(":")[0] for line in f.readlines()]

    # List cron jobs for each user
    for user in users:
        print(f"Cron jobs for user {user}:")
        try:
            output = subprocess.check_output(["crontab", "-l", "-u", user], text=True)
            print(output)
        except subprocess.CalledProcessError:
            print("No cron jobs.")
