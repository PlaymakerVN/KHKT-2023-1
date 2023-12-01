#Run in Root 
import os 

import time
import requests
import json

import socket

from datetime import datetime as dt
from browser_history import browsers, generic, utils,core



# POST
def POST(type,content):
    r = requests.post(url=server,data={type:content})
    print("POST : "+content)
# GET HOST
def get_hosts_path():
    plat = utils.get_platform_name()
    #LOCATE HOSTS 
    if plat == "Windows":
        hosts_path = "C:\Windows\System32\drivers\etc\hosts"
    if plat == "Linux":
        hosts_path = "/etc/hosts"
    print("USING "+plat+" METHOD")
    return hosts_path
#GET IP
def get_ip():
    r = requests.post(url=server,data={'text':'blacklist'})
    getted_ip = r.text.split('\n')
    return getted_ip
#CHECK PORT OPENING
def check_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1',8080))
    if result == 0:
       print ("Port is open")
       a=1
    else:
       print ("Port is not open")
       a=0
    sock.close()
    return a
#MAIN Function
#BLOCK

def block():
    r = requests.post(url=server,data={'text':'BLOCKED'})
    for i in range(len(website_list)):
        print("BLOCKED " + website_list[i])
        r = requests.post(url=server,data={'text':'IP BLOCKED: '+ website_list[i]})
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
#SAVE URL HISTORY
def save_url_history(se):
    domain_connected = core.get_history()
    domain_connected.save("history_file", output_format="json")
    f = open('history_file')
    data = json.load(f)
    print("SAVED HISTORY BROWSERS")
    for i in data['history']:
        a = i['URL']
        POST('url_p',i['URL'])


#MCORE PROGRAMME

# localhost's IP
redirect = "127.0.0.1"
server_local=""

d = input("LOCAL(1) or PUBLIC(2):")
if (d =="1"):
    server_local="y"
if (d =="2"):
    server_local="n"
#SERVER LOCATING

# if check_port() == 0:

if server_local == "y" or server_local == "Y":
    server="http://localhost:8000"
if server_local == "n" or server_local == "N":
    server="https://khkt-lxt.000webhostapp.com/post.php"

# Websites block
website_ban = ["anonops.com"]
website_cloud = get_ip()
website_list = website_cloud+website_ban
for i in range(len(website_list)):
    print("LIST :" + website_list[i])


POST('text','BOT IS STARTED')
POST('bl_p','127.0.0.1:80')
POST('bl_p','youtube.com')
POST('bl_p','facebook.com')
c = input("Y or N:")

hosts_path = get_hosts_path()
save_url_history(server_local)



while True:
    if(c == "y" or c == "Y"):
        block()
        break
    if (c == "n" or c =="N"):
        unblock()
        break

