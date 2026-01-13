# PDF翻译器

一个基于大语言模型的PDF文档翻译工具。

## 功能特性

- ✅ PDF文件解析（使用pdfplumber）
- ✅ 支持多种大语言模型API（DeepSeek、OpenAI）
- ✅ 支持分页翻译和批量翻译
- ✅ 原文与译文对比查看
- ✅ 美观的Web界面

## 安装

1. 安装依赖：
```bash
# 使用默认源
pip install -r requirements.txt

# 或使用清华大学镜像源（推荐，速度更快）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

2. 配置环境变量：
复制 `.env.example` 为 `.env`，并填入你的API密钥：
```bash
cp .env.example .env
# 然后编辑 .env 文件，填入你的 API 密钥
```

### 支持的API提供商

- **DeepSeek**（推荐，国内可用）
  - 获取API密钥：https://platform.deepseek.com
  - 模型：`deepseek-chat`, `deepseek-coder`

- **OpenAI**
  - 获取API密钥：https://platform.openai.com
  - 模型：`gpt-3.5-turbo`, `gpt-4`

## 使用方法

1. 启动应用：
```bash
python app.py
```

2. 打开浏览器访问：`http://localhost:5000`

3. 上传PDF文件，点击"上传并解析"

4. 选择要翻译的页面（可选），点击"开始翻译"

5. 查看翻译结果对比

## 配置说明

在 `.env` 文件中可以配置：
- `API_PROVIDER`: API提供商，`deepseek` 或 `openai`，默认 `deepseek`
- `API_KEY`: API密钥（必需）
- `MODEL`: 使用的模型
  - DeepSeek: `deepseek-chat`（默认）, `deepseek-coder`
  - OpenAI: `gpt-3.5-turbo`, `gpt-4`
- `TARGET_LANGUAGE`: 目标语言，默认 `中文`
- `SOURCE_LANGUAGE`: 源语言，默认 `英文`
- `TIMEOUT`: 超时时间（秒），默认 `30`
- `PROXY`: 代理地址（可选），如 `http://127.0.0.1:7890`

## 注意事项

- 确保有足够的OpenAI API额度
- 大文件翻译可能需要较长时间
- 建议先翻译少量页面测试效果
- 上传的PDF文件会保存在 `uploads/` 目录中

## 项目结构

```
PDFTranslator/
├── requirements.txt      # 项目依赖
├── config.py            # 配置文件
├── pdf_parser.py        # PDF解析模块
├── translator.py        # 翻译模块
├── app.py               # Web应用主程序
├── templates/
│   └── index.html       # 前端界面
├── static/
│   └── style.css        # 样式文件
├── uploads/            # 上传文件目录（自动创建）
└── README.md            # 说明文档

```
