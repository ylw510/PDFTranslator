from openai import OpenAI
from config import Config
from typing import List, Dict
import json
import time

class PDFTranslator:
    """PDF翻译器，使用大语言模型进行翻译"""

    def __init__(self):
        if not Config.API_KEY:
            raise ValueError(f"请设置API_KEY环境变量（当前使用: {Config.API_PROVIDER}）")

        # 构建客户端配置
        # OpenAI客户端的timeout参数应该是数字（秒）或Timeout对象
        client_kwargs = {
            'api_key': Config.API_KEY,
            'timeout': float(Config.TIMEOUT)  # 确保是浮点数
        }

        # 设置API地址
        if Config.BASE_URL:
            client_kwargs['base_url'] = Config.BASE_URL
        elif Config.API_PROVIDER == 'deepseek':
            # DeepSeek默认base_url
            client_kwargs['base_url'] = 'https://api.deepseek.com'

        # 如果设置了代理
        if Config.OPENAI_PROXY:
            import httpx
            import socket
            # 检查代理是否可用
            try:
                # 解析代理URL获取端口
                proxy_url = Config.OPENAI_PROXY
                if proxy_url.startswith('http://'):
                    host_port = proxy_url.replace('http://', '').split(':')
                    if len(host_port) == 2:
                        host, port = host_port[0], int(host_port[1])
                        # 检查端口是否可连接（快速检查，2秒超时）
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(2)
                        result = sock.connect_ex((host, port))
                        sock.close()
                        if result == 0:
                            # 代理端口可连接，使用代理
                            # httpx的timeout需要是Timeout对象，设置连接超时和读取超时
                            timeout_obj = httpx.Timeout(
                                Config.TIMEOUT,  # 总超时时间
                                connect=5.0  # 连接超时5秒
                            )
                            client_kwargs['http_client'] = httpx.Client(
                                proxy=proxy_url,
                                timeout=timeout_obj,
                                limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
                            )
                        else:
                            # 代理不可用，跳过代理配置
                            print(f"⚠️  警告: 代理 {proxy_url} 端口不可用，将尝试直接连接")
            except Exception as e:
                # 代理配置解析失败，跳过代理
                print(f"⚠️  警告: 代理配置错误 ({str(e)})，将尝试直接连接")

        self.client = OpenAI(**client_kwargs)
        self.model = Config.MODEL
        self.provider = Config.API_PROVIDER
        self.target_language = Config.TARGET_LANGUAGE
        self.source_language = Config.SOURCE_LANGUAGE

        print(f"✅ 已初始化 {Config.API_PROVIDER.upper()} 客户端，模型: {self.model}")

    def translate_text(self, text: str, source_lang: str = None, target_lang: str = None) -> str:
        """
        翻译文本
        """
        source_lang = source_lang or self.source_language
        target_lang = target_lang or self.target_language

        prompt = f"""请将以下{source_lang}文本翻译成{target_lang}。要求：
1. 保持原文的格式和结构
2. 翻译准确、流畅
3. 如果是技术文档，保持专业术语的准确性

原文：
{text}

翻译结果："""

        max_retries = 3
        retry_delay = 2  # 重试延迟（秒）

        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": f"你是一位专业的{source_lang}到{target_lang}翻译专家。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    timeout=Config.TIMEOUT
                )

                return response.choices[0].message.content.strip()

            except Exception as e:
                error_msg = str(e)
                error_type = type(e).__name__

                # 如果是连接错误，提供更详细的提示
                if 'Connection' in error_type or 'connection' in error_msg.lower():
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay * (attempt + 1))  # 指数退避
                        continue
                    else:
                        raise Exception(
                            f"连接失败（已重试{max_retries}次）: {error_msg}\n"
                            f"提示：\n"
                            f"1. 检查网络连接是否正常\n"
                            f"2. 如果在中国大陆，可能需要配置代理（在.env中设置PROXY）\n"
                            f"3. 检查API密钥是否正确\n"
                            f"4. 尝试增加超时时间（在.env中设置TIMEOUT）"
                        )
                else:
                    # 其他错误直接抛出
                    raise Exception(f"翻译失败: {error_msg}")

        raise Exception("翻译失败：达到最大重试次数")

    def translate_pages(self, pages: List[Dict], chunk_size: int = 2000) -> List[Dict]:
        """
        翻译PDF页面，支持分块处理长文本
        """
        translated_pages = []

        for page_data in pages:
            original_text = page_data['text']

            # 如果文本太长，分块翻译
            if len(original_text) > chunk_size:
                translated_text = self._translate_long_text(original_text, chunk_size)
            else:
                translated_text = self.translate_text(original_text)

            translated_pages.append({
                'page': page_data['page'],
                'original': original_text,
                'translated': translated_text
            })

        return translated_pages

    def _translate_long_text(self, text: str, chunk_size: int) -> str:
        """
        处理长文本，分块翻译后合并
        """
        # 按段落分割
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""

        for para in paragraphs:
            if len(current_chunk) + len(para) < chunk_size:
                current_chunk += para + '\n\n'
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = para + '\n\n'

        if current_chunk:
            chunks.append(current_chunk.strip())

        # 翻译每个块
        translated_chunks = []
        for chunk in chunks:
            translated_chunks.append(self.translate_text(chunk))

        return '\n\n'.join(translated_chunks)
