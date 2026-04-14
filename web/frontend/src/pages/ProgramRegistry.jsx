import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

const ProgramRegistry = () => {
  const [programs, setPrograms] = useState([])
  const [currentProgram, setCurrentProgram] = useState(null)
  const [frontier, setFrontier] = useState([])
  const [selectedProgram, setSelectedProgram] = useState(null)
  const [loading, setLoading] = useState(true)

  const fetchPrograms = async () => {
    try {
      const response = await fetch('http://localhost:3002/api/programs')
      const data = await response.json()
      setPrograms(data.programs)
      setCurrentProgram(data.current_program)
      setFrontier(data.frontier)
    } catch (error) {
      console.error('Failed to fetch programs:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchProgramDetail = async (name) => {
    try {
      const response = await fetch(`http://localhost:3002/api/programs/${name}`)
      const data = await response.json()
      setSelectedProgram(data)
    } catch (error) {
      console.error('Failed to fetch program detail:', error)
    }
  }

  const handleSwitch = async (name) => {
    try {
      await fetch(`http://localhost:3002/api/programs/${name}/switch`, {
        method: 'POST'
      })
      fetchPrograms()
    } catch (error) {
      console.error('Failed to switch program:', error)
    }
  }

  const handleDelete = async (name) => {
    if (!window.confirm(`Are you sure you want to delete program "${name}"?`)) {
      return
    }
    try {
      await fetch(`http://localhost:3002/api/programs/${name}`, {
        method: 'DELETE'
      })
      fetchPrograms()
      if (selectedProgram?.name === name) {
        setSelectedProgram(null)
      }
    } catch (error) {
      console.error('Failed to delete program:', error)
    }
  }

  useEffect(() => {
    fetchPrograms()
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen" style={{ background: 'var(--octo-bg-page)', padding: '80px 40px' }}>
        <div className="section-container">
          <div style={{ textAlign: 'center', padding: '80px' }}>
            <div style={{ color: 'var(--octo-text-secondary)' }}>Loading program registry...</div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen" style={{ background: 'var(--octo-bg-page)', padding: '80px 40px' }}>
      <div className="section-container">
        <div className="section-label">Program Registry</div>
        <h1 className="section-heading" style={{ marginBottom: '16px' }}>
          Program Version Management
        </h1>
        <p style={{ color: 'var(--octo-text-secondary)', marginBottom: '48px', fontSize: '1.125rem', maxWidth: '700px' }}>
          Browse and manage all evolved agent programs. Switch between versions, view configurations, and track performance.
        </p>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '32px' }}>
          {/* Programs List */}
          <div>
            <div className="card" style={{ marginBottom: '24px' }}>
              <h3 style={{ 
                fontFamily: 'var(--font-serif)', 
                fontSize: '1.2rem', 
                fontWeight: 500, 
                marginBottom: '20px',
                color: 'var(--octo-text-primary)'
              }}>
                All Programs
              </h3>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {programs.map((name) => {
                  const isCurrent = currentProgram === name
                  const frontierItem = frontier.find(f => f.name === name)
                  
                  return (
                    <div
                      key={name}
                      style={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        padding: '12px 16px',
                        background: isCurrent ? 'rgba(56, 152, 236, 0.1)' : 'var(--octo-dark-surface)',
                        borderRadius: 'var(--radius-comfortable)',
                        border: isCurrent ? '1px solid var(--octo-terracotta)' : '1px solid transparent',
                        cursor: 'pointer'
                      }}
                      onClick={() => fetchProgramDetail(name)}
                    >
                      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                        {isCurrent && (
                          <span style={{ fontSize: '1rem' }}>📍</span>
                        )}
                        <span style={{ 
                          color: 'var(--octo-text-primary)',
                          fontWeight: isCurrent ? 500 : 400
                        }}>
                          {name}
                        </span>
                      </div>
                      {frontierItem && (
                        <span style={{
                          color: 'var(--octo-coral)',
                          fontWeight: 500,
                          fontSize: '0.875rem'
                        }}>
                          {(frontierItem.score * 100).toFixed(1)}%
                        </span>
                      )}
                    </div>
                  )
                })}
              </div>
            </div>

            <Link
              to="/evolution"
              className="btn-secondary"
              style={{ width: '100%', color: '#ffffff', textAlign: 'center', display: 'block' }}
            >
              Back to Evolution
            </Link>
          </div>

          {/* Program Detail */}
          <div>
            {selectedProgram ? (
              <div className="card">
                <h3 style={{ 
                  fontFamily: 'var(--font-serif)', 
                  fontSize: '1.2rem', 
                  fontWeight: 500, 
                  marginBottom: '20px',
                  color: 'var(--octo-text-primary)'
                }}>
                  {selectedProgram.name}
                </h3>

                <div style={{ marginBottom: '24px' }}>
                  <div style={{ 
                    fontSize: '0.813rem', 
                    color: 'var(--octo-text-secondary)', 
                    marginBottom: '8px' 
                  }}>
                    Metadata
                  </div>
                  <div style={{ 
                    background: 'var(--octo-dark-surface)', 
                    padding: '16px', 
                    borderRadius: 'var(--radius-comfortable)',
                    fontSize: '0.875rem',
                    color: 'var(--octo-text-secondary)',
                    lineHeight: '1.8'
                  }}>
                    <div><strong>Generation:</strong> {selectedProgram.metadata.generation}</div>
                    {selectedProgram.metadata.parent && (
                      <div><strong>Parent:</strong> {selectedProgram.metadata.parent}</div>
                    )}
                    <div><strong>Created:</strong> {new Date(selectedProgram.metadata.created_at).toLocaleString()}</div>
                    {selectedProgram.metadata.score !== undefined && (
                      <div><strong>Score:</strong> {(selectedProgram.metadata.score * 100).toFixed(1)}%</div>
                    )}
                    {selectedProgram.metadata.tags?.length > 0 && (
                      <div><strong>Tags:</strong> {selectedProgram.metadata.tags.join(', ')}</div>
                    )}
                  </div>
                </div>

                {selectedProgram.skills?.length > 0 && (
                  <div style={{ marginBottom: '24px' }}>
                    <div style={{ 
                      fontSize: '0.813rem', 
                      color: 'var(--octo-text-secondary)', 
                      marginBottom: '8px' 
                    }}>
                      Skills
                    </div>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                      {selectedProgram.skills.map((skill, idx) => (
                        <span
                          key={idx}
                          style={{
                            background: 'rgba(56, 152, 236, 0.1)',
                            color: 'var(--octo-coral)',
                            padding: '4px 12px',
                            borderRadius: 'var(--radius-tight)',
                            fontSize: '0.813rem'
                          }}
                        >
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {selectedProgram.system_prompt && (
                  <div style={{ marginBottom: '24px' }}>
                    <div style={{ 
                      fontSize: '0.813rem', 
                      color: 'var(--octo-text-secondary)', 
                      marginBottom: '8px' 
                    }}>
                      System Prompt
                    </div>
                    <div style={{ 
                      background: 'var(--octo-dark-surface)', 
                      padding: '16px', 
                      borderRadius: 'var(--radius-comfortable)',
                      fontSize: '0.875rem',
                      color: 'var(--octo-text-secondary)',
                      maxHeight: '200px',
                      overflow: 'auto'
                    }}>
                      {selectedProgram.system_prompt}
                    </div>
                  </div>
                )}

                <div style={{ display: 'flex', gap: '12px' }}>
                  {currentProgram !== selectedProgram.name && (
                    <button
                      onClick={() => handleSwitch(selectedProgram.name)}
                      className="btn-primary"
                      style={{ flex: 1, color: '#ffffff' }}
                    >
                      Switch to this Version
                    </button>
                  )}
                  <button
                    onClick={() => handleDelete(selectedProgram.name)}
                    className="btn-secondary"
                    style={{ color: '#ffffff' }}
                  >
                    Delete
                  </button>
                </div>
              </div>
            ) : (
              <div className="card" style={{ 
                textAlign: 'center', 
                padding: '60px 40px',
                color: 'var(--octo-text-secondary)'
              }}>
                <div style={{ fontSize: '3rem', marginBottom: '16px' }}>📋</div>
                <div>Select a program to view details</div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default ProgramRegistry
