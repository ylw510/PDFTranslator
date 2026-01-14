<template>
  <el-card class="upload-card" shadow="hover">
    <template #header>
      <div class="card-header">
        <el-icon><Upload /></el-icon>
        <span>上传PDF文件</span>
      </div>
    </template>

    <el-upload
      ref="uploadRef"
      class="upload-dragger"
      drag
      :auto-upload="false"
      :on-change="handleFileChange"
      :show-file-list="false"
      accept=".pdf"
      :disabled="isUploading"
    >
      <el-icon class="el-icon--upload"><upload-filled /></el-icon>
      <div class="el-upload__text">
        将文件拖到此处，或<em>点击上传</em>
      </div>
      <template #tip>
        <div class="el-upload__tip">
          支持PDF格式文件，最大16MB
        </div>
      </template>
    </el-upload>

    <div v-if="selectedFile" class="file-info">
      <el-descriptions :column="1" border size="small">
        <el-descriptions-item label="文件名">
          {{ selectedFile.name }}
        </el-descriptions-item>
        <el-descriptions-item label="文件大小">
          {{ formatFileSize(selectedFile.size) }}
        </el-descriptions-item>
      </el-descriptions>
    </div>

    <div class="upload-actions">
      <el-button
        type="primary"
        :loading="isUploading"
        :disabled="!selectedFile || isUploading"
        @click="handleUpload"
        size="large"
      >
        <el-icon v-if="!isUploading"><Upload /></el-icon>
        {{ isUploading ? '上传中...' : '上传并解析' }}
      </el-button>
      <el-button
        v-if="selectedFile"
        @click="clearFile"
        :disabled="isUploading"
      >
        清除
      </el-button>
    </div>

    <el-progress
      v-if="isUploading"
      :percentage="uploadProgress"
      :status="uploadProgress === 100 ? 'success' : null"
      class="upload-progress"
    />
  </el-card>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Upload, UploadFilled } from '@element-plus/icons-vue'
import { uploadPDF } from '../services/api'
import { useTranslationStore } from '../stores/translation'

const emit = defineEmits(['uploaded'])

const uploadRef = ref(null)
const selectedFile = ref(null)
const isUploading = ref(false)
const uploadProgress = ref(0)

const translationStore = useTranslationStore()

const handleFileChange = (file) => {
  selectedFile.value = file.raw
  translationStore.setError(null)
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

const handleUpload = async () => {
  if (!selectedFile.value) {
    ElMessage.warning('请先选择文件')
    return
  }

  isUploading.value = true
  translationStore.setUploading(true)
  uploadProgress.value = 0

  // 模拟上传进度
  const progressInterval = setInterval(() => {
    if (uploadProgress.value < 90) {
      uploadProgress.value += 10
    }
  }, 200)

  try {
    const result = await uploadPDF(selectedFile.value)
    uploadProgress.value = 100

    translationStore.setFile(result)
    emit('uploaded', result)

    ElMessage.success(`解析成功！共 ${result.total_pages} 页`)
  } catch (error) {
    ElMessage.error(error.message || '上传失败')
    translationStore.setError(error.message)
  } finally {
    clearInterval(progressInterval)
    isUploading.value = false
    translationStore.setUploading(false)
    uploadProgress.value = 0
  }
}

const clearFile = () => {
  selectedFile.value = null
  uploadRef.value?.clearFiles()
  translationStore.reset()
}
</script>

<style scoped>
.upload-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
}

.upload-dragger {
  width: 100%;
}

.el-upload-dragger {
  padding: 40px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  border: 2px dashed #409eff;
  border-radius: 8px;
  transition: all 0.3s;
}

.el-upload-dragger:hover {
  border-color: #66b1ff;
  background: linear-gradient(135deg, #ecf5ff 0%, #d9ecff 100%);
}

.el-icon--upload {
  font-size: 67px;
  color: #409eff;
  margin-bottom: 16px;
}

.el-upload__text {
  color: #606266;
  font-size: 14px;
}

.el-upload__text em {
  color: #409eff;
  font-style: normal;
}

.el-upload__tip {
  color: #909399;
  font-size: 12px;
  margin-top: 8px;
}

.file-info {
  margin: 20px 0;
}

.upload-actions {
  display: flex;
  gap: 12px;
  margin-top: 20px;
  justify-content: center;
}

.upload-progress {
  margin-top: 20px;
}
</style>
