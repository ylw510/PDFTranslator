<template>
  <el-card class="control-card" shadow="hover" v-if="hasFile">
    <template #header>
      <div class="card-header">
        <el-icon><Setting /></el-icon>
        <span>翻译设置</span>
      </div>
    </template>

    <el-form :model="form" label-width="120px">
      <el-form-item label="页面范围">
        <el-input
          v-model="form.pageRange"
          placeholder="例如: 1,2,3 或 1-5 (留空翻译全部)"
          clearable
        >
          <template #prepend>
            <el-icon><Document /></el-icon>
          </template>
        </el-input>
        <div class="form-tip">
          共 {{ totalPages }} 页，留空将翻译全部页面
        </div>
      </el-form-item>

      <el-form-item>
        <el-button
          type="primary"
          size="large"
          :loading="isTranslating"
          :disabled="isTranslating"
          @click="handleTranslate"
          style="width: 100%"
        >
          <el-icon v-if="!isTranslating"><Promotion /></el-icon>
          {{ isTranslating ? '翻译中...' : '开始翻译' }}
        </el-button>
      </el-form-item>
    </el-form>

    <el-progress
      v-if="isTranslating"
      :percentage="progressPercent"
      :status="progressPercent === 100 ? 'success' : null"
      :format="formatProgress"
      class="translate-progress"
    />

    <el-alert
      v-if="error"
      :title="error"
      type="error"
      :closable="true"
      @close="clearError"
      style="margin-top: 20px"
    />
  </el-card>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Setting, Document, Promotion } from '@element-plus/icons-vue'
import { translatePDF } from '../services/api'
import { useTranslationStore } from '../stores/translation'

const emit = defineEmits(['translated'])

const form = ref({
  pageRange: ''
})

const translationStore = useTranslationStore()

const hasFile = computed(() => translationStore.hasFile)
const totalPages = computed(() => translationStore.totalPages)
const isTranslating = computed(() => translationStore.isTranslating)
const progressPercent = computed(() => translationStore.translateProgressPercent)
const error = computed(() => translationStore.error)

const parsePageRange = (range) => {
  if (!range || !range.trim()) return null

  const pageNumbers = []
  const parts = range.split(',')

  for (const part of parts) {
    const trimmed = part.trim()
    if (trimmed.includes('-')) {
      const [start, end] = trimmed.split('-').map(Number)
      if (start && end && start <= end) {
        for (let i = start; i <= end; i++) {
          pageNumbers.push(i)
        }
      }
    } else {
      const num = Number(trimmed)
      if (num > 0) {
        pageNumbers.push(num)
      }
    }
  }

  return pageNumbers.length > 0 ? pageNumbers : null
}

const handleTranslate = async () => {
  if (!translationStore.currentFile) {
    ElMessage.warning('请先上传PDF文件')
    return
  }

  const pageNumbers = parsePageRange(form.value.pageRange)

  if (pageNumbers && pageNumbers.some(p => p > totalPages.value)) {
    ElMessage.warning(`页面范围超出总页数 ${totalPages.value}`)
    return
  }

  translationStore.setTranslating(true)
  translationStore.setError(null)

  try {
    const result = await translatePDF(
      translationStore.currentFile.filepath,
      pageNumbers
    )

    translationStore.setTranslatedPages(result.translated_pages)
    emit('translated', result)

    ElMessage.success(`翻译完成！共翻译 ${result.total_pages} 页`)
  } catch (error) {
    ElMessage.error(error.message || '翻译失败')
    translationStore.setError(error.message)
  } finally {
    translationStore.setTranslating(false)
  }
}

const formatProgress = (percentage) => {
  return `翻译进度: ${percentage}% (${translationStore.translateProgress}/${totalPages.value})`
}

const clearError = () => {
  translationStore.setError(null)
}

watch(() => translationStore.currentFile, () => {
  form.value.pageRange = ''
})
</script>

<style scoped>
.control-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
}

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.translate-progress {
  margin-top: 20px;
}
</style>
