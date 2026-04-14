import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import SkillCard from '../components/SkillCard'

const SkillsHub = () => {
  const [skills, setSkills] = useState([])
  const [categories, setCategories] = useState([])
  const [tags, setTags] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('')
  const [selectedTags, setSelectedTags] = useState([])
  const [sortBy, setSortBy] = useState('updated_at')
  const [sortOrder, setSortOrder] = useState('desc')
  const [page, setPage] = useState(1)
  const [total, setTotal] = useState(0)
  const [hasNext, setHasNext] = useState(false)

  const [trendingSkills, setTrendingSkills] = useState([])
  const [recentSkills, setRecentSkills] = useState([])
  const [recommendedSkills, setRecommendedSkills] = useState([])
  const [popularSkills, setPopularSkills] = useState([])
  const [stats, setStats] = useState(null)

  const [activeTab, setActiveTab] = useState('all')

  useEffect(() => {
    fetchCategories()
    fetchTags()
    fetchStats()
    fetchTrendingSkills()
    fetchRecentSkills()
    fetchRecommendedSkills()
    fetchPopularSkills()
    fetchSkills()
  }, [page, sortBy, sortOrder, selectedCategory])

  useEffect(() => {
    if (searchQuery || selectedTags.length > 0) {
      searchSkills()
    } else {
      fetchSkills()
    }
  }, [searchQuery, selectedTags])

  const fetchStats = async () => {
    try {
      const response = await fetch('http://localhost:3003/api/stats/overview')
      const data = await response.json()
      setStats(data)
    } catch (error) {
      console.error('Error fetching stats:', error)
    }
  }

  const fetchTrendingSkills = async () => {
    try {
      const response = await fetch('http://localhost:3003/api/skills/trending?limit=6')
      const data = await response.json()
      setTrendingSkills(data.skills)
    } catch (error) {
      console.error('Error fetching trending skills:', error)
    }
  }

  const fetchRecentSkills = async () => {
    try {
      const response = await fetch('http://localhost:3003/api/skills/recent?limit=8')
      const data = await response.json()
      setRecentSkills(data.skills)
    } catch (error) {
      console.error('Error fetching recent skills:', error)
    }
  }

  const fetchRecommendedSkills = async () => {
    try {
      const response = await fetch('http://localhost:3003/api/skills/recommended?limit=6')
      const data = await response.json()
      setRecommendedSkills(data.skills)
    } catch (error) {
      console.error('Error fetching recommended skills:', error)
    }
  }

  const fetchPopularSkills = async () => {
    try {
      const response = await fetch('http://localhost:3003/api/skills/popular?limit=10')
      const data = await response.json()
      setPopularSkills(data.skills)
    } catch (error) {
      console.error('Error fetching popular skills:', error)
    }
  }

  const fetchCategories = async () => {
    try {
      const response = await fetch('http://localhost:3003/api/categories')
      const data = await response.json()
      setCategories(data.categories)
    } catch (error) {
      console.error('Error fetching categories:', error)
    }
  }

  const fetchTags = async () => {
    try {
      const response = await fetch('http://localhost:3003/api/tags')
      const data = await response.json()
      setTags(data.tags)
    } catch (error) {
      console.error('Error fetching tags:', error)
    }
  }

  const fetchSkills = async () => {
    setLoading(true)
    try {
      const params = new URLSearchParams({
        page,
        page_size: 12,
        sort_by: sortBy,
        sort_order: sortOrder
      })
      if (selectedCategory) {
        params.append('category', selectedCategory)
      }
      
      const response = await fetch(`http://localhost:3003/api/skills?${params}`)
      const data = await response.json()
      setSkills(data.skills)
      setTotal(data.total)
      setHasNext(data.has_next)
    } catch (error) {
      console.error('Error fetching skills:', error)
    } finally {
      setLoading(false)
    }
  }

  const searchSkills = async () => {
    setLoading(true)
    try {
      const response = await fetch('http://localhost:3003/api/skills/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: searchQuery,
          category: selectedCategory || undefined,
          tags: selectedTags.length > 0 ? selectedTags : undefined,
          sort_by: sortBy,
          sort_order: sortOrder,
          page,
          page_size: 12
        })
      })
      const data = await response.json()
      setSkills(data.skills)
      setTotal(data.total)
      setHasNext(data.has_next)
    } catch (error) {
      console.error('Error searching skills:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleRefresh = () => {
    fetchSkills()
    fetchTrendingSkills()
    fetchRecentSkills()
    fetchRecommendedSkills()
    fetchPopularSkills()
    fetchStats()
  }

  const handleTagToggle = (tag) => {
    setSelectedTags(prev => 
      prev.includes(tag) 
        ? prev.filter(t => t !== tag)
        : [...prev, tag]
    )
    setPage(1)
  }

  return (
    <div className="min-h-screen py-8">
      <div className="max-w-7xl mx-auto px-6">
        <div className="mb-10">
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 bg-gradient-to-br from-violet-500 via-purple-600 to-fuchsia-600 rounded-2xl flex items-center justify-center text-white text-3xl shadow-2xl shadow-purple-500/40 animate-pulse-subtle ring-4 ring-purple-500/20 relative overflow-hidden">
                <span className="relative z-10">📦</span>
                <div className="absolute inset-0 bg-white/10 animate-pulse"></div>
              </div>
              <div>
                <h1 className="text-5xl font-black bg-gradient-to-r from-blue-600 via-cyan-500 to-blue-700 dark:from-blue-400 dark:via-cyan-300 dark:to-blue-400 bg-clip-text text-transparent mb-3 tracking-wide drop-shadow-xl filter">
                  Skills Hub
                </h1>
                <p className="text-gray-700 dark:text-gray-300 text-base font-medium leading-relaxed max-w-xl">
                  Discover, share, and manage AI agent skills
                </p>
              </div>
            </div>
            <Link
              to="/skills-hub/create"
              className="btn btn-primary"
            >
              + Publish Skill
            </Link>
          </div>

          {stats && (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              <div className="card p-4 text-center">
                <div className="text-2xl font-bold text-octo-accent">{stats.total_skills}</div>
                <div className="text-sm text-gray-600 dark:text-gray-400">Total Skills</div>
              </div>
              <div className="card p-4 text-center">
                <div className="text-2xl font-bold text-green-500">{stats.public_skills}</div>
                <div className="text-sm text-gray-600 dark:text-gray-400">Public Skills</div>
              </div>
              <div className="card p-4 text-center">
                <div className="text-2xl font-bold text-blue-500">{stats.total_downloads.toLocaleString()}</div>
                <div className="text-sm text-gray-600 dark:text-gray-400">Downloads</div>
              </div>
              <div className="card p-4 text-center">
                <div className="text-2xl font-bold text-yellow-500">{stats.total_stars.toLocaleString()}</div>
                <div className="text-sm text-gray-600 dark:text-gray-400">Stars</div>
              </div>
            </div>
          )}

          <div className="card p-4 mb-6">
            <div className="flex flex-col md:flex-row gap-4">
              <div className="flex-1">
                <div className="relative">
                  <input
                    type="text"
                    placeholder="Search skills..."
                    value={searchQuery}
                    onChange={(e) => {
                      setSearchQuery(e.target.value)
                      setPage(1)
                    }}
                    className="w-full px-4 py-2 bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/50 text-gray-900 dark:text-gray-100"
                  />
                  <span className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 dark:text-gray-400">
                    🔍
                  </span>
                </div>
              </div>

              <select
                value={selectedCategory}
                onChange={(e) => {
                  setSelectedCategory(e.target.value)
                  setPage(1)
                }}
                className="px-4 py-2 bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/50 text-gray-900 dark:text-gray-100"
              >
                <option value="">All Categories</option>
                {categories.map((category) => (
                  <option key={category} value={category}>
                    {category}
                  </option>
                ))}
              </select>

              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="px-4 py-2 bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/50 text-gray-900 dark:text-gray-100"
              >
                <option value="updated_at">Recently Updated</option>
                <option value="created_at">Newest</option>
                <option value="download_count">Most Downloaded</option>
                <option value="star_count">Most Stars</option>
              </select>

              <button
                onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
                className="px-4 py-2 bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-100 dark:bg-gray-700 transition-colors text-gray-900 dark:text-gray-100"
              >
                {sortOrder === 'asc' ? '↑' : '↓'}
              </button>
            </div>

            {tags.length > 0 && (
              <div className="mt-4 flex flex-wrap gap-2">
                {tags.slice(0, 15).map((tag) => (
                  <button
                    key={tag}
                    onClick={() => handleTagToggle(tag)}
                    className={`px-3 py-1 rounded-full text-sm transition-colors ${
                      selectedTags.includes(tag)
                        ? 'bg-octo-accent text-white'
                        : 'bg-gray-50 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:bg-gray-700'
                    }`}
                  >
                    #{tag}
                  </button>
                ))}
                {tags.length > 15 && (
                  <span className="px-3 py-1 text-sm text-gray-500 dark:text-gray-400">
                    +{tags.length - 15} more
                  </span>
                )}
              </div>
            )}
          </div>
        </div>

        <div className="mb-8">
          <div className="flex gap-4 border-b border-gray-300 dark:border-gray-600 mb-6">
            <button
              onClick={() => setActiveTab('all')}
              className={`pb-3 px-4 transition-colors ${
                activeTab === 'all'
                  ? 'border-b-2 border-octo-accent text-octo-accent font-medium'
                  : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:text-gray-100'
              }`}
            >
              All Skills
            </button>
            <button
              onClick={() => setActiveTab('trending')}
              className={`pb-3 px-4 transition-colors ${
                activeTab === 'trending'
                  ? 'border-b-2 border-octo-accent text-octo-accent font-medium'
                  : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:text-gray-100'
              }`}
            >
              🔥 Trending
            </button>
            <button
              onClick={() => setActiveTab('recent')}
              className={`pb-3 px-4 transition-colors ${
                activeTab === 'recent'
                  ? 'border-b-2 border-octo-accent text-octo-accent font-medium'
                  : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:text-gray-100'
              }`}
            >
              ✨ New
            </button>
            <button
              onClick={() => setActiveTab('recommended')}
              className={`pb-3 px-4 transition-colors ${
                activeTab === 'recommended'
                  ? 'border-b-2 border-octo-accent text-octo-accent font-medium'
                  : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:text-gray-100'
              }`}
            >
              ⭐ Recommended
            </button>
            <button
              onClick={() => setActiveTab('popular')}
              className={`pb-3 px-4 transition-colors ${
                activeTab === 'popular'
                  ? 'border-b-2 border-octo-accent text-octo-accent font-medium'
                  : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:text-gray-100'
              }`}
            >
              📥 Popular
            </button>
          </div>

          {activeTab !== 'all' && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
              {(activeTab === 'trending' ? trendingSkills :
                activeTab === 'recent' ? recentSkills :
                activeTab === 'recommended' ? recommendedSkills :
                popularSkills).map((skill) => (
                <SkillCard
                  key={skill.skill_id}
                  skill={skill}
                  onStar={handleRefresh}
                  onFork={handleRefresh}
                />
              ))}
            </div>
          )}

          {activeTab === 'all' && (
            <>
              <div className="mb-4 flex items-center justify-between">
                <p className="text-gray-600 dark:text-gray-400">
                  {loading ? 'Loading...' : `${total} skills found`}
                </p>
              </div>

              {loading ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {[...Array(6)].map((_, idx) => (
                    <div key={idx} className="card p-6 animate-pulse">
                      <div className="h-6 bg-gray-50 dark:bg-gray-800 rounded mb-3 w-3/4"></div>
                      <div className="h-4 bg-gray-50 dark:bg-gray-800 rounded mb-2 w-full"></div>
                      <div className="h-4 bg-gray-50 dark:bg-gray-800 rounded mb-4 w-2/3"></div>
                      <div className="flex gap-2 mb-4">
                        <div className="h-6 bg-gray-50 dark:bg-gray-800 rounded w-16"></div>
                        <div className="h-6 bg-gray-50 dark:bg-gray-800 rounded w-20"></div>
                      </div>
                      <div className="h-10 bg-gray-50 dark:bg-gray-800 rounded"></div>
                    </div>
                  ))}
                </div>
              ) : skills.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {skills.map((skill) => (
                    <SkillCard
                      key={skill.skill_id}
                      skill={skill}
                      onStar={handleRefresh}
                      onFork={handleRefresh}
                    />
                  ))}
                </div>
              ) : (
                <div className="card p-12 text-center">
                  <div className="text-6xl mb-4">🔍</div>
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-2">
                    No skills found
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400 mb-6">
                    Try adjusting your search or filters
                  </p>
                  <button
                    onClick={() => {
                      setSearchQuery('')
                      setSelectedCategory('')
                      setSelectedTags([])
                      setPage(1)
                    }}
                    className="btn btn-secondary"
                  >
                    Clear Filters
                  </button>
                </div>
              )}

              {hasNext && (
                <div className="mt-8 flex justify-center">
                  <button
                    onClick={() => setPage(p => p + 1)}
                    disabled={loading}
                    className="btn btn-secondary"
                  >
                    Load More
                  </button>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  )
}

export default SkillsHub
