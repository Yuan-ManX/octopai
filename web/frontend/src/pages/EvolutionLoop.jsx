import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import EvolutionStatus from '../components/EvolutionStatus'

const EvolutionLoop = () => {
  const [status, setStatus] = useState(null)
  const [loading, setLoading] = useState(true)
  const [config, setConfig] = useState({
    max_iterations: 20,
    evolution_mode: 'skill_only',
    continue_mode: false
  })

  const fetchStatus = async () => {
    try {
      const response = await fetch('http://localhost:3002/api/evolution/status')
      const data = await response.json()
      setStatus(data)
    } catch (error) {
      console.error('Failed to fetch evolution status:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchStatus()
    const interval = setInterval(fetchStatus, 2000)
    return () => clearInterval(interval)
  }, [])

  const handleStart = async () => {
    try {
      const response = await fetch('http://localhost:3002/api/evolution/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(config)
      })
      await response.json()
      fetchStatus()
    } catch (error) {
      console.error('Failed to start evolution:', error)
    }
  }

  const handleStop = async () => {
    try {
      await fetch('http://localhost:3002/api/evolution/stop', {
        method: 'POST'
      })
      fetchStatus()
    } catch (error) {
      console.error('Failed to stop evolution:', error)
    }
  }

  const handleReset = async () => {
    if (!window.confirm('Are you sure you want to reset the evolution system? This will delete all progress.')) {
      return
    }
    try {
      await fetch('http://localhost:3002/api/evolution/reset', {
        method: 'POST'
      })
      fetchStatus()
    } catch (error) {
      console.error('Failed to reset evolution:', error)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen" style={{ background: 'var(--octo-bg-page)', padding: '80px 40px' }}>
        <div className="section-container">
          <div style={{ textAlign: 'center', padding: '80px' }}>
            <div style={{ color: 'var(--octo-text-secondary)' }}>Loading evolution system...</div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen" style={{ background: 'var(--octo-bg-page)', padding: '80px 40px' }}>
      <div className="section-container">
        <div className="section-label">Evolution Engine</div>
        <h1 className="section-heading" style={{ marginBottom: '16px' }}>
          Self-Evolving AI Agent
        </h1>
        <p style={{ color: 'var(--octo-text-secondary)', marginBottom: '48px', fontSize: '1.125rem', maxWidth: '700px' }}>
          Watch your AI agent evolve through continuous learning. The system identifies failures, proposes improvements, and retains only the best-performing configurations.
        </p>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '32px', marginBottom: '48px' }}>
          {/* Status Panel */}
          <div style={{ gridColumn: 'span 2' }}>
            <EvolutionStatus status={status} />
          </div>

          {/* Configuration Panel */}
          <div className="card">
            <h3 style={{ 
              fontFamily: 'var(--font-serif)', 
              fontSize: '1.2rem', 
              fontWeight: 500, 
              marginBottom: '20px',
              color: 'var(--octo-text-primary)'
            }}>
              Configuration
            </h3>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
              <div>
                <label style={{ 
                  display: 'block', 
                  fontSize: '0.875rem', 
                  color: 'var(--octo-text-secondary)', 
                  marginBottom: '8px' 
                }}>
                  Max Iterations
                </label>
                <input
                  type="number"
                  value={config.max_iterations}
                  onChange={(e) => setConfig({ ...config, max_iterations: parseInt(e.target.value) })}
                  style={{
                    width: '100%',
                    padding: '12px 16px',
                    background: 'var(--octo-dark-surface)',
                    border: '1px solid var(--octo-border-color)',
                    borderRadius: 'var(--radius-comfortable)',
                    color: 'var(--octo-text-primary)',
                    fontSize: '0.938rem',
                    fontFamily: 'var(--font-sans)'
                  }}
                  disabled={status?.is_running}
                />
              </div>

              <div>
                <label style={{ 
                  display: 'block', 
                  fontSize: '0.875rem', 
                  color: 'var(--octo-text-secondary)', 
                  marginBottom: '8px' 
                }}>
                  Evolution Mode
                </label>
                <select
                  value={config.evolution_mode}
                  onChange={(e) => setConfig({ ...config, evolution_mode: e.target.value })}
                  style={{
                    width: '100%',
                    padding: '12px 16px',
                    background: 'var(--octo-dark-surface)',
                    border: '1px solid var(--octo-border-color)',
                    borderRadius: 'var(--radius-comfortable)',
                    color: 'var(--octo-text-primary)',
                    fontSize: '0.938rem',
                    fontFamily: 'var(--font-sans)'
                  }}
                  disabled={status?.is_running}
                >
                  <option value="skill_only">Skill Only</option>
                  <option value="prompt_only">Prompt Only</option>
                  <option value="hybrid">Hybrid</option>
                </select>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <input
                  type="checkbox"
                  id="continue_mode"
                  checked={config.continue_mode}
                  onChange={(e) => setConfig({ ...config, continue_mode: e.target.checked })}
                  disabled={status?.is_running}
                />
                <label htmlFor="continue_mode" style={{ 
                  fontSize: '0.875rem', 
                  color: 'var(--octo-text-secondary)',
                  cursor: status?.is_running ? 'not-allowed' : 'pointer'
                }}>
                  Continue from last checkpoint
                </label>
              </div>
            </div>
          </div>

          {/* Control Panel */}
          <div className="card">
            <h3 style={{ 
              fontFamily: 'var(--font-serif)', 
              fontSize: '1.2rem', 
              fontWeight: 500, 
              marginBottom: '20px',
              color: 'var(--octo-text-primary)'
            }}>
              Controls
            </h3>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {!status?.is_running ? (
                <button
                  onClick={handleStart}
                  className="btn-primary"
                  style={{ width: '100%', color: '#ffffff' }}
                >
                  Start Evolution
                </button>
              ) : (
                <button
                  onClick={handleStop}
                  className="btn-secondary"
                  style={{ width: '100%', color: '#ffffff' }}
                >
                  Stop Evolution
                </button>
              )}

              <button
                onClick={handleReset}
                className="btn-secondary"
                style={{ 
                  width: '100%', 
                  color: '#ffffff',
                  opacity: status?.is_running ? 0.5 : 1,
                  cursor: status?.is_running ? 'not-allowed' : 'pointer'
                }}
                disabled={status?.is_running}
              >
                Reset System
              </button>

              <Link
                to="/registry"
                className="btn-secondary"
                style={{ width: '100%', color: '#ffffff', textAlign: 'center' }}
              >
                View Program Registry
              </Link>
            </div>

            <div style={{ marginTop: '24px', padding: '16px', background: 'var(--octo-dark-surface)', borderRadius: 'var(--radius-comfortable)' }}>
              <div style={{ fontSize: '0.813rem', color: 'var(--octo-text-secondary)', marginBottom: '8px' }}>
                Evolution Cycle
              </div>
              <ol style={{ 
                margin: 0, 
                paddingLeft: '20px', 
                color: 'var(--octo-text-secondary)',
                fontSize: '0.875rem',
                lineHeight: '1.8'
              }}>
                <li>Base Agent attempts tasks</li>
                <li>Proposer analyzes failures</li>
                <li>Generator creates improvements</li>
                <li>Evaluator measures performance</li>
                <li>Frontier retains best variants</li>
              </ol>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default EvolutionLoop
