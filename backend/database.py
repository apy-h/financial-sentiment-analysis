import sqlite3
import json
from datetime import datetime, timedelta
from contextlib import contextmanager

class Database:
    """SQLite database for storing analyzed posts"""
    
    def __init__(self, db_path='finance_sentiment.db'):
        """Initialize database connection"""
        self.db_path = db_path
        self._init_db()
    
    @contextmanager
    def _get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def _init_db(self):
        """Initialize database tables"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS posts (
                    id TEXT PRIMARY KEY,
                    text TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    author_id TEXT,
                    sentiment_label TEXT NOT NULL,
                    sentiment_score REAL NOT NULL,
                    sentiment_scores TEXT NOT NULL,
                    analyzed_at TEXT NOT NULL
                )
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_created_at 
                ON posts(created_at DESC)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_sentiment_label 
                ON posts(sentiment_label)
            ''')
    
    def save_post(self, post_data):
        """
        Save analyzed post to database
        
        Args:
            post_data: Dictionary with post data and sentiment
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO posts 
                (id, text, created_at, author_id, sentiment_label, 
                 sentiment_score, sentiment_scores, analyzed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                post_data['id'],
                post_data['text'],
                post_data['created_at'],
                post_data.get('author_id', 'unknown'),
                post_data['sentiment']['label'],
                post_data['sentiment']['score'],
                json.dumps(post_data['sentiment']['scores']),
                datetime.utcnow().isoformat()
            ))
    
    def get_recent_posts(self, limit=50):
        """
        Get recent analyzed posts
        
        Args:
            limit: Maximum number of posts to return
            
        Returns:
            List of post dictionaries
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, text, created_at, author_id, 
                       sentiment_label, sentiment_score, sentiment_scores
                FROM posts
                ORDER BY created_at DESC
                LIMIT ?
            ''', (limit,))
            
            posts = []
            for row in cursor.fetchall():
                posts.append({
                    'id': row['id'],
                    'text': row['text'],
                    'created_at': row['created_at'],
                    'author_id': row['author_id'],
                    'sentiment': {
                        'label': row['sentiment_label'],
                        'score': row['sentiment_score'],
                        'scores': json.loads(row['sentiment_scores'])
                    }
                })
            
            return posts
    
    def get_sentiment_stats(self):
        """
        Get overall sentiment statistics
        
        Returns:
            Dictionary with sentiment counts and percentages
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT sentiment_label, COUNT(*) as count
                FROM posts
                GROUP BY sentiment_label
            ''')
            
            stats = {'total': 0, 'by_sentiment': {}}
            for row in cursor.fetchall():
                label = row['sentiment_label']
                count = row['count']
                stats['by_sentiment'][label] = count
                stats['total'] += count
            
            # Calculate percentages
            if stats['total'] > 0:
                for label in stats['by_sentiment']:
                    count = stats['by_sentiment'][label]
                    stats['by_sentiment'][label] = {
                        'count': count,
                        'percentage': round((count / stats['total']) * 100, 2)
                    }
            
            return stats
    
    def get_sentiment_trends(self, days=7):
        """
        Get sentiment trends over time
        
        Args:
            days: Number of days to include in trends
            
        Returns:
            List of daily sentiment counts
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cutoff_date = (datetime.utcnow() - timedelta(days=days)).isoformat()
            
            cursor.execute('''
                SELECT DATE(created_at) as date, sentiment_label, COUNT(*) as count
                FROM posts
                WHERE created_at >= ?
                GROUP BY DATE(created_at), sentiment_label
                ORDER BY date DESC
            ''', (cutoff_date,))
            
            trends = {}
            for row in cursor.fetchall():
                date = row['date']
                label = row['sentiment_label']
                count = row['count']
                
                if date not in trends:
                    trends[date] = {'date': date, 'positive': 0, 'negative': 0, 'neutral': 0}
                
                trends[date][label] = count
            
            return list(trends.values())
