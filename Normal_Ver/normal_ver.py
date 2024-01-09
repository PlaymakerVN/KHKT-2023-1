import os
import time

from urllib.parse import urlsplit
import requests

from browser_history import browsers, generic, utils,core

import socket
import json
import re

from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from tkinter import filedialog
from tkinter import font
from tkinter import messagebox

import time
root = tk.Tk()
root.title("KHKT PROJECT : Weblock")
root.geometry("250x200")

ttk_theme="superhero"
# Styling
new_font = font.Font(family="Helvetica", size=30, weight="bold")

for widget in root.winfo_children():
    widget.configure(font=new_font)

style = Style(theme=ttk_theme)

current_os=""
filepath=""

ip_youtube_filter=["216.239.38.119 www.youtube.com #YOUTUBE FILTER",
"216.239.38.119 m.youtube.com #YOUTUBE FILTER",
"216.239.38.119 youtubei.googleapis.com #YOUTUBE FILTER",
"216.239.38.119 youtube.googleapis.com #YOUTUBE FILTER",
"216.239.38.119 www.youtube-nocookie.com #YOUTUBE FILTER"]
ip_bing_filter=["204.79.197.220 www.bing.com #Bing FILTER",
"204.79.197.220 bing.com #Bing FILTER",
"204.79.197.220 www2.bing.com #Bing FILTER",
"204.79.197.220 www3.bing.com #Bing FILTER"]
ip_google_filter="216.239.38.120 www.google.com #GOOGLE FILTER"
def get_local_ip():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    return IPAddr
def detect_system():
    global filepath
    global current_os
    if os.name == 'nt':
        current_os= "Windows"
        filepath = "C:/Windows/System32/drivers/etc/hosts"
    elif os.name == 'posix':
        current_os = "Linux"
        filepath = "/etc/hosts"
    print(filepath)
detect_system()
def create_file(file_name):
    try:
        with open(file_name, 'x') as file:
            print(f"File {file_name} created successfully.")
    except FileExistsError:
        print(f"File {file_name} already exists.")

# Now, let's call this function with the desired file name
create_file("database.txt")
def flush_dns():
    try:
        if current_os == "Windows" :
            os.system('ipconfig /flushdns')
        elif current_os == "Linux":
            os.system('sudo service network-manager restart')
        tk.messagebox.showinfo("Information", "DNS FLUSH")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while flush dns : {str(e)}")

def solve_url_his(input_url):
    if "https://" in input_url or "http://" in input_url:
        parsed_url = urlsplit(input_url)
        result = parsed_url.netloc
    else:
        result = input_url
    return result

full_url_history=[]
url_history=[]
time_history=[]
head_history=[]
def get_history():
    global history
    global full_url_history
    # SAVE HIS
    domain_connected = core.get_history()
    domain_connected.save("history_file", output_format="json")
    f = open('history_file')
    data = json.load(f)
    print("SAVED HISTORY BROWSERS")
    a=[]
    # FILTER HIS
    dataArray=data['history']
    for i in range(len(dataArray)):
        full_url_history.append((data['history'][i]['URL']))
        time_history.append(data['history'][i]['Timestamp'])
        url_history.append(solve_url_his(data['history'][i]['URL']))
        head_history.append(data['history'][i]['Title'])

def read_hosts_file():
    try:
        with open(filepath, 'r') as file:
            hosts = file.readlines()
        return hosts
    except FileNotFoundError:
        messagebox.showerror('Error', 'Hosts file not found.')
        return []


#Function Password
def get_password():
    with open(filepath, 'r') as file:
        lines = file.readlines()
        password = [line.split()[1] for line in lines if len(line.split()) > 1 and line.split()[0] == '#passw']
    return str(password[0])

def get_pass():
    with open(filepath, 'r+') as file:
        content = file.read()
        if "#passw" in content:
            return get_password()
        else:
            return "admin"

mkpass=get_pass()
print(mkpass)
def check_password():
    entered_password = str(password_entry.get())
    if entered_password == mkpass:
        password_frame.destroy()
        root.geometry("750x650")
    else:
        messagebox.showerror("Error", "Incorrect password!")
#UPDATE TABLE
website_blocked=[]
line_filehost=[]
def update_table():
    global website_blocked
    global line_filehost
    line_filehost=[]
    website_blocked=[]
    ip_addresses = read_hosts_file()
    table.delete(*table.get_children())
    row_column=0
    for line in ip_addresses:
        line_filehost.append(line)
        if not line.startswith("#"):
            items = line.split()
            if len(items) == 3:
                row_column=row_column+1
                ip_address, website, blocked = items
                website_blocked.append(website)
                table.insert('', 'end', text=row_column,values=[ip_address, website, blocked])
            elif len(items) == 2:
                row_column=row_column+1
                ip_address, website = items
                website_blocked.append(website)
                table.insert('', 'end',text=row_column, values=[ip_address, website, " "])
    search_var.set("")

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

