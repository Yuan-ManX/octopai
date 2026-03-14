import React, { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { api } from '../api/client'

function SkillDetail() {
  const { skillId } = useParams()
  const [skill, setSkill] = useState(null)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('overview')
  const [evolutionLoading, setEvolutionLoading] = useState(false)
  const [taskId, setTaskId] = useState(null)
  const [taskStatus, setTaskStatus] = useState(null)

  useEffect(() => {
    if (skillId) {
      loadSkill()
    }
  }, [skillId])

  const loadSkill = async () => {
    try {
      const response = await api.getSkill(skillId)
      setSkill(response.skill)
    } catch (error) {
      console.error('Error loading skill:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleEvolve = async () => {
    setEvolutionLoading(true)
    try {
      const response = await api.evolveSkill(skillId)
      setTaskId(response.task_id)
      pollTaskStatus(response.task_id)
    } catch (error) {
      console.error('Error evolving skill:', error)
      alert('Evolution failed, please try again')
    } finally {
      setEvolutionLoading(false)
    }
  }

  const pollTaskStatus = async (id) => {
    const pollInterval = setInterval(async () => {
      try {
        const status = await api.getTaskStatus(id)
        setTaskStatus(status)
        
        if (status.status === 'completed' || status.status === 'failed') {
          clearInterval(pollInterval)
          if (status.status === 'completed') {
            loadSkill()
          }
        }
      } catch (error) {
        console.error('Polling error:', error)
        clearInterval(pollInterval)
      }
    }, 2000)
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800'
      case 'evolving': return 'bg-yellow-100 text-yellow-800'
      case 'archived': return 'bg-gray-100 text-gray-800'
      default: return 'bg-blue-100 text-blue-800'
    }
  }

  if (loading) {
    return (
      <div className="text-center py-16">
        <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-purple-600 mx-auto mb-4"></div>
        <p className="text-gray-600">Loading...</p>
      </div>
    )
  }

  if (!skill) {
    return (
      <div className="text-center py-16">
        <div className="text-6xl mb-4">❓</div>
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Skill not found</h2>
        <Link
          to="/skills"
          className="px-8 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white font-semibold rounded-xl hover:from-purple-700 hover:to-blue-700 transition-all"
        >
          Back to Skill Library
        </Link>
      </div>
    )
  }

  return (
    <div className="max-w-5xl mx-auto">
      <div className="mb-8">
        <Link
          to="/skills"
          className="text-purple-600 hover:text-purple-800 font-semibold mb-4 inline-flex items-center gap-2"
        >
          ← Back to Skill Library
        </Link>
      </div>

      <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
        <div className="flex justify-between items-start mb-6">
          <div>
            <div className="flex items-center gap-4 mb-4">
              <span className="text-6xl">{skill.icon || '🧠'}</span>
              <div>
                <h1 className="text-3xl font-bold text-gray-800 mb-2">
                  {skill.name || 'Unnamed Skill'}
                </h1>
                <div className="flex items-center gap-3">
                  <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getStatusColor(skill.status || 'active')}`}>
                    {skill.status || 'active'}
                  </span>
                  <span className="text-gray-500">v{skill.version || '1.0'}</span>
                </div>
              </div>
            </div>
            <p className="text-gray-600 text-lg">
              {skill.description || 'No description available'}
            </p>
          </div>
          <button
            onClick={handleEvolve}
            disabled={evolutionLoading || taskId}
            className="px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white font-semibold rounded-xl hover:from-purple-700 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center gap-2"
          >
            {evolutionLoading ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                Evolving...
              </>
            ) : (
              <>🚀 Evolve Skill</>
            )}
          </button>
        </div>

        {taskId && (
          <div className="mt-6 p-6 bg-blue-50 rounded-xl">
            <h3 className="font-semibold text-blue-800 mb-3">Evolution Task</h3>
            <div className="text-sm text-blue-700">
              <p className="mb-2">
                <span className="font-semibold">Status:</span> {taskStatus?.status || 'pending'}
              </p>
              {taskStatus?.message && (
                <p>
                  <span className="font-semibold">Message:</span> {taskStatus.message}
                </p>
              )}
            </div>
          </div>
        )}
      </div>

      <div className="flex gap-4 mb-6 border-b border-gray-200">
        {['overview', 'code', 'history', 'usage'].map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`py-3 px-6 font-semibold border-b-2 transition-all ${
              activeTab === tab
                ? 'border-purple-600 text-purple-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
          >
            {tab === 'overview' && '📋 Overview'}
            {tab === 'code' && '💻 Code'}
            {tab === 'history' && '📜 History'}
            {tab === 'usage' && '📊 Usage'}
          </button>
        ))}
      </div>

      <div className="bg-white rounded-2xl shadow-xl p-8">
        {activeTab === 'overview' && (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-3">Basic Information</h3>
              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 bg-gray-50 rounded-xl">
                  <p className="text-sm text-gray-500 mb-1">Created</p>
                  <p className="font-semibold">
                    {skill.created_at ? new Date(skill.created_at).toLocaleString() : 'Unknown'}
                  </p>
                </div>
                <div className="p-4 bg-gray-50 rounded-xl">
                  <p className="text-sm text-gray-500 mb-1">Updated</p>
                  <p className="font-semibold">
                    {skill.updated_at ? new Date(skill.updated_at).toLocaleString() : 'Unknown'}
                  </p>
                </div>
                <div className="p-4 bg-gray-50 rounded-xl">
                  <p className="text-sm text-gray-500 mb-1">Evolutions</p>
                  <p className="font-semibold">{skill.evolution_count || 0}</p>
                </div>
                <div className="p-4 bg-gray-50 rounded-xl">
                  <p className="text-sm text-gray-500 mb-1">Usage</p>
                  <p className="font-semibold">{skill.usage_count || 0}</p>
                </div>
              </div>
            </div>

            {skill.tags && skill.tags.length > 0 && (
              <div>
                <h3 className="text-lg font-semibold text-gray-800 mb-3">Tags</h3>
                <div className="flex flex-wrap gap-2">
                  {skill.tags.map((tag, index) => (
                    <span
                      key={index}
                      className="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm font-medium"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'code' && (
          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Skill Code</h3>
            {skill.code ? (
              <pre className="bg-gray-900 text-green-400 p-6 rounded-xl overflow-x-auto text-sm">
                {skill.code}
              </pre>
            ) : (
              <p className="text-gray-500">No code available</p>
            )}
          </div>
        )}

        {activeTab === 'history' && (
          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Evolution History</h3>
            {skill.evolution_history && skill.evolution_history.length > 0 ? (
              <div className="space-y-4">
                {skill.evolution_history.map((history, index) => (
                  <div key={index} className="p-4 bg-gray-50 rounded-xl border-l-4 border-purple-500">
                    <div className="flex justify-between items-start mb-2">
                      <span className="font-semibold">v{history.version}</span>
                      <span className="text-sm text-gray-500">
                        {history.timestamp ? new Date(history.timestamp).toLocaleString() : 'Unknown'}
                      </span>
                    </div>
                    <p className="text-gray-600 text-sm">{history.description || 'Version update'}</p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500">No evolution history</p>
            )}
          </div>
        )}

        {activeTab === 'usage' && (
          <div>
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Usage Log</h3>
            {skill.usage_history && skill.usage_history.length > 0 ? (
              <div className="space-y-3">
                {skill.usage_history.map((usage, index) => (
                  <div key={index} className="p-4 bg-gray-50 rounded-xl">
                    <div className="flex justify-between items-start">
                      <span className="font-medium text-gray-800">{usage.action || 'Used'}</span>
                      <span className="text-sm text-gray-500">
                        {usage.timestamp ? new Date(usage.timestamp).toLocaleString() : 'Unknown'}
                      </span>
                    </div>
                    {usage.outcome && (
                      <p className="text-sm text-gray-600 mt-1">{usage.outcome}</p>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500">No usage log</p>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default SkillDetail
