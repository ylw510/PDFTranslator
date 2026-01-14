<template>
  <el-card class="result-card" shadow="hover" v-if="hasResults">
    <template #header>
      <div class="card-header">
        <el-icon><DocumentCopy /></el-icon>
        <span>翻译结果</span>
        <el-button
          type="primary"
          size="small"
          @click="exportResults"
          style="margin-left: auto"
        >
          <el-icon><Download /></el-icon>
          导出结果
        </el-button>
      </div>
    </template>

    <div class="results-container">
      <el-collapse v-model="activePages" accordion>
        <el-collapse-item
          v-for="page in translatedPages"
          :key="page.page"
          :name="page.page"
          :title="`第 ${page.page} 页`"
        >
          <div class="page-content">
            <el-row :gutter="20">
              <el-col :span="12">
                <div class="text-panel original">
                  <div class="panel-header">
                    <el-icon><Document /></el-icon>
                    <span>原文</span>
                  </div>
                  <div class="text-content">
                    <pre>{{ page.original }}</pre>
                  </div>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="text-panel translated">
                  <div class="panel-header">
                    <el-icon><Edit /></el-icon>
                    <span>译文</span>
                  </div>
                  <div class="text-content">
                    <pre>{{ page.translated }}</pre>
                  </div>
                </div>
              </el-col>
            </el-row>
          </div>
        </el-collapse-item>
      </el-collapse>
    </div>

    <div class="result-stats">
      <el-statistic title="总页数" :value="translatedPages.length" />
      <el-statistic title="翻译状态" value="已完成" />
    </div>
  </el-card>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { DocumentCopy, Download, Document, Edit } from '@element-plus/icons-vue'
import { useTranslationStore } from '../stores/translation'

const activePages = ref([])
const translationStore = useTranslationStore()

const hasResults = computed(() => translationStore.hasResults)
const translatedPages = computed(() => translationStore.translatedPages)

const exportResults = () => {
  // 导出功能待实现
  ElMessage.info('导出功能开发中...')

  // 可以导出为文本或PDF
  const content = translatedPages.value.map(page =>
    `第 ${page.page} 页\n原文:\n${page.original}\n\n译文:\n${page.translated}\n\n`
  ).join('\n' + '='.repeat(50) + '\n\n')

  const blob = new Blob([content], { type: 'text/plain;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = 'translation_result.txt'
  link.click()
  URL.revokeObjectURL(url)

  ElMessage.success('导出成功！')
}
</script>

<style scoped>
.result-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
}

.results-container {
  margin: 20px 0;
}

.page-content {
  padding: 10px 0;
}

.text-panel {
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  overflow: hidden;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: #fafafa;
}

.text-panel.original {
  border-left: 4px solid #409eff;
}

.text-panel.translated {
  border-left: 4px solid #67c23a;
}

.panel-header {
  padding: 12px 16px;
  background: white;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #303133;
}

.text-content {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
  max-height: 500px;
}

.text-content pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  line-height: 1.6;
  color: #606266;
}

.result-stats {
  display: flex;
  gap: 40px;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #e4e7ed;
  justify-content: center;
}

:deep(.el-collapse-item__header) {
  font-weight: 600;
  font-size: 16px;
}

:deep(.el-collapse-item__content) {
  padding: 0;
}
</style>
