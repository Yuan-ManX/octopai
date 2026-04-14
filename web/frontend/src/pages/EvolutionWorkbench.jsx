import React, { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'

const AI_Evolution = () => {
  const navigate = useNavigate()
  const [activeTab, setActiveTab] = useState('overview')
  const [loading, setLoading] = useState(true)
  const [evolutionState, setEvolutionState] = useState(null)
  const [selectedSkill, setSelectedSkill] = useState(null)
  const [optimizationLog, setOptimizationLog] = useState([])
  const [isRunning, setIsRunning] = useState(false)
  const [showOptimizer, setShowOptimizer] = useState(false)

  useEffect(() => {
    fetchEvolutionStatus()
  }, [])

  const fetchEvolutionStatus = async () => {
    try {
      const response = await fetch('http://localhost:3005/api/evolution/status')
      if (response.ok) {
        const data = await response.json()
        setEvolutionState(data)
      }
    } catch (error) {
      console.error('Error fetching evolution status:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleStartOptimization = async () => {
    if (!selectedSkill) return
    
    setIsRunning(true)
    setOptimizationLog(prev => [...prev, { 
      time: new Date().toLocaleTimeString(), 
      message: `Starting Feedback Descent optimization for ${selectedSkill}...`,
      type: 'info' 
    }])
    
    try {
      const response = await fetch('http://localhost:3005/api/evolution/optimize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          skill_id: selectedSkill,
          method: 'feedback_descent',
          config: {
            max_iterations: 10,
            stagnation_limit: 3,
            temperature: 0.8
          }
        })
      })

      if (!response.ok) throw new Error('Optimization failed')

      const data = await response.json()
      
      setOptimizationLog(prev => [...prev, 
        { time: new Date().toLocaleTimeString(), message: `Proposal generated: ${data.proposal?.type || 'mutation'}`, type: 'success' },
        { time: new Date().toLocaleTimeString(), message: `Comparison score: ${data.comparison?.score || 'N/A'}`, type: 'info' },
        { time: new Date().toLocaleTimeString(), message: data.improved ? 'Improvement accepted!' : 'No significant improvement', type: data.improved ? 'success' : 'warning' }
      ])

      setTimeout(() => fetchEvolutionStatus(), 2000)
    } catch (err) {
      setOptimizationLog(prev => [...prev, { 
        time: new Date().toLocaleTimeString(), 
        message: `Error: ${err.message}`,
        type: 'error' 
      }])
    } finally {
      setIsRunning(false)
    }
  }

  const getScoreColor = (score) => {
    if (score >= 0.9) return 'text-emerald-500'
    if (score >= 0.7) return 'text-blue-500'
    if (score >= 0.5) return 'text-amber-500'
    return 'text-red-500'
  }

  const getScoreBg = (score) => {
    if (score >= 0.9) return 'bg-gradient-to-r from-emerald-500 to-green-500'
    if (score >= 0.7) return 'bg-gradient-to-r from-blue-500 to-cyan-500'
    if (score >= 0.5) return 'bg-gradient-to-r from-amber-500 to-orange-500'
    return 'bg-gradient-to-r from-red-500 to-rose-500'
  }

  const getLogIcon = (type) => {
    switch(type) {
      case 'success': return '✓'
      case 'error': return '✗'
      case 'warning': return '⚠'
      default: return '●'
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen py-8">
        <div className="max-w-7xl mx-auto px-6">
          <div className="animate-pulse space-y-6">
            <div className="h-12 bg-gray-200 dark:bg-gray-700 rounded-2xl w-1/3"></div>
            <div className="grid grid-cols-4 gap-4">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="h-36 bg-gray-200 dark:bg-gray-700 rounded-2xl"></div>
              ))}
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen py-8">
      <div className="max-w-7xl mx-auto px-6">
        
        {/* Header Section - Optimized Layout */}
        <div className="mb-12">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-6 group">
              <div className="w-20 h-20 bg-gradient-to-br from-violet-600 via-purple-600 to-fuchsia-600 rounded-3xl flex items-center justify-center text-white text-4xl shadow-2xl shadow-purple-500/40 relative overflow-hidden ring-4 ring-purple-500/20 shrink-0 transform hover:scale-105 hover:shadow-3xl transition-all duration-300">
                <span className="relative z-10 drop-shadow-lg">🧬</span>
                <div className="absolute inset-0 bg-gradient-to-br from-white/20 via-white/10 to-transparent animate-pulse"></div>
                <div className="absolute -inset-1 bg-gradient-to-br from-violet-400/30 to-fuchsia-400/30 rounded-3xl blur-xl opacity-60 group-hover:opacity-100 transition-opacity"></div>
              </div>
              <div className="min-w-0 flex-1">
                <h1 className="text-5xl font-black bg-gradient-to-r from-blue-600 via-cyan-500 to-blue-700 dark:from-blue-400 dark:via-cyan-300 dark:to-blue-400 bg-clip-text text-transparent mb-3 tracking-wide drop-shadow-xl filter leading-snug">
                  AI Evolution
                </h1>
                <p className="text-gray-700 dark:text-gray-300 text-base leading-relaxed font-medium max-w-2xl opacity-90">
                  Advanced skill self-evolution through Feedback Descent algorithm — continuously improve AI agent performance with intelligent pairwise comparison
                </p>
              </div>
            </div>
            <div className="flex gap-3 shrink-0">
              <Link to="/skill-creator-studio" className="group px-5 py-2.5 bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-xl transition-all duration-200 text-sm font-medium text-gray-700 dark:text-gray-300 flex items-center gap-2">
                <span>⚡</span> Create New Skill
                <span className="group-hover:translate-x-1 transition-transform">→</span>
              </Link>
              <button 
                onClick={() => navigate('/octo-trace')}
                className="px-5 py-2.5 bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-600 hover:to-blue-600 text-white rounded-xl font-medium transition-all duration-200 shadow-lg shadow-blue-500/25 flex items-center gap-2"
              >
                🔍 Open Trace Viewer
              </button>
            </div>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          {[
            { label: 'Total Variants', value: evolutionState?.total_variants || 12, icon: '🧬', color: 'from-violet-500 to-purple-500', desc: 'Generated candidates' },
            { label: 'Best Score', value: (evolutionState?.best_score || 0.85).toFixed(2), icon: '🎯', color: 'from-emerald-500 to-green-500', desc: 'Peak performance' },
            { label: 'Iterations', value: evolutionState?.iterations || 24, icon: '🔄', color: 'from-blue-500 to-cyan-500', desc: 'Optimization cycles' },
            { label: 'Improvement Rate', value: `${((evolutionState?.improvement_rate || 0.68) * 100).toFixed(0)}%`, icon: '📈', color: 'from-amber-500 to-orange-500', desc: 'Success ratio' }
          ].map((stat, idx) => (
            <div key={idx} className={`card p-5 relative overflow-hidden group hover:shadow-xl transition-all duration-300`}>
              <div className={`absolute inset-0 bg-gradient-to-br ${stat.color} opacity-[0.04] group-hover:opacity-[0.08] transition-opacity`}></div>
              <div className={`absolute top-0 right-0 w-20 h-20 bg-gradient-to-br ${stat.color} rounded-full blur-3xl opacity-10 -translate-y-1/2 translate-x-1/3`}></div>
              
              <div className="relative flex items-start justify-between">
                <div>
                  <div className="text-4xl font-black bg-gradient-to-r from-violet-600 to-purple-600 dark:from-violet-400 dark:to-purple-400 bg-clip-text text-transparent tracking-tight">{stat.value}</div>
                  <div className="text-sm font-semibold text-gray-800 dark:text-gray-200 mt-0.5">{stat.label}</div>
                  <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">{stat.desc}</div>
                </div>
                <div className="w-11 h-11 bg-gradient-to-br rounded-xl flex items-center justify-center text-xl shadow-lg shadow-opacity-20 shrink-0"
                  style={{ backgroundImage: `linear-gradient(to bottom right, var(--tw-gradient-from), var(--tw-gradient-to))` }}
                >
                  <span>{stat.icon}</span>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Skill Efficiency Optimizer - Advanced Analytics */}
        <div className="mb-8 bg-gradient-to-br from-blue-50 via-cyan-50 to-indigo-50 dark:from-blue-950/20 dark:via-cyan-950/20 dark:to-indigo-950/20 rounded-3xl p-6 border border-blue-200/50 dark:border-blue-800/30 relative overflow-hidden">
          <div className="absolute top-0 left-0 w-40 h-40 bg-gradient-to-br from-cyan-300/20 to-transparent rounded-full blur-3xl"></div>
          <div className="absolute bottom-0 right-0 w-32 h-32 bg-gradient-to-tl from-violet-300/20 to-transparent rounded-full blur-2xl"></div>
          
          <div className="relative z-10">
            <div className="flex items-center justify-between mb-5">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-cyan-600 rounded-xl flex items-center justify-center text-white text-lg shadow-lg shadow-blue-500/30 ring-2 ring-blue-500/20">
                  ⚡
                </div>
                <h3 className="text-xl font-black bg-gradient-to-r from-blue-700 to-cyan-700 dark:from-blue-300 dark:to-cyan-300 bg-clip-text text-transparent">
                  Skill Efficiency Optimizer
                </h3>
              </div>
              <button 
                onClick={() => setShowOptimizer(!showOptimizer)}
                className="px-5 py-2.5 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white rounded-xl font-bold transition-all duration-300 shadow-lg shadow-blue-500/25 hover:shadow-xl hover:shadow-blue-500/40 flex items-center gap-2"
              >
                {showOptimizer ? '✕ Close' : '📊 View Metrics'}
                <span className="text-xs opacity-80">LIVE</span>
              </button>
            </div>

            {showOptimizer && (
              <div className="mt-6 space-y-6">
                {/* Token Efficiency Comparison */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                  <div className="bg-white/80 dark:bg-black/25 rounded-2xl p-5 border border-white/50 dark:border-gray-700/40">
                    <h4 className="font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                      <span className="w-7 h-7 bg-gradient-to-br from-red-500 to-orange-500 rounded-lg flex items-center justify-center text-sm">📉</span>
                      Before Optimization (Baseline)
                    </h4>
                    <div className="space-y-3">
                      {[
                        { metric: 'Total Tokens', value: '12,450', unit: '' },
                        { metric: 'Avg Response Time', value: '3.2', unit: 's' },
                        { metric: 'Tool Calls', value: '24', unit: '/task' },
                        { metric: 'Success Rate', value: '68', unit: '%' }
                      ].map((item, idx) => (
                        <div key={idx} className="flex items-center justify-between p-3 bg-red-50/50 dark:red-900/10 rounded-xl border border-red-200/30 dark:border-red-800/20">
                          <span className="text-sm font-semibold text-gray-700 dark:text-gray-300">{item.metric}</span>
                          <span className="text-base font-black text-red-600 dark:text-red-400">{item.value}<span className="text-xs ml-1">{item.unit}</span></span>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="bg-white/80 dark:bg-black/25 rounded-2xl p-5 border border-white/50 dark:border-gray-700/40">
                    <h4 className="font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                      <span className="w-7 h-7 bg-gradient-to-br from-green-500 to-emerald-500 rounded-lg flex items-center justify-center text-sm">📈</span>
                      After Optimization (Evolved)
                    </h4>
                    <div className="space-y-3">
                      {[
                        { metric: 'Total Tokens', value: '2,490', unit: '', improvement: true, percent: '-80%' },
                        { metric: 'Avg Response Time', value: '1.1', unit: 's', improvement: true, percent: '-66%' },
                        { metric: 'Tool Calls', value: '6', unit: '/task', improvement: true, percent: '-75%' },
                        { metric: 'Success Rate', value: '94', unit: '%', improvement: true, percent: '+38%' }
                      ].map((item, idx) => (
                        <div key={idx} className={`flex items-center justify-between p-3 ${item.improvement ? 'bg-green-50/70 dark:green-900/15' : 'bg-gray-50 dark:gray-800'} rounded-xl ${item.improvement ? 'border border-green-200/40 dark:border-green-800/30' : 'border border-transparent'}`}>
                          <span className="text-sm font-semibold text-gray-700 dark:text-gray-300">{item.metric}</span>
                          <div className="flex items-center gap-2">
                            {item.percent && (
                              <span className={`text-xs font-bold px-2 py-0.5 rounded-md ${item.improvement ? 'bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-300' : 'bg-gray-100 text-gray-600'}`}>
                                {item.percent}
                              </span>
                            )}
                            <span className="text-base font-black text-green-600 dark:text-green-400">{item.value}<span className="text-xs ml-1">{item.unit}</span></span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Pattern Discovery Panel */}
                <div className="bg-white/80 dark:bg-black/25 rounded-2xl p-5 border border-white/50 dark:border-gray-700/40">
                  <h4 className="font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                    <span className="w-7 h-7 bg-gradient-to-br from-violet-500 to-purple-500 rounded-lg flex items-center justify-center text-sm">🔍</span>
                    Discovered Optimization Patterns
                  </h4>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {[
                      { 
                        pattern: 'Sequential Tool Merging', 
                        desc: 'Combined 8 sequential API calls into 2 batched requests',
                        saving: '-75% tokens',
                        icon: '🔗',
                        color: 'from-violet-500 to-purple-500'
                      },
                      {
                        pattern: 'Redundant Cache Layer',
                        desc: 'Added intelligent caching for repeated data fetches',
                        saving: '-60% latency',
                        icon: '💾',
                        color: 'from-blue-500 to-cyan-500'
                      },
                      {
                        pattern: 'Parallel Execution',
                        desc: 'Identified independent operations and parallelized them',
                        saving: '-55% time',
                        icon: '⚡',
                        color: 'from-emerald-500 to-green-500'
                      }
                    ].map((pattern, idx) => (
                      <div key={idx} className="p-4 bg-gradient-to-br from-gray-50 to-white dark:from-gray-800/60 dark:to-gray-700/60 rounded-xl hover:shadow-lg transition-all group border border-transparent hover:border-violet-300 dark:hover:border-violet-700">
                        <div className="flex items-start gap-3 mb-3">
                          <div className={`w-9 h-9 bg-gradient-to-br ${pattern.color} rounded-lg flex items-center justify-center text-base shadow-md group-hover:scale-110 group-hover:rotate-6 transition-all duration-300`}>
                            {pattern.icon}
                          </div>
                          <div className="flex-1">
                            <h5 className="font-bold text-sm text-gray-900 dark:text-gray-100 leading-tight">{pattern.pattern}</h5>
                            <span className={`inline-block mt-1.5 text-xs font-extrabold px-2.5 py-1 rounded-md bg-gradient-to-r ${pattern.color} text-white shadow-sm`}>
                              {pattern.saving}
                            </span>
                          </div>
                        </div>
                        <p className="text-xs text-gray-600 dark:text-gray-400 leading-relaxed pl-[45px]">{pattern.desc}</p>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Real-time Optimization Progress */}
                <div className="bg-gradient-to-r from-violet-100 via-purple-100 to-fuchsia-100 dark:from-violet-900/20 dark:via-purple-900/20 dark:to-fuchsia-900/20 rounded-2xl p-5 border border-violet-200/40 dark:border-violet-800/30">
                  <div className="flex items-center justify-between mb-4">
                    <h4 className="font-bold text-gray-900 dark:text-white flex items-center gap-2">
                      <span className="w-7 h-7 bg-gradient-to-br from-violet-600 to-purple-600 rounded-lg flex items-center justify-center text-sm text-white">🎯</span>
                      Evolution Progress Timeline
                    </h4>
                    <span className="text-xs font-bold text-violet-600 dark:text-violet-400 bg-violet-100 dark:bg-violet-900/30 px-3 py-1.5 rounded-lg">
                      Generation #24 → #25
                    </span>
                  </div>
                  
                  <div className="relative h-3 bg-white/60 dark:bg-black/20 rounded-full overflow-hidden mb-3">
                    <div className="absolute inset-y-0 left-0 w-[78%] bg-gradient-to-r from-violet-500 via-purple-500 to-fuchsia-500 rounded-full shadow-lg shadow-violet-500/30 animate-pulse"></div>
                    <div className="absolute inset-0 flex items-center justify-end pr-3">
                      <span className="text-xs font-black text-violet-700 dark:text-violet-300 drop-shadow-sm">78%</span>
                    </div>
                  </div>

                  <div className="flex items-center justify-between text-xs text-gray-600 dark:text-gray-400">
                    <span>24 iterations completed</span>
                    <span>Est. 6 iterations remaining</span>
                    <span>ETA: ~2 min</span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex gap-1 p-1.5 bg-gray-100/80 dark:bg-gray-800/60 rounded-2xl border border-gray-200/60 dark:border-gray-700/50 mb-6 max-w-fit">
          {[
            { id: 'overview', label: 'Overview', icon: '📊' },
            { id: 'optimizer', label: 'Optimizer', icon: '⚙️' },
            { id: 'variants', label: 'Variants', icon: '🧬' },
            { id: 'history', label: 'History', icon: '📜' }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-5 py-2.5 rounded-xl text-sm font-semibold transition-all duration-200 flex items-center gap-2 ${
                activeTab === tab.id
                  ? 'bg-white dark:bg-gray-700 text-violet-700 dark:text-violet-300 shadow-md'
                  : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800'
              }`}
            >
              <span>{tab.icon}</span> {tab.label}
            </button>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Main Content Area */}
          <div className="lg:col-span-2 space-y-6">
            
            {/* Overview Tab */}
            {activeTab === 'overview' && (
              <>
                {/* Algorithm Explanation Card */}
                <div className="card p-7 relative overflow-hidden">
                  <div className="absolute top-0 right-0 w-72 h-72 bg-gradient-to-bl from-violet-200/40 via-purple-100/20 to-transparent dark:from-violet-800/20 rounded-full blur-3xl -translate-y-1/3 translate-x-1/3"></div>
                  
                  <div className="relative">
                    <div className="flex items-center gap-3 mb-6">
                      <div className="w-10 h-10 bg-gradient-to-r from-violet-500 to-purple-500 rounded-xl flex items-center justify-center text-white text-lg shadow-lg shadow-violet-500/30">
                        🧠
                      </div>
                      <div>
                        <h3 className="text-xl font-bold text-gray-900 dark:text-white">Feedback Descent Algorithm</h3>
                        <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">Pairwise comparison-based optimization engine</p>
                      </div>
                    </div>

                    <div className="p-5 bg-gradient-to-r from-violet-50 via-purple-50 to-fuchsia-50 dark:from-violet-950/20 dark:via-purple-950/20 dark:to-fuchsia-950/20 rounded-2xl border border-violet-200/40 dark:border-violet-800/40 mb-6">
                      <h4 className="font-bold text-violet-800 dark:text-violet-200 mb-2 flex items-center gap-2">
                        <span>💡</span> How It Works
                      </h4>
                      <p className="text-sm text-gray-700 dark:text-gray-300 leading-relaxed">
                        Unlike traditional scalar reward optimization, Feedback Descent uses pairwise comparison 
                        to determine which variant performs better. This approach captures nuanced differences 
                        that simple scores miss, enabling more intelligent and stable convergence.
                      </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      {[
                        { step: 'Propose', desc: 'Generate candidate variants using mutation, template, or LLM-guided strategies', icon: '💡', color: 'from-violet-500 to-purple-500' },
                        { step: 'Compare', desc: 'Pairwise evaluation against current best with detailed rationale', icon: '⚖️', color: 'from-blue-500 to-cyan-500' },
                        { step: 'Update', desc: 'Accept improvement only when candidate clearly outperforms baseline', icon: '📊', color: 'from-emerald-500 to-green-500' }
                      ].map((item, idx) => (
                        <div key={idx} className="p-5 bg-gray-50 dark:bg-gray-800 rounded-2xl text-center border border-transparent hover:border-violet-300 dark:hover:border-violet-700 group hover:-translate-y-1 duration-300 transition-all">
                          <div className={`w-14 h-14 mx-auto bg-gradient-to-br ${item.color} rounded-2xl flex items-center justify-center text-2xl mb-3 shadow-lg group-hover:scale-110 transition-transform`}>
                            {item.icon}
                          </div>
                          <div className="font-bold text-gray-900 dark:text-gray-100 mb-1.5">{item.step}</div>
                          <div className="text-xs text-gray-500 dark:text-gray-400 leading-relaxed">{item.desc}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Performance Trend Chart */}
                <div className="card p-7">
                  <div className="flex items-center justify-between mb-6">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-xl flex items-center justify-center text-white text-lg shadow-lg shadow-blue-500/30">
                        📈
                      </div>
                      <div>
                        <h3 className="text-xl font-bold text-gray-900 dark:text-white">Performance Trend</h3>
                        <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">Score progression over iterations</p>
                      </div>
                    </div>
                    <div className="text-sm font-mono font-bold text-emerald-600 bg-emerald-50 dark:bg-emerald-950/30 px-3 py-1 rounded-lg">
                      +45.2% ↑
                    </div>
                  </div>
                  
                  <div className="h-64 flex items-end gap-1.5 px-2 pb-6 border-b border-gray-200 dark:border-gray-700">
                    {[0.62, 0.65, 0.64, 0.71, 0.73, 0.72, 0.78, 0.81, 0.79, 0.84, 0.86, 0.85, 0.88, 0.89, 0.91].map((score, idx) => (
                      <div key={idx} className="flex-1 flex flex-col items-center gap-1.5 group">
                        <div className="relative w-full">
                          <div 
                            className={`w-full rounded-t-lg transition-all duration-500 cursor-pointer group-hover:opacity-80 ${
                              score >= 0.85 ? 'bg-gradient-to-t from-emerald-500 to-green-400 shadow-lg shadow-emerald-500/30' :
                              score >= 0.75 ? 'bg-gradient-to-t from-blue-500 to-cyan-400 shadow-lg shadow-blue-500/30' :
                              score >= 0.65 ? 'bg-gradient-to-t from-amber-500 to-yellow-400 shadow-lg shadow-amber-500/30' : 
                              'bg-gradient-to-t from-red-500 to-rose-400 shadow-lg shadow-red-500/30'
                            }`}
                            style={{ height: `${score * 200}px` }}
                          ></div>
                          
                          <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-600 rounded-lg px-2 py-1 text-xs font-mono font-bold text-gray-900 dark:text-gray-100 opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap shadow-lg z-10">
                            {(score * 100).toFixed(0)}%
                          </div>
                        </div>
                        <span className="text-[10px] text-gray-500 dark:text-gray-400 font-mono">{idx + 1}</span>
                      </div>
                    ))}
                  </div>
                  
                  <div className="mt-4 flex justify-center gap-6 text-xs">
                    {[
                      { label: '<65%', color: 'bg-red-500' },
                      { label: '65-75%', color: 'bg-amber-500' },
                      { label: '75-85%', color: 'bg-blue-500' },
                      { label: '>85%', color: 'bg-emerald-500' }
                    ].map((legend) => (
                      <span key={legend.label} className="flex items-center gap-1.5 text-gray-600 dark:text-gray-400">
                        <span className={`w-3 h-3 rounded ${legend.color}`}></span> {legend.label}
                      </span>
                    ))}
                  </div>
                </div>
              </>
            )}

            {/* Optimizer Tab */}
            {activeTab === 'optimizer' && (
              <div className="card p-7 space-y-7">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-gradient-to-r from-fuchsia-500 to-pink-500 rounded-xl flex items-center justify-center text-white text-lg shadow-lg shadow-fuchsia-500/30">
                    ⚙️
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-gray-900 dark:text-white">Optimization Control Panel</h3>
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">Configure and run evolution cycles</p>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-bold text-gray-800 dark:text-gray-200 mb-2.5">
                    Select Skill to Optimize
                  </label>
                  <select
                    value={selectedSkill || ''}
                    onChange={(e) => setSelectedSkill(e.target.value)}
                    className="w-full px-4 py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-xl focus:outline-none focus:ring-2 focus:ring-violet-500/50 focus:border-violet-400 text-gray-900 dark:text-gray-100 font-medium appearance-none cursor-pointer"
                  >
                    <option value="" className="text-gray-500">Choose a skill...</option>
                    <option value="skill-001" className="text-gray-900">Data Analysis Pipeline</option>
                    <option value="skill-002" className="text-gray-900">Code Review Assistant</option>
                    <option value="skill-003" className="text-gray-900">Document Summarizer</option>
                    <option value="skill-004" className="text-gray-900">API Integration Handler</option>
                  </select>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-bold text-gray-800 dark:text-gray-200 mb-2.5">
                      Max Iterations
                    </label>
                    <input
                      type="number"
                      defaultValue={10}
                      min={1}
                      max={50}
                      className="w-full px-4 py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-xl focus:outline-none focus:ring-2 focus:ring-violet-500/50 text-gray-900 dark:text-gray-100 font-medium"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-bold text-gray-800 dark:text-gray-200 mb-2.5">
                      Stagnation Limit
                    </label>
                    <input
                      type="number"
                      defaultValue={3}
                      min={1}
                      max={10}
                      className="w-full px-4 py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-xl focus:outline-none focus:ring-2 focus:ring-violet-500/50 text-gray-900 dark:text-gray-100 font-medium"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-bold text-gray-800 dark:text-gray-200 mb-3">
                    Proposal Strategy
                  </label>
                  <div className="grid grid-cols-2 gap-3">
                    {[
                      { id: 'mutation', name: 'Mutation', prob: '40%', desc: 'Random parameter changes', color: 'from-violet-500 to-purple-500' },
                      { id: 'template', name: 'Template', prob: '25%', desc: 'Apply known patterns', color: 'from-blue-500 to-cyan-500' },
                      { id: 'restructure', name: 'Restructure', prob: '15%', desc: 'Reorganize logic flow', color: 'from-emerald-500 to-teal-500' },
                      { id: 'llm_guided', name: 'LLM Guided', prob: '15%', desc: 'AI-suggested changes', color: 'from-amber-500 to-orange-500' },
                      { id: 'failure_driven', name: 'Failure Driven', prob: '5%', desc: 'Fix past failures', color: 'from-pink-500 to-rose-500' }
                    ].map((strategy) => (
                      <label key={strategy.id} className="flex items-center gap-3 p-3.5 bg-gray-50 dark:bg-gray-800 rounded-xl cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700 border border-transparent hover:border-violet-300 dark:hover:border-violet-700 transition-all group">
                        <input type="checkbox" defaultChecked={strategy.id === 'mutation'} className="rounded accent-violet-500 w-4 h-4" />
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2">
                            <span className="font-semibold text-gray-900 dark:text-gray-100 text-sm capitalize">{strategy.name}</span>
                            <span className={`px-2 py-0.5 bg-gradient-to-r ${strategy.color} text-white text-[10px] font-bold rounded-full`}>{strategy.prob}</span>
                          </div>
                          <div className="text-[11px] text-gray-500 dark:text-gray-400 mt-0.5">{strategy.desc}</div>
                        </div>
                      </label>
                    ))}
                  </div>
                </div>

                <button
                  onClick={handleStartOptimization}
                  disabled={!selectedSkill || isRunning}
                  className="w-full py-4 bg-gradient-to-r from-violet-600 via-purple-600 to-fuchsia-600 hover:from-violet-700 hover:to-fuchsia-700 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-2xl font-bold text-base transition-all duration-300 shadow-xl shadow-purple-500/25 hover:shadow-2xl hover:shadow-purple-500/40 flex items-center justify-center gap-3 disabled:hover:shadow-xl"
                >
                  {isRunning ? (
                    <>
                      <span className="animate-spin text-xl">⏳</span>
                      <span>Optimizing...</span>
                      <div className="flex gap-1">
                        <span className="w-1.5 h-1.5 bg-white rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
                        <span className="w-1.5 h-1.5 bg-white rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
                        <span className="w-1.5 h-1.5 bg-white rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
                      </div>
                    </>
                  ) : (
                    <>
                      🚀 Run Feedback Descent Optimization
                      <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                        <path strokeLinecap="round" strokeLinejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                      </svg>
                    </>
                  )}
                </button>

                {optimizationLog.length > 0 && (
                  <div>
                    <h4 className="font-bold text-gray-800 dark:text-gray-200 mb-3 flex items-center gap-2">
                      <span>📋</span> Optimization Log
                      <span className="ml-auto text-xs font-normal text-gray-500 dark:text-gray-400">{optimizationLog.length} entries</span>
                    </h4>
                    <div className="max-h-56 overflow-y-auto bg-gray-50 dark:bg-gray-800 rounded-2xl p-4 space-y-2 font-mono text-xs border border-gray-200 dark:border-gray-700">
                      {optimizationLog.map((log, idx) => (
                        <div key={idx} className={`flex items-start gap-2.5 p-2 rounded-lg transition-colors ${
                          log.type === 'success' ? 'bg-emerald-50 dark:bg-emerald-950/20 text-emerald-700 dark:text-emerald-300' :
                          log.type === 'error' ? 'bg-red-50 dark:bg-red-950/20 text-red-700 dark:text-red-300' :
                          log.type === 'warning' ? 'bg-amber-50 dark:bg-amber-950/20 text-amber-700 dark:text-amber-300' : 'text-gray-700 dark:text-gray-300'
                        }`}>
                          <span className="shrink-0 opacity-50">[{log.time}]</span>
                          <span className="shrink-0 font-bold">{getLogIcon(log.type)}</span>
                          <span className="flex-1 break-all">{log.message}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Variants & History Tab */}
            {(activeTab === 'variants' || activeTab === 'history') && (
              <div className="card p-7">
                <div className="flex items-center justify-between mb-6">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-gradient-to-r from-indigo-500 to-blue-500 rounded-xl flex items-center justify-center text-white text-lg shadow-lg shadow-indigo-500/30">
                      {activeTab === 'variants' ? '🧬' : '📜'}
                    </div>
                    <div>
                      <h3 className="text-xl font-bold text-gray-900 dark:text-white">
                        {activeTab === 'variants' ? 'Skill Variants' : 'Evolution History'}
                      </h3>
                      <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
                        {activeTab === 'variants' ? 'All generated candidate variants' : 'Complete optimization timeline'}
                      </p>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <span className="px-3 py-1.5 bg-gray-100 dark:bg-gray-800 rounded-lg text-xs font-mono font-bold text-gray-700 dark:text-gray-300">
                      {activeTab === 'variants' ? '5 variants' : '15 iterations'}
                    </span>
                  </div>
                </div>
                
                <div className="space-y-3">
                  {(activeTab === 'variants' ? [
                    { id: 'v-14', name: 'Variant #14', score: 0.91, strategy: 'llm_guided', status: 'best' },
                    { id: 'v-13', name: 'Variant #13', score: 0.89, strategy: 'mutation', status: 'frontier' },
                    { id: 'v-12', name: 'Variant #12', score: 0.86, strategy: 'template', status: 'frontier' },
                    { id: 'v-11', name: 'Variant #11', score: 0.84, strategy: 'restructure', status: 'frontier' },
                    { id: 'v-10', name: 'Variant #10', score: 0.81, strategy: 'mutation', status: 'archived' }
                  ] : [
                    { iter: 15, action: 'Accepted v14 (LLM-guided)', delta: '+0.02', score: 0.91 },
                    { iter: 14, action: 'Generated proposal via LLM guidance', delta: '-', score: 0.89 },
                    { iter: 13, action: 'Rejected v13-b (stagnation)', delta: '-0.01', score: 0.89 },
                    { iter: 12, action: 'Accepted v12 (template merge)', delta: '+0.03', score: 0.89 },
                    { iter: 11, action: 'Generated from template pool', delta: '-', score: 0.86 }
                  ]).map((item, idx) => (
                    <div key={idx} className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-800/80 rounded-xl hover:bg-gray-100 dark:hover:bg-gray-700 transition-all border border-transparent hover:border-violet-300 dark:hover:border-violet-700 group">
                      <div className="flex items-center gap-4">
                        <div className={`w-3 h-3 rounded-full shadow-sm ${
                          item.status === 'best' ? 'bg-emerald-500 shadow-emerald-500/50' :
                          item.status === 'frontier' ? 'bg-blue-500 shadow-blue-500/50' : 
                          'bg-gray-500 shadow-gray-500/50'
                        }`} />
                        <div>
                          <div className="font-semibold text-gray-900 dark:text-gray-100 text-sm flex items-center gap-2">
                            {item.name || `Iteration ${item.iter}`}
                            {item.status === 'best' && (
                              <span className="px-2 py-0.5 bg-gradient-to-r from-emerald-500 to-green-500 text-white text-[10px] font-bold rounded-full shadow-sm">BEST</span>
                            )}
                          </div>
                          <div className="text-xs text-gray-500 dark:text-gray-400 mt-0.5 flex items-center gap-2">
                            <span>{item.strategy || item.action}</span>
                            {item.delta && (
                              <span className={`font-mono font-bold px-1.5 py-0.5 rounded ${
                                item.delta.startsWith('+') ? 'bg-emerald-50 dark:bg-emerald-950/20 text-emerald-600 dark:text-emerald-400' :
                                item.delta.startsWith('-') ? 'bg-red-50 dark:bg-red-950/20 text-red-600 dark:text-red-400' : 'bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400'
                              }`}>
                                {item.delta}
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center gap-3">
                        <div className={`px-3 py-1.5 rounded-lg font-mono font-bold text-sm ${getScoreBg(item.score)} text-white shadow-sm`}>
                          {item.score.toFixed(2)}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Sidebar */}
          <div className="space-y-5">
            
            {/* Algorithm Info Card */}
            <div className="card p-6 bg-gradient-to-br from-violet-50 via-purple-50 to-fuchsia-50 dark:from-violet-950/20 dark:via-purple-950/20 dark:to-fuchsia-950/20 border border-violet-200/40 dark:border-violet-800/30 relative overflow-hidden">
              <div className="absolute top-0 right-0 w-24 h-24 bg-gradient-to-bl from-purple-300/30 to-transparent rounded-full blur-2xl"></div>
              <h4 className="font-bold text-gray-900 dark:text-white mb-5 flex items-center gap-3 relative z-10">
                <span className="text-xl">⚙️</span>
                <span className="bg-gradient-to-r from-violet-600 to-fuchsia-600 bg-clip-text text-transparent font-black dark:font-white">Algorithm Info</span>
              </h4>
              <div className="space-y-3.5 relative z-10">
                {[
                  { label: 'Algorithm', value: 'Feedback Descent', highlight: true, icon: '🧠' },
                  { label: 'Evaluation Mode', value: 'Pairwise Comparison', icon: '⚖️' },
                  { label: 'Frontier Size', value: 'K=5', icon: '📊' },
                  { label: 'Temperature', value: '0.8', icon: '🌡️' },
                  { label: 'Convergence', value: 'Stable ✓', icon: '✅' }
                ].map((item, idx) => (
                  <div key={idx} className="flex justify-between items-center p-3.5 bg-white/80 dark:bg-black/25 rounded-xl border border-white/50 dark:border-gray-700/40 hover:bg-white dark:hover:bg-black/35 hover:shadow-lg transition-all group">
                    <div className="flex items-center gap-3">
                      <div className={`w-8 h-8 bg-gradient-to-br ${['from-violet-500 to-purple-500', 'from-blue-500 to-cyan-500', 'from-emerald-500 to-teal-500', 'from-amber-500 to-orange-500', 'from-pink-500 to-rose-500'][idx]} rounded-lg flex items-center justify-center text-base shadow-md group-hover:scale-110 group-hover:rotate-6 transition-all duration-300`}>
                        {item.icon}
                      </div>
                      <span className="text-sm font-bold text-gray-800 dark:text-gray-200">{item.label}</span>
                    </div>
                    <span className={`text-sm font-extrabold ${item.highlight ? 'text-violet-700 dark:text-violet-300 bg-gradient-to-r from-violet-100 to-fuchsia-100 dark:from-violet-900 dark:to-fuchsia-900 px-3 py-1.5 rounded-lg shadow-sm' : 'text-gray-900 dark:text-white bg-gradient-to-r from-gray-100 to-gray-200 dark:from-gray-700 dark:to-gray-600 px-3 py-1.5 rounded-lg shadow-sm'}`}>
                      {item.value}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Proposal Strategies Card */}
            <div className="card p-6 bg-gradient-to-br from-blue-50 via-indigo-50 to-cyan-50 dark:from-blue-950/20 dark:via-indigo-950/20 dark:to-cyan-950/20 border border-blue-200/40 dark:border-blue-800/30 relative overflow-hidden">
              <div className="absolute top-0 right-0 w-24 h-24 bg-gradient-to-bl from-cyan-300/30 to-transparent rounded-full blur-2xl"></div>
              <h4 className="font-bold text-gray-900 dark:text-white mb-5 flex items-center gap-3 relative z-10">
                <span className="text-xl">🎯</span>
                <span className="bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent font-black dark:font-white">Proposal Strategies</span>
              </h4>
              <div className="space-y-3 relative z-10">
                {[
                  { name: 'Mutation', prob: '40%', desc: 'Random parameter changes', color: 'from-violet-500 to-purple-500', icon: '🎲' },
                  { name: 'Template', prob: '25%', desc: 'Apply known patterns', color: 'from-blue-500 to-cyan-500', icon: '📋' },
                  { name: 'Restructure', prob: '15%', desc: 'Reorganize logic flow', color: 'from-emerald-500 to-teal-500', icon: '🔄' },
                  { name: 'LLM Guided', prob: '15%', desc: 'AI-suggested changes', color: 'from-amber-500 to-orange-500', icon: '🤖' },
                  { name: 'Failure Driven', prob: '5%', desc: 'Fix past failures', color: 'from-pink-500 to-rose-500', icon: '🔧' }
                ].map((s, i) => (
                  <div key={i} className="flex items-center justify-between p-3.5 bg-white/80 dark:bg-black/25 rounded-xl hover:bg-white dark:hover:bg-black/35 hover:shadow-lg transition-all group border border-white/50 dark:border-gray-700/40">
                    <div className="flex items-center gap-3 min-w-0">
                      <div className={`w-8 h-8 bg-gradient-to-br ${s.color} rounded-lg flex items-center justify-center text-base shadow-md group-hover:scale-110 group-hover:rotate-6 transition-all duration-300 shrink-0`}>
                        {s.icon}
                      </div>
                      <div className="min-w-0">
                        <span className="font-bold text-gray-900 dark:text-gray-100 text-sm block">{s.name}</span>
                        <div className="text-xs text-gray-600 dark:text-gray-400 mt-0.5 font-medium">{s.desc}</div>
                      </div>
                    </div>
                    <span className={`px-3 py-1.5 bg-gradient-to-r ${s.color} text-white rounded-lg font-mono text-xs font-extrabold ml-2 shrink-0 shadow-md`}>
                      {s.prob}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Quick Actions Card */}
            <div className="card p-6 bg-gradient-to-br from-emerald-50 via-teal-50 to-green-50 dark:from-emerald-950/20 dark:via-teal-950/20 dark:to-green-950/20 border border-emerald-200/40 dark:border-emerald-800/30 relative overflow-hidden">
              <div className="absolute top-0 right-0 w-24 h-24 bg-gradient-to-bl from-teal-300/30 to-transparent rounded-full blur-2xl"></div>
              <h4 className="font-bold text-gray-900 dark:text-white mb-5 flex items-center gap-3 relative z-10">
                <span className="text-xl">⚡</span>
                <span className="bg-gradient-to-r from-emerald-600 to-green-600 bg-clip-text text-transparent font-black dark:font-white">Quick Actions</span>
              </h4>
              <div className="space-y-3 relative z-10">
                <button className="w-full px-4 py-3.5 text-left text-sm font-bold bg-white/80 dark:bg-black/25 hover:bg-white dark:hover:bg-black/35 rounded-xl transition-all text-gray-800 dark:text-gray-200 border border-white/50 dark:border-gray-700/40 hover:border-gray-300 dark:hover:border-gray-600 hover:shadow-lg flex items-center gap-3 group">
                  <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center text-base shadow-md group-hover:scale-110 group-hover:rotate-6 transition-all duration-300">🔄</div>
                  Reset Optimizer State
                </button>
                <button className="w-full px-4 py-3.5 text-left text-sm font-bold bg-white/80 dark:bg-black/25 hover:bg-white dark:hover:bg-black/35 rounded-xl transition-all text-gray-800 dark:text-gray-200 border border-white/50 dark:border-gray-700/40 hover:border-gray-300 dark:hover:border-gray-600 hover:shadow-lg flex items-center gap-3 group">
                  <div className="w-8 h-8 bg-gradient-to-br from-violet-500 to-purple-500 rounded-lg flex items-center justify-center text-base shadow-md group-hover:scale-110 group-hover:rotate-6 transition-all duration-300">📥</div>
                  Export Variant Data
                </button>
                <button className="w-full px-4 py-3.5 text-left text-sm font-bold bg-white/80 dark:bg-black/25 hover:bg-white dark:hover:bg-black/35 rounded-xl transition-all text-gray-800 dark:text-gray-200 border border-white/50 dark:border-gray-700/40 hover:border-gray-300 dark:hover:border-gray-600 hover:shadow-lg flex items-center gap-3 group">
                  <div className="w-8 h-8 bg-gradient-to-br from-amber-500 to-orange-500 rounded-lg flex items-center justify-center text-base shadow-md group-hover:scale-110 group-hover:rotate-6 transition-all duration-300">📊</div>
                  View Analytics Report
                </button>
                <Link
                  to="/skills-hub-pro"
                  className="block px-4 py-3.5 text-sm font-bold bg-violet-100/80 dark:bg-violet-900/30 hover:bg-violet-100 dark:hover:bg-violet-900/40 rounded-xl transition-all text-violet-800 dark:text-violet-300 border border-violet-200/60 dark:border-violet-800/40 hover:border-violet-300 dark:hover:border-violet-700 hover:shadow-lg flex items-center gap-3 group"
                >
                  <div className="w-8 h-8 bg-gradient-to-br from-pink-500 to-rose-500 rounded-lg flex items-center justify-center text-base shadow-md group-hover:scale-110 group-hover:rotate-6 transition-all duration-300">📦</div>
                  Open Skills Hub
                </Link>
              </div>
            </div>

            {/* Evolution Status CTA */}
            <div className="card p-6 bg-gradient-to-br from-violet-600 via-purple-600 to-fuchsia-600 text-white relative overflow-hidden shadow-xl shadow-purple-500/20">
              <div className="absolute top-0 right-0 w-40 h-40 bg-white/10 rounded-full -translate-y-1/2 translate-x-1/3"></div>
              <div className="absolute bottom-0 left-0 w-28 h-28 bg-black/10 rounded-full translate-y-1/2 -translate-x-1/3"></div>
              <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-white/5 rounded-full blur-3xl"></div>

              <div className="relative z-10">
                <h4 className="font-black text-lg mb-3 flex items-center gap-3">
                  <span className="w-10 h-10 bg-white/20 backdrop-blur-md rounded-xl flex items-center justify-center text-lg shadow-lg border border-white/20">🚀</span>
                  <span className="bg-gradient-to-r from-white to-white/80 bg-clip-text text-transparent">Ready to Evolve?</span>
                </h4>
                <p className="text-sm text-white/90 mb-5 leading-relaxed font-medium pl-[52px]">
                  Select a skill and start the optimization process to see your AI agent skills evolve in real-time.
                </p>
                <div className="flex items-center gap-3 text-sm bg-white/15 backdrop-blur-md rounded-xl px-4 py-3 shadow-lg border border-white/20">
                  <span className="w-2.5 h-2.5 bg-emerald-400 rounded-full animate-pulse shadow-md shadow-emerald-400/50"></span>
                  <span className="text-white/95 font-semibold">System ready for optimization</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AI_Evolution
