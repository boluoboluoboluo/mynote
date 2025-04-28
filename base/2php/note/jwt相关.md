#### jwt解密

> jwt版本："firebase/php-jwt": "^6.9"



##### composer安装php-jwt

```shell
composer require firebase/php-jwt
```

##### ~~旧版代码~~

```php
$jwt = JWT::encode($payload, $secretKey, 'HS256');
$decoded = JWT::decode($jwt, $secretKey, ['HS256']);
```

##### 当前版

```php
use \Firebase\JWT\JWT;
use Firebase\JWT\Key;

//jwt
public function jwt_test(){
    $key = "my_secret_key";		//密钥
    $payload = array(
        "id" => 1,
        "username" => "test",
        "iat" => time(),
        // "exp" => time() + 60*60*24	//有效期1天
        "exp" => time() + 1	//有效期1秒
    );
    $jwt = JWT::encode($payload,$key,'HS256');
    echo $jwt;
}

public function jwt_decode_test(){
    $jwt = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1dsfwefewfNiJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJ0ZXN0IiwiaWF0IjoxNjk5ODY3NDgzLCJleHAiOjE2OTk4Njc0ODR9.3USNV6vsL0BCPTDOMGNSptJerZSxA_M_-fglplC6xEA";
    $key = "my_secret_key";

    try{
        $decoded = JWT::decode($jwt, new Key($key, 'HS256'));
        // echo $decoded->username;
        // echo "<br>";
        // var_dump($decoded);
    } catch (\Firebase\JWT\ExpiredException $e) {
        echo "已过期";
    }catch(\Exception $e){
        echo "验证失败";
    }

        
}

```

##### 其他解密

不需要key

```php
$data = json_decode(base64_decode(str_replace('_', '/', str_replace('-','+',explode('.', $token)[1]))));
var_dump($data);	//解密后数据
```

