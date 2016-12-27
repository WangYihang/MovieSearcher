<?php
include_once("config.php");
require_once('page.class.php'); //分页类
$showrow = 10; //一页显示的行数
$curpage = empty($_GET['page']) ? 1 : $_GET['page']; //当前的页,还应该处理非数字的情况
$curpage = intval($curpage);
$url = "?page={page}"; //分页地址，如果有检索条件 ="?page={page}&q=".$_GET['q']
//省略了链接mysql的代码，测试时自行添加
$sql = "SELECT * FROM movies ";
$total = mysql_num_rows(mysql_query($sql)); //记录总条数
if (!empty($_GET['page']) && $total != 0 && $curpage > ceil($total / $showrow))
$curpage = ceil($total_rows / $showrow); //当前页数大于最后页数，取最后一页
//获取数据
$sql .= " LIMIT " . ($curpage - 1) * $showrow . ",$showrow";
?>


<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head> 
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" /> 
<title>电影资源快速查询</title>
<meta name="keywords" content="电影资源快速查询" />
<meta name="description" content="电影资源快速查询,王一航,哈尔滨工业大学" />
<link rel="stylesheet" type="text/css" href="http://www.sucaihuo.com/jquery/css/common.css" />
<style type="text/css">
p{margin:0}
#page{
height:40px;
padding:20px 0px;
}
#page a{
display:block;
float:left;
margin-right:10px;
padding:2px 12px;
height:24px;
border:1px #cccccc solid;
background:#fff;
text-decoration:none;
color:#808080;
font-size:12px;
line-height:24px;
}
#page a:hover{
color:#077ee3;
border:1px #077ee3 solid;
}
#page a.cur{
border:none;
background:#077ee3;
color:#fff;
}
#page p{
float:left;
padding:2px 12px;
font-size:12px;
height:24px;
line-height:24px;
color:#bbb;
border:1px #ccc solid;
background:#fcfcfc;
margin-right:8px;

}
#page p.pageRemark{
border-style:none;
background:none;
margin-right:0px;
padding:4px 0px;
color:#666;
}
#page p.pageRemark b{
color:red;
}
#page p.pageEllipsis{
border-style:none;
background:none;
padding:4px 0px;
color:#808080;
}
.dates li {font-size: 14px;margin:20px 0}
.dates li span{float:right}
</style>
</head>
<body>
<div class="head">
<div class="head_inner clearfix">
<ul id="nav">
<li><a href="index.php">首 页</a></li>
<li><form action="queue.php" method="POST">
请输入需要查询的关键字 : <input type="text" name="keyword">
<input type="submit" />
</form></li>
</ul>
<a class="logo" href="http://www.wangyihang.net"><img src="http://upload.jianshu.io/users/upload_avatars/2355077/9551c780e5a1.jpg?imageMogr/thumbnail/48x48/quality/100"/></a>
</div>
</div>
<div class="container">
<div class="demo">
<h2 class="title"><a href="index.php">电影资源快速查询</a></h2>
<div class="showPage">
<?php
if ($total > $showrow) {//总记录数大于每页显示数，显示分页
$page = new page($total, $showrow, $curpage, $url, 2);
echo $page->myde_write();
}
?>
</div>
<div class="showData">

<!--<ul class="dates">
<?php while ($row = mysql_fetch_array($query)) { ?>
<li>
<span><?php echo $row['movieID'] ?></span>
<a target="_blank" href="http://www.sucaihuo.com/js"><?php echo $row['t1'] ?></a>
</li>
<?php } ?>
</ul>
-->
<?php
echo "<table border='1'>
<tr>
<th>movieID</th>
<th>movieTitle</th>
<th>movieDescribe</th>
<th>movieTime</th>
<th>movieClickTimes</th>
<th>movieDownloadLink</th>
<th>movieKey</th>
</tr>";
$query = mysql_query($sql);
while ($row = mysql_fetch_array($query))
  {
  echo "<tr>";
  echo "<td>" . $row['movieID'] . "</td>";
  echo "<td>" . $row['movieTitle'] . "</td>";
  echo "<td>" . $row['movieDescribe'] . "</td>";
    echo "<td>" . $row['movieTime'] . "</td>";
      echo "<td>" . $row['movieClickTimes'] . "</td>";
  echo "<td>" . $row['movieDownloadLink'] . "</td>";
  echo "<td>" . $row['movieKey'] . "</td>";
  echo "</tr>";
  }
echo "</table>";
?>

<!--显示数据区-->
</div>

</div>
</div>
<div class="foot">
<a href="http://www.wangyihang.net/" target="_blank">Powered by 王一航</a>
</div>
<script type="text/javascript" src="http://www.sucaihuo.com/Public/js/other/jquery.js"></script> 
</body>
</html
