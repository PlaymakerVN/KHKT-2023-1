<?php
session_start();
$text = $_POST['text'];
//USER
function addinfile($dir) {
	file_put_contents($dir.".html", "");
}

if(isset($_SESSION['name'])){
	//Main Chat
	$text_message = "<div> <b class='user-name'>USER - ".date("g:i A")."</b><p id='user-chat'> ".stripslashes(htmlspecialchars($text))."</p></div><br>";
    file_put_contents("log.html", $text_message, FILE_APPEND | LOCK_EX);
	//Clear Function
	if (str_starts_with($_POST['text'],"/clear")) {
		$dir = explode('.', $_POST['text']);
		addinfile(trim($dir[1]));
		$text_message = "<div class='botchat'> 	<p class='chat-time'>".date("g:i A")."</p><b>".trim($dir[1])." cleared </b></div><br>";
		file_put_contents("log.html", $text_message, FILE_APPEND | LOCK_EX);
	}
    //Detect IP
    if (str_starts_with($_POST['text'],"IP")) {
		$ip = explode(' ', $_POST['text']);
		//SAVE IP
		file_put_contents("blacklist.html", trim($ip[1]).PHP_EOL, FILE_APPEND | LOCK_EX);
		//PRINT IP
	 	$text_message = "<div class='botchat'> 	<p class='chat-time'>".date("g:i A")."</p> <b>ADDED IP ".stripslashes(htmlspecialchars($ip[1]))."</b></div><br>";
    	file_put_contents("log.html", $text_message, FILE_APPEND | LOCK_EX);
	}
//BOT
}else{
	if($_POST['text']=="blacklist"){
		echo(file_get_contents("blacklist.html")); 
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