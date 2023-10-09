#Run in Root 

import time
import requests
from datetime import datetime as dt

# Host Locate
hosts_path = "C:\Windows\System32\drivers\etc\hosts"
# localhost's IP
redirect = "127.0.0.1"

# Websites block
# website_list =["fast.com"]
# check = input("Y or N:")

# url1 = 'http://incognitochat.free.nf'
r = requests.post(url="https://uninhibited-pints.000webhostapp.com/post.php",data={'text':'BOT IS STARTED'})

# Main 
# print(x.text)
# while True:
#     if check == "y" or check == "Y":
#         print("Working hours...")
#         with open(hosts_path, 'r+') as file:
#             content = file.read()
#             for website in website_list:
#                 if website in content:
#                     pass
#                 else:
#                     # Apply to host
#                     file.write(redirect + " " + website + "\n")
#         #Success 
#         print("Blocked !!") 
#         break
#     else:
#         with open(hosts_path, "r+") as file:
#             content = file.readlines()
#             file.seek(0)
#             for line in content:
#                 if not any(website in line for website in website_list):
#                     # Apply to host
#                     file.write(line)
#             file.truncate()
#             print("Unblocked !!")
#         break

# import flet as ft

# class Message():
#     def __init__(self, user: str, text: str):
#         self.user = user
#         self.text = text

# def main(page: ft.Page):

#     chat = ft.Column()
#     new_message = ft.TextField()

#     def on_message(message: Message):
#         chat.controls.append(ft.Text(f"{message.user}: {message.text}"))
#         page.update()

#     page.pubsub.subscribe(on_message)

#     def send_click(e):
#         page.pubsub.send_all(Message(user=page.session_id, text=new_message.value))
#         new_message.value = ""
#         page.update()

#     page.add(chat, ft.Row([new_message, ft.ElevatedButton("Send", on_click=send_click)]))

# ft.app(target=main, view=ft.AppView.WEB_BROWSER)