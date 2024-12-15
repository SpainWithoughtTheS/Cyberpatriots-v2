#!/usr/bin/env python3

import os
import subprocess
import sys

# Ensure the script is run as root
if os.geteuid() != 0:
    print("This script must be run as root. Use sudo to execute it.")
    sys.exit(1)

# Blacklisted services to skip
BLACKLISTED_SERVICES = [
    "systemd-journald",  # Critical system service
    "network-manager",   # Networking service
]


def list_running_services():
    """List all currently running services."""
    print("\nListing all running services...\n")
    result = subprocess.run(
        ["systemctl", "list-units", "--type=service", "--state=running"],
        capture_output=True, text=True
    )
    print(result.stdout)

def disable_service(service_name):
    """Disable and stop a service."""
    print(f"Disabling service: {service_name}")
    subprocess.run(["systemctl", "disable", service_name, "--now"], check=False)
    print(f"Service {service_name} disabled and stopped.")

def delete_service(service_name):
    """Completely delete a service if the file exists."""
    service_file = f"/etc/systemd/system/{service_name}.service"
    if os.path.exists(service_file):
        print(f"Deleting service file: {service_file}")
        os.remove(service_file)
        subprocess.run(["systemctl", "daemon-reload"], check=False)
        print(f"Service {service_name} deleted.")
    else:
        print(f"No service file found for {service_name}, skipping deletion.")

def process_service(service_name):
    """Ask the user whether to disable or delete the service."""
    print(f"\nProcessing service: {service_name}")
    action = input("Do you want to (d)isable, (D)elete, or (s)kip this service? [d/D/s]: ").strip().lower()
    if action == 'd':
        disable_service(service_name)
    elif action == 'd'.upper():
        delete_service(service_name)
    else:
        print(f"Skipping service: {service_name}")

def process_blacklisted(service_name):
    """Check if a service is blacklisted."""
    return service_name in BLACKLISTED_SERVICES

def review_services():
    """Review unnecessary services and take action."""
    print("\nReviewing unnecessary services...\n")

    # Combine additional services with running services
    result = subprocess.run(
        ["systemctl", "list-units", "--type=service", "--state=running", "--no-pager", "--plain"],
        capture_output=True, text=True
    )
    running_services = [line.split()[0] for line in result.stdout.splitlines() if line]
    services_to_check = set(running_services + ADDITIONAL_SERVICES)

    for service in sorted(services_to_check):
        if process_blacklisted(service):
            print(f"Service {service} is blacklisted. Skipping...")
            continue
        process_service(service)

def add_to_blacklist():
    """Add a service to the blacklist."""
    service_name = input("Enter the service name to blacklist: ").strip()
    if service_name not in BLACKLISTED_SERVICES:
        BLACKLISTED_SERVICES.append(service_name)
        print(f"Service {service_name} added to blacklist.")
    else:
        print(f"Service {service_name} is already blacklisted.")

def main():
    """Main script function with menu."""
    while True:
        print("\nService Management Script")
        print("1. List running services")
        print("2. Review and manage services")
        print("3. Add a service to the blacklist")
        print("4. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            list_running_services()
        elif choice == '2':
            review_services()
        elif choice == '3':
            add_to_blacklist()
        elif choice == '4':
            print("Exiting script. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
