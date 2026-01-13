#!/usr/bin/env python3
"""
测试OpenAI API连接和配置
"""
import sys
from config import Config
from translator import PDFTranslator

def test_config():
    """测试配置加载"""
    print("=" * 50)
    print("1. 检查配置...")
    print("=" * 50)

    print(f"API提供商: {Config.API_PROVIDER.upper()}")
    print(f"API密钥: {'已设置' if Config.API_KEY else '未设置'}")
    if Config.API_KEY:
        # 只显示前10个字符和后4个字符
        key_preview = Config.API_KEY[:10] + "..." + Config.API_KEY[-4:] if len(Config.API_KEY) > 14 else "***"
        print(f"API密钥预览: {key_preview}")

    print(f"模型: {Config.MODEL}")
    print(f"目标语言: {Config.TARGET_LANGUAGE}")
    print(f"源语言: {Config.SOURCE_LANGUAGE}")
    print(f"超时时间: {Config.TIMEOUT}秒")
    print(f"代理设置: {Config.PROXY if Config.PROXY else '未设置'}")
    print(f"API地址: {Config.BASE_URL if Config.BASE_URL else '使用默认'}")

    if not Config.API_KEY:
        print("\n❌ 错误: API_KEY 未设置！")
        print("请在 .env 文件中设置 API_KEY")
        print(f"当前使用: {Config.API_PROVIDER.upper()}")
        if Config.API_PROVIDER == 'deepseek':
            print("获取DeepSeek API密钥: https://platform.deepseek.com")
        else:
            print("获取OpenAI API密钥: https://platform.openai.com")
        return False

    return True

def test_translator_init():
    """测试翻译器初始化"""
    print("\n" + "=" * 50)
    print("2. 测试翻译器初始化...")
    print("=" * 50)

    try:
        translator = PDFTranslator()
        print("✅ 翻译器初始化成功")
        return translator
    except Exception as e:
        print(f"❌ 翻译器初始化失败: {str(e)}")
        return None

def test_api_connection(translator):
    """测试API连接"""
    print("\n" + "=" * 50)
    print("3. 测试API连接（发送简单测试请求）...")
    print("=" * 50)

    if not translator:
        print("❌ 跳过：翻译器未初始化")
        return False

    try:
        # 发送一个非常简短的测试请求
        test_text = "Hello"
        print(f"测试文本: {test_text}")
        print("正在发送请求...")
        print(f"超时设置: {Config.TIMEOUT}秒")

        # 添加超时保护
        import signal

        def timeout_handler(signum, frame):
            raise TimeoutError("请求超时")

        # 设置信号处理（仅Unix系统）
        if hasattr(signal, 'SIGALRM'):
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(Config.TIMEOUT + 5)  # 比配置的超时时间多5秒

        try:
            result = translator.translate_text(test_text, source_lang="英文", target_lang="中文")

            if hasattr(signal, 'SIGALRM'):
                signal.alarm(0)  # 取消超时

            print(f"✅ API连接成功！")
            print(f"翻译结果: {result}")
            return True
        except TimeoutError:
            if hasattr(signal, 'SIGALRM'):
                signal.alarm(0)
            raise

    except Exception as e:
        error_msg = str(e)
        print(f"❌ API连接失败: {error_msg}")

        # 提供解决建议
        if "Connection" in error_msg or "connection" in error_msg.lower():
            print("\n💡 解决建议:")
            print("   1. 检查网络连接")
            print("   2. 如果在中国大陆，请在 .env 文件中设置代理:")
            print("      PROXY=http://127.0.0.1:7890")
            print("   3. 检查防火墙设置")
        elif "401" in error_msg or "Unauthorized" in error_msg:
            print("\n💡 解决建议:")
            print("   1. 检查API密钥是否正确")
            print("   2. 检查API密钥是否有效且有额度")
        elif "timeout" in error_msg.lower():
            print("\n💡 解决建议:")
            print("   1. 尝试增加超时时间: TIMEOUT=120")
            print("   2. 检查网络速度")
        elif "402" in error_msg or "Insufficient Balance" in error_msg or "余额不足" in error_msg:
            print("\n💡 解决建议:")
            print("   1. 账户余额不足，请充值")
            if Config.API_PROVIDER == 'deepseek':
                print("   2. 访问 https://platform.deepseek.com 充值")
            else:
                print("   2. 访问 https://platform.openai.com 充值")

        return False

def main():
    print("\n" + "=" * 50)
    print("PDF翻译器 - 连接测试")
    print("=" * 50 + "\n")

    # 测试配置
    if not test_config():
        sys.exit(1)

    # 测试初始化
    translator = test_translator_init()
    if not translator:
        sys.exit(1)

    # 测试连接
    success = test_api_connection(translator)

    print("\n" + "=" * 50)
    if success:
        print("✅ 所有测试通过！可以正常使用翻译功能。")
    else:
        print("❌ 测试失败，请根据上述建议修复问题。")
    print("=" * 50 + "\n")

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
