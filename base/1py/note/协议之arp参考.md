### ARP协议结构

ARP（Address Resolution Protocol）用于将IP地址解析为MAC地址。

**ARP报文格式：**

```
0                   1                   2                   3
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|        硬件类型                |        协议类型                |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| 硬件地址长度  | 协议地址长度  |          操作码                |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                       发送方MAC地址                           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|        发送方MAC地址          |        发送方IP地址            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                        发送方IP地址                           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                        目标MAC地址                           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|        目标MAC地址            |        目标IP地址              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                        目标IP地址                            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

**字段说明：**

- 硬件类型：1（以太网）
- 协议类型：0x0800（IPv4）
- 硬件地址长度：6（MAC地址长度）
- 协议地址长度：4（IP地址长度）
- 操作码：1（请求），2（应答）

### Python原生实现ARP扫描

```py
import socket
import struct
import binascii
import fcntl
import os
import time
from threading import Thread, Lock

class ARPScanner:
    def __init__(self):
        self.results = {}
        self.lock = Lock()
    
    def get_interface_ip(self, interface='eth0'):
        """获取指定网络接口的IP地址"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            return socket.inet_ntoa(fcntl.ioctl(
                s.fileno(),
                0x8915,  # SIOCGIFADDR
                struct.pack('256s', interface[:15].encode())
            )[20:24])
        except:
            return None
    
    def get_interface_mac(self, interface='eth0'):
        """获取指定网络接口的MAC地址"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            info = fcntl.ioctl(
                s.fileno(),
                0x8927,  # SIOCGIFHWADDR
                struct.pack('256s', interface[:15].encode())
            )
            return ':'.join(f'{b:02x}' for b in info[18:24])
        except:
            return None
    
    def create_arp_request(self, source_ip, source_mac, target_ip):
        """创建ARP请求包"""
        
        # 以太网帧头
        target_mac = b'\xff\xff\xff\xff\xff\xff'  # 广播地址
        source_mac_bytes = binascii.unhexlify(source_mac.replace(':', ''))
        eth_type = b'\x08\x06'  # ARP类型
        
        # ARP数据包
        hardware_type = b'\x00\x01'  # 以太网
        protocol_type = b'\x08\x00'  # IPv4
        hardware_size = b'\x06'      # MAC地址长度
        protocol_size = b'\x04'      # IP地址长度
        opcode = b'\x00\x01'         # 请求
        
        # 转换IP地址为字节
        source_ip_bytes = socket.inet_aton(source_ip)
        target_ip_bytes = socket.inet_aton(target_ip)
        
        # 构建ARP包
        arp_packet = (
            hardware_type + protocol_type + hardware_size + protocol_size +
            opcode + source_mac_bytes + source_ip_bytes +
            b'\x00\x00\x00\x00\x00\x00' + target_ip_bytes
        )
        
        # 构建完整的以太网帧
        eth_frame = target_mac + source_mac_bytes + eth_type + arp_packet
        
        return eth_frame
    
    def parse_arp_response(self, data):
        """解析ARP响应"""
        # 解析以太网帧头 (14字节)
        dest_mac = data[0:6]
        src_mac = data[6:12]
        eth_type = data[12:14]
        
        if eth_type != b'\x08\x06':  # 不是ARP包
            return None
        
        # 解析ARP包 (从第14字节开始)
        arp_data = data[14:42]
        
        # 解析ARP字段
        (
            hardware_type, protocol_type, hardware_size, protocol_size,
            opcode, sender_mac, sender_ip, target_mac, target_ip
        ) = struct.unpack('!2s2s1s1s2s6s4s6s4s', arp_data)
        
        # 检查是否是ARP应答 (opcode = 2)
        if opcode != b'\x00\x02':
            return None
        
        # 转换MAC地址为字符串
        sender_mac_str = ':'.join(f'{b:02x}' for b in sender_mac)
        
        # 转换IP地址为字符串
        sender_ip_str = socket.inet_ntoa(sender_ip)
        
        return sender_ip_str, sender_mac_str
    
    def send_arp_request(self, interface, target_ip, source_ip, source_mac):
        """发送ARP请求"""
        try:
            # 创建原始套接字
            sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
            sock.bind((interface, 0))
            
            # 创建ARP请求包
            arp_request = self.create_arp_request(source_ip, source_mac, target_ip)
            
            # 发送ARP请求
            sock.send(arp_request)
            
            # 设置超时
            sock.settimeout(2)
            
            # 等待响应
            start_time = time.time()
            while time.time() - start_time < 2:
                try:
                    data = sock.recv(1024)
                    result = self.parse_arp_response(data)
                    if result:
                        ip, mac = result
                        if ip == target_ip:
                            with self.lock:
                                self.results[ip] = mac
                            break
                except socket.timeout:
                    continue
            
            sock.close()
            
        except Exception as e:
            print(f"发送ARP请求到 {target_ip} 时出错: {e}")
    
    def arp_scan_network(self, network, interface='eth0'):
        """扫描整个网络"""
        print(f"开始ARP扫描网络: {network}")
        
        # 获取本机信息
        source_ip = self.get_interface_ip(interface)
        source_mac = self.get_interface_mac(interface)
        
        if not source_ip or not source_mac:
            print("无法获取网络接口信息")
            return
        
        print(f"本机IP: {source_ip}, MAC: {source_mac}")
        
        # 生成要扫描的IP列表
        import ipaddress
        net = ipaddress.ip_network(network, strict=False)
        target_ips = [str(ip) for ip in net.hosts()]
        
        threads = []
        
        # 为每个IP创建线程
        for ip in target_ips:
            thread = Thread(target=self.send_arp_request, args=(interface, ip, source_ip, source_mac))
            threads.append(thread)
            thread.start()
            
            # 控制并发数量
            if len(threads) >= 50:
                for t in threads:
                    t.join()
                threads = []
        
        # 等待所有线程完成
        for thread in threads:
            thread.join()
        
        # 显示结果
        print(f"\n扫描完成! 发现 {len(self.results)} 个活跃设备:")
        for ip, mac in sorted(self.results.items()):
            print(f"  {ip}\t{mac}")

# 使用示例
if __name__ == "__main__":
    scanner = ARPScanner()
    
    # 扫描本地网络 (需要根据实际情况修改)
    # 注意: 需要root权限运行
    if os.geteuid() != 0:
        print("请使用root权限运行此脚本")
    else:
        # 替换为你的网络接口和网络段
        scanner.arp_scan_network("192.168.1.0/24", "eth0")
```

