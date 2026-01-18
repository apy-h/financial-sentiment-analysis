import os
import requests
import html
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta


class RedditRSSClient:
    """Fetch finance posts from subreddit RSS feeds without API credentials."""

    def __init__(self):
        self.subreddits = [s.strip() for s in os.environ.get(
            'REDDIT_SUBREDDITS', 'stocks,investing,wallstreetbets,finance'
        ).split(',') if s.strip()]
        self.user_agent = os.environ.get('REDDIT_USER_AGENT', 'finance-sentiment-rss/0.1')
        self.base_url = 'https://www.reddit.com'

    def fetch_posts(self, query=None, max_results=10):
        """Fetch recent posts via RSS across configured subreddits."""
        if max_results <= 0:
            return []

        search_query = query or 'stocks OR finance OR investing'
        headers = {'User-Agent': self.user_agent}

        collected = []
        per_sub_limit = max(1, min(50, max_results // max(len(self.subreddits), 1) + 1))

        for sub in self.subreddits or ['stocks', 'investing']:
            if len(collected) >= max_results:
                break

            url = f"{self.base_url}/r/{sub}/search.rss"
            params = {
                'q': search_query,
                'restrict_sr': 'on',
                'sort': 'new',
                'limit': per_sub_limit,
            }
            try:
                resp = requests.get(url, headers=headers, params=params, timeout=10)
                resp.raise_for_status()
                posts = self._parse_feed(resp.content, sub)
                for post in posts:
                    if len(collected) >= max_results:
                        break
                    collected.append(post)
            except Exception as exc:
                print(f"Error fetching RSS for r/{sub}: {exc}")
                continue

        if not collected:
            return self._get_mock_posts(max_results)
        return collected[:max_results]

    def _parse_feed(self, content, subreddit):
        """Parse Atom/RSS entries from Reddit feed content."""
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        try:
            root = ET.fromstring(content)
        except ET.ParseError:
            return []

        entries = root.findall('.//atom:entry', ns)
        results = []
        for entry in entries:
            title_el = entry.find('atom:title', ns)
            summary_el = entry.find('atom:summary', ns)
            updated_el = entry.find('atom:updated', ns)
            published_el = entry.find('atom:published', ns)
            link_el = entry.find('atom:link', ns)
            author_el = entry.find('atom:author/atom:name', ns)

            title = html.unescape(title_el.text) if title_el is not None and title_el.text else ''
            summary_raw = summary_el.text or '' if summary_el is not None else ''
            summary = html.unescape(summary_raw)
            text_parts = [title.strip()]
            if summary.strip():
                text_parts.append(summary.strip())
            text = '\n\n'.join([t for t in text_parts if t])

            created_str = (updated_el.text if updated_el is not None else None) or \
                          (published_el.text if published_el is not None else None)
            try:
                created_at = datetime.fromisoformat(created_str.replace('Z', '+00:00')).isoformat() if created_str else datetime.utcnow().isoformat()
            except Exception:
                created_at = datetime.utcnow().isoformat()

            link = link_el.attrib.get('href') if link_el is not None else ''
            author = author_el.text if author_el is not None else 'unknown'

            # entry id can contain URL; use last path segment for stability
            raw_id = entry.find('atom:id', ns).text if entry.find('atom:id', ns) is not None else link
            post_id = raw_id.split('/')[-1] if raw_id else f"reddit_{len(results)}"

            results.append({
                'id': f'reddit_{post_id}',
                'text': text or title or '(no title)',
                'created_at': created_at,
                'author_id': author,
                'subreddit': subreddit,
                'metrics': {},
                'link': link,
            })
        return results

    def _get_mock_posts(self, count=10):
        mock_texts = [
            "RSS mock: Redditors bullish on tech stocks after strong earnings.",
            "RSS mock: Inflation concerns rising; portfolios adjusting.",
            "RSS mock: Energy sector stabilizes as oil prices level off.",
            "RSS mock: Crypto sentiment mixed with BTC near key level.",
            "RSS mock: Value strategies seeing renewed interest.",
            "RSS mock: Debate on sustainability of the rally.",
            "RSS mock: Fed hints at possible cuts later this year.",
            "RSS mock: Gold as hedge amid uncertainty.",
            "RSS mock: AI chips keep semis strong.",
            "RSS mock: Emerging markets offering selective upside.",
        ]

        posts = []
        base_time = datetime.utcnow()
        for i in range(min(count, len(mock_texts))):
            posts.append({
                'id': f'reddit_rss_mock_{i+1}',
                'text': mock_texts[i],
                'created_at': (base_time - timedelta(minutes=i * 7)).isoformat(),
                'author_id': f'reddit_user_{i+1}',
                'subreddit': 'mockfinance',
                'metrics': {},
                'link': '',
            })
        return posts
