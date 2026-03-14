import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api/client'

function SkillList() {
  const [skills, setSkills] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')

  useEffect(() => {
    loadSkills()
  }, [])

  const loadSkills = async () => {
    try {
      const response = await api.listSkills()
      setSkills(response.skills || [])
    } catch (error) {
      console.error('Error loading skills:', error)
    } finally {
      setLoading(false)
    }
  }

  const filteredSkills = skills.filter(skill =>
    skill.name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    skill.description?.toLowerCase().includes(searchQuery.toLowerCase())
  )

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800'
      case 'evolving': return 'bg-yellow-100 text-yellow-800'
      case 'archived': return 'bg-gray-100 text-gray-800'
      default: return 'bg-blue-100 text-blue-800'
    }
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent mb-2">
            Skill Library
          </h1>
          <p className="text-gray-600">Manage and evolve all your Skills</p>
        </div>
        <Link
          to="/create"
          className="px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white font-semibold rounded-xl hover:from-purple-700 hover:to-blue-700 transition-all"
        >
          + Create New Skill
        </Link>
      </div>

      <div className="mb-8">
        <div className="relative">
          <input
            type="text"
            placeholder="Search Skills..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full px-6 py-4 pl-12 border border-gray-300 rounded-2xl focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all text-lg"
          />
          <div className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 text-xl">
            🔍
          </div>
        </div>
      </div>

      {loading ? (
        <div className="text-center py-16">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-purple-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      ) : filteredSkills.length === 0 ? (
        <div className="text-center py-16 bg-white rounded-2xl shadow-xl">
          <div className="text-6xl mb-4">📭</div>
          <h3 className="text-2xl font-bold text-gray-800 mb-2">
            {searchQuery ? 'No matching Skills found' : 'No Skills created yet'}
          </h3>
          <p className="text-gray-600 mb-6">
            {searchQuery ? 'Try a different search term' : 'Start creating your first evolvable Skill now'}
          </p>
          {!searchQuery && (
            <Link
              to="/create"
              className="px-8 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white font-semibold rounded-xl hover:from-purple-700 hover:to-blue-700 transition-all"
            >
              🚀 Create First Skill
            </Link>
          )}
        </div>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {filteredSkills.map((skill) => (
            <Link
              key={skill.id}
              to={`/skills/${skill.id}`}
              className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition-all hover:-translate-y-1"
            >
              <div className="flex justify-between items-start mb-4">
                <div className="text-4xl">
                  {skill.icon || '🧠'}
                </div>
                <span className={`px-3 py-1 rounded-full text-xs font-semibold ${getStatusColor(skill.status || 'active')}`}>
                  {skill.status || 'active'}
                </span>
              </div>
              
              <h3 className="text-xl font-bold text-gray-800 mb-2">
                {skill.name || 'Unnamed Skill'}
              </h3>
              
              <p className="text-gray-600 text-sm mb-4 line-clamp-3">
                {skill.description || 'No description available'}
              </p>
              
              <div className="flex items-center justify-between text-sm text-gray-400 pt-4 border-t border-gray-100">
                <span>v{skill.version || '1.0'}</span>
                <span>{skill.created_at ? new Date(skill.created_at).toLocaleDateString() : 'Just now'}</span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}

export default SkillList
