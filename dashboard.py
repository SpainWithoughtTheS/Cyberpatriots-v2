#!/usr/bin/env python3
import curses
import subprocess
import os

def get_scripts():
    return sorted([f for f in os.listdir('.') if f.endswith('.py') and f != 'dashboard.py'])

def run_script(script_name):
    try:
        subprocess.run(["python3", script_name])
    except Exception as e:
        input(f"Error running {script_name}: {e}\nPress Enter to continue...")

def safe_cmd(cmd, shell=False):
    try:
        return subprocess.check_output(cmd, shell=shell, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return None

def get_system_info():
    info = []

    # Uptime
    uptime = safe_cmd(["uptime", "-p"])
    info.append(f"Uptime: {uptime or 'N/A'}")

    # Load average
    loadavg = safe_cmd("cat /proc/loadavg", shell=True)
    if loadavg:
        la = loadavg.split()
        info.append(f"Load Avg (1/5/15 min): {la[0]}, {la[1]}, {la[2]}")
    else:
        info.append("Load Avg: N/A")

    # Memory usage
    meminfo = safe_cmd(["free", "-h"])
    if meminfo:
        mem_lines = meminfo.splitlines()
        info.append("Memory Usage:")
        info.extend(mem_lines[1:3])  # Mem and Swap lines
    else:
        info.append("Memory Usage: N/A")

    # Disk usage for root
    disk = safe_cmd(["df", "-h", "/"])
    if disk:
        disk_lines = disk.splitlines()
        info.append("Disk Usage (/):")
        info.append(disk_lines[1])
    else:
        info.append("Disk Usage: N/A")

    # Open listening ports (top 10)
    ports = safe_cmd(["ss", "-tuln"])
    if ports:
        ports_lines = ports.splitlines()
        info.append("Open Listening TCP/UDP Ports:")
        info.extend(ports_lines[:10])
        if len(ports_lines) > 10:
            info.append(f"... ({len(ports_lines)-10} more lines)")
    else:
        info.append("Ports: N/A")

    # Recent failed login attempts (last 10)
    failed_logins = safe_cmd("sudo tail -n 20 /var/log/auth.log | grep 'Failed password'", shell=True)
    info.append("Recent Failed Logins:")
    if failed_logins:
        info.extend(failed_logins.splitlines()[-10:])
    else:
        info.append("N/A or permission denied")

    # Currently logged in users
    users = safe_cmd("who", shell=True)
    info.append("Logged In Users:")
    if users:
        info.extend(users.splitlines())
    else:
        info.append("N/A")

    # UFW Firewall status
    ufw_status = safe_cmd("sudo ufw status verbose", shell=True)
    info.append("Firewall (UFW) Status:")
    if ufw_status:
        info.extend(ufw_status.splitlines())
    else:
        info.append("N/A or permission denied")

    # Top CPU consuming processes (top 5)
    top_cpu = safe_cmd("ps aux --sort=-%cpu | head -6", shell=True)
    info.append("Top CPU Processes:")
    if top_cpu:
        info.extend(top_cpu.splitlines())
    else:
        info.append("N/A")

    # Top Memory consuming processes (top 5)
    top_mem = safe_cmd("ps aux --sort=-%mem | head -6", shell=True)
    info.append("Top Memory Processes:")
    if top_mem:
        info.extend(top_mem.splitlines())
    else:
        info.append("N/A")

    # Kernel version
    kernel = safe_cmd(["uname", "-r"])
    info.append(f"Kernel Version: {kernel or 'N/A'}")

    # Last reboot time
    reboot = safe_cmd("who -b", shell=True)
    info.append(f"Last Reboot: {reboot or 'N/A'}")

    # Loaded kernel modules (first 10)
    lsmod = safe_cmd("lsmod | head -10", shell=True)
    info.append("Loaded Kernel Modules (top 10):")
    if lsmod:
        info.extend(lsmod.splitlines())
    else:
        info.append("N/A")

    # System temperature (requires lm-sensors)
    sensors = safe_cmd("sensors", shell=True)
    info.append("System Temperature:")
    if sensors:
        info.extend(sensors.splitlines()[:10])  
    else:
        info.append("N/A or lm-sensors not installed")

    return info

def dashboard(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
    highlight_color = curses.color_pair(1)

    scripts = get_scripts()
    current_row = 0
    mode = "scripts"  # or "system"

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        if mode == "scripts":
            stdscr.addstr(0, 2, "🛡️ CyberPatriot Script Dashboard - [Scripts]", curses.A_BOLD)
            stdscr.addstr(1, 2, "Use ↑/↓ to navigate, Enter to run, TAB to switch view, Q to quit")

            for idx, script in enumerate(scripts):
                y = idx + 3
                if y >= height - 1:
                    break
                if idx == current_row:
                    stdscr.attron(highlight_color)
                    stdscr.addstr(y, 4, script)
                    stdscr.attroff(highlight_color)
                else:
                    stdscr.addstr(y, 4, script)

        else:  # system info mode
            stdscr.addstr(0, 2, "🖥️ CyberPatriot System Info - [Press TAB to go back]", curses.A_BOLD)
            stdscr.addstr(1, 2, "Live system stats (may require sudo for full info)")
            info_lines = get_system_info()
            for idx, line in enumerate(info_lines):
                y = idx + 3
                if y >= height - 1:
                    break
                # Truncate line if too long
                if len(line) > width - 8:
                    line = line[:width - 11] + "..."
                stdscr.addstr(y, 4, line)

        stdscr.refresh()

        key = stdscr.getch()

        if key in [ord('q'), ord('Q')]:
            break
        elif key == curses.KEY_UP and mode == "scripts" and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and mode == "scripts" and current_row < len(scripts) - 1:
            current_row += 1
        elif key == ord('\t'):  # TAB key switches mode
            mode = "system" if mode == "scripts" else "scripts"
        elif key == ord('\n') and mode == "scripts":
            stdscr.clear()
            stdscr.addstr(0, 2, f"▶ Running {scripts[current_row]}... Press any key to return.")
            stdscr.refresh()
            curses.endwin()
            run_script(scripts[current_row])
            stdscr.getch()
            curses.curs_set(0)

if __name__ == "__main__":
    curses.wrapper(dashboard)
