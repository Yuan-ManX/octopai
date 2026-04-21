import React, { useState, useEffect, useCallback } from 'react';
import { Link } from 'react-router-dom';

/**
 * AI Wiki - Incremental Knowledge Base System with OctoTrace Integration
 * 
 * Core Architecture (Three-Layer Design):
 * Layer 1: Raw Sources - Immutable document collection (articles, papers, notes)
 * Layer 2: AI Wiki - LLM-generated structured knowledge base with cross-references
 * Layer 3: Schema Rules - Configuration defining structure, conventions, and workflows
 * 
 * Key Operations:
 * - INGEST: Analyze sources → Extract entities → Generate wiki pages → Update graph
 * - QUERY: Search knowledge base → Graph expansion → Context assembly → Answer synthesis
 * - LINT: Consistency check → Contradiction detection → Link validation → Quality scoring
 * 
 * OctoTrace Integration (Deep Observability):
 * - Evolution Timeline: Track how knowledge evolves over time with detailed operation logs
 * - Span Tree: Hierarchical view of all wiki operations (ingest/query/lint as spans)
 * - Cost Analytics: Token usage, operation costs, budget monitoring for LLM calls
 * - Trace Viewer: Real-time visualization of wiki operations with full stack traces
 * 
 * Integration Points:
 * - AutoResearch: Deep Research engine for multi-source ingestion
 * - Skills Hub: Wiki as knowledge foundation for skill execution
 * - OctoTrace: Full observability of knowledge evolution timeline (DEEP INTEGRATION)
 * - Evolution Workbench: Self-optimization of wiki quality metrics
 */

