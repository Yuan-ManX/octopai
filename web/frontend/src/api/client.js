/**
 * Octopai API Client
 *
 * Frontend client for the Octopai backend API, providing:
 * - Skill Creator (create and manage skills)
 * - Skill Evolution (Feedback Descent optimization)
 * - Skills Hub (skill marketplace and management)
 * - OctoTrace (cost and performance tracking)
 * - Skill Wiki (knowledge management)
 * - AutoSkill (autonomous research and optimization)
 */

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api'

// Helper functions for API calls
async function apiRequest(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers
  }

  try {
    const response = await fetch(url, {
      ...options,
      headers
    })

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`)
    }

    return await response.json()
  } catch (error) {
    console.error(`API Request Failed: ${endpoint}`, error)
    throw error
  }
}

// ============ Status API ============
export const api = {
  getStatus: () => apiRequest('/status'),

  // ============ Skill Creator API ============
  skills: {
    create: (data) => apiRequest('/skills', {
      method: 'POST',
      body: JSON.stringify(data)
    }),

    list: (category) => {
      const query = category ? `?category=${encodeURIComponent(category)}` : ''
      return apiRequest(`/skills${query}`)
    },

    get: (skillId) => apiRequest(`/skills/${skillId}`),

    update: (skillId, data) => apiRequest(`/skills/${skillId}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    }),

    delete: (skillId) => apiRequest(`/skills/${skillId}`, {
      method: 'DELETE'
    })
  },

  // ============ Skill Evolution API ============
  evolution: {
    start: (config) => apiRequest('/evolution/start', {
      method: 'POST',
      body: JSON.stringify(config)
    }),

    stop: (runId) => apiRequest(`/evolution/${runId}/stop`, {
      method: 'POST'
    }),

    getStatus: (runId) => apiRequest(`/evolution/${runId}`),

    getFrontier: () => apiRequest('/evolution/frontier'),

    listPrograms: () => apiRequest('/evolution/programs'),

    switchProgram: (name) => apiRequest(`/evolution/programs/${name}/switch`, {
      method: 'POST'
    })
  },

  // ============ AutoSkill API ============
  autoSkill: {
    createExperiment: (data) => apiRequest('/autoskill/experiments', {
      method: 'POST',
      body: JSON.stringify(data)
    }),

    listExperiments: () => apiRequest('/autoskill/experiments'),

    getExperiment: (experimentId) => apiRequest(`/autoskill/experiments/${experimentId}`),

    startExperiment: (experimentId) => apiRequest(`/autoskill/experiments/${experimentId}/start`, {
      method: 'POST'
    }),

    stopExperiment: (experimentId) => apiRequest(`/autoskill/experiments/${experimentId}/stop`, {
      method: 'POST'
    })
  },

  // ============ Skills Hub API ============
  skillsHub: {
    getStats: () => apiRequest('/skillshub/stats'),

    likeSkill: (skillId) => apiRequest(`/skillshub/skills/${skillId}/like`, {
      method: 'POST'
    })
  },

  // ============ OctoTrace API ============
  octoTrace: {
    getOverview: () => apiRequest('/octotrace/overview'),
    getCosts: () => apiRequest('/octotrace/costs')
  },

  // ============ Skill Wiki API ============
  skillWiki: {
    search: (query) => apiRequest(`/skillwiki/search?query=${encodeURIComponent(query)}`),
    getKnowledgeGraph: () => apiRequest('/skillwiki/knowledge')
  }
}

// ============ WebSocket for real-time updates ============
export class OctopaiWebSocket {
  constructor() {
    this.url = process.env.REACT_APP_WS_URL || 'ws://localhost:8000/ws'
    this.websocket = null
    this.callbacks = []
  }

  connect() {
    if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
      return
    }

    this.websocket = new WebSocket(this.url)

    this.websocket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        this.callbacks.forEach((callback) => callback(data))
      } catch (error) {
        console.error('Error parsing WebSocket message:', error)
      }
    }

    this.websocket.onerror = (error) => {
      console.error('WebSocket error:', error)
    }

    this.websocket.onclose = () => {
      console.log('WebSocket closed, attempting to reconnect...')
      setTimeout(() => this.connect(), 3000)
    }
  }

  disconnect() {
    if (this.websocket) {
      this.websocket.close()
    }
  }

  onMessage(callback) {
    this.callbacks.push(callback)
    return () => {
      this.callbacks = this.callbacks.filter((cb) => cb !== callback)
    }
  }
}

// Singleton WebSocket instance
export const octopaiWebSocket = new OctopaiWebSocket()

export default api
