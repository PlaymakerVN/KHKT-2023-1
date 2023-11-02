<?php
session_start();
// if(isset($_GET['logout'])){    
    
//     //Simple exit message 
//     $logout_message = "<div class='msgln'><span class='left-info'>User <b class='user-name-left'>". $_SESSION['name'] ."</b> has left the chat session.</span><br></div>";
//     file_put_contents("log.html", $logout_message, FILE_APPEND | LOCK_EX);
    
//     session_destroy();
//     header("Location: index.php"); //Redirect the user 
// }
$_SESSION['name']="USER";
// if(isset($_POST['enter'])){
//     if($_POST['name'] != ""){
//         $_SESSION['name'] = stripslashes(htmlspecialchars($_POST['name']));
//     }
//     else{
//         echo '<span class="error">Please type in a name</span>';
//     }
// }
// function loginForm(){
//     echo 
//     '<div id="loginform"> 
// <p>Please enter your name to continue!</p> 
// <form action="index.php" method="post"> 
// <label for="name">Name &mdash;</label> 
// <input type="text" name="name" id="name" /> 
// <input type="submit" name="enter" id="enter" value="Enter" /> 
// </form> 
// </div>';
// }
$index = file_get_contents("index.html");          
echo $index;
?>