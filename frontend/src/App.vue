<template>
  <div class="app-container">
    <el-container>
      <el-header class="app-header">
        <div class="header-content">
          <div class="logo">
            <el-icon><Document /></el-icon>
            <h1>PDF翻译器</h1>
          </div>
          <div class="header-actions">
            <el-button
              v-if="translationStore.hasResults"
              @click="resetAll"
              type="info"
              plain
            >
              <el-icon><Refresh /></el-icon>
              重置
            </el-button>
          </div>
        </div>
      </el-header>

      <el-main class="app-main">
        <div class="content-wrapper">
          <el-row :gutter="20">
            <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
              <!-- 文件上传组件 -->
              <FileUpload @uploaded="handleUploaded" />

              <!-- 翻译控制组件 -->
              <TranslationControl @translated="handleTranslated" />

              <!-- 结果显示组件 -->
              <ResultDisplay />
            </el-col>
          </el-row>
        </div>
      </el-main>

      <el-footer class="app-footer">
        <div class="footer-content">
          <p>© 2026 PDF翻译器 | 基于 Vue 3 + Element Plus 构建</p>
        </div>
      </el-footer>
    </el-container>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Document, Refresh } from '@element-plus/icons-vue'
import { useTranslationStore } from './stores/translation'
import FileUpload from './components/FileUpload.vue'
import TranslationControl from './components/TranslationControl.vue'
import ResultDisplay from './components/ResultDisplay.vue'

const translationStore = useTranslationStore()

const handleUploaded = (result) => {
  console.log('文件上传成功:', result)
}

const handleTranslated = (result) => {
  console.log('翻译完成:', result)
}

const resetAll = () => {
  translationStore.reset()
  ElMessage.success('已重置')
}

onMounted(() => {
  console.log('PDF翻译器已加载')
})
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.app-header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 0 40px;
  height: 70px;
  display: flex;
  align-items: center;
}

.header-content {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo .el-icon {
  font-size: 32px;
  color: #667eea;
}

.logo h1 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.app-main {
  padding: 40px 20px;
  min-height: calc(100vh - 140px);
}

.content-wrapper {
  max-width: 1400px;
  margin: 0 auto;
}

.app-footer {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}

.footer-content {
  text-align: center;
  color: #909399;
  font-size: 14px;
}

@media (max-width: 768px) {
  .app-header {
    padding: 0 20px;
  }

  .logo h1 {
    font-size: 20px;
  }

  .app-main {
    padding: 20px 10px;
  }
}
</style>