def handle_selection3():
    selected_value = var3.get()
    if selected_value == "on":
        with open(filepath, 'a') as file:
            print("FILTER Bing : ON")
            for item in range(len(ip_bing_filter)):
                file.write(f"\n"+ip_bing_filter[item])
    else:
        with open(filepath, 'r+') as file:
            print("FILTER Bing : OFF",)

            lines = file.readlines()
            file.seek(0)
            for line in lines:
                if not any(site in line for site in ip_bing_filter):
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
error=0
error_name=""
def block_ip(a):
    global error

    ip_address = a
    print(ip_address)
    if re.match(r'\d+\.\d+\.\d+\.\d+', ip_address):
        with open(filepath, 'r') as file:
            content=file.read()
            if ip_address not in content:
                if "." in ip_address:
                    try:
                        print("ADD",ip_address)
                        with open(filepath, 'a') as file:
                            file.write(f"\n{ip_address}")
                        entry.delete(0, 'end')
                        update_table()
                        error=0
                    except Exception as e:
                        messagebox.showerror("Error", f"An error occurred while blocking the IP address: {str(e)}")
                        error_name="Error", f"ERROR {e}"
                        error=1
                else:
                    error_name= "Error", f"Invalid IP, Form : www.website.com"
                    error=1
            elif ip_address in content:
                error_name ="Warning", "IP address already blocked."
                error=1
        return "ok"
    else:
        with open(filepath, 'r') as file:
            content=file.read()
            if f"127.0.0.1 {ip_address.split()[0]}" not in content:
                if "." in ip_address:
                    try:
                        print("ADD",ip_address)
                        with open(filepath, 'a') as file:
                            file.write(f"\n127.0.0.1 {ip_address}")
                        entry.delete(0, 'end')
                        update_table()
                        error=0
                    except Exception as e:
                        messagebox.showerror("Error", f"An error occurred while blocking the IP address: {str(e)}")
                        error_name="Error", f"ERROR {e}"
                        error=1
                else:
                    error_name= "Error", f"Invalid IP, Form : www.website.com"
                    error=1
            elif ip_address in content:
                error_name ="Warning", "IP address already blocked."
                error=1
        return "ok"
    update_table()


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
                        print("DELETE",ip_address)
                        continue
                    file.write(line)
                file.truncate()
        messagebox.showinfo("Success", f"The IP address has been unblocked.")
    update_table()
                
#FRAME AND SETTING 
db=[]
check = 1


def get_server():
    global server_ip , server_id
    with open(filepath, 'r') as file:
        lines = file.readlines()
        server_ip = [line.split()[1] for line in lines if len(line.split()) > 1 and line.startswith("#serv")][0]
        server_id = int([line.split()[2] for line in lines if len(line.split()) > 1 and line.startswith("#serv")][0])

def server_conf():
    global server_ip
    with open(filepath, 'r+') as file:
        content = file.read()
        if "#serv" in content:
            try :
                get_server()
                return True
            except Exception:
                return False
        else:
            return False

server_id = 0
server_ip="None"
server=server_conf()

print(server)
print(server_ip)
print(server_id)

def toggle_database():
    print(db)
    for i in range(len(db)):
        if re.match(r'\d+\.\d+\.\d+\.\d+', db[i]):
            if "#" in db[i]:
                block_ip(db[i])
            else:
                block_ip(db[i] + " #DATABASE")
        else:
            if "#" in db[i]:
                block_ip(solve_url_his(db[i]))
            else:
                block_ip(solve_url_his(db[i])+" #DATABASE")
    update_table()
    messagebox.showinfo("Success", f"Database are using")

def show_db_online():
    def update_table_w():
        table.delete(*table.get_children())
        row_column=0
        for idb in range(len(db)):
            items = db[idb].split()
            if len(items) == 3:
                row_column=row_column+1
                ip_address, website, blocked = items
                table.insert('', 'end', text=row_column,values=[ip_address, solve_url_his(website), blocked])
            elif len(items) == 2:
                row_column=row_column+1
                ip_address, website = items
                table.insert('', 'end',text=row_column, values=[ip_address, solve_url_his(website), " "])
            elif len(items) == 1:
                row_column=row_column+1
                website = items
                table.insert('', 'end',text=row_column, values=["127.0.0.1", solve_url_his(website), " "])
    def select_block_ds():
        global error

        selected_items = table.selection()
        for item in selected_items:
            if not table.exists(item):
                continue
            item_text = table.item(item)['values'][1]
            print(item_text)
            block_ip(item_text)
        if error == 0:
            messagebox.showinfo("Success", f"Ip address website has been blocked")
        else:
            messagebox.showerror("Error"), f"{error_name}"
            error=0
        update_table_w()
    def del_db():
        global db

        selected_items = table.selection()
        for item in selected_items:
            if not table.exists(item):
                continue
            item_text = table.item(item)['values'][1]
            db = [item for item in db if item_text not in item]
            print(item_text)
        update_table_w()


    show_db_window = tk.Toplevel(root)
    show_db_window.title("Database Show")
    show_db_window.geometry("400x400")
    table_frame = ttk.Frame(show_db_window)
    table_frame.pack(fill=tk.BOTH, expand=True,padx=15 ,pady=15)

    table_columns = ('IP', 'Website', 'Description')
    table = ttk.Treeview(table_frame, columns=table_columns)

    # Set the column widths
    table.column('#0', width=18)
    table.column('IP', width=50)
    table.column('Website', width=100)
    table.column('Description', width=100)
    # Create the table headings
    table.heading('#0', text='No.')
    table.heading('IP', text='IP')
    table.heading('Website', text='Website')
    table.heading('Description', text='Description')

    table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create a vertical scrollbar
    v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL,bootstyle="round")
    v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure the table to use the scrollbar
    table.config(yscrollcommand=v_scrollbar.set)
    v_scrollbar.config(command=table.yview)

    table.config(height=15)

    block_button = ttk.Button(show_db_window, text="Block IP", command=select_block_ds, bootstyle=ttk_theme)
    block_button.pack(side=tk.LEFT,padx=15,pady=10)

    del_button = ttk.Button(show_db_window, text="Delete IP", command=del_db, bootstyle=ttk_theme)
    del_button.pack(side=tk.LEFT,pady=10)

    exit_button = ttk.Button(show_db_window, text="Block All IP", command=toggle_database,bootstyle=ttk_theme)
    exit_button.pack(side=tk.RIGHT,padx=15,pady=10)

    # refresh_button = ttk.Button(show_db_window, text="Refresh", command=update_table_w,bootstyle=ttk_theme)
    # refresh_button.pack(side=tk.RIGHT,padx=15,pady=10)
    update_table_w()
