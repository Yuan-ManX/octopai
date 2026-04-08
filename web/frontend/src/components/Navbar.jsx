import React, { useState, useEffect } from 'react'
import { Link, useLocation } from 'react-router-dom'

const Navbar = () => {
  const location = useLocation()
  const [scrolled, setScrolled] = useState(false)
  
  const isActive = (path) => {
    if (path === '/') return location.pathname === '/'
    return location.pathname.startsWith(path)
  }

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20)
    }
    
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const navLinks = [
    { path: '/', label: 'Home' },
    { path: '/agent', label: 'AI Agent' },
    { path: '/skills', label: 'Skills Hub' },
    { path: '/research', label: 'Research' },
  ]

  const isDarkPage = ['/agent'].includes(location.pathname)

  return (
    <nav className={`nav-container ${scrolled ? 'scrolled' : ''}`} style={isDarkPage ? { 
      background: 'rgba(10, 14, 26, 0.92)', 
      borderBottomColor: 'var(--octo-navy)' 
    } : {}}>
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '16px 40px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <Link to="/" className="nav-brand" style={isDarkPage ? { color: 'var(--octo-text-light)' } : {}}>
          <span className="nav-logo-mark">O</span>
          Octopai
        </Link>

        <div className="nav-links">
          {navLinks.map(link => (
            <Link
              key={link.path}
              to={link.path}
              className="nav-link"
              style={{
                color: isDarkPage 
                  ? (isActive(link.path) ? 'var(--octo-text-light)' : 'var(--octo-text-tertiary)')
                  : (isActive(link.path) ? 'var(--octo-text-primary)' : ''),
                fontWeight: isActive(link.path) ? 500 : 400
              }}
            >
              {link.label}
            </Link>
          ))}
          
          <Link 
            to="/create" 
            className="btn-primary" 
            style={{ 
              padding: '8px 20px', 
              fontSize: '0.875rem',
              boxShadow: scrolled ? 'var(--octo-shadow-glow)' : undefined
            }}
          >
            Create Skill
          </Link>
        </div>

        {/* Mobile Menu Button */}
        <button
          className="md:hidden"
          style={{
            background: 'none',
            border: 'none',
            cursor: 'pointer',
            padding: '8px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke={isDarkPage ? 'var(--octo-text-light)' : 'var(--octo-text-primary)'} strokeWidth="2">
            <line x1="3" y1="6" x2="21" y2="6"/>
            <line x1="3" y1="12" x2="21" y2="12"/>
            <line x1="3" y1="18" x2="21" y2="18"/>
          </svg>
        </button>
      </div>
    </nav>
  )
}

export default Navbar
