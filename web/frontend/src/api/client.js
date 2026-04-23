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

    // Namespace endpoints
    listNamespaces: (user_id, namespace_type) => {
      let query = ''
      const params = []
      if (user_id) params.push(`user_id=${encodeURIComponent(user_id)}`)
      if (namespace_type) params.push(`namespace_type=${encodeURIComponent(namespace_type)}`)
      if (params.length > 0) query = `?${params.join('&')}`
      return apiRequest(`/skillshub/namespaces${query}`)
    },

    createNamespace: (data) => apiRequest('/skillshub/namespaces', {
      method: 'POST',
      body: JSON.stringify(data)
    }),

    getNamespace: (namespaceId) => apiRequest(`/skillshub/namespaces/${namespaceId}`),

    // Skill endpoints
    listSkills: (category, namespaceId) => {
      const params = []
      if (category) params.push(`category=${encodeURIComponent(category)}`)
      if (namespaceId) params.push(`namespace_id=${encodeURIComponent(namespaceId)}`)
      const query = params.length > 0 ? `?${params.join('&')}` : ''
      return apiRequest(`/skillshub/skills${query}`)
    },

    createSkillVersion: (skillId, data) => apiRequest(`/skillshub/skills/${skillId}/versions`, {
      method: 'POST',
      body: JSON.stringify(data)
    }),

    submitVersionForReview: (skillId, versionId, submitterId = 'anonymous') => {
      const query = submitterId ? `?submitter_id=${encodeURIComponent(submitterId)}` : ''
      return apiRequest(`/skillshub/skills/${skillId}/versions/${versionId}/submit${query}`, {
        method: 'POST'
      })
    },

    // Review endpoints
    getPendingReviews: (namespaceId) => {
      const query = namespaceId ? `?namespace_id=${encodeURIComponent(namespaceId)}` : ''
      return apiRequest(`/skillshub/reviews/pending${query}`)
    },

    approveReview: (reviewId, data) => apiRequest(`/skillshub/reviews/${reviewId}/approve`, {
      method: 'POST',
      body: JSON.stringify(data)
    }),

    rejectReview: (reviewId, data) => apiRequest(`/skillshub/reviews/${reviewId}/reject`, {
      method: 'POST',
      body: JSON.stringify(data)
    }),

    // Promotion endpoints
    requestPromotion: (data) => apiRequest('/skillshub/promotions', {
      method: 'POST',
      body: JSON.stringify(data)
    }),

    getPendingPromotions: () => apiRequest('/skillshub/promotions/pending'),

    approvePromotion: (promotionId, data) => apiRequest(`/skillshub/promotions/${promotionId}/approve`, {
      method: 'POST',
      body: JSON.stringify(data)
    }),

    rejectPromotion: (promotionId, data) => apiRequest(`/skillshub/promotions/${promotionId}/reject`, {
      method: 'POST',
      body: JSON.stringify(data)
    }),

    // Star and Rating endpoints
    starSkill: (skillId, userId = 'anonymous') => {
      const query = userId ? `?user_id=${encodeURIComponent(userId)}` : ''
      return apiRequest(`/skillshub/skills/${skillId}/star${query}`, {
        method: 'POST'
      })
    },

    unstarSkill: (skillId, userId = 'anonymous') => {
      const query = userId ? `?user_id=${encodeURIComponent(userId)}` : ''
      return apiRequest(`/skillshub/skills/${skillId}/unstar${query}`, {
        method: 'POST'
      })
    },

    rateSkill: (skillId, data) => apiRequest(`/skillshub/skills/${skillId}/rate`, {
      method: 'POST',
      body: JSON.stringify(data)
    }),

    // Search and discovery endpoints
    searchSkills: (query, namespaceId, visibility, category, limit) => {
      const params = []
      if (query) params.push(`query=${encodeURIComponent(query)}`)
      if (namespaceId) params.push(`namespace_id=${encodeURIComponent(namespaceId)}`)
      if (visibility) params.push(`visibility=${encodeURIComponent(visibility)}`)
      if (category) params.push(`category=${encodeURIComponent(category)}`)
      if (limit) params.push(`limit=${encodeURIComponent(limit)}`)
      const queryStr = params.length > 0 ? `?${params.join('&')}` : ''
      return apiRequest(`/skillshub/search${queryStr}`)
    },

    getPopularSkills: (namespaceId, limit) => {
      const params = []
      if (namespaceId) params.push(`namespace_id=${encodeURIComponent(namespaceId)}`)
      if (limit) params.push(`limit=${encodeURIComponent(limit)}`)
      const queryStr = params.length > 0 ? `?${params.join('&')}` : ''
      return apiRequest(`/skillshub/skills/popular${queryStr}`)
    },

    getRecentSkills: (namespaceId, limit) => {
      const params = []
      if (namespaceId) params.push(`namespace_id=${encodeURIComponent(namespaceId)}`)
      if (limit) params.push(`limit=${encodeURIComponent(limit)}`)
      const queryStr = params.length > 0 ? `?${params.join('&')}` : ''
      return apiRequest(`/skillshub/skills/recent${queryStr}`)
    },

    likeSkill: (skillId) => apiRequest(`/skillshub/skills/${skillId}/star`, {
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
