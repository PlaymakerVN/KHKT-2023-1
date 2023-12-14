import os
import time

import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

from tkinter import messagebox


root = tk.Tk()
root.title("KHKT PROJECT")
root.geometry("550x400")

ttk_theme="superhero"
# Styling
style = Style(theme=ttk_theme)


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
print(filepath)

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
    with open(filepath, 'r') as file:
        content=file.read()
        if ip_address not in content:
            if "www." in ip_address:
                try:
                    print("ADD",ip_address)
                    with open(filepath, 'a') as file:
                        file.write(f"\n127.0.0.1 {ip_address}")
                    messagebox.showinfo("Success", f"The IP address {ip_address} has been blocked.")
                    entry.delete(0, 'end')
                    update_table()
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred while blocking the IP address: {str(e)}")
            else:
                messagebox.showerror("Error", f"Invalid IP, Form : www.website.com")
        elif ip_address in content:
            messagebox.showwarning("Warning", "IP address already blocked.")

def delete_ip():
    selected_item = table.selection()
    if selected_item:
        ip_address = str(table.item(selected_item)['values'][0])
        try:
            with open(filepath, 'r+') as file:
                lines = file.readlines()
                file.seek(0)
                print("DELETE",ip_address)
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

#FILTER

ip_youtube_filter=["216.239.38.119 www.youtube.com",
"216.239.38.119 m.youtube.com",
"216.239.38.119 youtubei.googleapis.com",
"216.239.38.119 youtube.googleapis.com",
"216.239.38.119 www.youtube-nocookie.com"]

ip_google_filter="216.239.38.120     www.google.com"

def handle_selection():
    selected_value = var.get()
    if selected_value == "on":
        with open(filepath, 'a') as file:
            print("FILTER GOOGLE : ON")
            file.write(f"\n"+ip_google_filter)
    else:
        with open(filepath, 'r+') as file:
            print("FILTER GOOGLE : OFF",)
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                if not ip_google_filter in line:
                    file.write(line)
            file.truncate()
def handle_selection2():
    selected_value = var2.get()
    if selected_value == "on":
        with open(filepath, 'a') as file:
            print("FILTER YOUTUBE : ON")
            for item in range(len(ip_youtube_filter)):
                file.write(f"\n"+ip_youtube_filter[item])
    else:
        with open(filepath, 'r+') as file:
            print("FILTER YOUTUBE : OFF",)

            lines = file.readlines()
            file.seek(0)
            for line in lines:
                if not any(site in line for site in ip_youtube_filter):
                    file.write(line)
            file.truncate()

def on_or_off(a):    
    if isinstance(a, list):
        with open(filepath, 'r+') as file:
            content = file.read()
            file.seek(0)
            for e in range(len(a)):
                if a[e] in content:
                    return "on"
                else:
                    return "off"
    elif isinstance(a, str):
        with open(filepath, 'r+') as file:
            content = file.read()
            if a in content:
                return "on"
            else:
                return "off"
                
#Function Password
def get_password():
    with open(filepath, 'r') as file:
        lines = file.readlines()
        password = [line.split()[1] for line in lines if len(line.split()) > 1 and line.split()[0] == 'passw']
    return str(password[0])

def get_pass():
    with open(filepath, 'r+') as file:
        content = file.read()
        if "passw" in content:
            return get_password()
        else:
            return "admin"

mkpass=get_pass()
print(mkpass)
def check_password():
    entered_password = str(password_entry.get())
    if entered_password == mkpass:
        password_frame.destroy()
        # Put your main program logic here
    else:
        messagebox.showerror("Error", "Incorrect password!")

