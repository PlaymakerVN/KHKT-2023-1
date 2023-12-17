import tkinter as tk
from tkinter import ttk
import requests

def show_database():
    response = requests.get(db_entry.get())
    with open("database.txt", "wb") as f:
        f.write(response.content)

    with open("database.txt", "r") as f:
        database_contents = f.read()

    # You can replace the print statement with your preferred way to display the contents of the database
    print(database_contents)

db_on = tk.Tk()
db_on.title("KHKT-2023-1 Database")

url = "https://github.com/PlaymakerVN/KHKT-2023-1/blob/main/database.txt"

db_entry = ttk.Entry(db_on,text=url,font=("Helvetica", 12))
db_entry.pack(side=tk.LEFT, fill=tk.X,expand=True)

ttk.Button(db_on, text="Show Database", command=show_database).pack(side=tk.LEFT)

db_on.mainloop()