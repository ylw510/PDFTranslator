# 安装指南

本文档提供PDF翻译器的详细安装步骤。

## 目录

- [环境要求](#环境要求)
- [系统依赖](#系统依赖)
- [后端安装](#后端安装)
- [前端安装](#前端安装)
- [配置设置](#配置设置)
- [验证安装](#验证安装)

## 环境要求

### 必需环境

- **操作系统**: Linux / macOS / Windows
- **Python**: 3.8 或更高版本
- **Node.js**: 18.0 或更高版本（用于前端开发）
- **npm**: 8.0 或更高版本

### 检查环境

```bash
# 检查Python版本
python3 --version  # 应该 >= 3.8

# 检查Node.js版本
node --version      # 应该 >= 18.0

# 检查npm版本
npm --version       # 应该 >= 8.0
```

## 系统依赖

### Ubuntu/Debian

```bash
sudo apt update
sudo apt install python3 python3-pip nodejs npm
```

### CentOS/RHEL

```bash
sudo yum install python3 python3-pip nodejs npm
```

### macOS

```bash
# 使用Homebrew
brew install python3 node
```

## 后端安装

### 1. 克隆项目

```bash
git clone <repository-url>
cd PDFTranslator
```

### 2. 安装Python依赖

```bash
# 使用默认源
pip install -r requirements.txt

# 或使用清华镜像源（推荐，速度更快）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 3. 验证后端安装

```bash
python3 -c "import flask, pdfplumber, openai; print('✅ 后端依赖安装成功')"
```

## 前端安装

### 1. 进入前端目录

```bash
cd frontend
```

### 2. 安装Node.js依赖

```bash
# 使用默认源
npm install

# 或使用国内镜像源（推荐）
npm install --registry=https://registry.npmmirror.com
```

### 3. 验证前端安装

```bash
npm list vue vite element-plus
```

### Node.js版本问题

如果Node.js版本过低，请参考：[TROUBLESHOOTING.md](TROUBLESHOOTING.md#nodejs版本问题)

## 配置设置

### 1. 创建环境变量文件

```bash
# 从模板复制
cp .env.example .env

# 编辑配置文件
nano .env
# 或
vi .env
```

### 2. 配置API密钥

**DeepSeek配置示例：**
```env
API_PROVIDER=deepseek
API_KEY=sk-your-deepseek-api-key
MODEL=deepseek-chat
TARGET_LANGUAGE=中文
SOURCE_LANGUAGE=英文
TIMEOUT=30
```

**OpenAI配置示例：**
```env
API_PROVIDER=openai
API_KEY=sk-your-openai-api-key
MODEL=gpt-3.5-turbo
TARGET_LANGUAGE=中文
SOURCE_LANGUAGE=英文
TIMEOUT=30
```

### 3. 获取API密钥

#### DeepSeek
1. 访问 https://platform.deepseek.com
2. 注册/登录账号
3. 进入API密钥管理页面
4. 创建新密钥
5. 复制密钥到`.env`文件

#### OpenAI
1. 访问 https://platform.openai.com
2. 注册/登录账号
3. 进入API Keys页面
4. 创建新密钥
5. 复制密钥到`.env`文件

## 验证安装

### 1. 测试后端

```bash
# 测试API连接
python3 test_connection.py

# 或测试API密钥
python3 test_api_key.py
```

### 2. 测试前端

```bash
cd frontend
npm run dev
```

访问 http://localhost:3000 查看前端界面

### 3. 完整测试

```bash
# 终端1：启动后端
python3 app.py

# 终端2：启动前端
cd frontend
npm run dev
```

访问 http://localhost:3000，尝试上传PDF文件测试

## 常见安装问题

### Python依赖安装失败

**问题**: `pip install` 失败

**解决**:
```bash
# 升级pip
pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Node.js版本过低

**问题**: `npm install` 报错，提示Node.js版本不够

**解决**: 参考 [TROUBLESHOOTING.md](TROUBLESHOOTING.md#nodejs版本问题)

### 权限问题

**问题**: `Permission denied`

**解决**:
```bash
# 不要使用sudo安装Python包（推荐使用虚拟环境）
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 下一步

安装完成后，请查看：
- [部署指南](DEPLOYMENT.md) - 了解如何部署到生产环境
- [故障排除](TROUBLESHOOTING.md) - 解决常见问题
