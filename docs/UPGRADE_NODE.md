# Node.js 升级指南

## 问题说明

当前 Node.js 版本：**v12.22.9**
Vite 需要：**Node.js 14.18+ 或 16+**

## 解决方案

### 方案1：使用 NVM 升级（推荐）

NVM (Node Version Manager) 可以轻松管理多个 Node.js 版本。

#### 安装 NVM

```bash
# 下载并安装 NVM
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# 或者使用国内镜像
export NVM_SOURCE=https://gitee.com/mirrors/nvm.git
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# 重新加载 shell 配置
source ~/.bashrc
# 或
source ~/.zshrc
```

#### 安装并使用 Node.js 18

```bash
# 安装 Node.js 18 LTS（长期支持版本）
nvm install 18

# 使用 Node.js 18
nvm use 18

# 设置为默认版本
nvm alias default 18

# 验证版本
node --version  # 应该显示 v18.x.x
```

### 方案2：直接安装 Node.js

#### Ubuntu/Debian

```bash
# 使用 NodeSource 仓库安装 Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# 验证
node --version
npm --version
```

#### 使用国内镜像（如果下载慢）

```bash
# 使用淘宝镜像
export NVM_NODEJS_ORG_MIRROR=https://npm.taobao.org/mirrors/node
nvm install 18
```

### 方案3：使用包管理器

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nodejs npm

# 但这种方式可能版本较旧，建议使用方案1或2
```

## 升级后操作

1. **重新安装前端依赖**：
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install --registry=https://registry.npmmirror.com
```

2. **恢复 package.json 到最新版本**：
```bash
# 编辑 frontend/package.json，将 Vite 版本改回 5.x
# 因为 Node.js 18+ 支持 Vite 5
```

3. **启动开发服务器**：
```bash
npm run dev
```

## 验证

升级后运行：
```bash
node --version  # 应该 >= 18.0.0
npm --version   # 应该 >= 8.0.0
```

## 推荐版本

- **Node.js 18 LTS**（推荐）- 长期支持版本，稳定
- **Node.js 20 LTS** - 最新 LTS 版本
- **Node.js 16** - 如果无法安装 18，可以使用 16

## 如果无法升级 Node.js

如果由于系统限制无法升级 Node.js，可以考虑：

1. **使用 Docker**：在 Docker 容器中运行前端
2. **使用其他构建工具**：改用 Webpack 或 Rollup（但需要更多配置）
3. **使用在线 IDE**：如 CodeSandbox、StackBlitz 等

## 快速检查

运行以下命令检查当前环境：
```bash
node --version
npm --version
```

如果版本低于要求，请按照上述方案升级。
