#!/bin/bash
# 启动前端开发服务器

echo "=========================================="
echo "启动前端开发服务器"
echo "=========================================="

# 加载NVM
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"

# 切换到Node.js 18
nvm use 18

# 检查Node.js版本
NODE_VERSION=$(node --version)
echo "当前Node.js版本: $NODE_VERSION"

if [[ ! "$NODE_VERSION" =~ ^v1[89]\. ]] && [[ ! "$NODE_VERSION" =~ ^v2[0-9]\. ]]; then
    echo "❌ 错误: Node.js版本过低，需要18+"
    echo "请运行: nvm install 18 && nvm use 18"
    exit 1
fi

# 进入前端目录
cd "$(dirname "$0")/frontend" || exit 1

# 检查依赖是否安装
if [ ! -d "node_modules" ]; then
    echo "📦 安装前端依赖..."
    npm install --registry=https://registry.npmmirror.com
fi

# 检查并停止占用端口的进程
if lsof -ti:3000 >/dev/null 2>&1; then
    echo "⚠️  检测到端口3000被占用，正在停止..."
    lsof -ti:3000 | xargs kill -9 2>/dev/null
    sleep 1
fi

# 启动开发服务器
echo ""
echo "✅ 启动前端开发服务器..."
echo "访问地址: http://localhost:3000"
echo "按 Ctrl+C 停止"
echo ""

npm run dev -- --host 0.0.0.0 --port 3000
