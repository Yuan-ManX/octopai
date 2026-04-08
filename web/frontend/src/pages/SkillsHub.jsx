import React, { useState } from 'react'
import { Link } from 'react-router-dom'

const SkillsHub = () => {
  const [activeTab, setActiveTab] = useState('all')
  const [searchQuery, setSearchQuery] = useState('')

  const mockSkills = [
    {
      id: 1,
      name: 'Web Research Agent',
      category: 'Research',
      description: 'Autonomous web research and information synthesis with intelligent source evaluation.',
      version: '3.2.1',
      evolutionLevel: 'Advanced',
      lastEvolved: '2 hours ago',
      icon: '🔍'
    },
    {
      id: 2,
      name: 'Document Parser Pro',
      category: 'Parsing',
      description: 'Multi-format document extraction supporting PDF, DOCX, Excel, and custom formats.',
      version: '2.8.0',
      evolutionLevel: 'Mature',
      lastEvolved: '5 hours ago',
      icon: '📄'
    },
    {
      id: 3,
      name: 'Code Generator',
      category: 'Development',
      description: 'Intelligent code generation with multi-language support and best practice integration.',
      version: '4.1.0',
      evolutionLevel: 'Expert',
      lastEvolved: '1 hour ago',
      icon: '💻'
    },
    {
      id: 4,
      name: 'Data Analyst',
      category: 'Analytics',
      description: 'Statistical analysis, visualization generation, and pattern recognition engine.',
      version: '2.5.3',
      evolutionLevel: 'Intermediate',
      lastEvolved: '12 hours ago',
      icon: '📊'
    },
    {
      id: 5,
      name: 'Content Creator',
      category: 'Creative',
      description: 'Multi-format content generation with style adaptation and SEO optimization.',
      version: '3.0.2',
      evolutionLevel: 'Advanced',
      lastEvolved: '3 hours ago',
      icon: '✍️'
    },
    {
      id: 6,
      name: 'API Integrator',
      category: 'Integration',
      description: 'Seamless API connection builder with authentication handling and error recovery.',
      version: '1.9.0',
      evolutionLevel: 'Growing',
      lastEvolved: '8 hours ago',
      icon: '🔗'
    }
  ]

  const tabs = [
    { id: 'all', label: 'All Skills', count: mockSkills.length },
    { id: 'evolving', label: 'Evolving', count: 4 },
    { id: 'mature', label: 'Mature', count: 2 },
    { id: 'custom', label: 'Custom', count: 0 }
  ]

  const getEvolutionColor = (level) => {
    const colors = {
      'Expert': { bg: 'rgba(16, 185, 129, 0.10)', border: 'rgba(16, 185, 129, 0.30)', text: '#10b981' },
      'Advanced': { bg: 'rgba(56, 152, 236, 0.10)', border: 'rgba(56, 152, 236, 0.30)', text: '#3898ec' },
      'Mature': { bg: 'rgba(99, 102, 241, 0.10)', border: 'rgba(99, 102, 241, 0.30)', text: '#6366f1' },
      'Intermediate': { bg: 'rgba(245, 158, 11, 0.10)', border: 'rgba(245, 158, 11, 0.30)', text: '#f59e0b' },
      'Growing': { bg: 'rgba(148, 163, 184, 0.10)', border: 'rgba(148, 163, 184, 0.30)', text: '#94a3b8' }
    }
    return colors[level] || colors['Growing']
  }

  return (
    <div className="min-h-screen" style={{ background: 'var(--octo-pearl)' }}>
      {/* Navigation */}
      <nav className="nav-container">
        <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '16px 40px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <Link to="/" className="nav-brand">
            <span className="nav-logo-mark">O</span>
            Octopai
          </Link>
          <div className="nav-links">
            <Link to="/" className="nav-link">Home</Link>
            <Link to="/agent" className="nav-link">AI Agent</Link>
            <Link to="/research" className="nav-link">Research</Link>
            <Link to="/create" className="btn-primary" style={{ padding: '8px 20px', fontSize: '0.875rem' }}>
              Create Skill
            </Link>
          </div>
        </div>
      </nav>

      <main style={{ paddingTop: '60px', paddingBottom: '100px' }}>
        {/* Header Section */}
        <section className="section-container" style={{ paddingBottom: '40px' }}>
          <div style={{ display: 'flex', alignItems: 'start', justifyContent: 'space-between', marginBottom: '32px', flexWrap: 'wrap', gap: '24px' }}>
            <div>
              <div className="section-label">Skill Ecosystem</div>
              <h1 className="display-hero" style={{ fontSize: 'clamp(2rem, 4vw, 3rem)' }}>Skills Hub</h1>
              <p className="body-large" style={{ marginTop: '12px', maxWidth: '600px' }}>
                Centralized management for your self-evolving Skill ecosystem. 
                Monitor evolution progress, manage versions, and discover new capabilities.
              </p>
            </div>

            <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
              <Link to="/create" className="btn-primary">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M12 5v14M5 12h14"/>
                </svg>
                New Skill
              </Link>
            </div>
          </div>

          {/* Stats Bar */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
            gap: '20px',
            padding: '24px',
            background: 'white',
            border: '1px solid var(--octo-border-subtle)',
            borderRadius: 'var(--radius-xl)',
            marginBottom: '32px'
          }}>
            <div>
              <div className="stat-value" style={{ fontSize: '2rem' }}>{mockSkills.length}</div>
              <div className="stat-label">Total Skills</div>
            </div>
            <div>
              <div className="stat-value" style={{ fontSize: '2rem', color: '#10b981' }}>4</div>
              <div className="stat-label">Currently Evolving</div>
            </div>
            <div>
              <div className="stat-value" style={{ fontSize: '2rem', color: '#6366f1' }}>127</div>
              <div className="stat-label">Evolution Cycles</div>
            </div>
            <div>
              <div className="stat-value" style={{ fontSize: '2rem', color: '#f59e0b' }}>98%</div>
              <div className="stat-label">Avg. Success Rate</div>
            </div>
          </div>

          {/* Search and Filter */}
          <div style={{ display: 'flex', gap: '16px', marginBottom: '24px', flexWrap: 'wrap' }}>
            <div style={{ flex: '1', minWidth: '300px' }}>
              <input
                type="text"
                className="input-field"
                placeholder="Search skills by name, category, or capability..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                style={{ paddingLeft: '48px', backgroundImage: `url("data:image/svg+xml,%3Csvg width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='%2394a3b8' stroke-width='2'%3E%3Ccircle cx='11' cy='11' r='8'/%3E%3Cpath d='m21 21-4.35-4.35'/%3E%3C/svg%3E")`, backgroundRepeat: 'no-repeat', backgroundPosition: '16px center' }}
              />
            </div>
            
            <div style={{ display: 'flex', gap: '8px', background: 'white', border: '1px solid var(--octo-border-subtle)', borderRadius: 'var(--radius-lg)', padding: '4px' }}>
              {tabs.map(tab => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  style={{
                    padding: '8px 16px',
                    background: activeTab === tab.id ? 'var(--octo-electric-blue)' : 'transparent',
                    color: activeTab === tab.id ? 'white' : 'var(--octo-text-secondary)',
                    border: 'none',
                    borderRadius: 'var(--radius-md)',
                    fontFamily: 'var(--font-sans)',
                    fontSize: '0.875rem',
                    fontWeight: 500,
                    cursor: 'pointer',
                    transition: 'all var(--transition-fast)'
                  }}
                >
                  {tab.label} ({tab.count})
                </button>
              ))}
            </div>
          </div>
        </section>

        {/* Skills Grid */}
        <section style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 40px' }}>
          <div className="grid-cards">
            {mockSkills.map(skill => {
              const evoColor = getEvolutionColor(skill.evolutionLevel)
              return (
                <div key={skill.id} className="skill-card">
                  <div className="skill-card-header">
                    <div className="skill-card-icon">{skill.icon}</div>
                    <span 
                      className="skill-badge" 
                      style={{ 
                        background: evoColor.bg, 
                        borderColor: evoColor.border, 
                        color: evoColor.text 
                      }}
                    >
                      {skill.evolutionLevel}
                    </span>
                  </div>

                  <h3 className="card-title">{skill.name}</h3>
                  
                  <p className="card-description" style={{ marginBottom: '16px' }}>
                    {skill.description}
                  </p>

                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingTop: '16px', borderTop: '1px solid var(--octo-border-subtle)' }}>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                      <span style={{ fontSize: '0.75rem', color: 'var(--octo-text-tertiary)' }}>Version {skill.version}</span>
                      <span style={{ fontSize: '0.75rem', color: 'var(--octo-text-muted)' }}>Last evolved: {skill.lastEvolved}</span>
                    </div>
                    
                    <div style={{ display: 'flex', gap: '8px' }}>
                      <button 
                        style={{
                          padding: '6px 12px',
                          background: 'transparent',
                          color: 'var(--octo-electric-blue)',
                          border: '1px solid rgba(56, 152, 236, 0.30)',
                          borderRadius: 'var(--radius-md)',
                          fontSize: '0.813rem',
                          fontWeight: 500,
                          cursor: 'pointer',
                          transition: 'all var(--transition-fast)'
                        }}
                        onMouseEnter={(e) => {
                          e.target.style.background = 'rgba(56, 152, 236, 0.08)'
                        }}
                        onMouseLeave={(e) => {
                          e.target.style.background = 'transparent'
                        }}
                      >
                        View Details
                      </button>
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        </section>

        {/* Evolution Pipeline Visualization */}
        <section className="dark-section section-container" style={{ marginTop: '80px' }}>
          <div style={{ position: 'relative', zIndex: 1 }}>
            <div className="section-label">Evolution Process</div>
            <h2 className="section-heading">How Skills Self-Evolve</h2>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '32px', marginTop: '48px' }}>
              <div style={{ textAlign: 'center', padding: '32px' }}>
                <div style={{
                  width: '80px',
                  height: '80px',
                  margin: '0 auto 20px',
                  background: 'linear-gradient(135deg, rgba(56, 152, 236, 0.15), rgba(37, 99, 235, 0.10))',
                  border: '2px solid rgba(56, 152, 236, 0.30)',
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '2rem'
                }}>
                  📥
                </div>
                <h3 style={{ fontFamily: 'var(--font-serif)', fontSize: '1.3rem', fontWeight: 500, color: 'var(--octo-text-light)', marginBottom: '12px' }}>
                  Data Ingestion
                </h3>
                <p style={{ color: 'var(--octo-text-tertiary)', lineHeight: 1.65, fontSize: '0.9rem' }}>
                  Collects execution data, user feedback, performance metrics, and environmental signals.
                </p>
              </div>

              <div style={{ textAlign: 'center', padding: '32px' }}>
                <div style={{
                  width: '80px',
                  height: '80px',
                  margin: '0 auto 20px',
                  background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(79, 70, 229, 0.10))',
                  border: '2px solid rgba(99, 102, 241, 0.30)',
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '2rem'
                }}>
                  🧠
                </div>
                <h3 style={{ fontFamily: 'var(--font-serif)', fontSize: '1.3rem', fontWeight: 500, color: 'var(--octo-text-light)', marginBottom: '12px' }}>
                  Pattern Analysis
                </h3>
                <p style={{ color: 'var(--octo-text-tertiary)', lineHeight: 1.65, fontSize: '0.9rem' }}>
                  Identifies patterns, detects inefficiencies, discovers optimization opportunities.
                </p>
              </div>

              <div style={{ textAlign: 'center', padding: '32px' }}>
                <div style={{
                  width: '80px',
                  height: '80px',
                  margin: '0 auto 20px',
                  background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(5, 150, 105, 0.10))',
                  border: '2px solid rgba(16, 185, 129, 0.30)',
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '2rem'
                }}>
                  🔄
                </div>
                <h3 style={{ fontFamily: 'var(--font-serif)', fontSize: '1.3rem', fontWeight: 500, color: 'var(--octo-text-light)', marginBottom: '12px' }}>
                  Self-Optimization
                </h3>
                <p style={{ color: 'var(--octo-text-tertiary)', lineHeight: 1.65, fontSize: '0.9rem' }}>
                  Implements improvements autonomously, updates parameters, refines strategies.
                </p>
              </div>

              <div style={{ textAlign: 'center', padding: '32px' }}>
                <div style={{
                  width: '80px',
                  height: '80px',
                  margin: '0 auto 20px',
                  background: 'linear-gradient(135deg, rgba(245, 158, 11, 0.15), rgba(217, 119, 6, 0.10))',
                  border: '2px solid rgba(245, 158, 11, 0.30)',
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '2rem'
                }}>
                  📈
                </div>
                <h3 style={{ fontFamily: 'var(--font-serif)', fontSize: '1.3rem', fontWeight: 500, color: 'var(octo-text-light)', marginBottom: '12px' }}>
                  Validation & Deploy
                </h3>
                <p style={{ color: 'var(--octo-text-tertiary)', lineHeight: 1.65, fontSize: '0.9rem' }}>
                  Validates changes in sandbox, ensures stability, deploys updated Skill version.
                </p>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  )
}

export default SkillsHub
