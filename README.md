# PDF翻译器

一个基于大语言模型的PDF文档翻译工具，支持DeepSeek和OpenAI API，提供现代化的Web界面。

## ✨ 功能特性

- 📄 **PDF文件解析** - 使用pdfplumber提取PDF文本内容
- 🤖 **多模型支持** - 支持DeepSeek和OpenAI API
- 🌐 **现代化界面** - 基于Vue 3 + Element Plus构建
- 📊 **实时进度** - 显示上传和翻译进度
- 🔄 **双语对比** - 原文与译文并排显示
- 📱 **响应式设计** - 支持桌面和移动端
- ⚙️ **灵活配置** - 支持自定义页面范围翻译

## 🚀 快速开始

### 环境要求

- **Python**: 3.8+
- **Node.js**: 18.0+ (用于前端开发)
- **npm**: 8.0+

### 一键安装（推荐）

```bash
# 克隆项目
git clone <repository-url>
cd PDFTranslator

# 运行安装脚本
bash install.sh
```

### 手动安装

#### 1. 安装后端依赖

```bash
# 使用清华镜像源（推荐）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 2. 安装前端依赖

```bash
cd frontend
npm install --registry=https://registry.npmmirror.com
```

#### 3. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑.env文件，填入你的API密钥
nano .env
```

**必需配置：**
```env
API_PROVIDER=deepseek          # 或 openai
API_KEY=your_api_key_here      # 你的API密钥
```

## 📖 使用指南

### 开发模式

**方式1：分别启动（推荐）**

```bash
# 终端1：启动后端
python app.py

# 终端2：启动前端
cd frontend
npm run dev
```

访问：
- 前端界面：http://localhost:3000
- 后端API：http://localhost:5000


### 生产模式

```bash
# 1. 构建前端
cd frontend
npm run build

# 2. 启动后端（会自动服务前端静态文件）
cd ..
python app.py
```

访问：http://localhost:5000

## ⚙️ 配置说明

### API提供商配置

#### DeepSeek（推荐，国内可用）

1. 访问 https://platform.deepseek.com
2. 注册/登录账号
3. 创建API密钥
4. 在`.env`中配置：
```env
API_PROVIDER=deepseek
API_KEY=your_deepseek_api_key
MODEL=deepseek-chat
```

#### OpenAI

1. 访问 https://platform.openai.com
2. 注册/登录账号
3. 创建API密钥
4. 在`.env`中配置：
```env
API_PROVIDER=openai
API_KEY=your_openai_api_key
MODEL=gpt-3.5-turbo
```

### 完整配置选项

```env
# API配置
API_PROVIDER=deepseek              # deepseek 或 openai
API_KEY=your_api_key_here          # API密钥（必需）
MODEL=deepseek-chat                # 模型名称

# 翻译配置
TARGET_LANGUAGE=中文                # 目标语言
SOURCE_LANGUAGE=英文                # 源语言

# 性能配置
TIMEOUT=30                          # 超时时间（秒）

# 代理配置（可选）
PROXY=http://127.0.0.1:7890         # 代理地址
```

## 📁 项目结构

```
PDFTranslator/
├── app.py                 # Flask后端主程序
├── config.py              # 配置管理
├── pdf_parser.py          # PDF解析模块
├── translator.py          # 翻译模块
├── requirements.txt       # Python依赖
├── .env.example           # 环境变量模板
│
├── frontend/              # Vue3前端
│   ├── src/
│   │   ├── components/   # Vue组件
│   │   ├── services/     # API服务
│   │   ├── stores/       # 状态管理
│   │   └── styles/       # 样式文件
│   ├── package.json      # 前端依赖
│   └── vite.config.js    # Vite配置
│
├── docs/                  # 文档目录
│   ├── INSTALLATION.md   # 详细安装指南
│   ├── DEPLOYMENT.md     # 部署指南
│   └── TROUBLESHOOTING.md # 故障排除
│
├── uploads/              # 上传文件目录
└── README.md             # 本文件
```

## 🔧 常见问题

### Node.js版本问题

如果遇到Node.js版本过低，请查看：[docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md#nodejs版本问题)

### API连接失败

1. 检查API密钥是否正确
2. 检查账户余额是否充足
3. 如果在中国大陆，可能需要配置代理

### 前端无法访问后端

1. 确保后端已启动（端口5000）
2. 检查CORS配置
3. 查看浏览器控制台错误信息

更多问题请查看：[docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

## 📚 文档

- [详细安装指南](docs/INSTALLATION.md) - 完整的安装步骤
- [部署指南](docs/DEPLOYMENT.md) - 生产环境部署
- [故障排除](docs/TROUBLESHOOTING.md) - 常见问题解决
- [改进建议](IMPROVEMENTS.md) - 未来改进方向

## 🛠️ 开发

### 技术栈

**后端：**
- Flask - Web框架
- pdfplumber - PDF解析
- OpenAI SDK - API调用

**前端：**
- Vue 3 - 前端框架
- Vite - 构建工具
- Element Plus - UI组件库
- Pinia - 状态管理
- Axios - HTTP客户端

### 开发规范

- 代码风格：遵循PEP 8（Python）和ESLint（JavaScript）
- 提交信息：使用清晰的提交信息
- 分支管理：main（生产）、develop（开发）

## 📝 许可证

本项目采用 MIT 许可证。

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📧 联系方式

如有问题，请提交Issue或联系项目维护者。

---

**最后更新**: 2026-01-14
