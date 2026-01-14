import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 300000, // 5分钟超时，因为翻译可能需要较长时间
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    const message = error.response?.data?.error || error.message || '请求失败'
    return Promise.reject(new Error(message))
  }
)

// 上传PDF文件
export const uploadPDF = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  const response = await api.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    timeout: 60000 // 上传超时1分钟
  })
  return response
}

// 翻译PDF
export const translatePDF = async (filepath, pageNumbers = null) => {
  const response = await api.post('/translate', {
    filepath,
    page_numbers: pageNumbers
  })
  return response
}

export default api
