import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import Agent from './pages/Agent'
import SkillsHub from './pages/SkillsHub'
import Research from './pages/Research'
import CreateSkill from './pages/CreateSkill'
import SkillList from './pages/SkillList'
import SkillDetail from './pages/SkillDetail'
import Docs from './pages/Docs'

function App() {
  return (
    <div className="min-h-screen">
      <Navbar />
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/agent" element={<Agent />} />
          <Route path="/skills" element={<SkillsHub />} />
          <Route path="/research" element={<Research />} />
          <Route path="/create" element={<CreateSkill />} />
          <Route path="/skill-list" element={<SkillList />} />
          <Route path="/skills/:skillId" element={<SkillDetail />} />
          <Route path="/docs" element={<Docs />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
