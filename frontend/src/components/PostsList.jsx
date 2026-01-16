import React from 'react'

function PostsList({ posts }) {
  if (!posts || posts.length === 0) {
    return (
      <div className="posts-list">
        <h2>Recent Posts</h2>
        <p>No posts available. Fetch some posts to see them analyzed here!</p>
      </div>
    )
  }

  return (
    <div className="posts-list">
      <h2>Recent Posts ({posts.length})</h2>
      {posts.map((post) => (
        <div key={post.id} className="post">
          <div className="post-text">{post.text}</div>
          <div className="post-meta">
            <span>{new Date(post.created_at).toLocaleString()}</span>
            <span className={`sentiment-badge ${post.sentiment.label}`}>
              {post.sentiment.label.toUpperCase()} ({(post.sentiment.score * 100).toFixed(1)}%)
            </span>
          </div>
        </div>
      ))}
    </div>
  )
}

export default PostsList
