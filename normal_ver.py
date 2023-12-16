import os
import time

import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

from tkinter import messagebox


root = tk.Tk()
root.title("KHKT PROJECT")
root.geometry("600x500")

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
            hosts = file.readlines()
        return hosts
    except FileNotFoundError:
        messagebox.showerror('Error', 'Hosts file not found.')
        return []
def row_counter(row_num):
    for i in range(row_num):
        table.insert('', 'end', text=str(i+1), values=('', '', ''))
def update_table():
    ip_addresses = read_hosts_file()
    table.delete(*table.get_children())
    row_column=0
    for line in ip_addresses:
        items = line.split()
        if len(items) == 3:
            row_column=row_column+1
            ip_address, website, blocked = items
            table.insert('', 'end', text=row_column,values=[ip_address, website, blocked])
        elif len(items) == 2:
            row_column=row_column+1
            ip_address, website = items
            table.insert('', 'end',text=row_column, values=[ip_address, website, " "])

ip_youtube_filter=["216.239.38.119 www.youtube.com #YOUTUBE FILTER",
"216.239.38.119 m.youtube.com #YOUTUBE FILTER",
"216.239.38.119 youtubei.googleapis.com #YOUTUBE FILTER",
"216.239.38.119 youtube.googleapis.com #YOUTUBE FILTER",
"216.239.38.119 www.youtube-nocookie.com #YOUTUBE FILTER"]

ip_google_filter="216.239.38.120 www.google.com #GOOGLE FILTER"

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
    update_table()
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
    update_table()

def on_or_off(a,b):
    if b == "1":
        with open(filepath, 'r+') as file:
            content = file.read()
            file.seek(0)
            for e in range(len(a)):
                if a[e] in content:
                    return "1"
                else:
                    return "0"   
    if b == "o":
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

def block_ip(a):
    ip_address = a
    with open(filepath, 'r') as file:
        content=file.read()
        if ip_address not in content:
            if "." in ip_address:
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

def delete_ip(a,b):
    selected_items = b
    if a == "db":
        with open(filepath, 'r+') as file:
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                if len(line.split()) > 1 and line.split()[1] == selected_items:
                    continue
                file.write(line)
                print("DELETE",selected_items)
            file.truncate()  
    else:
        if len(selected_items) == 0:
            messagebox.showinfo('Info', 'Please select at least one IP address to unblock.')
            return
        for item in selected_items:
            if not table.exists(item):
                continue
            item_text = table.item(item)['values']
            print(item_text)
            ip_domain = str(item_text[0])
            ip_address = str(item_text[1])
            with open(filepath, 'r+') as file:
                lines = file.readlines()
                file.seek(0)
                for line in lines:
                    if len(line.split()) > 1 and line.split()[0] == ip_domain and line.split()[1] == ip_address:
                        continue
                    file.write(line)
                    print("DELETE",ip_address)
                file.truncate()
            messagebox.showinfo("Success", f"The IP address {ip_address} has been unblocked.")
    update_table()
                
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

#FRAME AND SETTING 
db=[]
def setting():
    frame = ttk.Frame(root,borderwidth=2, relief='solid')
    frame.place(relx=0.5, rely=0.5, relwidth=0.75, relheight=0.75, anchor='center')

    label = ttk.Label(frame , text="SETTING",bootstyle="warning")
    label.pack(pady=10,fill=tk.Y)

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
            root.protocol("WM_DELETE_WINDOW", root.iconify())
        # else:
        #     root.protocol("WM_DELETE_WINDOW", root.withdraw())
    # Create a checkbutton with a checkmark
    check_var = tk.IntVar(value=0)
    checkmark = ttk.Checkbutton(T_button_frame,variable=check_var,onvalue=1,offvalue=0,command=toggle_checkmark,bootstyle="square-toggle")
    checkmark.pack(padx=0)


    def get_db():
        global db
        dbtxt="database.txt"
        with open(dbtxt, 'r+') as file:
            for line in file:
                db.append(line.strip())
    get_db()
    def toggle_database():
        print(db)
        for i in range(len(db)):
            block_ip(db[i]+" #DATABASE")
        update_table()
    # Create a checkbutton with a checkmark
    change_password = ttk.Button(T_button_frame, text="USE DATABASE", command=toggle_database, bootstyle=ttk_theme)
    change_password.pack(side=tk.LEFT,padx=10)
    # Show information
    info = tk.messagebox.showinfo("Information", "KHKT PROJECT \n Project for educational purposes")


    # add a button to destroy the frame
    button_destroy = ttk.Button(frame, text="CLOSE", command=frame.destroy)
    button_destroy.pack(side=tk.BOTTOM,fill=tk.BOTH)

