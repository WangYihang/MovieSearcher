


<?php
// 接受用户添加的关键字的参数
$keyword = $_POST['keyword'];
echo $keyword;
// 这里需要防注入

//todo


$servername = "localhost";
$username = "ubuntu";
$password = "admin123";
$dbname = "bigdata";
header("Content-Type: text/html;charset=utf-8");
// 创建连接
$conn = new mysqli($servername, $username, $password, $dbname);
// 检测连接
if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
}
// 设置字符集
$conn->query("set names UTF8");


// 将用户post的数据(关键字)进行插入
if ($keyword != null){
    $conn->query("INSERT INTO queue (`keyword`) VALUES ('".$keyword."');");
}


$sql = "SELECT * from queue";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // 输出每行数据
    while($row = $result->fetch_assoc()) {
        echo "<br> id: ". $row["id"]. " - Name: ". $row["keyword"]. " " . $row["status"];
    }
} else {
    echo "0 个结果";
}
$conn->close();
// 添加到队列以后直接返回
Header("Location:index.php");
?> 
