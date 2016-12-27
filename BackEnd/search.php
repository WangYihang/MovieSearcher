<?php
	if(isset($_GET['keyword'])){
		$keyword = $_GET['keyword'];
		//$keyword = $keyword.replace(" ","");
		echo $keyword;
		//echo exec("python ~/dy2018.py ".$keyword);
		echo system("python ~/dy2018.py 警察");
    		//echo("ret is $ret");
		echo "Over";
	}else{
		die("Please GET the keyword!");
	}
?>
