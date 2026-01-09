### curl方式发送wsdl请求

> 1.准备
>
> 2.发送请求

案例描述：发送请求到nginx服务器，nginx转发到wsdl服务器，获取响应xml数据，并将xml转换为数组



#### ~~soap方式失败说明~~：

~~说明：本来是通过使用soap扩展，结果一直报wrong version错误，调试未果就放弃了。~~

~~相关代码记录如下：~~

```php
public function wsdl_base_8000(){
    $url = "http://a.a.a.a:8000/xxx/xxx/xx.xx.xx.CLS?WSDL=1";	//接口地址
    libxml_disable_entity_loader(false);
    $client=new SoapClient($url,array('trace'=>true));

    var_dump($client->__getFunctions());//打印暴露的方法
    echo "<br><br>";
    var_dump($client->__getTypes());//打印对应方法的参数和参数类型
}
```

~~调用接口暴露的方法，请求数据：~~

```php
 public function wsdl_test_8000(){
        libxml_disable_entity_loader(false);
       
        $url = "http://a.a.a.a:8000/xxx/xxx/xx.xx.xx.CLS?WSDL=1";
        $client=new SoapClient($url,array('trace'=>true,'cache_wsdl'=>0,'encoding'=>'UTF-8','soap_version'=>SOAP_1_2));
        // $client=new SoapClient($url,array('trace'=>true,'cache_wsdl'=>0,'encoding'=>'UTF-8'));
        $client->__setLocation($url);	//如果报cannot connect to host，此句有效
        try{
            //参数
            $param = array(
                        "messageCode"=>"123",
                        "inputContent"=>"<Request><levelId>1</levelId><locId>123</locId><sexDesc/></Request>"
                    );
            // $re = $client->__soapCall("SendMessageInfo",$param);             //对方接口提供的方法
            $re = $client->SendMessageInfo($param);             //对方接口提供的方法
            echo json_encode($re);
        }catch(SoapFault $f){
            var_dump($client->__getLastResponse());
            echo "<br><br>";
            var_dump($client->__getLastResponseHeaders());
            echo "<br><br>";
            echo "Error Message: {$f->getMessage()}";
        }
    }
```

~~上述操作失败，未找到原因，泪目~~



#### 1. 准备

假设nginx服务器ip是：`a.a.a.a`，wsdl服务器ip为：`b.b.b.b`

由于本案例是用nginx转发，所以先配置nginx:

```nginx
server {
  listen   8000;
  server_name 127.0.0.1;
  root /var/www/html;
  index index.html index.php index.htm;
  add_header X-Frame-Options SAMEORIGIN;
  location / {
    proxy_pass  http://b.b.b.b;
    proxy_http_version 1.1;
    proxy_set_header Connection "";
    proxy_set_header Host           $http_host;
    #proxy_set_header Host           b.b.b.b:80;
    proxy_redirect off;
    proxy_set_header X-Real-IP      $remote_addr;
    proxy_set_header X-Forwarded-For      $proxy_add_x_forwarded_for;
  }
```

配置后，可通过浏览器访问`http://a.a.a.a:8000`，获取wsdl服务器信息如下：

