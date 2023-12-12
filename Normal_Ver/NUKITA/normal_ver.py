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
            try:
                print("ADD",ip_address)
                with open(filepath, 'a') as file:
                    file.write(f"\n127.0.0.1 {ip_address}")
                messagebox.showinfo("Success", f"The IP address {ip_address} has been blocked.")
                entry.delete(0, 'end')
                update_table()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while blocking the IP address: {str(e)}")
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
                
root = tk.Tk()
root.title("KHKT PROJECT")
root.geometry("550x400")

# Styling
style = ttk.Style(root)
style.theme_use("alt")
style.configure("Treeview.Heading", font=("Helvetica", 8, "bold"))
style.configure("Treeview", font=("Helvetica", 12))
style.configure("TButton", font=("Helvetica", 12))

var = tk.StringVar(value=on_or_off(ip_google_filter))

var2 = tk.StringVar(value=on_or_off(ip_youtube_filter))

# Create radio buttons
radio_frame = tk.Frame(root, bd=1, relief="solid")
radio_frame.pack(side=tk.LEFT, padx=10,pady=10)

head_text = tk.Label(radio_frame, text="Google filter") 
head_text.pack()

radio_button1 = tk.Radiobutton(radio_frame, text="On", variable=var, value="on", command=handle_selection)
radio_button1.pack()

radio_button2 = tk.Radiobutton(radio_frame, text="Off", variable=var, value="off", command=handle_selection)
radio_button2.pack()

head_text = tk.Label(radio_frame, text="Youtube filter") 
head_text.pack()

radio_button3 = tk.Radiobutton(radio_frame, text="On", variable=var2, value="on", command=handle_selection2)
radio_button3.pack()

radio_button4 = tk.Radiobutton(radio_frame, text="Off", variable=var2, value="off", command=handle_selection2)
radio_button4.pack()

head_text = tk.Label(radio_frame, text="DNS PROTECT") 
head_text.pack()

radio_button5 = tk.Radiobutton(radio_frame, text="On", variable=var2, value="on", command=handle_selection2)
radio_button5.pack()

radio_button5 = tk.Radiobutton(radio_frame, text="Off", variable=var2, value="off", command=handle_selection2)
radio_button5.pack()


# Create the button frame
button_frame = tk.Frame(root, pady=10 , bd=1, relief="solid")
button_frame.pack(side=tk.TOP, fill=tk.X)

# Create the label
label = tk.Label(button_frame, text="Enter IP Address:")
label.pack(side=tk.LEFT)

# Create the entry
entry = tk.Entry(button_frame, font=("Helvetica", 12))
entry.pack(side=tk.LEFT)

# Create the button frame inner
button_frame_inner = tk.Frame(button_frame)
button_frame_inner.pack(side=tk.RIGHT)

# Create the block and delete buttons within the button frame inner
block_button = ttk.Button(button_frame_inner, text="Block IP", command=block_ip)
block_button.pack(side=tk.LEFT, padx=5)

delete_button = ttk.Button(button_frame_inner, text="Delete IP", command=delete_ip)
delete_button.pack(side=tk.LEFT)

# Fix the button_frame on top
button_frame.pack(side=tk.TOP, fill=tk.X)

# Center the button_frame within the root window
root.update()  # Update the root window to get its current size
button_frame.place(relx=0.5, rely=0, anchor=tk.N)

# Update button_frame position whenever the root window size changes
def update_button_frame_pos(event):
    button_frame.update()  # Update the button_frame to get its current size
    button_frame.place(relx=0.5, rely=0, anchor=tk.N)

root.bind("<Configure>", update_button_frame_pos)  # Bind the update_button_frame_pos function to the root window's size change event

# Table Frame

table_frame = tk.Frame(root, bd=1, relief="solid")
table_frame.pack(pady=70, anchor="center",side=tk.LEFT)

table_columns = ("Blocked IP Address",)
table = ttk.Treeview(table_frame, columns=table_columns, show="headings")
table.heading("Blocked IP Address", text="Blocked IP Address")
table.pack(padx=100)

table_frame.config(width=1600, height=800)  # Setting the new size for the table frame
table.config(height=15)  # Displaying 15 rows in the table
# Update Table
update_table()

root.mainloop()







