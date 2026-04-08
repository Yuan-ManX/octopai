import React, { useState } from 'react'
import { Link } from 'react-router-dom'

const Research = () => {
  const [activeModule, setActiveModule] = useState('explore')

  const researchModules = [
    {
      id: 'explore',
      title: 'Topic Exploration',
      icon: '🔭',
      description: 'Autonomously explore and map knowledge domains, identifying key concepts, relationships, and information gaps.',
      capabilities: ['Semantic search across sources', 'Knowledge graph construction', 'Trend identification', 'Gap analysis']
    },
    {
      id: 'synthesize',
      title: 'Information Synthesis',
      icon: '🧩',
      description: 'Synthesize information from multiple sources into coherent insights, identifying patterns and contradictions.',
      capabilities: ['Multi-source aggregation', 'Contradiction detection', 'Pattern recognition', 'Insight generation']
    },
    {
      id: 'analyze',
      title: 'Deep Analysis',
      icon: '📊',
      description: 'Perform rigorous analytical tasks including statistical analysis, comparative studies, and predictive modeling.',
      capabilities: ['Statistical analysis', 'Comparative studies', 'Predictive modeling', 'Hypothesis testing']
    },
    {
      id: 'generate',
      title: 'Report Generation',
      icon: '📝',
      description: 'Generate structured research outputs including reports, presentations, and documentation with proper citations.',
      capabilities: ['Structured report writing', 'Citation management', 'Visual data presentation', 'Executive summaries']
    }
  ]

  const workflowSteps = [
    { step: 1, phase: 'Define', desc: 'Specify research objectives, scope, constraints, and success criteria.' },
    { step: 2, phase: 'Plan', desc: 'Agent autonomously designs research methodology and identifies data sources.' },
    { step: 3, phase: 'Execute', desc: 'Conducts research operations, gathers data, performs analysis iteratively.' },
    { step: 4, phase: 'Synthesize', desc: 'Integrates findings, generates insights, produces structured outputs.' },
    { step: 5, phase: 'Evolve', desc: 'Research experience feeds back into Skill ecosystem for continuous improvement.' }
  ]

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
            <Link to="/skills" className="nav-link">Skills Hub</Link>
            <Link to="/create" className="btn-primary" style={{ padding: '8px 20px', fontSize: '0.875rem' }}>
              Create Skill
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section - Dark */}
      <section className="dark-section" style={{ paddingTop: '80px', paddingBottom: '100px' }}>
        <div style={{ position: 'relative', zIndex: 1, maxWidth: '1200px', margin: '0 auto', padding: '0 40px' }}>
          <div style={{ textAlign: 'center', maxWidth: '800px', margin: '0 auto' }}>
            <div className="hero-badge" style={{ marginBottom: '24px' }}>
              <span className="hero-badge-dot"></span>
              <span>Autonomous Research Engine</span>
            </div>

            <h1 style={{
              fontFamily: 'var(--font-serif)',
              fontSize: 'clamp(2.5rem, 5vw, 4rem)',
              fontWeight: 500,
              lineHeight: 1.10,
              color: 'var(--octo-text-light)',
              marginBottom: '24px'
            }}>
              AI-Powered Research<br/>
              <span style={{
                background: 'linear-gradient(135deg, var(--octo-electric-blue), var(--octo-cyan-accent))',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                backgroundClip: 'text'
              }}>Automation Platform</span>
            </h1>

            <p className="body-large" style={{ color: 'var(--octo-text-tertiary)', margin: '0 auto 40px' }}>
              Transform how research is conducted. Our autonomous research module can explore topics, 
              synthesize information, perform deep analysis, and generate comprehensive reports — 
              all while continuously evolving its research capabilities.
            </p>

            <div style={{ display: 'flex', gap: '16px', justifyContent: 'center', flexWrap: 'wrap' }}>
              <button className="btn-primary">
                Start Research Project
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M5 12h14M12 5l7 7-7 7"/>
                </svg>
              </button>
              <Link to="/agent" className="btn-dark">
                Use with AI Agent
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Research Modules Section */}
      <section className="section-container">
        <div className="section-label">Research Capabilities</div>
        <h2 className="section-heading">Four Pillars of Autonomous Research</h2>

        {/* Module Tabs */}
        <div style={{ 
          display: 'flex', 
          gap: '12px', 
          marginBottom: '40px', 
          flexWrap: 'wrap',
          background: 'white',
          border: '1px solid var(--octo-border-subtle)',
          borderRadius: 'var(--radius-xl)',
          padding: '8px'
        }}>
          {researchModules.map(module => (
            <button
              key={module.id}
              onClick={() => setActiveModule(module.id)}
              style={{
                flex: 1,
                minWidth: '200px',
                padding: '16px 20px',
                background: activeModule === module.id ? 'linear-gradient(135deg, rgba(56, 152, 236, 0.08), rgba(37, 99, 235, 0.05))' : 'transparent',
                border: activeModule === module.id ? '1px solid var(--octo-ring-blue)' : '1px solid transparent',
                borderRadius: 'var(--radius-lg)',
                textAlign: 'left',
                cursor: 'pointer',
                transition: 'all var(--transition-base)'
              }}
            >
              <div style={{ fontSize: '1.5rem', marginBottom: '8px' }}>{module.icon}</div>
              <div style={{ 
                fontFamily: 'var(--font-sans)', 
                fontWeight: 600, 
                fontSize: '0.938rem',
                color: activeModule === module.id ? 'var(--octo-electric-blue)' : 'var(--octo-text-primary)'
              }}>
                {module.title}
              </div>
            </button>
          ))}
        </div>

        {/* Active Module Detail */}
        {researchModules.filter(m => m.id === activeModule).map(module => (
          <div key={module.id} style={{
            background: 'white',
            border: '1px solid var(--octo-border-subtle)',
            borderRadius: 'var(--radius-xl)',
            padding: '48px',
            boxShadow: 'var(--octo-shadow-lg)'
          }}>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '48px', alignItems: 'start' }}>
              <div>
                <div style={{ fontSize: '4rem', marginBottom: '24px' }}>{module.icon}</div>
                <h3 style={{
                  fontFamily: 'var(--font-serif)',
                  fontSize: '2rem',
                  fontWeight: 500,
                  marginBottom: '16px'
                }}>
                  {module.title}
                </h3>
                <p className="body-large" style={{ marginBottom: '32px' }}>
                  {module.description}
                </p>

                <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
                  <button className="btn-primary" style={{ padding: '10px 20px' }}>
                    Try This Module
                  </button>
                  <button className="btn-secondary" style={{ padding: '10px 20px' }}>
                    View Examples
                  </button>
                </div>
              </div>

              <div>
                <h4 style={{
                  fontFamily: 'var(--font-sans)',
                  fontSize: '0.875rem',
                  fontWeight: 600,
                  textTransform: 'uppercase',
                  letterSpacing: '0.08em',
                  color: 'var(--octo-focus-blue)',
                  marginBottom: '20px'
                }}>
                  Core Capabilities
                </h4>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                  {module.capabilities.map((capability, index) => (
                    <div key={index} style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '12px',
                      padding: '14px 18px',
                      background: 'var(--octo-frost)',
                      border: '1px solid var(--octo-border-subtle)',
                      borderRadius: 'var(--radius-lg)'
                    }}>
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--octo-electric-blue)" strokeWidth="2">
                        <polyline points="20 6 9 17 4 12"/>
                      </svg>
                      <span style={{ fontFamily: 'var(--font-sans)', fontSize: '0.938rem', color: 'var(--octo-text-secondary)' }}>
                        {capability}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        ))}
      </section>

      {/* Workflow Section - Dark */}
      <section className="dark-section section-container">
        <div style={{ position: 'relative', zIndex: 1 }}>
          <div className="section-label">Research Workflow</div>
          <h2 className="section-heading">From Question to Insight — Autonomously</h2>
          
          <p className="body-large" style={{ maxWidth: '700px', marginBottom: '60px' }}>
            Our structured research workflow ensures systematic, thorough, and reproducible research outcomes.
          </p>

          <div style={{ position: 'relative' }}>
            {/* Timeline Line */}
            <div style={{
              position: 'absolute',
              left: '24px',
              top: '40px',
              bottom: '40px',
              width: '2px',
              background: 'linear-gradient(180deg, var(--octo-electric-blue) 0%, transparent 100%)'
            }}></div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
              {workflowSteps.map((step, index) => (
                <div key={step.step} style={{ 
                  display: 'flex', 
                  gap: '32px', 
                  alignItems: 'start',
                  paddingLeft: '72px',
                  position: 'relative'
                }}>
                  <div style={{
                    position: 'absolute',
                    left: 0,
                    top: 0,
                    width: '50px',
                    height: '50px',
                    background: 'linear-gradient(135deg, var(--octo-electric-blue), var(--octo-focus-blue))',
                    borderRadius: '50%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontFamily: 'var(--font-sans)',
                    fontSize: '1.25rem',
                    fontWeight: 600,
                    color: 'white',
                    boxShadow: 'var(--octo-shadow-glow)'
                  }}>
                    {step.step}
                  </div>

                  <div style={{ flex: 1, paddingTop: '8px' }}>
                    <h3 style={{
                      fontFamily: 'var(--font-serif)',
                      fontSize: '1.4rem',
                      fontWeight: 500,
                      color: 'var(--octo-text-light)',
                      marginBottom: '8px'
                    }}>
                      {step.phase}
                    </h3>
                    <p style={{ 
                      fontFamily: 'var(--font-sans)', 
                      color: 'var(--octo-text-tertiary)', 
                      lineHeight: 1.65,
                      fontSize: '0.938rem'
                    }}>
                      {step.desc}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Organization Features Section */}
      <section className="section-container">
        <div className="section-label">Intelligent Organization</div>
        <h2 className="section-heading">Research Knowledge Management</h2>

        <div className="grid-cards" style={{ marginTop: '48px' }}>
          <div className="card card-standard">
            <div className="card-label">Knowledge Graph</div>
            <div className="feature-icon">🕸️</div>
            <h3 className="card-title">Auto-Organized Insights</h3>
            <p className="card-description">
              All research outputs are automatically organized into interconnected knowledge graphs, 
              making it easy to discover relationships between findings and build on previous work.
            </p>
          </div>

          <div className="card card-standard">
            <div className="card-label">Version Control</div>
            <div className="feature-icon">📚</div>
            <h3 className="card-title">Complete Research History</h3>
            <p className="card-description">
              Every research project maintains full version history with change tracking, 
              allowing you to review evolution of ideas and revert to any previous state.
            </p>
          </div>

          <div className="card card-standard">
            <div className="card-label">Collaboration</div>
            <div className="feature-icon">👥</div>
            <h3 className="card-title">Team Research Spaces</h3>
            <p className="card-description">
              Collaborative research environments where teams can share findings, 
              comment on insights, and collectively evolve research capabilities.
            </p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section style={{ 
        background: 'linear-gradient(180deg, var(--octo-deep-black) 0%, var(--octo-dark-surface) 100%)',
        padding: '80px 40px',
        textAlign: 'center'
      }}>
        <div style={{ maxWidth: '700px', margin: '0 auto', position: 'relative', zIndex: 1 }}>
          <div className="hero-badge" style={{ marginBottom: '24px' }}>
            <span className="hero-badge-dot"></span>
            <span>Ready to Transform Your Research?</span>
          </div>

          <h2 style={{
            fontFamily: 'var(--font-serif)',
            fontSize: 'clamp(1.8rem, 3vw, 2.8rem)',
            fontWeight: 500,
            lineHeight: 1.20,
            color: 'var(--octo-text-light)',
            marginBottom: '20px'
          }}>
            Experience the Future of Research
          </h2>

          <p className="body-large" style={{ color: 'var(--octo-text-tertiary)', margin: '0 auto 36px' }}>
            Let our autonomous research engine handle the heavy lifting while you focus on 
            strategy and decision-making.
          </p>

          <div style={{ display: 'flex', gap: '16px', justifyContent: 'center', flexWrap: 'wrap' }}>
            <button className="btn-primary">
              Launch Research Module
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M5 12h14M12 5l7 7-7 7"/>
              </svg>
            </button>
            <Link to="/skills" className="btn-dark">
              Browse Research Skills
            </Link>
          </div>
        </div>
      </section>

      <div style={{ height: '80px' }}></div>
    </div>
  )
}

export default Research