```html
<definitions xmlns="http://schemas.xmlsoap.org/wsdl/" xmlns:soap-enc="http://schemas.xmlsoap.org/soap/encoding/" xmlns:mime="http://schemas.xmlsoap.org/wsdl/mime/" xmlns:s="http://www.w3.org/2001/XMLSchema" xmlns:s0="http://www.服务器.com.cn" xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/" xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" targetnamespace="http://www.服务器.com.cn">
    <types>
        <s:schema elementformdefault="qualified" targetnamespace="http://www.服务器.com.cn">
            <s:element name="SendMessageInfo">
                <s:complextype>
                    <s:sequence>
                        <s:element minoccurs="0" name="messageCode" type="s:string">
                        <s:element minoccurs="0" name="inputContent" type="s:string">
                    </s:element></s:element></s:sequence>
                </s:complextype>
            </s:element>
            <s:element name="SendMessageInfoResponse">
                <s:complextype>
                    <s:sequence>
                        <s:element name="SendMessageInfoResult" type="s:string">
                    </s:element></s:sequence>
                </s:complextype>
            </s:element>
        </s:schema>
    </types>
    <message name="SendMessageInfoSoapIn">
        <part name="parameters" element="s0:SendMessageInfo">
    </part></message>
    <message name="SendMessageInfoSoapOut">
        <part name="parameters" element="s0:SendMessageInfoResponse">
    </part></message>
    <porttype name="PUB0018Soap">
        <operation name="SendMessageInfo">
            <input message="s0:SendMessageInfoSoapIn">
            <output message="s0:SendMessageInfoSoapOut">
        </output></operation>
    </porttype>
    <binding name="PUB0018Soap" type="s0:PUB0018Soap">
        <soap:binding transport="http://schemas.xmlsoap.org/soap/http" style="document">
        <operation name="SendMessageInfo">
            <!-- 说明：下面这个地址是curl请求header里需要填写的soapaction地址-->
            <soap:operation soapaction="http://www.服务器.com.cn/xxx/xxx/xx.xx.xx.SendMessageInfo" style="document">
            <input>
                <soap:body use="literal">
            <output>
                <soap:body use="literal">
            </soap:body></output>
        </soap:body></soap:operation></operation>
    </soap:binding></binding>
    <service name="PUB0018">
        <port name="PUB0018Soap" binding="s0:PUB0018Soap">
            <!-- 说明：下面这个地址就是访问的服务地址-->
            <soap:address location="http://a.a.a.a/xxx/xxx/xx.xx.xx.cls">
        </soap:address></port>
    </service>
</definitions>
```

通过阅读上述信息，可发送请求，注意看我上面代码备注的说明

如条件允许，可通过`soapui`等工具，先发测试请求



#### 2. 发送请求

请求代码如下：

```php
public function wsdl_test3(){
    	header("content-type: text/html,charset:utf-8");

        $url = "http://a.a.a.a:8000/xxx/xxx/xx.xx.xx.CLS";
    	//请求的xml参数
        $output = '<?xml version="1.0" encoding="UTF-8" ?>'.
            		'<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" '.
            			'xmlns:dhcc="http://www.服务器.com.cn">'.
                    '<soapenv:Header/>'.
                    '<soapenv:Body>'.
                        '<dhcc:SendMessageInfo>'.
                            '<!--Optional:-->'.
                            '<dhcc:messageCode>123</dhcc:messageCode>'.
                            '<!--Optional:-->'.
                            '<dhcc:inputContent><![CDATA[<Request>'.
                                '<levelId>1</levelId>'.
                                '<locId>123</locId>'.
                                '<sexDesc/>'.
                                '</Request>'.
                                ']]></dhcc:inputContent>'.
                        '</dhcc:SendMessageInfo>'.
                    '</soapenv:Body>'.
                    '</soapenv:Envelope>';
		//请求头
        $headers = array(
                    'Host: a.a.a.a:8000',
                    'Content-Type: text/xml;charset=UTF-8',
                    'Accept: text/xml',
                    'Connection: Keep-Alive',
                    "Cache-Control: no-cache",
                    "Pragma: no-cache",
                    "Content-Length:".strlen($output),
                   'SOAPAction: "http://www.服务器.com.cn/xxx.xxx/xx.xx.xx.SendMessageInfo"',		//此处留心
                   //'User-Agent: Apache-HttpClient/4.5.5 (Java/16.0.2)'
                ); //SOAPAction: your op URL

        $ch = curl_init();
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
        // curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, FALSE);
        curl_setopt($ch, CURLOPT_URL, $url);
        // curl_setopt($ch, CURLOPT_ENCODING, 'UTF-8');
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 60);
        curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $output);
        // curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_BASIC);
        
        //---说明，此处为curl调试代码 start
        // curl_setopt($ch, CURLOPT_VERBOSE, 1);   //调试开关
        // $filename = date('Ymd');
        // $path = ROOT_PATH."你的log目录/".$filename.".log";
        // curl_setopt($ch, CURLOPT_STDERR, fopen($path, 'a')); // curl debug
        //---curl调试代码 end

        $data = curl_exec($ch);
        if($data === false){
            //echo curl_error($ch);	//如果出错，记录调试
        }else{
            //将返回的数据的CDATA部分用正则去掉
            $str2 = preg_replace("/<!\[CDATA\[/",'',$data);
            $str3 = preg_replace("/\]\]>/",'',$str2);
			//转成xml对象
            $xml = simplexml_load_string($str3); 
			//通过xml节点，层层获取子节点数据
            //说明：带冒号的节点如soapenv:Envelope，需要通过children(xmlns属性内容)访问
            $re =  $xml->children("http://schemas.xmlsoap.org/soap/envelope/")->Body->children("http://www.服务器.com.cn")->SendMessageInfoResponse->SendMessageInfoResult->Response;
            
			//节点都是xmlobject,仍需类型转换
            $code = (string) $re->ResultCode;
            $desc = (string) $re->ResultDesc;
            $arr = [];
            //xml列表数据转数组
            //特别说明，也可以通过json_decode(json_encode($xml),true)方式转数组，不过如果有中文，可能会出现乱码
            //所以我采用的是如下方法
            foreach($re->ResultList->ExaminationPackages as $item){
                $tmp = [];
                foreach($item as $k=>$v){
                    $tmp[$k] = (string)$v;	//参数名和值
                }
                array_push($arr,$tmp);
            }
            echo $code;
            echo $desc;
            var_dump($arr);
        }
        curl_close($ch);
    }
```