const AIWiki = () => {
  // State management for three-layer architecture
  const [activeTab, setActiveTab] = useState('overview');
  const [sources, setSources] = useState([
    { id: 1, name: 'Research Paper: Neural Architecture Search', type: 'pdf', size: '2.4MB', status: 'ingested', hash: 'sha256:abc123' },
    { id: 2, name: 'Meeting Notes: Q1 Planning', type: 'md', size: '45KB', status: 'ingested', hash: 'sha256:def456' },
    { id: 3, name: 'Article: LLM Training Techniques', type: 'url', size: 'N/A', status: 'pending', hash: null },
    { id: 4, name: 'Data Report: User Analytics', type: 'csv', size: '1.8MB', status: 'processing', hash: null },
  ]);

  const [wikiPages, setWikiPages] = useState([
    { id: 1, title: 'Neural Architecture Search', type: 'entity', links: 12, lastUpdated: '2 hours ago', quality: 94 },
    { id: 2, title: 'Evolution Strategies Overview', type: 'concept', links: 8, lastUpdated: '5 hours ago', quality: 89 },
    { id: 3, title: 'Q1 2026 Objectives', type: 'summary', links: 5, lastUpdated: '1 day ago', quality: 97 },
    { id: 4, title: 'Training Optimization Methods', type: 'comparison', links: 15, lastUpdated: '3 days ago', quality: 91 },
    { id: 5, title: 'User Behavior Patterns', type: 'analysis', links: 6, lastUpdated: '1 week ago', quality: 86 },
  ]);

  const [knowledgeGraph, setKnowledgeGraph] = useState({
    nodes: [
      { id: 'nas', label: 'Neural Architecture Search', group: 'research', connections: 12 },
      { id: 'evolution', label: 'Evolution Strategies', group: 'algorithm', connections: 8 },
      { id: 'training', label: 'Training Methods', group: 'technique', connections: 15 },
      { id: 'llm', label: 'Large Language Models', group: 'model', connections: 20 },
      { id: 'optimization', label: 'Optimization', group: 'concept', connections: 10 },
      { id: 'feedback', label: 'Feedback Descent', group: 'algorithm', connections: 6 },
    ],
    edges: [
      { source: 'nas', target: 'evolution', weight: 0.85, type: 'direct' },
      { source: 'nas', target: 'training', weight: 0.72, type: 'direct' },
      { source: 'evolution', target: 'optimization', weight: 0.91, type: 'strong' },
      { source: 'training', target: 'llm', weight: 0.88, type: 'direct' },
      { source: 'llm', target: 'feedback', weight: 0.76, type: 'related' },
      { source: 'optimization', target: 'feedback', weight: 0.82, type: 'methodology' },
    ]
  });

  const [queryInput, setQueryInput] = useState('');
  const [queryResults, setQueryResults] = useState(null);
  const [isIngesting, setIsIngesting] = useState(false);
  const [ingestProgress, setIngestProgress] = useState({ stage: '', progress: 0 });
  const [lintReport, setLintReport] = useState(null);
  const [selectedNode, setSelectedNode] = useState(null);

  // OctoTrace Integration States
  const [evolutionTimeline, setEvolutionTimeline] = useState([
    { timestamp: '2026-04-11T14:30:00Z', operation: 'INGEST', source: 'LLM Training Techniques', details: 'Created 3 wiki pages, added 12 graph edges', duration: '4.8s', tokens: 2450, cost: '$0.024', spanId: 'span_001' },
    { timestamp: '2026-04-11T14:25:00Z', operation: 'QUERY', source: 'User Question', details: 'Retrieved 5 nodes, expanded to 12 contexts', duration: '1.2s', tokens: 890, cost: '$0.009', spanId: 'span_002' },
    { timestamp: '2026-04-11T14:20:00Z', operation: 'LINT', source: 'System Check', details: '42/47 checks passed, found 1 contradiction', duration: '2.3s', tokens: 320, cost: '$0.003', spanId: 'span_003' },
    { timestamp: '2026-04-11T14:15:00Z', operation: 'DEEP_RESEARCH', source: 'AutoResearch Engine', details: 'Discovered 5 new papers on NAS, auto-ingested 2', duration: '45.6s', tokens: 12890, cost: '$0.129', spanId: 'span_004' },
    { timestamp: '2026-04-11T14:10:00Z', operation: 'INGEST', source: 'Meeting Notes Q1', details: 'Updated 2 existing pages, created 1 summary', duration: '3.1s', tokens: 1560, cost: '$0.016', spanId: 'span_005' },
    { timestamp: '2026-04-11T14:05:00Z', operation: 'QUERY', source: 'User Question', details: 'Answered about evolution strategies (89% confidence)', duration: '0.9s', tokens: 750, cost: '$0.008', spanId: 'span_006' },
    { timestamp: '2026-04-11T13:55:00Z', operation: 'INGEST', source: 'Research Paper NAS', details: 'Initial knowledge base creation, 5 pages', duration: '6.2s', tokens: 3420, cost: '$0.034', spanId: 'span_007' },
  ]);

  const [spanTree, setSpanTree] = useState({
    rootSpan: {
      id: 'root_wiki_session',
      operation: 'Wiki Session',
      startTime: '2026-04-11T13:55:00Z',
      duration: '45min',
      status: 'active',
      children: [
        {
          id: 'span_007',
          operation: 'INGEST - Research Paper NAS',
          startTime: '2026-04-11T13:55:00Z',
          duration: '6.2s',
          tokens: 3420,
          status: 'completed',
          children: [
            { id: 'span_007a', operation: 'Analysis Phase', duration: '3.1s', tokens: 1800, status: 'completed' },
            { id: 'span_007b', operation: 'Generation Phase', duration: '2.8s', tokens: 1620, status: 'completed' },
            { id: 'span_007c', operation: 'Graph Update', duration: '0.3s', tokens: 0, status: 'completed' }
          ]
        },
        {
          id: 'span_006',
          operation: 'QUERY - Evolution Strategies',
          startTime: '2026-04-11T14:05:00Z',
          duration: '0.9s',
          tokens: 750,
          status: 'completed',
          children: [
            { id: 'span_006a', operation: 'Tokenized Search', duration: '0.2s', tokens: 50, status: 'completed' },
            { id: 'span_006b', operation: 'Graph Expansion', duration: '0.3s', tokens: 400, status: 'completed' },
            { id: 'span_006c', operation: 'Context Assembly', duration: '0.4s', tokens: 300, status: 'completed' }
          ]
        },
        {
          id: 'span_005',
          operation: 'INGEST - Meeting Notes',
          startTime: '2026-04-11T14:10:00Z',
          duration: '3.1s',
          tokens: 1560,
          status: 'completed',
          children: [
            { id: 'span_005a', operation: 'Analysis Phase', duration: '1.5s', tokens: 900, status: 'completed' },
            { id: 'span_005b', operation: 'Generation Phase', duration: '1.4s', tokens: 660, status: 'completed' }
          ]
        },
        {
          id: 'span_004',
          operation: 'DEEP_RESEARCH - AutoDiscovery',
          startTime: '2026-04-11T14:15:00Z',
          duration: '45.6s',
          tokens: 12890,
          status: 'completed',
          children: [
            { id: 'span_004a', operation: 'Topic Generation', duration: '2.1s', tokens: 450, status: 'completed' },
            { id: 'span_004b', operation: 'Web Search (5 queries)', duration: '32.0s', tokens: 8900, status: 'completed' },
            { id: 'span_004c', operation: 'Auto-Ingest Results', duration: '8.2s', tokens: 3540, status: 'completed' },
            { id: 'span_004d', operation: 'Graph Integration', duration: '3.3s', tokens: 0, status: 'completed' }
          ]
        },
        {
          id: 'span_003',
          operation: 'LINT - Quality Check',
          startTime: '2026-04-11T14:20:00Z',
          duration: '2.3s',
          tokens: 320,
          status: 'completed',
          children: [
            { id: 'span_003a', operation: 'Consistency Check', duration: '0.8s', tokens: 120, status: 'completed' },
            { id: 'span_003b', operation: 'Link Validation', duration: '0.7s', tokens: 100, status: 'completed' },
            { id: 'span_003c', operation: 'Quality Scoring', duration: '0.8s', tokens: 100, status: 'completed' }
          ]
        },
        {
          id: 'span_002',
          operation: 'QUERY - User Question',
          startTime: '2026-04-11T14:25:00Z',
          duration: '1.2s',
          tokens: 890,
          status: 'completed'
        },
        {
          id: 'span_001',
          operation: 'INGEST - LLM Training',
          startTime: '2026-04-11T14:30:00Z',
          duration: '4.8s',
          tokens: 2450,
          status: 'in_progress',
          children: [
            { id: 'span_001a', operation: 'Analysis Phase', duration: '2.4s', tokens: 1300, status: 'completed' },
            { id: 'span_001b', operation: 'Generation Phase', duration: '2.1s', tokens: 1150, status: 'in_progress' },
            { id: 'span_001c', operation: 'Graph Update', duration: 'pending', tokens: 0, status: 'pending' }
          ]
        }
      ]
    }
  });

  const [costAnalytics, setCostAnalytics] = useState({
    totalTokens: 22280,
    totalCost: 0.223,
    budget: 1.00,
    operations: {
      INGEST: { count: 4, tokens: 10990, cost: 0.110, avgDuration: '4.5s' },
      QUERY: { count: 2, tokens: 1640, cost: 0.017, avgDuration: '1.1s' },
      LINT: { count: 1, tokens: 320, cost: 0.003, avgDuration: '2.3s' },
      DEEP_RESEARCH: { count: 1, tokens: 12890, cost: 0.129, avgDuration: '45.6s' }
    },
    tokenByLayer: {
      analysis: 6350,
      generation: 5830,
      graph_ops: 330,
      quality_checks: 420,
      retrieval: 1640,
      web_search: 8900
    },
    dailyUsage: [
      { date: 'Apr 5', tokens: 8500, cost: 0.085 },
      { date: 'Apr 6', tokens: 12300, cost: 0.123 },
      { date: 'Apr 7', tokens: 9800, cost: 0.098 },
      { date: 'Apr 8', tokens: 15600, cost: 0.156 },
      { date: 'Apr 9', tokens: 11200, cost: 0.112 },
      { date: 'Apr 10', tokens: 18900, cost: 0.189 },
      { date: 'Apr 11', tokens: 22280, cost: 0.223 }
    ],
    topOperations: [
      { operation: 'DEEP_RESEARCH - AutoDiscovery', tokens: 12890, percentage: 57.8 },
      { operation: 'INGEST - Research Paper NAS', tokens: 3420, percentage: 15.4 },
      { operation: 'INGEST - LLM Training Techniques', tokens: 2450, percentage: 11.0 },
      { operation: 'INGEST - Meeting Notes Q1', tokens: 1560, percentage: 7.0 },
      { operation: 'QUERY - Evolution Strategies', tokens: 750, percentage: 3.4 }
    ]
  });

  /**
   * INGEST Operation - Two-Step Chain-of-Thought Process
   * Step 1: Analysis Phase - LLM reads source, extracts key information
   * Step 2: Generation Phase - LLM generates structured wiki pages with cross-references
   */
  const handleIngest = useCallback(async () => {
    setIsIngesting(true);
    setIngestProgress({ stage: 'Analyzing sources...', progress: 10 });

    // Simulate two-step chain-of-thought ingest
    setTimeout(() => setIngestProgress({ stage: 'Extracting entities & concepts...', progress: 30 }), 800);
    setTimeout(() => setIngestProgress({ stage: 'Building knowledge graph connections...', progress: 50 }), 1600);
    setTimeout(() => setIngestProgress({ stage: 'Generating wiki pages with cross-references...', progress: 70 }), 2400);
    setTimeout(() => setIngestProgress({ stage: 'Updating index.md and log.md...', progress: 85 }), 3200);
    setTimeout(() => setIngestProgress({ stage: 'Running consistency checks...', progress: 95 }), 4000);
    
    setTimeout(() => {
      setIsIngesting(false);
      setIngestProgress({ stage: 'Complete! 3 new pages created, 7 links updated.', progress: 100 });
      
      // Update wiki pages with new content
      setWikiPages(prev => [...prev, {
        id: prev.length + 1,
        title: 'New Research Insights',
        type: 'entity',
        links: 4,
        lastUpdated: 'Just now',
        quality: 92
      }]);
    }, 4800);
  }, []);

  /**
   * QUERY Operation - Four-Phase Retrieval System
   * Phase 1: Tokenized search across wiki content
   * Phase 2: Graph expansion to related nodes
   * Phase 3: Budget control for context window
   * Phase 4: Context assembly with cited sources
   */
  const handleQuery = useCallback(async () => {
    if (!queryInput.trim()) return;

    setQueryResults({
      query: queryInput,
      answer: `Based on the accumulated knowledge base with ${wikiPages.length} wiki pages and ${knowledgeGraph.nodes.length} interconnected concepts:\n\n${queryInput.includes('evolution') || queryInput.includes('optimize') 
        ? 'The Evolution Workbench utilizes Feedback Descent algorithm for pairwise comparison optimization. Key findings from 12 research papers show 40-60% improvement in convergence speed compared to traditional gradient-based methods. The system maintains a frontier of top-K variants and uses UCB1 exploration strategy.' 
        : 'The knowledge base contains structured information across multiple domains including neural architectures, training methodologies, and optimization strategies. Cross-referencing reveals strong connections between architecture search and evolutionary algorithms (correlation: 0.85).'}`,
      sources: ['Neural Architecture Search (wiki#1)', 'Evolution Strategies Overview (wiki#2)', 'Training Optimization Methods (wiki#4)'],
      graphNodesVisited: 5,
      confidence: 0.89,
      timestamp: new Date().toISOString()
    });
  }, [queryInput, wikiPages.length, knowledgeGraph.nodes.length]);

  /**
   * LINT Operation - Quality Assurance System
   * Checks: Consistency, contradictions, orphan pages, broken links, quality scores
   */
  const handleLint = useCallback(() => {
    setLintReport({
      timestamp: new Date().toISOString(),
      totalChecks: 47,
      passed: 42,
      warnings: 4,
      errors: 1,
      issues: [
        { severity: 'error', type: 'Contradiction', message: 'TrainingMethods#4 claims "batch size 32 optimal" but NewResearch#6 shows "batch size 64 better"', location: 'wiki://TrainingMethods vs wiki://NewResearch' },
        { severity: 'warning', type: 'Orphan Page', message: '"Legacy Notes" has no incoming links', location: 'wiki://LegacyNotes' },
        { severity: 'warning', type: 'Broken Link', message: 'Reference to [[NonExistentPage]] in wiki#3', location: 'wiki://Q1_2026_Objectives' },
        { severity: 'info', type: 'Quality Score', message: 'Average page quality: 91.4% (target: 95%)', location: 'global' },
        { severity: 'info', type: 'Graph Density', message: 'Knowledge graph connectivity: 73% (good)', location: 'graph' },
      ],
      recommendations: [
        'Run human review on training batch size contradiction',
        'Consider merging or linking orphan pages',
        'Update broken wikilinks to valid targets',
        'Increase cross-references between research and methods sections'
      ]
    });
  }, []);

  /**
   * Deep Research Integration with AutoResearch Module
   * Triggers multi-query web search and auto-ingests results into wiki
   */
  const handleDeepResearch = async () => {
    setActiveTab('overview');
    // This would integrate with AutoResearch backend
    console.log('Initiating deep research workflow...');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 dark:from-gray-900 dark:via-blue-950 dark:to-indigo-950">
      {/* Header Section */}
      <div className="max-w-7xl mx-auto px-6 pt-8 pb-6">
        {/* Header - Optimized Layout */}
        <div className="mb-12">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-6 group">
              <div className="w-20 h-20 bg-gradient-to-br from-amber-500 via-orange-500 to-red-500 rounded-3xl flex items-center justify-center text-white text-4xl shadow-2xl shadow-orange-500/40 animate-pulse-subtle ring-4 ring-orange-500/20 relative overflow-hidden shrink-0 transform hover:scale-105 hover:shadow-3xl transition-all duration-300">
                <span className="relative z-10 drop-shadow-lg">📚</span>
                <div className="absolute inset-0 bg-gradient-to-br from-white/20 via-white/10 to-transparent animate-pulse"></div>
                <div className="absolute -inset-1 bg-gradient-to-br from-amber-400/30 to-red-400/30 rounded-3xl blur-xl opacity-60 group-hover:opacity-100 transition-opacity"></div>
              </div>
              <div className="min-w-0 flex-1">
                <h1 className="text-5xl font-black bg-gradient-to-r from-blue-600 via-cyan-500 to-blue-700 dark:from-blue-400 dark:via-cyan-300 dark:to-blue-400 bg-clip-text text-transparent mb-3 tracking-wide drop-shadow-xl filter leading-snug">
                  Skill Wiki
                </h1>
                <p className="text-gray-700 dark:text-gray-300 text-base leading-relaxed font-medium max-w-2xl opacity-90">
                  Incremental Knowledge Base System — Transform documents into structured, interlinked intelligence that compounds over time through continuous learning and evolution
                </p>
              </div>
            </div>
            
            {/* Action Buttons */}
            <div className="flex gap-3 shrink-0">
              <Link 
                to="/auto-skill" 
                className="group px-5 py-2.5 bg-gradient-to-r from-emerald-600 via-teal-600 to-cyan-600 hover:from-emerald-700 hover:to-cyan-700 text-white rounded-xl font-bold transition-all duration-300 shadow-lg shadow-emerald-500/25 hover:shadow-xl flex items-center gap-2"
              >
                <span className="text-lg group-hover:rotate-12 transition-transform duration-300 inline-block">🔬</span> 
                Deep Research
                <span className="group-hover:translate-x-0.5 transition-transform">→</span>
              </Link>
            </div>
          </div>
        </div>

        {/* Three-Layer Architecture Visualization */}
        <div className="mb-8 bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-3xl p-6 border border-amber-200/50 dark:border-amber-800/30 shadow-lg">
          <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-4 flex items-center gap-2">
            <span className="text-2xl">🏗️</span> Three-Layer Architecture
          </h3>
          <div className="grid grid-cols-3 gap-4">
            <div className="bg-gradient-to-br from-blue-50 to-cyan-50 dark:from-blue-950/50 dark:to-cyan-950/50 rounded-2xl p-4 border-2 border-blue-200 dark:border-blue-800">
              <div className="flex items-center gap-2 mb-2">
                <span className="text-2xl">📁</span>
                <h4 className="font-bold text-blue-700 dark:text-blue-300">Layer 1: Raw Sources</h4>
              </div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Immutable documents (PDFs, URLs, notes, data)</p>
              <div className="mt-2 text-xs font-mono bg-blue-100 dark:bg-blue-900/30 rounded px-2 py-1">{sources.length} sources</div>
            </div>
            
            <div className="bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-950/50 dark:to-pink-950/50 rounded-2xl p-4 border-2 border-purple-200 dark:border-purple-800 relative overflow-hidden">
              <div className="absolute top-0 right-0 w-20 h-20 bg-purple-200/30 dark:bg-purple-700/20 rounded-full blur-2xl"></div>
              <div className="relative">
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-2xl">📖</span>
                  <h4 className="font-bold text-purple-700 dark:text-purple-300">Layer 2: Skill Wiki</h4>
                </div>
                <p className="text-sm text-gray-600 dark:text-gray-400">LLM-generated structured knowledge with cross-references</p>
                <div className="mt-2 text-xs font-mono bg-purple-100 dark:bg-purple-900/30 rounded px-2 py-1">{wikiPages.length} wiki pages</div>
              </div>
            </div>
            
            <div className="bg-gradient-to-br from-amber-50 to-orange-50 dark:from-amber-950/50 dark:to-orange-950/50 rounded-2xl p-4 border-2 border-amber-200 dark:border-amber-800">
              <div className="flex items-center gap-2 mb-2">
                <span className="text-2xl">⚙️</span>
                <h4 className="font-bold text-amber-700 dark:text-amber-300">Layer 3: Schema</h4>
              </div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Rules, conventions, and workflow configurations</p>
              <div className="mt-2 text-xs font-mono bg-amber-100 dark:bg-amber-900/30 rounded px-2 py-1">Active</div>
            </div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex gap-2 mb-6 flex-wrap">
          {[
            { id: 'overview', icon: '📊', label: 'Overview' },
            { id: 'ingest', icon: '📥', label: 'Ingest' },
            { id: 'query', icon: '🔍', label: 'Query' },
            { id: 'graph', icon: '🕸️', label: 'Knowledge Graph' },
            { id: 'lint', icon: '✅', label: 'Lint & Review' },
            { id: 'sources', icon: '📁', label: 'Sources' },
            { id: 'wiki', icon: '📝', label: 'Wiki Pages' },
            { id: 'timeline', icon: '📊', label: 'Evolution Timeline' },
            { id: 'span-tree', icon: '🌳', label: 'Span Tree' },
            { id: 'cost-analytics', icon: '💰', label: 'Cost Analytics' },
            { id: 'trace-viewer', icon: '🔍', label: 'Trace Viewer' }
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-5 py-2.5 rounded-xl font-semibold transition-all duration-200 flex items-center gap-2 ${
                activeTab === tab.id
                  ? 'bg-gradient-to-r from-amber-500 to-orange-500 text-white shadow-lg shadow-orange-500/25'
                  : 'bg-white/70 dark:bg-gray-800/70 text-gray-700 dark:text-gray-300 hover:bg-amber-50 dark:hover:bg-amber-950/30 border border-gray-200 dark:border-gray-700'
              }`}
            >
              <span>{tab.icon}</span> {tab.label}
            </button>
          ))}
        </div>

        {/* Tab Content */}
        <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-3xl p-8 border border-gray-200/50 dark:border-gray-700/50 shadow-xl min-h-[600px]">
          
          {/* OVERVIEW TAB */}
          {activeTab === 'overview' && (
            <div>
              <h2 className="text-3xl font-black text-gray-800 dark:text-white mb-6">System Dashboard</h2>
              
              {/* Metrics Grid */}
              <div className="grid grid-cols-4 gap-4 mb-8">
                <div className="bg-gradient-to-br from-blue-500 to-cyan-500 rounded-2xl p-5 text-white shadow-lg">
                  <div className="text-4xl font-black">{sources.length}</div>
                  <div className="text-sm opacity-90 mt-1">Raw Sources</div>
                  <div className="text-xs opacity-75 mt-2">+2 this week</div>
                </div>
                
                <div className="bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl p-5 text-white shadow-lg">
                  <div className="text-4xl font-black">{wikiPages.length}</div>
                  <div className="text-sm opacity-90 mt-1">Wiki Pages</div>
                  <div className="text-xs opacity-75 mt-2">Avg quality: 91.4%</div>
                </div>
                
                <div className="bg-gradient-to-br from-amber-500 to-orange-500 rounded-2xl p-5 text-white shadow-lg">
                  <div className="text-4xl font-black">{knowledgeGraph.edges.length}</div>
                  <div className="text-sm opacity-90 mt-1">Graph Edges</div>
                  <div className="text-xs opacity-75 mt-2">73% connected</div>
                </div>
                
                <div className="bg-gradient-to-br from-emerald-500 to-teal-500 rounded-2xl p-5 text-white shadow-lg">
                  <div className="text-4xl font-black">89%</div>
                  <div className="text-sm opacity-90 mt-1">System Health</div>
                  <div className="text-xs opacity-75 mt-2">All systems operational</div>
                </div>
              </div>

              {/* Recent Activity Timeline */}
              <div className="mb-8">
                <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-4 flex items-center gap-2">
                  <span>⏱️</span> Recent Activity Log
                </h3>
                <div className="space-y-3">
                  {[
                    { time: '2 min ago', action: 'INGEST', detail: 'Processed "LLM Training Techniques" article', status: 'success' },
                    { time: '15 min ago', action: 'QUERY', detail: 'Answered question about evolution strategies', status: 'success' },
                    { time: '1 hour ago', action: 'LINT', detail: 'Completed consistency check (42/47 passed)', status: 'warning' },
                    { time: '3 hours ago', action: 'INGEST', detail: 'Added meeting notes to knowledge base', status: 'success' },
                    { time: '1 day ago', action: 'DEEP_RESEARCH', detail: 'Auto-discovered 5 new research papers on NAS', status: 'info' },
                  ].map((activity, idx) => (
                    <div key={idx} className={`flex items-start gap-3 p-3 rounded-xl ${
                      activity.status === 'success' ? 'bg-green-50 dark:bg-green-950/20' :
                      activity.status === 'warning' ? 'bg-yellow-50 dark:bg-yellow-950/20' :
                      'bg-blue-50 dark:bg-blue-950/20'
                    }`}>
                      <div className={`w-2 h-2 rounded-full mt-2 ${
                        activity.status === 'success' ? 'bg-green-500' :
                        activity.status === 'warning' ? 'bg-yellow-500' :
                        'bg-blue-500'
                      }`}></div>
                      <div className="flex-1">
                        <div className="flex items-center gap-2">
                          <span className="font-bold text-sm text-gray-800 dark:text-white">{activity.action}</span>
                          <span className="text-xs text-gray-500 dark:text-gray-400">{activity.time}</span>
                        </div>
                        <p className="text-sm text-gray-600 dark:text-gray-300">{activity.detail}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Quick Actions */}
              <div className="grid grid-cols-3 gap-4">
                <button
                  onClick={() => setActiveTab('ingest')}
                  className="p-5 bg-gradient-to-br from-blue-50 to-cyan-50 dark:from-blue-950/30 dark:to-cyan-950/30 rounded-2xl border-2 border-blue-200 dark:border-blue-800 hover:border-blue-400 dark:hover:border-blue-600 transition-all group"
                >
                  <div className="text-3xl mb-2 group-hover:scale-110 transition-transform inline-block">📥</div>
                  <div className="font-bold text-gray-800 dark:text-white">New Ingest</div>
                  <div className="text-xs text-gray-600 dark:text-gray-400 mt-1">Add sources to wiki</div>
                </button>
                
                <button
                  onClick={() => setActiveTab('query')}
                  className="p-5 bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-950/30 dark:to-pink-950/30 rounded-2xl border-2 border-purple-200 dark:border-purple-800 hover:border-purple-400 dark:hover:border-purple-600 transition-all group"
                >
                  <div className="text-3xl mb-2 group-hover:scale-110 transition-transform inline-block">💬</div>
                  <div className="font-bold text-gray-800 dark:text-white">Ask Question</div>
                  <div className="text-xs text-gray-600 dark:text-gray-400 mt-1">Query knowledge base</div>
                </button>
                
                <button
                  onClick={handleDeepResearch}
                  className="p-5 bg-gradient-to-br from-emerald-50 to-teal-50 dark:from-emerald-950/30 dark:to-teal-950/30 rounded-2xl border-2 border-emerald-200 dark:border-emerald-800 hover:border-emerald-400 dark:hover:border-emerald-600 transition-all group"
                >
                  <div className="text-3xl mb-2 group-hover:scale-110 transition-transform inline-block">🔬</div>
                  <div className="font-bold text-gray-800 dark:text-white">Deep Research</div>
                  <div className="text-xs text-gray-600 dark:text-gray-400 mt-1">Auto-discover & ingest</div>
                </button>
              </div>
            </div>
          )}

          {/* INGEST TAB - Two-Step Chain-of-Thought */}
          {activeTab === 'ingest' && (
            <div>
              <h2 className="text-3xl font-black text-gray-800 dark:text-white mb-6 flex items-center gap-3">
                <span className="text-4xl">📥</span> Ingest Operation
                <span className="text-sm font-normal text-gray-500 dark:text-gray-400">(Two-Step Chain-of-Thought)</span>
              </h2>
              
              <div className="grid grid-cols-2 gap-6 mb-6">
                {/* Step 1: Analysis */}
                <div className="bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-950/30 dark:to-indigo-950/30 rounded-2xl p-6 border-2 border-blue-200 dark:border-blue-800">
                  <div className="flex items-center gap-2 mb-4">
                    <div className="w-10 h-10 bg-blue-500 rounded-xl flex items-center justify-center text-white font-bold text-xl">1</div>
                    <h3 className="text-xl font-bold text-blue-700 dark:text-blue-300">Analysis Phase</h3>
                  </div>
                  <ul className="space-y-2 text-sm text-gray-700 dark:text-gray-300">
                    <li className="flex items-start gap-2"><span className="text-blue-500">•</span> Read and parse raw source content</li>
                    <li className="flex items-start gap-2"><span className="text-blue-500">•</span> Extract key entities, concepts, arguments</li>
                    <li className="flex items-start gap-2"><span className="text-blue-500">•</span> Identify connections to existing wiki pages</li>
                    <li className="flex items-start gap-2"><span className="text-blue-500">•</span> Flag contradictions with current knowledge</li>
                    <li className="flex items-start gap-2"><span className="text-blue-500">•</span> Generate structured analysis object</li>
                  </ul>
                </div>

                {/* Step 2: Generation */}
                <div className="bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-950/30 dark:to-pink-950/30 rounded-2xl p-6 border-2 border-purple-200 dark:border-purple-800">
                  <div className="flex items-center gap-2 mb-4">
                    <div className="w-10 h-10 bg-purple-500 rounded-xl flex items-center justify-center text-white font-bold text-xl">2</div>
                    <h3 className="text-xl font-bold text-purple-700 dark:text-purple-300">Generation Phase</h3>
                  </div>
                  <ul className="space-y-2 text-sm text-gray-700 dark:text-gray-300">
                    <li className="flex items-start gap-2"><span className="text-purple-500">•</span> Create source summary with frontmatter</li>
                    <li className="flex items-start gap-2"><span className="text-purple-500">•</span> Generate entity/concept pages</li>
                    <li className="flex items-start gap-2"><span className="text-purple-500">•</span> Add [[wikilinks]] cross-references</li>
                    <li className="flex items-start gap-2"><span className="text-purple-500">•</span> Update index.md and log.md</li>
                    <li className="flex items-start gap-2"><span className="text-purple-500">•</span> Create review items for human check</li>
                  </ul>
                </div>
              </div>

              {/* Progress Display */}
              {(isIngesting || ingestProgress.progress === 100) && (
                <div className="mb-6 bg-gray-50 dark:bg-gray-900 rounded-2xl p-6 border border-gray-200 dark:border-gray-700">
                  <div className="flex items-center justify-between mb-3">
                    <span className="font-bold text-gray-800 dark:text-white">Processing Status</span>
                    <span className="text-sm font-mono text-blue-600 dark:text-blue-400">{ingestProgress.progress}%</span>
                  </div>
                  <div className="w-full h-3 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 transition-all duration-500"
                      style={{ width: `${ingestProgress.progress}%` }}
                    ></div>
                  </div>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">{ingestProgress.stage}</p>
                </div>
              )}

              {/* Start Ingest Button */}
              <button
                onClick={handleIngest}
                disabled={isIngesting}
                className={`w-full py-4 rounded-2xl font-bold text-lg transition-all duration-300 flex items-center justify-center gap-3 ${
                  isIngesting
                    ? 'bg-gray-300 dark:bg-gray-700 text-gray-500 cursor-not-allowed'
                    : 'bg-gradient-to-r from-amber-500 via-orange-500 to-red-500 hover:from-amber-600 hover:to-red-600 text-white shadow-xl shadow-orange-500/25 hover:shadow-2xl hover:shadow-orange-500/40 transform hover:scale-[1.02]'
                }`}
              >
                <span className="text-2xl">🚀</span>
                {isIngesting ? 'Processing...' : 'Start Ingest Pipeline'}
              </button>

              {/* Pending Sources List */}
              <div className="mt-6">
                <h3 className="text-lg font-bold text-gray-800 dark:text-white mb-3">Source Queue ({sources.filter(s => s.status !== 'ingested').length} pending)</h3>
                <div className="space-y-2">
                  {sources.map(source => (
                    <div key={source.id} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-900 rounded-xl">
                      <div className="flex items-center gap-3">
                        <span className="text-xl">{source.type === 'pdf' ? '📄' : source.type === 'md' ? '📝' : source.type === 'url' ? '🔗' : '📊'}</span>
                        <div>
                          <div className="font-medium text-gray-800 dark:text-white text-sm">{source.name}</div>
                          <div className="text-xs text-gray-500 dark:text-gray-400">{source.size} • {source.hash || 'Not hashed'}</div>
                        </div>
                      </div>
                      <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                        source.status === 'ingested' ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400' :
                        source.status === 'processing' ? 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400' :
                        'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400'
                      }`}>
                        {source.status}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* QUERY TAB - Four-Phase Retrieval */}
          {activeTab === 'query' && (
            <div>
              <h2 className="text-3xl font-black text-gray-800 dark:text-white mb-6 flex items-center gap-3">
                <span className="text-4xl">🔍</span> Query Engine
                <span className="text-sm font-normal text-gray-500 dark:text-gray-400">(Four-Phase Retrieval)</span>
              </h2>

              {/* Query Input */}
              <div className="mb-6">
                <div className="flex gap-3">
                  <input
                    type="text"
                    value={queryInput}
                    onChange={(e) => setQueryInput(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleQuery()}
                    placeholder="Ask anything about your accumulated knowledge..."
                    className="flex-1 px-5 py-4 rounded-2xl border-2 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 text-gray-800 dark:text-white focus:outline-none focus:border-purple-400 dark:focus:border-purple-600 text-lg"
                  />
                  <button
                    onClick={handleQuery}
                    className="px-8 py-4 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white rounded-2xl font-bold text-lg shadow-lg shadow-purple-500/25 transition-all duration-300 hover:shadow-xl"
                  >
                    Query
                  </button>
                </div>
              </div>

              {/* Query Results */}
              {queryResults && (
                <div className="space-y-4">
                  <div className="bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-950/20 dark:to-emerald-950/20 rounded-2xl p-6 border-2 border-green-200 dark:border-green-800">
                    <div className="flex items-center justify-between mb-3">
                      <h3 className="font-bold text-green-700 dark:text-green-300">Answer Synthesis</h3>
                      <div className="flex items-center gap-2 text-sm">
                        <span className="px-3 py-1 bg-green-500 text-white rounded-full font-bold">{Math.round(queryResults.confidence * 100)}% Confidence</span>
                        <span className="text-gray-500 dark:text-gray-400">{queryResults.graphNodesVisited} nodes visited</span>
                      </div>
                    </div>
                    <p className="text-gray-700 dark:text-gray-300 whitespace-pre-line leading-relaxed">{queryResults.answer}</p>
                    
                    <div className="mt-4 pt-4 border-t border-green-200 dark:border-green-800">
                      <div className="text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">Cited Sources:</div>
                      <div className="flex flex-wrap gap-2">
                        {queryResults.sources.map((src, i) => (
                          <span key={i} className="px-3 py-1 bg-white dark:bg-gray-800 rounded-lg text-sm text-purple-600 dark:text-purple-400 border border-purple-200 dark:border-purple-800">
                            {src}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Query Phases Explanation */}
              {!queryResults && (
                <div className="grid grid-cols-2 gap-4">
                  <div className="p-4 bg-blue-50 dark:bg-blue-950/20 rounded-xl border border-blue-200 dark:border-blue-800">
                    <div className="font-bold text-blue-700 dark:text-blue-300 mb-2">Phase 1: Tokenized Search</div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Fast keyword matching across all wiki content with fuzzy matching</p>
                  </div>
                  <div className="p-4 bg-purple-50 dark:bg-purple-950/20 rounded-xl border border-purple-200 dark:border-purple-800">
                    <div className="font-bold text-purple-700 dark:text-purple-300 mb-2">Phase 2: Graph Expansion</div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Traverse knowledge graph to find related concepts and entities</p>
                  </div>
                  <div className="p-4 bg-pink-50 dark:pink-950/20 rounded-xl border border-pink-200 dark:border-pink-800">
                    <div className="font-bold text-pink-700 dark:text-pink-300 mb-2">Phase 3: Budget Control</div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Limit context window by relevance score and token count</p>
                  </div>
                  <div className="p-4 bg-amber-50 dark:amber-950/20 rounded-xl border border-amber-200 dark:border-amber-800">
                    <div className="font-bold text-amber-700 dark:text-amber-300 mb-2">Phase 4: Context Assembly</div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Compile relevant passages with source citations for LLM synthesis</p>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* KNOWLEDGE GRAPH TAB */}
          {activeTab === 'graph' && (
            <div>
              <h2 className="text-3xl font-black text-gray-800 dark:text-white mb-6 flex items-center gap-3">
                <span className="text-4xl">🕸️</span> Knowledge Graph Visualization
              </h2>

              {/* Interactive Graph Canvas */}
              <div className="bg-gradient-to-br from-slate-100 to-gray-200 dark:from-slate-900 dark:to-gray-800 rounded-2xl p-8 min-h-[400px] relative overflow-hidden border-2 border-gray-300 dark:border-gray-700">
                {/* Simplified graph visualization using CSS positioning */}
                <svg viewBox="0 0 800 400" className="w-full h-full">
                  {/* Edges (drawn first so they're behind nodes) */}
                  {knowledgeGraph.edges.map((edge, idx) => {
                    const sourceNode = knowledgeGraph.nodes.find(n => n.id === edge.source);
                    const targetNode = knowledgeGraph.nodes.find(n => n.id === edge.target);
                    if (!sourceNode || !targetNode) return null;
                    
                    // Simple positioning based on node index
                    const sx = 150 + (knowledgeGraph.nodes.indexOf(sourceNode) % 3) * 250;
                    const sy = 100 + Math.floor(knowledgeGraph.nodes.indexOf(sourceNode) / 3) * 200;
                    const tx = 150 + (knowledgeGraph.nodes.indexOf(targetNode) % 3) * 250;
                    const ty = 100 + Math.floor(knowledgeGraph.nodes.indexOf(targetNode) / 3) * 200;
                    
                    return (
                      <line
                        key={idx}
                        x1={sx} y1={sy} x2={tx} y2={ty}
                        stroke={`rgba(${edge.weight > 0.8 ? '147, 51, 234' : '59, 130, 246'}, ${edge.weight})`}
                        strokeWidth={edge.weight * 3}
                        markerEnd="url(#arrowhead)"
                      />
                    );
                  })}
                  
                  <defs>
                    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                      <polygon points="0 0, 10 3.5, 0 7" fill="#9333ea" />
                    </marker>
                  </defs>

                  {/* Nodes */}
                  {knowledgeGraph.nodes.map((node, idx) => {
                    const cx = 150 + (idx % 3) * 250;
                    const cy = 100 + Math.floor(idx / 3) * 200;
                    const isSelected = selectedNode === node.id;
                    
                    return (
                      <g
                        key={node.id}
                        onClick={() => setSelectedNode(node.id)}
                        className="cursor-pointer"
                      >
                        <circle
                          cx={cx} cy={cy} r={35 + node.connections}
                          fill={isSelected ? '#fbbf24' : `url(#gradient-${idx})`}
                          stroke={isSelected ? '#f59e0b' : '#fff'}
                          strokeWidth={3}
                          className="transition-all duration-300 hover:r-[50]"
                        />
                        <defs>
                          <radialGradient id={`gradient-${idx}`}>
                            <stop offset="0%" stopColor={
                              node.group === 'research' ? '#3b82f6' :
                              node.group === 'algorithm' ? '#8b5cf6' :
                              node.group === 'technique' ? '#ec4899' :
                              node.group === 'model' ? '#10b981' :
                              '#f59e0b'
                            } stopOpacity="0.8" />
                            <stop offset="100%" stopColor={
                              node.group === 'research' ? '#1d4ed8' :
                              node.group === 'algorithm' ? '#6d28d9' :
                              node.group === 'technique' ? '#be185d' :
                              node.group === 'model' ? '#059669' :
                              '#d97706'
                            } stopOpacity="1" />
                          </radialGradient>
                        </defs>
                        <text
                          x={cx} y={cy + 5}
                          textAnchor="middle"
                          fill="white"
                          fontSize="11"
                          fontWeight="bold"
                          className="pointer-events-none"
                        >
                          {node.label.length > 12 ? node.label.substring(0, 12) + '...' : node.label}
                        </text>
                        <text
                          x={cx} y={cy + 55}
                          textAnchor="middle"
                          fill="#6b7280"
                          fontSize="10"
                          className="pointer-events-none"
                        >
                          {node.connections} links
                        </text>
                      </g>
                    );
                  })}
                </svg>
              </div>

              {/* Selected Node Details */}
              {selectedNode && (() => {
                const node = knowledgeGraph.nodes.find(n => n.id === selectedNode);
                return node ? (
                  <div className="mt-4 p-4 bg-amber-50 dark:amber-950/20 rounded-xl border border-amber-200 dark:border-amber-800">
                    <h4 className="font-bold text-amber-700 dark:text-amber-300 text-lg mb-2">{node.label}</h4>
                    <div className="grid grid-cols-3 gap-3 text-sm">
                      <div><span className="text-gray-500 dark:text-gray-400">Group:</span> <span className="font-medium text-gray-800 dark:text-white capitalize">{node.group}</span></div>
                      <div><span className="text-gray-500 dark:text-gray-400">Connections:</span> <span className="font-medium text-gray-800 dark:text-white">{node.connections}</span></div>
                      <div><span className="text-gray-500 dark:text-gray-400">Type:</span> <span className="font-medium text-gray-800 dark:text-white">Entity</span></div>
                    </div>
                  </div>
                ) : null;
              })()}

              {/* Graph Statistics */}
              <div className="mt-4 grid grid-cols-4 gap-3">
                <div className="text-center p-3 bg-blue-50 dark:bg-blue-950/20 rounded-xl">
                  <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">{knowledgeGraph.nodes.length}</div>
                  <div className="text-xs text-gray-600 dark:text-gray-400">Total Nodes</div>
                </div>
                <div className="text-center p-3 bg-purple-50 dark:bg-purple-950/20 rounded-xl">
                  <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">{knowledgeGraph.edges.length}</div>
                  <div className="text-xs text-gray-600 dark:text-gray-400">Total Edges</div>
                </div>
                <div className="text-center p-3 bg-pink-50 dark:bg-pink-950/20 rounded-xl">
                  <div className="text-2xl font-bold text-pink-600 dark:text-pink-400">73%</div>
                  <div className="text-xs text-gray-600 dark:text-gray-400">Connectivity</div>
                </div>
                <div className="text-center p-3 bg-amber-50 dark:amber-950/20 rounded-xl">
                  <div className="text-2xl font-bold text-amber-600 dark:text-amber-400">0.84</div>
                  <div className="text-xs text-gray-600 dark:text-gray-400">Avg Weight</div>
                </div>
              </div>
            </div>
          )}

          {/* LINT TAB */}
          {activeTab === 'lint' && (
            <div>
              <h2 className="text-3xl font-black text-gray-800 dark:text-white mb-6 flex items-center gap-3">
                <span className="text-4xl">✅</span> Lint & Quality Assurance
              </h2>

              <button
                onClick={handleLint}
                className="mb-6 px-6 py-3 bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-600 hover:to-teal-600 text-white rounded-xl font-bold shadow-lg transition-all duration-300 flex items-center gap-2"
              >
                <span className="text-xl">🔍</span> Run Lint Check
              </button>

              {lintReport && (
                <div className="space-y-4">
                  {/* Summary Stats */}
                  <div className="grid grid-cols-4 gap-3">
                    <div className="p-4 bg-blue-50 dark:bg-blue-950/20 rounded-xl text-center">
                      <div className="text-3xl font-black text-blue-600 dark:text-blue-400">{lintReport.totalChecks}</div>
                      <div className="text-sm text-gray-600 dark:text-gray-400">Total Checks</div>
                    </div>
                    <div className="p-4 bg-green-50 dark:bg-green-950/20 rounded-xl text-center">
                      <div className="text-3xl font-black text-green-600 dark:text-green-400">{lintReport.passed}</div>
                      <div className="text-sm text-gray-600 dark:text-gray-400">Passed ✅</div>
                    </div>
                    <div className="p-4 bg-yellow-50 dark:bg-yellow-950/20 rounded-xl text-center">
                      <div className="text-3xl font-black text-yellow-600 dark:text-yellow-400">{lintReport.warnings}</div>
                      <div className="text-sm text-gray-600 dark:text-gray-400">Warnings ⚠️</div>
                    </div>
                    <div className="p-4 bg-red-50 dark:bg-red-950/20 rounded-xl text-center">
                      <div className="text-3xl font-black text-red-600 dark:text-red-400">{lintReport.errors}</div>
                      <div className="text-sm text-gray-600 dark:text-gray-400">Errors ❌</div>
                    </div>
                  </div>

                  {/* Issues List */}
                  <div className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-700 overflow-hidden">
                    <div className="px-4 py-3 bg-gray-50 dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 font-bold text-gray-800 dark:text-white">
                      Detected Issues
                    </div>
                    {lintReport.issues.map((issue, idx) => (
                      <div key={idx} className={`p-4 border-b border-gray-100 dark:border-gray-800 ${
                        issue.severity === 'error' ? 'bg-red-50 dark:bg-red-950/10' :
                        issue.severity === 'warning' ? 'bg-yellow-50 dark:bg-yellow-950/10' :
                        'bg-blue-50 dark:bg-blue-950/10'
                      }`}>
                        <div className="flex items-start gap-3">
                          <span className="text-xl">
                            {issue.severity === 'error' ? '❌' :
                             issue.severity === 'warning' ? '⚠️' : 'ℹ️'}
                          </span>
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-1">
                              <span className="font-bold text-sm text-gray-800 dark:text-white">{issue.type}</span>
                              <span className="text-xs px-2 py-0.5 rounded bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-400">{issue.location}</span>
                            </div>
                            <p className="text-sm text-gray-600 dark:text-gray-400">{issue.message}</p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* Recommendations */}
                  <div className="p-4 bg-emerald-50 dark:bg-emerald-950/20 rounded-xl border border-emerald-200 dark:border-emerald-800">
                    <h4 className="font-bold text-emerald-700 dark:text-emerald-300 mb-2">💡 Recommendations</h4>
                    <ul className="space-y-1">
                      {lintReport.recommendations.map((rec, idx) => (
                        <li key={idx} className="text-sm text-gray-700 dark:text-gray-300 flex items-start gap-2">
                          <span className="text-emerald-500">→</span> {rec}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* SOURCES TAB */}
          {activeTab === 'sources' && (
            <div>
              <h2 className="text-3xl font-black text-gray-800 dark:text-white mb-6 flex items-center gap-3">
                <span className="text-4xl">📁</span> Raw Sources Library
                <span className="text-sm font-normal text-gray-500 dark:text-gray-400">(Immutable - Read Only)</span>
              </h2>

              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b-2 border-gray-200 dark:border-gray-700">
                      <th className="text-left py-3 px-4 text-gray-700 dark:text-gray-300 font-bold">Name</th>
                      <th className="text-left py-3 px-4 text-gray-700 dark:text-gray-300 font-bold">Type</th>
                      <th className="text-left py-3 px-4 text-gray-700 dark:text-gray-300 font-bold">Size</th>
                      <th className="text-left py-3 px-4 text-gray-700 dark:text-gray-300 font-bold">Status</th>
                      <th className="text-left py-3 px-4 text-gray-700 dark:text-gray-300 font-bold">SHA256 Hash</th>
                      <th className="text-left py-3 px-4 text-gray-700 dark:text-gray-300 font-bold">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {sources.map(source => (
                      <tr key={source.id} className="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-900/50">
                        <td className="py-3 px-4">
                          <div className="flex items-center gap-2">
                            <span className="text-xl">{source.type === 'pdf' ? '📄' : source.type === 'md' ? '📝' : source.type === 'url' ? '🔗' : '📊'}</span>
                            <span className="font-medium text-gray-800 dark:text-white text-sm">{source.name}</span>
                          </div>
                        </td>
                        <td className="py-3 px-4">
                          <span className="px-2 py-1 bg-gray-100 dark:bg-gray-800 rounded text-xs font-mono text-gray-600 dark:text-gray-400 uppercase">{source.type}</span>
                        </td>
                        <td className="py-3 px-4 text-sm text-gray-600 dark:text-gray-400">{source.size}</td>
                        <td className="py-3 px-4">
                          <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                            source.status === 'ingested' ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400' :
                            source.status === 'processing' ? 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400' :
                            'bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400'
                          }`}>{source.status}</span>
                        </td>
                        <td className="py-3 px-4">
                          <code className="text-xs font-mono text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded">
                            {source.hash || 'Pending...'}
                          </code>
                        </td>
                        <td className="py-3 px-4">
                          <button className="text-sm text-blue-600 dark:text-blue-400 hover:underline font-medium">View</button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-950/20 rounded-xl border border-blue-200 dark:border-blue-800">
                <p className="text-sm text-blue-700 dark:text-blue-300">
                  <strong>💡 Note:</strong> All raw sources are immutable. The LLM reads from this layer but never modifies it. Changes only happen in the Wiki layer (Layer 2).
                </p>
              </div>
            </div>
          )}

          {/* WIKI PAGES TAB */}
          {activeTab === 'wiki' && (
            <div>
              <h2 className="text-3xl font-black text-gray-800 dark:text-white mb-6 flex items-center gap-3">
                <span className="text-4xl">📝</span> Wiki Pages Index
                <span className="text-sm font-normal text-gray-500 dark:text-gray-400">(LLM-Generated & Maintained)</span>
              </h2>

              <div className="grid grid-cols-2 gap-4">
                {wikiPages.map(page => (
                  <div key={page.id} className="p-5 bg-gradient-to-br from-white to-gray-50 dark:from-gray-800 dark:to-gray-900 rounded-2xl border-2 border-gray-200 dark:border-gray-700 hover:border-purple-400 dark:hover:border-purple-600 transition-all group">
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex items-center gap-2">
                        <span className="text-2xl">
                          {page.type === 'entity' ? '🏷️' :
                           page.type === 'concept' ? '💡' :
                           page.type === 'summary' ? '📋' :
                           page.type === 'comparison' ? '⚖️' :
                           '📊'}
                        </span>
                        <div>
                          <h3 className="font-bold text-gray-800 dark:text-white group-hover:text-purple-600 dark:group-hover:text-purple-400 transition-colors">{page.title}</h3>
                          <span className="text-xs px-2 py-0.5 bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-400 rounded font-medium uppercase">{page.type}</span>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-lg font-black text-green-600 dark:text-green-400">{page.quality}%</div>
                        <div className="text-xs text-gray-500 dark:text-gray-400">quality</div>
                      </div>
                    </div>
                    
                    <div className="flex items-center justify-between text-sm text-gray-600 dark:text-gray-400">
                      <div className="flex items-center gap-3">
                        <span className="flex items-center gap-1">
                          <span>🔗</span> {page.links} cross-references
                        </span>
                        <span className="flex items-center gap-1">
                          <span>🕐</span> {page.lastUpdated}
                        </span>
                      </div>
                      <button className="text-purple-600 dark:text-purple-400 hover:underline font-medium">Read →</button>
                    </div>
                  </div>
                ))}
              </div>

              <div className="mt-6 p-4 bg-purple-50 dark:bg-purple-950/20 rounded-xl border border-purple-200 dark:border-purple-800">
                <p className="text-sm text-purple-700 dark:text-purple-300">
                  <strong>🤖 AI-Maintained:</strong> All wiki pages are automatically generated and updated by the LLM during ingest operations. Humans curate sources; the LLM handles all summarizing, cross-referencing, and maintenance.
                </p>
              </div>
            </div>
          )}

          {/* EVOLUTION TIMELINE TAB - OctoTrace Integration */}
          {activeTab === 'timeline' && (
            <div>
              <h2 className="text-3xl font-black text-gray-800 dark:text-white mb-6 flex items-center gap-3">
                <span className="text-4xl">📊</span> Evolution Timeline
                <span className="text-sm font-normal text-gray-500 dark:text-gray-400">(OctoTrace Deep Integration)</span>
              </h2>

              {/* Timeline Statistics */}
              <div className="grid grid-cols-4 gap-4 mb-6">
                <div className="bg-gradient-to-br from-blue-500 to-cyan-500 rounded-2xl p-5 text-white shadow-lg">
                  <div className="text-3xl font-black">{evolutionTimeline.length}</div>
                  <div className="text-sm opacity-90 mt-1">Total Operations</div>
                  <div className="text-xs opacity-75 mt-2">Last 45 minutes</div>
                </div>
                
                <div className="bg-gradient-to-br from-green-500 to-emerald-500 rounded-2xl p-5 text-white shadow-lg">
                  <div className="text-3xl font-black">{evolutionTimeline.filter(t => t.operation === 'INGEST').length}</div>
                  <div className="text-sm opacity-90 mt-1">Ingest Operations</div>
                  <div className="text-xs opacity-75 mt-2">Sources processed</div>
                </div>
                
                <div className="bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl p-5 text-white shadow-lg">
                  <div className="text-3xl font-black">${(evolutionTimeline.reduce((sum, t) => sum + parseFloat(t.cost.replace('$', '')), 0)).toFixed(3)}</div>
                  <div className="text-sm opacity-90 mt-1">Total Cost</div>
                  <div className="text-xs opacity-75 mt-2">LLM API usage</div>
                </div>
                
                <div className="bg-gradient-to-br from-amber-500 to-orange-500 rounded-2xl p-5 text-white shadow-lg">
                  <div className="text-3xl font-black">{evolutionTimeline.reduce((sum, t) => sum + t.tokens, 0).toLocaleString()}</div>
                  <div className="text-sm opacity-90 mt-1">Total Tokens</div>
                  <div className="text-xs opacity-75 mt-2">Across all ops</div>
                </div>
              </div>

              {/* Interactive Timeline */}
              <div className="space-y-3">
                <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-4 flex items-center gap-2">
                  <span>⏱️</span> Operation Timeline (Chronological Order)
                </h3>
                
                {evolutionTimeline.map((event, idx) => (
                  <div key={idx} className={`flex items-start gap-4 p-4 rounded-xl border-2 transition-all hover:shadow-lg ${
                    event.operation === 'INGEST' ? 'bg-blue-50 dark:bg-blue-950/20 border-blue-200 dark:border-blue-800' :
                    event.operation === 'QUERY' ? 'bg-purple-50 dark:bg-purple-950/20 border-purple-200 dark:border-purple-800' :
                    event.operation === 'LINT' ? 'bg-yellow-50 dark:bg-yellow-950/20 border-yellow-200 dark:border-yellow-800' :
                    'bg-emerald-50 dark:bg-emerald-950/20 border-emerald-200 dark:border-emerald-800'
                  }`}>
                    {/* Timestamp & Operation Type */}
                    <div className="flex-shrink-0 w-32">
                      <div className="text-xs font-mono text-gray-500 dark:text-gray-400 mb-1">
                        {new Date(event.timestamp).toLocaleTimeString()}
                      </div>
                      <span className={`px-2 py-1 rounded-full text-xs font-bold ${
                        event.operation === 'INGEST' ? 'bg-blue-500 text-white' :
                        event.operation === 'QUERY' ? 'bg-purple-500 text-white' :
                        event.operation === 'LINT' ? 'bg-yellow-500 text-white' :
                        'bg-emerald-500 text-white'
                      }`}>
                        {event.operation}
                      </span>
                    </div>

                    {/* Event Details */}
                    <div className="flex-1">
                      <div className="font-bold text-gray-800 dark:text-white text-sm mb-1">{event.source}</div>
                      <div className="text-sm text-gray-600 dark:text-gray-400 mb-2">{event.details}</div>
                      
                      {/* Metrics Row */}
                      <div className="flex items-center gap-4 text-xs">
                        <span className="flex items-center gap-1 text-gray-500 dark:text-gray-400">
                          <span>⏱️</span> {event.duration}
                        </span>
                        <span className="flex items-center gap-1 text-gray-500 dark:text-gray-400">
                          <span>🔤</span> {event.tokens.toLocaleString()} tokens
                        </span>
                        <span className="flex items-center gap-1 text-gray-500 dark:text-gray-400">
                          <span>💰</span> {event.cost}
                        </span>
                        <span className="font-mono text-blue-600 dark:text-blue-400 bg-blue-100 dark:bg-blue-900/30 px-2 py-0.5 rounded">
                          {event.spanId}
                        </span>
                      </div>
                    </div>

                    {/* Action Button */}
                    <button 
                      onClick={() => setActiveTab('span-tree')}
                      className="flex-shrink-0 px-3 py-1.5 bg-white dark:bg-gray-800 rounded-lg text-xs font-medium text-cyan-600 dark:text-cyan-400 border border-cyan-200 dark:border-cyan-800 hover:bg-cyan-50 dark:hover:bg-cyan-950/30 transition-all"
                    >
                      View Span →
                    </button>
                  </div>
                ))}
              </div>

              {/* Timeline Visualization Bar */}
              <div className="mt-6 p-5 bg-gray-50 dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-700">
                <h4 className="font-bold text-gray-800 dark:text-white mb-3">📈 Activity Density (Last Hour)</h4>
                <div className="flex items-end gap-1 h-24">
                  {[...Array(12)].map((_, i) => {
                    const height = Math.random() * 80 + 20;
                    return (
                      <div 
                        key={i} 
                        className="flex-1 bg-gradient-to-t from-cyan-400 to-blue-500 rounded-t opacity-70 hover:opacity-100 transition-opacity cursor-pointer relative group"
                        style={{ height: `${height}%` }}
                      >
                        <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 bg-gray-900 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none">
                          {i * 5}-{i * 5 + 5} min ago
                        </div>
                      </div>
                    );
                  })}
                </div>
                <div className="flex justify-between mt-2 text-xs text-gray-500 dark:text-gray-400">
                  <span>60 min ago</span>
                  <span>55</span>
                  <span>50</span>
                  <span>45</span>
                  <span>40</span>
                  <span>35</span>
                  <span>30</span>
                  <span>25</span>
                  <span>20</span>
                  <span>15</span>
                  <span>10</span>
                  <span>5</span>
                  <span>Now</span>
                </div>
              </div>

              {/* Export Options */}
              <div className="mt-6 flex gap-3">
                <Link 
                  to="/octo-trace" 
                  className="px-5 py-2.5 bg-gradient-to-r from-cyan-500 via-blue-500 to-indigo-500 hover:from-cyan-600 hover:to-indigo-600 text-white rounded-xl font-bold shadow-lg shadow-cyan-500/25 transition-all duration-300 flex items-center gap-2"
                >
                  <span className="text-lg">🔍</span> Open Full OctoTrace Dashboard
                </Link>
                
                <button className="px-5 py-2.5 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 border-2 border-gray-200 dark:border-gray-700 rounded-xl font-semibold hover:border-cyan-400 dark:hover:border-cyan-600 transition-all flex items-center gap-2">
                  <span className="text-lg">📥</span> Export Timeline JSON
                </button>
              </div>
            </div>
          )}

          {/* SPAN TREE TAB - Hierarchical Operation View */}
          {activeTab === 'span-tree' && (
            <div>
              <h2 className="text-3xl font-black text-gray-800 dark:text-white mb-6 flex items-center gap-3">
                <span className="text-4xl">🌳</span> Span Tree View
                <span className="text-sm font-normal text-gray-500 dark:text-gray-400">(Hierarchical Operation Structure)</span>
              </h2>

              {/* Root Span Info */}
              <div className="mb-6 p-5 bg-gradient-to-r from-indigo-50 via-purple-50 to-pink-50 dark:from-indigo-950/20 dark:via-purple-950/20 dark:to-pink-950/20 rounded-2xl border-2 border-indigo-200 dark:border-indigo-800">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 bg-gradient-to-br from-indigo-500 to-purple-500 rounded-xl flex items-center justify-center text-white text-2xl font-black">
                      🌳
                    </div>
                    <div>
                      <h3 className="text-xl font-bold text-gray-800 dark:text-white">{spanTree.rootSpan.operation}</h3>
                      <div className="text-sm text-gray-600 dark:text-gray-400">
                        Started: {new Date(spanTree.rootSpan.startTime).toLocaleString()} • Duration: {spanTree.rootSpan.duration}
                      </div>
                    </div>
                  </div>
                  <span className={`px-4 py-2 rounded-full text-sm font-bold ${
                    spanTree.rootSpan.status === 'active' ? 'bg-green-500 text-white animate-pulse' : 'bg-gray-300 text-gray-700'
                  }`}>
                    {spanTree.rootSpan.status.toUpperCase()}
                  </span>
                </div>

                {/* Summary Stats */}
                <div className="grid grid-cols-4 gap-3 mt-4">
                  <div className="text-center p-3 bg-white/60 dark:bg-gray-900/60 rounded-xl">
                    <div className="text-2xl font-black text-indigo-600 dark:text-indigo-400">{spanTree.rootSpan.children.length}</div>
                    <div className="text-xs text-gray-600 dark:text-gray-400">Child Spans</div>
                  </div>
                  <div className="text-center p-3 bg-white/60 dark:bg-gray-900/60 rounded-xl">
                    <div className="text-2xl font-black text-purple-600 dark:text-purple-400">
                      {spanTree.rootSpan.children.reduce((sum, child) => sum + child.tokens, 0).toLocaleString()}
                    </div>
                    <div className="text-xs text-gray-600 dark:text-gray-400">Total Tokens</div>
                  </div>
                  <div className="text-center p-3 bg-white/60 dark:bg-gray-900/60 rounded-xl">
                    <div className="text-2xl font-black text-pink-600 dark:text-pink-400">
                      ${spanTree.rootSpan.children.reduce((sum, child) => sum + (child.tokens * 0.00001), 0).toFixed(3)}
                    </div>
                    <div className="text-xs text-gray-600 dark:text-gray-400">Est. Cost</div>
                  </div>
                  <div className="text-center p-3 bg-white/60 dark:bg-gray-900/60 rounded-xl">
                    <div className="text-2xl font-black text-emerald-600 dark:text-emerald-400">
                      {spanTree.rootSpan.children.filter(c => c.status === 'completed').length}/{spanTree.rootSpan.children.length}
                    </div>
                    <div className="text-xs text-gray-600 dark:text-gray-400">Completed</div>
                  </div>
                </div>
              </div>

              {/* Tree Visualization */}
              <div className="bg-white dark:bg-gray-900 rounded-2xl p-6 border-2 border-gray-200 dark:border-gray-700 overflow-x-auto">
                <div className="min-w-[800px]">
                  {/* Render tree structure */}
                  <div className="relative">
                    {/* Root node */}
                    <div className="flex items-center gap-4 mb-6">
                      <div className="w-48 p-4 bg-gradient-to-br from-indigo-500 to-purple-500 rounded-xl text-white shadow-lg">
                        <div className="font-bold text-sm">ROOT SPAN</div>
                        <div className="text-xs opacity-90">{spanTree.rootSpan.operation}</div>
                        <div className="mt-2 text-xs opacity-75">{spanTree.rootSpan.duration}</div>
                      </div>
                      <div className="flex-1 h-0.5 bg-gradient-to-r from-indigo-400 to-transparent"></div>
                    </div>

                    {/* Child spans */}
                    <div className="ml-24 space-y-4 border-l-2 border-indigo-200 dark:border-indigo-800 pl-6">
                      {spanTree.rootSpan.children.map((child, idx) => (
                        <div key={child.id}>
                          {/* Parent span row */}
                          <div className="flex items-start gap-4">
                            <div className={`w-56 p-4 rounded-xl text-white shadow-md transition-all hover:scale-105 ${
                              child.operation.includes('INGEST') ? 'bg-gradient-to-br from-blue-500 to-cyan-500' :
                              child.operation.includes('QUERY') ? 'bg-gradient-to-br from-purple-500 to-pink-500' :
                              child.operation.includes('LINT') ? 'bg-gradient-to-br from-yellow-500 to-orange-500' :
                              'bg-gradient-to-br from-emerald-500 to-teal-500'
                            }`}>
                              <div className="flex items-center justify-between mb-2">
                                <span className="font-bold text-xs">{child.operation.split(' - ')[0]}</span>
                                <span className={`px-2 py-0.5 rounded text-xs font-bold ${
                                  child.status === 'completed' ? 'bg-white/30' :
                                  child.status === 'in_progress' ? 'bg-white/40 animate-pulse' :
                                  'bg-gray-500/30'
                                }`}>
                                  {child.status.toUpperCase()}
                                </span>
                              </div>
                              <div className="text-xs opacity-90">{child.operation.includes(' - ') ? child.operation.split(' - ')[1] : ''}</div>
                              <div className="mt-2 flex justify-between text-xs opacity-75">
                                <span>{child.duration}</span>
                                <span>{child.tokens.toLocaleString()} tokens</span>
                              </div>
                            </div>

                            {/* Sub-spans if exist */}
                            {child.children && (
                              <div className="ml-4 mt-2 space-y-2">
                                <div className="w-0.5 h-full bg-gradient-to-b from-gray-300 to-transparent absolute ml-14"></div>
                                {child.children.map(subChild => (
                                  <div key={subChild.id} className="flex items-center gap-3 pl-4 border-l-2 border-gray-200 dark:border-gray-700">
                                    <div className={`w-44 p-3 rounded-lg text-sm ${
                                      subChild.status === 'completed' ? 'bg-green-50 dark:bg-green-950/20 text-green-700 dark:text-green-300 border border-green-200 dark:border-green-800' :
                                      subChild.status === 'in_progress' ? 'bg-yellow-50 dark:bg-yellow-950/20 text-yellow-700 dark:text-yellow-300 border border-yellow-200 dark:border-yellow-800 animate-pulse' :
                                      'bg-gray-50 dark:bg-gray-800 text-gray-600 dark:text-gray-400 border border-gray-200 dark:border-gray-700'
                                    }`}>
                                      <div className="font-medium text-xs">{subChild.operation}</div>
                                      <div className="text-xs opacity-70 mt-1">{subChild.duration} • {subChild.tokens} tokens</div>
                                    </div>
                                  </div>
                                ))}
                              </div>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              {/* Legend */}
              <div className="mt-6 flex items-center gap-6 justify-center text-sm">
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 rounded bg-gradient-to-br from-blue-500 to-cyan-500"></div>
                  <span className="text-gray-600 dark:text-gray-400">Ingest</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 rounded bg-gradient-to-br from-purple-500 to-pink-500"></div>
                  <span className="text-gray-600 dark:text-gray-400">Query</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 rounded bg-gradient-to-br from-yellow-500 to-orange-500"></div>
                  <span className="text-gray-600 dark:text-gray-400">Lint</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 rounded bg-gradient-to-br from-emerald-500 to-teal-500"></div>
                  <span className="text-gray-600 dark:text-gray-400">Deep Research</span>
                </div>
              </div>
            </div>
          )}

          {/* COST ANALYTICS TAB - Budget Monitoring */}
          {activeTab === 'cost-analytics' && (
            <div>
              <h2 className="text-3xl font-black text-gray-800 dark:text-white mb-6 flex items-center gap-3">
                <span className="text-4xl">💰</span> Cost Analytics Dashboard
                <span className="text-sm font-normal text-gray-500 dark:text-gray-400">(LLM Token Usage & Budget Tracking)</span>
              </h2>

              {/* Budget Overview */}
              <div className="mb-6 grid grid-cols-3 gap-4">
                <div className="bg-gradient-to-br from-emerald-500 to-teal-500 rounded-2xl p-6 text-white shadow-xl">
                  <div className="text-sm opacity-90 mb-2">Total Spend This Session</div>
                  <div className="text-4xl font-black">${costAnalytics.totalCost.toFixed(3)}</div>
                  <div className="mt-3 bg-white/20 rounded-full h-2 overflow-hidden">
                    <div 
                      className="h-full bg-white transition-all duration-500"
                      style={{ width: `${(costAnalytics.totalCost / costAnalytics.budget) * 100}%` }}
                    ></div>
                  </div>
                  <div className="text-xs opacity-75 mt-2">
                    {(costAnalytics.totalCost / costAnalytics.budget * 100).toFixed(1)}% of ${costAnalytics.budget.toFixed(2)} budget
                  </div>
                </div>

                <div className="bg-gradient-to-br from-blue-500 to-indigo-500 rounded-2xl p-6 text-white shadow-xl">
                  <div className="text-sm opacity-90 mb-2">Total Tokens Consumed</div>
                  <div className="text-4xl font-black">{(costAnalytics.totalTokens / 1000).toFixed(1)}K</div>
                  <div className="mt-3 space-y-1">
                    <div className="flex justify-between text-xs">
                      <span>Avg cost per 1K tokens</span>
                      <span>${((costAnalytics.totalCost / costAnalytics.totalTokens) * 1000).toFixed(4)}</span>
                    </div>
                  </div>
                </div>

                <div className="bg-gradient-to-br from-amber-500 to-orange-500 rounded-2xl p-6 text-white shadow-xl">
                  <div className="text-sm opacity-90 mb-2">Budget Remaining</div>
                  <div className="text-4xl font-black">${(costAnalytics.budget - costAnalytics.totalCost).toFixed(3)}</div>
                  <div className="text-xs opacity-75 mt-2">
                    Enough for ~{Math.floor((costAnalytics.budget - costAnalytics.totalCost) / 0.01)} more operations
                  </div>
                </div>
              </div>

              {/* Cost by Operation Type */}
              <div className="grid grid-cols-2 gap-4 mb-6">
                <div className="bg-white dark:bg-gray-900 rounded-2xl p-5 border-2 border-gray-200 dark:border-gray-700">
                  <h3 className="text-lg font-bold text-gray-800 dark:text-white mb-4">💸 Cost by Operation</h3>
                  <div className="space-y-3">
                    {Object.entries(costAnalytics.operations).map(([op, data]) => (
                      <div key={op} className="group">
                        <div className="flex justify-between items-center mb-1">
                          <span className="font-medium text-sm text-gray-700 dark:text-gray-300">{op}</span>
                          <span className="text-sm font-bold text-gray-800 dark:text-white">${data.cost.toFixed(3)} ({data.count}x)</span>
                        </div>
                        <div className="w-full h-2 bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden">
                          <div 
                            className={`h-full transition-all duration-500 group-hover:opacity-80 ${
                              op === 'DEEP_RESEARCH' ? 'bg-gradient-to-r from-emerald-400 to-teal-400' :
                              op === 'INGEST' ? 'bg-gradient-to-r from-blue-400 to-cyan-400' :
                              op === 'QUERY' ? 'bg-gradient-to-r from-purple-400 to-pink-400' :
                              'bg-gradient-to-r from-yellow-400 to-orange-400'
                            }`}
                            style={{ width: `${(data.cost / costAnalytics.totalCost) * 100}%` }}
                          ></div>
                        </div>
                        <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                          {data.tokens.toLocaleString()} tokens • Avg: {data.avgDuration}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="bg-white dark:bg-gray-900 rounded-2xl p-5 border-2 border-gray-200 dark:border-gray-700">
                  <h3 className="text-lg font-bold text-gray-800 dark:text-white mb-4">🔤 Token Distribution by Layer</h3>
                  <div className="space-y-3">
                    {Object.entries(costAnalytics.tokenByLayer).map(([layer, tokens]) => {
                      const percentage = (tokens / costAnalytics.totalTokens) * 100;
                      return (
                        <div key={layer} className="flex items-center gap-3">
                          <div className="w-28 text-sm font-medium text-gray-700 dark:text-gray-300 capitalize">
                            {layer.replace('_', ' ')}
                          </div>
                          <div className="flex-1 h-6 bg-gray-100 dark:bg-gray-800 rounded overflow-hidden relative">
                            <div 
                              className="h-full bg-gradient-to-r from-blue-400 to-purple-400 transition-all duration-500"
                              style={{ width: `${percentage}%` }}
                            ></div>
                            <span className="absolute right-2 top-1/2 transform -translate-y-1/2 text-xs font-bold text-gray-700 dark:text-white">
                              {tokens.toLocaleString()} ({percentage.toFixed(1)}%)
                            </span>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>

              {/* Daily Usage Chart */}
              <div className="bg-white dark:bg-gray-900 rounded-2xl p-5 border-2 border-gray-200 dark:border-gray-700 mb-6">
                <h3 className="text-lg font-bold text-gray-800 dark:text-white mb-4">📈 Daily Token Usage Trend (7 Days)</h3>
                <div className="flex items-end gap-2 h-48">
                  {costAnalytics.dailyUsage.map((day, idx) => {
                    const maxTokens = Math.max(...costAnalytics.dailyUsage.map(d => d.tokens));
                    const height = (day.tokens / maxTokens) * 100;
                    return (
                      <div key={idx} className="flex-1 flex flex-col items-center gap-2 group">
                        <div className="relative w-full flex items-end justify-center" style={{ height: '160px' }}>
                          <div 
                            className="w-full max-w-[60px] bg-gradient-to-t from-cyan-400 to-blue-500 rounded-t-lg opacity-70 group-hover:opacity-100 transition-all group-hover:from-cyan-500 group-hover:to-indigo-500 cursor-pointer relative"
                            style={{ height: `${height}%` }}
                          >
                            <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 px-2 py-1 bg-gray-900 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-10">
                              {day.tokens.toLocaleString()} tokens<br/>
                              ${day.cost}
                            </div>
                          </div>
                        </div>
                        <div className="text-xs text-gray-500 dark:text-gray-400 font-medium">{day.date}</div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Top Operations Table */}
              <div className="bg-white dark:bg-gray-900 rounded-2xl p-5 border-2 border-gray-200 dark:border-gray-700">
                <h3 className="text-lg font-bold text-gray-800 dark:text-white mb-4">🏆 Top 5 Most Expensive Operations</h3>
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-gray-200 dark:border-gray-700">
                      <th className="text-left py-2 px-3 text-sm font-bold text-gray-700 dark:text-gray-300">Operation</th>
                      <th className="text-right py-2 px-3 text-sm font-bold text-gray-700 dark:text-gray-300">Tokens</th>
                      <th className="text-right py-2 px-3 text-sm font-bold text-gray-700 dark:text-gray-300">% of Total</th>
                      <th className="text-left py-2 px-3 text-sm font-bold text-gray-700 dark:text-gray-300">Visual</th>
                    </tr>
                  </thead>
                  <tbody>
                    {costAnalytics.topOperations.map((op, idx) => (
                      <tr key={idx} className="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800/50">
                        <td className="py-3 px-3 text-sm text-gray-800 dark:text-white font-medium">{op.operation}</td>
                        <td className="py-3 px-3 text-sm text-gray-600 dark:text-gray-400 text-right font-mono">{op.tokens.toLocaleString()}</td>
                        <td className="py-3 px-3 text-sm text-gray-600 dark:text-gray-400 text-right">{op.percentage}%</td>
                        <td className="py-3 px-3">
                          <div className="w-24 h-2 bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden">
                            <div 
                              className="h-full bg-gradient-to-r from-red-400 via-yellow-400 to-green-400"
                              style={{ width: `${op.percentage}%` }}
                            ></div>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {/* Budget Alert */}
              {costAnalytics.totalCost > costAnalytics.budget * 0.8 && (
                <div className="mt-6 p-4 bg-yellow-50 dark:bg-yellow-950/20 rounded-xl border-2 border-yellow-200 dark:border-yellow-800">
                  <div className="flex items-center gap-2 text-yellow-700 dark:text-yellow-300 font-bold mb-2">
                    <span className="text-xl">⚠️</span> Budget Warning
                  </div>
                  <p className="text-sm text-yellow-600 dark:text-yellow-400">
                    You've used {(costAnalytics.totalCost / costAnalytics.budget * 100).toFixed(1)}% of your budget. Consider optimizing operations or increasing budget allocation.
                  </p>
                </div>
              )}
            </div>
          )}

          {/* TRACE VIEWER TAB - Real-time Operation Inspector */}
          {activeTab === 'trace-viewer' && (
            <div>
              <h2 className="text-3xl font-black text-gray-800 dark:text-white mb-6 flex items-center gap-3">
                <span className="text-4xl">🔍</span> Trace Viewer
                <span className="text-sm font-normal text-gray-500 dark:text-gray-400">(Real-time Operation Inspector)</span>
              </h2>

              {/* Live Status */}
              <div className="mb-6 p-5 bg-gradient-to-r from-green-50 via-emerald-50 to-teal-50 dark:from-green-950/20 dark:via-emerald-950/20 dark:to-teal-950/20 rounded-2xl border-2 border-green-200 dark:border-green-800">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                    <span className="font-bold text-green-700 dark:text-green-300 text-lg">Live Tracing Active</span>
                  </div>
                  <div className="flex items-center gap-4 text-sm text-green-600 dark:text-green-400">
                    <span className="flex items-center gap-1"><span>📡</span> Connected to OctoTrace Backend</span>
                    <span className="flex items-center gap-1"><span>⚡</span> Real-time Updates</span>
                    <span className="flex items-center gap-1"><span>🔄</span> Auto-refresh: 5s</span>
                  </div>
                </div>
              </div>

              {/* Current Operation Detail */}
              <div className="mb-6 bg-white dark:bg-gray-900 rounded-2xl p-6 border-2 border-cyan-200 dark:border-cyan-800 shadow-lg">
                <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-4 flex items-center gap-2">
                  <span className="w-2 h-2 bg-cyan-500 rounded-full animate-pulse"></span>
                  Currently Executing Operation
                </h3>
                
                <div className="grid grid-cols-2 gap-6">
                  {/* Left: Operation Info */}
                  <div className="space-y-4">
                    <div>
                      <label className="text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wide">Operation Type</label>
                      <div className="mt-1 text-2xl font-black text-blue-600 dark:text-blue-400">INGEST</div>
                    </div>
                    
                    <div>
                      <label className="text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wide">Source Document</label>
                      <div className="mt-1 text-lg font-medium text-gray-800 dark:text-white">LLM Training Techniques Article</div>
                    </div>

                    <div>
                      <label className="text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wide">Span ID</label>
                      <div className="mt-1 font-mono text-sm bg-cyan-50 dark:bg-cyan-950/30 inline-block px-3 py-1 rounded text-cyan-700 dark:text-cyan-300">span_001</div>
                    </div>

                    <div>
                      <label className="text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wide">Status</label>
                      <div className="mt-1 inline-flex items-center gap-2 px-3 py-1.5 bg-yellow-100 dark:bg-yellow-900/30 rounded-full">
                        <div className="w-2 h-2 bg-yellow-500 rounded-full animate-pulse"></div>
                        <span className="font-bold text-yellow-700 dark:text-yellow-300 text-sm">IN PROGRESS</span>
                      </div>
                    </div>
                  </div>

                  {/* Right: Progress & Metrics */}
                  <div className="space-y-4">
                    <div>
                      <label className="text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wide">Progress</label>
                      <div className="mt-2 w-full h-4 bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden">
                        <div className="h-full bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-500 transition-all duration-1000" style={{ width: '65%' }}></div>
                      </div>
                      <div className="mt-1 text-right text-sm font-mono text-gray-600 dark:text-gray-400">65%</div>
                    </div>

                    <div className="grid grid-cols-3 gap-3">
                      <div className="p-3 bg-gray-50 dark:bg-gray-800 rounded-xl text-center">
                        <div className="text-xl font-black text-gray-800 dark:text-white">4.8s</div>
                        <div className="text-xs text-gray-500 dark:text-gray-400">Duration</div>
                      </div>
                      <div className="p-3 bg-gray-50 dark:bg-gray-800 rounded-xl text-center">
                        <div className="text-xl font-black text-gray-800 dark:text-white">2,450</div>
                        <div className="text-xs text-gray-500 dark:text-gray-400">Tokens Used</div>
                      </div>
                      <div className="p-3 bg-gray-50 dark:bg-gray-800 rounded-xl text-center">
                        <div className="text-xl font-black text-gray-800 dark:text-white">$0.024</div>
                        <div className="text-xs text-gray-500 dark:text-gray-400">Cost</div>
                      </div>
                    </div>

                    <div>
                      <label className="text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wide">Current Phase</label>
                      <div className="mt-1 text-lg font-medium text-purple-600 dark:text-purple-400">Generation Phase</div>
                      <div className="text-sm text-gray-600 dark:text-gray-400">Creating wiki pages with cross-references...</div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Recent Spans List */}
              <div className="bg-white dark:bg-gray-900 rounded-2xl p-6 border-2 border-gray-200 dark:border-gray-700">
                <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-4">📋 Recent Span History</h3>
                
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b-2 border-gray-200 dark:border-gray-700">
                        <th className="text-left py-3 px-4 text-sm font-bold text-gray-700 dark:text-gray-300">Timestamp</th>
                        <th className="text-left py-3 px-4 text-sm font-bold text-gray-700 dark:text-gray-300">Operation</th>
                        <th className="text-left py-3 px-4 text-sm font-bold text-gray-700 dark:text-gray-300">Source</th>
                        <th className="text-center py-3 px-4 text-sm font-bold text-gray-700 dark:text-gray-300">Duration</th>
                        <th className="text-center py-3 px-4 text-sm font-bold text-gray-700 dark:text-gray-300">Tokens</th>
                        <th className="text-center py-3 px-4 text-sm font-bold text-gray-700 dark:text-gray-300">Cost</th>
                        <th className="text-center py-3 px-4 text-sm font-bold text-gray-700 dark:text-gray-300">Status</th>
                        <th className="text-left py-3 px-4 text-sm font-bold text-gray-700 dark:text-gray-300">Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {evolutionTimeline.slice(0, 7).map((event, idx) => (
                        <tr key={idx} className="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                          <td className="py-3 px-4 text-xs font-mono text-gray-500 dark:text-gray-400">
                            {new Date(event.timestamp).toLocaleTimeString()}
                          </td>
                          <td className="py-3 px-4">
                            <span className={`px-2 py-1 rounded text-xs font-bold ${
                              event.operation === 'INGEST' ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400' :
                              event.operation === 'QUERY' ? 'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-400' :
                              event.operation === 'LINT' ? 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400' :
                              'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400'
                            }`}>
                              {event.operation}
                            </span>
                          </td>
                          <td className="py-3 px-4 text-sm text-gray-800 dark:text-white max-w-[200px] truncate">{event.source}</td>
                          <td className="py-3 px-4 text-center text-sm text-gray-600 dark:text-gray-400 font-mono">{event.duration}</td>
                          <td className="py-3 px-4 text-center text-sm text-gray-600 dark:text-gray-400 font-mono">{event.tokens.toLocaleString()}</td>
                          <td className="py-3 px-4 text-center text-sm text-gray-600 dark:text-gray-400 font-mono">{event.cost}</td>
                          <td className="py-3 px-4 text-center">
                            <span className={`w-2 h-2 rounded-full inline-block ${
                              idx === 0 ? 'bg-yellow-500 animate-pulse' : 'bg-green-500'
                            }`}></span>
                          </td>
                          <td className="py-3 px-4">
                            <button className="text-xs text-cyan-600 dark:text-cyan-400 hover:underline font-medium">
                              Inspect →
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Quick Filters */}
              <div className="mt-6 flex gap-3 flex-wrap">
                <button className="px-4 py-2 bg-blue-500 text-white rounded-lg text-sm font-bold hover:bg-blue-600 transition-colors">
                  All Operations ({evolutionTimeline.length})
                </button>
                <button className="px-4 py-2 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 border-2 border-gray-200 dark:border-gray-700 rounded-lg text-sm font-medium hover:border-blue-400 dark:hover:border-blue-600 transition-colors">
                  Ingest Only ({evolutionTimeline.filter(t => t.operation === 'INGEST').length})
                </button>
                <button className="px-4 py-2 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 border-2 border-gray-200 dark:border-gray-700 rounded-lg text-sm font-medium hover:border-purple-400 dark:hover:border-purple-600 transition-colors">
                  Query Only ({evolutionTimeline.filter(t => t.operation === 'QUERY').length})
                </button>
                <button className="px-4 py-2 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 border-2 border-gray-200 dark:border-gray-700 rounded-lg text-sm font-medium hover:border-emerald-400 dark:hover:border-emerald-600 transition-colors">
                  Errors (0)
                </button>
              </div>

              {/* Export & Integration */}
              <div className="mt-6 flex gap-3">
                <Link 
                  to="/octo-trace" 
                  className="px-6 py-3 bg-gradient-to-r from-cyan-500 via-blue-500 to-indigo-500 hover:from-cyan-600 hover:to-indigo-600 text-white rounded-xl font-bold shadow-lg shadow-cyan-500/25 transition-all duration-300 flex items-center gap-2"
                >
                  <span className="text-lg">🔍</span> Launch Full OctoTrace Dashboard
                </Link>
                
                <button className="px-6 py-3 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 border-2 border-gray-200 dark:border-gray-700 rounded-xl font-semibold hover:border-cyan-400 dark:hover:border-cyan-600 transition-all flex items-center gap-2">
                  <span className="text-lg">📥</span> Export Trace Data (JSON)
                </button>
                
                <button className="px-6 py-3 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 border-2 border-gray-200 dark:border-gray-700 rounded-xl font-semibold hover:border-purple-400 dark:hover:border-purple-600 transition-all flex items-center gap-2">
                  <span className="text-lg">🔗</span> Sync with AutoResearch
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Integration Links Footer */}
        <div className="mt-8 grid grid-cols-4 gap-4">
          <Link to="/auto-research" className="p-4 bg-white/70 dark:bg-gray-800/70 backdrop-blur-sm rounded-xl border border-gray-200 dark:border-gray-700 hover:border-emerald-400 dark:hover:border-emerald-600 transition-all group text-center">
            <div className="text-2xl mb-2 group-hover:scale-110 transition-transform inline-block">🔬</div>
            <div className="font-bold text-sm text-gray-800 dark:text-white">AutoResearch</div>
            <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">Deep Research Engine</div>
          </Link>
          
          <Link to="/skills-hub-pro" className="p-4 bg-white/70 dark:bg-gray-800/70 backdrop-blur-sm rounded-xl border border-gray-200 dark:border-gray-700 hover:border-violet-400 dark:hover:border-violet-600 transition-all group text-center">
            <div className="text-2xl mb-2 group-hover:scale-110 transition-transform inline-block">📦</div>
            <div className="font-bold text-sm text-gray-800 dark:text-white">Skills Hub</div>
            <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">Knowledge Foundation</div>
          </Link>
          
          <Link to="/octo-trace" className="p-4 bg-white/70 dark:bg-gray-800/70 backdrop-blur-sm rounded-xl border border-gray-200 dark:border-gray-700 hover:border-cyan-400 dark:hover:border-cyan-600 transition-all group text-center">
            <div className="text-2xl mb-2 group-hover:scale-110 transition-transform inline-block">🔍</div>
            <div className="font-bold text-sm text-gray-800 dark:text-white">OctoTrace</div>
            <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">Evolution Tracking</div>
          </Link>
          
          <Link to="/evolution-workbench" className="p-4 bg-white/70 dark:bg-gray-800/70 backdrop-blur-sm rounded-xl border border-gray-200 dark:border-gray-700 hover:border-fuchsia-400 dark:hover:border-fuchsia-600 transition-all group text-center">
            <div className="text-2xl mb-2 group-hover:scale-110 transition-transform inline-block">🧬</div>
            <div className="font-bold text-sm text-gray-800 dark:text-white">Evolution</div>
            <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">Self-Optimization</div>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default AIWiki;
