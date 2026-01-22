<?php

//数据库查询操作
	function getquerydata($sql){
		//获取相关路径
		$config_path = "";
		//获取配置参数
		$config = require($config_path);
		//获取数据库连接
		$link = getconnection($config);
		$link->query("SET NAMES utf8");
		$data = array();
		$res = $link->query($sql);
		if($res->num_rows > 0){
			while($row = $res->fetch_assoc()){
				array_push($data,$row);
			}
		}
		if($link){
			mysqli_close($link);
		}
		return $data;
	}
	//获取数据库连接
	function getconnection($config){
		$link = new mysqli($config['db_host'],$config['db_user'],$config['db_pass'],$config['db_name']);
		if($link->connect_error){
			die("连接失败：".$link->connect_error);
		}
		return $link;
	}