def setting():
    if current_language == 'english':
        # Show information
        info = tk.messagebox.showinfo("Information", f"KHKT PROJECT \n Current Os : {current_os} \n Hosts path: {filepath} \n Project for educational purposes")
        #Frame
        frame = ttk.Frame(root,borderwidth=2, relief='solid')
        frame.place(relx=0.5, rely=0.5, relwidth=0.75, relheight=0.75, anchor='center')

        label = ttk.Label(frame , text="SETTINGS",bootstyle="warning")
        label.pack(pady=10,fill=tk.Y)

        P_button_frame = ttk.Frame(frame)
        P_button_frame.pack(side=tk.TOP, fill=tk.X )

        label_pass = ttk.Labelframe(frame , text="Password Change")
        label_pass.pack(side=tk.TOP, fill=tk.X ,padx=10 )

        cur_button_frame = ttk.Frame(label_pass)
        cur_button_frame.pack(side=tk.TOP, fill=tk.X,pady=10,padx=10)

        label_cur = ttk.Label(cur_button_frame , text="New Password")
        label_cur.pack(side=tk.LEFT,padx=10)

        new_password_entry = ttk.Entry(cur_button_frame, font=("Helvetica", 12),show="✵")
        new_password_entry.pack(fill=tk.X,expand=True,padx=6)


        def change_password_en_two():
            global mkpass
            new_password = password_change_entry.get()
            if new_password != new_password_entry.get():
                messagebox.showerror("Error", f"Not Match")
            elif new_password == new_password_entry.get() == mkpass:
                messagebox.showerror("Error", f"Not Current Password")
            elif new_password == new_password_entry.get() != mkpass and len(new_password)>6:
                with open(filepath, 'r+') as file:
                    lines = file.readlines()
                    file.seek(0)
                    for line in lines:
                        if len(line.split()) > 1 and line.split()[0] == '#passw' and line.split()[1] == mkpass:
                            continue
                        file.write(line)
                    file.truncate()
                    file.write(f"\n#passw {new_password}")
                mkpass= new_password
                messagebox.showinfo("Successful", f"Changed password to {new_password}")
            else:
                messagebox.showerror("Error", f"Password less than 6 letter")


        new_button_frame = ttk.Frame(label_pass)
        new_button_frame.pack(side=tk.TOP, fill=tk.X , pady=10,padx=10)

        label_new = ttk.Label(new_button_frame , text="Retype")
        label_new.pack(side=tk.LEFT,padx=35)

        password_change_entry = ttk.Entry(new_button_frame, font=("Helvetica", 12),show="✵")
        password_change_entry.pack(side=tk.LEFT, fill=tk.X,expand=True)

        change_password_two = ttk.Button(new_button_frame, text="Apply", command=change_password_en_two, bootstyle=ttk_theme)
        change_password_two.pack(side=tk.RIGHT,padx=10)

        online_button_frame = ttk.Labelframe(frame,text="Connect to Server")
        online_button_frame.pack(fill=tk.X , pady=10,padx=10)

        ip_server_frame = ttk.Frame(online_button_frame)
        ip_server_frame.pack(fill=tk.X , pady=10,padx=10)

        label_new = ttk.Label(ip_server_frame , text="IP Server")
        label_new.pack(side=tk.LEFT,padx=35)

        show_ip = ttk.Label(online_button_frame, text="Current Server : "+str(server_ip)+" [Id]: "+str(server_id))
        show_ip.pack(side=tk.BOTTOM)

        ip_server_entry = ttk.Entry(ip_server_frame, font=("Helvetica", 12))
        ip_server_entry.pack(side=tk.LEFT, fill=tk.X,expand=True)

        ip_server_entry.insert(0, server_ip)

        def connect_server():
            global server
            global server_ip
            global server_id
            if server == False:
                if messagebox.askokcancel("Confirm", "Warning : All Ip Will Be Delete!"):
                    try:
                        r = requests.post(url=ip_server_entry.get(),data={"new_connect":f"{get_local_ip()}:{current_os}"})
                        server_id=r.text.split(':')[1]
                        server_ip=ip_server_entry.get()
                        show_ip.config(text="Current Server : "+server_ip+" [Id]: "+str(server_id))
                        r = requests.post(url=ip_server_entry.get(),data={f"{server_id}:hreplace":"his"})
                        server = True
                        for i in range(len(url_history)):
                            r = requests.post(url=server_ip,data={server_id+":his":full_url_history[i]})
                        ip_server_ap.config(text="Disconnect")
                    except Exception as e:
                        messagebox.showerror("Error", f"An error occurred while connect: {str(e)}")
            elif server == True:
                server = False
                server_ip="None"
                server_id=0
                show_ip.config(text="Current Server : "+server_ip+" [Id]: "+str(server_id))
                ip_server_ap.config(text="Connect")
                with open(filepath, 'r+') as file:
                    file.truncate()


        def ip_server_ap_text():
            if server == True:
                return "Disconnect"
            elif server == False:
                return "Connect"

        ip_server_ap = ttk.Button(ip_server_frame, text=ip_server_ap_text(), command=connect_server, bootstyle=ttk_theme)
        ip_server_ap.pack(side=tk.RIGHT,padx=10)

        T_button_frame = ttk.Frame(frame)
        T_button_frame.pack(fill=tk.X)

        label = ttk.Label(T_button_frame , text="Display history")
        label.pack(side=tk.LEFT,padx=20,pady=5)

        def toggle_checkmark():
            global check
            value = check_var.get()
            if value == 0:
                check = 0
                new_table_frame.pack_forget()
            else:
                check = 1
                new_table_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True,padx=16, pady=14)
                   
        check_var = tk.IntVar(value=check)
        checkmark = ttk.Checkbutton(T_button_frame,variable=check_var,onvalue=1,offvalue=0,command=toggle_checkmark,bootstyle="square-toggle")
        checkmark.pack(padx=0,pady=5,side=tk.LEFT)



        def get_db():
            global db
            db=[]
            dbtxt="database.txt"
            with open(dbtxt, 'r+') as file:
                for line in file:
                    db.append(line.strip())
        get_db()

        # add a button to destroy the frame
        button_destroy = ttk.Button(frame, text="CLOSE", command=frame.destroy)
        button_destroy.pack(side=tk.BOTTOM,fill=tk.BOTH)


        # Button Import Data

        database=ttk.Frame(frame)
        database.pack(pady=10,side=tk.BOTTOM)


        def export_database():
            file_path = filedialog.asksaveasfilename()
            if file_path:
                with open(file_path, 'w') as file:
                    for i in range(len(website_blocked)):
                        file.write(website_blocked[i]+"\n")
            tk.messagebox.showinfo("Information", "All export")

        database_ex = ttk.Button(database, text="Export Database", command=export_database, bootstyle=ttk_theme)
        database_ex.pack(side=tk.RIGHT)

        def import_database():
            global cur_db
            global db
            db=[]
            file_path = filedialog.askopenfilename()
            if file_path:
                show_database.config(text="Current database : "+file_path)
                with open(file_path, 'r') as file:
                    for line in file:
                        db.append(line.strip())
            tk.messagebox.showinfo("Information", "Database imported , Press Use Database to Apply It")
            update_table()

        database_op = ttk.Button(database, text="Import Database", command=import_database, bootstyle=ttk_theme)
        database_op.pack(padx=4,side=tk.RIGHT)

        # DISPLAY AND APPLY

        database_us_frame=ttk.Frame(frame)
        database_us_frame.pack(side=tk.BOTTOM)

        db_s = ttk.Button(database, text="Show Database", command=show_db_online, bootstyle=ttk_theme)
        db_s.pack(padx=4,side=tk.LEFT)

        database_off = ttk.Button(database, text="Use Database", command=toggle_database, bootstyle=ttk_theme)
        database_off.pack(side=tk.LEFT)
        #Get database Online

        db_on= ttk.Frame(frame)
        db_on.pack(pady=5,side=tk.BOTTOM)

        show_database = ttk.Label(db_on, text="Current database : Inprogramme") 
        show_database.pack(pady=2)

        label_db = ttk.Label(db_on , text="IP Get Database Online")
        label_db.pack(padx=12,side=tk.LEFT)

        url = "https://raw.githubusercontent.com/PlaymakerVN/KHKT-2023-1/main/database.txt"

        db_entry = ttk.Entry(db_on, font=("Helvetica", 12))
        db_entry.insert(0, url)
        db_entry.pack(side=tk.LEFT, fill=tk.X,expand=True)
        def get_db_online():
            url=db_entry.get()
            response = requests.get(url)
            if response.status_code == 200:
                global db
                db=[]
                file_content = response.text
                db=file_content.splitlines()
                show_database.config(text="Current database : Online Database")
                tk.messagebox.showinfo("Information", "Database downloaded , Press Use Database to Apply It")
            else:
                tk.messagebox.showerror("Error", f"Error: {response.status_code} \n An Ip Invalid Or Dead")
                print(f"Error: {response.status_code}")
        db_ap = ttk.Button(db_on, text="Get", command=get_db_online, bootstyle=ttk_theme)
        db_ap.pack(side=tk.LEFT,padx=10)
    else:
        # Show information
        info = tk.messagebox.showinfo("Information", f"KHKT PROJECT \n Current Os : {current_os} \n Hosts path: {filepath} \n Project for educational purposes")
        #Frame
        frame = ttk.Frame(root,borderwidth=2, relief='solid')
        frame.place(relx=0.5, rely=0.5, relwidth=0.75, relheight=0.75, anchor='center')

        label = ttk.Label(frame , text="CÀI ĐẶT",bootstyle="warning")
        label.pack(pady=10,fill=tk.Y)

        P_button_frame = ttk.Frame(frame)
        P_button_frame.pack(side=tk.TOP, fill=tk.X )

        label_pass = ttk.Labelframe(frame , text="Thay đổi mật khẩu")
        label_pass.pack(side=tk.TOP, fill=tk.X ,padx=10 )

        cur_button_frame = ttk.Frame(label_pass)
        cur_button_frame.pack(side=tk.TOP, fill=tk.X,pady=10,padx=10)

        label_cur = ttk.Label(cur_button_frame , text="Nhập mật khẩu mới")
        label_cur.pack(side=tk.LEFT,padx=10)

        new_password_entry = ttk.Entry(cur_button_frame, font=("Helvetica", 12),show="✵")
        new_password_entry.pack(fill=tk.X,expand=True,padx=6)


        def change_password_en_two():
            global mkpass
            new_password = password_change_entry.get()
            if new_password != new_password_entry.get():
                messagebox.showerror("Error", f"Not Match")
            elif new_password == new_password_entry.get() == mkpass:
                messagebox.showerror("Error", f"Not Current Password")
            elif new_password == new_password_entry.get() != mkpass and len(new_password)>6:
                with open(filepath, 'r+') as file:
                    lines = file.readlines()
                    file.seek(0)
                    for line in lines:
                        if len(line.split()) > 1 and line.split()[0] == '#passw' and line.split()[1] == mkpass:
                            continue
                        file.write(line)
                    file.truncate()
                    file.write(f"\n#passw {new_password}")
                mkpass= new_password
                messagebox.showinfo("Successful", f"Changed password to {new_password}")
            else:
                messagebox.showerror("Error", f"Password less than 6 letter")


        new_button_frame = ttk.Frame(label_pass)
        new_button_frame.pack(side=tk.TOP, fill=tk.X , pady=10,padx=10)

        label_new = ttk.Label(new_button_frame , text="Nhập lại mật khẩu")
        label_new.pack(side=tk.LEFT,padx=35)

        password_change_entry = ttk.Entry(new_button_frame, font=("Helvetica", 12),show="✵")
        password_change_entry.pack(side=tk.LEFT, fill=tk.X,expand=True)

        change_password_two = ttk.Button(new_button_frame, text="Áp dụng", command=change_password_en_two, bootstyle=ttk_theme)
        change_password_two.pack(side=tk.RIGHT,padx=10)

        online_button_frame = ttk.Labelframe(frame,text="Kết nối đến Server")
        online_button_frame.pack(fill=tk.X , pady=10,padx=10)

        ip_server_frame = ttk.Frame(online_button_frame)
        ip_server_frame.pack(fill=tk.X , pady=10,padx=10)

        label_new = ttk.Label(ip_server_frame , text="IP Server")
        label_new.pack(side=tk.LEFT,padx=35)

        show_ip = ttk.Label(online_button_frame, text="Current Server : "+str(server_ip)+" [Id]: "+str(server_id))
        show_ip.pack(side=tk.BOTTOM)

        ip_server_entry = ttk.Entry(ip_server_frame, font=("Helvetica", 12))
        ip_server_entry.pack(side=tk.LEFT, fill=tk.X,expand=True)

        ip_server_entry.insert(0, server_ip)

        def connect_server():
            global server
            global server_ip
            global server_id
            if server == False:
                if messagebox.askokcancel("Confirm", "Warning : All Ip Will Be Delete!"):
                    try:
                        r = requests.post(url=ip_server_entry.get(),data={"new_connect":f"{get_local_ip()}:{current_os}"})
                        server_id=r.text.split(':')[1]
                        server_ip=ip_server_entry.get()
                        show_ip.config(text="Server hiện tại : "+server_ip+" [Id]: "+str(server_id))
                        r = requests.post(url=ip_server_entry.get(),data={f"{server_id}:hreplace":"his"})
                        server = True
                        for i in range(len(url_history)):
                            r = requests.post(url=server_ip,data={server_id+":his":full_url_history[i]})
                        ip_server_ap.config(text="Ngắt kết nối")
                    except Exception as e:
                        messagebox.showerror("Error", f"An error occurred while connect: {str(e)}")
            elif server == True:
                server = False
                server_ip="None"
                server_id=0
                show_ip.config(text="Server hiện tại: "+server_ip+" [Id]: "+str(server_id))
                ip_server_ap.config(text="Kết nối")
                with open(filepath, 'r+') as file:
                    file.truncate()


        def ip_server_ap_text():
            if server == True:
                return "Ngắt kết nối"
            elif server == False:
                return "Kết nối"

        ip_server_ap = ttk.Button(ip_server_frame, text=ip_server_ap_text(), command=connect_server, bootstyle=ttk_theme)
        ip_server_ap.pack(side=tk.RIGHT,padx=10)

        T_button_frame = ttk.Frame(frame)
        T_button_frame.pack(fill=tk.X)

        label = ttk.Label(T_button_frame , text="Hiển thị lịch sử")
        label.pack(side=tk.LEFT,padx=20,pady=5)

        def toggle_checkmark():
            global check
            value = check_var.get()
            if value == 0:
                check = 0
                new_table_frame.pack_forget()
            else:
                check = 1
                new_table_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True,padx=16, pady=14)
                   
        check_var = tk.IntVar(value=check)
        checkmark = ttk.Checkbutton(T_button_frame,variable=check_var,onvalue=1,offvalue=0,command=toggle_checkmark,bootstyle="square-toggle")
        checkmark.pack(padx=0,pady=5,side=tk.LEFT)



        def get_db():
            global db
            db=[]
            dbtxt="database.txt"
            with open(dbtxt, 'r+') as file:
                for line in file:
                    db.append(line.strip())
        get_db()

        # add a button to destroy the frame
        button_destroy = ttk.Button(frame, text="Đóng", command=frame.destroy)
        button_destroy.pack(side=tk.BOTTOM,fill=tk.BOTH)


        # Button Import Data

        database=ttk.Frame(frame)
        database.pack(pady=10,side=tk.BOTTOM)


        def export_database():
            file_path = filedialog.asksaveasfilename()
            if file_path:
                with open(file_path, 'w') as file:
                    for i in range(len(website_blocked)):
                        file.write(website_blocked[i]+"\n")
            tk.messagebox.showinfo("Information", "All export")

        database_ex = ttk.Button(database, text="Nhập Database", command=export_database, bootstyle=ttk_theme)
        database_ex.pack(side=tk.RIGHT)

        def import_database():
            global cur_db
            global db
            db=[]
            file_path = filedialog.askopenfilename()
            if file_path:
                show_database.config(text="Database sử dụng: "+file_path)
                with open(file_path, 'r') as file:
                    for line in file:
                        db.append(line.strip())
            tk.messagebox.showinfo("Information", "Database imported , Press Use Database to Apply It")
            update_table()

        database_op = ttk.Button(database, text="Nhập Database", command=import_database, bootstyle=ttk_theme)
        database_op.pack(padx=4,side=tk.RIGHT)

        # DISPLAY AND APPLY

        database_us_frame=ttk.Frame(frame)
        database_us_frame.pack(side=tk.BOTTOM)

        db_s = ttk.Button(database, text="Xem Database", command=show_db_online, bootstyle=ttk_theme)
        db_s.pack(padx=4,side=tk.LEFT)

        database_off = ttk.Button(database, text="Dùng Database", command=toggle_database, bootstyle=ttk_theme)
        database_off.pack(side=tk.LEFT)
        #Get database Online

        db_on= ttk.Frame(frame)
        db_on.pack(pady=5,side=tk.BOTTOM)

        show_database = ttk.Label(db_on, text="Database sử dụng: Inprogramme") 
        show_database.pack(pady=2)

        label_db = ttk.Label(db_on , text="IP Lấy Database Online")
        label_db.pack(padx=12,side=tk.LEFT)

        url = "https://raw.githubusercontent.com/PlaymakerVN/KHKT-2023-1/main/database.txt"

        db_entry = ttk.Entry(db_on, font=("Helvetica", 12))
        db_entry.insert(0, url)
        db_entry.pack(side=tk.LEFT, fill=tk.X,expand=True)
        def get_db_online():
            url=db_entry.get()
            response = requests.get(url)
            if response.status_code == 200:
                global db
                db=[]
                file_content = response.text
                db=file_content.splitlines()
                show_database.config(text="Database sử dụng: Online Database")
                tk.messagebox.showinfo("Information", "Database downloaded , Press Use Database to Apply It")
            else:
                tk.messagebox.showerror("Error", f"Error: {response.status_code} \n An Ip Invalid Or Dead")
                print(f"Error: {response.status_code}")
        db_ap = ttk.Button(db_on, text="Lấy", command=get_db_online, bootstyle=ttk_theme)
        db_ap.pack(side=tk.LEFT,padx=10)


