import tkinter as tk
from tkinter import ttk
import locale
from PIL import Image, ImageTk

def change_to_language():
    language = locale.getdefaultlocale()[0]
    if language == 'vi_VN':
        label.config(text="Nhấn vào nút dưới để chuyển đổi ngôn ngữ")
        button1.config(text="Việt Nam", image=vietnamese_flag, compound=tk.LEFT)
        button2.config(text="Anh", image=english_flag, compound=tk.LEFT)
    else:
        label.config(text="Click the button below to change the language")
        button1.config(text="Vietnamese", image=vietnamese_flag, compound=tk.LEFT)
        button2.config(text="English", image=english_flag, compound=tk.LEFT)

root = tk.Tk()
root.title("Ngôn ngữ ứng dụng")

label = ttk.Label(root, text="Click the button below to change the language")
label.pack(pady=10)

vietnamese_flag = ImageTk.PhotoImage(Image.open("vietnamese_flag.png"))
english_flag = ImageTk.PhotoImage(Image.open("english_flag.png"))

button1 = ttk.Button(root, text="Vietnamese", command=change_to_language)
button1.pack(pady=5)

button2 = ttk.Button(root, text="English", command=change_to_language)
button2.pack(pady=5)

change_to_language()

root.mainloop()

