# def testing(data):
# 	if data =="gay":
# 		print("YS IM GAYING")
# 		a = "LOL"
# 		return a
import os


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

def handle(key,data):
	user_post="<div><b class='user-name'> </b><p id='user-chat'>"+data+"</p></div><br>" + "\n"
	bot_post="<div class='botchat'><p class='chat-time'>"+data+"</p><b>  </b></div><br>"+"\n"
	connected_up=""
	#USER SEND
	if key == "text":
		append_text(f_log,user_post)
		print("ADDED TEXT" + data)
		a = "USER OK"

	#CLIENT METHOD
	if key=="bot":
		append_text(f_log,user_post)
		print("ADDED TEXT" + data)
		a = "CLIENT OK"
	if key =="url_p":
		append_text(f_his,data+"\n <hr>")
		append_text(f_log,bot_post)
		print("ADDED TEXT" + data)
		a = "CLIENT OK"
	if key =="bl_p":
		append_text(f_bl,data+"\n <hr>")
		append_text(f_log,bot_post)
		print("ADDED TEXT" + data)
		a = "CLIENT OK"
	if key=="replace" and data=="his":
		replace_text(f_his,"<hr>")
		print("CREATE" + data)
		a = "CLIENT OK"
	if key=="create":
		append_text(f_log,bot_post)
		print("CREATE" + data)
		a = "CLIENT OK"
	return a