def exit_program(event):
    root.destroy()  # Close the Tkinter window

def get_ip():
    try:
        r = requests.post(url=server_ip,data={'get_blacklist':'blacklist'})
        getted_ip = r.text.split('\n')
    except Exception as e :
        getted_ip=0
        print(e)
    return getted_ip

def server_connect_start():
    if server == True:
        with open(filepath, 'r+') as file:
            file.truncate()
            a= get_ip()
            for i in range(len(a)):
                if a[i] != "":
                    file.write(f"\n127.0.0.1 {a[i]} #Server")
                    file.write(f"\n#passw {mkpass}")
                    file.write(f"\n#serv {server_ip} {server_id}")
            update_table()

def schedule_server_connect_start():
    server_connect_start()
    root.after(10000, schedule_server_connect_start) # Runs after 10 seconds (10000 milliseconds)

root.bind("<Escape>", exit_program)


# Top panel
#TopBAR
button_frame = ttk.Frame(root)
button_frame.pack( fill=tk.X,padx=10 , pady=10)


label_ip = ttk.Label(button_frame , text="Enter IP Address:")
label_ip.pack(side=tk.LEFT , padx=12)

# label_ip.pack(side=tk.LEFT , padx=18)

entry = ttk.Entry(button_frame, font=("Helvetica", 12))
entry.pack(side=tk.LEFT, fill=tk.X,expand=True)


