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

# Function to get installed packages from dpkg
def get_installed_packages():
    try:
        result = subprocess.run(
            ['dpkg', '--get-selections'], 
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        if result.returncode == 0:
            installed_packages = set(line.split()[0] for line in result.stdout.splitlines())
            return installed_packages
        else:
            print(f"Error: {result.stderr}")
            return set()
    except Exception as e:
        print(f"Error retrieving installed packages: {e}")
        return set()

# Get the list of installed packages
installed_packages = get_installed_packages()

# Loop through each package and check if it's installed
for package in packages:
    if package in installed_packages:
        print(f"{package} is installed")
    else:
        # print(f"{package} is not installed")
        pass
