import React, { useState } from 'react'
import { api } from '../api/client'

function CreateSkill() {
  const [activeTab, setActiveTab] = useState('url')
  const [url, setUrl] = useState('')
  const [files, setFiles] = useState([])
  const [loading, setLoading] = useState(false)
  const [taskId, setTaskId] = useState(null)
  const [taskStatus, setTaskStatus] = useState(null)

  const handleSubmitUrl = async (e) => {
    e.preventDefault()
    if (!url) return
    
    setLoading(true)
    try {
      const response = await api.createSkillFromUrl(url)
      setTaskId(response.task_id)
      pollTaskStatus(response.task_id)
    } catch (error) {
      console.error('Error:', error)
      alert('Creation failed, please try again')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmitFiles = async (e) => {
    e.preventDefault()
    if (files.length === 0) return
    
    setLoading(true)
    try {
      const formData = new FormData()
      files.forEach(file => formData.append('files', file))
      const response = await api.createSkillFromFiles(formData)
      setTaskId(response.task_id)
      pollTaskStatus(response.task_id)
    } catch (error) {
      console.error('Error:', error)
      alert('Creation failed, please try again')
    } finally {
      setLoading(false)
    }
  }

  const pollTaskStatus = async (id) => {
    const pollInterval = setInterval(async () => {
      try {
        const status = await api.getTaskStatus(id)
        setTaskStatus(status)
        
        if (status.status === 'completed' || status.status === 'failed') {
          clearInterval(pollInterval)
        }
      } catch (error) {
        console.error('Polling error:', error)
        clearInterval(pollInterval)
      }
    }, 2000)
  }

  const resetForm = () => {
    setUrl('')
    setFiles([])
    setTaskId(null)
    setTaskStatus(null)
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent mb-4">
          Create New Skill
        </h1>
        <p className="text-gray-600 text-lg">
          Create evolvable Skills via URL or file upload
        </p>
      </div>

      {!taskId ? (
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <div className="flex gap-4 mb-8">
            <button
              onClick={() => setActiveTab('url')}
              className={`flex-1 py-3 px-6 rounded-xl font-semibold transition-all ${
                activeTab === 'url'
                  ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              📎 Create from URL
            </button>
            <button
              onClick={() => setActiveTab('files')}
              className={`flex-1 py-3 px-6 rounded-xl font-semibold transition-all ${
                activeTab === 'files'
                  ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              📁 Upload Files
            </button>
          </div>

          {activeTab === 'url' && (
            <form onSubmit={handleSubmitUrl} className="space-y-6">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Enter URL
                </label>
                <input
                  type="url"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  placeholder="https://example.com/article"
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                />
              </div>
              <button
                type="submit"
                disabled={loading || !url}
                className="w-full py-4 bg-gradient-to-r from-purple-600 to-blue-600 text-white font-semibold rounded-xl hover:from-purple-700 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
              >
                {loading ? 'Processing...' : '🚀 Create Skill'}
              </button>
            </form>
          )}

          {activeTab === 'files' && (
            <form onSubmit={handleSubmitFiles} className="space-y-6">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Select Files
                </label>
                <div className="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center hover:border-purple-500 transition-all">
                  <input
                    type="file"
                    multiple
                    onChange={(e) => setFiles(Array.from(e.target.files || []))}
                    className="hidden"
                    id="fileInput"
                  />
                  <label htmlFor="fileInput" className="cursor-pointer">
                    <div className="text-5xl mb-4">📄</div>
                    <p className="text-gray-600 mb-2">Click or drag files here</p>
                    <p className="text-sm text-gray-400">Supports PDF, TXT, MD, DOCX formats</p>
                  </label>
                </div>
                {files.length > 0 && (
                  <div className="mt-4 space-y-2">
                    {files.map((file, index) => (
                      <div key={index} className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                        <span>📄</span>
                        <span className="flex-1 text-sm">{file.name}</span>
                        <span className="text-xs text-gray-400">{(file.size / 1024).toFixed(1)} KB</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
              <button
                type="submit"
                disabled={loading || files.length === 0}
                className="w-full py-4 bg-gradient-to-r from-purple-600 to-blue-600 text-white font-semibold rounded-xl hover:from-purple-700 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
              >
                {loading ? 'Processing...' : '🚀 Create Skill'}
              </button>
            </form>
          )}
        </div>
      ) : (
        <div className="bg-white rounded-2xl shadow-xl p-8 text-center">
          <div className="text-6xl mb-6">
            {taskStatus?.status === 'completed' ? '🎉' : taskStatus?.status === 'failed' ? '❌' : '⏳'}
          </div>
          <h2 className="text-2xl font-bold mb-4">
            {taskStatus?.status === 'completed' ? 'Skill created successfully!' : 
             taskStatus?.status === 'failed' ? 'Creation failed' : 'Processing...'}
          </h2>
          {taskStatus && (
            <div className="text-left bg-gray-50 rounded-xl p-6 mb-6">
              <p className="text-sm text-gray-600 mb-2">
                <span className="font-semibold">Status:</span> {taskStatus.status}
              </p>
              {taskStatus.message && (
                <p className="text-sm text-gray-600">
                  <span className="font-semibold">Message:</span> {taskStatus.message}
                </p>
              )}
              {taskStatus.result && (
                <div className="mt-4">
                  <p className="text-sm font-semibold text-gray-700 mb-2">Result:</p>
                  <pre className="text-xs bg-white p-4 rounded-lg overflow-x-auto">
                    {JSON.stringify(taskStatus.result, null, 2)}
                  </pre>
                </div>
              )}
            </div>
          )}
          <div className="flex gap-4 justify-center">
            {taskStatus?.status === 'completed' && (
              <button
                onClick={() => window.location.href = '/skills'}
                className="px-8 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white font-semibold rounded-xl hover:from-purple-700 hover:to-blue-700 transition-all"
              >
                View Skill List
              </button>
            )}
            <button
              onClick={resetForm}
              className="px-8 py-3 bg-gray-100 text-gray-700 font-semibold rounded-xl hover:bg-gray-200 transition-all"
            >
              Create New Skill
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

export default CreateSkill
