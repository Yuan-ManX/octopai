import React, { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'

const EvolutionEngine = () => {
  const navigate = useNavigate()
  const [agents, setAgents] = useState([])
  const [stats, setStats] = useState(null)
  const [agentTypes, setAgentTypes] = useState([])
  const [loading, setLoading] = useState(true)
  
  // Filter states
  const [selectedType, setSelectedType] = useState('')
  const [selectedStatus, setSelectedStatus] = useState('')
  
  // Modal states
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [showTaskModal, setShowTaskModal] = useState(false)
  const [selectedAgent, setSelectedAgent] = useState(null)
  
  // Form state
  const [formData, setFormData] = useState({
    name: '',
    agent_type: 'general',
    model_name: 'gpt-4',
    visibility: 'private'
  })
  
  // Task form state
  const [taskData, setTaskData] = useState({
    task_description: '',
    task_type: 'general'
  })

  useEffect(() => {
    fetchAgents()
    fetchStats()
    fetchAgentTypes()
  }, [])

  useEffect(() => {
    fetchAgents()
  }, [selectedType, selectedStatus])

  const fetchAgents = async () => {
    setLoading(true)
    try {
      const params = new URLSearchParams({
        page: '1',
        page_size: '20'
      })
      if (selectedType) params.append('agent_type', selectedType)
      if (selectedStatus) params.append('status', selectedStatus)
      
      const response = await fetch(`http://localhost:3005/api/evolution/agents?${params}`)
      const data = await response.json()
      setAgents(data.agents || [])
    } catch (error) {
      console.error('Error fetching agents:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchStats = async () => {
    try {
      const response = await fetch('http://localhost:3005/api/evolution/stats')
      const data = await response.json()
      setStats(data)
    } catch (error) {
      console.error('Error fetching stats:', error)
    }
  }

  const fetchAgentTypes = async () => {
    try {
      const response = await fetch('http://localhost:3005/api/evolution/agent-types')
      const data = await response.json()
      setAgentTypes(data.types || [])
    } catch (error) {
      console.error('Error fetching agent types:', error)
    }
  }

  const handleCreateAgent = async () => {
    if (!formData.name.trim()) return
    
    try {
      const response = await fetch('http://localhost:3005/api/evolution/agents', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      })
      
      if (response.ok) {
        setShowCreateModal(false)
        setFormData({ name: '', agent_type: 'general', model_name: 'gpt-4', visibility: 'private' })
        fetchAgents()
        fetchStats()
      }
    } catch (error) {
      console.error('Error creating agent:', error)
    }
  }

  const handleExecuteTask = async () => {
    if (!selectedAgent || !taskData.task_description.trim()) return
    
    try {
      const response = await fetch(`http://localhost:3005/api/evolution/agents/${selectedAgent.agent_id}/tasks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(taskData)
      })
      
      if (response.ok) {
        setShowTaskModal(false)
        setTaskData({ task_description: '', task_type: 'general' })
        setSelectedAgent(null)
        fetchAgents()
        fetchStats()
        
        // Navigate to agent detail to see results
        navigate(`/evolution-engine/${selectedAgent.agent_id}`)
      }
    } catch (error) {
      console.error('Error executing task:', error)
    }
  }

  const handleStartEvolution = async (agentId) => {
    try {
      const response = await fetch(`http://localhost:3005/api/evolution/agents/${agentId}/evolve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
      })
      
      if (response.ok) {
        setTimeout(() => {
          fetchAgents()
          fetchStats()
        }, 5000)  // Wait for evolution to complete
      }
    } catch (error) {
      console.error('Error starting evolution:', error)
    }
  }

  const getStatusColor = (status) => {
    const colors = {
      idle: 'bg-gray-500/10 text-gray-400 border-gray-500/20',
      initializing: 'bg-blue-500/10 text-blue-500 border-blue-500/20',
      running: 'bg-green-500/10 text-green-500 border-green-500/20',
      evolving: 'bg-purple-500/10 text-purple-500 border-purple-500/20',
      evaluating: 'bg-yellow-500/10 text-yellow-500 border-yellow-500/20',
      completed: 'bg-emerald-500/10 text-emerald-500 border-emerald-500/20',
      error: 'bg-red-500/10 text-red-500 border-red-500/20',
      paused: 'bg-orange-500/10 text-orange-500 border-orange-500/20'
    }
    return colors[status] || colors.idle
  }

  const getStatusIcon = (status) => {
    const icons = {
      idle: '💤',
      initializing: '⚙️',
      running: '🚀',
      evolving: '🧬',
      evaluating: '📊',
      completed: '✅',
      error: '❌',
      paused: '⏸️'
    }
    return icons[status] || '💤'
  }

  const getAgentTypeIcon = (type) => {
    const icons = {
      general: '🤖',
      researcher: '🔬',
      developer: '💻',
      analyst: '📈'
    }
    return icons[type] || '🤖'
  }

  return (
    <div className="min-h-screen py-8">
      <div className="max-w-7xl mx-auto px-6">
        {/* Header */}
        <div className="mb-10">
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 bg-gradient-to-br from-violet-600 via-purple-600 to-fuchsia-600 rounded-2xl flex items-center justify-center text-white text-3xl shadow-2xl shadow-purple-500/40 animate-pulse-subtle ring-4 ring-purple-500/20 relative overflow-hidden">
                <span className="relative z-10">🧬</span>
                <div className="absolute inset-0 bg-white/10 animate-pulse"></div>
              </div>
              <div>
                <h1 className="text-5xl font-black bg-gradient-to-r from-blue-600 via-cyan-500 to-blue-700 dark:from-blue-400 dark:via-cyan-300 dark:to-blue-400 bg-clip-text text-transparent mb-3 tracking-wide drop-shadow-xl filter">
                  AI Agents Evolution Engine
                </h1>
                <p className="text-gray-700 dark:text-gray-300 text-base font-medium leading-relaxed max-w-xl">
                  Self-evolving agent system with continuous learning and feedback loops
                </p>
              </div>
            </div>
            <div className="flex gap-3">
              <button
                onClick={() => setShowTaskModal(true)}
                className="btn btn-secondary"
                disabled={agents.length === 0}
              >
                ▶️ Run Task
              </button>
              <button
                onClick={() => setShowCreateModal(true)}
                className="btn btn-primary"
              >
                + Create Agent
              </button>
            </div>
          </div>

          {/* Statistics Dashboard */}
          {stats && (
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
              <div className="card p-4 text-center">
                <div className="text-2xl font-bold text-octo-accent">{stats.total_agents}</div>
                <div className="text-sm text-octo-text-secondary">Total Agents</div>
              </div>
              <div className="card p-4 text-center">
                <div className="text-2xl font-bold text-green-500">{stats.active_agents}</div>
                <div className="text-sm text-octo-text-secondary">Active</div>
              </div>
              <div className="card p-4 text-center">
                <div className="text-2xl font-bold text-purple-500">{stats.evolving_agents}</div>
                <div className="text-sm text-octo-text-secondary">Evolving</div>
              </div>
              <div className="card p-4 text-center">
                <div className="text-2xl font-bold text-blue-500">{stats.total_evolutions}</div>
                <div className="text-sm text-octo-text-secondary">Evolution Cycles</div>
              </div>
              <div className="card p-4 text-center">
                <div className="text-2xl font-bold text-yellow-500">{stats.avg_quality}</div>
                <div className="text-sm text-octo-text-secondary">Avg Quality</div>
              </div>
            </div>
          )}

          {/* Filters */}
          <div className="card p-4 mb-6">
            <div className="flex flex-col md:flex-row gap-4">
              <select
                value={selectedType}
                onChange={(e) => setSelectedType(e.target.value)}
                className="px-4 py-2 bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/50 text-gray-900 dark:text-gray-100"
              >
                <option value="">All Agent Types</option>
                {agentTypes.map((type) => (
                  <option key={type.id} value={type.id}>
                    {getAgentTypeIcon(type.id)} {type.name}
                  </option>
                ))}
              </select>

              <select
                value={selectedStatus}
                onChange={(e) => setSelectedStatus(e.target.value)}
                className="px-4 py-2 bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/50 text-gray-900 dark:text-gray-100"
              >
                <option value="">All Statuses</option>
                <option value="idle">💤 Idle</option>
                <option value="running">🚀 Running</option>
                <option value="evolving">🧬 Evolving</option>
                <option value="completed">✅ Completed</option>
                <option value="error">❌ Error</option>
              </select>
            </div>
          </div>
        </div>

        {/* Agents Grid */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">
            Evolving Agents ({agents.length})
          </h2>

          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[...Array(6)].map((_, idx) => (
                <div key={idx} className="card p-6 animate-pulse">
                  <div className="h-6 bg-gray-50 dark:bg-gray-800 rounded mb-3 w-3/4"></div>
                  <div className="h-4 bg-gray-50 dark:bg-gray-800 rounded mb-2 w-full"></div>
                  <div className="h-4 bg-gray-50 dark:bg-gray-800 rounded mb-4 w-2/3"></div>
                  <div className="flex gap-2">
                    <div className="h-6 bg-gray-50 dark:bg-gray-800 rounded w-16"></div>
                    <div className="h-6 bg-gray-50 dark:bg-gray-800 rounded w-24"></div>
                  </div>
                </div>
              ))}
            </div>
          ) : agents.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {agents.map((agent) => (
                <Link
                  key={agent.agent_id}
                  to={`/evolution-engine/${agent.agent_id}`}
                  className="block group"
                >
                  <div className="card p-6 transition-all duration-200 hover:shadow-xl hover:-translate-y-1 hover:border-purple-500/30">
                    {/* Agent Header */}
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-2 flex-wrap">
                          <span className={`px-2 py-0.5 rounded text-xs font-medium border ${getStatusColor(agent.status)}`}>
                            {getStatusIcon(agent.status)} {agent.status}
                          </span>
                          <span className={`px-2 py-0.5 rounded text-xs font-medium ${
                            agent.visibility === 'public' 
                              ? 'bg-green-500/10 text-green-500' 
                              : 'bg-yellow-500/10 text-yellow-500'
                          }`}>
                            {agent.visibility}
                          </span>
                        </div>
                        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 truncate group-hover:text-purple-400 transition-colors">
                          {getAgentTypeIcon(agent.config?.agent_type)} {agent.name}
                        </h3>
                      </div>
                    </div>

                    {/* Agent Info */}
                    <div className="space-y-2 mb-4">
                      <div className="flex items-center justify-between text-xs text-octo-text-tertiary">
                        <span>Model: {agent.config?.model_name || 'gpt-4'}</span>
                        <span>Gen {agent.current_generation || 1}</span>
                      </div>
                      <div className="flex items-center gap-2 text-xs text-octo-text-tertiary">
                        <span>⭐ {agent.average_quality?.toFixed(1) || '0.0'} quality</span>
                        <span>•</span>
                        <span>🎯 {agent.total_skills || 0} skills</span>
                      </div>
                    </div>

                    {/* Skills Preview */}
                    {agent.skills && agent.skills.length > 0 && (
                      <div className="mb-4 flex flex-wrap gap-1">
                        {agent.skills.slice(0, 3).map((skill, idx) => (
                          <span 
                            key={idx}
                            className="px-2 py-0.5 bg-purple-500/10 text-purple-400 rounded text-xs truncate max-w-[120px]"
                          >
                            {skill.name}
                          </span>
                        ))}
                        {(agent.skills.length > 3) && (
                          <span className="px-2 py-0.5 bg-octo-bg-tertiary rounded text-xs text-octo-text-tertiary">
                            +{agent.skills.length - 3} more
                          </span>
                        )}
                      </div>
                    )}

                    {/* Stats Footer */}
                    <div className="pt-3 border-t border-gray-300 dark:border-gray-600 grid grid-cols-4 gap-2 text-center">
                      <div>
                        <div className="text-sm font-bold text-green-500">{agent.total_tasks_completed || 0}</div>
                        <div className="text-[10px] text-octo-text-tertiary">Tasks</div>
                      </div>
                      <div>
                        <div className="text-sm font-bold text-purple-500">{agent.total_evolutions || 0}</div>
                        <div className="text-[10px] text-octo-text-tertiary">Evolutions</div>
                      </div>
                      <div>
                        <div className="text-sm font-bold text-blue-500">{agent.star_count || 0}</div>
                        <div className="text-[10px] text-octo-text-tertiary">Stars</div>
                      </div>
                      <div>
                        <div className="text-sm font-bold text-yellow-500">{agent.fork_count || 0}</div>
                        <div className="text-[10px] text-octo-text-tertiary">Forks</div>
                      </div>
                    </div>

                    {/* Action Buttons */}
                    <div className="mt-3 pt-3 border-t border-gray-300 dark:border-gray-600 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button
                        onClick={(e) => {
                          e.preventDefault()
                          e.stopPropagation()
                          handleStartEvolution(agent.agent_id)
                        }}
                        disabled={agent.status === 'evolving'}
                        className="flex-1 px-3 py-1.5 text-xs font-medium bg-purple-500/10 text-purple-400 rounded hover:bg-purple-500/20 transition-colors disabled:opacity-50"
                      >
                        🧬 Evolve
                      </button>
                      <button
                        onClick={(e) => {
                          e.preventDefault()
                          e.stopPropagation()
                          setSelectedAgent(agent)
                          setShowTaskModal(true)
                        }}
                        className="flex-1 px-3 py-1.5 text-xs font-medium bg-green-500/10 text-green-400 rounded hover:bg-green-500/20 transition-colors"
                      >
                        ▶️ Run Task
                      </button>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          ) : (
            <div className="card p-12 text-center">
              <div className="text-6xl mb-4">🧬</div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-2">
                No Evolving Agents Yet
              </h3>
              <p className="text-octo-text-secondary mb-6">
                Create your first self-evolving agent and watch it learn and improve
              </p>
              <button
                onClick={() => setShowCreateModal(true)}
                className="btn btn-primary"
              >
                + Create Your First Agent
              </button>
            </div>
          )}
        </div>

        {/* Evolution Process Info */}
        <div className="card p-6 mb-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
            🔄 How Evolution Works
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-6 gap-4">
            {[
              { phase: 'Assessment', icon: '📊', desc: 'Evaluate current capabilities' },
              { phase: 'Ideation', icon: '💡', desc: 'Generate improvement ideas' },
              { phase: 'Generation', icon: '⚙️', desc: 'Create new skills/prompts' },
              { phase: 'Evaluation', icon: '✅', desc: 'Test new capabilities' },
              { phase: 'Integration', icon: '🔗', desc: 'Merge successful changes' },
              { phase: 'Validation', icon: '🛡️', desc: 'Verify improvements' }
            ].map((step, idx) => (
              <div key={idx} className="text-center">
                <div className="text-3xl mb-2">{step.icon}</div>
                <div className="font-semibold text-gray-900 dark:text-gray-100 text-sm">{step.phase}</div>
                <div className="text-xs text-octo-text-tertiary mt-1">{step.desc}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Create Agent Modal */}
        {showCreateModal && (
          <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4" onClick={() => setShowCreateModal(false)}>
            <div className="bg-octo-bg-primary rounded-xl shadow-2xl max-w-lg w-full p-6" onClick={(e) => e.stopPropagation()}>
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                  🤖 Create New Evolving Agent
                </h2>
                <button
                  onClick={() => setShowCreateModal(false)}
                  className="text-octo-text-tertiary hover:text-gray-900 dark:text-gray-100 text-2xl"
                >
                  ×
                </button>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-900 dark:text-gray-100 mb-2">
                    Agent Name *
                  </label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                    placeholder="Enter agent name"
                    className="w-full px-4 py-2 bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/50 text-gray-900 dark:text-gray-100"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-900 dark:text-gray-100 mb-2">
                      Agent Type *
                    </label>
                    <select
                      value={formData.agent_type}
                      onChange={(e) => setFormData({...formData, agent_type: e.target.value})}
                      className="w-full px-4 py-2 bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/50 text-gray-900 dark:text-gray-100"
                    >
                      {agentTypes.map((type) => (
                        <option key={type.id} value={type.id}>
                          {getAgentTypeIcon(type.id)} {type.name}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-900 dark:text-gray-100 mb-2">
                      Model
                    </label>
                    <select
                      value={formData.model_name}
                      onChange={(e) => setFormData({...formData, model_name: e.target.value})}
                      className="w-full px-4 py-2 bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/50 text-gray-900 dark:text-gray-100"
                    >
                      <option value="gpt-4">GPT-4</option>
                      <option value="gpt-4-turbo">GPT-4 Turbo</option>
                      <option value="claude-3-opus">Claude 3 Opus</option>
                      <option value="claude-3-sonnet">Claude 3 Sonnet</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-900 dark:text-gray-100 mb-2">
                    Visibility
                  </label>
                  <select
                    value={formData.visibility}
                    onChange={(e) => setFormData({...formData, visibility: e.target.value})}
                    className="w-full px-4 py-2 bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/50 text-gray-900 dark:text-gray-100"
                  >
                    <option value="private">Private</option>
                    <option value="public">Public</option>
                    <option value="shared">Shared</option>
                  </select>
                </div>
              </div>

              <div className="flex justify-end gap-3 mt-6 pt-6 border-t border-gray-300 dark:border-gray-600">
                <button
                  onClick={() => setShowCreateModal(false)}
                  className="btn btn-secondary"
                >
                  Cancel
                </button>
                <button
                  onClick={handleCreateAgent}
                  disabled={!formData.name}
                  className="btn btn-primary"
                >
                  Create Agent
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Execute Task Modal */}
        {showTaskModal && (
          <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4" onClick={() => setShowTaskModal(false)}>
            <div className="bg-octo-bg-primary rounded-xl shadow-2xl max-w-lg w-full p-6" onClick={(e) => e.stopPropagation()}>
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                  ▶️ Execute Task
                </h2>
                <button
                  onClick={() => setShowTaskModal(false)}
                  className="text-octo-text-tertiary hover:text-gray-900 dark:text-gray-100 text-2xl"
                >
                  ×
                </button>
              </div>

              {selectedAgent && (
                <div className="mb-4 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                  <div className="text-sm text-octo-text-tertiary">Selected Agent:</div>
                  <div className="font-semibold text-gray-900 dark:text-gray-100">
                    {getAgentTypeIcon(selectedAgent.config?.agent_type)} {selectedAgent.name}
                  </div>
                </div>
              )}

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-900 dark:text-gray-100 mb-2">
                    Task Description *
                  </label>
                  <textarea
                    value={taskData.task_description}
                    onChange={(e) => setTaskData({...taskData, task_description: e.target.value})}
                    rows={3}
                    placeholder="Describe the task you want the agent to perform..."
                    className="w-full px-4 py-2 bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/50 text-gray-900 dark:text-gray-100"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-900 dark:text-gray-100 mb-2">
                    Task Type
                  </label>
                  <select
                    value={taskData.task_type}
                    onChange={(e) => setTaskData({...task_data, task_type: e.target.value})}
                    className="w-full px-4 py-2 bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/50 text-gray-900 dark:text-gray-100"
                  >
                    <option value="general">General</option>
                    <option value="data_analysis">Data Analysis</option>
                    <option value="research">Research</option>
                    <option value="code_generation">Code Generation</option>
                    <option value="communication">Communication</option>
                  </select>
                </div>
              </div>

              <div className="flex justify-end gap-3 mt-6 pt-6 border-t border-gray-300 dark:border-gray-600">
                <button
                  onClick={() => setShowTaskModal(false)}
                  className="btn btn-secondary"
                >
                  Cancel
                </button>
                <button
                  onClick={handleExecuteTask}
                  disabled={!taskData.task_description.trim()}
                  className="btn btn-primary"
                >
                  Execute Task
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default EvolutionEngine
