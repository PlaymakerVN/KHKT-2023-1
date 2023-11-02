#Run in Root 
import os 
import time
import requests
from browser_history import get_history
from datetime import datetime as dt
server="http://localhost:8080/post.php"
hosts_path="/home/playmakervn/Documents/GitHub/KHKT-2023-1/Test/untitled.txt"
# r = requests.post(url=server,data={'text':'TESTING SERVER'})
# r = requests.post(url=server,data={'text':'ip'})
# a=r.text.split('\n')
# for i in range(len(a)):
# 	print(a[i])
# print(a[0])
# print(a[1])
def unblock():
    with open(hosts_path, "r+") as file:
    	domain_connected = get_history()
    	file.write(domain_connected.histories)
    pass
unblock()
# with open(hosts_path, 'r+') as file:
# 	content = file.read()
# 	for i in range(len(a)):
# 		file.write("Testing " + a[i] + "\n")
