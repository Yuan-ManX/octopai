import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

const Research = () => {
  const [projects, setProjects] = useState([])
  const [domains, setDomains] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  
  // Filter states
  const [selectedDomain, setSelectedDomain] = useState('')
  const [selectedStatus, setSelectedStatus] = useState('')
  const [searchQuery, setSearchQuery] = useState('')
  const [sortBy, setSortBy] = useState('updated_at')
  
  // Modal states
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [showLiteratureModal, setShowLiteratureModal] = useState(false)
  const [selectedProject, setSelectedProject] = useState(null)
  const [literatureResults, setLiteratureResults] = useState(null)
  const [literatureQuery, setLiteratureQuery] = useState('')
  
  // Form state
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    domain: '',
    visibility: 'private',
    topic: '',
    keywords: []
  })

  useEffect(() => {
    fetchProjects()
    fetchDomains()
    fetchStats()
  }, [])

  useEffect(() => {
    fetchProjects()
  }, [selectedDomain, selectedStatus])

  const fetchProjects = async () => {
    setLoading(true)
    try {
      const params = new URLSearchParams({
        page: '1',
        page_size: '20',
        sort_by: sortBy
      })
      if (selectedDomain) params.append('domain', selectedDomain)
      if (selectedStatus) params.append('status', selectedStatus)
      
      const response = await fetch(`http://localhost:3004/api/research/projects?${params}`)
      const data = await response.json()
      setProjects(data.projects || [])
    } catch (error) {
      console.error('Error fetching projects:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchDomains = async () => {
    try {
      const response = await fetch('http://localhost:3004/api/research/domains')
      const data = await response.json()
      setDomains(data.domains || [])
    } catch (error) {
      console.error('Error fetching domains:', error)
    }
  }

  const fetchStats = async () => {
    try {
      const response = await fetch('http://localhost:3004/api/research/stats')
      const data = await response.json()
      setStats(data)
    } catch (error) {
      console.error('Error fetching stats:', error)
    }
  }

  const handleCreateProject = async () => {
    if (!formData.name.trim()) return
    
    try {
      const response = await fetch('http://localhost:3004/api/research/projects', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...formData,
          namespace: 'demo'
        })
      })
      
      if (response.ok) {
        setShowCreateModal(false)
        setFormData({ name: '', description: '', domain: '', visibility: 'private', topic: '', keywords: [] })
        fetchProjects()
        fetchStats()
      }
    } catch (error) {
      console.error('Error creating project:', error)
    }
  }

  const handleSearchLiterature = async () => {
    if (!literatureQuery.trim()) return
    
    try {
      const response = await fetch('http://localhost:3004/api/research/literature/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: literatureQuery,
          max_results: 10
        })
      })
      
      const data = await response.json()
      setLiteratureResults(data.search)
    } catch (error) {
      console.error('Error searching literature:', error)
    }
  }

  const getStatusColor = (status) => {
    const colors = {
      ideation: 'bg-purple-500/10 text-purple-500 border-purple-500/20',
      planning: 'bg-blue-500/10 text-blue-500 border-blue-500/20',
      experimenting: 'bg-yellow-500/10 text-yellow-500 border-yellow-500/20',
      analyzing: 'bg-orange-500/10 text-orange-500 border-orange-500/20',
      writing: 'bg-green-500/10 text-green-500 border-green-500/20',
      review: 'bg-cyan-500/10 text-cyan-500 border-cyan-500/20',
      completed: 'bg-emerald-500/10 text-emerald-500 border-emerald-500/20',
      archived: 'bg-gray-500/10 text-gray-400 border-gray-500/20'
    }
    return colors[status] || colors.ideation
  }

  const getStatusIcon = (status) => {
    const icons = {
      ideation: '💡',
      planning: '📋',
      experimenting: '🔬',
      analyzing: '📊',
      writing: '✍️',
      review: '👀',
      completed: '✅',
      archived: '📦'
    }
    return icons[status] || '💡'
  }

  return (
    <div className="min-h-screen py-8">
      <div className="max-w-7xl mx-auto px-6">
        {/* Header */}
        <div className="mb-12">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-6 group">
              <div className="w-20 h-20 bg-gradient-to-br from-emerald-500 via-teal-500 to-cyan-600 rounded-3xl flex items-center justify-center text-white text-4xl shadow-2xl shadow-emerald-500/40 animate-pulse-subtle ring-4 ring-emerald-500/20 relative overflow-hidden shrink-0 transform hover:scale-105 hover:shadow-3xl transition-all duration-300">
                <span className="relative z-10 drop-shadow-lg">🔬</span>
                <div className="absolute inset-0 bg-gradient-to-br from-white/20 via-white/10 to-transparent animate-pulse"></div>
                <div className="absolute -inset-1 bg-gradient-to-br from-emerald-400/30 to-cyan-400/30 rounded-3xl blur-xl opacity-60 group-hover:opacity-100 transition-opacity"></div>
              </div>
              <div className="min-w-0 flex-1">
                <h1 className="text-5xl font-black bg-gradient-to-r from-blue-600 via-cyan-500 to-blue-700 dark:from-blue-400 dark:via-cyan-300 dark:to-blue-400 bg-clip-text text-transparent mb-3 tracking-wide drop-shadow-xl filter leading-snug">
                  AutoResearch Workbench
                </h1>
                <p className="text-gray-700 dark:text-gray-300 text-base leading-relaxed font-medium max-w-2xl opacity-90">
                  Autonomous Scientific Discovery & Experimentation Platform — AI agents conduct research, run experiments, and evolve approaches autonomously
                </p>
              </div>
            </div>
            <div className="flex gap-3 shrink-0">
              <button
                onClick={() => setShowLiteratureModal(true)}
                className="px-5 py-2.5 bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-xl transition-all duration-200 text-sm font-bold text-gray-700 dark:text-gray-300 flex items-center gap-2"
              >
                📚 Search Literature
              </button>
              <button
                onClick={() => setShowCreateModal(true)}
                className="px-5 py-2.5 bg-gradient-to-r from-emerald-600 via-teal-600 to-cyan-600 hover:from-emerald-700 hover:to-cyan-700 text-white rounded-xl font-bold transition-all duration-200 shadow-lg shadow-emerald-500/25 hover:shadow-xl flex items-center gap-2"
              >
                + New Research Project
              </button>
            </div>
          </div>
        </div>

        {/* Statistics Dashboard */}
        {stats && (
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
              <div className="card p-4 text-center">
                <div className="text-2xl font-bold text-violet-600 dark:text-violet-400">{stats.total_projects}</div>
                <div className="text-sm text-gray-600 dark:text-gray-400">Total Projects</div>
              </div>
              <div className="card p-4 text-center">
                <div className="text-2xl font-bold text-green-500">{stats.successful_experiments}</div>
                <div className="text-sm text-gray-600 dark:text-gray-400">Experiments</div>
              </div>
              <div className="card p-4 text-center">
                <div className="text-2xl font-bold text-blue-500">{stats.success_rate * 100}%</div>
                <div className="text-sm text-gray-600 dark:text-gray-400">Success Rate</div>
              </div>
              <div className="card p-4 text-center">
                <div className="text-2xl font-bold text-purple-500">{stats.public_projects}</div>
                <div className="text-sm text-gray-600 dark:text-gray-400">Public Projects</div>
              </div>
              <div className="card p-4 text-center">
                <div className="text-2xl font-bold text-yellow-500">
                  {Object.keys(stats.domains).length}
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-400">Domains</div>
              </div>
            </div>
          )}

          {/* Filters */}
          <div className="card p-4 mb-6">
            <div className="flex flex-col md:flex-row gap-4">
              <div className="flex-1">
                <input
                  type="text"
                  placeholder="Search research projects..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full px-4 py-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-violet-500/50 text-gray-900 dark:text-gray-100"
                />
              </div>

              <select
                value={selectedDomain}
                onChange={(e) => setSelectedDomain(e.target.value)}
                className="px-4 py-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-violet-500/50 text-gray-900 dark:text-gray-100"
              >
                <option value="">All Domains</option>
                {domains.map((domain) => (
                  <option key={domain} value={domain}>{domain}</option>
                ))}
              </select>

              <select
                value={selectedStatus}
                onChange={(e) => setSelectedStatus(e.target.value)}
                className="px-4 py-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-violet-500/50 text-gray-900 dark:text-gray-100"
              >
                <option value="">All Statuses</option>
                <option value="ideation">💡 Ideation</option>
                <option value="planning">📋 Planning</option>
                <option value="experimenting">🔬 Experimenting</option>
                <option value="analyzing">📊 Analyzing</option>
                <option value="writing">✍️ Writing</option>
                <option value="review">👀 Review</option>
                <option value="completed">✅ Completed</option>
              </select>
            </div>
          </div>
        </div>

        {/* Research Projects Grid */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">
            Research Projects ({projects.length})
          </h2>

          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[...Array(6)].map((_, idx) => (
                <div key={idx} className="card p-6 animate-pulse">
                  <div className="h-6 bg-white dark:bg-gray-800 rounded mb-3 w-3/4"></div>
                  <div className="h-4 bg-white dark:bg-gray-800 rounded mb-2 w-full"></div>
                  <div className="h-4 bg-white dark:bg-gray-800 rounded mb-4 w-2/3"></div>
                  <div className="flex gap-2">
                    <div className="h-6 bg-white dark:bg-gray-800 rounded w-16"></div>
                    <div className="h-6 bg-white dark:bg-gray-800 rounded w-24"></div>
                  </div>
                </div>
              ))}
            </div>
          ) : projects.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {projects.map((project) => (
                <Link
                  key={project.project_id}
                  to={`/research/${project.project_id}`}
                  className="block group"
                >
                  <div className="card p-6 transition-all duration-200 hover:shadow-xl hover:-translate-y-1 hover:border-blue-500/30">
                    {/* Project Header */}
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-2 flex-wrap">
                          <span className={`px-2 py-0.5 rounded text-xs font-medium border ${getStatusColor(project.status)}`}>
                            {getStatusIcon(project.status)} {project.status}
                          </span>
                          <span className={`px-2 py-0.5 rounded text-xs font-medium ${
                            project.visibility === 'public' 
                              ? 'bg-green-500/10 text-green-500' 
                              : 'bg-yellow-500/10 text-yellow-500'
                          }`}>
                            {project.visibility}
                          </span>
                        </div>
                        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 truncate group-hover:text-violet-600 dark:text-violet-400 transition-colors">
                          {project.name}
                        </h3>
                      </div>
                    </div>

                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-4 line-clamp-2 leading-relaxed">
                      {project.description}
                    </p>

                    {/* Domain and Keywords */}
                    {project.domain && (
                      <div className="mb-3">
                        <span className="inline-flex items-center px-2 py-1 bg-blue-500/10 text-violet-600 dark:text-violet-400 rounded-full text-xs">
                          🎯 {project.domain}
                        </span>
                        {project.subdomain && (
                          <span className="inline-flex items-center px-2 py-1 bg-blue-500/10 text-blue-400 rounded-full text-xs ml-1">
                            → {project.subdomain}
                          </span>
                        )}
                      </div>
                    )}

                    {project.keywords && project.keywords.length > 0 && (
                      <div className="flex flex-wrap gap-1 mb-4">
                        {project.keywords.slice(0, 4).map((keyword, idx) => (
                          <span 
                            key={idx}
                            className="px-1.5 py-0.5 bg-gray-100 dark:bg-gray-700 rounded text-xs text-gray-500 dark:text-gray-400"
                          >
                            #{keyword}
                          </span>
                        ))}
                      </div>
                    )}

                    {/* Stats Footer */}
                    <div className="pt-3 border-t border-gray-300 dark:border-gray-600 flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
                      <div className="flex items-center gap-3">
                        <span>🧪 {project.total_experiments} experiments</span>
                        <span>✅ {project.successful_experiments} successful</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <span>⭐ {project.star_count}</span>
                        <span>👁️ {project.view_count}</span>
                      </div>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          ) : (
            <div className="card p-12 text-center">
              <div className="text-6xl mb-4">🔬</div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-2">
                No Research Projects Yet
              </h3>
              <p className="text-gray-600 dark:text-gray-400 mb-6">
                Start your autonomous scientific discovery journey by creating a new project
              </p>
              <button
                onClick={() => setShowCreateModal(true)}
                className="btn btn-primary"
              >
                + Create Your First Research Project
              </button>
            </div>
          )}
        </div>

        {/* Create Project Modal */}
        {showCreateModal && (
          <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4" onClick={() => setShowCreateModal(false)}>
            <div className="bg-white dark:bg-gray-900 rounded-xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6" onClick={(e) => e.stopPropagation()}>
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                  🚀 Create New Research Project
                </h2>
                <button
                  onClick={() => setShowCreateModal(false)}
                  className="text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:text-gray-100 text-2xl"
                >
                  ×
                </button>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-900 dark:text-gray-100 mb-2">
                    Project Name *
                  </label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                    placeholder="Enter research project title"
                    className="w-full px-4 py-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-violet-500/50 text-gray-900 dark:text-gray-100"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-900 dark:text-gray-100 mb-2">
                    Description *
                  </label>
                  <textarea
                    value={formData.description}
                    onChange={(e) => setFormData({...formData, description: e.target.value})}
                    rows={3}
                    placeholder="Describe your research goals and objectives"
                    className="w-full px-4 py-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-violet-500/50 text-gray-900 dark:text-gray-100"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-900 dark:text-gray-100 mb-2">
                      Domain *
                    </label>
                    <select
                      value={formData.domain}
                      onChange={(e) => setFormData({...formData, domain: e.target.value})}
                      className="w-full px-4 py-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-violet-500/50 text-gray-900 dark:text-gray-100"
                    >
                      <option value="">Select Domain</option>
                      <option value="Machine Learning">Machine Learning</option>
                      <option value="Natural Language Processing">Natural Language Processing</option>
                      <option value="Computer Vision">Computer Vision</option>
                      <option value="Quantum Computing">Quantum Computing</option>
                      <option value="Robotics">Robotics</option>
                      <option value="Bioinformatics">Bioinformatics</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-900 dark:text-gray-100 mb-2">
                      Visibility
                    </label>
                    <select
                      value={formData.visibility}
                      onChange={(e) => setFormData({...formData, visibility: e.target.value})}
                      className="w-full px-4 py-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-violet-500/50 text-gray-900 dark:text-gray-100"
                    >
                      <option value="private">Private</option>
                      <option value="public">Public</option>
                      <option value="collaborative">Collaborative</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-900 dark:text-gray-100 mb-2">
                    Research Topic / Hypothesis
                  </label>
                  <input
                    type="text"
                    value={formData.topic}
                    onChange={(e) => setFormData({...formData, topic: e.target.value})}
                    placeholder="What scientific question are you investigating?"
                    className="w-full px-4 py-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-violet-500/50 text-gray-900 dark:text-gray-100"
                  />
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
                  onClick={handleCreateProject}
                  disabled={!formData.name || !formData.description}
                  className="btn btn-primary"
                >
                  Create Project
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Literature Search Modal */}
        {showLiteratureModal && (
          <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4" onClick={() => setShowLiteratureModal(false)}>
            <div className="bg-white dark:bg-gray-900 rounded-xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto p-6" onClick={(e) => e.stopPropagation()}>
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                  📚 Academic Literature Search
                </h2>
                <button
                  onClick={() => setShowLiteratureModal(false)}
                  className="text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:text-gray-100 text-2xl"
                >
                  ×
                </button>
              </div>

              <div className="mb-6">
                <div className="flex gap-3">
                  <input
                    type="text"
                    value={literatureQuery}
                    onChange={(e) => setLiteratureQuery(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSearchLiterature()}
                    placeholder="Search for papers, topics, or authors..."
                    className="flex-1 px-4 py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-violet-500/50 text-gray-900 dark:text-gray-100"
                  />
                  <button
                    onClick={handleSearchLiterature}
                    disabled={!literatureQuery.trim()}
                    className="btn btn-primary"
                  >
                    🔍 Search
                  </button>
                </div>
              </div>

              {literatureResults && (
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">
                    Found {literatureResults.total_found} papers for "{literatureResults.query}"
                  </h3>
                  
                  <div className="space-y-4">
                    {literatureResults.results.map((paper, idx) => (
                      <div key={idx} className="card p-5 border-l-4 border-l-octo-accent">
                        <div className="flex items-start justify-between mb-2">
                          <h4 className="text-base font-semibold text-gray-900 dark:text-gray-100 flex-1 mr-4">
                            {paper.title}
                          </h4>
                          <span className={`px-2 py-1 rounded text-xs font-medium ${
                            paper.relevance_score > 0.8 
                              ? 'bg-green-500/10 text-green-500' 
                              : paper.relevance_score > 0.6
                              ? 'bg-yellow-500/10 text-yellow-500'
                              : 'bg-gray-500/10 text-gray-400'
                          }`}>
                            {(paper.relevance_score * 100).toFixed(0)}% relevant
                          </span>
                        </div>
                        
                        <p className="text-sm text-gray-600 dark:text-gray-400 mb-3 line-clamp-2">
                          {paper.abstract}
                        </p>
                        
                        <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
                          <div className="flex items-center gap-4">
                            <span>{paper.authors?.join(', ')}</span>
                            <span>{paper.year}</span>
                            <span>{paper.venue}</span>
                          </div>
                          <div className="flex items-center gap-3">
                            <span>📄 {paper.citation_count} citations</span>
                            {paper.doi && (
                              <a href={`https://doi.org/${paper.doi}`} target="_blank" rel="noopener noreferrer" className="text-violet-600 dark:text-violet-400 hover:underline">
                                View DOI
                              </a>
                            )}
                          </div>
                        </div>

                        {paper.key_findings && paper.key_findings.length > 0 && (
                          <div className="mt-3 pt-3 border-t border-gray-300 dark:border-gray-600">
                            <div className="text-xs font-medium text-gray-900 dark:text-gray-100 mb-2">Key Findings:</div>
                            <ul className="list-disc list-inside space-y-1">
                              {paper.key_findings.slice(0, 3).map((finding, fIdx) => (
                                <li key={fIdx} className="text-xs text-gray-600 dark:text-gray-400">{finding}</li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    )
}

export default Research
