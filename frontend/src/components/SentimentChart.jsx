import React from 'react'
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js'
import { Bar } from 'react-chartjs-2'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

function SentimentChart({ trends }) {
  if (!trends || trends.length === 0) {
    return (
      <div className="card">
        <h2>Sentiment Trends</h2>
        <p>No trend data available yet.</p>
      </div>
    )
  }

  const labels = trends.map(t => t.date).reverse()
  const positiveData = trends.map(t => t.positive).reverse()
  const negativeData = trends.map(t => t.negative).reverse()
  const neutralData = trends.map(t => t.neutral).reverse()

  const data = {
    labels,
    datasets: [
      {
        label: 'Positive',
        data: positiveData,
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
      {
        label: 'Negative',
        data: negativeData,
        backgroundColor: 'rgba(255, 99, 132, 0.6)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1,
      },
      {
        label: 'Neutral',
        data: neutralData,
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1,
      },
    ],
  }

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Sentiment Trends Over Time',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  }

  return (
    <div className="card">
      <h2>Sentiment Trends</h2>
      <div className="chart-container">
        <Bar data={data} options={options} />
      </div>
    </div>
  )
}

export default SentimentChart
