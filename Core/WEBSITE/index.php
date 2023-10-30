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
?>
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf+7" />
        <title>KHKT - LXT</title>
        <meta name="description" content="KHKT - LXT" />
        <link rel="stylesheet" href="style.css?v=<?php echo time(); ?>">
    </head>
    <body>
        <?php
        // if(!isset($_SESSION['name'])){
        //     loginForm();
        // }
        // else {
        ?>
            <div id="title">
                <p class="welcome">Welcome, <b><?php echo $_SESSION['name']; ?></b></p>
                <!-- <p class="logout"><a id="exit" href="#">Exit Chat</a></p> -->
            </div>
            <div class="sidebar">
                <div id="user"></div>
                <div id="user-list"></div>
            </div>
            <div id="console-box">
                <div id="wrapper-1">
                </div>
                <div id="wrapper-2">
                    <div id="chatbox">
                    <?php
                    if(file_exists("log.html") && filesize("log.html") > 0){
                        $contents = file_get_contents("log.html");          
                        echo $contents;
                    }
                    ?>
                    </div>
                    <form name="message" action="">
                        <input name="usermsg" type="text" id="usermsg" />
                        <input name="submitmsg" type="submit" id="submitmsg" value="Send" />
                    </form>
                </div>
            </div>
            <div id="menu">
            </div>
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
        <script type="text/javascript">
            // jQuery Document 
            $(document).ready(function () {
                $("#submitmsg").click(function () {
                    var clientmsg = $("#usermsg").val();
                    $.post("post.php", { text: clientmsg });
                    $("#usermsg").val("");
                    return false;
                });
                function loadLog() {
                    var oldscrollHeight = $("#chatbox")[0].scrollHeight - 20; //Scroll height before the request 
                    $.ajax({
                        url: "log.html",
                        cache: false,
                        success: function (html) {
                            $("#chatbox").html(html); //Insert chat log into the #chatbox div 
                            //Auto-scroll 
                            var newscrollHeight = $("#chatbox")[0].scrollHeight - 20; //Scroll height after the request 
                            if(newscrollHeight > oldscrollHeight){
                                $("#chatbox").animate({ scrollTop: newscrollHeight }, 'normal'); //Autoscroll to bottom of div 
                            }   
                        }
                    });
                }
                setInterval (loadLog, 2500);
                $("#exit").click(function () {
                    var exit = confirm("Are you sure you want to end the session?");
                    if (exit == true) {
                    window.location = "index.php?logout=true";
                    }
                });
            });
        </script>
    </body>
</html>
<?php
// }
?>