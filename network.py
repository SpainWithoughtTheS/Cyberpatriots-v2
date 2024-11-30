#!/usr/bin/env python3

import os
import subprocess
import sys

# Ensure the script is run as root
if os.geteuid() != 0:
    print("This script must be run as root. Use sudo to execute it.")
    sys.exit(1)

# List of known suspicious ports
SUSPICIOUS_PORTS = [23, 31337, 6667, 12345, 54321]  # Example: Telnet, IRC, backdoors, etc.

# Function to check for open ports and network connections
def scan_open_ports():
    """Scan and display open ports and network connections."""
    print("\nScanning open ports and network connections...\n")
    
    # Prefer `ss` if available, fallback to `netstat`
    try:
        result = subprocess.run(["ss", "-tuln"], capture_output=True, text=True, check=True)
        print(result.stdout)
        return result.stdout.splitlines()
    except FileNotFoundError:
        print("`ss` not found. Falling back to `netstat`...")
        result = subprocess.run(["netstat", "-tuln"], capture_output=True, text=True, check=True)
        print(result.stdout)
        return result.stdout.splitlines()

# Function to parse open ports from the scan results
def parse_ports(lines):
    """Extract open ports and associated information."""
    open_ports = []
    for line in lines:
        if "LISTEN" in line or "ESTABLISHED" in line:
            parts = line.split()
            if len(parts) >= 4:
                protocol = parts[0]
                local_address = parts[3]
                port = int(local_address.split(":")[-1]) if ":" in local_address else None
                open_ports.append((protocol, local_address, port))
    return open_ports

# Function to process suspicious ports
def process_port(protocol, address, port):
    """Ask user if they want to close a suspicious port."""
    print(f"\nSuspicious port detected: {port} ({protocol} - {address})")
    action = input("Do you want to close this port? (y/n): ").strip().lower()
    if action == 'y':
        close_port(port)
    else:
        print(f"Port {port} left open.")

# Function to close a port
def close_port(port):
    """Attempt to close a port by stopping its associated service."""
    print(f"Closing port: {port}")
    
    # Find and kill the process using the port
    try:
        result = subprocess.run(
            ["fuser", f"{port}/tcp"],
            capture_output=True, text=True, check=True
        )
        process_ids = result.stdout.strip()
        if process_ids:
            print(f"Killing process(es) associated with port {port}: {process_ids}")
            subprocess.run(["kill", "-9"] + process_ids.split(), check=True)
            print(f"Port {port} closed successfully.")
        else:
            print(f"No process found using port {port}.")
    except subprocess.CalledProcessError:
        print(f"Unable to close port {port}. You may need to investigate manually.")

# Main audit function
def audit_network():
    """Audit the network and handle suspicious ports."""
    lines = scan_open_ports()
    open_ports = parse_ports(lines)
    
    for protocol, address, port in open_ports:
        if port in SUSPICIOUS_PORTS:
            process_port(protocol, address, port)
        else:
            print(f"Safe port detected: {port} ({protocol} - {address})")

# Menu for managing suspicious network activity
def main():
    """Main script menu."""
    while True:
        print("\nNetwork Audit Script")
        print("1. Scan and audit network")
        print("2. Add a suspicious port to watchlist")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            audit_network()
        elif choice == '2':
            try:
                port = int(input("Enter the port number to add to the watchlist: ").strip())
                if port not in SUSPICIOUS_PORTS:
                    SUSPICIOUS_PORTS.append(port)
                    print(f"Port {port} added to the watchlist.")
                else:
                    print(f"Port {port} is already in the watchlist.")
            except ValueError:
                print("Invalid port number. Please try again.")
        elif choice == '3':
            print("Exiting script. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
