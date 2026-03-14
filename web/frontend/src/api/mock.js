const mockSkills = [
  {
    id: 'skill-1',
    name: 'Web Page Analyzer',
    description: 'Analyze and extract content from web pages, converting them into structured Markdown format for AI agents.',
    version: '1.2.0',
    status: 'active',
    icon: '🌐',
    tags: ['web', 'analysis', 'markdown'],
    created_at: '2024-01-15T10:30:00Z',
    updated_at: '2024-03-10T14:20:00Z',
    evolution_count: 3,
    usage_count: 47,
    code: `# Web Page Analyzer Skill\n\nThis skill analyzes web pages and extracts structured content.\n\n## Usage\n\n\`\`\`python\nanalyze_page(url)\n\`\`\``,
    evolution_history: [
      { version: '1.0.0', timestamp: '2024-01-15T10:30:00Z', description: 'Initial release' },
      { version: '1.1.0', timestamp: '2024-02-05T09:15:00Z', description: 'Added image extraction' },
      { version: '1.2.0', timestamp: '2024-03-10T14:20:00Z', description: 'Improved content parsing' },
    ],
    usage_history: [
      { action: 'Execute', timestamp: '2024-03-14T08:30:00Z', outcome: 'Successfully analyzed 3 pages' },
      { action: 'Evolve', timestamp: '2024-03-10T14:20:00Z', outcome: 'Evolution completed, version 1.2.0' },
    ]
  },
  {
    id: 'skill-2',
    name: 'Data Parser',
    description: 'Parse and extract data from various file formats including PDF, DOCX, Excel, and CSV files.',
    version: '2.1.0',
    status: 'active',
    icon: '📊',
    tags: ['data', 'parsing', 'files'],
    created_at: '2024-02-01T16:45:00Z',
    updated_at: '2024-03-12T11:30:00Z',
    evolution_count: 2,
    usage_count: 28,
    code: `# Data Parser Skill\n\nParse various file formats into structured data.\n\n## Supported Formats\n- PDF\n- DOCX\n- Excel (XLSX)\n- CSV`,
    evolution_history: [
      { version: '1.0.0', timestamp: '2024-02-01T16:45:00Z', description: 'Initial release with PDF support' },
      { version: '2.0.0', timestamp: '2024-02-20T13:00:00Z', description: 'Added Excel and CSV support' },
      { version: '2.1.0', timestamp: '2024-03-12T11:30:00Z', description: 'Performance optimization' },
    ],
    usage_history: [
      { action: 'Execute', timestamp: '2024-03-13T15:45:00Z', outcome: 'Processed 5 data files successfully' },
    ]
  },
  {
    id: 'skill-3',
    name: 'Code Assistant',
    description: 'Helps with code analysis, refactoring suggestions, and best practices recommendations.',
    version: '1.0.0',
    status: 'evolving',
    icon: '💻',
    tags: ['code', 'analysis', 'refactoring'],
    created_at: '2024-03-05T09:00:00Z',
    updated_at: '2024-03-14T10:00:00Z',
    evolution_count: 1,
    usage_count: 12,
    code: `# Code Assistant Skill\n\nAnalyze code and provide refactoring suggestions.\n\n## Features\n- Code quality analysis\n- Best practice recommendations\n- Refactoring suggestions`,
    evolution_history: [
      { version: '1.0.0', timestamp: '2024-03-05T09:00:00Z', description: 'Initial release' },
    ],
    usage_history: [
      { action: 'Evolve', timestamp: '2024-03-14T10:00:00Z', outcome: 'Evolution in progress...' },
    ]
  }
]

const mockTasks = new Map()
let taskCounter = 0

export const mockApi = {
  listSkills: async () => {
    await new Promise(resolve => setTimeout(resolve, 500))
    return { skills: mockSkills }
  },

  getSkill: async (skillId) => {
    await new Promise(resolve => setTimeout(resolve, 300))
    const skill = mockSkills.find(s => s.id === skillId)
    return { skill }
  },

  createSkillFromUrl: async (url) => {
    await new Promise(resolve => setTimeout(resolve, 1000))
    const taskId = `task-${++taskCounter}`
    mockTasks.set(taskId, {
      id: taskId,
      status: 'processing',
      message: 'Converting URL to skill...',
      created_at: new Date().toISOString()
    })
    setTimeout(() => {
      mockTasks.set(taskId, {
        id: taskId,
        status: 'completed',
        message: 'Skill created successfully!',
        result: { skill_id: `skill-${Date.now()}` },
        created_at: new Date().toISOString()
      })
    }, 4000)
    return { task_id: taskId }
  },

  createSkillFromFiles: async (formData) => {
    await new Promise(resolve => setTimeout(resolve, 1000))
    const taskId = `task-${++taskCounter}`
    mockTasks.set(taskId, {
      id: taskId,
      status: 'processing',
      message: 'Processing files...',
      created_at: new Date().toISOString()
    })
    setTimeout(() => {
      mockTasks.set(taskId, {
        id: taskId,
        status: 'completed',
        message: 'Skill created successfully from files!',
        result: { skill_id: `skill-${Date.now()}` },
        created_at: new Date().toISOString()
      })
    }, 4000)
    return { task_id: taskId }
  },

  evolveSkill: async (skillId) => {
    await new Promise(resolve => setTimeout(resolve, 800))
    const taskId = `task-${++taskCounter}`
    mockTasks.set(taskId, {
      id: taskId,
      status: 'processing',
      message: 'Starting evolution process...',
      created_at: new Date().toISOString()
    })
    let step = 0
    const evolutionSteps = [
      'Executing skill candidates...',
      'Analyzing execution traces...',
      'Identifying improvement patterns...',
      'Generating optimized version...',
      'Finalizing evolution...'
    ]
    const interval = setInterval(() => {
      if (step < evolutionSteps.length) {
        mockTasks.set(taskId, {
          id: taskId,
          status: 'processing',
          message: evolutionSteps[step],
          created_at: new Date().toISOString()
        })
        step++
      } else {
        clearInterval(interval)
        mockTasks.set(taskId, {
          id: taskId,
          status: 'completed',
          message: 'Evolution completed successfully!',
          result: { new_version: '2.0.0' },
          created_at: new Date().toISOString()
        })
      }
    }, 1200)
    return { task_id: taskId }
  },

  getTaskStatus: async (taskId) => {
    await new Promise(resolve => setTimeout(resolve, 200))
    return mockTasks.get(taskId) || { status: 'not_found', message: 'Task not found' }
  }
}
