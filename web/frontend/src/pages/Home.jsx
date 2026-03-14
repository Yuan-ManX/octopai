import React from 'react'
import { Link } from 'react-router-dom'

const isDemoMode = import.meta.env.VITE_DEMO_MODE === 'true'

const Home = () => {
  return (
    <div className="space-y-12">
      {isDemoMode && (
        <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-6 py-4 rounded-2xl text-center">
          <div className="flex items-center justify-center gap-2 mb-2">
            <span className="text-2xl">🎬</span>
            <span className="font-bold text-lg">Demo Mode</span>
          </div>
          <p className="text-purple-100">
            This is a demo version with mock data. For full functionality, run the local backend service.
          </p>
        </div>
      )}

      <section className="text-center py-16">
        <div className="inline-flex items-center space-x-2 bg-purple-50 border border-purple-200 rounded-full px-4 py-2 mb-6">
          <span className="w-2 h-2 bg-purple-500 rounded-full animate-pulse"></span>
          <span className="text-purple-700 text-sm font-medium">Everything Can Be a Skill</span>
        </div>
        <h1 className="text-5xl md:text-6xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent mb-6">
          EXO
          <span className="block text-2xl md:text-3xl font-normal text-gray-600 mt-2">
            AI Agent Skills Exploration, Extension, and Evolution Framework
          </span>
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto mb-8">
          Through intelligent learning and continuous self-evolution, Skills grow and improve, significantly elevating AI Agent cognitive capabilities.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            to="/create"
            className="px-8 py-4 bg-gradient-to-r from-purple-600 to-blue-600 text-white font-semibold rounded-xl hover:from-purple-700 hover:to-blue-700 transition-all text-lg"
          >
            Start Creating Skills
          </Link>
          <Link
            to="/skills"
            className="px-8 py-4 bg-gray-100 text-gray-700 font-semibold rounded-xl hover:bg-gray-200 transition-all text-lg"
          >
            Browse Skill Library
          </Link>
        </div>
      </section>

      <section className="grid md:grid-cols-3 gap-8">
        <div className="bg-white rounded-2xl shadow-lg p-8 hover:shadow-xl transition-all hover:-translate-y-1">
          <div className="w-14 h-14 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center mb-4">
            <span className="text-white text-2xl">🌐</span>
          </div>
          <h3 className="text-xl font-bold text-gray-800 mb-2">Everything Can Be a Skill</h3>
          <p className="text-gray-600">
            Any resource — web pages, documents, videos, code, datasets — can be transformed into structured, AI-ready Skills.
          </p>
        </div>

        <div className="bg-white rounded-2xl shadow-lg p-8 hover:shadow-xl transition-all hover:-translate-y-1">
          <div className="w-14 h-14 bg-gradient-to-br from-green-500 to-green-600 rounded-xl flex items-center justify-center mb-4">
            <span className="text-white text-2xl">🚀</span>
          </div>
          <h3 className="text-xl font-bold text-gray-800 mb-2">Skills Evolve Through Learning</h3>
          <p className="text-gray-600">
            Every Skill continuously learns from usage, feedback, and interactions, growing more powerful and comprehensive over time.
          </p>
        </div>

        <div className="bg-white rounded-2xl shadow-lg p-8 hover:shadow-xl transition-all hover:-translate-y-1">
          <div className="w-14 h-14 bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl flex items-center justify-center mb-4">
            <span className="text-white text-2xl">🧠</span>
          </div>
          <h3 className="text-xl font-bold text-gray-800 mb-2">Elevate AI Agent Cognition</h3>
          <p className="text-gray-600">
            Through an evolved Skill ecosystem, significantly expand the cognitive boundaries and capabilities of AI Agents.
          </p>
        </div>
      </section>

      <section className="bg-white rounded-2xl shadow-xl p-8">
        <h2 className="text-2xl font-bold text-gray-800 mb-8 text-center">Core Features</h2>
        <div className="grid md:grid-cols-2 gap-6">
          <div className="flex items-start space-x-4 p-4 bg-gray-50 rounded-xl">
            <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center flex-shrink-0">
              <span className="text-purple-600 font-bold text-xl">1</span>
            </div>
            <div>
              <h4 className="font-bold text-gray-800 mb-1">One-Click URL to Skill</h4>
              <p className="text-gray-600">Instantly transform any internet resource into structured, AI-ready Skills.</p>
            </div>
          </div>
          <div className="flex items-start space-x-4 p-4 bg-gray-50 rounded-xl">
            <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center flex-shrink-0">
              <span className="text-purple-600 font-bold text-xl">2</span>
            </div>
            <div>
              <h4 className="font-bold text-gray-800 mb-1">Multi-Format Resource Parser</h4>
              <p className="text-gray-600">Supports PDF, DOC, Excel, images, videos, and many other file formats.</p>
            </div>
          </div>
          <div className="flex items-start space-x-4 p-4 bg-gray-50 rounded-xl">
            <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center flex-shrink-0">
              <span className="text-purple-600 font-bold text-xl">3</span>
            </div>
            <div>
              <h4 className="font-bold text-gray-800 mb-1">Intelligent Evolution Engine</h4>
              <p className="text-gray-600">Three-stage evolution pipeline: Executor → Reflector → Optimizer.</p>
            </div>
          </div>
          <div className="flex items-start space-x-4 p-4 bg-gray-50 rounded-xl">
            <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center flex-shrink-0">
              <span className="text-purple-600 font-bold text-xl">4</span>
            </div>
            <div>
              <h4 className="font-bold text-gray-800 mb-1">SkillHub Management</h4>
              <p className="text-gray-600">Centralized storage, version control, smart search, and Skill merging.</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}

export default Home
