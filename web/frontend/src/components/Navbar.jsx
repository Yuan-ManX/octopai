import React from 'react'
import { Link, useLocation } from 'react-router-dom'

const Navbar = () => {
  const location = useLocation()
  
  const isActive = (path) => location.pathname === path
  
  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-br from-purple-600 to-blue-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">E</span>
              </div>
              <span className="text-xl font-bold text-gray-900">EXO</span>
            </Link>
            <div className="hidden md:ml-10 md:flex md:space-x-1">
              <Link
                to="/"
                className={`px-4 py-2 text-sm font-semibold rounded-lg transition-all ${
                  isActive('/')
                    ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                Home
              </Link>
              <Link
                to="/create"
                className={`px-4 py-2 text-sm font-semibold rounded-lg transition-all ${
                  isActive('/create')
                    ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                Create Skill
              </Link>
              <Link
                to="/skills"
                className={`px-4 py-2 text-sm font-semibold rounded-lg transition-all ${
                  isActive('/skills')
                    ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                Skill Library
              </Link>
              <Link
                to="/docs"
                className={`px-4 py-2 text-sm font-semibold rounded-lg transition-all ${
                  isActive('/docs')
                    ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
              >
                Documentation
              </Link>
            </div>
          </div>
          <div className="flex items-center">
            <div className="text-sm text-gray-500">
              <span className="hidden sm:inline font-medium">Everything Can Be a Skill</span>
            </div>
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
