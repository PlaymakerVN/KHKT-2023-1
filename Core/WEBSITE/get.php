echo 'Dữ Liệu Chúng Tôi Nhận Được Là <br/>';
foreach ($_GET as $key => $val)
{
    echo '<strong>' . $key . ' => ' . $val . '</strong><br/>';
}