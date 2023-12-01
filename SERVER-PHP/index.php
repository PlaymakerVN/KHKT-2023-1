<?php
session_start();
$_SESSION['name']="USER";
$index = file_get_contents("index.html");          
echo $index;
?>