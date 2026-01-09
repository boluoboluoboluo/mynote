### ICMP协议结构

ICMP（Internet Control Message Protocol）是网络层的控制协议，用于在主机和路由器之间传递控制信息。

**ICMP报文格式：**

```
0                   1                   2                   3
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|    类型(Type)  |    代码(Code)   |          校验和(Checksum)     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                            数据部分                            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

**常见类型：**

- 类型 0: Echo Reply（回显应答）
- 类型 8: Echo Request（回显请求）
- 类型 3: Destination Unreachable（目标不可达）
- 类型 11: Time Exceeded（超时）

### Python原生实现ICMP Ping

```py
import socket
import struct
import time
import select
import os

def calculate_checksum(data):
    """计算ICMP校验和"""
    if len(data) % 2:
        data += b'\x00'
    
    checksum = 0
    for i in range(0, len(data), 2):
        word = (data[i] << 8) + data[i + 1]
        checksum += word
    
    checksum = (checksum >> 16) + (checksum & 0xffff)
    checksum += (checksum >> 16)
    return ~checksum & 0xffff

def create_icmp_packet(identifier, sequence, payload_size=56):
    """创建ICMP Echo Request数据包"""
    # ICMP头: 类型(8), 代码(0), 校验和(0), 标识符, 序列号
    header = struct.pack('!BBHHH', 8, 0, 0, identifier, sequence)
    
    # 数据部分（时间戳 + 填充数据）
    timestamp = struct.pack('!d', time.time())
    padding = b'\x00' * (payload_size - len(timestamp))
    data = timestamp + padding
    
    # 计算校验和
    checksum = calculate_checksum(header + data)
    
    # 重新打包包含正确校验和的头部
    header = struct.pack('!BBHHH', 8, 0, checksum, identifier, sequence)
    
    return header + data

def parse_icmp_response(data, identifier):
    """解析ICMP响应"""
    # 跳过IP头 (20字节)
    icmp_header = data[20:28]
    type, code, checksum, packet_id, sequence = struct.unpack('!BBHHH', icmp_header)
    
    if type == 0 and packet_id == identifier:  # Echo Reply且标识符匹配
        timestamp = struct.unpack('!d', data[28:36])[0]
        return sequence, time.time() - timestamp
    return None

def ping(host, timeout=2, count=4):
    """执行Ping操作"""
    try:
        dest_addr = socket.gethostbyname(host)
    except socket.gaierror:
        print(f"无法解析主机: {host}")
        return
    
    # 创建原始套接字 (需要管理员权限)
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    except PermissionError:
        print("需要管理员/root权限来创建原始套接字")
        return
    
    identifier = os.getpid() & 0xFFFF
    print(f"正在Ping {host} [{dest_addr}]:")
    
    sent = 0
    received = 0
    rtt_times = []
    
    for sequence in range(count):
        # 创建并发送ICMP包
        packet = create_icmp_packet(identifier, sequence)
        send_time = time.time()
        sock.sendto(packet, (dest_addr, 0))
        sent += 1
        
        # 等待响应
        ready = select.select([sock], [], [], timeout)
        if ready[0]:
            recv_time = time.time()
            try:
                data, addr = sock.recvfrom(1024)
                result = parse_icmp_response(data, identifier)
                if result:
                    sequence_num, rtt = result
                    rtt_ms = rtt * 1000
                    rtt_times.append(rtt_ms)
                    received += 1
                    print(f"来自 {addr[0]} 的回复: 字节={len(data)-28} 时间={rtt_ms:.2f}ms")
                else:
                    print("收到不匹配的ICMP包")
            except socket.error:
                print("接收数据时出错")
        else:
            print("请求超时。")
        
        time.sleep(1)  # 每次ping之间间隔1秒
    
    sock.close()
    
    # 统计信息
    if received > 0:
        print(f"\n{host} 的 Ping 统计信息:")
        print(f"    数据包: 已发送 = {sent}, 已接收 = {received}, 丢失 = {sent - received} ({(sent-received)/sent*100:.0f}% 丢失)")
        print(f"往返行程的估计时间(以毫秒为单位):")
        print(f"    最短 = {min(rtt_times):.2f}ms，最长 = {max(rtt_times):.2f}ms，平均 = {sum(rtt_times)/len(rtt_times):.2f}ms")
    else:
        print(f"\n{host} 的 Ping 统计信息:")
        print(f"    数据包: 已发送 = {sent}, 已接收 = {received}, 丢失 = {sent - received} (100% 丢失)")

# 使用示例
if __name__ == "__main__":
    ping("google.com")
```

