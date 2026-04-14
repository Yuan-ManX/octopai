import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

const SkillCard = ({ skill, onStar, onFork }) => {
  const [isStarred, setIsStarred] = useState(false)
  const [hovered, setHovered] = useState(false)

  useEffect(() => {
    const checkStarred = async () => {
      try {
        const response = await fetch(`http://localhost:3003/api/skills/${skill.skill_id}/starred`)
        const data = await response.json()
        setIsStarred(data.starred)
      } catch (error) {
        console.error('Error checking starred status:', error)
      }
    }
    checkStarred()
  }, [skill.skill_id])

  const handleStar = async (e) => {
    e.preventDefault()
    e.stopPropagation()
    try {
      const response = await fetch(`http://localhost:3003/api/skills/${skill.skill_id}/star`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: 'demo_user' })
      })
      const data = await response.json()
      setIsStarred(data.starred)
      if (onStar) onStar()
    } catch (error) {
      console.error('Error toggling star:', error)
    }
  }

  const handleFork = async (e) => {
    e.preventDefault()
    e.stopPropagation()
    try {
      const response = await fetch(`http://localhost:3003/api/skills/${skill.skill_id}/fork`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ new_namespace: 'demo', new_name: `${skill.name} (forked)` })
      })
      if (response.ok && onFork) {
        onFork()
      }
    } catch (error) {
      console.error('Error forking skill:', error)
    }
  }

  const getVisibilityColor = () => {
    switch(skill.visibility) {
      case 'public':
        return 'bg-green-500/10 text-green-500 border-green-500/20'
      case 'private':
        return 'bg-yellow-500/10 text-yellow-500 border-yellow-500/20'
      case 'internal':
        return 'bg-gray-500/10 text-gray-400 border-gray-500/20'
      default:
        return 'bg-octo-accent/10 text-octo-accent border-octo-accent/20'
    }
  }

  const getStatusColor = () => {
    switch(skill.status) {
      case 'published':
        return 'bg-blue-500/10 text-blue-500 border-blue-500/20'
      case 'deprecated':
        return 'bg-red-500/10 text-red-500 border-red-500/20'
      default:
        return 'bg-gray-500/10 text-gray-400 border-gray-500/20'
    }
  }

  const getCategoryIcon = (category) => {
    const icons = {
      'Data Science': '📊',
      'Development': '💻',
      'Research': '🔍',
      'Content Creation': '✍️',
      'AI Tools': '🤖',
      'Productivity': '⚡',
      'Integration': '🔗',
      'Automation': '⚙️',
      'default': '📁'
    }
    return icons[category] || icons['default']
  }

  return (
    <Link 
      to={`/skills-hub/${skill.skill_id}`} 
      className="block group"
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      <div className={`card p-5 transition-all duration-200 ${
        hovered 
          ? 'shadow-xl shadow-octo-accent/10 -translate-y-1 border-octo-accent/30' 
          : 'shadow-md hover:shadow-lg'
      }`}>
        <div className="flex justify-between items-start mb-3">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-2 flex-wrap">
              <span className="text-xs text-octo-text-tertiary font-mono truncate max-w-[100px]">
                {skill.namespace}/
              </span>
              <h3 className="text-base font-semibold text-gray-900 dark:text-gray-100 truncate group-hover:text-octo-accent transition-colors">
                {skill.name}
              </h3>
            </div>
            
            <div className="flex items-center gap-1.5 mb-2 flex-wrap">
              <span className={`px-1.5 py-0.5 rounded text-xs font-medium border ${getVisibilityColor()}`}>
                {skill.visibility}
              </span>
              {skill.status && (
                <span className={`px-1.5 py-0.5 rounded text-xs font-medium border ${getStatusColor()}`}>
                  {skill.status}
                </span>
              )}
              {skill.latest_version && (
                <span className="text-xs text-octo-text-tertiary font-mono">
                  v{skill.latest_version.version}
                </span>
              )}
            </div>

            <p className="text-sm text-gray-600 dark:text-gray-400 mb-3 line-clamp-2 leading-relaxed">
              {skill.description}
            </p>
          </div>

          <div className="ml-3 flex-shrink-0">
            <div className={`w-12 h-12 rounded-lg flex items-center justify-center text-2xl transition-transform ${
              hovered ? 'scale-110 rotate-3' : ''
            } ${
              skill.categories?.[0] 
                ? 'bg-gradient-to-br from-octo-accent/20 to-blue-500/20' 
                : 'bg-gray-50 dark:bg-gray-800'
            }`}>
              {skill.categories?.[0] ? getCategoryIcon(skill.categories[0]) : '🎯'}
            </div>
          </div>
        </div>

        {skill.categories && skill.categories.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mb-3">
            {skill.categories.slice(0, 2).map((category, idx) => (
              <span 
                key={idx}
                className="inline-flex items-center gap-1 px-2 py-0.5 bg-gray-50 dark:bg-gray-800 rounded-full text-xs text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:bg-gray-700 transition-colors"
              >
                <span>{getCategoryIcon(category)}</span>
                {category}
              </span>
            ))}
            {skill.categories.length > 2 && (
              <span className="px-2 py-0.5 bg-gray-100 dark:bg-gray-700 rounded-full text-xs text-octo-text-tertiary">
                +{skill.categories.length - 2} more
              </span>
            )}
          </div>
        )}

        {skill.tags && skill.tags.length > 0 && (
          <div className="flex flex-wrap gap-1 mb-3">
            {skill.tags.slice(0, 4).map((tag, idx) => (
              <span 
                key={idx}
                className="px-1.5 py-0.5 bg-gray-100 dark:bg-gray-700 rounded text-xs text-octo-text-tertiary hover:text-octo-accent hover:bg-octo-accent/10 transition-colors cursor-default"
              >
                #{tag}
              </span>
            ))}
            {skill.tags.length > 4 && (
              <span className="px-1.5 py-0.5 text-xs text-octo-text-tertiary">
                +{skill.tags.length - 4}
              </span>
            )}
          </div>
        )}

        <div className="flex items-center justify-between pt-3 border-t border-octo-border">
          <div className="flex items-center gap-3 text-xs text-octo-text-tertiary">
            <div className="flex items-center gap-1 group/star" title="Stars">
              <span className={isStarred ? 'text-yellow-500' : ''}>⭐</span>
              <span className={isStarred ? 'font-medium text-yellow-600' : ''}>{skill.star_count}</span>
            </div>
            <div className="flex items-center gap-1" title="Forks">
              <span>🍴</span>
              <span>{skill.fork_count}</span>
            </div>
            <div className="flex items-center gap-1 hidden sm:flex" title="Downloads">
              <span>⬇️</span>
              <span>{skill.download_count}</span>
            </div>
            <div className="flex items-center gap-1 hidden md:flex" title="Views">
              <span>👁️</span>
              <span>{skill.view_count}</span>
            </div>
            {skill.versions && (
              <div className="flex items-center gap-1 hidden lg:flex" title="Versions">
                <span>📦</span>
                <span>{skill.versions.length}</span>
              </div>
            )}
          </div>
          
          <div className="flex items-center gap-1.5 opacity-0 group-hover:opacity-100 transition-opacity">
            <button
              onClick={handleStar}
              className={`px-2.5 py-1 rounded-md text-xs font-medium transition-all ${
                isStarred 
                  ? 'bg-yellow-500 text-white shadow-sm shadow-yellow-500/25' 
                  : 'bg-gray-50 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-yellow-500/10 hover:text-yellow-500'
              }`}
              title={isStarred ? 'Unstar' : 'Star this skill'}
            >
              {isStarred ? '★' : '☆'}
            </button>
            <button
              onClick={handleFork}
              className="px-2.5 py-1 rounded-md text-xs font-medium bg-gray-50 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-blue-500/10 hover:text-blue-500 transition-colors"
              title="Fork this skill"
            >
              🍴
            </button>
          </div>
        </div>

        {hovered && (
          <div className="mt-3 pt-3 border-t border-octo-border border-dashed animate-fadeIn">
            <div className="flex items-center justify-between text-xs text-octo-text-tertiary">
              <span>Click to view details →</span>
              <span className="font-mono">npx octopai install {skill.namespace}/{skill.slug}</span>
            </div>
          </div>
        )}
      </div>
    </Link>
  )
}

export default SkillCard