补充案例的响应数据：

```html
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:s="http://www.w3.org/2001/XMLSchema">
   <SOAP-ENV:Body>
      <SendMessageInfoResponse xmlns="http://www.服务器.com.cn">
         <SendMessageInfoResult><![CDATA[<Response><ResultCode>0</ResultCode><ResultDesc>成功</ResultDesc><ResultList><ExaminationPackages><packageId>38</packageId><packageDesc>F1Y-FB(含妇科常规检查)</packageDesc><packageAmt>1187.9</packageAmt><ordSetsId>194</ordSetsId><levelDesc>健康体检</levelDesc><levelId>1</levelId><giFlag>个人</giFlag><sexDesc>女</sexDesc><ordSetsType>N</ordSetsType><locId>526</locId><locDesc>体检科</locDesc><originAmt>1187.9</originAmt><sort>10</sort><minAge>18</minAge><maxAge>49</maxAge></ExaminationPackages><ExaminationPackages><packageId>39</packageId><packageDesc>F1N(不含妇科常规检查)</packageDesc><packageAmt>799.9</packageAmt><ordSetsId>196</ordSetsId><levelDesc>健康体检</levelDesc><levelId>1</levelId><giFlag>个人</giFlag><sexDesc>女</sexDesc><ordSetsType>N</ordSetsType><locId>526</locId><locDesc>体检科</locDesc><originAmt>799.9</originAmt><sort>20</sort><minAge>18</minAge><maxAge>49</maxAge></ExaminationPackages><ExaminationPackages><packageId>40</packageId><packageDesc>F2Y-FB(含妇科常规检查)</packageDesc><packageAmt>1217.9</packageAmt><ordSetsId>198</ordSetsId><levelDesc>健康体检</levelDesc><levelId>1</levelId><giFlag>个人</giFlag><sexDesc>女</sexDesc><ordSetsType>N</ordSetsType><locId>526</locId><locDesc>体检科</locDesc><originAmt>1217.9</originAmt><sort>30</sort><minAge>50</minAge><maxAge>65</maxAge></ExaminationPackages></ResultList></Response>]]></SendMessageInfoResult>
      </SendMessageInfoResponse>
   </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
```

