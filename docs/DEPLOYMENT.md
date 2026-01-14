# 部署指南

本文档介绍如何将PDF翻译器部署到生产环境。

## 目录

- [部署方式](#部署方式)
- [开发模式部署](#开发模式部署)
- [生产模式部署](#生产模式部署)
- [Docker部署](#docker部署)
- [Nginx反向代理](#nginx反向代理)
- [安全建议](#安全建议)

## 部署方式

### 方式对比

| 方式 | 适用场景 | 优点 | 缺点 |
|------|---------|------|------|
| 开发模式 | 本地开发、测试 | 热重载、快速开发 | 性能较低 |
| 生产模式 | 单机部署 | 简单快速 | 单点故障 |
| Docker | 容器化部署 | 环境隔离、易扩展 | 需要Docker |
| Nginx | 高并发生产 | 高性能、负载均衡 | 配置复杂 |

## 开发模式部署

适用于开发和测试环境。

### 启动步骤

```bash
# 终端1：启动后端
python3 app.py

# 终端2：启动前端
cd frontend
npm run dev
```

### 访问地址

- 前端：http://localhost:3000
- 后端：http://localhost:5000

## 生产模式部署

### 1. 构建前端

```bash
cd frontend
npm run build
```

构建后的文件在 `frontend/dist/` 目录

### 2. 配置后端

确保 `app.py` 中的静态文件配置正确：

```python
if os.path.exists('frontend/dist'):
    app = Flask(__name__, static_folder='frontend/dist', static_url_path='')
```

### 3. 启动后端

```bash
# 开发模式（不推荐生产）
python3 app.py

# 使用Gunicorn（推荐）
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 4. 访问应用

访问：http://your-server-ip:5000

## Docker部署

### 1. 创建Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    nodejs npm \
    && rm -rf /var/lib/apt/lists/*

# 安装Python依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 安装前端依赖并构建
COPY frontend/package*.json ./frontend/
RUN cd frontend && npm install --registry=https://registry.npmmirror.com
COPY frontend/ ./frontend/
RUN cd frontend && npm run build

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 5000

# 启动应用
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### 2. 创建docker-compose.yml

```yaml
version: '3.8'

services:
  pdf-translator:
    build: .
    ports:
      - "5000:5000"
    environment:
      - API_PROVIDER=${API_PROVIDER}
      - API_KEY=${API_KEY}
    volumes:
      - ./uploads:/app/uploads
      - ./.env:/app/.env
    restart: unless-stopped
```

### 3. 构建和运行

```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

## Nginx反向代理

### 1. 安装Nginx

```bash
sudo apt install nginx
```

### 2. 配置Nginx

创建配置文件 `/etc/nginx/sites-available/pdf-translator`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /path/to/PDFTranslator/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # 后端API
    location /api {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 文件上传大小限制
    client_max_body_size 16M;
}
```

### 3. 启用配置

```bash
sudo ln -s /etc/nginx/sites-available/pdf-translator /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 4. HTTPS配置（可选）

使用Let's Encrypt获取SSL证书：

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## 安全建议

### 1. 环境变量安全

- ✅ 不要将`.env`文件提交到Git
- ✅ 使用强密码和API密钥
- ✅ 定期轮换API密钥

### 2. 文件上传安全

- ✅ 限制文件大小（已在配置中设置）
- ✅ 验证文件类型
- ✅ 定期清理uploads目录

### 3. 网络安全

- ✅ 使用HTTPS（生产环境）
- ✅ 配置防火墙规则
- ✅ 限制API访问频率

### 4. 服务器安全

- ✅ 定期更新系统
- ✅ 使用非root用户运行
- ✅ 配置日志监控

## 性能优化

### 1. 使用Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 app:app
```

### 2. 使用Redis缓存（可选）

```bash
pip install redis flask-caching
```

### 3. 前端资源优化

- 启用Gzip压缩
- 使用CDN加速
- 图片懒加载

## 监控和日志

### 1. 应用日志

```bash
# 查看应用日志
tail -f logs/app.log

# 使用systemd管理（推荐）
sudo systemctl start pdf-translator
sudo systemctl status pdf-translator
```

### 2. 错误监控

考虑集成：
- Sentry - 错误追踪
- Prometheus - 性能监控
- Grafana - 可视化

## 备份和恢复

### 1. 数据备份

```bash
# 备份上传文件
tar -czf uploads_backup_$(date +%Y%m%d).tar.gz uploads/

# 备份配置文件
cp .env .env.backup
```

### 2. 恢复

```bash
# 恢复上传文件
tar -xzf uploads_backup_YYYYMMDD.tar.gz

# 恢复配置
cp .env.backup .env
```

## 故障排除

遇到问题请查看：[TROUBLESHOOTING.md](TROUBLESHOOTING.md)
