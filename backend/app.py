from flask import Flask, jsonify, request
from flask_cors import CORS
from sentiment_analyzer import SentimentAnalyzer
from x_api_client import XAPIClient
from database import Database
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Initialize components
sentiment_analyzer = SentimentAnalyzer()
x_client = XAPIClient()
db = Database()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})

@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    """Analyze sentiment of provided text"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    sentiment = sentiment_analyzer.analyze(text)
    return jsonify(sentiment)

@app.route('/api/fetch-posts', methods=['GET'])
def fetch_posts():
    """Fetch and analyze finance posts from X"""
    query = request.args.get('query', '#stocks OR #finance OR #investing')
    try:
        max_results = int(request.args.get('max_results', 10))
        max_results = max(1, min(max_results, 100))  # Clamp between 1 and 100
    except ValueError:
        return jsonify({'error': 'Invalid max_results parameter'}), 400
    
    try:
        posts = x_client.search_recent_posts(query, max_results)
        analyzed_posts = []
        
        for post in posts:
            sentiment = sentiment_analyzer.analyze(post['text'])
            analyzed_post = {
                'id': post['id'],
                'text': post['text'],
                'created_at': post['created_at'],
                'author_id': post.get('author_id', 'unknown'),
                'sentiment': sentiment
            }
            analyzed_posts.append(analyzed_post)
            db.save_post(analyzed_post)
        
        return jsonify({
            'posts': analyzed_posts,
            'count': len(analyzed_posts)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Get stored posts from database"""
    try:
        limit = int(request.args.get('limit', 50))
        limit = max(1, min(limit, 1000))  # Clamp between 1 and 1000
    except ValueError:
        return jsonify({'error': 'Invalid limit parameter'}), 400
    posts = db.get_recent_posts(limit)
    return jsonify({'posts': posts, 'count': len(posts)})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get sentiment statistics"""
    stats = db.get_sentiment_stats()
    return jsonify(stats)

@app.route('/api/trends', methods=['GET'])
def get_trends():
    """Get sentiment trends over time"""
    try:
        days = int(request.args.get('days', 7))
        days = max(1, min(days, 365))  # Clamp between 1 and 365
    except ValueError:
        return jsonify({'error': 'Invalid days parameter'}), 400
    trends = db.get_sentiment_trends(days)
    return jsonify({'trends': trends})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
