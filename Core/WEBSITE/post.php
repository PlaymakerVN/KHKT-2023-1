<?php
session_start();
$text = $_POST['text'];
$testing = "no";
//USER
if(isset($_SESSION['name'])){
	//Main Chat
	$text_message = "<div> <b class='user-name'>".$_SESSION['name']."</b> ".stripslashes(htmlspecialchars($text))."</div><br>";
    file_put_contents("log.html", $text_message, FILE_APPEND | LOCK_EX);
	//Clear Function
	if($_POST['text'] == "Console.clear"){
		file_put_contents("log.html", "");
	}
	if($_POST['text'] == "Console.IP"){
		$text_message = "<div class='botchat'> 	<p class='chat-time'>".date("g:i A")."</p> <b>IP CLEARED</b></div><br>";
		file_put_contents("ip_ban.html", "");
	}
    //Detect IP
    if (str_starts_with($_POST['text'],"IP")) {
		$ip = explode(' ', $_POST['text']);
		//SAVE IP
		if ($testing == "yes"){
			file_put_contents("ip_ban.html", $ip[1], FILE_APPEND | LOCK_EX);
			file_put_contents("ip_ban.html", "");
		}else{
			file_put_contents("ip_ban.html", $ip[1], FILE_APPEND | LOCK_EX);
		}
		//PRINT IP
	 	$text_message = "<div class='botchat'> 	<p class='chat-time'>".date("g:i A")."</p> <b>ADDED IP ".stripslashes(htmlspecialchars($ip[1]))."</b></div><br>";
    	file_put_contents("log.html", $text_message, FILE_APPEND | LOCK_EX);
	}
//BOT
}else{
	if($_POST['text']=="ip"){
		file_get_contents("ip_ban.html"); 
	}else{
	//Main
    $_SESSION['name']="BOT";
	date_default_timezone_set('Asia/Ho_Chi_Minh');
	$text_message = "<div class='botchat'>
						<p class='chat-time'>".date("g:i A")."</p> 
						<b>".stripslashes(htmlspecialchars($text))."</b>
					</div>
					<br>";
    file_put_contents("log.html", $text_message, FILE_APPEND | LOCK_EX);
	}
}
?>