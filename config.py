import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API提供商配置
    API_PROVIDER = os.getenv('API_PROVIDER', 'deepseek').lower()  # 'openai' 或 'deepseek'

    # API密钥配置（通用）
    API_KEY = os.getenv('API_KEY', os.getenv('OPENAI_API_KEY', ''))  # 优先使用API_KEY，兼容OPENAI_API_KEY
    OPENAI_API_KEY = API_KEY  # 保持兼容性

    # 模型配置
    if API_PROVIDER == 'deepseek':
        DEFAULT_MODEL = 'deepseek-chat'
        DEFAULT_BASE_URL = 'https://api.deepseek.com'
    else:
        DEFAULT_MODEL = 'gpt-3.5-turbo'
        DEFAULT_BASE_URL = None

    MODEL = os.getenv('MODEL', DEFAULT_MODEL)
    OPENAI_MODEL = MODEL  # 保持兼容性
    BASE_URL = os.getenv('BASE_URL', os.getenv('OPENAI_BASE_URL', DEFAULT_BASE_URL))
    OPENAI_BASE_URL = BASE_URL  # 保持兼容性

    # 代理和超时配置
    PROXY = os.getenv('PROXY', os.getenv('OPENAI_PROXY', None))
    OPENAI_PROXY = PROXY  # 保持兼容性
    TIMEOUT = int(os.getenv('TIMEOUT', os.getenv('OPENAI_TIMEOUT', '60')))
    OPENAI_TIMEOUT = TIMEOUT  # 保持兼容性

    # 翻译配置
    TARGET_LANGUAGE = os.getenv('TARGET_LANGUAGE', '中文')
    SOURCE_LANGUAGE = os.getenv('SOURCE_LANGUAGE', '英文')

    # 文件上传配置
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'pdf'}
