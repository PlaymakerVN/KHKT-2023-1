#Run in Root 
import os 
import time
import requests
import json
import socket
import urllib.parse
import time
import subprocess


from datetime import datetime as dt
from browser_history import browsers, generic, utils,core

version = "Alpha_1.1"
# POST
def POST(type,content):
    r = requests.post(url=server,data={type:content})
    # print("POST : "+content)
def post_info():
     r = requests.post(url=server,data={"new_connect":"123123.123"})
     print(r.text)
    # POST("new_connect",utils.get_platform_name())
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
def get_local_ip():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    return IPAddr


def get_ip():
    r = requests.post(url=server,data={'get_blacklist':'blacklist'})
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

def block(website_list):
    # r = requests.post(url=server,data={'text':'BLOCKED'})
    for i in range(len(website_list)):
        print("BLOCKED " + website_list[i])
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
def solve_url_his(input_url):
    parsed_url = urllib.parse.urlparse(input_url)
    result = parsed_url.scheme + "://" + parsed_url.netloc
    return result
def post_url_his(se):

    # SAVE HIS
    domain_connected = core.get_history()
    domain_connected.save("history_file", output_format="json")
    f = open('history_file')
    data = json.load(f)
    print("SAVED HISTORY BROWSERS")
    a=[]
    b=[]
    # FILTER HIS
    dataArray=data['history']
    POST('replace','his')
    for i in range(len(dataArray)):
        # b.append(solve_url_his(data['history'][i]['URL']))
        # print(b)
        a.append(solve_url_his(data['history'][i]['URL']))
        # Remove duplcated
        c= list(set(a))
    for o in range(len(c)):
        r=POST('his_p',c[o])
        #LOG
    print("HISTORY SAVED AND POSTED ", len(a) )

#MCORE PROGRAMME

# localhost's IP
redirect = "127.0.0.1"

#SERVER LOCATING

server_local=1
if server_local == 1:
    server="http://localhost:8000"
if server_local == 2:
    server="https://khkt-lxt.000webhostapp.com/post.php"

# Websites block
# website_ban = ["anonops.com"]
# website_cloud = get_ip()
# website_list = website_cloud+website_ban
# for i in range(len(website_list)):
#     print("LIST :" + website_list[i])

# c = input("Y or N:")
hosts_path = get_hosts_path()
post_info()
post_url_his(server_local)
c="y"
while True:
    if(c == "y" or c == "Y"):
        block(get_ip())
    if (c == "n" or c =="N"):
        break
