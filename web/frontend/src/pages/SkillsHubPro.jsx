import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

const SkillsHub = () => {
  const [activeView, setActiveView] = useState('repositories')
  const [activeTab, setActiveTab] = useState('all')
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [showAnalytics, setShowAnalytics] = useState(false)
  const [newRepo, setNewRepo] = useState({ name: '', description: '', visibility: 'public', category: '' })
  const [creating, setCreating] = useState(false)
  
  const [repositories, setRepositories] = useState([])
  const [pullRequests, setPullRequests] = useState([])
  const [issues, setIssues] = useState([])
  const [activityFeed, setActivityFeed] = useState([])
  const [stats, setStats] = useState(null)

  useEffect(() => {
    fetchHubData()
  }, [])

  const fetchHubData = async () => {
    setLoading(true)
    try {
      const [reposRes, statsRes] = await Promise.all([
        fetch('http://localhost:3005/api/v1/hub/repositories'),
        fetch('http://localhost:3005/api/v1/hub/stats')
      ])
      
      if (reposRes.ok) {
        const reposData = await reposRes.json()
        setRepositories(reposData.repositories || [])
      }
      
      if (statsRes.ok) {
        setStats(await statsRes.json())
      }

      setPullRequests([
        { id: 'pr-001', title: 'Add multi-language support', repo: 'data-analyzer', author: 'alice', status: 'open', created: '2h ago', comments: 3 },
        { id: 'pr-002', title: 'Optimize memory usage', repo: 'code-reviewer', author: 'bob', status: 'review', created: '5h ago', comments: 7 },
        { id: 'pr-003', title: 'Fix edge case in parser', repo: 'doc-summarizer', author: 'charlie', status: 'merged', created: '1d ago', comments: 2 }
      ])

      setIssues([
        { id: 'issue-001', title: 'Performance degradation on large inputs', type: 'bug', priority: 'high', status: 'open', repo: 'data-analyzer' },
        { id: 'issue-002', title: 'Add streaming support', type: 'feature', priority: 'medium', status: 'open', repo: 'api-handler' },
        { id: 'issue-003', title: 'Documentation incomplete', type: 'docs', priority: 'low', status: 'closed', repo: 'code-reviewer' }
      ])

      setActivityFeed([
        { user: 'alice', action: 'pushed to', target: 'data-analyzer/main', time: '5m ago', icon: '📤' },
        { user: 'bob', action: 'opened MR in', target: 'code-reviewer', time: '2h ago', icon: '🔀' },
        { user: 'charlie', action: 'starred', target: 'doc-summarizer', time: '3h ago', icon: '⭐' },
        { user: 'diana', action: 'forked', target: 'api-handler', time: '5h ago', icon: '🍴' },
        { user: 'eve', action: 'closed issue in', target: 'data-analyzer', time: '1d ago', icon: '✅' },
        { user: 'frank', action: 'published', target: 'new-skill-template', time: '2d ago', icon: '🚀' }
      ])

    } catch (error) {
      console.error('Error fetching hub data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateRepository = async () => {
    if (!newRepo.name.trim()) return
    
    setCreating(true)
    try {
      const response = await fetch('http://localhost:3005/api/v1/hub/repositories', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: newRepo.name,
          description: newRepo.description,
          visibility: newRepo.visibility,
          owner_id: 'demo-user'
        })
      })
      
      if (response.ok) {
        setShowCreateModal(false)
        setNewRepo({ name: '', description: '', visibility: 'public', category: '' })
        fetchHubData()
      }
    } catch (error) {
      console.error('Error creating repository:', error)
    } finally {
      setCreating(false)
    }
  }

  const getVisibilityBadge = (visibility) => {
    switch(visibility) {
      case 'public': return <span className="px-2.5 py-1 bg-emerald-50 dark:bg-emerald-950/30 text-emerald-700 dark:text-emerald-300 rounded-lg text-xs font-bold border border-emerald-200 dark:border-emerald-800 flex items-center gap-1"><span className="w-1.5 h-1.5 bg-emerald-500 rounded-full"></span>Public</span>
      case 'private': return <span className="px-2.5 py-1 bg-amber-50 dark:bg-amber-950/30 text-amber-700 dark:text-amber-300 rounded-lg text-xs font-bold border border-amber-200 dark:border-amber-800 flex items-center gap-1"><span className="w-1.5 h-1.5 bg-amber-500 rounded-full"></span>Private</span>
      default: return <span className="px-2.5 py-1 bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 rounded-lg text-xs font-bold border border-gray-200 dark:border-gray-700 flex items-center gap-1"><span className="w-1.5 h-1.5 bg-gray-400 rounded-full"></span>{visibility}</span>
    }
  }

  const getPRStatusStyle = (status) => {
    switch(status) {
      case 'open': return 'bg-emerald-50 dark:bg-emerald-950/20 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800'
      case 'review': return 'bg-amber-50 dark:bg-amber-950/20 text-amber-700 dark:text-amber-300 border border-amber-200 dark:border-amber-800'
      case 'merged': return 'bg-violet-50 dark:bg-violet-950/20 text-violet-700 dark:text-violet-300 border border-violet-200 dark:border-violet-800'
      case 'closed': return 'bg-red-50 dark:bg-red-950/20 text-red-700 dark:text-red-300 border border-red-200 dark:border-red-800'
      default: return 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400'
    }
  }

  const getIssuePriorityStyle = (priority) => {
    switch(priority) {
      case 'critical': return 'text-red-600 font-bold bg-red-50 dark:bg-red-950/20 px-2 py-0.5 rounded'
      case 'high': return 'text-orange-600 font-semibold bg-orange-50 dark:bg-orange-950/20 px-2 py-0.5 rounded'
      case 'medium': return 'text-yellow-600 bg-yellow-50 dark:bg-yellow-950/20 px-2 py-0.5 rounded'
      case 'low': return 'text-blue-500 bg-blue-50 dark:bg-blue-950/20 px-2 py-0.5 rounded'
      default: return 'text-gray-500'
    }
  }

  const filteredRepos = repositories.filter(repo => {
    if (activeTab === 'public') return repo.visibility === 'public'
    if (activeTab === 'private') return repo.visibility === 'private'
    if (activeTab === 'starred') return (repo.star_count || 0) > 5
    return true
  }).filter(repo =>
    !searchQuery || repo.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    repo.description?.toLowerCase().includes(searchQuery.toLowerCase())
  )

  return (
    <div className="min-h-screen py-8">
      <div className="max-w-7xl mx-auto px-6">
        
        {/* Header Section - Optimized Layout */}
          <div className="mb-12">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-6 group">
              <div className="w-20 h-20 bg-gradient-to-br from-violet-500 via-purple-600 to-fuchsia-600 rounded-3xl flex items-center justify-center text-white text-4xl shadow-2xl shadow-purple-500/40 relative overflow-hidden ring-4 ring-purple-500/20 shrink-0 transform hover:scale-105 hover:shadow-3xl transition-all duration-300">
                <span className="relative z-10 drop-shadow-lg">📦</span>
                <div className="absolute inset-0 bg-gradient-to-br from-white/20 via-white/10 to-transparent animate-pulse"></div>
                <div className="absolute -inset-1 bg-gradient-to-br from-violet-400/30 to-fuchsia-400/30 rounded-3xl blur-xl opacity-60 group-hover:opacity-100 transition-opacity"></div>
              </div>
              <div className="min-w-0 flex-1">
                <h1 className="text-5xl font-black bg-gradient-to-r from-blue-600 via-cyan-500 to-blue-700 dark:from-blue-400 dark:via-cyan-300 dark:to-blue-400 bg-clip-text text-transparent mb-3 tracking-wide drop-shadow-xl filter leading-snug">
                  Skills Hub
                </h1>
                <p className="text-gray-700 dark:text-gray-300 text-base leading-relaxed font-medium max-w-2xl opacity-90">
                  The intelligent skill ecosystem for AI agents — create, manage, collaborate, and evolve your skills with version control and seamless integration
                </p>
              </div>
            </div>
            
            {/* Action Buttons - Enhanced */}
            <div className="flex gap-3 shrink-0">
              <Link 
                to="/skill-creator-studio" 
                className="group px-6 py-3 bg-gradient-to-r from-blue-500 via-cyan-500 to-blue-600 hover:from-blue-600 hover:to-cyan-700 text-white rounded-xl font-bold transition-all duration-300 shadow-lg shadow-blue-500/25 hover:shadow-xl hover:shadow-blue-500/40 flex items-center gap-2.5 border border-transparent hover:border-white/20"
              >
                <span className="text-lg group-hover:rotate-12 transition-transform duration-300 inline-block">⚡</span> 
                Create Skill
                <span className="text-xs opacity-80 group-hover:opacity-100 transition-opacity">NEW</span>
                <span className="group-hover:translate-x-0.5 transition-transform">→</span>
              </Link>
              <button 
                onClick={() => setShowCreateModal(true)}
                className="px-6 py-3 bg-gradient-to-r from-violet-600 via-purple-600 to-fuchsia-600 hover:from-violet-700 hover:to-fuchsia-700 text-white rounded-xl font-bold transition-all duration-300 shadow-xl shadow-purple-500/30 hover:shadow-purple-500/50 flex items-center gap-2.5 border border-purple-400/30 hover:border-purple-300/50"
              >
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8H4" />
                </svg>
                New Repository
                <span className="text-xs opacity-80">PRO</span>
              </button>
              <button 
                onClick={() => setShowAnalytics(!showAnalytics)}
                className="px-5 py-3 bg-gradient-to-r from-emerald-500 via-teal-500 to-green-600 hover:from-emerald-600 hover:to-green-700 text-white rounded-xl font-bold transition-all duration-300 shadow-lg shadow-emerald-500/25 hover:shadow-xl hover:shadow-emerald-500/40 flex items-center gap-2"
              >
                📊 Analytics
              </button>
            </div>
          </div>

          {/* Stats Cards */}
          {stats && (
            <div className="grid grid-cols-3 md:grid-cols-6 gap-3">
              {[
                { label: 'Repositories', value: stats.total_repositories || 24, icon: '📦', color: 'from-violet-500 to-purple-500' },
                { label: 'Public', value: stats.public_repos || 18, icon: '🌐', color: 'from-emerald-500 to-teal-500' },
                { label: 'Private', value: stats.private_repos || 6, icon: '🔒', color: 'from-amber-500 to-orange-500' },
                { label: 'Merge Requests', value: pullRequests.length, icon: '🔀', color: 'from-fuchsia-500 to-pink-500' },
                { label: 'Open Issues', value: issues.filter(i => i.status === 'open').length, icon: '🐛', color: 'from-red-500 to-rose-500' },
                { label: 'Collaborators', value: stats.total_collaborators || 42, icon: '👥', color: 'from-blue-500 to-cyan-500' }
              ].map((stat, idx) => (
                <div key={idx} className={`card p-4 text-center relative overflow-hidden group hover:scale-[1.02] transition-transform duration-200`}>
                  <div className={`absolute inset-0 bg-gradient-to-br ${stat.color} opacity-[0.05] group-hover:opacity-[0.1] transition-opacity`}></div>
                  <div className="relative">
                    <div className="text-2xl mb-1">{stat.icon}</div>
                    <div className="text-xl font-bold text-gray-900 dark:text-gray-100">{stat.value}</div>
                    <div className="text-[11px] text-gray-600 dark:text-gray-400 mt-0.5 font-medium">{stat.label}</div>
                  </div>
                </div>
              ))}
            </div>
          )}

        {/* Skill Library Analytics - Advanced Feature */}
        <div className="mb-8 bg-gradient-to-br from-emerald-50 via-teal-50 to-green-50 dark:from-emerald-950/20 dark:via-teal-950/20 dark:to-green-950/20 rounded-3xl p-6 border border-emerald-200/50 dark:border-emerald-800/30 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-40 h-40 bg-gradient-to-bl from-emerald-300/20 to-transparent rounded-full blur-3xl"></div>
          
          <div className="relative z-10">
            <div className="flex items-center justify-between mb-5">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-gradient-to-br from-emerald-600 to-green-600 rounded-xl flex items-center justify-center text-white text-lg shadow-lg shadow-emerald-500/30 ring-2 ring-emerald-500/20">
                  📊
                </div>
                <h3 className="text-xl font-black bg-gradient-to-r from-emerald-700 to-green-700 dark:from-emerald-300 dark:to-green-300 bg-clip-text text-transparent">
                  Skill Library Analytics
                </h3>
              </div>
            </div>

            {showAnalytics && (
              <div className="mt-6 space-y-6">
                {/* Efficiency Metrics Grid */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                  {[
                    { 
                      metric: 'Avg Token Savings', 
                      value: '78%', 
                      icon: '⚡', 
                      desc: 'Across all composite skills',
                      color: 'from-green-500 to-emerald-500',
                      trend: '+12% vs last week'
                    },
                    { 
                      metric: 'Total Reuses', 
                      value: '1,247', 
                      icon: '🔄', 
                      desc: 'Skill invocations saved',
                      color: 'from-blue-500 to-cyan-500',
                      trend: '+234 this month'
                    },
                    { 
                      metric: 'Active Composites', 
                      value: '34', 
                      icon: '🔗', 
                      desc: 'Multi-skill workflows',
                      color: 'from-violet-500 to-purple-500',
                      trend: '+5 new'
                    },
                    { 
                      metric: 'Library Coverage', 
                      value: '94%', 
                      icon: '📚', 
                      desc: 'Of common use cases',
                      color: 'from-amber-500 to-orange-500',
                      trend: '+8%'
                    }
                  ].map((item, idx) => (
                    <div key={idx} className="bg-white/80 dark:bg-black/25 rounded-2xl p-5 border border-white/50 dark:border-gray-700/40 hover:shadow-xl transition-all group">
                      <div className="flex items-start justify-between mb-3">
                        <div className={`w-10 h-10 bg-gradient-to-br ${item.color} rounded-xl flex items-center justify-center text-lg shadow-md group-hover:scale-110 group-hover:rotate-6 transition-all duration-300`}>
                          {item.icon}
                        </div>
                        <span className={`text-xs font-bold px-2 py-1 rounded-md ${item.trend.includes('+') ? 'bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-300' : 'bg-gray-100 text-gray-600'}`}>
                          {item.trend}
                        </span>
                      </div>
                      <div className="text-3xl font-black bg-gradient-to-r from-gray-900 to-gray-700 dark:from-white dark:to-gray-200 bg-clip-text text-transparent mb-1">
                        {item.value}
                      </div>
                      <div className="text-sm font-bold text-gray-800 dark:text-gray-200">{item.metric}</div>
                      <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">{item.desc}</div>
                    </div>
                  ))}
                </div>

                {/* Top Performing Skills */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
                  <div className="bg-white/80 dark:bg-black/25 rounded-2xl p-5 border border-white/50 dark:border-gray-700/40">
                    <h4 className="font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                      <span className="w-7 h-7 bg-gradient-to-br from-yellow-500 to-orange-500 rounded-lg flex items-center justify-center text-sm">🏆</span>
                      Top Performing Skills (by Reuse)
                    </h4>
                    <div className="space-y-2.5">
                      {[
                        { name: 'Web Research Agent', uses: 342, savings: '82%' },
                        { name: 'Document Parser Pro', uses: 287, savings: '76%' },
                        { name: 'Code Generator', uses: 256, savings: '71%' },
                        { name: 'Data Analyst Suite', uses: 198, savings: '68%' },
                        { name: 'API Integrator Hub', uses: 164, savings: '64%' }
                      ].map((skill, idx) => (
                        <div key={idx} className="flex items-center gap-3 p-3.5 bg-gradient-to-r from-yellow-50 to-orange-50 dark:from-yellow-900/15 dark:to-orange-900/15 rounded-xl hover:shadow-md transition-all group">
                          <div className={`w-8 h-8 rounded-lg flex items-center justify-center text-sm font-bold text-white shadow-md ${
                            idx === 0 ? 'bg-gradient-to-br from-yellow-400 to-orange-500' :
                            idx === 1 ? 'bg-gradient-to-br from-gray-400 to-gray-500' :
                            idx === 2 ? 'bg-gradient-to-br from-amber-600 to-amber-700' :
                            'bg-gradient-to-br from-orange-400 to-red-500'
                          }`}>
                            #{idx + 1}
                          </div>
                          <span className="font-bold text-sm text-gray-800 dark:text-gray-200 flex-1">{skill.name}</span>
                          <span className="text-xs font-extrabold text-gray-600 dark:text-gray-400">{skill.uses} uses</span>
                          <span className="text-xs font-black px-2.5 py-1 rounded-md bg-gradient-to-r from-green-500 to-emerald-500 text-white shadow-sm">
                            {skill.savings}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Skill Dependency Graph Preview */}
                  <div className="bg-white/80 dark:bg-black/25 rounded-2xl p-5 border border-white/50 dark:border-gray-700/40">
                    <h4 className="font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                      <span className="w-7 h-7 bg-gradient-to-br from-violet-500 to-purple-500 rounded-lg flex items-center justify-center text-sm">🕸️</span>
                      Composite Skill Dependencies
                    </h4>
                    <div className="space-y-3">
                      {[
                        {
                          composite: 'Full Research Workflow',
                          atoms: ['Web Search', 'Content Extract', 'Summary Gen', 'Data Format'],
                          usage: 89,
                          complexity: 'High'
                        },
                        {
                          composite: 'Auto Documentation Pipeline',
                          atoms: ['Code Parse', 'Doc Generate', 'Format Output'],
                          usage: 156,
                          complexity: 'Medium'
                        },
                        {
                          composite: 'Data Analysis Suite',
                          atoms: ['Data Load', 'Clean', 'Visualize', 'Report'],
                          usage: 203,
                          complexity: 'Medium'
                        }
                      ].map((comp, idx) => (
                        <div key={idx} className="p-4 bg-gradient-to-br from-violet-50 to-purple-50 dark:from-violet-900/20 dark:to-purple-900/20 rounded-xl border border-violet-200/30 dark:border-violet-800/20 hover:shadow-lg transition-all group">
                          <div className="flex items-center justify-between mb-3">
                            <h5 className="font-bold text-sm text-gray-900 dark:text-gray-100">{comp.composite}</h5>
                            <div className="flex gap-2">
                              <span className="text-xs font-bold px-2 py-1 rounded-md bg-violet-100 text-violet-700 dark:bg-violet-900/30 dark:text-violet-300">
                                {comp.usage}× used
                              </span>
                              <span className={`text-xs font-bold px-2 py-1 rounded-md ${
                                comp.complexity === 'High' ? 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300' : 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300'
                              }`}>
                                {comp.complexity}
                              </span>
                            </div>
                          </div>
                          <div className="flex flex-wrap gap-2">
                            {comp.atoms.map((atom, aIdx) => (
                              <span key={aIdx} className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-white dark:bg-black/30 rounded-lg text-xs font-semibold text-gray-700 dark:text-gray-300 border border-gray-200 dark:border-gray-700 shadow-sm">
                                <span className="w-1.5 h-1.5 rounded-full bg-violet-500"></span>
                                {atom}
                              </span>
                            ))}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
        </div>

        {/* View Tabs */}
        <div className="flex gap-1 p-1.5 bg-gray-100/80 dark:bg-gray-800/60 rounded-2xl border border-gray-200/60 dark:border-gray-700/50 mb-6 overflow-x-auto">
          {[
            { id: 'repositories', label: 'Repositories', icon: '📦' },
            { id: 'pull-requests', label: 'Merge Requests', icon: '🔀' },
            { id: 'issues', label: 'Issues', icon: '🐛' },
            { id: 'activity', label: 'Activity Feed', icon: '📡' },
            { id: 'explore', label: 'Explore', icon: '🔍' }
          ].map((view) => (
            <button
              key={view.id}
              onClick={() => setActiveView(view.id)}
              className={`px-5 py-2.5 whitespace-nowrap transition-all duration-200 rounded-xl flex items-center gap-2 text-sm font-semibold ${
                activeView === view.id
                  ? 'bg-white dark:bg-gray-700 text-violet-700 dark:text-violet-300 shadow-md'
                  : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800'
              }`}
            >
              <span>{view.icon}</span> {view.label}
            </button>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          
          {/* Main Content Area */}
          <div className="lg:col-span-3 space-y-6">
            
            {/* Repositories / Explore View */}
            {(activeView === 'repositories' || activeView === 'explore') && (
              <>
                {/* Search & Filter Bar */}
                <div className="card p-5">
                  <div className="flex flex-col md:flex-row gap-3">
                    <div className="flex-1 relative">
                      <input
                        type="text"
                        placeholder="Search skills by name or description..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="w-full pl-11 pr-4 py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-xl focus:outline-none focus:ring-2 focus:ring-violet-500/40 focus:border-violet-400 text-gray-900 dark:text-gray-100 placeholder:text-gray-400 dark:placeholder:text-gray-500 transition-all font-medium"
                      />
                      <span className="absolute left-4 top-1/2 -translate-y-1/2 text-lg">🔍</span>
                      {searchQuery && (
                        <button onClick={() => setSearchQuery('')} className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">×</button>
                      )}
                    </div>
                    <select className="px-4 py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-xl focus:outline-none focus:ring-2 focus:ring-violet-500/40 text-gray-900 dark:text-gray-100 font-semibold cursor-pointer hover:border-violet-400 transition-all min-w-[150px] appearance-none">
                      <option value="" className="text-gray-500">All Types</option>
                      <option value="skill-pack" className="text-gray-900">Skill Pack</option>
                      <option value="template" className="text-gray-900">Template</option>
                      <option value="tool-integration" className="text-gray-900">Tool Integration</option>
                      <option value="agent-module" className="text-gray-900">Agent Module</option>
                    </select>
                    <select className="px-4 py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-xl focus:outline-none focus:ring-2 focus:ring-violet-500/40 text-gray-900 dark:text-gray-100 font-semibold cursor-pointer hover:border-violet-400 transition-all min-w-[160px] appearance-none">
                      <option value="updated" className="text-gray-900">Last Updated</option>
                      <option value="name" className="text-gray-900">Name A-Z</option>
                      <option value="stars" className="text-gray-900">Most Stars</option>
                      <option value="newest" className="text-gray-900">Newest First</option>
                      <option value="downloads" className="text-gray-900">Most Downloads</option>
                    </select>
                  </div>
                </div>

                {/* Filter Tabs */}
                <div className="flex gap-2">
                  {['all', 'public', 'private', 'starred'].map((tab) => (
                    <button
                      key={tab}
                      onClick={() => setActiveTab(tab)}
                      className={`px-5 py-2.5 rounded-xl text-sm font-semibold transition-all capitalize ${
                        activeTab === tab
                          ? 'bg-gradient-to-r from-violet-600 to-purple-600 text-white shadow-lg shadow-violet-500/25 scale-[1.02]'
                          : 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700 hover:text-gray-900 dark:hover:text-gray-200 border border-transparent hover:border-gray-300 dark:hover:border-gray-600'
                      }`}
                    >
                      {tab === 'all' && 'All'}
                      {tab === 'public' && 'Public'}
                      {tab === 'private' && 'Private'}
                      {tab === 'starred' && 'Starred'}
                    </button>
                  ))}
                  
                  <div className="ml-auto flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400">
                    <span className="font-mono font-bold text-gray-900 dark:text-gray-100 bg-gray-100 dark:bg-gray-800 px-3 py-1.5 rounded-lg">{filteredRepos.length}</span>
                    results
                  </div>
                </div>

                {/* Repository List */}
                <div className="space-y-3">
                  {loading ? (
                    [...Array(5)].map((_, i) => (
                      <div key={i} className="card p-7 animate-pulse space-y-3">
                        <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded-lg w-1/3"></div>
                        <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded-lg w-2/3"></div>
                        <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded-lg w-1/4"></div>
                      </div>
                    ))
                  ) : filteredRepos.length > 0 ? (
                    filteredRepos.map((repo) => (
                      <div 
                        key={repo.repo_id || repo.name} 
                        className="card p-6 hover:shadow-xl hover:shadow-purple-500/10 hover:border-violet-300 dark:hover:border-violet-700 transition-all duration-300 group cursor-pointer relative overflow-hidden"
                      >
                        <div className={`absolute inset-0 bg-gradient-to-r from-violet-500/0 via-purple-500/0 to-fuchsia-500/0 group-hover:from-violet-500/[0.02] group-hover:to-fuchsia-500/[0.02] transition-all`}></div>
                        
                        <div className="relative flex items-start justify-between">
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center gap-3 mb-2.5 flex-wrap">
                              <Link 
                                to={`/skills-hub/${repo.repo_id || repo.name}`}
                                className="text-lg font-bold text-violet-700 dark:text-violet-300 hover:text-violet-600 dark:hover:text-violet-200 truncate transition-colors"
                              >
                                {repo.name}
                              </Link>
                              {getVisibilityBadge(repo.visibility)}
                              <span className="px-2.5 py-1 bg-cyan-50 dark:bg-cyan-950/30 text-cyan-700 dark:text-cyan-300 rounded-lg text-xs font-bold border border-cyan-200 dark:border-cyan-800">
                                {repo.language || 'Python'}
                              </span>
                            </div>
                            <p className="text-sm text-gray-600 dark:text-gray-400 mb-4 line-clamp-2 leading-relaxed">
                              {repo.description || 'No description provided'}
                            </p>
                            <div className="flex items-center gap-6 text-xs text-gray-500 dark:text-gray-400">
                              <button className="flex items-center gap-1.5 font-semibold hover:text-amber-600 dark:hover:text-amber-400 transition-colors group/star">
                                <span className="text-base group-hover/star:scale-125 transition-transform">⭐</span> 
                                <span className="text-gray-800 dark:text-gray-200">{repo.star_count || 0}</span>
                              </button>
                              <button className="flex items-center gap-1.5 font-semibold hover:text-blue-600 dark:hover:text-blue-400 transition-colors group/fork">
                                <span className="text-base group-hover/fork:scale-125 transition-transform">🍴</span> 
                                <span className="text-gray-800 dark:text-gray-200">{repo.fork_count || 0}</span>
                              </button>
                              <button className="flex items-center gap-1.5 font-semibold hover:text-green-600 dark:hover:text-green-400 transition-colors group/watch">
                                <span className="text-base group-hover/watch:scale-125 transition-transform">👁️</span> 
                                <span className="text-gray-800 dark:text-gray-200">{repo.watch_count || 0}</span>
                              </button>
                              <span className="ml-auto text-gray-400 dark:text-gray-500 font-mono">Updated {repo.updated_at || 'recently'}</span>
                            </div>
                          </div>
                          
                          {/* Hover Action Buttons */}
                          <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-all ml-4 shrink-0 translate-x-2 group-hover:translate-x-0">
                            <button className="px-4 py-2 text-xs font-bold bg-amber-50 hover:bg-amber-100 dark:bg-amber-950/20 dark:hover:bg-amber-950/40 text-amber-700 dark:text-amber-300 rounded-xl border border-amber-200 dark:border-amber-800 transition-all flex items-center gap-1.5 shadow-sm">
                              ⭐ Star
                            </button>
                            <button className="px-4 py-2 text-xs font-bold bg-blue-50 hover:bg-blue-100 dark:bg-blue-950/20 dark:hover:bg-blue-950/40 text-blue-700 dark:text-blue-300 rounded-xl border border-blue-200 dark:border-blue-800 transition-all flex items-center gap-1.5 shadow-sm">
                              🍴 Fork
                            </button>
                          </div>
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className="card p-16 text-center relative overflow-hidden">
                      <div className="absolute inset-0 bg-gradient-to-br from-violet-50 via-purple-50 to-fuchsia-50 dark:from-violet-950/10 dark:via-purple-950/10 dark:to-fuchsia-950/10"></div>
                      <div className="relative">
                        <div className="text-6xl mb-4">{activeView === 'explore' ? '🔍' : '📦'}</div>
                        <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
                          No repositories found
                        </h3>
                        <p className="text-gray-600 dark:text-gray-400 mb-6 max-w-md mx-auto">
                          {searchQuery ? 'Try adjusting your search terms or filters' : 'Create your first repository to start building your skill collection'}
                        </p>
                        <button 
                          onClick={() => setShowCreateModal(true)}
                          className="px-6 py-3 bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-700 hover:to-purple-700 text-white rounded-xl font-semibold transition-all shadow-lg shadow-purple-500/25 inline-flex items-center gap-2"
                        >
                          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                            <path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8H4" />
                          </svg>
                          Create Your First Repository
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              </>
            )}

            {/* Pull Requests View */}
            {activeView === 'pull-requests' && (
              <div className="card p-7 space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-gradient-to-r from-fuchsia-500 to-pink-500 rounded-xl flex items-center justify-center text-white text-lg shadow-lg shadow-fuchsia-500/30">
                      🔀
                    </div>
                    <div>
                      <h3 className="font-bold text-lg text-gray-900 dark:text-white">Merge Requests</h3>
                      <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">Review and merge code changes</p>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <button className="px-4 py-2 text-sm font-semibold bg-emerald-50 dark:bg-emerald-950/20 text-emerald-700 dark:text-emerald-300 rounded-xl border border-emerald-200 dark:border-emerald-800 hover:bg-emerald-100 dark:hover:bg-emerald-950/30 transition-colors flex items-center gap-1.5">
                      <span className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse shadow-sm shadow-emerald-500/50"></span>
                      Open ({pullRequests.filter(p => p.status === 'open').length})
                    </button>
                    <button className="px-4 py-2 text-sm font-semibold bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 rounded-xl hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors">
                      All ({pullRequests.length})
                    </button>
                  </div>
                </div>
                
                {pullRequests.map((pr) => (
                  <div key={pr.id} className="p-5 bg-gray-50 dark:bg-gray-800/80 rounded-2xl hover:bg-gray-100 dark:hover:bg-gray-700 transition-all border border-transparent hover:border-violet-300 dark:hover:border-violet-700 group">
                    <div className="flex items-start justify-between">
                      <div className="flex items-start gap-4">
                        <span className={`mt-1 w-3.5 h-3.5 rounded-full shrink-0 ${
                          pr.status === 'open' ? 'bg-emerald-500 shadow-md shadow-emerald-500/50' :
                          pr.status === 'review' ? 'bg-amber-500 shadow-md shadow-amber-500/50' :
                          pr.status === 'merged' ? 'bg-violet-500 shadow-md shadow-violet-500/50' : 'bg-red-500 shadow-md shadow-red-500/50'
                        }`}></span>
                        <div className="flex-1">
                          <div className="flex items-center gap-2.5 mb-1.5 flex-wrap">
                            <span className="font-bold text-gray-900 dark:text-gray-100">{pr.title}</span>
                            <span className={`px-2.5 py-1 rounded-lg text-xs font-bold capitalize border ${getPRStatusStyle(pr.status)}`}>
                              {pr.status.charAt(0).toUpperCase() + pr.status.slice(1)}
                            </span>
                          </div>
                          <div className="text-xs text-gray-500 dark:text-gray-400 flex items-center gap-3">
                            <span className="font-mono bg-gray-100 dark:bg-gray-700 px-2.5 py-1 rounded-lg font-semibold text-gray-700 dark:text-gray-300">{pr.repo}</span>
                            <span>by <strong className="text-gray-800 dark:text-gray-200">{pr.author}</strong></span>
                            <span>{pr.created}</span>
                            <span className="flex items-center gap-1 text-gray-800 dark:text-gray-200">💬 <strong>{pr.comments}</strong></span>
                          </div>
                        </div>
                      </div>
                      <button className="px-5 py-2 text-xs font-bold bg-gradient-to-r from-violet-600 to-purple-600 text-white rounded-xl hover:opacity-90 transition-opacity shrink-0 shadow-lg shadow-violet-500/20 group-hover:scale-105 transition-transform">
                        Review →
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Issues View */}
            {activeView === 'issues' && (
              <div className="card p-7 space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-gradient-to-r from-red-500 to-rose-500 rounded-xl flex items-center justify-center text-white text-lg shadow-lg shadow-red-500/30">
                      🐛
                    </div>
                    <div>
                      <h3 className="font-bold text-lg text-gray-900 dark:text-white">Issues</h3>
                      <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">Track bugs, features, and improvements</p>
                    </div>
                  </div>
                  <button className="px-5 py-2.5 text-sm font-bold bg-gradient-to-r from-violet-600 to-purple-600 text-white rounded-xl hover:opacity-90 transition-opacity shadow-lg shadow-violet-500/25 flex items-center gap-2">
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8H4" />
                    </svg>
                    New Issue
                  </button>
                </div>
                
                {issues.map((issue) => (
                  <div key={issue.id} className="p-5 bg-gray-50 dark:bg-gray-800/80 rounded-2xl hover:bg-gray-100 dark:hover:bg-gray-700 transition-all border border-transparent hover:border-violet-300 dark:hover:border-violet-700 group">
                    <div className="flex items-start gap-4">
                      <span className={`mt-0.5 text-xl shrink-0 ${
                        issue.type === 'bug' ? '🐛' : issue.type === 'feature' ? '✨' : '📖'
                      }`}></span>
                      <div className="flex-1">
                        <div className="flex items-center gap-2.5 mb-1.5 flex-wrap">
                          <span className="font-bold text-gray-900 dark:text-gray-100">{issue.title}</span>
                          <span className={`text-xs font-bold uppercase tracking-wide ${getIssuePriorityStyle(issue.priority)}`}>
                            {issue.priority}
                          </span>
                          {issue.status === 'closed' && (
                            <span className="px-2.5 py-1 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 rounded-lg text-xs font-bold">Closed</span>
                          )}
                        </div>
                        <div className="text-xs text-gray-500 dark:text-gray-400 flex items-center gap-3">
                          <span className="font-mono bg-gray-100 dark:bg-gray-700 px-2.5 py-1 rounded-lg font-semibold text-gray-700 dark:text-gray-300">{issue.repo}</span>
                          <span className="capitalize px-2.5 py-1 rounded-lg bg-gray-100 dark:bg-gray-700 font-semibold text-gray-600 dark:text-gray-400">{issue.type}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Activity Feed View */}
            {activeView === 'activity' && (
              <div className="card p-7">
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-xl flex items-center justify-center text-white text-lg shadow-lg shadow-cyan-500/30">
                    📡
                  </div>
                  <div>
                    <h3 className="font-bold text-lg text-gray-900 dark:text-white">Recent Activity</h3>
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">Latest actions across all repositories</p>
                  </div>
                </div>
                {activityFeed.map((activity, idx) => (
                  <div key={idx} className="flex items-start gap-4 pb-5 border-b border-gray-200 dark:border-gray-700 last:border-0 last:pb-0 hover:bg-gray-50 dark:hover:bg-gray-800/50 -mx-3 px-3 py-3 rounded-xl transition-all group">
                    <div className="w-11 h-11 bg-gradient-to-br from-violet-500 via-purple-500 to-fuchsia-500 rounded-xl flex items-center justify-center text-white text-sm font-bold shrink-0 shadow-md shadow-purple-500/25 group-hover:scale-110 transition-transform">
                      {activity.user[0].toUpperCase()}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm text-gray-800 dark:text-gray-200 leading-relaxed">
                        <span className="font-bold text-gray-900 dark:text-gray-100">{activity.user}</span>{' '}
                        <span className="text-gray-600 dark:text-gray-400">{activity.action}</span>{' '}
                        <span className="text-violet-600 dark:text-violet-400 hover:text-violet-500 dark:hover:text-violet-300 hover:underline cursor-pointer font-semibold truncate inline-block max-w-[220px] align-bottom">{activity.target}</span>
                      </p>
                      <p className="text-xs text-gray-500 dark:text-gray-400 mt-1.5 font-mono">{activity.time}</p>
                    </div>
                    <span className="text-xl shrink-0 group-hover:scale-125 transition-transform">{activity.icon}</span>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Sidebar */}
          <div className="space-y-5">
            
            {/* Quick Stats Card */}
            <div className="card p-6 bg-gradient-to-br from-violet-50 via-purple-50 to-fuchsia-50 dark:from-violet-950/20 dark:via-purple-950/20 dark:to-fuchsia-950/20 border border-violet-200/40 dark:border-violet-800/30 relative overflow-hidden">
              <div className="absolute top-0 right-0 w-24 h-24 bg-gradient-to-bl from-purple-300/30 to-transparent rounded-full blur-2xl"></div>
              <h4 className="font-bold text-gray-900 dark:text-white mb-5 flex items-center gap-3 relative z-10">
                <span className="text-xl">📊</span>
                <span className="bg-gradient-to-r from-violet-600 to-fuchsia-600 bg-clip-text text-transparent font-black dark:font-white">Your Stats</span>
              </h4>
              <div className="space-y-3.5 relative z-10">
                {[
                  { label: 'Your Repositories', value: '8', icon: '📦', color: 'from-violet-500 to-purple-500' },
                  { label: 'Contributed To', value: '12', icon: '🤝', color: 'from-blue-500 to-cyan-500' },
                  { label: 'MRs Reviewed', value: '24', icon: '✅', color: 'from-emerald-500 to-green-500' },
                  { label: 'Issues Resolved', value: '18', icon: '🎯', color: 'from-amber-500 to-orange-500' }
                ].map((item, idx) => (
                  <div key={idx} className="flex items-center justify-between p-3.5 bg-white/80 dark:bg-black/25 rounded-xl border border-white/50 dark:border-gray-700/40 hover:bg-white dark:hover:bg-black/35 hover:shadow-lg transition-all group">
                    <div className="flex items-center gap-3">
                      <div className={`w-9 h-9 bg-gradient-to-br ${item.color} rounded-xl flex items-center justify-center text-base shadow-md group-hover:scale-110 group-hover:rotate-3 transition-all duration-300`}>
                        {item.icon}
                      </div>
                      <span className="text-sm font-bold text-gray-800 dark:text-gray-200">{item.label}</span>
                    </div>
                    <span className="font-mono font-extrabold text-gray-900 dark:text-white text-sm bg-gradient-to-r from-gray-100 to-gray-200 dark:from-gray-700 dark:to-gray-600 px-3 py-1.5 rounded-lg shadow-sm">{item.value}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Top Contributors Card */}
            <div className="card p-6 bg-gradient-to-br from-amber-50 via-yellow-50 to-orange-50 dark:from-amber-950/20 dark:via-yellow-950/20 dark:to-orange-950/20 border border-amber-200/40 dark:border-amber-800/30 relative overflow-hidden">
              <div className="absolute top-0 right-0 w-24 h-24 bg-gradient-to-bl from-yellow-300/30 to-transparent rounded-full blur-2xl"></div>
              <h4 className="font-bold text-gray-900 dark:text-white mb-5 flex items-center gap-3 relative z-10">
                <span className="text-xl">🏆</span>
                <span className="bg-gradient-to-r from-amber-600 to-orange-600 bg-clip-text text-transparent font-black dark:font-white">Top Contributors</span>
              </h4>
              <div className="space-y-3 relative z-10">
                {['alice', 'bob', 'charlie', 'diana'].map((user, i) => (
                  <div key={user} className="flex items-center gap-3 p-3.5 bg-white/80 dark:bg-black/25 rounded-xl hover:bg-white dark:hover:bg-black/35 hover:shadow-lg transition-all group border border-transparent hover:border-amber-300 dark:hover:border-amber-700">
                    <div className={`w-11 h-11 rounded-xl flex items-center justify-center text-white text-base font-bold shrink-0 shadow-lg group-hover:scale-110 group-hover:rotate-6 transition-all duration-300 ${
                      i === 0 ? 'bg-gradient-to-br from-amber-400 to-orange-500' :
                      i === 1 ? 'bg-gradient-to-br from-slate-400 to-slate-500' :
                      i === 2 ? 'bg-gradient-to-br from-amber-600 to-amber-700' :
                      'bg-gradient-to-br from-orange-400 to-rose-500'
                    }`}>
                      {user[0].toUpperCase()}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="text-sm font-bold text-gray-900 dark:text-gray-100 truncate">{user}</div>
                      <div className="text-xs text-gray-600 dark:text-gray-400 mt-0.5 font-medium">{12 - i * 2} contributions</div>
                    </div>
                    <span className={`text-xs font-extrabold px-3 py-1.5 rounded-lg ${
                      i === 0 ? 'bg-gradient-to-r from-amber-400 to-orange-500 text-white shadow-md' :
                      i <= 2 ? 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 border border-gray-200 dark:border-gray-700' :
                      'bg-gray-50 dark:bg-gray-800/50 text-gray-600 dark:text-gray-400'
                    }`}>
                      #{i + 1}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Quick Actions Card */}
            <div className="card p-6 bg-gradient-to-br from-blue-50 via-indigo-50 to-cyan-50 dark:from-blue-950/20 dark:via-indigo-950/20 dark:to-cyan-950/20 border border-blue-200/40 dark:border-blue-800/30 relative overflow-hidden">
              <div className="absolute top-0 right-0 w-24 h-24 bg-gradient-to-bl from-cyan-300/30 to-transparent rounded-full blur-2xl"></div>
              <h4 className="font-bold text-gray-900 dark:text-white mb-5 flex items-center gap-3 relative z-10">
                <span className="text-xl">⚡</span>
                <span className="bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent font-black dark:font-white">Quick Actions</span>
              </h4>
              <div className="space-y-3 relative z-10">
                <button className="w-full px-4 py-3.5 text-left text-sm font-bold bg-white/80 dark:bg-black/25 hover:bg-white dark:hover:bg-black/35 rounded-xl transition-all text-gray-800 dark:text-gray-200 border border-white/50 dark:border-gray-700/40 hover:border-emerald-300 dark:hover:border-emerald-700 hover:shadow-lg flex items-center gap-3 group">
                  <div className="w-8 h-8 bg-gradient-to-br from-emerald-500 to-green-500 rounded-lg flex items-center justify-center text-base shadow-md group-hover:scale-110 group-hover:rotate-6 transition-all duration-300">🚀</div>
                  Publish to Marketplace
                </button>
                <button className="w-full px-4 py-3.5 text-left text-sm font-bold bg-white/80 dark:bg-black/25 hover:bg-white dark:hover:bg-black/35 rounded-xl transition-all text-gray-800 dark:text-gray-200 border border-white/50 dark:border-gray-700/40 hover:border-blue-300 dark:hover:border-blue-700 hover:shadow-lg flex items-center gap-3 group">
                  <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center text-base shadow-md group-hover:scale-110 group-hover:rotate-6 transition-all duration-300">👥</div>
                  Invite Collaborator
                </button>
                <button className="w-full px-4 py-3.5 text-left text-sm font-bold bg-white/80 dark:bg-black/25 hover:bg-white dark:hover:bg-black/35 rounded-xl transition-all text-gray-800 dark:text-gray-200 border border-white/50 dark:border-gray-700/40 hover:border-amber-300 dark:hover:border-amber-700 hover:shadow-lg flex items-center gap-3 group">
                  <div className="w-8 h-8 bg-gradient-to-br from-amber-500 to-orange-500 rounded-lg flex items-center justify-center text-base shadow-md group-hover:scale-110 group-hover:rotate-6 transition-all duration-300">📊</div>
                  View Analytics
                </button>
                <Link to="/evolution-workbench" className="block px-4 py-3.5 text-sm font-bold bg-violet-100/80 dark:bg-violet-900/30 hover:bg-violet-100 dark:hover:bg-violet-900/40 rounded-xl transition-all text-violet-800 dark:text-violet-300 border border-violet-200/60 dark:border-violet-800/40 hover:border-violet-300 dark:hover:border-violet-700 hover:shadow-lg flex items-center gap-3 group">
                  <div className="w-8 h-8 bg-gradient-to-br from-violet-500 to-purple-500 rounded-lg flex items-center justify-center text-base shadow-md group-hover:scale-110 group-hover:rotate-6 transition-all duration-300">🧬</div>
                  Open AI Evolution Workbench
                </Link>
                <Link to="/octo-trace" className="block px-4 py-3.5 text-sm font-bold bg-cyan-100/80 dark:bg-cyan-900/30 hover:bg-cyan-100 dark:hover:bg-cyan-900/40 rounded-xl transition-all text-cyan-800 dark:text-cyan-300 border border-cyan-200/60 dark:border-cyan-800/40 hover:border-cyan-300 dark:hover:border-cyan-700 hover:shadow-lg flex items-center gap-3 group">
                  <div className="w-8 h-8 bg-gradient-to-br from-cyan-500 to-blue-500 rounded-lg flex items-center justify-center text-base shadow-md group-hover:scale-110 group-hover:rotate-6 transition-all duration-300">🔍</div>
                  Open OctoTrace Dashboard
                </Link>
              </div>
            </div>

            {/* CTA Card */}
            <div className="card p-6 bg-gradient-to-br from-violet-600 via-purple-600 to-fuchsia-600 text-white relative overflow-hidden shadow-xl shadow-purple-500/20">
              <div className="absolute top-0 right-0 w-40 h-40 bg-white/10 rounded-full -translate-y-1/2 translate-x-1/3"></div>
              <div className="absolute bottom-0 left-0 w-28 h-28 bg-black/10 rounded-full translate-y-1/2 -translate-x-1/3"></div>
              <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-white/5 rounded-full blur-3xl"></div>

              <div className="relative z-10">
                <h4 className="font-black text-lg mb-3 flex items-center gap-3">
                  <span className="w-10 h-10 bg-white/20 backdrop-blur-md rounded-xl flex items-center justify-center text-lg shadow-lg border border-white/20">🎉</span>
                  <span className="bg-gradient-to-r from-white to-white/80 bg-clip-text text-transparent">Join the Community</span>
                </h4>
                <p className="text-sm text-white/90 mb-5 leading-relaxed font-medium pl-[52px]">
                  Connect with other developers, share your skills, and contribute to the growing ecosystem of AI agent capabilities.
                </p>
                <button className="w-full px-5 py-3.5 bg-white/25 hover:bg-white/35 backdrop-blur-md rounded-xl text-sm font-bold transition-all border border-white/30 hover:border-white/50 shadow-lg hover:shadow-xl hover:-translate-y-0.5 transform flex items-center justify-center gap-2">
                  Explore Community →
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Create Repository Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div className="absolute inset-0 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200" onClick={() => setShowCreateModal(false)}></div>
          <div className="relative bg-white dark:bg-gray-900 rounded-2xl shadow-2xl w-full max-w-lg p-7 animate-in zoom-in-95 fade-in slide-in-from-bottom-4 duration-300">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-gradient-to-r from-violet-500 to-purple-500 rounded-xl flex items-center justify-center text-white text-lg shadow-lg shadow-violet-500/30">
                  📦
                </div>
                <h3 className="text-xl font-bold text-gray-900 dark:text-white">Create New Repository</h3>
              </div>
              <button 
                onClick={() => setShowCreateModal(false)}
                className="w-9 h-9 rounded-xl flex items-center justify-center hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 text-lg font-light"
              >×</button>
            </div>
            
            <div className="space-y-5">
              <div>
                <label className="block text-sm font-bold text-gray-800 dark:text-gray-200 mb-2.5">
                  Repository Name <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  value={newRepo.name}
                  onChange={(e) => setNewRepo({...newRepo, name: e.target.value})}
                  placeholder="my-awesome-skill"
                  className="w-full px-4 py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-xl focus:outline-none focus:ring-2 focus:ring-violet-500/40 focus:border-violet-400 text-gray-900 dark:text-gray-100 font-medium transition-all placeholder:text-gray-400 dark:placeholder:text-gray-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-bold text-gray-800 dark:text-gray-200 mb-2.5">Description</label>
                <textarea
                  value={newRepo.description}
                  onChange={(e) => setNewRepo({...newRepo, description: e.target.value})}
                  rows={3}
                  placeholder="Describe what this repository contains..."
                  className="w-full px-4 py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-xl focus:outline-none focus:ring-2 focus:ring-violet-500/40 focus:border-violet-400 text-gray-900 dark:text-gray-100 resize-none transition-all placeholder:text-gray-400 dark:placeholder:text-gray-500"
                />
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-bold text-gray-800 dark:text-gray-200 mb-2.5">Visibility</label>
                  <select
                    value={newRepo.visibility}
                    onChange={(e) => setNewRepo({...newRepo, visibility: e.target.value})}
                    className="w-full px-4 py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-xl focus:outline-none focus:ring-2 focus:ring-violet-500/40 text-gray-900 dark:text-gray-100 font-semibold cursor-pointer appearance-none"
                  >
                    <option value="public" className="text-gray-900">Public</option>
                    <option value="private" className="text-gray-900">Private</option>
                    <option value="internal" className="text-gray-900">Internal</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-bold text-gray-800 dark:text-gray-200 mb-2.5">Category</label>
                  <input
                    type="text"
                    value={newRepo.category}
                    onChange={(e) => setNewRepo({...newRepo, category: e.target.value})}
                    placeholder="e.g., Data Science"
                    className="w-full px-4 py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-xl focus:outline-none focus:ring-2 focus:ring-violet-500/40 text-gray-900 dark:text-gray-100 font-medium placeholder:text-gray-400 dark:placeholder:text-gray-500"
                  />
                </div>
              </div>
            </div>
            
            <div className="flex justify-end gap-3 mt-7 pt-5 border-t border-gray-200 dark:border-gray-700">
              <button 
                onClick={() => setShowCreateModal(false)}
                className="px-6 py-2.5 text-sm font-semibold text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-xl transition-colors border border-gray-300 dark:border-gray-600"
              >
                Cancel
              </button>
              <button 
                onClick={handleCreateRepository}
                disabled={!newRepo.name.trim() || creating}
                className="px-6 py-2.5 text-sm font-bold bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-xl transition-all shadow-lg shadow-violet-500/25 flex items-center gap-2"
              >
                {creating ? (
                  <>
                    <span className="animate-spin">⏳</span> Creating...
                  </>
                ) : (
                  <>
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8H4" />
                    </svg>
                    Create Repository
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default SkillsHub
