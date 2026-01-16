import React from 'react'

function Dashboard({ stats }) {
  if (!stats || !stats.by_sentiment) {
    return (
      <div className="dashboard">
        <div className="card">
          <h2>Statistics</h2>
          <p>No data available yet. Click "Fetch New Posts" to get started!</p>
        </div>
      </div>
    )
  }

  const { total, by_sentiment } = stats

  return (
    <div className="dashboard">
      <div className="card">
        <h2>Sentiment Overview</h2>
        <div className="stats-grid">
          <div className="stat-item positive">
            <div className="label">Positive</div>
            <div className="value">{by_sentiment.positive?.count || 0}</div>
            <div className="percentage">{by_sentiment.positive?.percentage || 0}%</div>
          </div>
          <div className="stat-item negative">
            <div className="label">Negative</div>
            <div className="value">{by_sentiment.negative?.count || 0}</div>
            <div className="percentage">{by_sentiment.negative?.percentage || 0}%</div>
          </div>
          <div className="stat-item neutral">
            <div className="label">Neutral</div>
            <div className="value">{by_sentiment.neutral?.count || 0}</div>
            <div className="percentage">{by_sentiment.neutral?.percentage || 0}%</div>
          </div>
        </div>
        <div style={{ marginTop: '20px', textAlign: 'center', color: '#666' }}>
          <strong>Total Posts Analyzed:</strong> {total}
        </div>
      </div>
    </div>
  )
}

export default Dashboard