button_frame_inner = ttk.Frame(button_frame)
button_frame_inner.pack(side=tk.RIGHT)

def button_blockip():
    global error
    if entry.get() == "":
        selected_items = new_table.selection()
        for item in selected_items:
            if not new_table.exists(item):
                continue
            item_text = new_table.item(item)['values'][0]
            print(item_text)
            block_ip(item_text)
        if error == 0:
            messagebox.showinfo("Success", f"Ip address website has been blocked")
        else:
            messagebox.showerror("Error"), f"{error_name}"
            error=0

    else:
        block_ip(solve_url_his(entry.get()))
        if error == 0:
            messagebox.showinfo("Success", f"An Ip address {entry.get()} has been blocked")
        else:
            messagebox.showerror("Error"), f"{error_name}"
            error=0


block_button = ttk.Button(button_frame_inner, text="Block IP", command=button_blockip, bootstyle=ttk_theme)
block_button.pack(side=tk.LEFT,padx=6)

delete_button = ttk.Button(button_frame_inner, text="Unblock IP", command=lambda: delete_ip(0,table.selection()) ,bootstyle=ttk_theme)
delete_button.pack(side=tk.LEFT)


# Setting
setting_button = ttk.Button(button_frame_inner, text="⚙", command=setting , bootstyle=ttk_theme)
setting_button.pack(side=tk.LEFT,padx=6)

