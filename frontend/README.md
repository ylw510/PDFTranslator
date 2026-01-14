# PDF翻译器 - 前端

基于 Vue 3 + Element Plus 构建的现代化前端界面。

## 技术栈

- **Vue 3** - 渐进式JavaScript框架
- **Vite** - 下一代前端构建工具
- **Element Plus** - Vue 3 UI组件库
- **Pinia** - Vue状态管理
- **Axios** - HTTP客户端

## 开发

### 安装依赖

```bash
cd frontend
npm install
# 或使用国内镜像
npm install --registry=https://registry.npmmirror.com
```

### 启动开发服务器

```bash
npm run dev
```

前端将在 http://localhost:3000 运行

### 构建生产版本

```bash
npm run build
```

构建后的文件将输出到 `dist/` 目录

## 项目结构

```
frontend/
├── src/
│   ├── components/      # Vue组件
│   │   ├── FileUpload.vue
│   │   ├── TranslationControl.vue
│   │   └── ResultDisplay.vue
│   ├── services/        # API服务
│   │   └── api.js
│   ├── stores/          # 状态管理
│   │   └── translation.js
│   ├── styles/          # 样式文件
│   │   └── main.css
│   ├── App.vue          # 根组件
│   └── main.js          # 入口文件
├── index.html
├── package.json
└── vite.config.js
```

## 功能特性

- ✅ 拖拽上传文件
- ✅ 实时进度显示
- ✅ 响应式设计
- ✅ 现代化UI界面
- ✅ 翻译结果对比查看
- ✅ 导出翻译结果
