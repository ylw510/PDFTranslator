#!/bin/bash
# 启动后端服务器

echo "=========================================="
echo "启动后端服务器"
echo "=========================================="

# 进入项目目录
cd "$(dirname "$0")" || exit 1

# 检查Python依赖
if ! python3 -c "import flask" 2>/dev/null; then
    echo "📦 安装后端依赖..."
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
fi

# 检查环境变量
if [ ! -f ".env" ]; then
    echo "⚠️  警告: .env 文件不存在"
    echo "请先创建 .env 文件并配置API密钥"
    echo "可以复制 .env.example 作为模板"
fi

# 检查并停止占用端口的进程
if lsof -ti:5000 >/dev/null 2>&1; then
    echo "⚠️  检测到端口5000被占用，正在停止..."
    lsof -ti:5000 | xargs kill -9 2>/dev/null
    sleep 1
    echo "✅ 已释放端口5000"
fi

# 启动后端服务器
echo ""
echo "✅ 启动后端服务器..."
echo "API地址: http://localhost:5000"
echo "按 Ctrl+C 停止"
echo ""

python3 app.py
