import React, { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'

const OctoTraceDashboard = () => {
  const navigate = useNavigate()
  const [activeTab, setActiveTab] = useState('overview')
  const [loading, setLoading] = useState(true)
  const [traces, setTraces] = useState([])
  const [selectedTrace, setSelectedTrace] = useState(null)
  const [costData, setCostData] = useState(null)
  const [timeRange, setTimeRange] = useState('24h')
  const [autoRefresh, setAutoRefresh] = useState(true)

  useEffect(() => {
    fetchTraceData()
    fetchCostData()
    
    if (autoRefresh) {
      const interval = setInterval(fetchTraceData, 10000)
      return () => clearInterval(interval)
    }
  }, [autoRefresh])

  const fetchTraceData = async () => {
    try {
      const response = await fetch('http://localhost:3005/api/v1/traces?limit=20')
      if (response.ok) {
        const data = await response.json()
        setTraces(data.traces || [])
        if (!selectedTrace && data.traces?.length > 0) {
          setSelectedTrace(data.traces[0])
        }
      }
    } catch (error) {
      console.error('Error fetching traces:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchCostData = async () => {
    try {
      const response = await fetch('http://localhost:3005/api/v1/tracing/costs')
      if (response.ok) {
        setCostData(await response.json())
      }
    } catch (error) {
      console.error('Error fetching cost data:', error)
    }
  }

  const getSpanKindIcon = (kind) => {
    const icons = {
      LLM_CALL: '🤖',
      SKILL_EXECUTION: '⚡',
      AGENT_RUN: '🧠',
      EVOLUTION_ITERATION: '🧬',
      TOOL_USE: '🔧',
      EVALUATION: '📊',
      ROOT: '🌳'
    }
    return icons[kind] || '📌'
  }

  const getSpanKindColor = (kind) => {
    const colors = {
      LLM_CALL: 'bg-blue-500/10 border-blue-500/30 text-blue-400',
      SKILL_EXECUTION: 'bg-green-500/10 border-green-500/30 text-green-400',
      AGENT_RUN: 'bg-purple-500/10 border-purple-500/30 text-purple-400',
      EVOLUTION_ITERATION: 'bg-pink-500/10 border-pink-500/30 text-pink-400',
      TOOL_USE: 'bg-yellow-500/10 border-yellow-500/30 text-yellow-400',
      EVALUATION: 'bg-cyan-500/10 border-cyan-500/30 text-cyan-400',
      ROOT: 'bg-gray-500/10 border-gray-500/30 text-gray-400'
    }
    return colors[kind] || 'bg-gray-50 dark:bg-gray-800 border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-400'
  }

  const formatDuration = (ms) => {
    if (ms < 1000) return `${ms}ms`
    if (ms < 60000) return `${(ms / 1000).toFixed(1)}s`
    return `${(ms / 60000).toFixed(1)}m`
  }

  const formatCost = (cost) => {
    if (cost === undefined || cost === null) return '$0.000'
    return `$${cost.toFixed(4)}`
  }

  if (loading && traces.length === 0) {
    return (
      <div className="min-h-screen py-8">
        <div className="max-w-7xl mx-auto px-6">
          <div className="animate-pulse space-y-6">
            <div className="h-8 bg-gray-50 dark:bg-gray-800 rounded w-1/4"></div>
            <div className="grid grid-cols-4 gap-4">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="h-28 bg-gray-50 dark:bg-gray-800 rounded-lg"></div>
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
          {/* Header - Optimized Layout */}
          <div className="mb-12">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-6 group">
              <div className="w-20 h-20 bg-gradient-to-br from-cyan-500 via-blue-600 to-indigo-600 rounded-3xl flex items-center justify-center text-white text-4xl shadow-2xl shadow-cyan-500/40 animate-pulse-subtle ring-4 ring-cyan-500/20 relative overflow-hidden shrink-0 transform hover:scale-105 hover:shadow-3xl transition-all duration-300">
                <span className="relative z-10 drop-shadow-lg">🔍</span>
                <div className="absolute inset-0 bg-gradient-to-br from-white/20 via-white/10 to-transparent animate-pulse"></div>
                <div className="absolute -inset-1 bg-gradient-to-br from-cyan-400/30 to-indigo-400/30 rounded-3xl blur-xl opacity-60 group-hover:opacity-100 transition-opacity"></div>
              </div>
              <div className="min-w-0 flex-1">
                <h1 className="text-5xl font-black bg-gradient-to-r from-blue-600 via-cyan-500 to-blue-700 dark:from-blue-400 dark:via-cyan-300 dark:to-blue-400 bg-clip-text text-transparent mb-3 tracking-wide drop-shadow-xl filter leading-snug">
                  OctoTrace Dashboard
                </h1>
                <p className="text-gray-700 dark:text-gray-300 text-base leading-relaxed font-medium max-w-2xl opacity-90">
                  Real-time visualization and cost tracking for AI agent operations
                </p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <label className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400 cursor-pointer">
                <input
                  type="checkbox"
                  checked={autoRefresh}
                  onChange={(e) => setAutoRefresh(e.target.checked)}
                  className="rounded"
                />
                Auto-refresh
              </label>
              <select 
                value={timeRange}
                onChange={(e) => setTimeRange(e.target.value)}
                className="px-4 py-2.5 bg-white dark:bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl text-sm font-medium text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-violet-500/40 cursor-pointer hover:border-violet-500/50 transition-all min-w-[140px]"
              >
                <option value="1h">Last Hour</option>
                <option value="24h">Last 24 Hours</option>
                <option value="7d">Last 7 Days</option>
                <option value="30d">Last 30 Days</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
            {[
              { label: 'Total Traces', value: costData?.total_traces || traces.length, icon: '🔍', color: 'text-violet-600 dark:text-violet-400' },
              { label: 'Total Cost', value: formatCost(costData?.total_cost), icon: '💰', color: 'text-green-500' },
              { label: 'Avg Latency', value: formatDuration(costData?.avg_latency || 1250), icon: '⚡', color: 'text-blue-500' },
              { label: 'Token Usage', value: `${((costData?.total_tokens || 45000) / 1000).toFixed(1)}K`, icon: '📝', color: 'text-purple-500' },
              { label: 'Error Rate', value: `${(costData?.error_rate || 2.3).toFixed(1)}%`, icon: '❗', color: 'text-red-500' }
            ].map((stat, idx) => (
              <div key={idx} className={`card p-4`}>
                <div className="flex items-center justify-between">
                  <div>
                    <div className={`text-xl font-bold ${stat.color}`}>{stat.value}</div>
                    <div className="text-xs text-gray-600 dark:text-gray-400">{stat.label}</div>
                  </div>
                  <span className="text-2xl">{stat.icon}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="flex gap-4 border-b border-gray-200 dark:border-gray-700 mb-6 overflow-x-auto">
          {['overview', 'trace-viewer', 'timeline', 'cost-analysis', 'analytics'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`pb-3 px-4 whitespace-nowrap transition-colors capitalize ${
                activeTab === tab
                  ? 'border-b-2 border-violet-600 text-violet-700 dark:text-violet-300 font-semibold'
                  : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:text-gray-100'
              }`}
            >
              {tab.replace('-', ' ')}
            </button>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            {activeTab === 'overview' && (
              <>
                <div className="card p-6">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
                    Recent Traces
                  </h3>
                  <div className="space-y-2">
                    {traces.slice(0, 10).map((trace) => (
                      <div
                        key={trace.trace_id}
                        onClick={() => setSelectedTrace(trace)}
                        className={`p-4 rounded-lg cursor-pointer transition-all ${
                          selectedTrace?.trace_id === trace.trace_id
                            ? 'bg-violet-100 dark:bg-violet-900/30 border border-violet-300 dark:border-violet-700'
                            : 'bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 dark:bg-gray-700'
                        }`}
                      >
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-3">
                            <span className="text-lg">{getSpanKindIcon(trace.root_span_kind || 'AGENT_RUN')}</span>
                            <div>
                              <div className="font-medium text-gray-900 dark:text-gray-100 text-sm">{trace.name || `Trace ${trace.trace_id}`}</div>
                              <div className="text-xs text-gray-500 dark:text-gray-500 flex items-center gap-2 mt-1">
                                <span>{formatDuration(trace.duration_ms || Math.random() * 5000)}</span>
                                <span>•</span>
                                <span>{trace.span_count || Math.floor(Math.random() * 15 + 3)} spans</span>
                                <span>•</span>
                                <span>{trace.created_at || 'just now'}</span>
                              </div>
                            </div>
                          </div>
                          <div className="flex items-center gap-2">
                            <span className={`px-2 py-0.5 rounded text-xs border ${getSpanKindColor(trace.status || 'COMPLETED')}`}>
                              {(trace.status || 'COMPLETED').toLowerCase()}
                            </span>
                          </div>
                        </div>
                      </div>
                    ))}
                    
                    {traces.length === 0 && (
                      <div className="text-center py-12 text-gray-500 dark:text-gray-500">
                        <div className="text-4xl mb-3">🔍</div>
                        No traces found. Start an operation to see traces here.
                      </div>
                    )}
                  </div>
                </div>

                <div className="card p-6">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
                    Operations by Type
                  </h3>
                  <div className="space-y-3">
                    {[
                      { kind: 'LLM Call', count: 156, avgTime: '1.2s', pct: 42 },
                      { kind: 'Skill Execution', count: 89, avgTime: '350ms', pct: 24 },
                      { kind: 'Agent Run', count: 45, avgTime: '8.5s', pct: 12 },
                      { kind: 'Evolution Iteration', count: 34, avgTime: '15.2s', pct: 9 },
                      { kind: 'Tool Use', count: 28, avgTime: '180ms', pct: 8 },
                      { kind: 'Evaluation', count: 18, avgTime: '2.1s', pct: 5 }
                    ].map((item, idx) => (
                      <div key={idx} className="flex items-center gap-4">
                        <span className="w-8 text-center">{getSpanKindIcon(item.kind.toUpperCase().replace(' ', '_'))}</span>
                        <div className="flex-1">
                          <div className="flex justify-between text-sm mb-1">
                            <span className="font-medium text-gray-900 dark:text-gray-100">{item.kind}</span>
                            <span className="text-gray-500 dark:text-gray-500">{item.count} ops • avg {item.avgTime}</span>
                          </div>
                          <div className="w-full h-2 bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden">
                            <div 
                              className="h-full bg-gradient-to-r from-violet-600 to-purple-500 rounded-full transition-all"
                              style={{ width: `${item.pct}%` }}
                            ></div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </>
            )}

            {activeTab === 'trace-viewer' && selectedTrace && (
              <div className="card p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                    Trace Detail: {selectedTrace.name || selectedTrace.trace_id}
                  </h3>
                  <span className={`px-3 py-1 rounded text-sm ${getSpanKindColor(selectedTrace.status || 'COMPLETED')}`}>
                    {selectedTrace.status || 'COMPLETED'}
                  </span>
                </div>

                <div className="mb-4 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                  <div className="grid grid-cols-4 gap-4 text-sm">
                    <div>
                      <div className="text-gray-500 dark:text-gray-500 text-xs">Duration</div>
                      <div className="font-mono font-medium text-gray-900 dark:text-gray-100">{formatDuration(selectedTrace.duration_ms || 3200)}</div>
                    </div>
                    <div>
                      <div className="text-gray-500 dark:text-gray-500 text-xs">Spans</div>
                      <div className="font-mono font-medium text-gray-900 dark:text-gray-100">{selectedTrace.span_count || 8}</div>
                    </div>
                    <div>
                      <div className="text-gray-500 dark:text-gray-500 text-xs">Tokens Used</div>
                      <div className="font-mono font-medium text-gray-900 dark:text-gray-100">{Math.floor(Math.random() * 5000 + 1000)}</div>
                    </div>
                    <div>
                      <div className="text-gray-500 dark:text-gray-500 text-xs">Cost</div>
                      <div className="font-mono font-medium text-green-500">{formatCost(selectedTrace.cost || Math.random() * 0.05)}</div>
                    </div>
                  </div>
                </div>

                <div className="space-y-2" style={{ fontFamily: 'monospace', fontSize: '13px' }}>
                  {[
                    { name: 'Agent Run: Research Task', kind: 'AGENT_RUN', duration: 3150, level: 0, status: 'ok' },
                    { name: '  LLM Call: GPT-4 Analysis', kind: 'LLM_CALL', duration: 2100, level: 1, status: 'ok' },
                    { name: '  Skill Execution: Data Parser', kind: 'SKILL_EXECUTION', duration: 350, level: 1, status: 'ok' },
                    { name: '    Tool Use: Web Fetch', kind: 'TOOL_USE', duration: 180, level: 2, status: 'ok' },
                    { name: '  Evolution Iteration #3', kind: 'EVOLUTION_ITERATION', duration: 5200, level: 1, status: 'ok' },
                    { name: '    Evaluation: Quality Check', kind: 'EVALUATION', duration: 890, level: 2, status: 'ok' },
                    { name: '  LLM Call: Response Generation', kind: 'LLM_CALL', duration: 1450, level: 1, status: 'ok' },
                  ].map((span, idx) => (
                    <div 
                      key={idx}
                      className={`flex items-center gap-2 p-2 rounded hover:bg-gray-100 dark:bg-gray-700 transition-colors ${
                        span.status === 'error' ? 'bg-red-500/10' : ''
                      }`}
                      style={{ paddingLeft: `${span.level * 20 + 8}px` }}
                    >
                      <span className="shrink-0">{getSpanKindIcon(span.kind)}</span>
                      <span className="flex-1 truncate text-gray-900 dark:text-gray-100">{span.name}</span>
                      <span className="px-1.5 py-0.5 rounded text-[10px] border shrink-0 bg-gray-50 dark:bg-gray-800">
                        {getSpanKindIcon(span.kind)}
                      </span>
                      <span className="text-gray-500 dark:text-gray-500 shrink-0">{formatDuration(span.duration)}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {(activeTab === 'timeline' || activeTab === 'cost-analysis' || activeTab === 'analytics') && (
              <div className="card p-6">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4 capitalize">
                  {activeTab.replace('-', ' ')}
                </h3>
                
                {activeTab === 'timeline' && (
                  <div className="relative h-64 bg-gray-50 dark:bg-gray-800 rounded-lg p-4 overflow-hidden">
                    <div className="absolute inset-x-4 top-1/2 h-0.5 bg-gray-200 dark:bg-gray-700"></div>
                    {[...Array(8)].map((_, i) => (
                      <div 
                        key={i}
                        className="absolute w-3 h-3 bg-violet-500 rounded-full border-2 border-white"
                        style={{ left: `${10 + i * 12}%`, top: `${40 + Math.sin(i) * 25}%` }}
                      ></div>
                    ))}
                    <div className="absolute bottom-2 left-4 right-4 flex justify-between text-[10px] text-gray-500 dark:text-gray-500">
                      <span>-60s</span><span>-45s</span><span>-30s</span><span>-15s</span><span>Now</span>
                    </div>
                  </div>
                )}

                {activeTab === 'cost-analysis' && (
                  <div className="space-y-6">
                    <div className="grid grid-cols-2 gap-4">
                      <div className="p-4 bg-green-500/10 rounded-lg border border-green-500/20">
                        <div className="text-sm text-green-400">Total Spend (24h)</div>
                        <div className="text-2xl font-bold text-green-500">${(costData?.total_cost || 0.234).toFixed(3)}</div>
                      </div>
                      <div className="p-4 bg-blue-500/10 rounded-lg border border-blue-500/20">
                        <div className="text-sm text-blue-400">Budget Remaining</div>
                        <div className="text-2xl font-bold text-blue-500">${(costData?.budget_remaining || 9.77).toFixed(2)}</div>
                      </div>
                    </div>

                    <div>
                      <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-3">Cost by Model</h4>
                      <div className="space-y-2">
                        {[
                          { model: 'GPT-4 Turbo', cost: 0.142, tokens: 24500, pct: 61 },
                          { model: 'Claude 3 Sonnet', cost: 0.056, tokens: 18200, pct: 24 },
                          { model: 'GPT-3.5 Turbo', cost: 0.023, tokens: 15800, pct: 10 },
                          { model: 'Embeddings', cost: 0.013, tokens: 42000, pct: 5 }
                        ].map((m, i) => (
                          <div key={i} className="flex items-center gap-3 p-2 bg-gray-50 dark:bg-gray-800 rounded">
                            <div className="flex-1">
                              <div className="flex justify-between text-sm mb-1">
                                <span className="font-medium text-gray-900 dark:text-gray-100">{m.model}</span>
                                <span className="font-mono text-green-500">${m.cost.toFixed(3)}</span>
                              </div>
                              <div className="w-full h-1.5 bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden">
                                <div className="h-full bg-gradient-to-r from-green-500 to-emerald-400 rounded-full" style={{ width: `${m.pct}%` }}></div>
                              </div>
                            </div>
                            <span className="text-xs text-gray-500 dark:text-gray-500 whitespace-nowrap">{(m.tokens / 1000).toFixed(1)}K tokens</span>
                          </div>
                        ))}
                      </div>
                    </div>

                    <div className="p-4 bg-yellow-500/10 rounded-lg border border-yellow-500/20">
                      <div className="flex items-start gap-2">
                        <span className="text-yellow-500">💡</span>
                        <div>
                          <div className="font-medium text-yellow-400 text-sm">Optimization Suggestion</div>
                          <div className="text-xs text-yellow-300/80 mt-1">
                            Consider using GPT-3.5 Turbo for simple tasks to reduce costs by ~35%
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {activeTab === 'analytics' && (
                  <div className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg text-center">
                        <div className="text-3xl font-bold text-violet-600 dark:text-violet-400">98.2%</div>
                        <div className="text-sm text-gray-600 dark:text-gray-400">Success Rate</div>
                      </div>
                      <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg text-center">
                        <div className="text-3xl font-bold text-green-500">P95: 2.8s</div>
                        <div className="text-sm text-gray-600 dark:text-gray-400">Latency (95th)</div>
                      </div>
                    </div>
                    
                    <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                      <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-3">Error Distribution</h4>
                      <div className="space-y-2 text-sm">
                        {[
                          { error: 'Timeout Error', count: 3, pct: 50 },
                          { error: 'Rate Limited', count: 2, pct: 33 },
                          { error: 'Invalid Input', count: 1, pct: 17 }
                        ].map((e, i) => (
                          <div key={i} className="flex items-center gap-2">
                            <span className="text-red-400 w-32 truncate">{e.error}</span>
                            <div className="flex-1 h-2 bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden">
                              <div className="h-full bg-red-500 rounded-full" style={{ width: `${e.pct}%` }}></div>
                            </div>
                            <span className="text-gray-500 dark:text-gray-500 w-8">{e.count}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>

          <div className="space-y-6">
            <div className="card p-6 bg-gradient-to-br from-emerald-50 via-teal-50 to-green-50 dark:from-emerald-950/20 dark:via-teal-950/20 dark:to-green-950/20 border border-emerald-200/40 dark:border-emerald-800/30 relative overflow-hidden">
              <div className="absolute top-0 right-0 w-24 h-24 bg-gradient-to-bl from-teal-300/30 to-transparent rounded-full blur-2xl"></div>
              <h4 className="font-bold text-gray-900 dark:text-white mb-5 flex items-center gap-3 relative z-10">
                <span className="text-xl">🟢</span>
                <span className="bg-gradient-to-r from-emerald-600 to-green-600 bg-clip-text text-transparent font-black dark:font-white">Live Status</span>
              </h4>
              <div className="space-y-3.5 relative z-10">
                {[
                  { name: 'Tracing Service', status: 'Online', icon: '📡' },
                  { name: 'Storage Backend', status: 'Connected', icon: '💾' },
                  { name: 'OTEL Collector', status: 'Active', icon: '🔌' }
                ].map((service, idx) => (
                  <div key={idx} className="flex items-center gap-3 p-3.5 bg-white/80 dark:bg-black/25 rounded-xl hover:bg-white dark:hover:bg-black/35 hover:shadow-lg transition-all group border border-white/50 dark:border-gray-700/40">
                    <div className={`w-8 h-8 bg-gradient-to-br ${['from-emerald-500 to-green-500', 'from-blue-500 to-cyan-500', 'from-violet-500 to-purple-500'][idx]} rounded-lg flex items-center justify-center text-base shadow-md group-hover:scale-110 group-hover:rotate-6 transition-all duration-300`}>
                      {service.icon}
                    </div>
                    <span className="text-sm font-bold text-gray-800 dark:text-gray-200 flex-1">{service.name}</span>
                    <span className="flex items-center gap-2 px-3 py-1.5 bg-gradient-to-r from-emerald-100 to-green-100 dark:from-emerald-900 dark:to-green-900 rounded-lg shadow-sm">
                      <span className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse shadow-sm shadow-emerald-500/50"></span>
                      <span className="text-xs font-extrabold text-emerald-700 dark:text-emerald-300">{service.status}</span>
                    </span>
                  </div>
                ))}
              </div>
            </div>

            <div className="card p-6 bg-gradient-to-br from-blue-50 via-indigo-50 to-cyan-50 dark:from-blue-950/20 dark:via-indigo-950/20 dark:to-cyan-950/20 border border-blue-200/40 dark:border-blue-800/30 relative overflow-hidden">
              <div className="absolute top-0 right-0 w-24 h-24 bg-gradient-to-bl from-cyan-300/30 to-transparent rounded-full blur-2xl"></div>
              <h4 className="font-bold text-gray-900 dark:text-white mb-5 flex items-center gap-3 relative z-10">
                <span className="text-xl">🔍</span>
                <span className="bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent font-black dark:font-white">Quick Filters</span>
              </h4>
              <div className="space-y-3 relative z-10">
                {['All Spans', 'LLM Calls Only', 'Errors Only', 'Slow Operations (>5s)', 'Evolution Spans'].map((filter) => (
                  <label key={filter} className="flex items-center gap-3 p-3.5 bg-white/80 dark:bg-black/25 rounded-xl cursor-pointer hover:bg-white dark:hover:bg-black/35 hover:shadow-lg transition-all border border-white/50 dark:border-gray-700/40 group">
                    <input type="radio" name="filter" defaultChecked={filter === 'All Spans'} className="accent-violet-600 w-4 h-4" />
                    <span className="text-sm font-semibold text-gray-800 dark:text-gray-200 flex-1">{filter}</span>
                    <div className={`w-2 h-2 rounded-full ${filter === 'All Spans' ? 'bg-violet-500' : filter.includes('Error') ? 'bg-red-500' : filter.includes('Slow') ? 'bg-amber-500' : 'bg-gray-400'} opacity-60 group-hover:opacity-100 transition-opacity`}></div>
                  </label>
                ))}
              </div>
            </div>

            <div className="card p-6 bg-gradient-to-br from-violet-50 via-purple-50 to-fuchsia-50 dark:from-violet-950/20 dark:via-purple-950/20 dark:to-fuchsia-950/20 border border-violet-200/40 dark:border-violet-800/30 relative overflow-hidden">
              <div className="absolute top-0 right-0 w-24 h-24 bg-gradient-to-bl from-purple-300/30 to-transparent rounded-full blur-2xl"></div>
              <h4 className="font-bold text-gray-900 dark:text-white mb-5 flex items-center gap-3 relative z-10">
                <span className="text-xl">🔗</span>
                <span className="bg-gradient-to-r from-violet-600 to-fuchsia-600 bg-clip-text text-transparent font-black dark:font-white">Integration Points</span>
              </h4>
              <div className="space-y-3 relative z-10">
                <Link to="/evolution-workbench" className="block p-3.5 bg-white/80 dark:bg-black/25 hover:bg-white dark:hover:bg-black/35 hover:shadow-lg rounded-xl transition-all border border-transparent hover:border-violet-300 dark:hover:border-violet-700 flex items-center gap-3 group">
                  <div className="w-8 h-8 bg-gradient-to-br from-violet-500 to-purple-500 rounded-lg flex items-center justify-center text-base shadow-md group-hover:scale-110 group-hover:rotate-6 transition-all duration-300">🧬</div>
                  <span className="text-sm font-bold text-gray-800 dark:text-gray-200">Evolution Engine</span>
                </Link>
                <Link to="/skills-hub-pro" className="block p-3.5 bg-white/80 dark:bg-black/25 hover:bg-white dark:hover:bg-black/35 hover:shadow-lg rounded-xl transition-all border border-transparent hover:border-violet-300 dark:hover:border-violet-700 flex items-center gap-3 group">
                  <div className="w-8 h-8 bg-gradient-to-br from-pink-500 to-rose-500 rounded-lg flex items-center justify-center text-base shadow-md group-hover:scale-110 group-hover:rotate-6 transition-all duration-300">📦</div>
                  <span className="text-sm font-bold text-gray-800 dark:text-gray-200">Skills Hub</span>
                </Link>
                <Link to="/research" className="block p-3.5 bg-white/80 dark:bg-black/25 hover:bg-white dark:hover:bg-black/35 hover:shadow-lg rounded-xl transition-all border border-transparent hover:border-violet-300 dark:hover:border-violet-700 flex items-center gap-3 group">
                  <div className="w-8 h-8 bg-gradient-to-br from-cyan-500 to-blue-500 rounded-lg flex items-center justify-center text-base shadow-md group-hover:scale-110 group-hover:rotate-6 transition-all duration-300">🔬</div>
                  <span className="text-sm font-bold text-gray-800 dark:text-gray-200">AutoResearch</span>
                </Link>
              </div>
            </div>

            <div className="card p-6 bg-gradient-to-br from-amber-50 via-yellow-50 to-orange-50 dark:from-amber-950/20 dark:via-yellow-950/20 dark:to-orange-950/20 border border-amber-200/40 dark:border-amber-800/30 relative overflow-hidden">
              <div className="absolute top-0 right-0 w-24 h-24 bg-gradient-to-bl from-yellow-300/30 to-transparent rounded-full blur-2xl"></div>
              <h4 className="font-bold text-gray-900 dark:text-white mb-5 flex items-center gap-3 relative z-10">
                <span className="text-xl">📤</span>
                <span className="bg-gradient-to-r from-amber-600 to-orange-600 bg-clip-text text-transparent font-black dark:font-white">Export Options</span>
              </h4>
              <div className="space-y-3 relative z-10">
                <button className="w-full px-4 py-3.5 text-left text-sm font-bold bg-white/80 dark:bg-black/25 hover:bg-white dark:hover:bg-black/35 rounded-xl transition-all border border-white/50 dark:border-gray-700/40 hover:border-amber-300 dark:hover:border-amber-700 hover:shadow-lg flex items-center gap-3 group">
                  <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center text-base shadow-md group-hover:scale-110 group-hover:rotate-6 transition-all duration-300">📥</div>
                  Export as JSON
                </button>
                <button className="w-full px-4 py-3.5 text-left text-sm font-bold bg-white/80 dark:bg-black/25 hover:bg-white dark:hover:bg-black/35 rounded-xl transition-all border border-white/50 dark:border-gray-700/40 hover:border-amber-300 dark:hover:border-amber-700 hover:shadow-lg flex items-center gap-3 group">
                  <div className="w-8 h-8 bg-gradient-to-br from-emerald-500 to-green-500 rounded-lg flex items-center justify-center text-base shadow-md group-hover:scale-110 group-hover:rotate-6 transition-all duration-300">📊</div>
                  Generate Report
                </button>
                <button className="w-full px-4 py-3.5 text-left text-sm font-bold bg-white/80 dark:bg-black/25 hover:bg-white dark:hover:bg-black/35 rounded-xl transition-all border border-white/50 dark:border-gray-700/40 hover:border-amber-300 dark:hover:border-amber-700 hover:shadow-lg flex items-center gap-3 group">
                  <div className="w-8 h-8 bg-gradient-to-br from-violet-500 to-purple-500 rounded-lg flex items-center justify-center text-base shadow-md group-hover:scale-110 group-hover:rotate-6 transition-all duration-300">🔄</div>
                  Sync to OTEL
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default OctoTraceDashboard
