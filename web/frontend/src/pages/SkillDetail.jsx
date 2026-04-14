import React, { useState, useEffect } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'

const SkillDetail = () => {
  const { skillId } = useParams()
  const navigate = useNavigate()
  const [skill, setSkill] = useState(null)
  const [loading, setLoading] = useState(true)
  const [isStarred, setIsStarred] = useState(false)
  const [activeTab, setActiveTab] = useState('overview')
  const [copiedInstall, setCopiedInstall] = useState(false)
  const [selectedVersion, setSelectedVersion] = useState(null)

  useEffect(() => {
    fetchSkill()
    checkStarred()
  }, [skillId])

  const fetchSkill = async () => {
    try {
      const response = await fetch(`http://localhost:3003/api/skills/${skillId}`)
      if (!response.ok) {
        navigate('/skills-hub')
        return
      }
      const data = await response.json()
      setSkill(data)
      if (data.latest_version) {
        setSelectedVersion(data.latest_version.version)
      }
    } catch (error) {
      console.error('Error fetching skill:', error)
      navigate('/skills-hub')
    } finally {
      setLoading(false)
    }
  }

  const checkStarred = async () => {
    try {
      const response = await fetch(`http://localhost:3003/api/skills/${skillId}/starred`)
      const data = await response.json()
      setIsStarred(data.starred)
    } catch (error) {
      console.error('Error checking starred status:', error)
    }
  }

  const handleStar = async () => {
    try {
      const response = await fetch(`http://localhost:3003/api/skills/${skillId}/star`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: 'demo_user' })
      })
      const data = await response.json()
      setIsStarred(data.starred)
      fetchSkill()
    } catch (error) {
      console.error('Error toggling star:', error)
    }
  }

  const handleFork = async () => {
    try {
      const response = await fetch(`http://localhost:3003/api/skills/${skillId}/fork`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ new_namespace: 'demo', new_name: `${skill.name} (forked)` })
      })
      if (response.ok) {
        const data = await response.json()
        navigate(`/skills-hub/${data.skill_id}`)
      }
    } catch (error) {
      console.error('Error forking skill:', error)
    }
  }

  const handleDownload = async (version) => {
    try {
      const params = version ? `?version=${version}` : ''
      const response = await fetch(`http://localhost:3003/api/skills/${skillId}/download${params}`)
      const data = await response.json()
      
      const blob = new Blob([data.content], { type: 'text/markdown' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `${skill.name.replace(/\s+/g, '-')}-${data.version}.md`
      a.click()
      URL.revokeObjectURL(url)
      
      fetchSkill()
    } catch (error) {
      console.error('Error downloading skill:', error)
    }
  }

  const copyInstallCommand = () => {
    const command = `npx octopai install ${skill.namespace}/${skill.slug}`
    navigator.clipboard.writeText(command).then(() => {
      setCopiedInstall(true)
      setTimeout(() => setCopiedInstall(false), 2000)
    }).catch(err => {
      console.error('Failed to copy:', err)
    })
  }

  if (loading) {
    return (
      <div className="min-h-screen py-8">
        <div className="max-w-5xl mx-auto px-6">
          <div className="card p-8 animate-pulse">
            <div className="h-8 bg-gray-50 dark:bg-gray-800 rounded mb-4 w-1/2"></div>
            <div className="h-4 bg-gray-50 dark:bg-gray-800 rounded mb-6 w-full"></div>
            <div className="h-64 bg-gray-50 dark:bg-gray-800 rounded"></div>
          </div>
        </div>
      </div>
    )
  }

  if (!skill) {
    return (
      <div className="min-h-screen py-8">
        <div className="max-w-5xl mx-auto px-6">
          <div className="card p-12 text-center">
            <div className="text-6xl mb-4">😕</div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-2">
              Skill not found
            </h3>
            <Link to="/skills-hub" className="btn btn-primary">
              Back to Skills Hub
            </Link>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen py-8">
      <div className="max-w-5xl mx-auto px-6">
        <div className="mb-4">
          <Link
            to="/skills-hub"
            className="inline-flex items-center gap-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:text-gray-100 transition-colors"
          >
            ← Back to Skills Hub
          </Link>
        </div>

        <div className="card p-8 mb-6">
          <div className="flex items-start justify-between mb-6">
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-2 flex-wrap">
                <span className="text-gray-600 dark:text-gray-400 font-mono text-sm">
                  {skill.namespace}/
                </span>
                <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">
                  {skill.name}
                </h1>
                <span className={`px-2 py-1 rounded text-xs font-medium ${
                  skill.visibility === 'public' 
                    ? 'bg-green-500/10 text-green-500' 
                    : skill.visibility === 'private'
                    ? 'bg-yellow-500/10 text-yellow-500'
                    : 'bg-gray-500/10 text-gray-500'
                }`}>
                  {skill.visibility}
                </span>
                {skill.status && (
                  <span className={`px-2 py-1 rounded text-xs font-medium ${
                    skill.status === 'published' 
                      ? 'bg-blue-500/10 text-blue-500'
                      : skill.status === 'deprecated'
                      ? 'bg-red-500/10 text-red-500'
                      : 'bg-gray-500/10 text-gray-500'
                  }`}>
                    {skill.status}
                  </span>
                )}
              </div>
              <p className="text-lg text-gray-600 dark:text-gray-400 mb-4">
                {skill.description}
              </p>

              <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-4 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                <div className="text-center">
                  <div className="text-xl font-bold text-yellow-500">{skill.star_count}</div>
                  <div className="text-xs text-gray-500 dark:text-gray-400">Stars</div>
                </div>
                <div className="text-center">
                  <div className="text-xl font-bold text-blue-500">{skill.fork_count}</div>
                  <div className="text-xs text-gray-500 dark:text-gray-400">Forks</div>
                </div>
                <div className="text-center">
                  <div className="text-xl font-bold text-green-500">{skill.download_count}</div>
                  <div className="text-xs text-gray-500 dark:text-gray-400">Downloads</div>
                </div>
                <div className="text-center">
                  <div className="text-xl font-bold text-purple-500">{skill.view_count}</div>
                  <div className="text-xs text-gray-500 dark:text-gray-400">Views</div>
                </div>
                <div className="text-center">
                  <div className="text-xl font-bold text-octo-accent">
                    {skill.versions ? skill.versions.length : 0}
                  </div>
                  <div className="text-xs text-gray-500 dark:text-gray-400">Versions</div>
                </div>
              </div>

              {skill.categories && skill.categories.length > 0 && (
                <div className="flex flex-wrap gap-2 mb-3">
                  {skill.categories.map((category, idx) => (
                    <Link
                      key={idx}
                      to={`/skills-hub?category=${encodeURIComponent(category)}`}
                      className="px-3 py-1 bg-octo-accent/10 text-octo-accent rounded-full text-sm hover:bg-octo-accent/20 transition-colors"
                    >
                      📁 {category}
                    </Link>
                  ))}
                </div>
              )}

              {skill.tags && skill.tags.length > 0 && (
                <div className="flex flex-wrap gap-1">
                  {skill.tags.map((tag, idx) => (
                    <span
                      key={idx}
                      className="px-2 py-0.5 bg-gray-50 dark:bg-gray-800 rounded text-xs text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:text-gray-100 cursor-pointer"
                    >
                      #{tag}
                    </span>
                  ))}
                </div>
              )}
            </div>

            <div className="flex flex-col gap-2 ml-6 min-w-[140px]">
              <button
                onClick={handleStar}
                className={`px-4 py-2 rounded-lg transition-all flex items-center justify-center gap-2 ${
                  isStarred 
                    ? 'bg-octo-accent text-white shadow-lg shadow-octo-accent/25' 
                    : 'bg-gray-50 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:bg-gray-700 border border-gray-300 dark:border-gray-600'
                }`}
              >
                {isStarred ? '★ Starred' : '☆ Star'}
              </button>
              <button
                onClick={handleFork}
                className="px-4 py-2 rounded-lg bg-gray-50 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:bg-gray-700 transition-colors flex items-center justify-center gap-2 border border-gray-300 dark:border-gray-600"
              >
                🍴 Fork
              </button>
              <button
                onClick={() => handleDownload(selectedVersion)}
                className="px-4 py-2 rounded-lg btn btn-primary flex items-center justify-center gap-2"
              >
                ⬇️ Download
              </button>
            </div>
          </div>

          <div className="mt-6 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
            <div className="flex items-center justify-between mb-2">
              <label className="text-sm font-medium text-gray-900 dark:text-gray-100">
                Install Command
              </label>
              <button
                onClick={copyInstallCommand}
                className="px-3 py-1 text-xs bg-octo-accent text-white rounded hover:bg-octo-accent/90 transition-colors"
              >
                {copiedInstall ? '✓ Copied!' : '📋 Copy'}
              </button>
            </div>
            <code className="block p-3 bg-gray-100 dark:bg-gray-700 rounded font-mono text-sm text-gray-900 dark:text-gray-100 overflow-x-auto">
              npx octopai install {skill.namespace}/{skill.slug}
            </code>
          </div>
        </div>

        <div className="card">
          <div className="border-b border-gray-300 dark:border-gray-600 px-6">
            <div className="flex gap-6 overflow-x-auto">
              {[
                { id: 'overview', label: '📖 Overview', icon: '📖' },
                { id: 'versions', label: '📦 Versions', icon: '📦' },
                { id: 'metadata', label: '⚙️ Metadata', icon: '⚙️' },
                { id: 'content', label: '📄 Content', icon: '📄' },
                { id: 'stats', label: '📊 Statistics', icon: '📊' }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`py-4 px-2 border-b-2 transition-colors whitespace-nowrap ${
                    activeTab === tab.id
                      ? 'border-octo-accent text-octo-accent font-medium'
                      : 'border-transparent text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:text-gray-100'
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </div>
          </div>

          <div className="p-6">
            {activeTab === 'overview' && (
              <div className="space-y-6">
                {skill.latest_version && skill.latest_version.content && (
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-3">
                      About this Skill
                    </h3>
                    <div className="prose prose-invert max-w-none">
                      <pre className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg overflow-x-auto text-sm">
                        <code className="text-gray-900 dark:text-gray-100 whitespace-pre-wrap leading-relaxed">
                          {skill.latest_version.content}
                        </code>
                      </pre>
                    </div>
                  </div>
                )}

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                    <h4 className="font-semibold text-gray-900 dark:text-gray-100 mb-2">
                      Quick Info
                    </h4>
                    <dl className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <dt className="text-gray-500 dark:text-gray-400">Created</dt>
                        <dd className="text-gray-900 dark:text-gray-100">
                          {new Date(skill.created_at).toLocaleDateString()}
                        </dd>
                      </div>
                      <div className="flex justify-between">
                        <dt className="text-gray-500 dark:text-gray-400">Last Updated</dt>
                        <dd className="text-gray-900 dark:text-gray-100">
                          {new Date(skill.updated_at).toLocaleDateString()}
                        </dd>
                      </div>
                      <div className="flex justify-between">
                        <dt className="text-gray-500 dark:text-gray-400">Owner Type</dt>
                        <dd className="text-gray-900 dark:text-gray-100 capitalize">
                          {skill.owner_type}
                        </dd>
                      </div>
                      <div className="flex justify-between">
                        <dt className="text-gray-500 dark:text-gray-400">Latest Version</dt>
                        <dd className="text-gray-900 dark:text-gray-100">
                          v{skill.latest_version?.version || 'N/A'}
                        </dd>
                      </div>
                    </dl>
                  </div>

                  <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                    <h4 className="font-semibold text-gray-900 dark:text-gray-100 mb-2">
                      Links & Resources
                    </h4>
                    <div className="space-y-2">
                      {skill.metadata?.homepage && (
                        <a
                          href={skill.metadata.homepage}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center gap-2 text-octo-accent hover:underline text-sm"
                        >
                          🔗 Homepage
                        </a>
                      )}
                      {skill.metadata?.repository && (
                        <a
                          href={skill.metadata.repository}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center gap-2 text-octo-accent hover:underline text-sm"
                        >
                          📂 Repository
                        </a>
                      )}
                      {skill.metadata?.documentation && (
                        <a
                          href={skill.metadata.documentation}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center gap-2 text-octo-accent hover:underline text-sm"
                        >
                          📚 Documentation
                        </a>
                      )}
                      {!skill.metadata?.homepage && !skill.metadata?.repository && !skill.metadata?.documentation && (
                        <p className="text-gray-500 dark:text-gray-400 text-sm">
                          No external links available
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'versions' && (
              <div className="space-y-4">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                    Version History ({skill.versions ? skill.versions.length : 0} versions)
                  </h3>
                  <select
                    value={selectedVersion || ''}
                    onChange={(e) => setSelectedVersion(e.target.value)}
                    className="px-3 py-1 bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded text-sm text-gray-900 dark:text-gray-100"
                  >
                    {skill.versions && skill.versions.map((v) => (
                      <option key={v.version_id} value={v.version}>
                        v{v.version} {v.is_latest ? '(Latest)' : ''}
                      </option>
                    ))}
                  </select>
                </div>

                {skill.versions && skill.versions.length > 0 ? (
                  <div className="space-y-3">
                    {skill.versions
                      .slice()
                      .reverse()
                      .map((version, idx) => (
                        <div key={idx} className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg border-l-4 border-l-blue-500">
                          <div className="flex items-center justify-between mb-2">
                            <div className="flex items-center gap-3">
                              <span className="font-semibold text-gray-900 dark:text-gray-100 text-lg">
                                v{version.version}
                              </span>
                              {version.is_latest && (
                                <span className="px-2 py-0.5 bg-octo-accent text-white text-xs rounded font-medium">
                                  Latest
                                </span>
                              )}
                            </div>
                            <div className="flex items-center gap-3">
                              <span className="text-sm text-gray-500 dark:text-gray-400">
                                {new Date(version.created_at).toLocaleDateString()}
                              </span>
                              <button
                                onClick={() => handleDownload(version.version)}
                                className="px-3 py-1 text-xs bg-octo-accent text-white rounded hover:bg-octo-accent/90 transition-colors"
                              >
                                ⬇️ Download
                              </button>
                            </div>
                          </div>
                          {version.changelog && (
                            <div className="mb-2 p-2 bg-gray-100 dark:bg-gray-700 rounded text-sm text-gray-600 dark:text-gray-400">
                              <strong>Changelog:</strong> {version.changelog}
                            </div>
                          )}
                          <div className="flex items-center gap-4 text-sm text-gray-500 dark:text-gray-400">
                            <span>👤 Created by {version.created_by}</span>
                            <span>📥 {version.download_count} downloads</span>
                          </div>
                        </div>
                      ))
                    }
                  </div>
                ) : (
                  <div className="text-center py-8 text-gray-500 dark:text-gray-400">
                    No versions published yet
                  </div>
                )}
              </div>
            )}

            {activeTab === 'metadata' && skill.metadata && (
              <div className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                        Skill Name
                      </label>
                      <p className="text-gray-900 dark:text-gray-100 font-mono">{skill.metadata.name}</p>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                        Author
                      </label>
                      <p className="text-gray-900 dark:text-gray-100">{skill.metadata.author}</p>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                        Version
                      </label>
                      <p className="text-gray-900 dark:text-gray-100 font-mono">v{skill.metadata.version}</p>
                    </div>
                    {skill.metadata.category && (
                      <div>
                        <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                          Category
                        </label>
                        <p className="text-gray-900 dark:text-gray-100">{skill.metadata.category}</p>
                      </div>
                    )}
                    {skill.metadata.license && (
                      <div>
                        <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">
                          License
                        </label>
                        <p className="text-gray-900 dark:text-gray-100">{skill.metadata.license}</p>
                      </div>
                    )}
                  </div>

                  <div className="space-y-4">
                    {skill.metadata.keywords && skill.metadata.keywords.length > 0 && (
                      <div>
                        <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">
                          Keywords
                        </label>
                        <div className="flex flex-wrap gap-1">
                          {skill.metadata.keywords.map((keyword, idx) => (
                            <span
                              key={idx}
                              className="px-2 py-1 bg-octo-accent/10 text-octo-accent rounded text-xs"
                            >
                              {keyword}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {skill.metadata.requirements && skill.metadata.requirements.length > 0 && (
                      <div>
                        <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">
                          Requirements
                        </label>
                        <ul className="list-disc list-inside space-y-1 text-gray-900 dark:text-gray-100 text-sm">
                          {skill.metadata.requirements.map((req, idx) => (
                            <li key={idx}>{req}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {skill.metadata.compatibility && (
                      <div>
                        <label className="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">
                          Compatibility
                        </label>
                        <pre className="text-xs bg-gray-50 dark:bg-gray-800 p-2 rounded overflow-x-auto">
                          {JSON.stringify(skill.metadata.compatibility, null, 2)}
                        </pre>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'content' && skill.latest_version && (
              <div>
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                    Skill Content (v{selectedVersion || skill.latest_version.version})
                  </h3>
                  <button
                    onClick={() => handleDownload(selectedVersion)}
                    className="px-4 py-2 btn btn-primary text-sm"
                  >
                    ⬇️ Download this version
                  </button>
                </div>
                <div className="relative">
                  <pre className="bg-gray-50 dark:bg-gray-800 p-6 rounded-lg overflow-x-auto max-h-[600px] overflow-y-auto border border-gray-300 dark:border-gray-600">
                    <code className="text-gray-900 dark:text-gray-100 whitespace-pre-wrap text-sm leading-relaxed font-mono">
                      {skill.latest_version.content}
                    </code>
                  </pre>
                </div>
              </div>
            )}

            {activeTab === 'stats' && (
              <div className="space-y-6">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                  Skill Statistics & Analytics
                </h3>
                
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="p-4 bg-gradient-to-br from-yellow-500/10 to-yellow-600/5 rounded-lg border border-yellow-500/20">
                    <div className="text-3xl font-bold text-yellow-500">{skill.star_count}</div>
                    <div className="text-sm text-gray-500 dark:text-gray-400 mt-1">Total Stars</div>
                  </div>
                  <div className="p-4 bg-gradient-to-br from-blue-500/10 to-blue-600/5 rounded-lg border border-blue-500/20">
                    <div className="text-3xl font-bold text-blue-500">{skill.fork_count}</div>
                    <div className="text-sm text-gray-500 dark:text-gray-400 mt-1">Total Forks</div>
                  </div>
                  <div className="p-4 bg-gradient-to-br from-green-500/10 to-green-600/5 rounded-lg border border-green-500/20">
                    <div className="text-3xl font-bold text-green-500">{skill.download_count}</div>
                    <div className="text-sm text-gray-500 dark:text-gray-400 mt-1">Total Downloads</div>
                  </div>
                  <div className="p-4 bg-gradient-to-br from-purple-500/10 to-purple-600/5 rounded-lg border border-purple-500/20">
                    <div className="text-3xl font-bold text-purple-500">{skill.view_count}</div>
                    <div className="text-sm text-gray-500 dark:text-gray-400 mt-1">Total Views</div>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                    <h4 className="font-semibold text-gray-900 dark:text-gray-100 mb-3">
                      Engagement Metrics
                    </h4>
                    <div className="space-y-3">
                      <div>
                        <div className="flex justify-between text-sm mb-1">
                          <span className="text-gray-500 dark:text-gray-400">Star Rate</span>
                          <span className="text-gray-900 dark:text-gray-100">
                            {skill.view_count > 0 ? ((skill.star_count / skill.view_count) * 100).toFixed(1) : 0}%
                          </span>
                        </div>
                        <div className="w-full h-2 bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden">
                          <div 
                            className="h-full bg-yellow-500 rounded-full transition-all"
                            style={{ width: `${Math.min(100, (skill.star_count / Math.max(1, skill.view_count)) * 100)}%` }}
                          ></div>
                        </div>
                      </div>
                      <div>
                        <div className="flex justify-between text-sm mb-1">
                          <span className="text-gray-500 dark:text-gray-400">Download Rate</span>
                          <span className="text-gray-900 dark:text-gray-100">
                            {skill.view_count > 0 ? ((skill.download_count / skill.view_count) * 100).toFixed(1) : 0}%
                          </span>
                        </div>
                        <div className="w-full h-2 bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden">
                          <div 
                            className="h-full bg-green-500 rounded-full transition-all"
                            style={{ width: `${Math.min(100, (skill.download_count / Math.max(1, skill.view_count)) * 100)}%` }}
                          ></div>
                        </div>
                      </div>
                      <div>
                        <div className="flex justify-between text-sm mb-1">
                          <span className="text-gray-500 dark:text-gray-400">Fork Rate</span>
                          <span className="text-gray-900 dark:text-gray-100">
                            {skill.view_count > 0 ? ((skill.fork_count / skill.view_count) * 100).toFixed(1) : 0}%
                          </span>
                        </div>
                        <div className="w-full h-2 bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden">
                          <div 
                            className="h-full bg-blue-500 rounded-full transition-all"
                            style={{ width: `${Math.min(100, (skill.fork_count / Math.max(1, skill.view_count)) * 100)}%` }}
                          ></div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                    <h4 className="font-semibold text-gray-900 dark:text-gray-100 mb-3">
                      Version Activity
                    </h4>
                    {skill.versions && skill.versions.length > 0 ? (
                      <div className="space-y-2">
                        {skill.versions.slice(-5).reverse().map((v, idx) => (
                          <div key={idx} className="flex items-center justify-between text-sm">
                            <span className="font-mono text-gray-900 dark:text-gray-100">v{v.version}</span>
                            <div className="flex items-center gap-3 text-gray-500 dark:text-gray-400">
                              <span>📥 {v.download_count}</span>
                              <span>{new Date(v.created_at).toLocaleDateString()}</span>
                            </div>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <p className="text-gray-500 dark:text-gray-400 text-sm">
                        No version activity yet
                      </p>
                    )}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default SkillDetail
