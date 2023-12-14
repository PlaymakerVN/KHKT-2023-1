import tkinter as tk
from datetime import datetime, timedelta

blocked_ips = {}

def block_ip():
    ip = ip_entry.get()
    # Check if IP is already blocked
    if ip in blocked_ips:
        status_label.config(text=f"IP '{ip}' is already blocked")
        return
    
    # Set a default block period of 1 hour
    block_duration = datetime.now() + timedelta(hours=1)
    blocked_ips[ip] = block_duration
    status_label.config(text=f"IP '{ip}' blocked until {block_duration}")
    ip_entry.delete(0, tk.END)

def unblock_ip():
    ip = ip_entry.get()
    # Check if IP is blocked
    if ip not in blocked_ips:
        status_label.config(text=f"IP '{ip}' is not currently blocked")
        return
    
    del blocked_ips[ip]
    status_label.config(text=f"IP '{ip}' unblocked")
    ip_entry.delete(0, tk.END)

def check_blocked():
    ip = ip_entry.get()
    if ip in blocked_ips:
        block_duration = blocked_ips[ip]
        status_label.config(text=f"IP '{ip}' is blocked until {block_duration}")
    else:
        status_label.config(text=f"IP '{ip}' is not currently blocked")
    ip_entry.delete(0, tk.END)

window = tk.Tk()
window.title("IP Blocker")

ip_label = tk.Label(window, text="IP Address:")
ip_label.pack()

ip_entry = tk.Entry(window)
ip_entry.pack()

block_button = tk.Button(window, text="Block IP", command=block_ip)
block_button.pack()

unblock_button = tk.Button(window, text="Unblock IP", command=unblock_ip)
unblock_button.pack()

check_button = tk.Button(window, text="Check Blocked", command=check_blocked)
check_button.pack()

status_label = tk.Label(window, text="")
status_label.pack()

window.mainloop()