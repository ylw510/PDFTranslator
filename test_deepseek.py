#!/usr/bin/env python3
"""
测试 DeepSeek API 连接
"""
from config import Config
from translator import PDFTranslator

print("=" * 60)
print("DeepSeek API 测试")
print("=" * 60)

print(f"\nAPI提供商: {Config.API_PROVIDER}")
print(f"API密钥: {'已设置' if Config.API_KEY else '未设置'}")
if Config.API_KEY:
    key_preview = Config.API_KEY[:10] + "..." + Config.API_KEY[-4:] if len(Config.API_KEY) > 14 else "***"
    print(f"密钥预览: {key_preview}")
print(f"模型: {Config.MODEL}")
print(f"Base URL: {Config.BASE_URL or '默认'}")
print(f"超时: {Config.TIMEOUT}秒")

if not Config.API_KEY:
    print("\n❌ 错误: 未设置 API_KEY")
    print("请在 .env 文件中设置 API_KEY=your_deepseek_api_key")
    exit(1)

try:
    print("\n初始化翻译器...")
    translator = PDFTranslator()
    
    print("\n发送测试请求...")
    result = translator.translate_text("Hello", source_lang="英文", target_lang="中文")
    
    print(f"\n✅ 测试成功！")
    print(f"翻译结果: {result}")
    
except Exception as e:
    print(f"\n❌ 测试失败: {e}")
    print("\n请检查:")
    print("1. API_KEY 是否正确")
    print("2. 网络连接是否正常")
    print("3. DeepSeek API 是否可用")
    exit(1)
