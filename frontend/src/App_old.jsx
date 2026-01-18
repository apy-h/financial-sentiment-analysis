import React, { useState, useEffect } from 'react'
import axios from 'axios'
import Dashboard from './components/Dashboard'
import PostsList from './components/PostsList'
import SentimentChart from './components/SentimentChart'

function App() {
  const [posts, setPosts] = useState([])
  const [stats, setStats] = useState(null)
  const [trends, setTrends] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:5000'

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const [postsRes, statsRes, trendsRes] = await Promise.all([
        axios.get(`${API_BASE}/api/posts?limit=20`),
        axios.get(`${API_BASE}/api/stats`),
        axios.get(`${API_BASE}/api/trends?days=7`)
      ])

      setPosts(postsRes.data.posts)
      setStats(statsRes.data)
      setTrends(trendsRes.data.trends)
    } catch (err) {
      console.error('Error loading data:', err)
    }
  }

  const fetchNewPosts = async () => {
    setLoading(true)
    setError(null)

    try {
      const response = await axios.get(`${API_BASE}/api/fetch-posts?max_results=15`)
      await loadData() // Reload all data
      setLoading(false)
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to fetch posts')
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>📈 Finance Sentiment Analysis</h1>
        <p>Real-time sentiment analysis of finance-related Reddit posts (RSS) using FinBERT</p>
      </header>

      <div className="controls">
        <button onClick={fetchNewPosts} disabled={loading}>
          {loading ? 'Fetching & Analyzing...' : 'Fetch New Posts'}
        </button>
        <button onClick={loadData} disabled={loading}>
          Refresh Data
        </button>
      </div>

      {error && (
        <div className="error">
          <strong>Error:</strong> {error}
        </div>
      )}

      {loading && (
        <div className="loading">
          Fetching and analyzing posts...
        </div>
      )}

      <Dashboard stats={stats} />

      <SentimentChart trends={trends} />

      <PostsList posts={posts} />
    </div>
  )
}

export default App
