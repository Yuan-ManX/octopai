import React, { useState, useEffect, useRef } from 'react'
import { useNavigate, Link } from 'react-router-dom'

const CONTENT_TYPES = [
  { id: 'text', label: 'Text', icon: '📝', desc: 'Articles, documentation, notes', color: 'from-blue-500 to-cyan-500' },
  { id: 'code', label: 'Code', icon: '💻', desc: 'Python, JavaScript, Rust, Go...', color: 'from-violet-500 to-purple-500' },
  { id: 'document', label: 'Document', icon: '📄', desc: 'PDF, Word, Markdown files', color: 'from-emerald-500 to-teal-500' },
  { id: 'media', label: 'Media', icon: '🎬', desc: 'Audio, Video transcription', color: 'from-pink-500 to-rose-500' },
  { id: 'presentation', label: 'Presentation', icon: '📊', desc: 'PPT, Keynote extraction', color: 'from-amber-500 to-orange-500' },
  { id: 'template', label: 'Template', icon: '📋', desc: 'Existing skill templates', color: 'from-indigo-500 to-blue-500' },
  { id: 'url', label: 'URL Import', icon: '🔗', desc: 'Import from web or GitHub', color: 'from-fuchsia-500 to-pink-500' },
  { id: 'natural', label: 'Natural Language', icon: '🗣️', desc: 'Describe in plain language', color: 'from-teal-500 to-green-500' },
  { id: 'api', label: 'API Definition', icon: '🔌', desc: 'OpenAPI/Swagger spec', color: 'from-orange-500 to-red-500' },
  { id: 'dataset', label: 'Dataset', icon: '📚', desc: 'CSV/JSON patterns', color: 'from-slate-500 to-zinc-500' },
]

const CREATION_METHODS = [
  { id: 'auto', label: 'Auto-Generate', icon: '🤖', desc: 'AI analyzes and creates automatically', color: 'from-purple-600 to-violet-600' },
  { id: 'guided', label: 'Guided Wizard', icon: '🧭', desc: 'Step-by-step AI assistance', color: 'from-blue-600 to-cyan-600' },
  { id: 'from-scratch', label: 'From Scratch', icon: '✏️', desc: 'Manual definition editor', color: 'from-emerald-600 to-teal-600' },
  { id: 'import', label: 'Import Existing', icon: '📥', desc: 'Import from other formats', color: 'from-amber-600 to-orange-600' },
]

