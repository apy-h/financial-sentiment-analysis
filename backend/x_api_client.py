import os
import requests
from datetime import datetime, timedelta

class XAPIClient:
    """Client for X (Twitter) API v2"""
    
    def __init__(self):
        """Initialize X API client with bearer token from environment"""
        self.bearer_token = os.environ.get('X_BEARER_TOKEN', '')
        self.base_url = 'https://api.twitter.com/2'
        
    def _get_headers(self):
        """Get headers for API requests"""
        return {
            'Authorization': f'Bearer {self.bearer_token}',
            'Content-Type': 'application/json'
        }
    
    def search_recent_posts(self, query, max_results=10):
        """
        Search recent posts using X API v2
        
        Args:
            query: Search query (e.g., '#stocks OR #finance')
            max_results: Maximum number of results (10-100)
            
        Returns:
            List of post dictionaries
        """
        if not self.bearer_token:
            # Return mock data if no API token is available
            return self._get_mock_posts(max_results)
        
        endpoint = f'{self.base_url}/tweets/search/recent'
        params = {
            'query': query,
            'max_results': min(max_results, 100),
            'tweet.fields': 'created_at,author_id,public_metrics',
        }
        
        try:
            response = requests.get(
                endpoint,
                headers=self._get_headers(),
                params=params,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            posts = []
            for tweet in data.get('data', []):
                posts.append({
                    'id': tweet['id'],
                    'text': tweet['text'],
                    'created_at': tweet.get('created_at', datetime.utcnow().isoformat()),
                    'author_id': tweet.get('author_id', 'unknown'),
                    'metrics': tweet.get('public_metrics', {})
                })
            
            return posts
        except Exception as e:
            print(f"Error fetching posts from X API: {e}")
            # Return mock data on error
            return self._get_mock_posts(max_results)
    
    def _get_mock_posts(self, count=10):
        """
        Generate mock finance posts for testing
        
        Args:
            count: Number of mock posts to generate
            
        Returns:
            List of mock post dictionaries
        """
        mock_texts = [
            "Apple stock hits new all-time high! $AAPL investors celebrating today. #stocks #investing",
            "Market downturn expected as inflation concerns grow. Time to be cautious. #finance #economy",
            "Tesla's Q4 earnings beat expectations. Strong performance across all segments. $TSLA #earnings",
            "Federal Reserve signals potential rate cuts. Markets respond positively. #finance #fed",
            "Tech stocks rally continues. NASDAQ up 2% today. Great day for investors! #stocks",
            "Oil prices stabilize after recent volatility. Energy sector showing resilience. #commodities",
            "Bitcoin struggles below $40k. Crypto markets remain uncertain. #crypto #bitcoin",
            "Warren Buffett's latest investment strategy revealed. Value investing still works! #investing",
            "S&P 500 reaches new milestone. Bull market continues strong. #stocks #SPX",
            "Gold prices surge amid economic uncertainty. Safe haven assets in demand. #gold #investing",
            "Amazon announces stock split. Retail investors excited about accessibility. $AMZN #stocks",
            "Housing market shows signs of cooling. Interest rates impact becoming clear. #realestate",
            "Nvidia's AI chips driving stock growth. Semiconductor sector booming. $NVDA #tech",
            "Bond yields rising, affecting equity valuations. Portfolio rebalancing time? #bonds #finance",
            "Emerging markets offer opportunities despite risks. Diversification key. #investing #EM"
        ]
        
        posts = []
        base_time = datetime.utcnow()
        
        for i in range(min(count, len(mock_texts))):
            posts.append({
                'id': f'mock_{i+1}',
                'text': mock_texts[i],
                'created_at': (base_time - timedelta(minutes=i*10)).isoformat(),
                'author_id': f'user_{i+1}',
                'metrics': {
                    'like_count': (i + 1) * 10,
                    'retweet_count': (i + 1) * 5
                }
            })
        
        return posts
