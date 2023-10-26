#Run in Root 

import time
import requests
from datetime import datetime as dt

# Host Locate
# hosts_path = "C:\Windows\System32\drivers\etc\hosts"
hosts_path = "/etc/hosts"
# localhost's IP
redirect = "127.0.0.1"
server="http://localhost:8080/post.php"
# server="https://khkt-lxt.000webhostapp.com/post.php"
# 
r = requests.post(url=server,data={'text':'BOT IS STARTED'})
# Websites block
website_list =["anonsop.com","text.com"]

c = input("Y or N:")
#Function
# def get_ip():
r = requests.post(url=server,data={'text':'ip'})
a = r.text.split('\n')
print(a)
    # for a in range(len(a)):
    #     print(a)
#     pass
# get_ip()
#BLOCK
def block():
    r = requests.post(url=server,data={'text':'BLOCKED'})
    #POST IP
    for i in range(len(website_list)):
        print("BLOCKED " + website_list[i])
        r = requests.post(url=server,data={'text':'IP : '+ website_list[i]})
    for j in range(len(a)):
        print("BLOCKED " + a[j])
        r = requests.post(url=server,data={'text':'IP : '+ a[j]})
    #READ FILE
    with open(hosts_path, 'r+') as file:
        content = file.read()
        for website in website_list:
            if website in content:
                pass
            else:
                # Apply to host
                file.write(redirect + " " + website + "\n")
                file.write(redirect + " " +"www."+ website + "\n")
                for k in range(len(a)):
                    file.write(redirect + " " + a[k] + "\n")
    pass

#UNBLOCK
def unblock():
    r = requests.post(url=server,data={'text':'UNBLOCKED'})
    with open(hosts_path, "r+") as file:
        content = file.readlines()
        file.seek(0)
        for line in content:
            if not any(website in line for website in website_list):
                # Apply to host
                file.write(line)
                #POST
        file.truncate()
        print("Unblocked !!")
    pass




#MCORE PROGRAMME
while True:
    if(c == "y" or c == "Y"):
        block()
        break
    if (c == "n" or c =="N"):
        unblock()
        break

