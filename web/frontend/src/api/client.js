import axios from 'axios'
import { mockApi } from './mock'

const isDemoMode = import.meta.env.VITE_DEMO_MODE === 'true'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

const realApi = {
  createSkillFromUrl: async (url) => {
    const response = await apiClient.post('/skills/create/url', { url })
    return response.data
  },

  createSkillFromFiles: async (formData) => {
    const response = await apiClient.post('/skills/create/files', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  getTaskStatus: async (taskId) => {
    const response = await apiClient.get(`/tasks/${taskId}`)
    return response.data
  },

  listSkills: async () => {
    const response = await apiClient.get('/skills')
    return response.data
  },

  getSkill: async (skillId) => {
    const response = await apiClient.get(`/skills/${skillId}`)
    return response.data
  },

  evolveSkill: async (skillId) => {
    const response = await apiClient.post(`/skills/${skillId}/evolve`)
    return response.data
  },
}

export const api = isDemoMode ? mockApi : realApi

export default apiClient
