import React, { useState } from 'react'
import { Link } from 'react-router-dom'

const translations = {
  en: {
    heroSubtitle: 'The Infinite Evolution Intelligence Engine for AI Agents',
    heroDescription: 'An AI Agent Platform featuring Skill Creator, Skill Evolution, Skills Hub, OctoTrace, Skill Wiki, and AutoSkill — empowering AI agents to learn, adapt, evolve, and accumulate knowledge continuously.',
    launchAgent: 'Launch Agent',
    coreCapabilities: 'Core Capabilities',
    sixPillars: 'Six Pillars of Intelligence',
    skillCreator: 'Skill Creator',
    skillCreatorTitle: 'Skill Creator',
    skillCreatorDesc: 'Transform any content into AI agent skills — code, documents, media, APIs, or natural language descriptions. Intelligent analysis with automatic quality scoring.',
    evolution: 'Evolution',
    evolutionTitle: 'Skill Evolution',
    evolutionDesc: 'Advanced self-evolution engine with Feedback Descent algorithm. Optimize skills through pairwise comparison, frontier management, and continuous improvement.',
    skillsHub: 'Skills Hub',
    skillsHubTitle: 'Skills Hub',
    skillsHubDesc: 'The intelligent skill ecosystem for AI agents. Create, manage, collaborate, and evolve your skills with version control and seamless integration.',
    octoTrace: 'OctoTrace',
    octoTraceTitle: 'OctoTrace Dashboard',
    octoTraceDesc: 'Real-time visualization tracking for all AI operations. Span tree view, cost analytics, budget monitoring, token usage tracking across all modules.',
    autoSkill: 'AutoSkill',
    autoSkillTitle: 'AutoSkill',
    autoSkillDesc: 'Autonomous AI research system that experiments iteratively. Let AI agents conduct research while you sleep — modifying code, training models, evaluating results, and evolving approaches.',
    skillWiki: 'Skill Wiki',
    skillWikiTitle: 'Skill Wiki Knowledge Base',
    aiWikiDesc: 'Incremental knowledge management system with three-layer architecture. Transform documents into structured, interlinked intelligence with LLM-powered ingestion, intelligent querying, and quality assurance.',
    howOctopaiEvolves: 'How Octopai Evolves',
    dataIngestion: 'Data Ingestion',
    dataIngestionDesc: 'Collects execution data, user feedback, performance metrics, and environmental signals from every interaction.',
    patternAnalysis: 'Pattern Analysis',
    patternAnalysisDesc: 'Identifies patterns, detects inefficiencies, discovers optimization opportunities, and maps improvement pathways through Feedback Descent.',
    selfOptimization: 'Self-Optimization',
    selfOptimizationDesc: 'Implements improvements autonomously using pairwise comparison optimization. Updates parameters, refines strategies, and evolves Skills without human intervention.',
    validationDeploy: 'Validation & Deploy',
    validationDeployDesc: 'Validates changes in sandbox, ensures stability, manages version control, and deploys updated versions with rollback-ready safety.',
    visibilityInsight: 'Visibility & Insight',
    visibilityInsightDesc: 'Full-stack observability with OctoTrace. Real-time span trees, cost tracking, performance analytics, and token monitoring for every operation.',
    skillsEcosystem: 'Skills Ecosystem',
    browseSkillsHub: 'Browse the Skills Hub',
    skillsHubDescription: 'A GitHub-style repository system for AI agent skills. Browse, create, fork, collaborate, and publish skill packs with full version control.',
    browseAllSkills: 'Browse All Skills',
    autonomousResearch: 'Autonomous AI Research & Scientific Discovery',
    autoResearchDescription: 'Empower AI agents to conduct autonomous research and scientific discovery through iterative experimentation. Automatically modifies code, trains models, evaluates results, and evolves approaches — accelerating innovation while you focus on high-value decisions.',
    perExperiment: 'Per Experiment',
    experimentsPerHour: 'Experiments/Hour',
    overnightRuns: 'Overnight Runs',
    autonomyLoop: 'Autonomy Loop',
    exploreAutoResearch: 'Explore AutoResearch',
    product: 'Product',
    aiAgent: 'AI Agent',
    resources: 'Resources',
    documentation: 'Documentation',
    research: 'Research',
    examples: 'Examples',
    tutorials: 'Tutorials',
    community: 'Community',
    github: 'GitHub',
    discord: 'Discord',
    twitter: 'Twitter',
    blog: 'Blog',
    company: 'Company',
    about: 'About',
    careers: 'Careers',
    privacy: 'Privacy',
    terms: 'Terms',
    brandDescription: 'The Infinite Evolution Intelligence Engine for AI Agents',
    copyright: '© 2026 Octopai. All rights reserved.',
    webResearchAgent: 'Web Research Agent',
    documentParserPro: 'Document Parser Pro',
    codeGenerator: 'Code Generator',
    dataAnalyst: 'Data Analyst',
    contentCreator: 'Content Creator',
    apiIntegrator: 'API Integrator',
    skillCreatorStudio: 'Skill Creator Studio',
    evolutionWorkbench: 'Evolution Workbench',
    skillsHubPro: 'Skills Hub',
    octoTraceDashboard: 'OctoTrace Dashboard',
    researchCategory: 'Research',
    parsingCategory: 'Parsing',
    developmentCategory: 'Development',
    analyticsCategory: 'Analytics',
    creativeCategory: 'Creative',
    integrationCategory: 'Integration',
    webResearchAgentDesc: 'Autonomous web research and information synthesis.',
    documentParserProDesc: 'Multi-format document extraction and processing.',
    codeGeneratorDesc: 'Intelligent code generation with multi-language support.',
    dataAnalystDesc: 'Statistical analysis and visualization generation.',
    contentCreatorDesc: 'Multi-format content generation and optimization.',
    apiIntegratorDesc: 'Seamless API connection builder with error recovery.',
    skillCreatorDesc: 'Create skills from any input type with intelligent analysis.',
    skillEvolutionDesc: 'Self-evolve skills using Feedback Descent optimization.',
    skillsHubDesc: 'Manage skills in GitHub-style repositories.',
    octoTraceDesc: 'Visualize and track all AI operations in real-time.',
    techArchitecture: 'Enterprise-Grade Architecture',
    persistence: 'Persistent Storage',
    persistenceDesc: 'SQLite database with 12 tables and 18 indexes. WAL mode for high concurrency. Multi-tenant data isolation with full transactional integrity.',
    llmIntegration: 'LLM Integration',
    llmIntegrationDesc: 'Native OpenAI/Claude support with automatic failover. Two-step chain-of-thought ingestion, four-phase query retrieval, and comprehensive quality assurance.',
    realtime: 'Real-Time Communication',
    realtimeDesc: 'WebSocket-powered live updates replacing polling. 15 event types for instant trace notifications, cost alerts, and operation progress.',
    authSystem: 'Authentication & RBAC',
    authSystemDesc: 'JWT-based multi-role system (admin/editor/viewer/researcher). 11 permission categories, API key management, and session tracking.',
    exportSystem: 'Multi-Format Export',
    exportSystemDesc: 'Export to Markdown, PDF, JSON, CSV, or HTML. Async job processing with progress tracking. Batch operations and custom templates.',
    versionControl: 'Version Control System',
    versionControlDesc: 'Complete wiki page history with line-by-line diff comparison. One-click rollback, change attribution, and growth analytics.',
    platformStats: 'Platform Statistics',
    totalModules: '6 Core Modules',
    totalModulesDesc: 'Integrated AI agent platform',
    apiEndpoints: '26+ API Endpoints',
    apiEndpointsDesc: 'Comprehensive RESTful API',
    codebaseSize: '6,000+ Lines',
    codebaseSizeDesc: 'Production-ready codebase',
    supportedFormats: '5 Export Formats',
    supportedFormatsDesc: 'MD/PDF/JSON/CSV/HTML'
  },
  zh: {
    heroSubtitle: 'AI Agent的无限进化智能引擎',
    heroDescription: '一个具有Skill Creator、Skill Evolution、Skills Hub、OctoTrace、Skill Wiki和AutoSkill的无限进化AI Agent平台——赋能AI Agent持续学习、适应、进化和积累知识。',
    launchAgent: '启动Agent',
    coreCapabilities: '核心能力',
    sixPillars: '六大核心能力',
    skillCreator: '技能创建',
    skillCreatorTitle: 'Skill Creator',
    skillCreatorDesc: '将任何内容转化为AI Agent技能——代码、文档、媒体、API或自然语言描述。智能分析自动质量评分。',
    evolution: '进化',
    evolutionTitle: 'Skill Evolution',
    evolutionDesc: '高级自进化引擎，采用Feedback Descent算法。通过成对比较、前沿管理和持续优化来改进技能。',
    skillsHub: 'Skills Hub',
    skillsHubTitle: 'Skills Hub',
    skillsHubDesc: 'AI Agent智能技能生态系统 — 创建、管理、协作和进化您的技能，支持版本控制和无缝集成',
    octoTrace: 'OctoTrace',
    octoTraceTitle: 'OctoTrace Dashboard',
    octoTraceDesc: '所有AI操作的实时可视化追踪。Span树视图、成本分析、预算监控、跨模块Token使用追踪。',
    autoSkill: 'AutoSkill',
    autoSkillTitle: 'AutoSkill',
    autoSkillDesc: '自主AI研究系统，进行迭代式实验。让AI Agent在您睡觉时进行研究——修改代码、训练模型、评估结果并进化方法。',
    skillWiki: 'Skill Wiki',
    skillWikiTitle: 'Skill Wiki 知识库',
    skillWikiDesc: '增量式知识管理系统，采用三层架构。通过LLM驱动的导入、智能查询和质量保证，将文档转化为结构化、相互关联的智能知识。',
    evolution: '进化',
    howOctopaiEvolves: 'Octopai如何进化',
    dataIngestion: '数据摄入',
    dataIngestionDesc: '从每一次交互中收集执行数据、用户反馈、性能指标和环境信号。',
    patternAnalysis: '模式分析',
    patternAnalysisDesc: '识别模式、检测低效、发现优化机会并通过Feedback Descent映射改进路径。',
    selfOptimization: '自我优化',
    selfOptimizationDesc: '使用成对比较优化自主实施改进。更新参数、优化策略并在无需人工干预的情况下进化技能。',
    validationDeploy: '验证与部署',
    validationDeployDesc: '在沙箱中验证更改、确保稳定性、管理版本控制并通过回滚式安全机制部署更新版本。',
    visibilityInsight: '可见性与洞察',
    visibilityInsightDesc: 'OctoTrace全栈可观测性。实时Span树、成本追踪、性能分析和每次操作的Token监控。',
    skillsEcosystem: '技能生态系统',
    browseSkillsHub: '浏览Skills Hub',
    skillsHubDescription: 'GitHub风格的AI Agent技能仓库系统。浏览、创建、Fork、协作并发布具有完整版本控制的技能包。',
    browseAllSkills: '浏览所有技能',
    autonomousResearch: 'AI自动化研究与科学发现',
    autoResearchDescription: '赋能AI Agent通过迭代实验进行自主研究与科学发现。自动修改代码、训练模型、评估结果并演进方法 — 在您专注高价值决策的同时加速创新。',
    perExperiment: '每次实验',
    experimentsPerHour: '实验/小时',
    overnightRuns: '夜间运行',
    autonomyLoop: '自主循环',
    exploreAutoResearch: '探索AutoResearch',
    fivePillars: '五大核心能力',
    product: '产品',
    aiAgent: 'AI Agent',
    resources: '资源',
    documentation: '文档',
    research: '研究',
    examples: '示例',
    tutorials: '教程',
    community: '社区',
    github: 'GitHub',
    discord: 'Discord',
    twitter: 'Twitter',
    blog: '博客',
    company: '公司',
    about: '关于',
    careers: '招聘',
    privacy: '隐私',
    terms: '条款',
    brandDescription: 'AI Agent的无限进化智能引擎',
    copyright: '© 2026 Octopai。保留所有权利。',
    webResearchAgent: '网络研究Agent',
    documentParserPro: '文档解析专家',
    codeGenerator: '代码生成器',
    dataAnalyst: '数据分析器',
    contentCreator: '内容创作者',
    apiIntegrator: 'API集成器',
    skillCreatorStudio: 'Skill Creator Studio',
    evolutionWorkbench: 'Evolution Workbench',
    skillsHubPro: 'Skills Hub',
    octoTraceDashboard: 'OctoTrace Dashboard',
    researchCategory: '研究',
    parsingCategory: '解析',
    developmentCategory: '开发',
    analyticsCategory: '分析',
    creativeCategory: '创意',
    integrationCategory: '集成',
    webResearchAgentDesc: '自主网络研究和信息合成。',
    documentParserProDesc: '多格式文档提取和处理。',
    codeGeneratorDesc: '支持多语言的智能代码生成。',
    dataAnalystDesc: '统计分析和可视化生成。',
    contentCreatorDesc: '多格式内容生成和优化。',
    apiIntegratorDesc: '具有错误恢复功能的无缝API连接构建器。',
    skillCreatorStudioDesc: '从任何输入类型创建技能，具备智能分析功能。',
    evolutionWorkbenchDesc: '使用Feedback Descent优化实现技能自进化。',
    skillsHubProDesc: '在GitHub风格仓库中管理技能。',
    octoTraceDashboardDesc: '实时可视化和追踪所有AI操作。',
  }
}

