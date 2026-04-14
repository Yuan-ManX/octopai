import React, { useState, useEffect } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'

const AgentDetail = () => {
  const { agentId } = useParams()
  const navigate = useNavigate()
  
  const [agent, setAgent] = useState(null)
  const [skills, setSkills] = useState([])
  const [performanceHistory, setPerformanceHistory] = useState([])
  const [evolutionTree, setEvolutionTree] = useState([])
  const [feedbackBuffer, setFeedbackBuffer] = useState([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('overview')
  const [evolving, setEvolving] = useState(false)

  useEffect(() => {
    if (agentId) {
      fetchAgentDetail()
      fetchAgentSkills()
      fetchPerformanceHistory()
      fetchEvolutionTree()
      fetchFeedback()
    }
  }, [agentId])

  const fetchAgentDetail = async () => {
    try {
      const response = await fetch(`http://localhost:3005/api/evolution/agents/${agentId}`)
      if (response.ok) {
        const data = await response.json()
        setAgent(data.agent)
      }
    } catch (error) {
      console.error('Error fetching agent:', error)
    }
  }

  const fetchAgentSkills = async () => {
    try {
      const response = await fetch(`http://localhost:3005/api/evolution/agents/${agentId}/skills`)
      if (response.ok) {
        const data = await response.json()
        setSkills(data.skills || [])
      }
    } catch (error) {
      console.error('Error fetching skills:', error)
    }
  }

  const fetchPerformanceHistory = async () => {
    try {
      const response = await fetch(`http://localhost:3005/api/evolution/agents/${agentId}/performance`)
      if (response.ok) {
        const data = await response.json()
        setPerformanceHistory(data.performance_history || [])
        setLoading(false)
      }
    } catch (error) {
      console.error('Error fetching performance:', error)
      setLoading(false)
    }
  }

  const fetchEvolutionTree = async () => {
    try {
      const response = await fetch(`http://localhost:3005/api/evolution/agents/${agentId}/evolution-tree`)
      if (response.ok) {
        const data = await response.json()
        setEvolutionTree(data.evolution_tree || [])
      }
    } catch (error) {
      console.error('Error fetching evolution tree:', error)
    }
  }

  const fetchFeedback = async () => {
    try {
      const response = await fetch(`http://localhost:3005/api/evolution/agents/${agentId}/feedback`)
      if (response.ok) {
        const data = await response.json()
        setFeedbackBuffer(data.feedback_buffer || [])
      }
    } catch (error) {
      console.error('Error fetching feedback:', error)
    }
  }

  const handleStartEvolution = async () => {
    setEvolving(true)
    try {
      await fetch(`http://localhost:3005/api/evolution/agents/${agentId}/evolve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          strategy: 'feedback_descent',
          learning_rate: 0.1,
          exploration_rate: 0.3,
          max_iterations: 50
        })
      })
      
      setTimeout(() => {
        fetchAgentDetail()
        fetchPerformanceHistory()
        fetchEvolutionTree()
        fetchAgentSkills()
        setEvolving(false)
      }, 5000)
    } catch (error) {
      console.error('Error starting evolution:', error)
      setEvolving(false)
    }
  }

  const handleExecuteTask = async () => {
    const taskDescription = prompt('Enter task description:')
    if (!taskDescription) return

    try {
      await fetch(`http://localhost:3005/api/evolution/agents/${agentId}/tasks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          task_description: taskDescription,
          task_type: 'general'
        })
      })
      
      setTimeout(() => {
        fetchAgentDetail()
        fetchPerformanceHistory()
        fetchFeedback()
      }, 1500)
    } catch (error) {
      console.error('Error executing task:', error)
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

  const getGradeColor = (grade) => {
    const colors = { S: 'text-yellow-400', A: 'text-green-400', B: 'text-blue-400', C: 'text-orange-400', D: 'text-red-400' }
    return colors[grade] || 'text-gray-400'
  }

  const getSkillTypeColor = (type) => {
    const colors = {
      task_execution: 'bg-blue-500/10 text-blue-400',
      code_generation: 'bg-purple-500/10 text-purple-400',
      data_analysis: 'bg-cyan-500/10 text-cyan-400',
      research: 'bg-emerald-500/10 text-emerald-400',
      communication: 'bg-pink-500/10 text-pink-400',
      tool_use: 'bg-orange-500/10 text-orange-400',
      custom: 'bg-gray-500/10 text-gray-400'
    }
    return colors[type] || colors.custom
  }

  if (loading && !agent) {
    return (
      <div className="min-h-screen py-8">
        <div className="max-w-7xl mx-auto px-6">
          <div className="animate-pulse space-y-4">
            <div className="h-8 bg-gray-50 dark:bg-gray-800 rounded w-1/3"></div>
            <div className="h-64 bg-gray-50 dark:bg-gray-800 rounded"></div>
            <div className="grid grid-cols-3 gap-4">
              <div className="h-40 bg-gray-50 dark:bg-gray-800 rounded"></div>
              <div className="h-40 bg-gray-50 dark:bg-gray-800 rounded"></div>
              <div className="h-40 bg-gray-50 dark:bg-gray-800 rounded"></div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (!agent) {
    return (
      <div className="min-h-screen py-8 flex items-center justify-center">
        <div className="card p-12 text-center">
          <div className="text-6xl mb-4">🔍</div>
          <h2 className="text-xl font-semibold mb-2">Agent Not Found</h2>
          <p className="text-octo-text-secondary mb-4">The agent you are looking for does not exist</p>
          <Link to="/evolution-engine" className="btn btn-primary">Back to Agents</Link>
        </div>
      </div>
    )
  }

  const tabs = [
    { id: 'overview', label: 'Overview', icon: '📊' },
    { id: 'skills', label: `Skills (${skills.length})`, icon: '⚡' },
    { id: 'evolution', label: 'Evolution History', icon: '🧬' },
    { id: 'performance', label: 'Performance', icon: '📈' },
    { id: 'feedback', label: 'Feedback Signals', icon: '📡' }
  ]

  return (
    <div className="min-h-screen py-8">
      <div className="max-w-7xl mx-auto px-6">
        {/* Back Navigation */}
        <Link to="/evolution-engine" className="inline-flex items-center gap-2 text-gray-500 dark:text-gray-400 hover:text-violet-600 dark:text-violet-400 transition-colors mb-6">
          ← Back to Agents
        </Link>

        {/* Agent Header */}
        <div className="card p-8 mb-6 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-purple-500/5 to-transparent rounded-full -translate-y-32 translate-x-32"></div>
          
          <div className="relative">
            <div className="flex items-start justify-between mb-6">
              <div>
                <div className="flex items-center gap-3 mb-3 flex-wrap">
                  <span className={`px-3 py-1 rounded-lg text-sm font-medium border ${getStatusColor(agent.status)}`}>
                    {agent.status === 'evolving' ? '🧬 Evolving...' : 
                     agent.status === 'running' ? '🚀 Running' :
                     agent.status === 'idle' ? '💤 Idle' : agent.status}
                  </span>
                  <span className={`px-3 py-1 rounded-lg text-sm font-medium ${
                    agent.visibility === 'public' ? 'bg-green-500/10 text-green-500' : 'bg-yellow-500/10 text-yellow-500'
                  }`}>
                    {agent.visibility}
                  </span>
                  {agent.config?.evolution_config?.strategy && (
                    <span className="px-3 py-1 rounded-lg text-sm font-medium bg-indigo-500/10 text-indigo-400">
                      Strategy: {agent.config.evolution_config.strategy.replace('_', ' ')}
                    </span>
                  )}
                </div>
                <div className="flex items-center gap-4 mt-4">
                  <div className="w-16 h-16 bg-gradient-to-br from-violet-600 via-purple-600 to-fuchsia-600 rounded-2xl flex items-center justify-center text-white text-3xl shadow-2xl shadow-purple-500/40 animate-pulse-subtle ring-4 ring-purple-500/20 relative overflow-hidden shrink-0">
                    <span className="relative z-10">🤖</span>
                    <div className="absolute inset-0 bg-white/10 animate-pulse"></div>
                  </div>
                  <div>
                    <h1 className="text-5xl font-black bg-gradient-to-r from-blue-600 via-cyan-500 to-blue-700 dark:from-blue-400 dark:via-cyan-300 dark:to-blue-400 bg-clip-text text-transparent mb-3 tracking-wide drop-shadow-xl filter">
                      {agent.name}
                    </h1>
                    <p className="text-gray-700 dark:text-gray-300 text-base font-medium leading-relaxed max-w-xl">
                      Type: <span className="font-bold capitalize">{agent.config?.agent_type}</span> •
                      Model: <span className="font-mono text-sm">{agent.config?.model_name}</span> •
                      Generation: <span className="bg-gradient-to-r from-purple-500 to-pink-500 bg-clip-text text-transparent font-black">Gen {agent.current_generation}</span>
                    </p>
                  </div>
                </div>
              </div>
              
              <div className="flex gap-3">
                <button
                  onClick={handleExecuteTask}
                  disabled={agent.status === 'evolving'}
                  className="btn btn-secondary"
                >
                  ▶️ Run Task
                </button>
                <button
                  onClick={handleStartEvolution}
                  disabled={evolving || agent.status === 'evolving'}
                  className={`btn ${evolving ? 'animate-pulse' : ''}`}
                >
                  🧬 {evolving ? 'Evolving...' : 'Start Evolution'}
                </button>
              </div>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
              <div className="bg-gray-50 dark:bg-gray-800/50 rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-green-500">{agent.total_tasks_completed || 0}</div>
                <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">Tasks Done</div>
              </div>
              <div className="bg-gray-50 dark:bg-gray-800/50 rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-red-400">{agent.total_tasks_failed || 0}</div>
                <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">Failed</div>
              </div>
              <div className="bg-gray-50 dark:bg-gray-800/50 rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-purple-500">{agent.total_evolutions || 0}</div>
                <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">Evolutions</div>
              </div>
              <div className="bg-gray-50 dark:bg-gray-800/50 rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-blue-500">{agent.total_skills || 0}</div>
                <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">Total Skills</div>
              </div>
              <div className="bg-gray-50 dark:bg-gray-800/50 rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-yellow-500">{(agent.average_quality || 0).toFixed(1)}</div>
                <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">Avg Quality</div>
              </div>
              <div className="bg-gray-50 dark:bg-gray-800/50 rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-emerald-500">{(agent.experience_points || 0).toFixed(0)}</div>
                <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">XP Points</div>
              </div>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-2 rounded-lg font-medium text-sm whitespace-nowrap transition-all ${
                activeTab === tab.id
                  ? 'bg-violet-600 text-white shadow-lg shadow-violet-500/25'
                  : 'bg-gray-50 dark:bg-gray-800 text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:text-gray-100'
              }`}
            >
              {tab.icon} {tab.label}
            </button>
          ))}
        </div>

        {/* Tab Content */}
        {activeTab === 'overview' && (
          <div className="space-y-6">
            {/* Recent Evolution Runs */}
            <div className="card p-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">🧬 Recent Evolution Runs</h3>
              {agent.evolution_runs && agent.evolution_runs.length > 0 ? (
                <div className="space-y-3">
                  {[...agent.evolution_runs].reverse().slice(0, 5).map((run) => (
                    <div key={run.run_id} className="bg-gray-50 dark:bg-gray-800/50 rounded-lg p-4">
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center gap-3">
                          <span className={`px-2 py-0.5 rounded text-xs font-medium border ${getStatusColor(run.status)}`}>
                            {run.status}
                          </span>
                          <span className="text-sm text-gray-500 dark:text-gray-400">
                            Phase: <span className="capitalize text-gray-900 dark:text-gray-100">{run.current_phase?.replace('_', ' ')}</span>
                          </span>
                        </div>
                        <div className="text-sm text-gray-500 dark:text-gray-400">
                          {run.duration_seconds ? `${run.duration_seconds}s` : 'In Progress'}
                        </div>
                      </div>
                      
                      <div className="grid grid-cols-4 gap-4 mt-3 text-center">
                        <div>
                          <div className="text-lg font-bold text-purple-500">{run.skills_created || 0}</div>
                          <div className="text-[10px] text-gray-500 dark:text-gray-400">Skills Created</div>
                        </div>
                        <div>
                          <div className="text-lg font-bold text-green-500">{run.skills_improved || 0}</div>
                          <div className="text-[10px] text-gray-500 dark:text-gray-400">Improved</div>
                        </div>
                        <div>
                          <div className="text-lg font-bold text-blue-500">{(run.overall_improvement || 0).toFixed(1)}%</div>
                          <div className="text-[10px] text-gray-500 dark:text-gray-400">Improvement</div>
                        </div>
                        <div>
                          <div className="text-lg font-bold text-yellow-500">{run.iterations_completed || 0}</div>
                          <div className="text-[10px] text-gray-500 dark:text-gray-400">Iterations</div>
                        </div>
                      </div>

                      {run.validation_results && (
                        <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
                          <div className="flex items-center gap-4 text-xs text-gray-500 dark:text-gray-400">
                            <span>Stability: {(run.validation_results.stability_score || 0).toFixed(2)}</span>
                            <span>Converged: {run.validation_results.converged ? '✅ Yes' : '⏳ No'}</span>
                            <span>{run.validation_results.performance_delta || ''}</span>
                          </div>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8 text-gray-500 dark:text-gray-400">
                  No evolution runs yet. Click "Start Evolution" to begin!
                </div>
              )}
            </div>

            {/* Recent Tasks */}
            <div className="card p-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">📋 Recent Task Executions</h3>
              {agent.task_executions && agent.task_executions.length > 0 ? (
                <div className="space-y-2">
                  {[...agent.task_executions].reverse().slice(0, 8).map((exec) => (
                    <div key={exec.execution_id} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800/30 rounded-lg">
                      <div className="flex-1 min-w-0 mr-4">
                        <div className="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">
                          {exec.task_description}
                        </div>
                        <div className="flex items-center gap-3 mt-1 text-xs text-gray-500 dark:text-gray-400">
                          <span className={`px-1.5 py-0.5 rounded ${exec.success ? 'bg-green-500/10 text-green-500' : 'bg-red-500/10 text-red-500'}`}>
                            {exec.success ? '✅ Success' : '❌ Failed'}
                          </span>
                          <span>Type: {exec.task_type}</span>
                          <span>{exec.duration_ms}ms</span>
                          <span>{exec.tokens_used} tokens</span>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-lg font-bold text-violet-600 dark:text-violet-400">{(exec.quality_score || 0).toFixed(1)}</div>
                        <div className="text-[10px] text-gray-500 dark:text-gray-400">Quality</div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8 text-gray-500 dark:text-gray-400">
                  No tasks executed yet.
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'skills' && (
          <div className="card p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">⚡ Agent Skills ({skills.length})</h3>
              <span className="text-sm text-gray-500 dark:text-gray-400">
                Active: {skills.filter(s => s.is_active).length}/{skills.length}
              </span>
            </div>
            
            {skills.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {skills.map((skill) => {
                  const eval_data = skill.evaluation || {}
                  return (
                    <div key={skill.skill_id} className="bg-gray-50 dark:bg-gray-800/30 rounded-lg p-5 border border-transparent hover:border-purple-500/30 transition-all">
                      <div className="flex items-start justify-between mb-3">
                        <div>
                          <h4 className="font-semibold text-gray-900 dark:text-gray-100">{skill.name}</h4>
                          <span className={`inline-block px-2 py-0.5 rounded text-xs mt-1 ${getSkillTypeColor(skill.skill_type)}`}>
                            {skill.skill_type?.replace('_', ' ')}
                          </span>
                        </div>
                        <div className="text-right">
                          <span className={`text-2xl font-bold ${getGradeColor(eval_data.grade || 'C')}`}>
                            {eval_data.grade || 'C'}
                          </span>
                          <div className="text-[10px] text-gray-500 dark:text-gray-400">Grade</div>
                        </div>
                      </div>

                      <p className="text-sm text-octo-text-secondary mb-4 line-clamp-2">{skill.description}</p>

                      {eval_data.overall !== undefined && (
                        <div className="space-y-2">
                          <div className="flex items-center justify-between text-xs">
                            <span className="text-gray-500 dark:text-gray-400">Overall Score</span>
                            <div className="flex items-center gap-2">
                              <div className="w-24 h-2 bg-octo-bg-tertiary rounded-full overflow-hidden">
                                <div 
                                  className="h-full bg-gradient-to-r from-purple-500 to-pink-500 rounded-full"
                                  style={{ width: `${Math.min(eval_data.overall * 10, 100)}%` }}
                                ></div>
                              </div>
                              <span className="font-mono text-gray-900 dark:text-gray-100">{eval_data.overall.toFixed(1)}</span>
                            </div>
                          </div>
                          
                          <div className="grid grid-cols-3 gap-2 text-center text-xs">
                            <div className="bg-octo-bg-tertiary/50 rounded p-2">
                              <div className="font-semibold text-blue-400">{(eval_data.quality || 0).toFixed(1)}</div>
                              <div className="text-gray-500 dark:text-gray-400">Quality</div>
                            </div>
                            <div className="bg-octo-bg-tertiary/50 rounded p-2">
                              <div className="font-semibold text-green-400">{(eval_data.performance || 0).toFixed(1)}</div>
                              <div className="text-gray-500 dark:text-gray-400">Perf</div>
                            </div>
                            <div className="bg-octo-bg-tertiary/50 rounded p-2">
                              <div className="font-semibold text-yellow-400">{(eval_data.reliability || 0).toFixed(1)}</div>
                              <div className="text-gray-500 dark:text-gray-400">Reliable</div>
                            </div>
                          </div>

                          <div className="grid grid-cols-3 gap-2 text-center text-xs">
                            <div className="bg-octo-bg-tertiary/50 rounded p-2">
                              <div className="font-semibold text-pink-400">{(eval_data.novelty || 0).toFixed(1)}</div>
                              <div className="text-gray-500 dark:text-gray-400">Novelty</div>
                            </div>
                            <div className="bg-octo-bg-tertiary/50 rounded p-2">
                              <div className="font-semibold text-cyan-400">{(skill.adaptation_score || 0).toFixed(1)}</div>
                              <div className="text-gray-500 dark:text-gray-400">Adapt</div>
                            </div>
                            <div className="bg-octo-bg-tertiary/50 rounded p-2">
                              <div className="font-semibold text-emerald-400">{(skill.generalization_score || 0).toFixed(1)}</div>
                              <div className="text-gray-500 dark:text-gray-400">General</div>
                            </div>
                          </div>
                        </div>
                      )}

                      <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700 flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
                        <span>v{skill.version} • {skill.evolution_count} evolutions</span>
                        <span>Success: {(skill.success_rate * 100).toFixed(0)}%</span>
                      </div>
                    </div>
                  )
                })}
              </div>
            ) : (
              <div className="text-center py-12 text-gray-500 dark:text-gray-400">
                No skills available for this agent
              </div>
            )}
          </div>
        )}

        {activeTab === 'evolution' && (
          <div className="space-y-6">
            <div className="card p-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">🌳 Skill Evolution Tree</h3>
              {evolutionTree.length > 0 ? (
                <div className="relative">
                  <div className="absolute left-4 top-0 bottom-0 w-0.5 bg-gradient-to-b from-purple-500 via-pink-500 to-cyan-500"></div>
                  <div className="space-y-4 pl-10">
                    {evolutionTree.map((node, idx) => (
                      <div key={idx} className="relative">
                        <div className="absolute -left-6 top-3 w-3 h-3 rounded-full bg-purple-500 border-2 border-octo-bg-primary"></div>
                        <div className="bg-gray-50 dark:bg-gray-800/50 rounded-lg p-4">
                          <div className="flex items-center justify-between">
                            <div>
                              <span className="font-medium text-gray-900 dark:text-gray-100">{node.name}</span>
                              <span className="ml-2 px-2 py-0.5 bg-purple-500/10 text-purple-400 rounded text-xs">
                                Gen {node.generation}
                              </span>
                            </div>
                            <span className="text-xs text-gray-500 dark:text-gray-400">
                              {new Date(node.timestamp).toLocaleString()}
                            </span>
                          </div>
                          {node.source_template && (
                            <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                              Source Template: {node.source_template}
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="text-center py-12 text-gray-500 dark:text-gray-400">
                  Start evolution to build your skill tree!
                </div>
              )}
            </div>

            <div className="card p-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">🔄 Full Evolution Timeline</h3>
              {agent.evolution_runs && agent.evolution_runs.length > 0 ? (
                <div className="space-y-4">
                  {agent.evolution_runs.map((run, idx) => (
                    <div key={run.run_id} className="border-l-2 border-purple-500/30 pl-4">
                      <div className="flex items-center gap-3 mb-2">
                        <span className="text-sm font-bold text-purple-400">Run #{idx + 1}</span>
                        <span className={`px-2 py-0.5 rounded text-xs ${getStatusColor(run.status)}`}>{run.status}</span>
                        <span className="text-xs text-gray-500 dark:text-gray-400">
                          {run.started_at ? new Date(run.started_at).toLocaleString() : ''}
                        </span>
                      </div>
                      
                      {run.phase_timings && Object.keys(run.phase_timings).length > 0 && (
                        <div className="mt-2 space-y-1">
                          {Object.entries(run.phase_timings).map(([phase, duration]) => (
                            <div key={phase} className="flex items-center gap-2 text-xs">
                              <span className="w-24 text-gray-500 dark:text-gray-400 capitalize">{phase.replace('_', ' ')}</span>
                              <div className="flex-1 h-1.5 bg-octo-bg-tertiary rounded-full overflow-hidden">
                                <div 
                                  className="h-full bg-gradient-to-r from-purple-500 to-pink-500 rounded-full"
                                  style={{ width: `${Math.min(duration / 50 * 100, 100)}%` }}
                                ></div>
                              </div>
                              <span className="w-12 text-right text-gray-500 dark:text-gray-400">{duration}ms</span>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8 text-gray-500 dark:text-gray-400">No evolution history yet</div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'performance' && (
          <div className="card p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-6">📈 Performance Trend</h3>
            
            {performanceHistory.length > 0 ? (
              <>
                <div className="mb-6">
                  <div className="flex items-end gap-2 h-48">
                    {performanceHistory.slice(-15).map((point, idx) => {
                      const height = Math.max(point.quality * 10, 5)
                      return (
                        <div key={idx} className="flex-1 flex flex-col items-center">
                          <div 
                            className="w-full bg-gradient-to-t from-purple-600 to-pink-500 rounded-t transition-all hover:opacity-80"
                            style={{ height: `${height}%`, minHeight: '4px' }}
                          ></div>
                          <span className="text-[9px] text-gray-500 dark:text-gray-400 mt-1">G{point.generation}</span>
                        </div>
                      )
                    })}
                  </div>
                </div>

                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="border-b border-gray-200 dark:border-gray-700">
                        <th className="text-left py-2 px-3 text-gray-500 dark:text-gray-400 font-medium">Generation</th>
                        <th className="text-right py-2 px-3 text-gray-500 dark:text-gray-400 font-medium">Quality</th>
                        <th className="text-right py-2 px-3 text-gray-500 dark:text-gray-400 font-medium">Improvement</th>
                        <th className="text-right py-2 px-3 text-gray-500 dark:text-gray-400 font-medium">Skills</th>
                        <th className="text-left py-2 px-3 text-gray-500 dark:text-gray-400 font-medium">Timestamp</th>
                      </tr>
                    </thead>
                    <tbody>
                      {[...performanceHistory].reverse().slice(0, 10).map((point, idx) => (
                        <tr key={idx} className="border-b border-gray-200 dark:border-gray-700/50 hover:bg-gray-50 dark:bg-gray-800/30">
                          <td className="py-2 px-3 font-medium text-purple-400">Gen {point.generation}</td>
                          <td className="py-2 px-3 text-right font-mono">{point.quality?.toFixed(2)}</td>
                          <td className="py-2 px-3 text-right text-green-400">+{point.improvement?.toFixed(1)}%</td>
                          <td className="py-2 px-3 text-right">{point.skills_count}</td>
                          <td className="py-2 px-3 text-gray-500 dark:text-gray-400 text-xs">
                            {new Date(point.timestamp).toLocaleString()}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </>
            ) : (
              <div className="text-center py-12 text-gray-500 dark:text-gray-400">
                Execute tasks and run evolutions to see performance trends!
              </div>
            )}
          </div>
        )}

        {activeTab === 'feedback' && (
          <div className="card p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">📡 Feedback Signal Buffer</h3>
            
            {feedbackBuffer.length > 0 ? (
              <div className="space-y-2">
                {feedbackBuffer.map((signal, idx) => (
                  <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800/30 rounded-lg">
                    <div className="flex items-center gap-3">
                      <span className={`w-2 h-2 rounded-full ${
                        signal.signal_type === 'skill_improvement' ? 'bg-green-500' : 'bg-blue-500'
                      }`}></span>
                      <span className="text-sm font-medium text-gray-900 dark:text-gray-100 capitalize">
                        {signal.signal_type?.replace('_', ' ')}
                      </span>
                      {signal.skill_id && (
                        <span className="text-xs text-gray-500 dark:text-gray-400 font-mono">
                          {signal.skill_id.substring(0, 8)}...
                        </span>
                      )}
                    </div>
                    <div className="flex items-center gap-4">
                      <span className={`text-sm font-bold ${
                        signal.delta >= 0 ? 'text-green-400' : 'text-red-400'
                      }`}>
                        {signal.delta >= 0 ? '+' : ''}{signal.delta?.toFixed(3)}
                      </span>
                      <span className="text-xs text-gray-500 dark:text-gray-400">
                        {new Date(signal.timestamp).toLocaleTimeString()}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-12 text-gray-500 dark:text-gray-400">
                <div className="text-4xl mb-3">📡</div>
                No feedback signals collected yet.
                <br />
                Run tasks and evolutions to generate feedback signals.
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default AgentDetail
