##### aes加密

```php
 public function dh_aes_test(){
        $str = "xxxxxxxxxxxxxxxxxx";//待加密串
        $appKey = "CaVE*******";	//密钥
        $iv = "010203060708";		//偏移量
        
        //第2个参数：可通过openssl_get_cipher_methods() 获取有效加密方式列表。
        //第4个参数：options 是以下标记的按位或： OPENSSL_RAW_DATA 、 OPENSSL_ZERO_PADDING。
     	//（128位默认使用pkcs5padding填充，256位默认使用pkcs7padding填充）
        $aes_str openssl_encrypt($str,'aes-128-cbc',$appKey,OPENSSL_RAW_DATA,$iv);
     	//$re_str = bin2hex($aes_str);	//转16进制
		$re_str = base64_encode($aes_str);	//base64编码
     
     	return $re_str;
    }
```

##### aes解密

函数：`openssl_decrypt` 。其他同上

