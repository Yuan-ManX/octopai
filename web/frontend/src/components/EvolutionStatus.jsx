import React from 'react'

const EvolutionStatus = ({ status }) => {
  if (!status) {
    return (
      <div style={{ 
        padding: '32px', 
        textAlign: 'center', 
        color: 'var(--octo-text-secondary)' 
      }}>
        Loading evolution status...
      </div>
    )
  }

  const progress = (status.iteration / status.max_iterations) * 100

  return (
    <div className="card" style={{ marginBottom: '24px' }}>
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center', 
        marginBottom: '16px' 
      }}>
        <h3 style={{ 
          fontFamily: 'var(--font-serif)', 
          fontSize: '1.2rem', 
          fontWeight: 500, 
          margin: 0,
          color: 'var(--octo-text-primary)'
        }}>
          Evolution Status
        </h3>
        <span style={{
          background: status.is_running ? 'rgba(56, 152, 236, 0.2)' : 'var(--octo-dark-surface)',
          color: status.is_running ? 'var(--octo-coral)' : 'var(--octo-text-secondary)',
          padding: '4px 12px',
          borderRadius: 'var(--radius-tight)',
          fontSize: '0.813rem',
          fontWeight: 500
        }}>
          {status.is_running ? 'Running' : 'Idle'}
        </span>
      </div>

      {/* Progress Bar */}
      <div style={{ marginBottom: '20px' }}>
        <div style={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          marginBottom: '8px',
          fontSize: '0.875rem',
          color: 'var(--octo-text-secondary)'
        }}>
          <span>Iteration {status.iteration} of {status.max_iterations}</span>
          <span>{Math.round(progress)}%</span>
        </div>
        <div style={{
          background: 'var(--octo-dark-surface)',
          height: '8px',
          borderRadius: '4px',
          overflow: 'hidden'
        }}>
          <div style={{
            background: 'var(--octo-terracotta)',
            height: '100%',
            width: `${progress}%`,
            borderRadius: '4px',
            transition: 'width 0.3s ease'
          }}/>
        </div>
      </div>

      {/* Stats Grid */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', 
        gap: '16px' 
      }}>
        <div style={{
          background: 'var(--octo-dark-surface)',
          padding: '16px',
          borderRadius: 'var(--radius-comfortable)'
        }}>
          <div style={{ 
            fontSize: '0.813rem', 
            color: 'var(--octo-text-secondary)', 
            marginBottom: '4px' 
          }}>
            Total Cost
          </div>
          <div style={{ 
            fontSize: '1.5rem', 
            fontWeight: 500, 
            color: 'var(--octo-text-primary)' 
          }}>
            ${status.total_cost.toFixed(4)}
          </div>
        </div>

        <div style={{
          background: 'var(--octo-dark-surface)',
          padding: '16px',
          borderRadius: 'var(--radius-comfortable)'
        }}>
          <div style={{ 
            fontSize: '0.813rem', 
            color: 'var(--octo-text-secondary)', 
            marginBottom: '4px' 
          }}>
            Frontier Size
          </div>
          <div style={{ 
            fontSize: '1.5rem', 
            fontWeight: 500, 
            color: 'var(--octo-text-primary)' 
          }}>
            {status.frontier.length}
          </div>
        </div>
      </div>

      {/* Frontier List */}
      {status.frontier.length > 0 && (
        <div style={{ marginTop: '20px' }}>
          <div style={{ 
            fontSize: '0.875rem', 
            color: 'var(--octo-text-secondary)', 
            marginBottom: '12px' 
          }}>
            Top Performing Programs
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {status.frontier.map((program, index) => (
              <div 
                key={index}
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  padding: '12px 16px',
                  background: index === 0 ? 'rgba(56, 152, 236, 0.1)' : 'var(--octo-dark-surface)',
                  borderRadius: 'var(--radius-comfortable)',
                  border: index === 0 ? '1px solid var(--octo-terracotta)' : '1px solid transparent'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  {index === 0 && (
                    <span style={{ fontSize: '1.2rem' }}>👑</span>
                  )}
                  <span style={{ 
                    color: 'var(--octo-text-primary)',
                    fontWeight: index === 0 ? 500 : 400
                  }}>
                    {program.name}
                  </span>
                </div>
                <span style={{
                  color: 'var(--octo-coral)',
                  fontWeight: 500,
                  fontSize: '0.938rem'
                }}>
                  {(program.score * 100).toFixed(1)}%
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default EvolutionStatus
