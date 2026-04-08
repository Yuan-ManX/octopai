import React, { useState } from 'react'
import { Link } from 'react-router-dom'

const Agent = () => {
  const [inputValue, setInputValue] = useState('')
  const [isProcessing, setIsProcessing] = useState(false)

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!inputValue.trim()) return
    
    setIsProcessing(true)
    // Simulate processing
    setTimeout(() => {
      setIsProcessing(false)
      // Handle agent response here
    }, 2000)
  }

  const suggestedPrompts = [
    'Research latest AI developments',
    'Create a web scraping skill',
    'Analyze this document',
    'Generate code for API integration',
    'Explore machine learning techniques'
  ]

  return (
    <div className="min-h-screen" style={{ background: 'linear-gradient(180deg, var(--octo-deep-black) 0%, var(--octo-dark-surface) 100%)' }}>
      {/* Navigation */}
      <nav className="nav-container" style={{ background: 'rgba(10, 14, 26, 0.92)', borderBottomColor: 'var(--octo-navy)' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '16px 40px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <Link to="/" className="nav-brand" style={{ color: 'var(--octo-text-light)' }}>
            <span className="nav-logo-mark">O</span>
            Octopai
          </Link>
          <div className="nav-links">
            <Link to="/" className="nav-link" style={{ color: 'var(--octo-text-tertiary)' }}>Home</Link>
            <Link to="/skills" className="nav-link" style={{ color: 'var(--octo-text-tertiary)' }}>Skills Hub</Link>
            <Link to="/research" className="nav-link" style={{ color: 'var(--octo-text-tertiary)' }}>Research</Link>
            <Link to="/create" className="btn-primary" style={{ padding: '8px 20px', fontSize: '0.875rem' }}>
              Create Skill
            </Link>
          </div>
        </div>
      </nav>

      {/* Main Agent Interface */}
      <main style={{ paddingTop: '60px', paddingBottom: '100px' }}>
        {/* Header Section */}
        <section style={{ textAlign: 'center', marginBottom: '60px', position: 'relative', zIndex: 1 }}>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', padding: '8px 16px', background: 'rgba(56, 152, 236, 0.08)', border: '1px solid rgba(56, 152, 236, 0.20)', borderRadius: '9999px', marginBottom: '24px' }}>
            <span style={{ width: '6px', height: '6px', background: 'var(--octo-focus-blue)', borderRadius: '50%', animation: 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite' }}></span>
            <span style={{ fontSize: '0.875rem', fontWeight: 500, color: 'var(--octo-electric-blue)' }}>AI Agent Engine Active</span>
          </div>
          
          <h1 style={{ fontFamily: 'var(--font-serif)', fontSize: 'clamp(2rem, 5vw, 3.5rem)', fontWeight: 500, lineHeight: 1.10, color: 'var(--octo-text-light)', marginBottom: '16px' }}>
            What would you like to accomplish?
          </h1>
          
          <p style={{ fontFamily: 'var(--font-sans)', fontSize: '1.125rem', lineHeight: 1.65, color: 'var(--octo-text-tertiary)', maxWidth: '600px', margin: '0 auto' }}>
            Your self-evolving AI Agent is ready to tackle complex tasks using its continuously growing Skill ecosystem.
          </p>
        </section>

        {/* Agent Input Box - GenSpark/Manus Style */}
        <section className="agent-input-container">
          <form onSubmit={handleSubmit}>
            <div className="agent-input-wrapper">
              <textarea
                className="agent-input"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Describe your objective in detail... The agent will autonomously plan, execute, and evolve Skills to achieve your goal."
                rows={5}
              />
              
              <div className="agent-input-actions">
                <div className="agent-input-hints">
                  {suggestedPrompts.slice(0, 3).map((prompt, index) => (
                    <button
                      key={index}
                      type="button"
                      className="agent-input-hint"
                      onClick={() => setInputValue(prompt)}
                    >
                      {prompt}
                    </button>
                  ))}
                </div>
                
                <button 
                  type="submit" 
                  className="agent-submit-btn"
                  disabled={!inputValue.trim() || isProcessing}
                  style={{ opacity: (!inputValue.trim() || isProcessing) ? 0.5 : 1 }}
                >
                  {isProcessing ? (
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ animation: 'spin 1s linear infinite' }}>
                      <circle cx="12" cy="12" r="10" strokeOpacity="0.25"/>
                      <path d="M12 2a10 10 0 0 1 10 10" strokeLinecap="round"/>
                    </svg>
                  ) : (
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M5 12h14M12 5l7 7-7 7"/>
                    </svg>
                  )}
                </button>
              </div>
            </div>
          </form>
        </section>

        {/* Agent Capabilities Grid */}
        <section style={{ maxWidth: '1200px', margin: '80px auto 0', padding: '0 40px', position: 'relative', zIndex: 1 }}>
          <div style={{ textAlign: 'center', marginBottom: '48px' }}>
            <div className="section-label">Agent Capabilities</div>
            <h2 style={{ fontFamily: 'var(--font-serif)', fontSize: 'clamp(1.8rem, 3vw, 2.5rem)', fontWeight: 500, color: 'var(--octo-text-light)' }}>
              Powered by Self-Evolving Intelligence
            </h2>
          </div>

          <div className="grid-features">
            <div style={{ background: 'rgba(26, 35, 50, 0.6)', border: '1px solid rgba(71, 85, 105, 0.3)', borderRadius: 'var(--radius-xl)', padding: '32px', backdropFilter: 'blur(10px)' }}>
              <div className="feature-icon" style={{ marginBottom: '20px' }}>🎯</div>
              <h3 style={{ fontFamily: 'var(--font-serif)', fontSize: '1.4rem', fontWeight: 500, color: 'var(--octo-text-light)', marginBottom: '12px' }}>
                Autonomous Task Execution
              </h3>
              <p style={{ color: 'var(--octo-text-tertiary)', lineHeight: 1.65, fontSize: '0.938rem' }}>
                The Agent breaks down complex objectives into executable subtasks, selects appropriate Skills, 
                and executes them autonomously — adapting strategies based on real-time feedback.
              </p>
            </div>

            <div style={{ background: 'rgba(26, 35, 50, 0.6)', border: '1px solid rgba(71, 85, 105, 0.3)', borderRadius: 'var(--radius-xl)', padding: '32px', backdropFilter: 'blur(10px)' }}>
              <div className="feature-icon" style={{ marginBottom: '20px' }}>🧬</div>
              <h3 style={{ fontFamily: 'var(--font-serif)', fontSize: '1.4rem', fontWeight: 500, color: 'var(--octo-text-light)', marginBottom: '12px' }}>
                Dynamic Skill Evolution
              </h3>
              <p style={{ color: 'var(--octo-text-tertiary)', lineHeight: 1.65, fontSize: '0.938rem' }}>
                During task execution, the Agent identifies Skill gaps and automatically evolves new capabilities. 
                Learned experiences are captured and integrated into the Skill ecosystem permanently.
              </p>
            </div>

            <div style={{ background: 'rgba(26, 35, 50, 0.6)', border: '1px solid rgba(71, 85, 105, 0.3)', borderRadius: 'var(--radius-xl)', padding: '32px', backdropFilter: 'blur(10px)' }}>
              <div className="feature-icon" style={{ marginBottom: '20px' }}>🔄</div>
              <h3 style={{ fontFamily: 'var(--font-serif)', fontSize: '1.4rem', fontWeight: 500, color: 'var(--octo-text-light)', marginBottom: '12px' }}>
                Continuous Learning Loop
              </h3>
              <p style={{ color: 'var(--octo-text-tertiary)', lineHeight: 1.65, fontSize: '0.938rem' }}>
                Every interaction feeds the evolution pipeline. The Agent learns from successes and failures, 
                refining its approach and expanding its intelligence with each completed mission.
              </p>
            </div>
          </div>
        </section>

        {/* How It Works Section */}
        <section style={{ maxWidth: '1200px', margin: '80px auto 0', padding: '0 40px', position: 'relative', zIndex: 1 }}>
          <div style={{ textAlign: 'center', marginBottom: '48px' }}>
            <div className="section-label">Workflow</div>
            <h2 style={{ fontFamily: 'var(--font-serif)', fontSize: 'clamp(1.8rem, 3vw, 2.5rem)', fontWeight: 500, color: 'var(--octo-text-light)' }}>
              From Objective to Outcome
            </h2>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '24px', marginTop: '48px' }}>
            {[
              { step: '01', title: 'Understand', desc: 'Agent analyzes your objective, identifies key requirements, and formulates a comprehensive execution strategy.' },
              { step: '02', title: 'Plan', desc: 'Decomposes the objective into subtasks, maps available Skills, and identifies evolution opportunities.' },
              { step: '03', title: 'Execute', desc: 'Runs tasks autonomously, invoking Skills, handling errors, and adapting to changing conditions.' },
              { step: '04', title: 'Evolve', desc: 'Captures learnings, refines Skills, updates knowledge base — making the entire system smarter.' }
            ].map((item, index) => (
              <div key={index} style={{ textAlign: 'center', padding: '32px 24px' }}>
                <div style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  width: '56px',
                  height: '56px',
                  background: 'linear-gradient(135deg, var(--octo-electric-blue), var(--octo-focus-blue))',
                  borderRadius: '50%',
                  fontFamily: 'var(--font-sans)',
                  fontSize: '1.25rem',
                  fontWeight: 600,
                  color: 'white',
                  marginBottom: '20px'
                }}>
                  {item.step}
                </div>
                <h3 style={{ fontFamily: 'var(--font-serif)', fontSize: '1.2rem', fontWeight: 500, color: 'var(--octo-text-light)', marginBottom: '12px' }}>
                  {item.title}
                </h3>
                <p style={{ color: 'var(--octo-text-tertiary)', lineHeight: 1.65, fontSize: '0.9rem' }}>
                  {item.desc}
                </p>
              </div>
            ))}
          </div>
        </section>

        {/* CTA Section */}
        <section style={{ textAlign: 'center', marginTop: '80px', position: 'relative', zIndex: 1 }}>
          <p style={{ color: 'var(--octo-text-tertiary)', marginBottom: '24px', fontSize: '0.938rem' }}>
            Want to expand what your Agent can do?
          </p>
          <div style={{ display: 'flex', gap: '16px', justifyContent: 'center', flexWrap: 'wrap' }}>
            <Link to="/create" className="btn-primary">
              Create New Skill
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M12 5v14M5 12h14"/>
              </svg>
            </Link>
            <Link to="/skills" className="btn-secondary" style={{ background: 'rgba(255, 255, 255, 0.05)', borderColor: 'rgba(71, 85, 105, 0.4)', color: 'var(--octo-text-light)' }}>
              Browse Skill Hub
            </Link>
          </div>
        </section>
      </main>

      <style>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  )
}

export default Agent
