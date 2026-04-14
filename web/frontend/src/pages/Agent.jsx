import React, { useState } from 'react'

const Agent = () => {
  const [inputValue, setInputValue] = useState('')
  const [isProcessing, setIsProcessing] = useState(false)

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!inputValue.trim()) return
    
    setIsProcessing(true)
    setTimeout(() => {
      setIsProcessing(false)
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
    <div className="min-h-screen relative" style={{ background: 'var(--octo-bg-page)' }}>
      {/* Stars Background */}
      <div className="stars" aria-hidden="true"></div>
      <div className="stars2" aria-hidden="true"></div>
      <div className="stars3" aria-hidden="true"></div>

      {/* Header Section */}
      <main style={{ paddingTop: '60px', paddingBottom: '100px', position: 'relative', zIndex: 1 }}>
        <section style={{ textAlign: 'center', marginBottom: '60px', padding: '0 40px' }}>
          <h1 style={{ fontFamily: 'var(--font-serif)', fontSize: 'clamp(2rem, 5vw, 3.5rem)', fontWeight: 500, lineHeight: 1.10, color: 'var(--octo-text-primary)', marginBottom: '16px' }}>
            What would you like to accomplish?
          </h1>
          
          <p style={{ fontFamily: 'var(--font-sans)', fontSize: '1.125rem', lineHeight: 1.65, color: 'var(--octo-text-secondary)', maxWidth: '600px', margin: '0 auto' }}>
            Your self-evolving AI Agent is ready to tackle complex tasks using its continuously growing Skill ecosystem.
          </p>
        </section>

        {/* Agent Input Box */}
        <section style={{ maxWidth: '900px', margin: '0 auto', padding: '0 40px' }}>
          <form onSubmit={handleSubmit}>
            <div style={{
              background: 'var(--octo-bg-card)',
              border: '1px solid var(--octo-border-color)',
              borderRadius: 'var(--radius-very)',
              padding: '32px',
              position: 'relative',
              zIndex: 1
            }}>
              <textarea
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Describe your objective in detail... The agent will autonomously plan, execute, and evolve Skills to achieve your goal."
                rows={5}
                style={{
                  width: '100%',
                  background: 'transparent',
                  color: 'var(--octo-text-primary)',
                  border: 'none',
                  fontSize: '1.125rem',
                  fontFamily: 'var(--font-sans)',
                  lineHeight: '1.6',
                  outline: 'none',
                  resize: 'none',
                  marginBottom: '24px'
                }}
              />
              
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
                <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                  {suggestedPrompts.slice(0, 3).map((prompt, index) => (
                    <button
                      key={index}
                      type="button"
                      onClick={() => setInputValue(prompt)}
                      style={{
                        padding: '8px 16px',
                        background: 'rgba(48, 48, 46, 0.5)',
                        border: '1px solid var(--octo-border-color)',
                        borderRadius: 'var(--radius-comfortable)',
                        color: 'var(--octo-text-secondary)',
                        fontSize: '0.875rem',
                        fontFamily: 'var(--font-sans)',
                        cursor: 'pointer',
                        transition: 'all var(--transition-base)'
                      }}
                      onMouseEnter={(e) => {
                        e.target.style.borderColor = 'var(--octo-coral)'
                        e.target.style.color = 'var(--octo-text-primary)'
                      }}
                      onMouseLeave={(e) => {
                        e.target.style.borderColor = 'var(--octo-border-color)'
                        e.target.style.color = 'var(--octo-text-secondary)'
                      }}
                    >
                      {prompt}
                    </button>
                  ))}
                </div>
                
                <button 
                  type="submit" 
                  className="btn-primary"
                  disabled={!inputValue.trim() || isProcessing}
                  style={{ opacity: (!inputValue.trim() || isProcessing) ? 0.5 : 1, color: '#ffffff' }}
                >
                  {isProcessing ? (
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ animation: 'spin 1s linear infinite' }}>
                      <circle cx="12" cy="12" r="10" strokeOpacity="0.25"/>
                      <path d="M12 2a10 10 0 0 1 10 10" strokeLinecap="round"/>
                    </svg>
                  ) : (
                    <>
                      Send to Agent
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M5 12h14M12 5l7 7-7 7"/>
                      </svg>
                    </>
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
            <h2 style={{ fontFamily: 'var(--font-serif)', fontSize: 'clamp(1.8rem, 3vw, 2.5rem)', fontWeight: 500, color: 'var(--octo-text-primary)' }}>
              Powered by Self-Evolving Intelligence
            </h2>
          </div>

          <div className="card-grid">
            <div className="card">
              <div className="feature-icon">🎯</div>
              <h3>Autonomous Task Execution</h3>
              <p>
                The Agent breaks down complex objectives into executable subtasks, selects appropriate Skills, 
                and executes them autonomously — adapting strategies based on real-time feedback.
              </p>
            </div>

            <div className="card">
              <div className="feature-icon">🧬</div>
              <h3>Dynamic Skill Evolution</h3>
              <p>
                During task execution, the Agent identifies Skill gaps and automatically evolves new capabilities. 
                Learned experiences are captured and integrated into the Skill ecosystem permanently.
              </p>
            </div>

            <div className="card">
              <div className="feature-icon">🔄</div>
              <h3>Continuous Learning Loop</h3>
              <p>
                Every interaction feeds the evolution pipeline. The Agent learns from successes and failures, 
                refining its approach and expanding its intelligence with each completed mission.
              </p>
            </div>
          </div>
        </section>

        {/* Evolution Timeline */}
        <section className="dark-section" style={{ marginTop: '80px' }}>
          <div className="section-container">
            <div className="section-label">Evolution Cycle</div>
            <h2 className="section-heading">From Objective to Outcome</h2>

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
                    background: 'var(--octo-terracotta)',
                    borderRadius: '50%',
                    fontFamily: 'var(--font-sans)',
                    fontSize: '1.25rem',
                    fontWeight: 600,
                    color: 'white',
                    marginBottom: '20px'
                  }}>
                    {item.step}
                  </div>
                  <h3 style={{ fontFamily: 'var(--font-serif)', fontSize: '1.3rem', fontWeight: 500, color: 'var(--octo-text-primary)', marginBottom: '12px' }}>
                    {item.title}
                  </h3>
                  <p style={{ color: 'var(--octo-text-secondary)', lineHeight: 1.65, fontSize: '0.938rem' }}>
                    {item.desc}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </section>
      </main>

      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.5; }
        }
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  )
}

export default Agent
