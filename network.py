import subprocess


def list_suspicious_connections():
    # Define known safe ports and IPs
    safe_ports = {22, 80, 443, 53, 123}  # SSH, HTTP, HTTPS, DNS, NTP
    safe_ips = {"127.0.0.1", "0.0.0.0", "::1"}

    try:
        # Run the 'ss' command with sudo to get detailed connection info
        result = subprocess.run(
            ["sudo", "ss", "-tlnp"],
            capture_output=True,
            text=True,
            check=True
        )

        # Parse output line by line
        suspicious_connections = []
        for line in result.stdout.splitlines():
            if "LISTEN" in line:
                parts = line.split()

                # Extract local address, port, and process info
                local_address = parts[3]
                ip, port = local_address.rsplit(':', 1)
                port = int(port) if port.isdigit() else None

                process_info = parts[6] if len(parts) > 6 else "Unknown"

                # Skip safe connections
                if ip in safe_ips or port in safe_ports:
                    continue

                # Add to suspicious connections list
                suspicious_connections.append({
                    "ip": ip,
                    "port": port,
                    "process_info": process_info
                })

        # Display suspicious connections
        if suspicious_connections:
            print("Suspicious Connections Found:")
            for conn in suspicious_connections:
                print(f"IP: {conn['ip']}, Port: {conn['port']}, Process: {conn['process_info']}")
        else:
            print("No suspicious connections found.")

    except subprocess.CalledProcessError as e:
        print("Failed to run 'ss' command. Make sure you have sudo privileges.")
        print(e)


# Usage in main.py
if __name__ == "__main__":
    list_suspicious_connections()
