import subprocess
import os

# Define critical applications to skip
CRITICAL_APPS = [
    "base-files",  # Essential base system files
    "bash",        # GNU Bourne-Again Shell
    "coreutils",   # Basic file, shell, and text utilities
    "dpkg",        # Debian package manager
    "systemd",     # System and service manager
    "gnupg",       # GNU privacy guard
    "apt",         # Package handling utility
    "libc6",       # GNU C Library
    "login",       # System login tools
    "util-linux",  # System utilities
    "daemon",      # Daemon processes manager
]

# File to save output
OUTPUT_FILE = os.path.expanduser("~/filtered_installed_apps.txt")


def get_installed_apps():
    """
    Get the list of installed applications using the 'dpkg-query' command.
    Returns a list of dictionaries containing package name, version, and description.
    """
    try:
        result = subprocess.run(
            ["dpkg-query", "-W", "-f=${binary:Package}\t${Version}\t${Description}\n"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        lines = result.stdout.splitlines()
        installed_apps = []
        for line in lines:
            parts = line.split("\t")
            if len(parts) == 3:
                installed_apps.append({
                    "name": parts[0],
                    "version": parts[1],
                    "description": parts[2]
                })
        return installed_apps
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving installed applications: {e.stderr}")
        return []


def is_critical_app(app_name):
    """
    Check if the given application is in the critical apps list.
    """
    return app_name in CRITICAL_APPS


def filter_installed_apps(apps):
    """
    Filter out critical applications and return the remaining apps.
    """
    return [app for app in apps if not is_critical_app(app["name"])]


def print_apps(apps):
    """
    Print the filtered applications in a human-readable format.
    """
    print(f"{'APPLICATION NAME':<30}{'VERSION':<20}{'DESCRIPTION'}")
    print("-" * 80)
    for app in apps:
        print(f"{app['name']:<30}{app['version']:<20}{app['description']}")


def save_apps_to_file(apps, filepath):
    """
    Save the filtered applications to a text file.
    """
    with open(filepath, "w") as f:
        f.write(f"{'APPLICATION NAME':<30}{'VERSION':<20}{'DESCRIPTION'}\n")
        f.write("-" * 80 + "\n")
        for app in apps:
            f.write(f"{app['name']:<30}{app['version']:<20}{app['description']}\n")
    print(f"Filtered applications saved to {filepath}")


def main():
    print("Gathering installed applications...")
    installed_apps = get_installed_apps()

    if not installed_apps:
        print("No installed applications found or an error occurred.")
        return

    print("Filtering non-critical applications...")
    filtered_apps = filter_installed_apps(installed_apps)

    if filtered_apps:
        print("\nFiltered Applications:")
        print_apps(filtered_apps)
        save_apps_to_file(filtered_apps, OUTPUT_FILE)
    else:
        print("No non-critical applications found.")


if __name__ == "__main__":
    main()
