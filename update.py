import subprocess
import os
import sys

# Function to execute shell commands
def run_command(command, capture_output=False):
    try:
        result = subprocess.run(command, shell=True, text=True, check=True, capture_output=capture_output)
        return result.stdout.strip() if capture_output else None
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        sys.exit(1)

# Backup the current sources.list
def backup_sources_list():
    sources_file = "/etc/apt/sources.list"
    backup_file = "/etc/apt/sources.list.bak"
    if not os.path.exists(backup_file):
        print("Creating a backup of the current sources.list...")
        run_command(f"sudo cp {sources_file} {backup_file}")
        print(f"Backup created at {backup_file}")
    else:
        print("Backup already exists at /etc/apt/sources.list.bak")

# Display the current sources.list
def show_current_sources():
    print("\nCurrent /etc/apt/sources.list:")
    run_command("cat /etc/apt/sources.list")

# Update sources.list
def update_sources_list():
    new_sources = []
    print("\nEnter the new repository URLs, line by line. Type 'DONE' when finished:")
    while True:
        repo = input("Repository URL: ")
        if repo.upper() == "DONE":
            break
        new_sources.append(repo)
    
    if new_sources:
        print("\nUpdating sources.list with new repositories...")
        with open("/tmp/sources.list.new", "w") as temp_file:
            temp_file.write("\n".join(new_sources) + "\n")
        run_command("sudo mv /tmp/sources.list.new /etc/apt/sources.list")
        print("sources.list updated.")
    else:
        print("No new repositories provided. Keeping the current sources.list.")

# Update and upgrade the system
def update_and_upgrade(full_upgrade=False):
    print("\nUpdating package list...")
    run_command("sudo apt update")
    print("\nUpgrading the system...")
    run_command("sudo apt upgrade -y")
    if full_upgrade:
        print("\nPerforming a full upgrade...")
        run_command("sudo apt full-upgrade -y")
    print("\nCleaning up...")
    run_command("sudo apt autoremove -y")
    run_command("sudo apt clean")

# Main function
def main():
    print("=== Update System Using sources.list ===")
    backup_sources_list()
    show_current_sources()

    choice = input("\nDo you want to (1) keep the current repositories or (2) update them? Enter 1 or 2: ")
    if choice == "2":
        update_sources_list()
    else:
        print("\nKeeping the current sources.list.")
    
    full_upgrade = input("\nDo you want to perform a full upgrade (may remove old packages)? (y/n): ").lower() == "y"
    update_and_upgrade(full_upgrade=full_upgrade)

    print("\nSystem update completed.")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("Please run this script as root (use sudo).")
        sys.exit(1)
    main()