const Home = () => {
  const [language, setLanguage] = useState('en')
  const t = translations[language]

  const skills = [
    { name: t.webResearchAgent, category: t.researchCategory, desc: t.webResearchAgentDesc, icon: '🔍' },
    { name: t.documentParserPro, category: t.parsingCategory, desc: t.documentParserProDesc, icon: '📄' },
    { name: t.codeGenerator, category: t.developmentCategory, desc: t.codeGeneratorDesc, icon: '💻' },
    { name: t.dataAnalyst, category: t.analyticsCategory, desc: t.dataAnalystDesc, icon: '📊' },
    { name: t.contentCreator, category: t.creativeCategory, desc: t.contentCreatorDesc, icon: '✍️' },
    { name: t.apiIntegrator, category: t.integrationCategory, desc: t.apiIntegratorDesc, icon: '🔌' },
    { name: t.skillCreator, category: t.developmentCategory, desc: t.skillCreatorDesc, icon: '⚡' },
    { name: t.skillEvolution, category: t.researchCategory, desc: t.skillEvolutionDesc, icon: '🧬' },
    { name: t.skillsHub, category: t.integrationCategory, desc: t.skillsHubDesc, icon: '📦' },
    { name: t.octoTrace, category: t.analyticsCategory, desc: t.octoTraceDesc, icon: '🔎' }
  ]

  return (
    <div className="min-h-screen relative" style={{ background: 'var(--octo-bg-page)' }}>
      {/* Clean Background - Stars only, no vertical lines! */}
      <div className="stars" aria-hidden="true"></div>
      <div className="stars2" aria-hidden="true"></div>
      <div className="stars3" aria-hidden="true"></div>
      
      {/* Tech Particles */}
      <div className="tech-particles" aria-hidden="true">
        {[...Array(20)].map((_, i) => (
          <div 
            key={i} 
            className="tech-particle" 
            style={{ 
              left: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 15}s`,
              animationDuration: `${15 + Math.random() * 10}s`,
              opacity: Math.random() * 0.5 + 0.3
            }}
          />
        ))}
      </div>

      {/* HERO SECTION - Enhanced with Visual Impact */}
      <section className="hero-section fade-in-up" style={{ position: 'relative', overflow: 'hidden' }}>
        {/* Animated gradient orbs */}
        <div style={{ 
          position: 'absolute', top: '-10%', left: '-5%', width: '400px', height: '400px',
          background: 'radial-gradient(circle, rgba(245, 158, 11, 0.15) 0%, transparent 70%)',
          borderRadius: '50%', filter: 'blur(60px)', animation: 'float 8s ease-in-out infinite'
        }} />
        <div style={{ 
          position: 'absolute', bottom: '-15%', right: '-10%', width: '500px', height: '500px',
          background: 'radial-gradient(circle, rgba(59, 130, 246, 0.12) 0%, transparent 70%)',
          borderRadius: '50%', filter: 'blur(80px)', animation: 'float 12s ease-in-out infinite reverse'
        }} />
        
        <div style={{ position: 'relative', zIndex: 1 }}>
          <h1 className="tech-float">
            Octopai
          </h1>
          
          <p className="gradient-text" style={{ fontSize: '1.9rem', marginBottom: '20px', fontWeight: 600, letterSpacing: '-0.02em', maxWidth: '900px', margin: '0 auto 24px' }}>
            {t.heroSubtitle}
          </p>
          
          <p style={{ 
            fontSize: '1.05rem', lineHeight: '1.6', maxWidth: '1000px', margin: '0 auto 36px', 
            color: 'var(--octo-text-secondary)', opacity: 0.95
          }}>
            {t.heroDescription}
          </p>
          
          <div className="hero-actions" style={{ display: 'flex', gap: '16px', justifyContent: 'center', flexWrap: 'wrap', alignItems: 'center' }}>
            <Link to="/agent" className="btn-primary tech-pulse-glow" style={{ color: '#ffffff', padding: '16px 36px', fontSize: '1.05rem' }}>
              {t.launchAgent}
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M5 12h14M12 5l7 7-7 7"/>
              </svg>
            </Link>
            
            <Link to="/skill-wiki" className="btn-secondary" style={{ 
                padding: '16px 36px', fontSize: '1.05rem', borderColor: 'rgba(245, 158, 11, 0.5)',
                background: 'rgba(245, 158, 11, 0.08)', backdropFilter: 'blur(8px)'
              }}>
                📚 Explore Skill Wiki
            </Link>
            
            <a href="#capabilities" style={{
              display: 'inline-flex', alignItems: 'center', gap: '6px', color: 'var(--octo-text-secondary)',
              textDecoration: 'none', fontSize: '0.95rem', transition: 'all 0.3s ease'
            }}
            onMouseEnter={(e) => e.currentTarget.style.color = 'var(--octo-text-primary)'}
            onMouseLeave={(e) => e.currentTarget.style.color = 'var(--octo-text-secondary)'}>
              Learn More ↓
            </a>
          </div>

          {/* Quick Stats Bar */}
          <div style={{ 
            marginTop: '56px', display: 'flex', justifyContent: 'center', gap: '48px', flexWrap: 'wrap',
            padding: '28px 40px', background: 'rgba(255, 255, 255, 0.03)', borderRadius: '16px',
            border: '1px solid var(--octo-border-color)', backdropFilter: 'blur(10px)'
          }}>
            {[
              { value: '6', label: 'Core Modules', icon: '🎯' },
              { value: '26+', label: 'API Endpoints', icon: '🔌' },
              { value: '6K+', label: 'Lines of Code', icon: '💻' },
              { value: '∞', label: 'Evolution Potential', icon: '🧬' }
            ].map((stat, idx) => (
              <div key={idx} style={{ textAlign: 'center', minWidth: '100px' }}>
                <div style={{ fontSize: '2rem', fontWeight: 900, background: 'linear-gradient(135deg, #f59e0b 0%, #f97316 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text' }}>
                  {stat.value}
                </div>
                <div style={{ fontSize: '0.85rem', color: '#9ca3af', marginTop: '4px' }}>{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <hr className="section-divider"/>

      {/* FIVE CORE CAPABILITIES */}
      <section className="section-container">
        <div className="section-label">{t.coreCapabilities}</div>
        <h2 className="section-heading">{t.sixPillars}</h2>
        
        <div className="card-grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))' }}>
          {/* Skill Creator Studio */}
          <Link to="/skill-creator" style={{ textDecoration: 'none' }}>
            <div 
              className="card card-whisper" 
              style={{ 
                cursor: 'pointer', height: '100%', transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
                position: 'relative', overflow: 'hidden'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-8px) scale(1.02)'
                e.currentTarget.style.boxShadow = '0 20px 60px rgba(245, 158, 11, 0.2)'
                e.currentTarget.style.borderColor = 'rgba(245, 158, 11, 0.4)'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0) scale(1)'
                e.currentTarget.style.boxShadow = ''
                e.currentTarget.style.borderColor = ''
              }}
            >
              <div className="card-label">{t.skillCreator}</div>
              <div className="feature-icon" style={{ fontSize: '2rem' }}>⚡</div>
              <h3>{t.skillCreatorTitle}</h3>
              <p>{t.skillCreatorDesc}</p>
              <div style={{ 
                marginTop: '16px', paddingTop: '16px', borderTop: '1px solid var(--octo-border-color)',
                display: 'flex', gap: '8px', flexWrap: 'wrap'
              }}>
                <span style={{ fontSize: '0.75rem', padding: '4px 10px', borderRadius: '12px', background: 'rgba(59, 130, 246, 0.1)', color: '#3b82f6', fontWeight: '600' }}>Code → Skills</span>
                <span style={{ fontSize: '0.75rem', padding: '4px 10px', borderRadius: '12px', background: 'rgba(168, 85, 247, 0.1)', color: '#a855f7', fontWeight: '600' }}>Quality Scoring</span>
              </div>
            </div>
          </Link>

          {/* Skill Evolution */}
          <Link to="/skill-evolution" style={{ textDecoration: 'none' }}>
            <div 
              className="card card-whisper"
              style={{ cursor: 'pointer', height: '100%', transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)' }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-8px) scale(1.02)'
                e.currentTarget.style.boxShadow = '0 20px 60px rgba(139, 92, 246, 0.2)'
                e.currentTarget.style.borderColor = 'rgba(139, 92, 246, 0.4)'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0) scale(1)'
                e.currentTarget.style.boxShadow = ''
                e.currentTarget.style.borderColor = ''
              }}
            >
              <div className="card-label">{t.evolution}</div>
              <div className="feature-icon" style={{ fontSize: '2rem' }}>🧬</div>
              <h3>{t.evolutionTitle}</h3>
              <p>{t.evolutionDesc}</p>
              <div style={{ marginTop: '16px', paddingTop: '16px', borderTop: '1px solid var(--octo-border-color)', display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                <span style={{ fontSize: '0.75rem', padding: '4px 10px', borderRadius: '12px', background: 'rgba(16, 185, 129, 0.1)', color: '#10b981', fontWeight: '600' }}>Feedback Descent</span>
                <span style={{ fontSize: '0.75rem', padding: '4px 10px', borderRadius: '12px', background: 'rgba(236, 72, 153, 0.1)', color: '#ec4899', fontWeight: '600' }}>Self-Optimize</span>
              </div>
            </div>
          </Link>

          {/* Skills Hub */}
          <Link to="/skills-hub" style={{ textDecoration: 'none' }}>
            <div 
              className="card card-whisper"
              style={{ cursor: 'pointer', height: '100%', transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)' }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-8px) scale(1.02)'
                e.currentTarget.style.boxShadow = '0 20px 60px rgba(16, 185, 129, 0.2)'
                e.currentTarget.style.borderColor = 'rgba(16, 185, 129, 0.4)'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0) scale(1)'
                e.currentTarget.style.boxShadow = ''
                e.currentTarget.style.borderColor = ''
              }}
            >
              <div className="card-label">{t.skillsHub}</div>
              <div className="feature-icon" style={{ fontSize: '2rem' }}>📦</div>
              <h3>{t.skillsHubTitle}</h3>
              <p>{t.skillsHubDesc}</p>
              <div style={{ marginTop: '16px', paddingTop: '16px', borderTop: '1px solid var(--octo-border-color)', display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                <span style={{ fontSize: '0.75rem', padding: '4px 10px', borderRadius: '12px', background: 'rgba(6, 182, 212, 0.1)', color: '#0891b2', fontWeight: '600' }}>Version Control</span>
                <span style={{ fontSize: '0.75rem', padding: '4px 10px', borderRadius: '12px', background: 'rgba(245, 158, 11, 0.1)', color: '#d97706', fontWeight: '600' }}>Collaboration</span>
              </div>
            </div>
          </Link>

          {/* OctoTrace Dashboard */}
          <Link to="/octo-trace" style={{ textDecoration: 'none' }}>
            <div 
              className="card card-whisper"
              style={{ cursor: 'pointer', height: '100%', transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)' }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-8px) scale(1.02)'
                e.currentTarget.style.boxShadow = '0 20px 60px rgba(59, 130, 246, 0.2)'
                e.currentTarget.style.borderColor = 'rgba(59, 130, 246, 0.4)'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0) scale(1)'
                e.currentTarget.style.boxShadow = ''
                e.currentTarget.style.borderColor = ''
              }}
            >
              <div className="card-label">{t.octoTrace}</div>
              <div className="feature-icon" style={{ fontSize: '2rem' }}>🔍</div>
              <h3>{t.octoTraceTitle}</h3>
              <p>{t.octoTraceDesc}</p>
              <div style={{ marginTop: '16px', paddingTop: '16px', borderTop: '1px solid var(--octo-border-color)', display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                <span style={{ fontSize: '0.75rem', padding: '4px 10px', borderRadius: '12px', background: 'rgba(239, 68, 68, 0.1)', color: '#dc2626', fontWeight: '600' }}>Span Tree</span>
                <span style={{ fontSize: '0.75rem', padding: '4px 10px', borderRadius: '12px', background: 'rgba(34, 197, 94, 0.1)', color: '#16a34a', fontWeight: '600' }}>Cost Analytics</span>
              </div>
            </div>
          </Link>

          {/* Skill Wiki - NEW MODULE */}
          <Link to="/skill-wiki" style={{ textDecoration: 'none' }}>
            <div 
              className="card card-whisper" 
              style={{ 
                cursor: 'pointer', height: '100%', 
                transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
                position: 'relative'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-8px) scale(1.02)'
                e.currentTarget.style.boxShadow = '0 20px 60px rgba(245, 158, 11, 0.2)'
                e.currentTarget.style.borderColor = 'rgba(245, 158, 11, 0.4)'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0) scale(1)'
                e.currentTarget.style.boxShadow = ''
                e.currentTarget.style.borderColor = ''
              }}
            >
              <div className="card-label">{t.skillWiki}</div>
              <div className="feature-icon" style={{ fontSize: '2rem' }}>📚</div>
              <h3>{t.skillWikiTitle}</h3>
              <p>{t.skillWikiDesc}</p>
              <div style={{ marginTop: '16px', display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                <span style={{ fontSize: '0.75rem', padding: '4px 10px', borderRadius: '12px', background: 'rgba(59, 130, 246, 0.1)', color: '#3b82f6', fontWeight: '600' }}>LLM Ingest</span>
                <span style={{ fontSize: '0.75rem', padding: '4px 10px', borderRadius: '12px', background: 'rgba(168, 85, 247, 0.1)', color: '#a855f7', fontWeight: '600' }}>Smart Query</span>
                <span style={{ fontSize: '0.75rem', padding: '4px 10px', borderRadius: '12px', background: 'rgba(16, 185, 129, 0.1)', color: '#10b981', fontWeight: '600' }}>Quality Lint</span>
              </div>
            </div>
          </Link>

          {/* AutoSkill */}
          <Link to="/auto-skill" style={{ textDecoration: 'none' }}>
            <div 
              className="card card-whisper"
              style={{ cursor: 'pointer', height: '100%', transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)' }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-8px) scale(1.02)'
                e.currentTarget.style.boxShadow = '0 20px 60px rgba(16, 185, 129, 0.2)'
                e.currentTarget.style.borderColor = 'rgba(16, 185, 129, 0.4)'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0) scale(1)'
                e.currentTarget.style.boxShadow = ''
                e.currentTarget.style.borderColor = ''
              }}
            >
              <div className="card-label">{t.autoSkill}</div>
              <div className="feature-icon" style={{ fontSize: '2rem' }}>🔬</div>
              <h3>{t.autoSkillTitle}</h3>
              <p>{t.autoSkillDesc}</p>
              <div style={{ marginTop: '16px', paddingTop: '16px', borderTop: '1px solid var(--octo-border-color)', display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                <span style={{ fontSize: '0.75rem', padding: '4px 10px', borderRadius: '12px', background: 'rgba(139, 92, 246, 0.1)', color: '#7c3aed', fontWeight: '600' }}>Autonomous</span>
                <span style={{ fontSize: '0.75rem', padding: '4px 10px', borderRadius: '12px', background: 'rgba(236, 72, 153, 0.1)', color: '#db2777', fontWeight: '600' }}>Iterative</span>
              </div>
            </div>
          </Link>
        </div>
      </section>

      <hr className="section-divider"/>

      {/* SELF-EVOLUTION SECTION */}
      <section className="dark-section">
        <div className="section-container">
          <div className="section-label">{t.evolution}</div>
          <h2 className="section-heading">{t.howOctopaiEvolves}</h2>
          
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '32px', marginTop: '48px' }}>
            <div style={{ textAlign: 'center', padding: '32px' }}>
              <div style={{ fontSize: '3rem', marginBottom: '16px' }}>📥</div>
              <h3 style={{ fontFamily: 'var(--font-serif)', fontSize: '1.4rem', fontWeight: 500, marginBottom: '12px', color: 'var(--octo-text-primary)' }}>
                {t.dataIngestion}
              </h3>
              <p style={{ color: 'var(--octo-text-secondary)', lineHeight: '1.65', fontSize: '0.938rem' }}>
                {t.dataIngestionDesc}
              </p>
            </div>

            <div style={{ textAlign: 'center', padding: '32px' }}>
              <div style={{ fontSize: '3rem', marginBottom: '16px' }}>🧠</div>
              <h3 style={{ fontFamily: 'var(--font-serif)', fontSize: '1.4rem', fontWeight: 500, marginBottom: '12px', color: 'var(--octo-text-primary)' }}>
                {t.patternAnalysis}
              </h3>
              <p style={{ color: 'var(--octo-text-secondary)', lineHeight: '1.65', fontSize: '0.938rem' }}>
                {t.patternAnalysisDesc}
              </p>
            </div>

            <div style={{ textAlign: 'center', padding: '32px' }}>
              <div style={{ fontSize: '3rem', marginBottom: '16px' }}>🔄</div>
              <h3 style={{ fontFamily: 'var(--font-serif)', fontSize: '1.4rem', fontWeight: 500, marginBottom: '12px', color: 'var(--octo-text-primary)' }}>
                {t.selfOptimization}
              </h3>
              <p style={{ color: 'var(--octo-text-secondary)', lineHeight: '1.65', fontSize: '0.938rem' }}>
                {t.selfOptimizationDesc}
              </p>
            </div>

            <div style={{ textAlign: 'center', padding: '32px' }}>
              <div style={{ fontSize: '3rem', marginBottom: '16px' }}>📈</div>
              <h3 style={{ fontFamily: 'var(--font-serif)', fontSize: '1.4rem', fontWeight: 500, marginBottom: '12px', color: 'var(--octo-text-primary)' }}>
                {t.validationDeploy}
              </h3>
              <p style={{ color: 'var(--octo-text-secondary)', lineHeight: '1.65', fontSize: '0.938rem' }}>
                {t.validationDeployDesc}
              </p>
            </div>

            <div style={{ textAlign: 'center', padding: '32px' }}>
              <div style={{ fontSize: '3rem', marginBottom: '16px' }}>🔍</div>
              <h3 style={{ fontFamily: 'var(--font-serif)', fontSize: '1.4rem', fontWeight: 500, marginBottom: '12px', color: 'var(--octo-text-primary)' }}>
                {t.visibilityInsight}
              </h3>
              <p style={{ color: 'var(--octo-text-secondary)', lineHeight: '1.65', fontSize: '0.938rem' }}>
                {t.visibilityInsightDesc}
              </p>
            </div>
          </div>
        </div>
      </section>

      <hr className="section-divider"/>

      {/* SKILLS HUB PREVIEW */}
      <section className="section-container">
        <div className="section-label">{t.skillsEcosystem}</div>
        <h2 className="section-heading">{t.browseSkillsHub}</h2>
        <p style={{ color: 'var(--octo-text-secondary)', marginBottom: '48px', fontSize: '1.125rem', maxWidth: '700px' }}>
          {t.skillsHubDescription}
        </p>
        
        <div className="skills-grid">
          {skills.map((skill, index) => (
            <div key={index} className="skill-card">
              <div className="skill-card-header">
                <div className="skill-card-icon">{skill.icon}</div>
                <span className="skill-badge" style={{ 
                  background: 'rgba(56, 152, 236, 0.10)', 
                  borderColor: 'rgba(56, 152, 236, 0.30)', 
                  color: 'var(--octo-coral)' 
                }}>
                  {skill.category}
                </span>
              </div>
              <h3 className="card-title">{skill.name}</h3>
              <p className="card-description">{skill.desc}</p>
            </div>
          ))}
        </div>
        
        <div style={{ textAlign: 'center', marginTop: '48px' }}>
          <Link to="/skills" className="btn-primary" style={{ color: '#ffffff' }}>
            {t.browseAllSkills}
          </Link>
        </div>
      </section>

      <hr className="section-divider"/>

      {/* AUTORESEARCH SECTION */}
      <section className="dark-section">
        <div className="section-container">
          <div className="section-label">{t.autoResearch}</div>
          <h2 className="section-heading">{t.autonomousResearch}</h2>
          <p style={{ color: 'var(--octo-text-secondary)', marginBottom: '48px', fontSize: '1.125rem', maxWidth: '800px', textAlign: 'center' }}>
            {t.autoResearchDescription}
          </p>
          
          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
            gap: '32px', 
            textAlign: 'center'
          }}>
            <div>
              <div className="stat-value">~5min</div>
              <div className="stat-label">{t.perExperiment}</div>
            </div>
            <div>
              <div className="stat-value">~12/hr</div>
              <div className="stat-label">{t.experimentsPerHour}</div>
            </div>
            <div>
              <div className="stat-value">~100+</div>
              <div className="stat-label">{t.overnightRuns}</div>
            </div>
            <div>
              <div className="stat-value">∞</div>
              <div className="stat-label">{t.autonomyLoop}</div>
            </div>
          </div>
          
          <div style={{ textAlign: 'center', marginTop: '48px' }}>
            <Link to="/research" className="btn-secondary" style={{ color: '#ffffff' }}>
              {t.exploreAutoResearch}
            </Link>
          </div>
        </div>
      </section>

      <hr className="section-divider"/>

      {/* ENTERPRISE-GRADE ARCHITECTURE SECTION - NEW */}
      <section className="section-container">
        <div className="section-label">{t.techArchitecture}</div>
        <h2 className="section-heading">Six Pillars of Production-Ready Infrastructure</h2>
        <p style={{ color: 'var(--octo-text-secondary)', marginBottom: '48px', fontSize: '1.125rem', maxWidth: '800px', textAlign: 'center' }}>
          Built for scale, designed for reliability. Every module engineered with enterprise-grade capabilities.
        </p>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', gap: '32px' }}>
          {/* 1. Persistent Storage */}
          <div className="card card-whisper" style={{ padding: '32px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '20px' }}>
              <div style={{ width: '56px', height: '56px', background: 'linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%)', borderRadius: '14px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.75rem', boxShadow: '0 8px 24px rgba(59, 130, 246, 0.25)' }}>💾</div>
              <div>
                <h3 style={{ fontFamily: 'var(--font-serif)', fontSize: '1.35rem', fontWeight: 600, color: 'var(--octo-text-primary)', marginBottom: '4px' }}>{t.persistence}</h3>
                <span style={{ fontSize: '0.8rem', padding: '4px 12px', borderRadius: '12px', background: 'rgba(59, 130, 246, 0.1)', color: '#3b82f6', fontWeight: '600' }}>12 Tables · 18 Indexes</span>
              </div>
            </div>
            <p style={{ color: 'var(--octo-text-secondary)', lineHeight: '1.7', fontSize: '0.938rem' }}>{t.persistenceDesc}</p>
            <div style={{ marginTop: '20px', paddingTop: '16px', borderTop: '1px solid var(--octo-border-color)', display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
              <span style={{ fontSize: '0.8rem', color: '#6b7280' }}>✓ WAL Mode</span>
              <span style={{ fontSize: '0.8rem', color: '#6b7280' }}>✓ Multi-Tenant</span>
              <span style={{ fontSize: '0.8rem', color: '#6b7280' }}>✓ ACID Compliant</span>
            </div>
          </div>

          {/* 2. LLM Integration */}
          <div className="card card-whisper" style={{ padding: '32px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '20px' }}>
              <div style={{ width: '56px', height: '56px', background: 'linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%)', borderRadius: '14px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.75rem', boxShadow: '0 8px 24px rgba(139, 92, 246, 0.25)' }}>🤖</div>
              <div>
                <h3 style={{ fontFamily: 'var(--font-serif)', fontSize: '1.35rem', fontWeight: 600, color: 'var(--octo-text-primary)', marginBottom: '4px' }}>{t.llmIntegration}</h3>
                <span style={{ fontSize: '0.8rem', padding: '4px 12px', borderRadius: '12px', background: 'rgba(139, 92, 246, 0.1)', color: '#8b5cf6', fontWeight: '600' }}>OpenAI + Claude</span>
              </div>
            </div>
            <p style={{ color: 'var(--octo-text-secondary)', lineHeight: '1.7', fontSize: '0.938rem' }}>{t.llmIntegrationDesc}</p>
            <div style={{ marginTop: '20px', paddingTop: '16px', borderTop: '1px solid var(--octo-border-color)', display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
              <span style={{ fontSize: '0.8rem', color: '#6b7280' }}>✓ Auto-Failover</span>
              <span style={{ fontSize: '0.8rem', color: '#6b7280' }}>✓ Token Tracking</span>
              <span style={{ fontSize: '0.8rem', color: '#6b7280' }}>✓ Cost Analytics</span>
            </div>
          </div>

          {/* 3. Real-Time Communication */}
          <div className="card card-whisper" style={{ padding: '32px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '20px' }}>
              <div style={{ width: '56px', height: '56px', background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)', borderRadius: '14px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.75rem', boxShadow: '0 8px 24px rgba(16, 185, 129, 0.25)' }}>📡</div>
              <div>
                <h3 style={{ fontFamily: 'var(--font-serif)', fontSize: '1.35rem', fontWeight: 600, color: 'var(--octo-text-primary)', marginBottom: '4px' }}>{t.realtime}</h3>
                <span style={{ fontSize: '0.8rem', padding: '4px 12px', borderRadius: '12px', background: 'rgba(16, 185, 129, 0.1)', color: '#10b981', fontWeight: '600' }}>15 Event Types</span>
              </div>
            </div>
            <p style={{ color: 'var(--octo-text-secondary)', lineHeight: '1.7', fontSize: '0.938rem' }}>{t.realtimeDesc}</p>
            <div style={{ marginTop: '20px', paddingTop: '16px', borderTop: '1px solid var(--octo-border-color)', display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
              <span style={{ fontSize: '0.8rem', color: '#6b7280' }}>✓ WebSocket</span>
              <span style={{ fontSize: '0.8rem', color: '#6b7280' }}>✓ Live Updates</span>
              <span style={{ fontSize: '0.8rem', color: '#6b7280' }}>✓ Heartbeat</span>
            </div>
          </div>

          {/* 4. Authentication & RBAC */}
          <div className="card card-whisper" style={{ padding: '32px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '20px' }}>
              <div style={{ width: '56px', height: '56px', background: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)', borderRadius: '14px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.75rem', boxShadow: '0 8px 24px rgba(245, 158, 11, 0.25)' }}>🔐</div>
              <div>
                <h3 style={{ fontFamily: 'var(--font-serif)', fontSize: '1.35rem', fontWeight: 600, color: 'var(--octo-text-primary)', marginBottom: '4px' }}>{t.authSystem}</h3>
                <span style={{ fontSize: '0.8rem', padding: '4px 12px', borderRadius: '12px', background: 'rgba(245, 158, 11, 0.1)', color: '#d97706', fontWeight: '600' }}>4 Roles · 11 Permissions</span>
              </div>
            </div>
            <p style={{ color: 'var(--octo-text-secondary)', lineHeight: '1.7', fontSize: '0.938rem' }}>{t.authSystemDesc}</p>
            <div style={{ marginTop: '20px', paddingTop: '16px', borderTop: '1px solid var(--octo-border-color)', display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
              <span style={{ fontSize: '0.8rem', color: '#6b7280' }}>✓ JWT Tokens</span>
              <span style={{ fontSize: '0.8rem', color: '#6b7280' }}>✓ API Keys</span>
              <span style={{ fontSize: '0.8rem', color: '#6b7280' }}>✓ Sessions</span>
            </div>
          </div>

          {/* 5. Multi-Format Export */}
          <div className="card card-whisper" style={{ padding: '32px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '20px' }}>
              <div style={{ width: '56px', height: '56px', background: 'linear-gradient(135deg, #ec4899 0%, #db2777 100%)', borderRadius: '14px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.75rem', boxShadow: '0 8px 24px rgba(236, 72, 153, 0.25)' }}>📤</div>
              <div>
                <h3 style={{ fontFamily: 'var(--font-serif)', fontSize: '1.35rem', fontWeight: 600, color: 'var(--octo-text-primary)', marginBottom: '4px' }}>{t.exportSystem}</h3>
                <span style={{ fontSize: '0.8rem', padding: '4px 12px', borderRadius: '12px', background: 'rgba(236, 72, 153, 0.1)', color: '#db2777', fontWeight: '600' }}>MD · PDF · JSON · CSV · HTML</span>
              </div>
            </div>
            <p style={{ color: 'var(--octo-text-secondary)', lineHeight: '1.7', fontSize: '0.938rem' }}>{t.exportSystemDesc}</p>
            <div style={{ marginTop: '20px', paddingTop: '16px', borderTop: '1px solid var(--octo-border-color)', display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
              <span style={{ fontSize: '0.8rem', color: '#6b7280' }}>✓ Async Jobs</span>
              <span style={{ fontSize: '0.8rem', color: '#6b7280' }}>✓ Progress Track</span>
              <span style={{ fontSize: '0.8rem', color: '#6b7280' }}>✓ Batch Ops</span>
            </div>
          </div>

          {/* 6. Version Control System */}
          <div className="card card-whisper" style={{ padding: '32px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '20px' }}>
              <div style={{ width: '56px', height: '56px', background: 'linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)', borderRadius: '14px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.75rem', boxShadow: '0 8px 24px rgba(6, 182, 212, 0.25)' }}>🔄</div>
              <div>
                <h3 style={{ fontFamily: 'var(--font-serif)', fontSize: '1.35rem', fontWeight: 600, color: 'var(--octo-text-primary)', marginBottom: '4px' }}>{t.versionControl}</h3>
                <span style={{ fontSize: '0.8rem', padding: '4px 12px', borderRadius: '12px', background: 'rgba(6, 182, 212, 0.1)', color: '#0891b2', fontWeight: '600' }}>Full History · Diff · Rollback</span>
              </div>
            </div>
            <p style={{ color: 'var(--octo-text-secondary)', lineHeight: '1.7', fontSize: '0.938rem' }}>{t.versionControlDesc}</p>
            <div style={{ marginTop: '20px', paddingTop: '16px', borderTop: '1px solid var(--octo-border-color)', display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
              <span style={{ fontSize: '0.8rem', color: '#6b7280' }}>✓ Line Diff</span>
              <span style={{ fontSize: '0.8rem', color: '#6b7280' }}>✓ Snapshots</span>
              <span style={{ fontSize: '0.8rem', color: '#6b7280' }}>✓ Attribution</span>
            </div>
          </div>
        </div>

        {/* Platform Statistics Bar */}
        <div style={{ marginTop: '64px', padding: '40px', background: 'linear-gradient(135deg, rgba(245, 158, 11, 0.05) 0%, rgba(251, 146, 60, 0.03) 100%)', border: '2px solid rgba(245, 158, 11, 0.2)', borderRadius: '20px' }}>
          <h3 style={{ fontFamily: 'var(--font-serif)', fontSize: '1.5rem', fontWeight: 700, color: 'var(--octo-text-primary)', marginBottom: '32px', textAlign: 'center' }}>{t.platformStats}</h3>
          
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '32px', textAlign: 'center' }}>
            <div>
              <div style={{ fontSize: '3rem', fontWeight: 900, background: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text', marginBottom: '8px' }}>6</div>
              <div style={{ fontSize: '1.1rem', fontWeight: 600, color: 'var(--octo-text-primary)' }}>{t.totalModules}</div>
              <div style={{ fontSize: '0.875rem', color: '#6b7280', marginTop: '4px' }}>{t.totalModulesDesc}</div>
            </div>
            
            <div>
              <div style={{ fontSize: '3rem', fontWeight: 900, background: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text', marginBottom: '8px' }}>26+</div>
              <div style={{ fontSize: '1.1rem', fontWeight: 600, color: 'var(--octo-text-primary)' }}>{t.apiEndpoints}</div>
              <div style={{ fontSize: '0.875rem', color: '#6b7280', marginTop: '4px' }}>{t.apiEndpointsDesc}</div>
            </div>
            
            <div>
              <div style={{ fontSize: '3rem', fontWeight: 900, background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text', marginBottom: '8px' }}>6K+</div>
              <div style={{ fontSize: '1.1rem', fontWeight: 600, color: 'var(--octo-text-primary)' }}>{t.codebaseSize}</div>
              <div style={{ fontSize: '0.875rem', color: '#6b7280', marginTop: '4px' }}>{t.codebaseSizeDesc}</div>
            </div>
            
            <div>
              <div style={{ fontSize: '3rem', fontWeight: 900, background: 'linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text', marginBottom: '8px' }}>5</div>
              <div style={{ fontSize: '1.1rem', fontWeight: 600, color: 'var(--octo-text-primary)' }}>{t.supportedFormats}</div>
              <div style={{ fontSize: '0.875rem', color: '#6b7280', marginTop: '4px' }}>{t.supportedFormatsDesc}</div>
            </div>
            
            <div>
              <div style={{ fontSize: '3rem', fontWeight: 900, background: 'linear-gradient(135deg, #ec4899 0%, #db2777 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text', marginBottom: '8px' }}>∞</div>
              <div style={{ fontSize: '1.1rem', fontWeight: 600, color: 'var(--octo-text-primary)' }}>Scalability</div>
              <div style={{ fontSize: '0.875rem', color: '#6b7280', marginTop: '4px' }}>Infinite Evolution Potential</div>
            </div>
          </div>
        </div>
      </section>

      <hr className="section-divider"/>

      {/* FOOTER */}
      {/* FOOTER - Optimized Layout */}
      <footer style={{ padding: '60px 40px', position: 'relative', zIndex: 1 }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1.5fr repeat(4, 1fr)', gap: '48px', marginBottom: '48px' }}>
            {/* Octopai Brand Section */}
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '20px' }}>
                <span style={{
                  width: '40px',
                  height: '40px',
                  background: 'var(--octo-terracotta)',
                  borderRadius: 'var(--radius-comfortable)',
                  display: 'inline-flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'var(--octo-ivory)',
                  fontFamily: 'var(--font-serif)',
                  fontSize: '22px',
                  fontWeight: 600,
                  boxShadow: '0 4px 12px rgba(239, 68, 68, 0.3)'
                }}>🐙</span>
                <span style={{ fontFamily: 'var(--font-serif)', fontSize: '24px', fontWeight: 600, color: 'var(--octo-text-primary)', letterSpacing: '-0.02em' }}>Octopai</span>
              </div>
              <p style={{ color: 'var(--octo-text-secondary)', fontSize: '0.9rem', lineHeight: '1.7', marginBottom: '24px', opacity: 0.85 }}>
                {t.brandDescription}
              </p>
            </div>

            {/* Product */}
            <div>
              <h4 style={{ fontFamily: 'var(--font-serif)', fontSize: '1rem', fontWeight: 600, color: 'var(--octo-text-primary)', marginBottom: '18px', letterSpacing: '-0.01em' }}>
                {t.product}
              </h4>
              <ul style={{ listStyle: 'none', margin: 0, padding: 0 }}>
                <li style={{ marginBottom: '12px' }}><Link to="/agent" style={{ color: '#ffffff', textDecoration: 'none', fontSize: '0.9rem', opacity: 0.9, transition: 'opacity 0.2s' }} onMouseEnter={(e) => e.target.style.opacity = '1'} onMouseLeave={(e) => e.target.style.opacity = '0.9'}>{t.aiAgent}</Link></li>
                <li style={{ marginBottom: '12px' }}><Link to="/skills" style={{ color: '#ffffff', textDecoration: 'none', fontSize: '0.9rem', opacity: 0.9, transition: 'opacity 0.2s' }} onMouseEnter={(e) => e.target.style.opacity = '1'} onMouseLeave={(e) => e.target.style.opacity = '0.9'}>{t.skillsHub}</Link></li>
                <li style={{ marginBottom: '12px' }}><Link to="/ai-wiki" style={{ color: '#ffffff', textDecoration: 'none', fontSize: '0.9rem', opacity: 0.9, transition: 'opacity 0.2s' }} onMouseEnter={(e) => e.target.style.opacity = '1'} onMouseLeave={(e) => e.target.style.opacity = '0.9'}>AI Wiki</Link></li>
                <li style={{ marginBottom: '12px' }}><Link to="/research" style={{ color: '#ffffff', textDecoration: 'none', fontSize: '0.9rem', opacity: 0.9, transition: 'opacity 0.2s' }} onMouseEnter={(e) => e.target.style.opacity = '1'} onMouseLeave={(e) => e.target.style.opacity = '0.9'}>{t.autoResearch}</Link></li>
              </ul>
            </div>

            {/* Resources */}
            <div>
              <h4 style={{ fontFamily: 'var(--font-serif)', fontSize: '1rem', fontWeight: 600, color: 'var(--octo-text-primary)', marginBottom: '18px', letterSpacing: '-0.01em' }}>
                {t.resources}
              </h4>
              <ul style={{ listStyle: 'none', margin: 0, padding: 0 }}>
                <li style={{ marginBottom: '12px' }}><a href="#" style={{ color: '#ffffff', textDecoration: 'none', fontSize: '0.9rem', opacity: 0.9, transition: 'opacity 0.2s' }} onMouseEnter={(e) => e.target.style.opacity = '1'} onMouseLeave={(e) => e.target.style.opacity = '0.9'}>{t.documentation}</a></li>
                <li style={{ marginBottom: '12px' }}><a href="#" style={{ color: '#ffffff', textDecoration: 'none', fontSize: '0.9rem', opacity: 0.9, transition: 'opacity 0.2s' }} onMouseEnter={(e) => e.target.style.opacity = '1'} onMouseLeave={(e) => e.target.style.opacity = '0.9'}>{t.research}</a></li>
                <li style={{ marginBottom: '12px' }}><a href="#" style={{ color: '#ffffff', textDecoration: 'none', fontSize: '0.9rem', opacity: 0.9, transition: 'opacity 0.2s' }} onMouseEnter={(e) => e.target.style.opacity = '1'} onMouseLeave={(e) => e.target.style.opacity = '0.9'}>{t.examples}</a></li>
                <li style={{ marginBottom: '12px' }}><a href="#" style={{ color: '#ffffff', textDecoration: 'none', fontSize: '0.9rem', opacity: 0.9, transition: 'opacity 0.2s' }} onMouseEnter={(e) => e.target.style.opacity = '1'} onMouseLeave={(e) => e.target.style.opacity = '0.9'}>{t.tutorials}</a></li>
              </ul>
            </div>

            {/* Community */}
            <div>
              <h4 style={{ fontFamily: 'var(--font-serif)', fontSize: '1rem', fontWeight: 600, color: 'var(--octo-text-primary)', marginBottom: '18px', letterSpacing: '-0.01em' }}>
                {t.community}
              </h4>
              <ul style={{ listStyle: 'none', margin: 0, padding: 0 }}>
                <li style={{ marginBottom: '12px' }}><a href="#" style={{ color: '#ffffff', textDecoration: 'none', fontSize: '0.9rem', opacity: 0.9, transition: 'opacity 0.2s' }} onMouseEnter={(e) => e.target.style.opacity = '1'} onMouseLeave={(e) => e.target.style.opacity = '0.9'}>{t.github}</a></li>
                <li style={{ marginBottom: '12px' }}><a href="#" style={{ color: '#ffffff', textDecoration: 'none', fontSize: '0.9rem', opacity: 0.9, transition: 'opacity 0.2s' }} onMouseEnter={(e) => e.target.style.opacity = '1'} onMouseLeave={(e) => e.target.style.opacity = '0.9'}>{t.discord}</a></li>
                <li style={{ marginBottom: '12px' }}><a href="#" style={{ color: '#ffffff', textDecoration: 'none', fontSize: '0.9rem', opacity: 0.9, transition: 'opacity 0.2s' }} onMouseEnter={(e) => e.target.style.opacity = '1'} onMouseLeave={(e) => e.target.style.opacity = '0.9'}>{t.twitter}</a></li>
                <li style={{ marginBottom: '12px' }}><a href="#" style={{ color: '#ffffff', textDecoration: 'none', fontSize: '0.9rem', opacity: 0.9, transition: 'opacity 0.2s' }} onMouseEnter={(e) => e.target.style.opacity = '1'} onMouseLeave={(e) => e.target.style.opacity = '0.9'}>{t.blog}</a></li>
              </ul>
            </div>

            {/* Company */}
            <div>
              <h4 style={{ fontFamily: 'var(--font-serif)', fontSize: '1rem', fontWeight: 600, color: 'var(--octo-text-primary)', marginBottom: '18px', letterSpacing: '-0.01em' }}>
                {t.company}
              </h4>
              <ul style={{ listStyle: 'none', margin: 0, padding: 0 }}>
                <li style={{ marginBottom: '12px' }}><a href="#" style={{ color: '#ffffff', textDecoration: 'none', fontSize: '0.9rem', opacity: 0.9, transition: 'opacity 0.2s' }} onMouseEnter={(e) => e.target.style.opacity = '1'} onMouseLeave={(e) => e.target.style.opacity = '0.9'}>{t.about}</a></li>
                <li style={{ marginBottom: '12px' }}><a href="#" style={{ color: '#ffffff', textDecoration: 'none', fontSize: '0.9rem', opacity: 0.9, transition: 'opacity 0.2s' }} onMouseEnter={(e) => e.target.style.opacity = '1'} onMouseLeave={(e) => e.target.style.opacity = '0.9'}>{t.careers}</a></li>
                <li style={{ marginBottom: '12px' }}><a href="#" style={{ color: '#ffffff', textDecoration: 'none', fontSize: '0.9rem', opacity: 0.9, transition: 'opacity 0.2s' }} onMouseEnter={(e) => e.target.style.opacity = '1'} onMouseLeave={(e) => e.target.style.opacity = '0.9'}>{t.privacy}</a></li>
                <li style={{ marginBottom: '12px' }}><a href="#" style={{ color: '#ffffff', textDecoration: 'none', fontSize: '0.9rem', opacity: 0.9, transition: 'opacity 0.2s' }} onMouseEnter={(e) => e.target.style.opacity = '1'} onMouseLeave={(e) => e.target.style.opacity = '0.9'}>{t.terms}</a></li>
              </ul>
            </div>
          </div>

          <div style={{ borderTop: '1px solid var(--octo-border-color)', paddingTop: '24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            {/* Language Switcher */}
            <button
              onClick={() => setLanguage(language === 'en' ? 'zh' : 'en')}
              className="group px-5 py-2.5 bg-gradient-to-r from-gray-800 to-gray-900 dark:from-gray-700 dark:to-gray-800 hover:from-blue-600 hover:to-cyan-600 text-white rounded-xl font-semibold transition-all duration-300 shadow-lg hover:shadow-xl hover:shadow-blue-500/25 flex items-center gap-2.5 border border-gray-700 dark:border-gray-600 hover:border-transparent"
            >
              <span className="text-lg group-hover:rotate-12 transition-transform duration-300 inline-block">🌐</span>
              <span>{language === 'en' ? '中文' : 'English'}</span>
              <span className="text-xs opacity-70 group-hover:opacity-100 transition-opacity">↔</span>
            </button>

            {/* Copyright */}
            <p style={{ color: 'var(--octo-text-secondary)', fontSize: '0.875rem', margin: 0 }}>
              {t.copyright}
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default Home