def setting():
    frame = ttk.Frame(root)
    frame.place(relx=0.5, rely=0.5, relwidth=0.75, relheight=0.75, anchor='center')

    label = ttk.Label(frame , text="SETTING",bootstyle="warning")
    label.pack(padx=12,fill=tk.Y)

    P_button_frame = ttk.Frame(frame)
    P_button_frame.pack( fill=tk.X , pady=10,padx=10)

    label = ttk.Label(P_button_frame , text="PASSWORD CHANGE")
    label.pack(padx=12,side=tk.LEFT)

    password_change_entry = ttk.Entry(P_button_frame, font=("Helvetica", 12))
    password_change_entry.pack(side=tk.LEFT, fill=tk.X,expand=True)

    button_frame_inner = ttk.Frame(P_button_frame)
    button_frame_inner.pack(side=tk.RIGHT)

    def change_password_en():
        global mkpass
        if password_change_entry.get() == mkpass:
            print(password_change_entry.get())
            messagebox.showerror("Error", f"Not Current Password")
        elif password_change_entry.get() != mkpass and len(password_change_entry.get())>6:
            with open(filepath, 'r+') as file:
                lines = file.readlines()
                file.seek(0)
                print(password_change_entry.get())
                for line in lines:
                    if len(line.split()) > 1 and line.split()[0] == 'passw' and line.split()[1] == mkpass:
                        continue
                    file.write(line)
                file.truncate()
                file.write(f"\npassw {password_change_entry.get()}")
            mkpass= password_change_entry.get()
            messagebox.showinfo("Successful", f"Changed password to {password_change_entry.get()}")
        else:
            messagebox.showerror("Error", f"Password more than 6 letter")


    change_password = ttk.Button(P_button_frame, text="Apply", command=change_password_en, bootstyle=ttk_theme)
    change_password.pack(side=tk.LEFT,padx=10)

    T_button_frame = ttk.Frame(frame)
    T_button_frame.pack(fill=tk.X)

    label = ttk.Label(T_button_frame , text="Force running background")
    label.pack(side=tk.LEFT,padx=20)

    def toggle_checkmark():
        value = check_var.get()
        if value == 1:
            root.protocol("WM_DELETE_WINDOW", root.withdraw())
        else:
            root.protocol("WM_DELETE_WINDOW", root.iconify())
    # Create a checkbutton with a checkmark
    check_var = tk.IntVar(value=0)
    checkmark = ttk.Checkbutton(T_button_frame,variable=check_var,onvalue=1,offvalue=0,command=toggle_checkmark)
    checkmark.pack(padx=0)
    # add a button to destroy the frame
    button_destroy = ttk.Button(frame, text="CLOSE", command=frame.destroy)
    button_destroy.pack(side=tk.BOTTOM,fill=tk.BOTH,padx=10)

def on_closing():
    root.iconify()
    # root.withdraw()
# root.protocol("WM_DELETE_WINDOW", root.iconify())

# Top panel
button_frame = ttk.Frame(root)
button_frame.pack( fill=tk.X , pady=10,padx=10)


label = ttk.Label(button_frame , text="Enter IP Address:")
label.pack(side=tk.LEFT , padx=12)


entry = ttk.Entry(button_frame, font=("Helvetica", 12))
entry.pack(side=tk.LEFT, fill=tk.X,expand=True)


button_frame_inner = ttk.Frame(button_frame)
button_frame_inner.pack(side=tk.RIGHT)


block_button = ttk.Button(button_frame_inner, text="Block IP", command=block_ip , bootstyle=ttk_theme)
block_button.pack(side=tk.LEFT,padx=10)

delete_button = ttk.Button(button_frame_inner, text="Delete IP", command=delete_ip ,bootstyle=ttk_theme)
delete_button.pack(side=tk.LEFT)

# Setting
setting_button = ttk.Button(button_frame_inner, text="S", command=setting , bootstyle=ttk_theme)
setting_button.pack(side=tk.LEFT,padx=10)

# CREATE RADIO
var = tk.StringVar(value=on_or_off(ip_google_filter))

var2 = tk.StringVar(value=on_or_off(ip_youtube_filter))

# Create radio buttons
radio_frame = ttk.Frame(root, padding=10)
radio_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

head_text = ttk.Label(radio_frame, text="Google filter") 
head_text.pack()

radio_button1 = ttk.Radiobutton(radio_frame, text="On", variable=var, value="on", command=handle_selection)
radio_button1.pack()

radio_button2 = ttk.Radiobutton(radio_frame, text="Off", variable=var, value="off", command=handle_selection)
radio_button2.pack()

head_text = ttk.Label(radio_frame, text="Youtube filter") 
head_text.pack()

radio_button3 = ttk.Radiobutton(radio_frame, text="On", variable=var2, value="on", command=handle_selection2)
radio_button3.pack()

radio_button4 = ttk.Radiobutton(radio_frame, text="Off", variable=var2, value="off", command=handle_selection2)
radio_button4.pack()


# Create TABLE 

table_frame = tk.Frame(root, bd=1, relief="solid",)
table_frame.pack(fill=tk.BOTH, padx=10, pady=10 ,expand=True)

table_columns = ("Blocked IP Address",)
table = ttk.Treeview(table_frame, columns=table_columns, show="headings")
table.heading("Blocked IP Address", text="Blocked IP Address")
table.pack(fill=tk.BOTH, expand=True)

table.config(height=15) # Displaying 15 rows in the table

update_table()


# Password frame
# password_frame = tk.Frame(root)
# password_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

# password_label = tk.Label(password_frame, text="Enter password: ")
# password_label.pack()

# password_entry = tk.Entry(password_frame, show="*")
# password_entry.pack()

# submit_button = tk.Button(password_frame, text="Submit", command=check_password)
# submit_button.pack(pady=10)

root.mainloop()







