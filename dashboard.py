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

def get_system_info():
    info = []
    # Uptime
    try:
        uptime = subprocess.check_output(["uptime", "-p"]).decode().strip()
        info.append(f"Uptime: {uptime}")
    except:
        info.append("Uptime: N/A")

    # CPU Load
    try:
        load = subprocess.check_output(["cat", "/proc/loadavg"]).decode().split()
        info.append(f"Load Average (1/5/15 min): {load[0]}, {load[1]}, {load[2]}")
    except:
        info.append("Load Average: N/A")

    # Memory Usage
    try:
        meminfo = subprocess.check_output(["free", "-h"]).decode().splitlines()
        info.append("Memory Usage:")
        info.extend(meminfo[1:3])  # Mem and Swap lines
    except:
        info.append("Memory Usage: N/A")

    # Disk Usage
    try:
        disk = subprocess.check_output(["df", "-h", "/"]).decode().splitlines()
        info.append("Disk Usage (/):")
        info.append(disk[1])
    except:
        info.append("Disk Usage: N/A")

    # Open Ports (Listening)
    try:
        ports = subprocess.check_output(["ss", "-tuln"]).decode().splitlines()
        info.append("Open TCP/UDP Listening Ports:")
        info.extend(ports[:10])  # show top 10 for brevity
        if len(ports) > 10:
            info.append(f"... ({len(ports)-10} more lines)")
    except:
        info.append("Ports: N/A")

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
                x = 4
                y = idx + 3
                if y >= height - 1:
                    break
                if idx == current_row:
                    stdscr.attron(highlight_color)
                    stdscr.addstr(y, x, script)
                    stdscr.attroff(highlight_color)
                else:
                    stdscr.addstr(y, x, script)

        else:  # system info mode
            stdscr.addstr(0, 2, "🖥️ CyberPatriot System Info - [Press TAB to go back]", curses.A_BOLD)
            stdscr.addstr(1, 2, "Live system stats (top of output only)")
            info_lines = get_system_info()
            for idx, line in enumerate(info_lines):
                y = idx + 3
                if y >= height - 1:
                    break
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
