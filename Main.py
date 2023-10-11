#Run in Root 

import time
import requests
from datetime import datetime as dt

# Host Locate
hosts_path = "C:\Windows\System32\drivers\etc\hosts"
# localhost's IP
redirect = "127.0.0.1"

server="https://uninhibited-pints.000webhostapp.com/post.php"

r = requests.post(url=server,data={'text':'BOT IS STARTED'})

# Websites block
website_list =["fast.com","text.com"]

check = input("Y or N:")

#Main
while True:
    if check == "y" or check == "Y":
        print("Working hours...")
        r = requests.post(url=server,data={'text':'BLOCKED'})
        #POST IP
        for i in range(len(website_list)):
        	r = requests.post(url=server,data={'text':'IP : '+ website_list[i]})
        with open(hosts_path, 'r+') as file:
            content = file.read()
            for website in website_list:
                if website in content:
                    pass
                else:
                    # Apply to host
                    file.write(redirect + " " + website + "\n")
                    file.write(redirect + " " +"www."+ website + "\n")
        #Success 
        print("Blocked !!") 
        break
    else:
        with open(hosts_path, "r+") as file:
            content = file.readlines()
            file.seek(0)
            for line in content:
                if not any(website in line for website in website_list):
                    # Apply to host
                    file.write(line)
            file.truncate()
            print("Unblocked !!")
        break