language_dict = {
    'english': {
        'label_ip':'Enter IP Address:',
        'block_button': 'Block IP',
        'delete_button': 'Unblock IP',
        'setting_button': '⚙',
        'google_text':'Google Filter',
        'youtube_text':'Youtube Filter',
        'bing_text':'Bing Filter',
        'refresh_button':'Refresh',
        'reset_button':'Reset IP',
        'searcH_i':'Search:',
    },
    'vietnamese': {
        'label_ip':'Nhập địa chỉ IP: ',
        'block_button': 'Chặn IP',
        'delete_button': 'Bỏ Chặn IP',
        'setting_button': '⚙',
        'google_text':'Bộ lọc Google',
        'youtube_text':'Bộ lọc Youtube',
        'bing_text':'Bộ lọc Bing',
        'refresh_button':' Làm mới ',
        'reset_button':'Khôi phục',
        'searcH_i':'Tìm kiếm:',
        'clear_button':'Flush DNS',

    },
    # Add other languages here
}

def change_to_language():
    global current_language
    current_language = 'vietnamese' if current_language == 'english' else 'english'

    for button, text in language_dict[current_language].items():
        eval(f"{button}.config(text=text)")

    if current_language == 'english':
        change_language_button.config(image=english_flag)
        table.heading('#0', text='No.')
        table.heading('IP', text='IP')
        table.heading('Website', text='Website')
        table.heading('Description', text='Description')
        new_table.heading('#0', text='No.')
        new_table.heading('URL', text='URL')
        new_table.heading('Title', text='Title')
        new_table.heading('Time', text='Time')
    elif current_language == 'vietnamese':
        change_language_button.config(image=vietnamese_flag)
        table.heading('#0', text='STT')
        table.heading('IP', text='IP')
        table.heading('Website', text='Website')
        table.heading('Description', text='Ghi chú')
        new_table.heading('#0', text="STT")
        new_table.heading('URL', text="URL")
        new_table.heading('Title', text="Tiêu đề")
        new_table.heading('Time', text="Thời Gian")


