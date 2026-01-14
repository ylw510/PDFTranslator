import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useTranslationStore = defineStore('translation', () => {
  // 状态
  const currentFile = ref(null)
  const totalPages = ref(0)
  const translatedPages = ref([])
  const isUploading = ref(false)
  const isTranslating = ref(false)
  const uploadProgress = ref(0)
  const translateProgress = ref(0)
  const error = ref(null)

  // 计算属性
  const hasFile = computed(() => currentFile.value !== null)
  const hasResults = computed(() => translatedPages.value.length > 0)
  const translateProgressPercent = computed(() => {
    if (totalPages.value === 0) return 0
    return Math.round((translateProgress.value / totalPages.value) * 100)
  })

  // 方法
  function setFile(fileInfo) {
    currentFile.value = fileInfo
    totalPages.value = fileInfo.total_pages || 0
    translatedPages.value = []
    error.value = null
  }

  function setTranslatedPages(pages) {
    translatedPages.value = pages
    translateProgress.value = pages.length
  }

  function setUploading(value) {
    isUploading.value = value
  }

  function setTranslating(value) {
    isTranslating.value = value
  }

  function setError(err) {
    error.value = err
  }

  function reset() {
    currentFile.value = null
    totalPages.value = 0
    translatedPages.value = []
    isUploading.value = false
    isTranslating.value = false
    uploadProgress.value = 0
    translateProgress.value = 0
    error.value = null
  }

  return {
    // 状态
    currentFile,
    totalPages,
    translatedPages,
    isUploading,
    isTranslating,
    uploadProgress,
    translateProgress,
    error,
    // 计算属性
    hasFile,
    hasResults,
    translateProgressPercent,
    // 方法
    setFile,
    setTranslatedPages,
    setUploading,
    setTranslating,
    setError,
    reset
  }
})
