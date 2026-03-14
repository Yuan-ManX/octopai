import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import CreateSkill from './pages/CreateSkill'
import SkillList from './pages/SkillList'
import SkillDetail from './pages/SkillDetail'
import Docs from './pages/Docs'

function App() {
  return (
    <div className="min-h-screen">
      <Navbar />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/create" element={<CreateSkill />} />
          <Route path="/skills" element={<SkillList />} />
          <Route path="/skills/:skillId" element={<SkillDetail />} />
          <Route path="/docs" element={<Docs />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
