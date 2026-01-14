# 故障排除

本文档提供常见问题的解决方案。

## 目录

- [安装问题](#安装问题)
- [运行问题](#运行问题)
- [API问题](#api问题)
- [前端问题](#前端问题)
- [网络问题](#网络问题)

## 安装问题

### Node.js版本问题

**问题**: `npm install` 报错，提示Node.js版本不够

**错误信息**:
```
npm WARN EBADENGINE Unsupported engine
```

**解决方案**:

1. **使用NVM升级Node.js（推荐）**

```bash
# 安装NVM
export NVM_SOURCE=https://gitee.com/mirrors/nvm.git
curl -o- https://gitee.com/mirrors/nvm/raw/v0.39.0/install.sh | bash

# 加载NVM
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"

# 安装Node.js 18
nvm install 18
nvm use 18
nvm alias default 18

# 验证
node --version  # 应该 >= 18.0
```

2. **直接安装Node.js**

```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

详细说明：参考 [UPGRADE_NODE.md](../UPGRADE_NODE.md)

### Python依赖安装失败

**问题**: `pip install` 失败

**解决方案**:

```bash
# 升级pip
pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 如果还有问题，尝试使用虚拟环境
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 前端依赖安装失败

**问题**: `npm install` 失败

**解决方案**:

```bash
# 清除缓存
npm cache clean --force

# 删除node_modules重新安装
rm -rf node_modules package-lock.json
npm install --registry=https://registry.npmmirror.com

# 如果网络问题，使用代理
npm config set proxy http://127.0.0.1:7890
npm install
```

## 运行问题

### 后端无法启动

**问题**: `python app.py` 报错

**常见错误**:

1. **ModuleNotFoundError: No module named 'flask_cors'**

```bash
pip install flask-cors==4.0.0 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

2. **端口被占用**

```bash
# 检查端口占用
lsof -i :5000
# 或
netstat -tlnp | grep 5000

# 杀死占用进程
kill -9 <PID>
```

3. **权限问题**

```bash
# 确保有写入权限
chmod -R 755 uploads/
```

### 前端无法启动

**问题**: `npm run dev` 报错

**常见错误**:

1. **vite: not found**

```bash
# 确保已安装依赖
cd frontend
npm install
```

2. **端口被占用**

```bash
# 检查端口占用
lsof -i :3000

# 或使用其他端口
npm run dev -- --port 3001
```

3. **无法访问localhost:3000**

```bash
# 使用--host参数
npm run dev -- --host 0.0.0.0
```

## API问题

### API密钥无效

**错误**: `401 Unauthorized` 或 `Invalid API Key`

**解决方案**:

1. 检查`.env`文件中的`API_KEY`是否正确
2. 确认API密钥是否已激活
3. 登录对应平台检查密钥状态

### 账户余额不足

**错误**: `402 Insufficient Balance`

**解决方案**:

1. 登录对应平台充值
   - DeepSeek: https://platform.deepseek.com
   - OpenAI: https://platform.openai.com
2. 检查账户余额和使用情况

### 连接超时

**错误**: `Connection timeout` 或 `Request timeout`

**解决方案**:

1. 检查网络连接
2. 增加超时时间（在`.env`中设置`TIMEOUT=60`）
3. 如果在中国大陆，配置代理：
```env
PROXY=http://127.0.0.1:7890
```

### 频率限制

**错误**: `429 Rate Limit`

**解决方案**:

1. 等待一段时间后重试
2. 检查API调用频率限制
3. 考虑升级账户套餐

## 前端问题

### 无法连接后端

**错误**: `Request failed with status code 500` 或 `Network Error`

**解决方案**:

1. **检查后端是否运行**
```bash
# 检查端口
ss -tlnp | grep 5000
```

2. **检查CORS配置**
确保`app.py`中有：
```python
from flask_cors import CORS
CORS(app)
```

3. **检查API地址**
在`frontend/src/services/api.js`中确认`baseURL`正确

### 页面空白

**问题**: 打开页面显示空白

**解决方案**:

1. 打开浏览器开发者工具（F12）
2. 查看Console标签的错误信息
3. 检查Network标签的请求状态
4. 确认前端构建是否成功

### 样式丢失

**问题**: 页面样式不正确

**解决方案**:

```bash
# 重新构建前端
cd frontend
rm -rf dist node_modules
npm install
npm run build
```

## 网络问题

### 无法访问localhost

**问题**: 无法访问 http://localhost:3000 或 http://localhost:5000

**解决方案**:

1. **检查服务是否运行**
```bash
# 检查端口监听
ss -tlnp | grep -E ':(3000|5000)'
```

2. **使用0.0.0.0绑定**
```bash
# 后端
python app.py  # 默认绑定0.0.0.0

# 前端
npm run dev -- --host 0.0.0.0
```

3. **从其他机器访问**
使用服务器IP地址：`http://your-server-ip:3000`

### 代理配置问题

**问题**: 代理无法使用

**解决方案**:

1. **检查代理是否运行**
```bash
# 测试代理
curl -x http://127.0.0.1:7890 https://www.google.com
```

2. **检查代理配置**
在`.env`中确认`PROXY`配置正确：
```env
PROXY=http://127.0.0.1:7890
```

3. **Windows代理配置**
如果代理在Windows上，使用Windows IP：
```env
PROXY=http://192.168.1.3:7890
```

## 文件上传问题

### 文件上传失败

**错误**: `413 Request Entity Too Large`

**解决方案**:

1. 检查文件大小（限制16MB）
2. 检查Nginx配置（如果有）：
```nginx
client_max_body_size 16M;
```

### PDF解析失败

**错误**: `PDF解析失败`

**解决方案**:

1. 确认PDF文件格式正确
2. 检查PDF是否加密或损坏
3. 尝试其他PDF文件测试

## 性能问题

### 翻译速度慢

**问题**: 翻译时间过长

**解决方案**:

1. 减少翻译页面数量
2. 增加超时时间
3. 检查网络速度
4. 考虑使用更快的API模型

### 内存占用高

**问题**: 服务器内存不足

**解决方案**:

1. 限制并发翻译数量
2. 定期清理uploads目录
3. 使用更高效的PDF解析方式

## 获取帮助

如果以上方案都无法解决问题：

1. 查看应用日志
2. 检查浏览器控制台错误
3. 提交Issue并附上错误信息
4. 提供环境信息（Python版本、Node版本等）

## 常用命令

```bash
# 检查服务状态
ss -tlnp | grep -E ':(3000|5000)'

# 查看Python进程
ps aux | grep python

# 查看Node进程
ps aux | grep node

# 查看日志
tail -f logs/app.log

# 测试API
curl http://localhost:5000/api/upload
```
