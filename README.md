# Multithreaded TCP Port Scanner 🔍

A Python desktop utility designed for NOC and SOC teams to identify exposed Layer 4 TCP services across network hosts.

**Features:**
* Scans high-priority service ports (SSH, HTTP, HTTPS, RDP, DNS, FTP, etc.).
* Resolves domain hostnames to IPv4 addresses dynamically using `socket.gethostbyname`.
* Employs Python's `threading` library to prevent UI freezing during socket connection timeouts.
* Features a terminal-styled Tkinter GUI for real-time connection status reporting.

*Built as Day 4 of a 30-Day Network Engineering & Security portfolio streak.*