vietnamese_flag = ImageTk.PhotoImage(Image.open("vietnamese_flag.png").resize((30, 15), Image.NEAREST))
english_flag = ImageTk.PhotoImage(Image.open("english_flag.png").resize((30, 15), Image.NEAREST))

current_language = 'english'


change_language_button = ttk.Button(button_frame_inner, image=english_flag, command=change_to_language)
change_language_button.pack(side=tk.LEFT)


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
def select_radio_button(button):
    for btn in [radio_button1, radio_button2]:
        if btn != button:
            btn.invoke() # Unselects the radio button
    button.invoke() # Selects the desired radio button

var = tk.StringVar(value=on_or_off(ip_google_filter,"o"))

var2 = tk.StringVar(value=on_or_off(ip_youtube_filter,"o"))

var3 = tk.StringVar(value=on_or_off(ip_bing_filter,"o"))

# Create radio buttons
left_bar =ttk.Frame(root)
left_bar.pack(side=tk.LEFT,fill=tk.Y,pady=10,padx=10)

radio_frame = ttk.Frame(left_bar)
radio_frame.pack(fill=tk.BOTH , expand=True)

google_text = ttk.Label(radio_frame, text="Google Filter") 
google_text.pack()

radio_button1 = ttk.Radiobutton(radio_frame, text="On", variable=var, value="on", command=handle_selection)
radio_button1.pack()

radio_button2 = ttk.Radiobutton(radio_frame, text="Off", variable=var, value="off", command=handle_selection)
radio_button2.pack()

youtube_text = ttk.Label(radio_frame, text="Youtube Filter") 
youtube_text.pack()

radio_button3 = ttk.Radiobutton(radio_frame, text="On", variable=var2, value="on", command=handle_selection2)
radio_button3.pack()

radio_button4 = ttk.Radiobutton(radio_frame, text="Off", variable=var2, value="off", command=handle_selection2)
radio_button4.pack()

bing_text = ttk.Label(radio_frame, text="Bing Filter") 
bing_text.pack()

radio_button5 = ttk.Radiobutton(radio_frame, text="On", variable=var3, value="on", command=handle_selection3)
radio_button5.pack()

radio_button6 = ttk.Radiobutton(radio_frame, text="Off", variable=var3, value="off", command=handle_selection3)
radio_button6.pack()

def change_theme():
    global Style
    theme_name = combo.get()
    style = Style(theme=theme_name)

combo = ttk.Combobox(radio_frame, values=style.theme_names(), width=8)
combo.current(style.theme_names().index(style.theme_use()))
combo.pack(side=tk.BOTTOM, pady=10)
combo.bind("<<ComboboxSelected>>", lambda event: change_theme())
combo.set('Theme')
combo.bind('<FocusIn>', lambda event: combo.set(combo.get()))
combo.bind('<FocusOut>', lambda event: combo.set('Theme'))

def clear_all_ip():
    if messagebox.askokcancel("Confirm", "Warning : All Ip Will Be Delete ! \n Are you sure you want to clear all IP?"):
        with open(filepath, 'r+') as file:
            file.truncate()
            file.write(f"\n#passw {mkpass}")
            if server == True:
                file.write(f"\n#serv {server_ip} {server_id}")
        tk.messagebox.showinfo("Information", "All ip was deleted")
        select_radio_button(radio_button1)
        select_radio_button(radio_button4)


reset_button = ttk.Button(radio_frame, text="  Reset IP  ", command=clear_all_ip, bootstyle=ttk_theme)
reset_button.pack(side=tk.BOTTOM,padx=10,fill=tk.X)

clear_button = ttk.Button(radio_frame, text="Flush Dns", command=flush_dns, bootstyle=ttk_theme)
clear_button.pack(side=tk.BOTTOM,pady=10,fill=tk.X,padx=10)

def update_his():
    a=0
    for i, item in enumerate(url_history, start=0):
        new_table.insert('', i, text=a+1, values=[url_history[a],head_history[a],time_history[a]])
        a=a+1

