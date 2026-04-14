import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import SkillsHub from './pages/SkillsHub'
import SkillDetail from './pages/SkillDetail'
import Research from './pages/Research'
import CreateSkill from './pages/CreateSkill'
import SkillList from './pages/SkillList'
import OldSkillsHub from './pages/OldSkillsHub'
import Docs from './pages/Docs'
import EvolutionEngine from './pages/EvolutionEngine'
import AgentDetail from './pages/AgentDetail'

import SkillCreatorStudio from './pages/SkillCreatorStudio'
import EvolutionWorkbench from './pages/EvolutionWorkbench'
import SkillsHubPro from './pages/SkillsHubPro'
import OctoTraceDashboard from './pages/OctoTraceDashboard'
import AIWiki from './pages/AIWiki'

function App() {
  return (
    <div className="min-h-screen">
      <Navbar />
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          
          <Route path="/evolution-engine" element={<EvolutionEngine />} />
          <Route path="/evolution-engine/:agentId" element={<AgentDetail />} />
          <Route path="/evolution-workbench" element={<EvolutionWorkbench />} />
          
          <Route path="/skills-hub" element={<SkillsHub />} />
          <Route path="/skills-hub/:skillId" element={<SkillDetail />} />
          <Route path="/skills-hub/create" element={<CreateSkill />} />
          <Route path="/skills-hub-pro" element={<SkillsHubPro />} />
          
          <Route path="/skill-creator-studio" element={<SkillCreatorStudio />} />
          <Route path="/octo-trace" element={<OctoTraceDashboard />} />
          <Route path="/ai-wiki" element={<AIWiki />} />
          
          <Route path="/skills" element={<OldSkillsHub />} />
          <Route path="/research" element={<Research />} />
          <Route path="/create" element={<CreateSkill />} />
          <Route path="/skill-list" element={<SkillList />} />
          <Route path="/docs" element={<Docs />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
