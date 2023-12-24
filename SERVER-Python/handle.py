# def testing(data):
# 	if data =="gay":
# 		print("YS IM GAYING")
# 		a = "LOL"
# 		return a
import os
import json
import requests

f_device="information.html"
f_connected="devicecon.html"
f_log="log.html"
f_his=[]
f_bl="blacklist.html"
def append_text(file_path, text):
    mode = 'a' if os.path.exists(file_path) else 'w'    
    with open(file_path, mode) as file:
        file.write(text)
def replace_text(file_path, text):
    mode = 'w'
    with open(file_path, mode) as file:
        file.write(text)
def delete_string(filename, string_to_delete):
    # Open file in read mode
    with open(filename, 'r') as read_file:
        # Read all lines in the file
        lines = read_file.readlines()

    # Open file in write mode
    with open(filename, 'w') as write_file:
        # Write all lines to the file, skipping the line that contains the string to delete
        for line in lines:
            if string_to_delete not in line:
                write_file.write(line)
def delete_line(file_path, target_string):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            if target_string not in line:
                file.write(line)
def create_file(filename):
	try:
		with open(filename, 'x') as file:
			print(f"File {filename} created successfully.")
	except FileExistsError:
		print(f"File {filename} already exists.")
device_connected=[]
replace_text(f_device,"0")
replace_text(f_connected,"")
def get_db(url):
	response = requests.get(url)
	if response.status_code == 200:
		file_content = response.text
		append_text(f_log,f"{url} ip getted")
		append_text(f_bl,"\n"+file_content)
	else:
		append_text(f_log,f"{url} cant get")
		print(f"Error: {response.status_code}")
db1="https://raw.githubusercontent.com/PlaymakerVN/KHKT-2023-1/main/database.txt"
def handle(key,data):
	user_post="<div><b class='user-name'> </b><p id='user-chat'>"+data+"</p></div><br>" + "\n"
	bot_post="<div class='botchat'><p class='chat-time'>"+data+"</p><b>  </b></div><br>"+"\n"
	connected_up=""
	#USER SEND
	if key == "text":
		if data.startswith("/clear:"):
			f_clear=data.split(":")[1]
			replace_text(f_clear,"\n")
			r = "USER OK"
		else:
			append_text(f_log,user_post)
			print("ADDED TEXT" + data)
			r = "USER OK"
	if key == "post_blacklist":
		if data.startswith("$del:"):
			del_ip=data.split(":")[1]
			delete_line(f_bl,del_ip)
			r = "USER OK"
		if data.startswith("$clear"):
			append_text(f_log,"CLEAR BLACKLIST")
			replace_text(f_bl,"\n")
		if data.startswith("$get:"):
			append_text(f_log,"GETTING DATA")
			url=data.split("$get:")[0]
			get_db(db1)
			r = "USER OK"
		if data.startswith("$add:"):
			url=data.split("$add:")[1]
			append_text(f_bl,url+"\n")
			r = "USER OK"
	#CLIENT METHOD\
	# MAKE ID FOR DEIVCE CONNECTED
	if key=="new_connect":
		with open(f_connected, 'r+') as file:
			data_ip=data.split(":")[0]
			data_os=data.split(":")[1]
			global device_connected
			content = file.read()
			if data_ip in device_connected : 
				p = device_connected.index(data_ip)
				r="ID :"+str(int(p)+1)
			if data_ip not in device_connected:
				device_connected.append(data_ip)
				p = device_connected.index(data_ip)

				file.write('<a href=""id="'+str(int(p)+1)+'"><span1 class="tooltip">'+data_ip+'</span></a>' + "\n")
				print("DEVICE CONNECTED : ",device_connected)
				print("WRITE " + data_ip)

				#INFORMATION UPDATE
				replace_text(f_device,str(len(device_connected)))

				print("NEW DEVICE CONNECT SET ID :"+str(int(p)+1))
				r="ID :"+str(int(p)+1)
				hp="history."+str(int(p)+1)+".html"
				bp="blocked."+str(int(p)+1)+".html"
				create_file(hp)
				create_file(bp)
				f_his.append(hp)

	if key=="get_blacklist":
		file = open(f_bl, "r")
		# Read the content of the file
		content = file.read()
		# Print the content
		print(content)
		file.close()
		r = content


	# HISTORY POST
	if ":his" in key:
		cl_id=int(key.split(':his')[0])
		append_text(f_his[cl_id-1],data+"\n <hr>")
		print("ADDED TEXT" + data)
		r = "CLIENT OK"
	#BLACKLIST POST
	if key =="bl_p":
		append_text(f_bl,data+"\n <hr>")
		append_text(f_log,bot_post)
		print("ADDED TEXT" + data)
		r = "CLIENT OK"
	if ":hreplace" in key and data=="his":

		cl_id=int(key.split(':hreplace')[0])
		replace_text(f_his[cl_id-1],"<hr>")

		print("CREATE" + data)
		r = "CLIENT OK"

	return r

