import subprocess

# List of packages to check
packages = [
    'nmap', 'metasploit-framework', 'burpsuite', 'john', 'hydra', 'sqlmap', 
    'wireshark', 'aircrack-ng', 'nikto', 'gobuster', 'dirb', 'hashcat', 'wpscan', 
    'enum4linux', 'netcat', 'openvpn', 'ophcrack', 'binwalk', 'radare2', 'masscan', 
    'snort', 'maltego', 'cewl', 'recon-ng', 'theharvester', 'dnsrecon', 'beef-xss', 
    'cisco-torch', 'etherape', 'yersinia', 'zaproxy', 'kismet', 'hping3', 'armitage', 
    'netsniff-ng', 'cuckoo', 'volatility', 'mimikatz', 'setoolkit', 'msfpc', 'uniscan', 
    'veil', 'wifite', 'responder', 'empire', 'mitmproxy', 'patator', 'medusa', 'fcrackzip', 
    'foremost', 'sleuthkit', 'autopsy', 'chntpw', 'flasm', 'macchanger', 'truecrack', 
    'tcpflow', 'tcpreplay', 'tcpdump', 'sslyze', 'powersploit', 'reaver', 'pixiewps', 
    'photon', 'lynis', 'joomscan', 'ettercap', 'sslstrip', 'slowhttptest', 'skipfish', 
    'seclists', 'pyrit', 'proxychains', 'proxychains-ng', 'vsftpd', 'samba', 'apache', 
    'nginx', 'pop3', 'smtp', 'squid'
]

# Function to check if a package is installed
def check_package_installed(package):
    try:
        result = subprocess.run(
            ['dpkg', '-l', package], 
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        # If package is found, return True
        return result.returncode == 0
    except Exception as e:
        print(f"Error checking package {package}: {e}")
        return False

# Loop through each package and check if it's installed
for package in packages:
    if check_package_installed(package):
        print(f"{package} is installed")