def refresh_all():
    global url_history
    global time_history
    global head_history

    url_history=[]
    time_history=[]
    head_history=[]

    update_his()
    get_history()
    messagebox.showinfo("Success", f"Ip Blocked Refresh !,\n {len(website_blocked)} website blocked has been loaded.\n History refresh ! \n {len(url_history)} url has been loaded.")

refresh_button = ttk.Button(radio_frame, text="  Refresh  ", command=refresh_all, bootstyle=ttk_theme)
refresh_button.pack(side=tk.BOTTOM,fill=tk.X,padx=10)

def open_docx_file(file_path):
    if os.name == 'nt': # Windows
        os.startfile(file_path)
    else: # MacOS and Linux
        subprocess.run(['open', file_path] if os.name == 'posix' else ['start', file_path])

# HELP BUTTON AND FRAME
def show_help(event):
    if current_language == 'english':
        open_docx_file('help_en.pdf')
    else:
        open_docx_file('help_vi.pdf')
# button_help_frame=tk.Frame(left_bar)
# button_help_frame.pack(side=tk.BOTTOM,fill=tk.X)

bottom_frame = ttk.Frame()
bottom_frame.pack(fill=tk.X,padx=10)

button_help = tk.Label(bottom_frame, text="❓", bg=root.cget('bg'))
button_help.config(font=("Arial", 15)) # adjust the font size according to your needs
button_help.pack(side=tk.RIGHT)
button_help.bind("<Button-1>", show_help)

searcH_i=ttk.Label(bottom_frame,text="Search:")
searcH_i.pack(side=tk.LEFT, pady=10)

search_var = tk.StringVar()

def on_search_entry_changed(*args):
    search_input = search_var.get()
    table.delete(*table.get_children())
    b=0
    for i, line in enumerate(line_filehost):
        if not line.startswith("#"):
            items = line.split()
            if len(items) == 3:
                ip_address, website, blocked = items
                b=b+1
            elif len(items) == 2:
                ip_address, website, blocked = items[0], items[1], " "
                b=b+1
            else:
                continue

            if search_input and search_input.lower() not in website.lower():
                continue

            table.insert('', 'end', text=b, values=[ip_address, website, blocked])


search_var.trace('w', on_search_entry_changed)
search_frame = ttk.Frame(bottom_frame)
search_frame.pack(fill=tk.X, padx=10, pady=10)
    
search_entry = ttk.Entry(search_frame, textvariable=search_var)
search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)


# Create TABLE 
def open_file():
    with open('database.txt', 'r') as file:
        content = file.read()
    # Insert content into new table
    new_table.insert('', 'end', values=(content,))

table_frame = ttk.Frame(root)
table_frame.pack(fill=tk.BOTH, expand=True,padx=10 ,pady=14)

table_columns = ('IP', 'Website', 'Description')
table = ttk.Treeview(table_frame, columns=table_columns)

# Set the column widths
table.column('#0', width=18)
table.column('IP', width=50)
table.column('Website', width=100)
table.column('Description', width=100)
# Create the table headings
table.heading('#0', text='No.')
table.heading('IP', text='IP')
table.heading('Website', text='Website')
table.heading('Description', text='Description')

table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a vertical scrollbar
v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL,bootstyle="round")
v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the table to use the scrollbar
table.config(yscrollcommand=v_scrollbar.set)
v_scrollbar.config(command=table.yview)

table.config(height=15)
# Create a new frame for the second table
new_table_frame = ttk.Frame(root)
new_table_frame.pack(fill=tk.BOTH, expand=True, padx=10,pady=15)

# Create a new table
new_table_columns = ('URL','Title','Time')
new_table = ttk.Treeview(new_table_frame, columns=new_table_columns)

# Set the column widths
new_table.column('#0', width=18)
new_table.column('URL', width=50)
new_table.column('Title', width=100)
new_table.column('Time', width=100)
# Create the table headings
new_table.heading('#0', text='No.')
new_table.heading('URL', text='URL')
new_table.heading('Title', text='Title')
new_table.heading('Time', text='Time')
new_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a vertical scrollbar for the new table
new_v_scrollbar = ttk.Scrollbar(new_table_frame, orient=tk.VERTICAL, bootstyle="round")
new_v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the new table to use the scrollbar
new_table.config(yscrollcommand=new_v_scrollbar.set)
new_v_scrollbar.config(command=new_table.yview)

new_table.config(height=8)

get_history()
update_his()

update_table()

# Password frame

password_frame = tk.Frame(root)
password_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

password_label = tk.Label(password_frame, text="LOGIN")
password_label.pack(padx=50)

password_label = tk.Label(password_frame, text="Enter password: ")
password_label.pack()

password_entry = tk.Entry(password_frame, show="✵")
password_entry.pack()

submit_button = ttk.Button(password_frame, text="Ok", command=check_password)
submit_button.pack(pady=10)

exit_button = tk.Label(password_frame, text="Press ESC to exit")
exit_button.pack(pady=10,side=tk.BOTTOM)

#PURPOSE
# text_conner = tk.Label(root, text="VER:⨻delta_test",font=("Helvetica",7))
# text_conner.pack(side=tk.LEFT,padx=10)

def on_close():
    result = messagebox.askokcancel("Quit", "Do want to run as hidden \n It cant be turn off")
    if result:
        root.withdraw()
    else:
        root.destroy()
root.protocol("WM_DELETE_WINDOW", on_close)

schedule_server_connect_start()

root.mainloop()