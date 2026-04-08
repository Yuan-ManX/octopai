import React from 'react'
import { Link } from 'react-router-dom'

const Home = () => {
  return (
    <div className="space-y-0">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-badge">
          <span className="hero-badge-dot"></span>
          <span>Self-Evolving AI Agent Intelligence Engine</span>
        </div>

        <h1 className="display-hero hero-title">
          <span className="highlight">Octopai</span>
        </h1>

        <p className="body-large hero-subtitle">
          The Next Generation AI Agent Platform with Self-Evolving Skills and Autonomous Research Capabilities.
          Transform any resource into intelligent Skills that continuously learn, adapt, and evolve.
        </p>

        <div className="hero-actions">
          <Link to="/agent" className="btn-primary">
            <span>Launch AI Agent</span>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M5 12h14M12 5l7 7-7 7"/>
            </svg>
          </Link>
          <Link to="/skills" className="btn-secondary">
            Explore Skill Hub
          </Link>
          <Link to="/research" className="btn-dark">
            View Research Module
          </Link>
        </div>
      </section>

      <hr className="section-divider" />

      {/* Core Philosophy Section */}
      <section className="section-container">
        <div className="section-label">01 / Core Philosophy</div>
        <h2 className="section-heading">Everything Can Evolve into Intelligence</h2>

        <div className="grid-features">
          <div className="card card-standard">
            <div className="card-label">Universal Skill Transformation</div>
            <div className="feature-icon">🌐</div>
            <h3 className="card-title">From Resource to Skill</h3>
            <p className="card-description">
              Any digital resource — web pages, documents, videos, code repositories, datasets — 
              can be transformed into structured, AI-ready Skills through our proprietary parsing engine.
              One click to convert knowledge into actionable intelligence.
            </p>
          </div>

          <div className="card card-standard">
            <div className="card-label">Continuous Learning System</div>
            <div className="feature-icon">🧬</div>
            <h3 className="card-title">Skills That Evolve</h3>
            <p className="card-description">
              Every Skill in Octopai possesses self-evolution capabilities. Through continuous learning 
              from usage patterns, feedback loops, and interaction data, Skills grow more sophisticated 
              and comprehensive over time — no manual updates required.
            </p>
          </div>

          <div className="card card-standard">
            <div className="card-label">Cognitive Expansion</div>
            <div className="feature-icon">🧠</div>
            <h3 className="card-title">Elevate Agent Intelligence</h3>
            <p className="card-description">
              Through an evolved Skill ecosystem, AI Agents transcend traditional limitations. 
              Each Skill contributes to a collective intelligence network that expands cognitive 
              boundaries and enables complex multi-domain problem solving.
            </p>
          </div>
        </div>
      </section>

      {/* Dark Section - Evolution Engine */}
      <section className="dark-section section-container">
        <div style={{ position: 'relative', zIndex: 1 }}>
          <div className="section-label">02 / Evolution Architecture</div>
          <h2 className="section-heading">Three-Stage Self-Evolution Pipeline</h2>
          <p className="body-large" style={{ maxWidth: '700px', marginBottom: '48px' }}>
            Our proprietary evolution engine empowers Skills to autonomously improve through 
            execution, reflection, and optimization cycles.
          </p>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '32px' }}>
            <div className="evolution-step">
              <div className="evolution-number">1</div>
              <h3 style={{ fontFamily: 'var(--font-serif)', fontSize: '1.4rem', fontWeight: 500, marginTop: '12px', marginBottom: '12px' }}>
                Executor
              </h3>
              <p style={{ color: 'var(--octo-text-tertiary)', lineHeight: 1.65 }}>
                Skills execute tasks in real-world scenarios, gathering performance data, 
                success metrics, and failure patterns. Each execution generates valuable 
                experience data for the learning loop.
              </p>
            </div>

            <div className="evolution-step">
              <div className="evolution-number">2</div>
              <h3 style={{ fontFamily: 'var(--font-serif)', fontSize: '1.4rem', fontWeight: 500, marginTop: '12px', marginBottom: '12px' }}>
                Reflector
              </h3>
              <p style={{ color: 'var(--octo-text-tertiary)', lineHeight: 1.65 }}>
                Advanced reflection mechanisms analyze execution outcomes, identify patterns, 
                detect inefficiencies, and generate insights about what works and what needs improvement.
              </p>
            </div>

            <div className="evolution-step">
              <div className="evolution-number">3</div>
              <h3 style={{ fontFamily: 'var(--font-serif)', fontSize: '1.4rem', fontWeight: 500, marginTop: '12px', marginBottom: '12px' }}>
                Optimizer
              </h3>
              <p style={{ color: 'var(--octo-text-tertiary)', lineHeight: 1.65 }}>
                Based on reflections, the optimizer automatically refines Skill parameters, 
                adjusts strategies, and implements improvements — creating a continuous cycle of self-betterment.
              </p>
            </div>
          </div>
        </div>
      </section>

      <hr className="section-divider" />

      {/* Capabilities Section */}
      <section className="section-container">
        <div className="section-label">03 / Core Capabilities</div>
        <h2 className="section-heading">Built for Autonomous Intelligence</h2>

        <div className="grid-cards" style={{ marginTop: '48px' }}>
          <div className="skill-card">
            <div className="skill-card-header">
              <div className="skill-card-icon">⚡</div>
              <span className="skill-badge">Instant</span>
            </div>
            <h3 className="card-title">One-Click URL to Skill</h3>
            <p className="card-description">
              Paste any URL and watch as our intelligent parser extracts structure, semantics, 
              and actionable knowledge — transforming web content into a fully functional Skill in seconds.
            </p>
          </div>

          <div className="skill-card">
            <div className="skill-card-header">
              <div className="skill-card-icon">📄</div>
              <span className="skill-badge">Multi-Format</span>
            </div>
            <h3 className="card-title">Universal Resource Parser</h3>
            <p className="card-description">
              Support for PDF, DOCX, Excel, images, videos, code repositories, databases, 
              and custom formats. Our parser adapts to any input type automatically.
            </p>
          </div>

          <div className="skill-card">
            <div className="skill-card-header">
              <div className="skill-card-icon">🔄</div>
              <span className="skill-badge">Autonomous</span>
            </div>
            <h3 className="card-title">Self-Evolution Loop</h3>
            <p className="card-description">
              Skills continuously refine themselves without human intervention. The evolution 
              pipeline runs 24/7, making every Skill smarter with each iteration.
            </p>
          </div>

          <div className="skill-card">
            <div className="skill-card-header">
              <div className="skill-card-icon">🎯</div>
              <span className="skill-badge">Intelligent</span>
            </div>
            <h3 className="card-title">Smart Skill Hub</h3>
            <p className="card-description">
              Centralized management with version control, semantic search, skill merging, 
              dependency tracking, and collaborative evolution across teams.
            </p>
          </div>

          <div className="skill-card">
            <div className="skill-card-header">
              <div className="skill-card-icon">🔬</div>
              <span className="skill-badge">Research</span>
            </div>
            <h3 className="card-title">Autonomous Research Module</h3>
            <p className="card-description">
              AI-driven research automation that can explore topics, synthesize information, 
              generate insights, and produce structured research outputs autonomously.
            </p>
          </div>

          <div className="skill-card">
            <div className="skill-card-header">
              <div className="skill-card-icon">🤝</div>
              <span className="skill-badge">Collaborative</span>
            </div>
            <h3 className="card-title">Agent Orchestration</h3>
            <p className="card-description">
              Multiple AI Agents work together seamlessly, sharing Skills, coordinating tasks, 
              and achieving complex objectives through intelligent workflow orchestration.
            </p>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="dark-section" style={{ padding: '80px 40px' }}>
        <div style={{ position: 'relative', zIndex: 1, maxWidth: '1200px', margin: '0 auto' }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '48px', textAlign: 'center' }}>
            <div>
              <div className="stat-value">∞</div>
              <div className="stat-label">Evolution Potential</div>
            </div>
            <div>
              <div className="stat-value">100+</div>
              <div className="stat-label">Resource Formats</div>
            </div>
            <div>
              <div className="stat-value">24/7</div>
              <div className="stat-label">Self-Learning Cycle</div>
            </div>
            <div>
              <div className="stat-value">3-Stage</div>
              <div className="stat-label">Evolution Pipeline</div>
            </div>
          </div>
        </div>
      </section>

      <hr className="section-divider" />

      {/* CTA Section */}
      <section className="section-container" style={{ textAlign: 'center' }}>
        <div className="section-label">Get Started</div>
        <h2 className="section-heading">Experience Self-Evolving Intelligence</h2>
        <p className="body-large" style={{ maxWidth: '600px', margin: '0 auto 40px' }}>
          Join the next generation of AI platforms where Skills don't just exist — they evolve, 
          adapt, and grow smarter every day.
        </p>
        <div className="hero-actions" style={{ justifyContent: 'center' }}>
          <Link to="/agent" className="btn-primary">
            Start with AI Agent
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M5 12h14M12 5l7 7-7 7"/>
            </svg>
          </Link>
          <Link to="/create" className="btn-secondary">
            Create Your First Skill
          </Link>
        </div>
      </section>

      <div style={{ height: '80px' }}></div>
    </div>
  )
}

export default Home
