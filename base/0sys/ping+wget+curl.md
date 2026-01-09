##### 网络传输

##### ping

|        参数         | 详解                                                         |
| :-----------------: | :----------------------------------------------------------- |
|         -a          | Audible ping.                                                |
|         -A          | 自适应ping，根据ping包往返时间确定ping的速度；               |
|         -b          | 允许ping一个广播 地址；                                      |
|         -B          | 不允许ping改变包头的源地址；                                 |
|    **-c count**     | ping指定次数后停止ping；                                     |
|         -d          | 使用Socket的SO_DEBUG功能；                                   |
|    -F flow_label    | 为ping回显请求分配一个20位的“flow label”，如果未设置，内核会为ping随机分配； |
|       **-f**        | 极限检测，快速连续ping一台主机，ping的速度达到100次每秒；    |
|     -i interval     | 设定间隔几秒发送一个ping包，默认一秒ping一次；               |
|    -I interface     | 指定网卡接口、或指定的本机地址送出数据包；                   |
|     -l preload      | 设置在送出要求信息之前，先行发出的数据包；                   |
|         -L          | 抑制组播报文回送，只适用于[ping](http://aiezu.com/article/linux_ping_command.html)的目标为一个组播地址 |
|         -n          | 不要将ip地址转换成主机名；                                   |
|     -p pattern      | 指定填充ping数据包的十六进制内容，在诊断与数据有关的网络错误时这个选项就非常有用，如：“-p ff”； |
|         -q          | 不显示任何传送封包的信息，只显示最后的结果                   |
|       -Q tos        | 设置Qos(Quality of Service)，它是ICMP数据报相关位；可以是十进制或十六进制数，详见rfc1349和rfc2474文档； |
|         -R          | 记录ping的路由过程(IPv4 only)； 注意：由于IP头的限制，最多只能记录9个路由，其他会被忽略； |
|         -r          | 忽略正常的路由表，直接将数据包送到远端主机上，通常是查看本机的网络接口是否有问题；如果主机不直接连接的网络上，则返回一个错误。 |
|      -S sndbuf      | Set socket sndbuf. If not specified, it is selected to buffer not more than one packet. |
|    -s packetsize    | 指定每次ping发送的数据字节数，默认为“56字节”+“28字节”的ICMP头，一共是84字节； 包头+内容不能大于65535，所以最大值为65507（linux:65507, windows:65500）； |
|       -t ttl        | 设置TTL(Time To Live)为指定的值。该字段指定IP包被路由器丢弃之前允许通过的最大网段数； |
| -T timestamp_option | 设置IP timestamp选项,可以是下面的任何一个： 　　'tsonly' (only timestamps) 　　'tsandaddr' (timestamps and addresses) 　　'tsprespec host1 [host2 [host3]]' (timestamp prespecified hops). |
|       -M hint       | 设置MTU（最大传输单元）分片策略。 可设置为： 　　'do'：禁止分片，即使包被丢弃； 　　'want'：当包过大时分片； 　　'dont'：不设置分片标志（DF flag）； |
|       -m mark       | 设置mark；                                                   |
|         -v          | 使ping处于verbose方式，它要ping命令除了打印ECHO-RESPONSE数据包之外，还打印其它所有返回的ICMP数据包； |
|         -U          | Print full user-to-user latency (the old behaviour). Normally ping prints network round trip time, which can be different f.e. due to DNS failures. |
|     -W timeout      | 以毫秒为单位设置ping的超时时间；                             |
|     -w deadline     | deadline；                                                   |



##### wget

```shell
#wget：从web下载文件
wget --spider URL	#测试下载链接
wget -P /usr/sf down_url	#下载到指定目录 
wget -O xxx.zip down_url	#指定文件名保存,(动态链接文件名不正确时使用此方式) 
wget -q down_url	#不显示执行过程
wget -c down_url	#断点续传
wget -b down_url	#后台下载，下载过程日志重定向到当前目录中的wget-log文件中，要查看下载状态，可以使用tail -f wget-log查看
wget -i download_list.txt	#下载多个文件，每个url单独一行
wget --limit-rate=1m down_url	#限制下载速度

wget -d http://example.com	#显示请求和响应信息
wget --post-data="key1=value1&key2=value2" http://example.com	#post请求

wget --header="Cookie: key=value" http://example.com	#设置cookie

#模拟下载
wget -U 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.43 Safari/537.36' https://download.redis.io/releases/redis-6.0.8.tar.gz
#伪装下载2
wget --user-agent="Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.204 Safari/534.16" http://www.coonote.com/testfile.zip
```

##### curl

```shell
curl：需安装
sudo apt update
sudo apt install curl
curl --version

#说明：如果出现依赖关系问题，提示 依赖: libcurl4 (= 7.64.0-4+deb10u3) 但是 7.74.0-1.3+deb11u1 正要被安装
解决方法：
sudo apt purge libcurl4
sudo apt install curl


curl url	#请求
curl -X POST https://www.example.com	#POST 请求。-X参数指定 HTTP 请求的方法。
curl -s url	#不显示请求内容的进度信息
curl url -o 1.txt	#把请求内容存储到1.txt
# -H 添加header
curl -H 'Accept-Language: en-US' https://google.com	#
curl -i https://www.example.com	#i参数打印出服务器回应的 HTTP 标头。
curl -I https://www.example.com	#只获取头部信息
curl -v https://www.example.com	#v参数输出通信的整个过程，用于调试。


# -A 指定用户代理
curl -A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36' https://google.com
curl -H 'User-Agent: php/1.0' https://google.com	#指定代理

curl -b 'foo=bar' https://google.com 	# 发送cookie
curl -c cookies.txt https://www.google.com	#将服务器返回的cookie写入cookies.txt

$ curl -d 'login=emma＆password=123'-X POST https://google.com/login	#发送post
$ curl -d 'login=emma' -d 'password=123' -X POST  https://google.com/login	#同上
#使用-d参数以后，HTTP 请求会自动加上标头Content-Type : application/x-www-form-urlencoded。并且会自动将请求转为 POST 方法，因此可以省略-X POST。
curl -d '@data.txt' https://google.com/login	#读取data.txt文件的内容，作为数据体向服务器发送。
curl --data-urlencode 'comment=hello world' https://google.com/login	#采用post发送，数据hello world之间有一个空格，需要进行 URL 编码。

curl -e 'https://google.com?q=example' https://www.example.com	#设置refer
curl -H 'Referer: https://google.com?q=example' https://www.example.com	#同上

#-F参数用来向服务器上传二进制文件。
curl -F 'file=@photo.png' https://google.com/profile	#命令会给 HTTP 请求加上标头Content-Type: multipart/form-data，然后将文件photo.png作为file字段上传。
curl -F 'file=@photo.png;type=image/png' https://google.com/profile	#指定 MIME 类型为image/png，否则 curl 会把 MIME 类型设为application/octet-stream。

curl -G -d 'q=kitties' -d 'count=20' https://google.com/search	#get请求
curl -u 'bob:12345' https://google.com/login	#u参数用来设置服务器认证的用户名和密码。

#-L参数会让 HTTP 请求跟随服务器的重定向。curl 默认不跟随重定向
curl -L -d 'tweet=hi' https://api.twitter.com/tweet

# -x指定 HTTP 请求的代理。
curl -x socks5://james:cats@myproxy.com:8080 https://www.example.com	#指定 HTTP 请求通过http://myproxy.com:8080的 socks5 代理发出。


```