def exit_program(event):
    root.destroy()  # Close the Tkinter window

root.bind("<Escape>", exit_program)


# Top panel
#TopBAR
button_frame = ttk.Frame(root)
button_frame.pack( fill=tk.X,padx=10 , pady=10)


label = ttk.Label(button_frame , text="Enter IP Address:")
label.pack(side=tk.LEFT , padx=12)


entry = ttk.Entry(button_frame, font=("Helvetica", 12))
entry.pack(side=tk.LEFT, fill=tk.X,expand=True)


button_frame_inner = ttk.Frame(button_frame)
button_frame_inner.pack(side=tk.RIGHT)


block_button = ttk.Button(button_frame_inner, text="Block IP", command=lambda: block_ip(entry.get()), bootstyle=ttk_theme)
block_button.pack(side=tk.LEFT,padx=10)

delete_button = ttk.Button(button_frame_inner, text="Delete IP", command=lambda: delete_ip(0,table.selection()) ,bootstyle=ttk_theme)
delete_button.pack(side=tk.LEFT)


# Setting
setting_button = ttk.Button(button_frame_inner, text="S", command=setting , bootstyle=ttk_theme)
setting_button.pack(side=tk.LEFT,padx=10)


# # Time Selection
# time_frame = ttk.LabelFrame(root)
# time_frame.pack(fill=tk.X,padx=10 , pady=10)

# hour_var = tk.StringVar(root)
# hour_combobox = ttk.Combobox(root, textvariable=hour_var, values=[str(i).zfill(2) for i in range(24)], width=3)
# hour_combobox.current(0)
# hour_combobox.pack(side=tk.LEFT)

# minute_var = tk.StringVar(root)
# minute_combobox = ttk.Combobox(root, textvariable=minute_var, values=[str(i).zfill(2) for i in range(60)], width=3)
# minute_combobox.current(0)
# minute_combobox.pack()
# CREATE RADIO
var = tk.StringVar(value=on_or_off(ip_google_filter,"o"))

var2 = tk.StringVar(value=on_or_off(ip_youtube_filter,"o"))

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


table_frame = ttk.Frame(root)
table_frame.pack(fill=tk.BOTH, expand=True)

table_columns = ('IP', 'Website', 'Description')
table = ttk.Treeview(table_frame, columns=table_columns ,)

# Set the column widths
table.column('#0', width=25)
table.column('IP', width=50)
table.column('Website', width=100)
table.column('Description', width=100)
# Create the table headings
table.heading('#0', text='No.')
table.heading('IP', text='IP')
table.heading('Website', text='Website')
table.heading('Description', text='Description')

table.pack(fill=tk.BOTH, expand=True,pady=10,padx=16)

table.config(height=15)

update_table()



# Password frame
# password_frame = tk.Frame(root)
# password_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

# password_label = tk.Label(password_frame, text="Enter password: ")
# password_label.pack()

# password_entry = tk.Entry(password_frame, show="@")
# password_entry.pack()

# submit_button = tk.Button(password_frame, text="Submit", command=check_password)
# submit_button.pack(pady=10)

# PURPOSE
text_conner = tk.Label(root, text="project for educational purposes")
text_conner.place(anchor="sw", relx=0, rely=1)

root.mainloop()







