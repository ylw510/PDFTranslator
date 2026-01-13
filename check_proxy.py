#!/usr/bin/env python3
"""
检查代理配置和连接
"""
import socket
import sys

def check_proxy_port(host, port):
    """检查代理端口是否可用"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        return False

def main():
    print("=" * 50)
    print("代理连接检查")
    print("=" * 50)

    # 常见代理端口
    common_ports = [7890, 1080, 8080, 8118, 10808, 10809]

    print("\n检查常见代理端口...")
    available_proxies = []

    for port in common_ports:
        if check_proxy_port('127.0.0.1', port):
            print(f"✅ 端口 {port} 可用")
            available_proxies.append(f"http://127.0.0.1:{port}")
        else:
            print(f"❌ 端口 {port} 不可用")

    if available_proxies:
        print(f"\n找到可用的代理: {available_proxies[0]}")
        print(f"\n请在 .env 文件中设置:")
        print(f"OPENAI_PROXY={available_proxies[0]}")
    else:
        print("\n⚠️  未找到可用的代理服务器")
        print("\n解决方案:")
        print("1. 启动你的代理软件（如 Clash、V2Ray 等）")
        print("2. 或者移除 .env 中的 OPENAI_PROXY 配置（如果网络可以直接访问OpenAI）")
        print("3. 或者使用其他代理地址")

if __name__ == "__main__":
    main()
