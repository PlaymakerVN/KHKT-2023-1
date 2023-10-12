<?php
session_start();
if(isset($_SESSION['name'])){
	$text = $_POST['text'];
	if($_POST['text'] == "Console.clear"){
		file_put_contents("log.html", "");
	}else{
	$text_message = "<div> <b class='user-name'>".$_SESSION['name']."</b> ".stripslashes(htmlspecialchars($text))."</div><br>";
    file_put_contents("log.html", $text_message, FILE_APPEND | LOCK_EX);
	}
}else{
    $_SESSION['name']="BOT";
    $text = $_POST['text'];
	date_default_timezone_set('Asia/Ho_Chi_Minh');
	$text_message = "<div class='botchat'>
						<p class='chat-time'>".date("g:i A")."</p> 
						<b>".stripslashes(htmlspecialchars($text))."</b>
					</div>
					<br>";
    file_put_contents("log.html", $text_message, FILE_APPEND | LOCK_EX);

}
?>