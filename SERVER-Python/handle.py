# def testing(data):
# 	if data =="gay":
# 		print("YS IM GAYING")
# 		a = "LOL"
# 		return a
import os
import json

f_device="information.html"
f_connected="devicecon.html"
f_log="log.html"
f_his="history.html"
f_bl="blacklist.html"
def append_text(file_path, text):
    mode = 'a' if os.path.exists(file_path) else 'w'    
    with open(file_path, mode) as file:
        file.write(text)
def replace_text(file_path, text):
    mode = 'w'
    with open(file_path, mode) as file:
        file.write(text)
device_connected=[]
replace_text(f_device,"0")
replace_text(f_connected,"")

def handle(key,data):
	user_post="<div><b class='user-name'> </b><p id='user-chat'>"+data+"</p></div><br>" + "\n"
	bot_post="<div class='botchat'><p class='chat-time'>"+data+"</p><b>  </b></div><br>"+"\n"
	connected_up=""
	#USER SEND
	if key == "text":
		append_text(f_log,user_post)
		print("ADDED TEXT" + data)
		r = "USER OK"
	#CLIENT METHOD\
	# MAKE ID FOR DEIVCE CONNECTED
	if key=="new_connect":
		with open(f_connected, 'r+') as file:
			global device_connected
			content = file.read()
			if data in device_connected : 
				p = device_connected.index(data)
				r="ID :"+str(int(p)+1)
			if data not in device_connected:
				device_connected.append(data)
				file.write('<a href=""><span1 class="tooltip">'+data+'</span></a>' + "\n")

				print("DEVICE CONNECTED : ",device_connected)
				print("WRITE " + data)

				#INFORMATION UPDATE
				replace_text(f_device,str(len(device_connected)))


				p = device_connected.index(data)
				print("NEW DEVICE CONNECT SET ID :"+str(int(p)+1))
				r="ID :"+str(int(p)+1)

	# if key=="bot":
	# 	append_text(f_device,user_post)
	# 	print("ADDED TEXT" + data)
	# 	r = "CLIENT OK"

	# HISTORY POST
	if key =="his_p":
		append_text(f_his,data+"\n <hr>")
		append_text(f_log,bot_post)
		print("ADDED TEXT" + data)
		r = "CLIENT OK"
	#BLACKLIST POST
	if key =="bl_p":
		append_text(f_bl,data+"\n <hr>")
		append_text(f_log,bot_post)
		print("ADDED TEXT" + data)
		r = "CLIENT OK"
	if key=="replace" and data=="his":
		replace_text(f_his,"<hr>")
		print("CREATE" + data)
		r = "CLIENT OK"
	return r

