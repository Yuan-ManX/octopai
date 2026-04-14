import React from 'react'
import { Link, useLocation } from 'react-router-dom'

const Navbar = () => {
  const location = useLocation()
  
  const isActive = (path) => {
    if (path === '/') return location.pathname === '/'
    return location.pathname.startsWith(path)
  }

  const navLinks = [
    { path: '/', label: 'Home' },
    { path: '/skill-creator-studio', label: 'Skill Creator' },
    { path: '/evolution-workbench', label: 'AI Evolution' },
    { path: '/skills-hub-pro', label: 'Skills Hub' },
    { path: '/octo-trace', label: 'OctoTrace' },
    { path: '/ai-wiki', label: 'AI Wiki' },
    { path: '/research', label: 'AutoResearch' },
  ]

  return (
    <nav className="nav-container">
      <Link to="/" className="nav-brand">
        <span className="nav-logo-mark">🐙</span>
        Octopai
      </Link>

      <div className="nav-links">
        {navLinks.map(link => (
          <Link
            key={link.path}
            to={link.path}
            style={{
              color: isActive(link.path) ? 'var(--octo-text-primary)' : 'var(--octo-text-secondary)',
              fontWeight: isActive(link.path) ? 500 : 400
            }}
          >
            {link.label}
          </Link>
        ))}
      </div>
    </nav>
  )
}

export default Navbar