const SkillCreatorStudio = () => {
  const navigate = useNavigate()
  const fileInputRef = useRef(null)
  const dropZoneRef = useRef(null)
  
  const [activeStep, setActiveStep] = useState(1)
  const [loading, setLoading] = useState(false)
  const [analyzing, setAnalyzing] = useState(false)
  const [error, setError] = useState(null)
  const [creationMethod, setCreationMethod] = useState('auto')
  
  const [selectedType, setSelectedType] = useState('text')
  const [content, setContent] = useState('')
  const [fileName, setFileName] = useState('')
  const [isDragging, setIsDragging] = useState(false)
  
  const [analysisResult, setAnalysisResult] = useState(null)
  const [skillConfig, setSkillConfig] = useState({
    name: '',
    description: '',
    namespace: 'demo',
    visibility: 'public',
    version: '1.0.0',
    author: 'demo',
    category: '',
    tags: [],
    keywords: [],
    license: 'MIT',
    homepage: '',
    repository: ''
  })
  
  const [tagInput, setTagInput] = useState('')
  const [generatedSkill, setGeneratedSkill] = useState(null)
  const [evolutionReady, setEvolutionReady] = useState(false)
  const [previewMode, setPreviewMode] = useState('card')
  const [recentSkills, setRecentSkills] = useState([])
  const [showSuccessConfetti, setShowSuccessConfetti] = useState(false)
  
  // Composite Skill Composer state
  const [showComposer, setShowComposer] = useState(false)
  const [composerSkills, setComposerSkills] = useState([])
  const [dragOver, setDragOver] = useState(false)

  useEffect(() => {
    loadRecentSkills()
  }, [])

  const loadRecentSkills = async () => {
    try {
      const response = await fetch('http://localhost:3005/api/hub/repositories?limit=5')
      if (response.ok) {
        const data = await response.json()
        setRecentSkills(data.repositories || [])
      }
    } catch (err) {
      console.log('Could not load recent skills')
    }
  }

  // Composite Skill Composer handlers
  const handleDragStart = (e, skillName) => {
    e.dataTransfer.setData('skill', skillName)
    e.dataTransfer.effectAllowed = 'copy'
  }

  const handleDropToCanvas = (e) => {
    e.preventDefault()
    setDragOver(false)
    
    const skillName = e.dataTransfer.getData('skill')
    if (skillName && !composerSkills.includes(skillName)) {
      setComposerSkills([...composerSkills, skillName])
    }
  }

  const removeFromComposer = (index) => {
    setComposerSkills(composerSkills.filter((_, idx) => idx !== index))
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(true)
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
  }

  const handleDrop = async (e) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
    
    const file = e.dataTransfer.files?.[0]
    if (!file) return
    
    await processFile(file)
  }

  const processFile = async (file) => {
    setFileName(file.name)
    
    if (file.type.startsWith('text/') || file.name.endsWith('.md') || 
        file.name.endsWith('.py') || file.name.endsWith('.js') || 
        file.name.endsWith('.json') || file.name.endsWith('.txt') ||
        file.name.endsWith('.ts') || file.name.endsWith('.jsx') ||
        file.name.endsWith('.tsx') || file.name.endsWith('.rs') ||
        file.name.endsWith('.go') || file.name.endsWith('.java') ||
        file.name.endsWith('.cpp') || file.name.endsWith('.h') ||
        file.name.endsWith('.yaml') || file.name.endsWith('.yml') ||
        file.name.endsWith('.toml') || file.name.endsWith('.csv')) {
      const text = await file.text()
      setContent(text)
      autoDetectContentType(file.name, text)
    } else if (file.type.startsWith('image/') || file.type.startsWith('audio/') || 
               file.type.startsWith('video/')) {
      setContent(`[Media file: ${file.name} (${(file.size / 1024).toFixed(1)} KB)]\nType: ${file.type}\nSize: ${(file.size / 1024 / 1024).toFixed(2)} MB`)
      setSelectedType('media')
    } else {
      setContent(`[Binary file: ${file.name} (${(file.size / 1024).toFixed(1)} KB)]`)
      setSelectedType('media')
    }
  }

  const handleContentUpload = async (e) => {
    const file = e.target.files?.[0]
    if (!file) return
    await processFile(file)
  }

  const autoDetectContentType = (name, text) => {
    const ext = name.split('.').pop().toLowerCase()
    const typeMap = {
      py: 'code', js: 'code', ts: 'code', jsx: 'code', tsx: 'code',
      java: 'code', cpp: 'code', h: 'code', c: 'code',
      rs: 'code', go: 'code', rb: 'code', php: 'code',
      md: 'text', txt: 'text', rst: 'text', adoc: 'text',
      pdf: 'document', doc: 'document', docx: 'document',
      ppt: 'presentation', pptx: 'presentation',
      mp3: 'media', mp4: 'media', wav: 'media', mov: 'media',
      webm: 'media', ogg: 'media', flac: 'media',
      yaml: 'code', yml: 'code', json: 'code', toml: 'code',
      csv: 'dataset', xml: 'code', html: 'code'
    }
    setSelectedType(typeMap[ext] || 'text')
  }

  const handleAnalyzeContent = async () => {
    if (!content.trim()) return
    
    setAnalyzing(true)
    setError(null)
    
    try {
      const response = await fetch('http://localhost:3005/api/creator/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          content,
          filename: fileName || undefined
        })
      })
      
      if (!response.ok) throw new Error('Analysis failed')
      
      const data = await response.json()
      setAnalysisResult(data.analysis)
      
      if (data.recommended_config) {
        setSkillConfig(prev => ({
          ...prev,
          name: data.recommended_config.name || prev.name,
          category: data.recommended_config.category || prev.category,
          tags: [...new Set([...prev.tags, ...(data.recommended_config.suggested_tags || [])])]
        }))
      }
      
      setActiveStep(2)
    } catch (err) {
      setError(err.message)
    } finally {
      setAnalyzing(false)
    }
  }

  const handleGenerateSkill = async () => {
    if (!skillConfig.name || !skillConfig.description || !content) return
    
    setLoading(true)
    setError(null)
    
    try {
      const response = await fetch('http://localhost:3005/api/creator/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          request: {
            name: skillConfig.name,
            description: skillConfig.description,
            source_type: selectedType,
            source_content: content,
            metadata: {
              version: skillConfig.version,
              author: skillConfig.author,
              category: skillConfig.category,
              tags: skillConfig.tags,
              keywords: skillConfig.keywords
            }
          }
        })
      })
      
      if (!response.ok) throw new Error('Generation failed')
      
      const data = await response.json()
      setGeneratedSkill(data.result)
      setActiveStep(3)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handlePublishToHub = async () => {
    if (!generatedSkill) return
    
    setLoading(true)
    
    try {
      const response = await fetch('http://localhost:3005/api/hub/repositories', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: generatedSkill.skill_name || skillConfig.name,
          description: skillConfig.description,
          visibility: skillConfig.visibility,
          owner_id: 'demo-user'
        })
      })
      
      if (response.ok) {
        setShowSuccessConfetti(true)
        setTimeout(() => setShowSuccessConfetti(false), 2000)
        setEvolutionReady(true)
        setActiveStep(4)
      }
    } catch (err) {
      console.error('Publish error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleStartEvolution = () => {
    navigate('/evolution-workbench')
  }

  const handleAddTag = (e) => {
    if (e.key === 'Enter' && tagInput.trim()) {
      e.preventDefault()
      if (!skillConfig.tags.includes(tagInput.trim())) {
        setSkillConfig(prev => ({
          ...prev,
          tags: [...prev.tags, tagInput.trim()]
        }))
      }
      setTagInput('')
    }
  }

  const getQualityColor = (score) => {
    if (score >= 0.8) return 'text-green-500'
    if (score >= 0.6) return 'text-yellow-500'
    return 'text-red-500'
  }

  const getQualityBg = (score) => {
    if (score >= 0.8) return 'bg-gradient-to-r from-green-500 to-emerald-500'
    if (score >= 0.6) return 'bg-gradient-to-r from-yellow-500 to-amber-500'
    return 'bg-gradient-to-r from-red-500 to-rose-500'
  }

  const stepLabels = ['Select Method', 'Input Content', 'Configure Skill', 'Generate & Publish']
  const stepDescriptions = [
    'Choose how you want to create your skill',
    'Provide your source material for analysis',
    'Fine-tune the skill configuration details',
    'Review and publish your creation'
  ]

  return (
    <div className="min-h-screen py-8 relative overflow-hidden">
      {showSuccessConfetti && (
        <div className="fixed inset-0 z-[100] pointer-events-none flex items-center justify-center">
          <div className="absolute inset-0 bg-black/20 backdrop-blur-sm"></div>
          <div className="relative z-10 text-9xl animate-bounce">🎉</div>
        </div>
      )}

      <div className="max-w-7xl mx-auto px-6">
        
        {/* Header - Optimized Layout */}
        <div className="mb-12">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-6 group">
              <div className="w-20 h-20 bg-gradient-to-br from-violet-500 via-purple-600 to-fuchsia-600 rounded-3xl flex items-center justify-center text-white text-4xl shadow-2xl shadow-purple-500/40 animate-pulse-subtle ring-4 ring-purple-500/20 relative overflow-hidden shrink-0 transform hover:scale-105 hover:shadow-3xl transition-all duration-300">
                <span className="relative z-10 drop-shadow-lg">⚡</span>
                <div className="absolute inset-0 bg-gradient-to-br from-white/20 via-white/10 to-transparent animate-pulse"></div>
                <div className="absolute -inset-1 bg-gradient-to-br from-violet-400/30 to-fuchsia-400/30 rounded-3xl blur-xl opacity-60 group-hover:opacity-100 transition-opacity"></div>
              </div>
              <div className="min-w-0 flex-1">
                <h1 className="text-5xl font-black bg-gradient-to-r from-blue-600 via-cyan-500 to-blue-700 dark:from-blue-400 dark:via-cyan-300 dark:to-blue-400 bg-clip-text text-transparent mb-3 tracking-wide drop-shadow-xl filter leading-snug">
                  Skill Creator Studio
                </h1>
                <p className="text-gray-700 dark:text-gray-300 text-base leading-relaxed font-medium max-w-2xl opacity-90">
                  Transform any content into intelligent AI agent skills — code, documents, media, APIs, or describe what you need in plain language
                </p>
              </div>
            </div>
            <Link 
              to="/skills-hub-pro" 
              className="group px-5 py-2.5 bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-700 border border-gray-300 dark:border-gray-600 hover:border-violet-400 rounded-xl transition-all duration-200 text-sm font-medium text-gray-700 dark:text-gray-300 hover:text-violet-600 flex items-center gap-2"
            >
              📦 View Skills Hub
              <span className="group-hover:translate-x-1 transition-transform">→</span>
            </Link>
          </div>
        </div>

        {/* Composite Skill Composer - Advanced Feature */}
        <div className="mb-8 bg-gradient-to-br from-violet-50 via-purple-50 to-fuchsia-50 dark:from-violet-950/20 dark:via-purple-950/20 dark:to-fuchsia-950/20 rounded-3xl p-6 border border-violet-200/50 dark:border-violet-800/30 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-40 h-40 bg-gradient-to-bl from-purple-300/20 to-transparent rounded-full blur-3xl"></div>
          <div className="absolute bottom-0 left-0 w-32 h-32 bg-gradient-to-tr from-cyan-300/20 to-transparent rounded-full blur-2xl"></div>
          
          <div className="relative z-10">
            <div className="flex items-center justify-between mb-5">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-gradient-to-br from-violet-600 to-purple-600 rounded-xl flex items-center justify-center text-white text-lg shadow-lg shadow-violet-500/30 ring-2 ring-violet-500/20">
                  🔗
                </div>
                <h3 className="text-xl font-black bg-gradient-to-r from-violet-700 to-purple-700 dark:from-violet-300 dark:to-purple-300 bg-clip-text text-transparent">
                  Composite Skill Composer
                </h3>
              </div>
              <button 
                onClick={() => setShowComposer(!showComposer)}
                className="px-5 py-2.5 bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-700 hover:to-purple-700 text-white rounded-xl font-bold transition-all duration-300 shadow-lg shadow-violet-500/25 hover:shadow-xl hover:shadow-violet-500/40 flex items-center gap-2"
              >
                {showComposer ? '✕ Close' : '⚡ Open Composer'}
                <span className="text-xs opacity-80">NEW</span>
              </button>
            </div>

            {showComposer && (
              <div className="mt-6 space-y-6">
                <p className="text-sm font-semibold text-gray-700 dark:text-gray-300 leading-relaxed">
                  Combine multiple atomic skills into powerful composite workflows. Build complex tool chains that can be reused across tasks — inspired by advanced compositional AI agent architectures.
                </p>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
                  {/* Available Atomic Skills */}
                  <div className="bg-white/80 dark:bg-black/25 rounded-2xl p-5 border border-white/50 dark:border-gray-700/40">
                    <h4 className="font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                      <span className="w-7 h-7 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center text-sm">📦</span>
                      Atomic Skills Library
                    </h4>
                    <div className="space-y-2.5 max-h-64 overflow-y-auto pr-2">
                      {['Web Research Agent', 'Document Parser', 'Code Generator', 'Data Analyst', 'Content Creator', 'API Integrator', 'Email Automation', 'Database Query'].map((skill, idx) => (
                        <div 
                          key={idx}
                          draggable
                          onDragStart={(e) => handleDragStart(e, skill)}
                          className={`flex items-center gap-3 p-3 bg-gradient-to-r ${['from-blue-50 to-cyan-50', 'from-violet-50 to-purple-50', 'from-emerald-50 to-teal-50', 'from-amber-50 to-orange-50', 'from-pink-50 to-rose-50'][idx % 5]} dark:from-gray-800/60 dark:to-gray-700/60 rounded-xl cursor-grab hover:shadow-lg hover:scale-[1.02] transition-all group border border-transparent hover:border-violet-300 dark:hover:border-violet-700`}
                        >
                          <div className={`w-8 h-8 bg-gradient-to-br ${['from-blue-500 to-cyan-500', 'from-violet-500 to-purple-500', 'from-emerald-500 to-teal-500', 'from-amber-500 to-orange-500', 'from-pink-500 to-rose-500'][idx % 5]} rounded-lg flex items-center justify-center text-sm shadow-md group-hover:rotate-6 transition-transform duration-300`}>
                            {['🔍', '📄', '💻', '📊', '✍️'][idx % 5]}
                          </div>
                          <span className="text-sm font-bold text-gray-800 dark:text-gray-200 flex-1">{skill}</span>
                          <span className="text-xs text-gray-500 dark:text-gray-400 opacity-0 group-hover:opacity-100 transition-opacity">⠿</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Composition Canvas */}
                  <div className="lg:col-span-2 bg-white/90 dark:bg-black/35 rounded-2xl p-5 border-2 border-dashed border-violet-300 dark:border-violet-700 min-h-[280px]"
                       onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
                       onDragLeave={() => setDragOver(false)}
                       onDrop={handleDropToCanvas}
                  >
                    <h4 className="font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                      <span className="w-7 h-7 bg-gradient-to-br from-emerald-500 to-green-500 rounded-lg flex items-center justify-center text-sm">🎨</span>
                      Composition Canvas
                      <span className="ml-auto text-xs font-normal text-gray-500 dark:text-gray-400">{composerSkills.length} skills added</span>
                    </h4>

                    {composerSkills.length === 0 ? (
                      <div className={`flex flex-col items-center justify-center h-48 border-2 ${dragOver ? 'border-violet-400 bg-violet-50/50' : 'border-gray-200 dark:border-gray-600'} border-dashed rounded-xl transition-all`}>
                        <span className="text-4xl mb-3 opacity-50">🎯</span>
                        <p className="text-sm font-semibold text-gray-500 dark:text-gray-400 mb-1">Drag atomic skills here</p>
                        <p className="text-xs text-gray-400 dark:text-gray-500">Build your composite workflow</p>
                      </div>
                    ) : (
                      <div className="space-y-3">
                        {composerSkills.map((skill, idx) => (
                          <div key={idx} className="flex items-center gap-3 p-4 bg-gradient-to-r from-violet-100 to-purple-100 dark:from-violet-900/30 dark:to-purple-900/30 rounded-xl border border-violet-200 dark:border-violet-800 shadow-md hover:shadow-lg transition-all group">
                            <div className="w-8 h-8 bg-violet-600 rounded-lg flex items-center justify-center text-white text-sm font-bold shadow-md">
                              {idx + 1}
                            </div>
                            <span className="font-bold text-gray-900 dark:text-gray-100 flex-1">{skill}</span>
                            <button 
                              onClick={() => removeFromComposer(idx)}
                              className="w-7 h-7 bg-red-100 hover:bg-red-200 dark:bg-red-900/30 dark:hover:bg-red-900/50 rounded-lg flex items-center justify-center text-red-600 hover:text-red-700 transition-colors opacity-0 group-hover:opacity-100"
                            >
                              ✕
                            </button>
                            {idx < composerSkills.length - 1 && (
                              <div className="absolute right-6 top-full w-0.5 h-4 bg-violet-400"></div>
                            )}
                          </div>
                        ))}
                        
                        {/* Efficiency Metrics Preview */}
                        <div className="mt-5 pt-4 border-t border-violet-200 dark:border-violet-800">
                          <div className="grid grid-cols-3 gap-4">
                            <div className="text-center p-3 bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 rounded-xl">
                              <div className="text-2xl font-black text-green-600 dark:text-green-400">
                                {Math.max(0, Math.min(85, 45 + composerSkills.length * 8))}%
                              </div>
                              <div className="text-xs font-bold text-gray-600 dark:text-gray-400 mt-1">Token Save</div>
                            </div>
                            <div className="text-center p-3 bg-gradient-to-br from-blue-50 to-cyan-50 dark:from-blue-900/20 dark:to-cyan-900/20 rounded-xl">
                              <div className="text-2xl font-black text-blue-600 dark:text-blue-400">
                                {composerSkills.length}x
                              </div>
                              <div className="text-xs font-bold text-gray-600 dark:text-gray-400 mt-1">Complexity</div>
                            </div>
                            <div className="text-center p-3 bg-gradient-to-br from-violet-50 to-purple-50 dark:from-violet-900/20 dark:to-purple-900/20 rounded-xl">
                              <div className="text-2xl font-black text-violet-600 dark:text-violet-400">
                                ∞
                              </div>
                              <div className="text-xs font-bold text-gray-600 dark:text-gray-400 mt-1">Reusable</div>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>

                {composerSkills.length >= 2 && (
                  <div className="flex gap-4 pt-2">
                    <button 
                      onClick={() => {
                        alert(`Composite skill "${composerSkills.join(' + ')}" created successfully!\n\nThis workflow combines ${composerSkills.length} atomic skills into a single reusable composite skill.`)
                      }}
                      className="flex-1 px-6 py-3.5 bg-gradient-to-r from-violet-600 via-purple-600 to-fuchsia-600 hover:from-violet-700 hover:to-fuchsia-700 text-white rounded-xl font-bold transition-all duration-300 shadow-xl shadow-violet-500/30 hover:shadow-violet-500/50 flex items-center justify-center gap-2"
                    >
                      <span>💾</span>
                      Save Composite Skill
                    </button>
                    <button 
                      onClick={() => {
                        setComposerSkills([])
                        setDragOver(false)
                      }}
                      className="px-6 py-3.5 bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-xl font-bold transition-all text-gray-700 dark:text-gray-300"
                    >
                      Clear All
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Progress Steps */}
        <div className="mb-10 p-1 bg-gray-100/80 dark:bg-gray-800/60 rounded-2xl border border-gray-200/60 dark:border-gray-700/50">
          <div className="flex items-center justify-between px-8 py-4">
            {[1, 2, 3, 4].map((step) => (
              <React.Fragment key={step}>
                <div className={`flex flex-col items-center gap-2 cursor-pointer group`} onClick={() => step < activeStep && setActiveStep(step)}>
                  <div className={`relative w-12 h-12 rounded-full flex items-center justify-center text-base font-bold transition-all duration-500 ${
                    activeStep > step 
                      ? 'bg-gradient-to-br from-green-500 to-emerald-500 text-white shadow-lg shadow-green-500/30 scale-105' 
                      : activeStep === step 
                        ? 'bg-gradient-to-br from-violet-500 via-purple-500 to-fuchsia-500 text-white shadow-xl shadow-purple-500/40 ring-4 ring-purple-500/20 scale-110' 
                        : 'bg-gray-200 dark:bg-gray-700 text-gray-500 dark:text-gray-400 group-hover:bg-gray-300 dark:group-hover:bg-gray-600 group-hover:text-gray-700 dark:group-hover:text-gray-300'
                  }`}>
                    {activeStep > step ? (
                      <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
                        <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                      </svg>
                    ) : (
                      step
                    )}
                    {activeStep === step && (
                      <span className="absolute inset-0 rounded-full bg-violet-500 animate-ping opacity-20"></span>
                    )}
                  </div>
                  <div className="text-center">
                    <div className={`text-xs font-semibold whitespace-nowrap transition-colors ${
                      activeStep >= step ? 'text-violet-600 dark:text-violet-400' : 'text-gray-500 dark:text-gray-400'
                    }`}>
                      {stepLabels[step - 1]}
                    </div>
                    <div className="text-[10px] text-gray-400 dark:text-gray-500 mt-0.5 hidden sm:block">{stepDescriptions[step - 1]}</div>
                  </div>
                </div>
                {step < 4 && (
                  <div className={`flex-1 h-0.5 mx-4 rounded-full transition-all duration-700 ${
                    activeStep > step ? 'bg-gradient-to-r from-green-500 to-emerald-400' : 'bg-gray-300 dark:bg-gray-600'
                  }`}></div>
                )}
              </React.Fragment>
            ))}
          </div>
        </div>

        {/* Error Banner */}
        {error && (
          <div className="mb-6 bg-gradient-to-r from-red-500/10 to-rose-500/10 border border-red-300 dark:border-red-800/50 rounded-xl p-4 flex items-center gap-3 animate-in slide-in-from-top-2 duration-200">
            <div className="w-8 h-8 bg-red-500/20 rounded-lg flex items-center justify-center shrink-0">
              <span>❌</span>
            </div>
            <span className="text-red-700 dark:text-red-400 font-medium flex-1">{error}</span>
            <button onClick={() => setError(null)} className="w-8 h-8 rounded-lg hover:bg-red-500/10 flex items-center justify-center text-red-500 hover:text-red-700 transition-colors font-bold">×</button>
          </div>
        )}

        <div className="grid grid-cols-1 xl:grid-cols-4 gap-6">
          {/* Main Content Area */}
          <div className="xl:col-span-3 space-y-6">

            {/* Step 1: Select Creation Method & Input Content */}
            {activeStep === 1 && (
              <>
                {/* Creation Methods Selection */}
                <div className="card p-7 space-y-7">
                  <div className="flex items-center gap-3 mb-2">
                    <div className="w-8 h-8 bg-gradient-to-r from-violet-500 to-purple-500 rounded-lg flex items-center justify-center text-white text-sm font-bold">1</div>
                    <h3 className="text-xl font-bold text-gray-900 dark:text-white">Choose Your Creation Method</h3>
                  </div>
                  
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {CREATION_METHODS.map((method) => (
                      <button
                        key={method.id}
                        onClick={() => setCreationMethod(method.id)}
                        className={`relative p-5 rounded-2xl border-2 transition-all duration-300 group ${
                          creationMethod === method.id
                            ? `border-transparent bg-gradient-to-br ${method.color} text-white shadow-xl scale-[1.02]`
                            : 'border-gray-200 dark:border-gray-700 hover:border-violet-400 bg-white dark:bg-gray-800 hover:shadow-lg hover:-translate-y-0.5'
                        }`}
                      >
                        <div className={`text-3xl mb-3 ${creationMethod !== method.id && 'group-hover:scale-110'} transition-transform`}>{method.icon}</div>
                        <div className={`font-bold mb-1 ${creationMethod === method.id ? 'text-white' : 'text-gray-900 dark:text-gray-100'}`}>{method.label}</div>
                        <div className={`text-xs leading-relaxed ${creationMethod === method.id ? 'text-white/85' : 'text-gray-500 dark:text-gray-400'}`}>{method.desc}</div>
                        {creationMethod === method.id && (
                          <div className="absolute top-3 right-3 w-6 h-6 bg-white/30 rounded-full flex items-center justify-center">
                            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="white" strokeWidth={3}><path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" /></svg>
                          </div>
                        )}
                      </button>
                    ))}
                  </div>

                  {/* Content Type Selection */}
                  <div className="border-t border-gray-200 dark:border-gray-700 pt-7">
                    <div className="flex items-center gap-3 mb-5">
                      <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center text-white text-sm font-bold">2</div>
                      <h4 className="font-bold text-gray-900 dark:text-white">Select Input Type</h4>
                    </div>
                    
                    <div className="grid grid-cols-5 md:grid-cols-10 gap-2.5">
                      {CONTENT_TYPES.map((type) => (
                        <button
                          key={type.id}
                          onClick={() => setSelectedType(type.id)}
                          className={`relative p-3 rounded-xl border-2 transition-all duration-200 group ${
                            selectedType === type.id
                              ? `border-transparent bg-gradient-to-br ${type.color} text-white shadow-lg scale-105`
                              : 'border-gray-200 dark:border-gray-700 hover:border-violet-400 bg-white dark:bg-gray-800 hover:scale-105 hover:shadow-md'
                          }`}
                        >
                          <div className="text-xl mb-1">{type.icon}</div>
                          <div className={`text-[10px] font-bold leading-tight ${selectedType === type.id ? 'text-white' : 'text-gray-800 dark:text-gray-200'}`}>{type.label}</div>
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Content Input Area with Drag & Drop */}
                  <div className="border-t border-gray-200 dark:border-gray-700 pt-7">
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-lg flex items-center justify-center text-white text-sm font-bold">3</div>
                        <label className="font-bold text-gray-900 dark:text-white">
                          {selectedType === 'url' ? 'URL to Import' : 
                           selectedType === 'natural' ? 'Describe Your Skill' :
                           selectedType === 'api' ? 'API Specification' :
                           selectedType === 'dataset' ? 'Dataset Content' :
                           'Content Input'}
                        </label>
                      </div>
                      <div className="flex gap-2">
                        {!['url', 'natural'].includes(selectedType) && (
                          <>
                            <button
                              onClick={() => fileInputRef.current?.click()}
                              className="px-4 py-2 text-sm bg-violet-50 hover:bg-violet-100 dark:bg-violet-950/30 dark:hover:bg-violet-950/50 text-violet-700 dark:text-violet-300 rounded-xl transition-all font-medium flex items-center gap-2 border border-violet-200 dark:border-violet-800"
                            >
                              📁 Upload File
                            </button>
                            {fileName && (
                              <span className="px-4 py-2 text-sm bg-blue-50 dark:bg-blue-950/30 text-blue-700 dark:text-blue-300 rounded-xl flex items-center gap-2 border border-blue-200 dark:border-blue-800 font-medium max-w-[220px] truncate">
                                📎 {fileName}
                                <button onClick={() => {setFileName(''); setContent('')}} className="hover:text-red-600 ml-1 font-bold">×</button>
                              </span>
                            )}
                          </>
                        )}
                      </div>
                      <input
                        ref={fileInputRef}
                        type="file"
                        onChange={handleContentUpload}
                        className="hidden"
                        accept=".txt,.md,.py,.js,.ts,.jsx,.tsx,.json,.pdf,.doc,.docx,.ppt,.pptx,.rs,.go,.java,.cpp,.c,.h,.rb,.php,.yaml,.yml,.toml,.csv,.xml,.html,.mp3,.mp4,.wav,.mov,.webm,.ogg,.flac"
                      />
                    </div>

                    {/* Drag and Drop Zone */}
                    <div
                      ref={dropZoneRef}
                      onDragOver={handleDragOver}
                      onDragLeave={handleDragLeave}
                      onDrop={handleDrop}
                      className={`relative rounded-2xl border-2 border-dashed transition-all duration-300 ${
                        isDragging 
                          ? 'border-violet-500 bg-violet-50 dark:bg-violet-950/20 scale-[1.01]' 
                          : 'border-gray-300 dark:border-gray-600 hover:border-violet-400 bg-gray-50/50 dark:bg-gray-800/30'
                      }`}
                    >
                      {isDragging && (
                        <div className="absolute inset-0 z-10 flex items-center justify-center bg-violet-50/90 dark:bg-violet-950/50 rounded-2xl">
                          <div className="text-center">
                            <div className="text-5xl mb-3">📥</div>
                            <div className="text-lg font-bold text-violet-700 dark:text-violet-300">Drop files here</div>
                            <div className="text-sm text-violet-500 dark:text-violet-400">Release to upload</div>
                          </div>
                        </div>
                      )}

                      {selectedType === 'natural' ? (
                        <textarea
                          value={content}
                          onChange={(e) => setContent(e.target.value)}
                          rows={11}
                          placeholder={`Describe the skill you want to create in natural language...

Example:
"I want a skill that can analyze Python code for performance bottlenecks. It should identify slow functions, memory leaks, and suggest optimizations."

Be specific about:
• What the skill should do
• When it should be used  
• What inputs it expects
• What outputs it produces`}
                          className="w-full px-5 py-4 bg-transparent focus:outline-none text-gray-900 dark:text-gray-100 resize-none placeholder:text-gray-400 dark:placeholder:text-gray-500"
                        />
                      ) : selectedType === 'url' ? (
                        <div className="p-5 space-y-4">
                          <input
                            type="url"
                            placeholder="https://github.com/user/repo or https://example.com/article"
                            value={content}
                            onChange={(e) => setContent(e.target.value)}
                            className="w-full px-5 py-3.5 bg-transparent border-none focus:outline-none text-gray-900 dark:text-gray-100 placeholder:text-gray-400 dark:placeholder:text-gray-500 text-base"
                          />
                          <div className="flex gap-2 flex-wrap">
                            {['GitHub Repository', 'Documentation Page', 'API Spec', 'Research Paper'].map((hint) => (
                              <button key={hint} onClick={() => setContent('https://')} className="px-4 py-1.5 text-xs bg-gray-100 dark:bg-gray-700 rounded-full text-gray-600 dark:text-gray-400 hover:bg-violet-50 dark:hover:bg-violet-950/30 hover:text-violet-600 dark:hover:text-violet-400 transition-all font-medium border border-transparent hover:border-violet-300 dark:hover:border-violet-700">
                                {hint}
                              </button>
                            ))}
                          </div>
                        </div>
                      ) : (
                        <textarea
                          value={content}
                          onChange={(e) => setContent(e.target.value)}
                          rows={14}
                          placeholder={
                            selectedType === 'code' ? '# Paste your code here\ndef example_function():\n    pass' :
                            selectedType === 'document' ? '# Paste document content here\n## Title\n\nYour content...' :
                            selectedType === 'media' ? '# Media file will be processed\n# Upload audio/video for transcription and analysis' :
                            selectedType === 'presentation' ? '# Slide content or outline\n## Slide 1: Title\n\n## Slide 2: Introduction' :
                            selectedType === 'template' ? '# Template configuration\n---\nname: my-skill\ndescription: ...' :
                            selectedType === 'api' ? 'openapi: "3.0.0"\ninfo:\n  title: My API\n  version: 1.0.0' :
                            selectedType === 'dataset' ? 'column1,column2,column3\nvalue1,value2,value3\nvalue4,value5,value6' :
                            `Paste or upload your ${selectedType} content here...`
                          }
                          className="w-full px-5 py-4 bg-transparent focus:outline-none text-gray-900 dark:text-gray-100 font-mono text-sm resize-none placeholder:text-gray-400 dark:placeholder:text-gray-500"
                        />
                      )}

                      {!content && !isDragging && (
                        <div className="absolute bottom-6 left-1/2 -translate-x-1/2 text-center pointer-events-none">
                          <p className="text-sm text-gray-400 dark:text-gray-500">
                            <span className="font-medium text-gray-500 dark:text-gray-400">Drop files here</span> or paste content above
                          </p>
                        </div>
                      )}
                    </div>

                    {/* Action Bar */}
                    <div className="flex justify-between items-center pt-5 mt-5 border-t border-gray-200 dark:border-gray-700">
                      <div className="flex items-center gap-4">
                        {content.length > 0 && (
                          <div className="flex items-center gap-2 px-3 py-1.5 bg-gray-100 dark:bg-gray-800 rounded-lg text-xs text-gray-600 dark:text-gray-400 font-mono">
                            <span>{content.length.toLocaleString()}</span>
                            <span className="text-gray-300 dark:text-gray-600">|</span>
                            <span>{content.split(/\s+/).filter(w => w).length.toLocaleString()} words</span>
                            <span className="text-gray-300 dark:text-gray-600">|</span>
                            <span>{content.split('\n').length} lines</span>
                          </div>
                        )}
                      </div>
                      <button
                        onClick={handleAnalyzeContent}
                        disabled={!content.trim() || analyzing}
                        className="group px-8 py-3 bg-gradient-to-r from-violet-600 via-purple-600 to-fuchsia-600 hover:from-violet-700 hover:to-fuchsia-700 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-xl font-semibold transition-all duration-300 shadow-lg shadow-purple-500/25 hover:shadow-xl hover:shadow-purple-500/40 flex items-center gap-2 disabled:hover:shadow-lg"
                      >
                        {analyzing ? (
                          <>
                            <span className="animate-spin">⏳</span>
                            Analyzing Content...
                          </>
                        ) : (
                          <>
                            🔍 Analyze & Continue
                            <span className="group-hover:translate-x-1 transition-transform">→</span>
                          </>
                        )}
                      </button>
                    </div>
                  </div>
                </div>
              </>
            )}

            {/* Step 2: Configure Skill */}
            {activeStep === 2 && (
              <div className="card p-7 space-y-7">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-xl flex items-center justify-center text-white font-bold">⚙️</div>
                    <h3 className="text-xl font-bold text-gray-900 dark:text-white">Configure Your Skill</h3>
                  </div>
                  <button
                    onClick={() => setActiveStep(1)}
                    className="text-sm text-violet-600 hover:text-violet-700 dark:text-violet-400 dark:hover:text-violet-300 font-medium flex items-center gap-1.5 px-3 py-1.5 rounded-lg hover:bg-violet-50 dark:hover:bg-violet-950/20 transition-all"
                  >
                    ← Back to Content
                  </button>
                </div>

                {/* Analysis Results Card */}
                {analysisResult && (
                  <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-blue-50 via-purple-50 to-pink-50 dark:from-blue-950/30 dark:via-purple-950/30 dark:to-pink-950/30 border border-blue-200/70 dark:border-blue-800/50">
                    <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-bl from-purple-200/50 to-transparent dark:from-purple-800/20 rounded-full blur-3xl"></div>
                    <div className="relative p-6">
                      <div className="flex items-start justify-between mb-5">
                        <div className="flex items-center gap-3">
                          <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-500 rounded-xl flex items-center justify-center text-white text-lg shadow-lg shadow-blue-500/30">
                            🔬
                          </div>
                          <div>
                            <h4 className="font-bold text-blue-800 dark:text-blue-200 text-lg">Intelligent Analysis Results</h4>
                            <p className="text-xs text-blue-600/80 dark:text-blue-400/80 mt-0.5">AI-powered content understanding</p>
                          </div>
                        </div>
                        <div className={`px-4 py-1.5 rounded-full text-sm font-bold text-white shadow-lg ${getQualityBg(analysisResult.quality_score || 0)}`}>
                          {(analysisResult.quality_score * 100 || 0).toFixed(0)}% Quality
                        </div>
                      </div>
                      
                      <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                        {[
                          { label: 'Content Type', value: analysisResult.content_type || selectedType, icon: '📋' },
                          { label: 'Language', value: analysisResult.detected_language || 'Auto', icon: '🌐' },
                          { label: 'Complexity', value: analysisResult.complexity || 'Medium', icon: '📊' },
                          { label: 'Sections', value: analysisResult.section_count || Math.ceil(content.length / 500), icon: '📑' },
                          { label: 'Recommended', value: analysisResult.recommended_skill_type || 'Custom', icon: '💡', highlight: true }
                        ].map((item, idx) => (
                          <div key={idx} className={`bg-white/80 dark:bg-gray-900/50 backdrop-blur-sm rounded-xl p-3.5 border ${item.highlight ? 'border-violet-300/60 bg-violet-50/70 dark:bg-violet-900/30' : 'border-white/50 dark:border-gray-700/50'}`}>
                            <div className={`${item.highlight ? 'text-violet-700 dark:text-violet-300' : 'text-blue-700 dark:text-blue-300'} text-[10px] uppercase tracking-wider font-bold`}>{item.label}</div>
                            <div className="flex items-center gap-1.5 mt-1">
                              <span className="text-sm">{item.icon}</span>
                              <div className={`font-bold text-gray-900 dark:text-gray-100 capitalize text-sm ${item.highlight && 'text-violet-700 dark:text-violet-300'}`}>
                                {item.value}
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>

                      {analysisResult.extracted_entities && analysisResult.extracted_entities.length > 0 && (
                        <div className="mt-5 pt-5 border-t border-blue-200/40 dark:border-blue-800/30">
                          <div className="text-blue-700 dark:text-blue-300 text-sm mb-3 font-semibold flex items-center gap-2">
                            <span>🏷️</span> Detected Entities ({analysisResult.extracted_entities.length})
                          </div>
                          <div className="flex flex-wrap gap-2">
                            {analysisResult.extracted_entities.slice(0, 15).map((entity, idx) => (
                              <span key={idx} className="px-3 py-1.5 bg-white/85 dark:bg-gray-800/60 text-blue-800 dark:text-blue-200 rounded-lg text-xs font-medium border border-blue-100/60 dark:border-blue-900/40 hover:bg-blue-50 dark:hover:bg-blue-900/30 transition-colors cursor-default">
                                {entity}
                              </span>
                            ))}
                            {analysisResult.extracted_entities.length > 15 && (
                              <span className="px-3 py-1.5 bg-blue-100/60 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400 rounded-lg text-xs font-medium">
                                +{analysisResult.extracted_entities.length - 15} more
                              </span>
                            )}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {/* Configuration Form */}
                <div className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                    <div>
                      <label className="block text-sm font-bold text-gray-800 dark:text-gray-200 mb-2.5">
                        Skill Name <span className="text-red-500">*</span>
                      </label>
                      <input
                        type="text"
                        value={skillConfig.name}
                        onChange={(e) => setSkillConfig(prev => ({...prev, name: e.target.value}))}
                        required
                        placeholder="e.g., python-code-analyzer"
                        className="w-full px-4 py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-xl focus:outline-none focus:ring-2 focus:ring-violet-500/50 focus:border-violet-400 text-gray-900 dark:text-gray-100 transition-all font-medium placeholder:text-gray-400 dark:placeholder:text-gray-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-bold text-gray-800 dark:text-gray-200 mb-2.5">
                        Category
                      </label>
                      <select
                        value={skillConfig.category}
                        onChange={(e) => setSkillConfig(prev => ({...prev, category: e.target.value}))}
                        className="w-full px-4 py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-xl focus:outline-none focus:ring-2 focus:ring-violet-500/50 focus:border-violet-400 text-gray-900 dark:text-gray-100 font-medium cursor-pointer appearance-none"
                      >
                        <option value="" className="text-gray-500">Select category...</option>
                        <option value="data-science">Data Science</option>
                        <option value="development">Development</option>
                        <option value="research">Research</option>
                        <option value="automation">Automation</option>
                        <option value="analytics">Analytics</option>
                        <option value="creative">Creative</option>
                        <option value="integration">Integration</option>
                        <option value="security">Security</option>
                      </select>
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-bold text-gray-800 dark:text-gray-200 mb-2.5">
                      Description <span className="text-red-500">*</span>
                    </label>
                    <textarea
                      value={skillConfig.description}
                      onChange={(e) => setSkillConfig(prev => ({...prev, description: e.target.value}))}
                      required
                      rows={3}
                      placeholder="Describe what this skill does, when to use it, and what inputs/outputs it expects..."
                      className="w-full px-4 py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-xl focus:outline-none focus:ring-2 focus:ring-violet-500/50 focus:border-violet-400 text-gray-900 dark:text-gray-100 resize-none transition-all placeholder:text-gray-400 dark:placeholder:text-gray-500"
                    />
                  </div>

                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {[
                      { key: 'namespace', label: 'Namespace', placeholder: 'demo' },
                      { key: 'version', label: 'Version', placeholder: '1.0.0' },
                      { key: 'visibility', label: 'Visibility', type: 'select', options: ['public', 'private', 'internal'] },
                      { key: 'license', label: 'License', type: 'select', options: ['MIT', 'Apache-2.0', 'GPL-3.0', 'BSD-3-Clause', 'Proprietary'] }
                    ].map((field) => (
                      <div key={field.key}>
                        <label className="block text-sm font-bold text-gray-800 dark:text-gray-200 mb-2">{field.label}</label>
                        {field.type === 'select' ? (
                          <select
                            value={skillConfig[field.key]}
                            onChange={(e) => setSkillConfig(prev => ({...prev, [field.key]: e.target.value}))}
                            className="w-full px-3 py-2.5 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-xl focus:outline-none focus:ring-2 focus:ring-violet-500/50 text-gray-900 dark:text-gray-100 text-sm font-medium cursor-pointer"
                          >
                            {field.options.map(opt => <option key={opt} value={opt} className="text-gray-900">{opt.charAt(0).toUpperCase() + opt.slice(1)}</option>)}
                          </select>
                        ) : (
                          <input
                            type="text"
                            value={skillConfig[field.key]}
                            onChange={(e) => setSkillConfig(prev => ({...prev, [field.key]: e.target.value}))}
                            placeholder={field.placeholder}
                            className="w-full px-3 py-2.5 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-xl focus:outline-none focus:ring-2 focus:ring-violet-500/50 text-gray-900 dark:text-gray-100 text-sm placeholder:text-gray-400 dark:placeholder:text-gray-500"
                          />
                        )}
                      </div>
                    ))}
                  </div>

                  {/* Tags Section */}
                  <div>
                    <label className="block text-sm font-bold text-gray-800 dark:text-gray-200 mb-2.5">
                      Tags
                    </label>
                    <div className="flex flex-wrap gap-2 mb-3 min-h-[36px] p-3 bg-gray-50 dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 focus-within:ring-2 focus-within:ring-violet-500/50 focus-within:border-violet-400 transition-all">
                      {skillConfig.tags.map((tag) => (
                        <span key={tag} className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-gradient-to-r from-violet-500 to-purple-500 text-white rounded-lg text-sm font-medium shadow-sm shadow-purple-500/20">
                          #{tag}
                          <button
                            type="button"
                            onClick={() => setSkillConfig(prev => ({
                              ...prev,
                              tags: prev.tags.filter(t => t !== tag)
                            }))}
                            className="hover:text-red-200 font-bold text-sm opacity-80 hover:opacity-100 transition-opacity"
                          >×</button>
                        </span>
                      ))}
                      <input
                        type="text"
                        value={tagInput}
                        onChange={(e) => setTagInput(e.target.value)}
                        onKeyPress={handleAddTag}
                        placeholder="Press Enter to add..."
                        className="flex-1 min-w-[150px] bg-transparent border-none outline-none text-gray-900 dark:text-gray-100 text-sm placeholder:text-gray-400 dark:placeholder:text-gray-500"
                      />
                    </div>
                    <p className="text-xs text-gray-500 dark:text-gray-400 ml-1">Add relevant tags to help others discover this skill</p>
                  </div>
                </div>

                {/* Navigation Buttons */}
                <div className="flex justify-end gap-3 pt-5 border-t border-gray-200 dark:border-gray-700">
                  <button onClick={() => setActiveStep(1)} className="px-6 py-2.5 bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-xl font-semibold transition-all text-gray-700 dark:text-gray-300">
                    ← Back
                  </button>
                  <button
                    onClick={handleGenerateSkill}
                    disabled={!skillConfig.name || !skillConfig.description || loading}
                    className="px-8 py-2.5 bg-gradient-to-r from-violet-600 via-purple-600 to-fuchsia-600 hover:from-violet-700 hover:to-fuchsia-700 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-xl font-semibold transition-all shadow-lg shadow-purple-500/25 hover:shadow-xl flex items-center gap-2"
                  >
                    {loading ? (
                      <><span className="animate-spin">⏳</span> Generating...</>
                    ) : (
                      <>⚡ Generate Skill →</>
                    )}
                  </button>
                </div>
              </div>
            )}

            {/* Step 3: Preview Generated Skill */}
            {activeStep === 3 && generatedSkill && (
              <div className="card p-7 space-y-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-gradient-to-r from-green-500 to-emerald-500 rounded-xl flex items-center justify-center text-white text-lg shadow-lg shadow-green-500/30">
                      ✓
                    </div>
                    <h3 className="text-xl font-bold text-gray-900 dark:text-white">Generated Skill Preview</h3>
                  </div>
                  <div className="flex gap-2 bg-gray-100 dark:bg-gray-800 p-1 rounded-xl">
                    <button
                      onClick={() => setPreviewMode('card')}
                      className={`px-4 py-2 text-sm rounded-lg transition-all font-semibold ${
                        previewMode === 'card' 
                          ? 'bg-white dark:bg-gray-700 text-violet-700 dark:text-violet-300 shadow-sm' 
                          : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
                      }`}
                    >
                      🎴 Card View
                    </button>
                    <button
                      onClick={() => setPreviewMode('raw')}
                      className={`px-4 py-2 text-sm rounded-lg transition-all font-semibold ${
                        previewMode === 'raw' 
                          ? 'bg-white dark:bg-gray-700 text-violet-700 dark:text-violet-300 shadow-sm' 
                          : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
                      }`}
                    >
                      {} Raw JSON
                    </button>
                  </div>
                </div>

                {previewMode === 'card' ? (
                  <div className="overflow-hidden rounded-2xl border border-gray-200 dark:border-gray-700 shadow-xl shadow-purple-500/5">
                    {/* Card Header */}
                    <div className="bg-gradient-to-r from-violet-600 via-purple-600 to-fuchsia-600 p-8 relative overflow-hidden">
                      <div className="absolute top-0 right-0 w-96 h-96 bg-white/5 rounded-full -translate-y-1/2 translate-x-1/3"></div>
                      <div className="absolute bottom-0 left-0 w-64 h-64 bg-black/10 rounded-full translate-y-1/2 -translate-x-1/3"></div>
                      
                      <div className="relative flex items-start gap-5">
                        <div className="w-20 h-20 bg-white/20 backdrop-blur-md rounded-2xl flex items-center justify-center text-4xl shadow-2xl border border-white/20">
                          🧠
                        </div>
                        <div className="flex-1 pt-1">
                          <h2 className="text-2xl font-bold text-white tracking-tight">{generatedSkill.skill_name || skillConfig.name}</h2>
                          <p className="text-white/70 mt-1 text-sm">Version {generatedSkill.version || skillConfig.version}</p>
                          <div className="flex gap-2 mt-4">
                            <span className="px-3 py-1 bg-white/20 backdrop-blur rounded-lg text-xs text-white font-semibold border border-white/15">
                              {selectedType.toUpperCase()}
                            </span>
                            <span className="px-3 py-1 bg-white/20 backdrop-blur rounded-lg text-xs text-white font-semibold border border-white/15">
                              {skillConfig.visibility.toUpperCase()}
                            </span>
                            <span className="px-3 py-1 bg-white/20 backdrop-blur rounded-lg text-xs text-white font-semibold border border-white/15">
                              {skillConfig.category?.toUpperCase() || 'UNCATEGORIZED'}
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    {/* Card Body */}
                    <div className="p-7 space-y-5 bg-white dark:bg-gray-900">
                      <div>
                        <div className="text-[11px] text-gray-500 dark:text-gray-400 uppercase tracking-widest font-bold mb-2">Description</div>
                        <p className="text-gray-800 dark:text-gray-200 leading-relaxed text-sm">{skillConfig.description}</p>
                      </div>

                      {generatedSkill.skill_definition && (
                        <div>
                          <div className="text-[11px] text-gray-500 dark:text-gray-400 uppercase tracking-widest font-bold mb-2">Skill Definition</div>
                          <pre className="text-xs bg-gray-50 dark:bg-gray-800 p-5 rounded-xl overflow-auto max-h-72 text-gray-800 dark:text-gray-200 border border-gray-200 dark:border-gray-700 font-mono leading-relaxed">
                            {typeof generatedSkill.skill_definition === 'string'
                              ? generatedSkill.skill_definition
                              : JSON.stringify(generatedSkill.skill_definition, null, 2)
                            }
                          </pre>
                        </div>
                      )}

                      {skillConfig.tags.length > 0 && (
                        <div className="flex flex-wrap gap-2 pt-3 border-t border-gray-200 dark:border-gray-700">
                          {skillConfig.tags.map((tag) => (
                            <span key={tag} className="px-3 py-1.5 bg-violet-100 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300 rounded-lg text-xs font-semibold border border-violet-200 dark:border-violet-800">
                              #{tag}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                ) : (
                  <div className="rounded-2xl border border-gray-200 dark:border-gray-700 overflow-hidden">
                    <div className="bg-gray-100 dark:bg-gray-800 px-4 py-2.5 border-b border-gray-200 dark:border-gray-700 flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full bg-red-500/70"></div>
                      <div className="w-3 h-3 rounded-full bg-yellow-500/70"></div>
                      <div className="w-3 h-3 rounded-full bg-green-500/70"></div>
                      <span className="ml-2 text-xs text-gray-500 dark:text-gray-400 font-mono">skill-output.json</span>
                    </div>
                    <pre className="text-xs bg-gray-100 dark:bg-gray-800 p-5 overflow-auto max-h-96 text-gray-800 dark:text-gray-200 font-mono leading-relaxed">
                      {JSON.stringify(generatedSkill, null, 2)}
                    </pre>
                  </div>
                )}

                <div className="flex justify-end gap-3 pt-5 border-t border-gray-200 dark:border-gray-700">
                  <button onClick={() => setActiveStep(2)} className="px-6 py-2.5 bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-xl font-semibold transition-all text-gray-700 dark:text-gray-300">
                    ✏️ Edit Configuration
                  </button>
                  <button
                    onClick={handlePublishToHub}
                    disabled={loading || evolutionReady}
                    className="px-8 py-2.5 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-xl font-semibold transition-all shadow-lg shadow-emerald-500/25 hover:shadow-xl flex items-center gap-2"
                  >
                    {evolutionReady ? '✓ Published!' : loading ? 'Publishing...' : '🚀 Publish to Skills Hub'}
                  </button>
                </div>
              </div>
            )}

            {/* Step 4: Success State */}
            {activeStep === 4 && (
              <div className="card p-16 text-center space-y-6 relative overflow-hidden">
                <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-violet-50 via-purple-50 to-fuchsia-50 dark:from-violet-950/20 dark:via-purple-950/20 dark:to-fuchsia-950/20"></div>
                <div className="absolute top-10 left-10 w-32 h-32 bg-violet-200/40 dark:bg-violet-800/20 rounded-full blur-3xl"></div>
                <div className="absolute bottom-10 right-10 w-40 h-40 bg-fuchsia-200/40 dark:bg-fuchsia-800/20 rounded-full blur-3xl"></div>
                
                <div className="relative">
                  <div className="inline-block relative">
                    <div className="text-8xl animate-bounce">🎉</div>
                    <div className="absolute -top-2 -right-2 w-10 h-10 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full flex items-center justify-center text-white text-lg font-bold animate-pulse shadow-lg shadow-green-500/40">
                      ✓
                    </div>
                  </div>
                  
                  <h3 className="text-3xl font-bold text-gray-900 dark:text-white mt-6 mb-3">
                    Skill Created Successfully!
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400 max-w-lg mx-auto text-lg leading-relaxed">
                    Your skill <span className="text-violet-600 dark:text-violet-400 font-bold">{skillConfig.name}</span> has been published to the Skills Hub and is ready for evolution.
                  </p>
                  
                  <div className="flex justify-center gap-4 pt-6">
                    <Link to="/skills-hub-pro" className="group px-6 py-3 bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-xl font-semibold transition-all text-gray-700 dark:text-gray-300 flex items-center gap-2">
                      📦 View in Hub
                      <span className="group-hover:translate-x-1 transition-transform">→</span>
                    </Link>
                    <button onClick={handleStartEvolution} className="px-6 py-3 bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-700 hover:to-purple-700 text-white rounded-xl font-semibold transition-all shadow-lg shadow-purple-500/25 hover:shadow-xl flex items-center gap-2">
                      🧬 Start Evolution
                    </button>
                    <button onClick={() => {
                      setActiveStep(1)
                      setGeneratedSkill(null)
                      setEvolutionReady(false)
                      setContent('')
                      setFileName('')
                      setAnalysisResult(null)
                      setSkillConfig({
                        name: '', description: '', namespace: 'demo', visibility: 'public',
                        version: '1.0.0', author: 'demo', category: '', tags: [], keywords: []
                      })
                    }} className="px-6 py-3 bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-xl font-semibold transition-all text-gray-700 dark:text-gray-300">
                      + Create Another
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Sidebar */}
          <div className="space-y-5">
            
            {/* Live Statistics */}
            <div className="card p-6 bg-gradient-to-br from-violet-50 via-purple-50 to-fuchsia-50 dark:from-violet-950/20 dark:via-purple-950/20 dark:to-fuchsia-950/20 border border-violet-200/40 dark:border-violet-800/30 relative overflow-hidden">
              <div className="absolute top-0 right-0 w-24 h-24 bg-gradient-to-bl from-purple-300/30 to-transparent rounded-full blur-2xl"></div>
              <h4 className="font-bold text-gray-900 dark:text-white mb-5 flex items-center gap-3 relative z-10">
                <span className="text-xl">📊</span> 
                <span className="bg-gradient-to-r from-violet-600 to-fuchsia-600 bg-clip-text text-transparent font-black dark:font-white">Live Statistics</span>
              </h4>
              <div className="space-y-3.5 relative z-10">
                {[
                  { label: 'Characters', value: content.length.toLocaleString(), icon: '📝', color: 'from-blue-500 to-cyan-500' },
                  { label: 'Words', value: content.split(/\s+/).filter(w => w).length.toLocaleString(), icon: '📃', color: 'from-violet-500 to-purple-500' },
                  { label: 'Lines', value: content.split('\n').length.toLocaleString(), icon: '📏', color: 'from-emerald-500 to-teal-500' },
                  { label: 'Tags', value: skillConfig.tags.length.toString(), icon: '🏷️', color: 'from-amber-500 to-orange-500' },
                  { label: 'Current Step', value: `${activeStep}/4`, icon: '📍', color: 'from-pink-500 to-rose-500' },
                ].map((stat, idx) => (
                  <div key={idx} className="flex items-center justify-between p-3.5 bg-white/80 dark:bg-black/25 rounded-xl border border-white/50 dark:border-gray-700/40 hover:bg-white dark:hover:bg-black/35 hover:shadow-lg transition-all group">
                    <div className="flex items-center gap-3">
                      <div className={`w-9 h-9 bg-gradient-to-br ${stat.color} rounded-xl flex items-center justify-center text-base shadow-md group-hover:scale-110 group-hover:rotate-3 transition-all duration-300`}>
                        {stat.icon}
                      </div>
                      <span className="text-sm font-bold text-gray-800 dark:text-gray-200">{stat.label}</span>
                    </div>
                    <span className="font-mono font-extrabold text-gray-900 dark:text-white text-sm bg-gradient-to-r from-gray-100 to-gray-200 dark:from-gray-700 dark:to-gray-600 px-3 py-1.5 rounded-lg shadow-sm">{stat.value}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Quick Tips */}
            <div className="card p-6 bg-gradient-to-br from-amber-50 via-yellow-50 to-orange-50 dark:from-amber-950/20 dark:via-yellow-950/20 dark:to-orange-950/20 border border-amber-200/40 dark:border-amber-800/30 relative overflow-hidden">
              <div className="absolute top-0 right-0 w-24 h-24 bg-gradient-to-bl from-yellow-300/30 to-transparent rounded-full blur-2xl"></div>
              <h4 className="font-bold text-gray-900 dark:text-white mb-5 flex items-center gap-3 relative z-10">
                <span className="text-xl">💡</span>
                <span className="bg-gradient-to-r from-amber-600 to-orange-600 bg-clip-text text-transparent font-black dark:font-white">Quick Tips</span>
              </h4>
              <ul className="space-y-3.5 relative z-10 text-sm text-gray-700 dark:text-gray-300 font-medium">
                {[
                  { icon: '🎯', text: 'Support for 10+ input formats including code, media, and APIs' },
                  { icon: '🤖', text: 'AI-powered automatic content analysis and quality scoring' },
                  { icon: '🗣️', text: 'Natural language skill description supported' },
                  { icon: '🧬', text: 'Published skills can be evolved automatically' },
                  { icon: '🔄', text: 'Drag & drop files directly into the editor' },
                ].map((tip, idx) => (
                  <li key={idx} className="flex items-start gap-3 p-3.5 bg-white/70 dark:bg-black/25 rounded-xl hover:bg-white dark:hover:bg-black/35 hover:shadow-lg transition-all group -mx-1">
                    <div className={`w-8 h-8 bg-gradient-to-br ${['from-red-500 to-rose-500', 'from-blue-500 to-cyan-500', 'from-emerald-500 to-teal-500', 'from-violet-500 to-purple-500', 'from-pink-500 to-fuchsia-500'][idx]} rounded-lg flex items-center justify-center text-base shadow-md group-hover:scale-110 group-hover:rotate-6 transition-all duration-300 shrink-0 mt-0.5`}>
                      {tip.icon}
                    </div>
                    <span className="leading-relaxed font-semibold">{tip.text}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Recent Skills */}
            {recentSkills.length > 0 && (
              <div className="card p-6 bg-gradient-to-br from-blue-50 via-indigo-50 to-cyan-50 dark:from-blue-950/20 dark:via-indigo-950/20 dark:to-cyan-950/20 border border-blue-200/40 dark:border-blue-800/30 relative overflow-hidden">
                <div className="absolute top-0 right-0 w-24 h-24 bg-gradient-to-bl from-cyan-300/30 to-transparent rounded-full blur-2xl"></div>
                <h4 className="font-bold text-gray-900 dark:text-white mb-5 flex items-center gap-3 relative z-10">
                  <span className="text-xl">🕐</span>
                  <span className="bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent font-black dark:font-white">Recent Skills</span>
                </h4>
                <div className="space-y-3 relative z-10">
                  {recentSkills.slice(0, 5).map((repo, idx) => (
                    <Link
                      key={idx}
                      to={`/skills-hub/${repo.repo_id || repo.id}`}
                      className="group block p-3.5 bg-white/80 dark:bg-black/25 rounded-xl hover:bg-white dark:hover:bg-black/35 hover:shadow-lg transition-all border border-transparent hover:border-violet-300 dark:hover:border-violet-700"
                    >
                      <div className="flex items-center gap-3">
                        <div className={`w-8 h-8 bg-gradient-to-br ${['from-emerald-500 to-teal-500', 'from-violet-500 to-purple-500', 'from-pink-500 to-rose-500', 'from-amber-500 to-orange-500', 'from-blue-500 to-cyan-500'][idx % 5]} rounded-lg flex items-center justify-center text-base shadow-md group-hover:scale-110 group-hover:rotate-6 transition-all duration-300 shrink-0`}>
                          📦
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="font-bold text-gray-800 dark:text-gray-200 text-sm truncate group-hover:text-violet-600 dark:group-hover:text-violet-400 transition-colors">{repo.name}</div>
                          <div className="text-xs text-gray-600 dark:text-gray-400 flex items-center gap-2 mt-1 font-medium">
                            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 shadow-sm shadow-emerald-500/50"></span>
                            {repo.visibility || 'public'}
                          </div>
                        </div>
                      </div>
                    </Link>
                  ))}
                </div>
              </div>
            )}

            {/* Next Step CTA */}
            <div className="card p-6 bg-gradient-to-br from-violet-600 via-purple-600 to-fuchsia-600 text-white relative overflow-hidden shadow-xl shadow-purple-500/20">
              <div className="absolute top-0 right-0 w-40 h-40 bg-white/10 rounded-full -translate-y-1/2 translate-x-1/3"></div>
              <div className="absolute bottom-0 left-0 w-28 h-28 bg-black/10 rounded-full translate-y-1/2 -translate-x-1/3"></div>
              <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-white/5 rounded-full blur-3xl"></div>

              <div className="relative z-10">
                <h4 className="font-black text-lg mb-3 flex items-center gap-3">
                  <span className="w-10 h-10 bg-white/20 backdrop-blur-md rounded-xl flex items-center justify-center text-lg shadow-lg border border-white/20">🧬</span>
                  <span className="bg-gradient-to-r from-white to-white/80 bg-clip-text text-transparent">Next Step</span>
                </h4>
                <p className="text-sm text-white/90 mb-5 leading-relaxed font-medium pl-[52px]">
                  After creating your skill, use the AI Evolution Workbench to optimize its performance through self-evolution.
                </p>
                <Link to="/evolution-workbench" className="block w-full text-center px-5 py-3.5 bg-white/25 hover:bg-white/35 backdrop-blur-md rounded-xl text-sm font-bold transition-all border border-white/30 hover:border-white/50 shadow-lg hover:shadow-xl hover:-translate-y-0.5 transform">
                  Open AI Evolution →
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default SkillCreatorStudio
