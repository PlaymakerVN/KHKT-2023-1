# def testing(data):
# 	if data =="gay":
# 		print("YS IM GAYING")
# 		a = "LOL"
# 		return a
import os


p_log="log.html"

def append_text_to_file(file_path, text):
    mode = 'a' if os.path.exists(file_path) else 'w'
    
    with open(file_path, mode) as file:
        file.write(text)

def handle(key,data):
	user_post="<div><b class='user-name'>USER </b><p id='user-chat'>"+data+"</p></div><br>" + "\n"
	bot_post="<div class='botchat'><p class='chat-time'>"+data+"</p><b> cleared </b></div><br>"+"\n"
	connected_up=""
	#USER SEND
	if key == "text":
		append_text_to_file(p_log,user_post)
		print("ADDED TEXT " + data)
		a = "USER OK"
	#CLIENT METHOD
	if key=="bot":
		append_text_to_file(p_log,user_post)
		print("ADDED TEXT " + data)
		a = "CLIENT OK"
	if key=="create":
		append_text_to_file(p_log,connected_up)
		print("CREATE " + data)
		a = "CLIENT OK"
	return a

