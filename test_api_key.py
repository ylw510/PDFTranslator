#!/usr/bin/env python3
"""
测试 OpenAI API Key 是否有效
"""
import sys
from openai import OpenAI
from config import Config

def test_api_key():
    """测试API密钥"""
    print("=" * 60)
    print("OpenAI API Key 测试")
    print("=" * 60)

    # 检查API密钥是否配置
    if not Config.OPENAI_API_KEY:
        print("❌ 错误: 未设置 OPENAI_API_KEY")
        print("请在 .env 文件中设置 OPENAI_API_KEY")
        return False

    # 显示API密钥预览
    key_preview = Config.OPENAI_API_KEY[:10] + "..." + Config.OPENAI_API_KEY[-4:] if len(Config.OPENAI_API_KEY) > 14 else "***"
    print(f"\nAPI密钥预览: {key_preview}")
    print(f"模型: {Config.OPENAI_MODEL}")
    print(f"超时设置: {Config.OPENAI_TIMEOUT}秒")

    # 初始化客户端
    print("\n" + "-" * 60)
    print("1. 初始化 OpenAI 客户端...")
    print("-" * 60)

    try:
        client_kwargs = {
            'api_key': Config.OPENAI_API_KEY,
            'timeout': float(Config.OPENAI_TIMEOUT)
        }

        # 如果设置了代理
        if Config.OPENAI_PROXY:
            import httpx
            import socket
            print(f"检测到代理配置: {Config.OPENAI_PROXY}")

            # 检查代理是否可用
            try:
                proxy_url = Config.OPENAI_PROXY
                if proxy_url.startswith('http://'):
                    host_port = proxy_url.replace('http://', '').split(':')
                    if len(host_port) == 2:
                        host, port = host_port[0], int(host_port[1])
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(2)
                        result = sock.connect_ex((host, port))
                        sock.close()
                        if result == 0:
                            timeout_obj = httpx.Timeout(Config.OPENAI_TIMEOUT, connect=5.0)
                            client_kwargs['http_client'] = httpx.Client(
                                proxy=proxy_url,
                                timeout=timeout_obj
                            )
                            print("✅ 代理可用，将使用代理")
                        else:
                            print("⚠️  代理端口不可用，将尝试直接连接")
            except Exception as e:
                print(f"⚠️  代理配置检查失败: {e}，将尝试直接连接")

        client = OpenAI(**client_kwargs)
        print("✅ 客户端初始化成功")

    except Exception as e:
        print(f"❌ 客户端初始化失败: {e}")
        return False

    # 测试API调用
    print("\n" + "-" * 60)
    print("2. 发送测试请求...")
    print("-" * 60)

    try:
        print("正在发送请求（这可能需要几秒钟）...")

        response = client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=[
                {"role": "user", "content": "Say 'Hello' in one word."}
            ],
            max_tokens=10,
            timeout=Config.OPENAI_TIMEOUT
        )

        result = response.choices[0].message.content.strip()

        print("✅ API调用成功！")
        print(f"\n响应内容: {result}")
        print(f"使用的模型: {response.model}")
        print(f"Token使用: {response.usage.total_tokens if hasattr(response, 'usage') else 'N/A'}")

        return True

    except Exception as e:
        error_msg = str(e)
        error_type = type(e).__name__

        print(f"\n❌ API调用失败")
        print(f"错误类型: {error_type}")
        print(f"错误信息: {error_msg}")

        # 提供详细的错误分析
        print("\n" + "-" * 60)
        print("错误分析:")
        print("-" * 60)

        if "401" in error_msg or "Unauthorized" in error_msg or "Invalid" in error_msg:
            print("🔴 API密钥无效或已过期")
            print("   解决方案:")
            print("   1. 检查API密钥是否正确")
            print("   2. 登录 OpenAI 官网检查API密钥状态")
            print("   3. 确认API密钥是否有足够的额度")

        elif "429" in error_msg or "rate limit" in error_msg.lower():
            print("🟡 API调用频率超限")
            print("   解决方案:")
            print("   1. 等待一段时间后重试")
            print("   2. 检查API使用额度")

        elif "Connection" in error_type or "connection" in error_msg.lower() or "timeout" in error_msg.lower():
            print("🟡 网络连接问题")
            print("   解决方案:")
            print("   1. 检查网络连接")
            print("   2. 如果在中国大陆，配置代理:")
            print("      OPENAI_PROXY=http://127.0.0.1:7890")
            print("   3. 增加超时时间: OPENAI_TIMEOUT=30")

        elif "503" in error_msg or "Service Unavailable" in error_msg:
            print("🟡 OpenAI服务暂时不可用")
            print("   解决方案:")
            print("   1. 等待一段时间后重试")
            print("   2. 检查 OpenAI 服务状态")

        else:
            print("🟡 其他错误")
            print("   请查看上面的错误信息进行排查")

        return False

def main():
    print("\n")
    success = test_api_key()

    print("\n" + "=" * 60)
    if success:
        print("✅ 测试通过！API密钥有效，可以正常使用。")
    else:
        print("❌ 测试失败，请根据上述建议修复问题。")
    print("=" * 60 + "\n")

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
