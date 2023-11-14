text_message"<div> <b class='user-name'>USER - ".date("g:i A")."</b><p id='user-chat'> ".stripslashes(htmlspecialchars($text))."</p></div><br>"
bot_message = "<div class='botchat'><p class='chat-time'></p><b> cleared </b></div><br>";
# def testing(data):
# 	if data =="gay":
# 		print("YS IM GAYING")
# 		a = "LOL"
# 		return a

def handle(key,data):
	if key == "text":

	if data == "gay":
		with open("log.html", "a") as file:
			file.write("<div class='botchat'><p class='chat-time'>"+data+"</p><b> cleared </b></div><br>")
			file.write("\n")
			print("ADDED TEXT" + data)
	else:
		print("not work")
	a = "LOL"
	return a

