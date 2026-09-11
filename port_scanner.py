import socket
import threading
import tkinter as tk
from tkinter import ttk, messagebox

# Common ports monitored in NOC / SOC environments
TARGET_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3389: "RDP",
    8080: "HTTP-Proxy"
}

def scan_target(target_ip):
    text_output.config(state=tk.NORMAL)
    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, f"[*] Resolving and initiating scan on: {target_ip}\n")
    text_output.insert(tk.END, "-" * 50 + "\n")
    
    try:
        resolved_ip = socket.gethostbyname(target_ip)
        text_output.insert(tk.END, f"[*] Target IP resolved: {resolved_ip}\n\n")
    except socket.gaierror:
        text_output.insert(tk.END, f"[!] Host resolution error: Unable to resolve '{target_ip}'\n")
        text_output.config(state=tk.DISABLED)
        btn_scan.config(state=tk.NORMAL)
        lbl_status.config(text="Resolution Failed", fg="#c0392b")
        return

    open_ports = 0

    for port, service in TARGET_PORTS.items():
        # AF_INET = IPv4, SOCK_STREAM = TCP
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.7)  # Prevents long hangs on filtered ports
        result = s.connect_ex((resolved_ip, port))
        
        if result == 0:
            open_ports += 1
            text_output.insert(tk.END, f"[OPEN]  Port {port:<5} | Service: {service}\n")
        s.close()

    text_output.insert(tk.END, "-" * 50 + "\n")
    text_output.insert(tk.END, f"[*] Scan finished. {open_ports} open port(s) detected.\n")
    text_output.config(state=tk.DISABLED)
    btn_scan.config(state=tk.NORMAL)
    lbl_status.config(text=f"Completed ({open_ports} open)", fg="#27ae60")

def start_scan_thread():
    target_ip = entry_host.get().strip()
    if not target_ip:
        messagebox.showerror("Input Error", "Please enter a valid IP address or domain name.")
        return

    lbl_status.config(text="Scanning in progress...", fg="#e67e22")
    btn_scan.config(state=tk.DISABLED)

    # Execute socket operations on a background thread so the GUI remains responsive
    scan_thread = threading.Thread(target=scan_target, args=(target_ip,), daemon=True)
    scan_thread.start()

# --- Tkinter GUI Layout ---
root = tk.Tk()
root.title("NOC Toolkit - TCP Port Scanner")
root.geometry("520x460")
root.resizable(False, False)

frame = ttk.Frame(root, padding="15")
frame.pack(fill=tk.BOTH, expand=True)

# Top Bar / Inputs
lbl_title = tk.Label(frame, text="TCP Port & Service Scanner", font=("Helvetica", 13, "bold"))
lbl_title.pack(anchor="w", pady=(0, 10))

input_frame = ttk.Frame(frame)
input_frame.pack(fill=tk.X, pady=(0, 10))

lbl_host = tk.Label(input_frame, text="Target IP / Hostname:", font=("Helvetica", 10))
lbl_host.pack(side=tk.LEFT, padx=(0, 8))

entry_host = ttk.Entry(input_frame, width=25, font=("Helvetica", 10))
entry_host.pack(side=tk.LEFT, padx=(0, 8))
entry_host.insert(0, "scanme.nmap.org")

btn_scan = tk.Button(input_frame, text="Start Scan", command=start_scan_thread, bg="#2c3e50", fg="white", font=("Helvetica", 9, "bold"))
btn_scan.pack(side=tk.LEFT)

lbl_status = tk.Label(frame, text="Ready", font=("Helvetica", 9, "italic"), fg="#555")
lbl_status.pack(anchor="w", pady=(0, 5))

# Output Console Display
text_frame = tk.Frame(frame)
text_frame.pack(fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(text_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_output = tk.Text(text_frame, font=("Consolas", 9), bg="#1e1e1e", fg="#00ff00", yscrollcommand=scrollbar.set)
text_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
text_output.config(state=tk.DISABLED)
scrollbar.config(command=text_output.yview)

root.mainloop()