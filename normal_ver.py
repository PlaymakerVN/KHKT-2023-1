import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


def detect_system():
    if os.name == 'nt':
        print("Windows")
        hosts_path = "C:\Windows\System32\drivers\etc\hosts"
        return hosts_path
    elif os.name == 'posix':
        print("Linux")
        hosts_path = "/etc/hosts"
        return hosts_path 

filepath = detect_system()
def read_hosts_file():
    try:
        with open(filepath, 'r') as file:
            lines = file.readlines()
            ip_addresses = [line.split()[1] for line in lines if len(line.split()) > 1 and line.split()[0] == '127.0.0.1']
            return ip_addresses
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while reading the hosts file: {str(e)}")

def update_table():
    ip_addresses = read_hosts_file()
    table.delete(*table.get_children())
    for ip_address in ip_addresses:
        table.insert('', 'end', values=(ip_address,))

def block_ip():
    ip_address = entry.get()
    if ip_address:
        try:
            with open(filepath, 'a') as file:
                file.write(f"\n127.0.0.1 {ip_address}")
            messagebox.showinfo("Success", f"The IP address {ip_address} has been blocked.")
            entry.delete(0, 'end')
            update_table()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while blocking the IP address: {str(e)}")
    else:
        messagebox.showwarning("Warning", "Please enter an IP address.")

def delete_ip():
    selected_item = table.selection()
    if selected_item:
        ip_address = table.item(selected_item)['values'][0]
        try:
            with open(filepath, 'r+') as file:
                lines = file.readlines()
                file.seek(0)
                for line in lines:
                    if len(line.split()) > 1 and line.split()[0] == '127.0.0.1' and line.split()[1] == ip_address:
                        continue
                    file.write(line)
                file.truncate()
            messagebox.showinfo("Success", f"The IP address {ip_address} has been unblocked.")
            update_table()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while deleting the IP address: {str(e)}")
    else:
        messagebox.showwarning("Warning", "Please select an IP address to delete.")

root = tk.Tk()
root.title("KHKT PROJECT")
root.geometry("400x400")

# Styling
style = ttk.Style(root)
style.theme_use("clam")
style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
style.configure("Treeview", font=("Helvetica", 12))
style.configure("TButton", font=("Helvetica", 12))

# IP Address Entry
label = tk.Label(root, text="Enter IP Address:")
label.pack()

entry = tk.Entry(root, font=("Helvetica", 12))
entry.pack()

# Button Frame
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

block_button = ttk.Button(button_frame, text="Block IP", command=block_ip)
block_button.pack(side=tk.LEFT, padx=5)

delete_button = ttk.Button(button_frame, text="Delete IP", command=delete_ip)
delete_button.pack(side=tk.LEFT)

# Table Frame
table_frame = tk.Frame(root)
table_frame.pack(pady=10)

table_columns = ("Blocked IP Address",)
table = ttk.Treeview(table_frame, columns=table_columns, show="headings")
table.heading("Blocked IP Address", text="Blocked IP Address")
table.pack()

# Update Table
update_table()

root.mainloop()







