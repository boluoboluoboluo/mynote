###  wsdl接口通信示例

```php
//获取证书接口调试，获取z证书串
public function get_token(){
    libxml_disable_entity_loader(false);
    $baseparams = $this->get_params();   //获取基本参数
    $url = $baseparams['url'];
    
    $client=new SoapClient($url);

    $data['IdentityId'] = $baseparams['IdentityId'];                    //中介账号
    $data['Password'] = $baseparams['Password'];                        //密码
    $data['MacAddress'] = $baseparams['MacAddress'];                    //mac地址

    $param['requestJson'] = json_encode($data);

    $re = $client->CreateToken($param);				//对方接口提供的方法
    $token_result = $re->CreateTokenResult;			//对方接口返回的字段对象数据

    $token = '';
    if($token_result){
        $re_arr = json_decode($token_result,true);
        if($re_arr['Content']){
            $token = $re_arr['Content']['TokenValue'];
        }
    }
    return $token;
}
//获取相关参数
private function get_params(){
    // $baseparams['url'] = "https://xxx.com/zj/xxx.xx?wsdl";     //测试地址
    $baseparams['IdentityId'] = "test";               //中介账号
    // $baseparams['Password'] = "123456";                 //密码    测试
    $baseparams['MacAddress'] = "9C-B6-D0-B7-8-37";    //mac地址
    return $baseparams;
}
```



### wsdl接口通信示例2

```php
public function wsdl_lhhos_test(){
		$url = "http://x.x.x.x:xx/xxx/services/xxx?wsdl";
	    libxml_disable_entity_loader(false);
	    $client=new SoapClient($url,array('trace'=>true));

	    var_dump($client->__getFunctions());//打印暴露的方法
	    echo "<br><br>";
	    var_dump($client->__getTypes());//打印对应方法的参数和参数类型
	}
```

打印暴露的方法，和参数及参数类型 示例：

```sh
 [29]=> string(74) "ExamOrderRegisterResponse ExamOrderRegister(ExamOrderRegister $parameters)"
 
 [58]=> string(41) "struct ExamOrderRegister { string XML; }" [59]=> string(52) "struct ExamOrderRegisterResponse { string String; }" 
 
 
 #说明
 由上面可知，方法为ExamOrderRegister，参数为键为XML的关联数组
```

请求代码示例：

```php
public function wsdl_lhhos_test2(){
    libxml_disable_entity_loader(false);
    $url = "http://x.x.x.x:xx/xxx/services/xxx?wsdl";
	    
    $client=new SoapClient($url);

    $xml = "<?xml version=\"1.0\" encoding=\"utf-8\"?>".
                "<inxml><orderId>111111</orderId>".
                "<payTime>2021-08-10 12:30:00</payTime>".
            "</inxml>";

    $param["XML"] = $xml;
    $re = $client->ExamOrderRegister($param);				//对方接口提供的方法
    //var_dump($re);
   	$xml_str = $re->String;
    $xml_obj = simplexml_load_string($xml_str); 	
    $code = (string) $xml_obj->code;
    $msg = (string) $xml_obj->msg;
    if(!$xml_obj){
        echo "接口返回异常...";
    }
    if($code != "0"){
        echo "接口返回异常：".$msg;
    }
    $arr = [];
    foreach($xml_obj->returnContents->returnContent as $content){
        $tmp = [];
        foreach($content as $k=>$v){
            $tmp[$k] = (string)$v;	//参数名和
        }
    }
    var_dump($arr);
}

```





