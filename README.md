# 📈 Finance Sentiment Analysis Dashboard

A production-quality financial sentiment intelligence platform that analyzes Reddit discussions using state-of-the-art FinBERT AI to provide real-time market sentiment insights across stocks, industries, and sectors.

---

## ✨ Features

### 🤖 **AI-Powered Sentiment Analysis**
- **FinBERT Model** - Specialized BERT model fine-tuned for financial sentiment analysis (ProsusAI/finbert)
- Real-time classification into Positive, Neutral, and Negative sentiment with confidence scores
- Context-aware analysis understanding financial terminology and market language

### 📊 **Comprehensive Market Intelligence**
- **Market Pulse Dashboard** - Real-time overview of market sentiment trends
- **Most Discussed Stocks** - Track which tickers are generating the most conversation
- **Industry & Sector Analysis** - Aggregated sentiment across market segments
- **Sentiment Heatmaps** - Visual representation of industry-level market mood

### 📡 **Reddit RSS Integration**
- Fetches posts from multiple finance subreddits (r/stocks, r/investing, r/wallstreetbets, etc.)
- **No API keys required** - Uses RSS feeds for seamless data collection
- Configurable subreddit sources and search queries
- Automatic deduplication and post tracking

### 🎯 **Advanced Ticker Intelligence**
- **Smart Ticker Extraction** - Identifies stock symbols in posts with high accuracy
- **False Positive Filtering** - Eliminates common words like "CEO", "PR", "DD"
- **Company Metadata** - Maps tickers to company names, industries, and sectors
- Support for 100+ major stocks with extensible ticker mappings

### 🔍 **Powerful Filtering & Analytics**
- Filter by ticker symbol, industry, sector, sentiment, or date range
- Multi-dimensional data exploration
- Pagination support for large datasets
- Custom time-range analysis (daily/weekly granularity)

### 📉 **Rich Data Visualizations**
- **Sentiment Trends** - Track sentiment changes over time
- **Stock Comparison Charts** - Compare sentiment across multiple tickers
- **Volume-Sentiment Correlation** - Analyze post volume vs. market mood
- **Industry Heatmaps** - Sector-level sentiment distribution
- **Interactive Charts** - Built with Chart.js for dynamic data exploration

### 🎨 **Modern User Interface**
- Responsive React-based frontend
- Clean, intuitive three-panel layout (Overview, Analytics, Posts)
- Clickable posts with direct Reddit links
- Loading states and error handling
- Mobile-friendly responsive design

---

## 🏗️ Architecture

### Backend Stack
- **Framework**: Flask 3.0 with CORS support
- **AI/ML**: HuggingFace Transformers + PyTorch (CPU-optimized)
- **Database**: SQLite with optimized schema
- **Data Source**: Reddit RSS feeds (no authentication required)
- **API**: RESTful v1 API with standardized responses

### Frontend Stack
- **Framework**: React 19 with modern hooks
- **Build Tool**: Vite 7.3 for fast development
- **Charts**: Chart.js 4.5 + react-chartjs-2
- **HTTP Client**: Axios for API communication
- **Styling**: Modern CSS with responsive design

### Database Schema
Enhanced relational schema with:
- **Posts** - Analyzed Reddit posts with full metadata
- **Tickers** - Stock symbols with company info, sector, industry
- **Industries & Sectors** - Hierarchical classification
- **Post-Ticker Relationships** - Many-to-many associations
- **Optimized Indexes** - Fast querying on filters and aggregations

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.8+** with pip
- **Node.js 16+** with npm
- ~2GB disk space for FinBERT model and dependencies

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the database**:
   ```bash
   python migrations.py
   ```

4. **Start the Flask server**:
   ```bash
   python app.py
   ```

   The backend will start on `http://localhost:5000`

   **⚠️ First Run Note**: FinBERT model (~500MB) will be downloaded automatically from HuggingFace. This may take 5-10 minutes depending on your connection.

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install Node dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm run dev
   ```

   The frontend will start on `http://localhost:5173` (Vite default)

### Verify Installation

1. Open `http://localhost:5173` in your browser
2. Click **"Fetch New Posts"** button
3. Wait for Reddit posts to be fetched and analyzed
4. Explore the dashboard, filters, and visualizations

---

## 📖 Usage Guide

### Fetching Posts
1. Click the **"Fetch New Posts"** button in the header
2. Posts are fetched from configured subreddits via RSS
3. Each post is analyzed for sentiment and ticker mentions
4. Results appear in real-time as analysis completes

### Navigating the Dashboard

#### **Overview Tab**
- **Market Pulse** - Quick market sentiment snapshot
- **Key Metrics** - Total posts, sentiment distribution, top stocks
- **Most Discussed/Positive/Negative Stocks** - Ranked lists

#### **Analytics Tab**
- **Sentiment Trends** - Line charts showing sentiment over time
- **Stock Comparison** - Side-by-side ticker sentiment analysis
- **Industry Heatmap** - Sector-level aggregated sentiment
- **Volume-Sentiment Correlation** - Post activity vs. market mood

#### **Posts Tab**
- Paginated list of all analyzed posts
- Individual sentiment scores and extracted tickers
- Direct links to original Reddit discussions
- Sorting and filtering options

### Using Filters

**Ticker Filter**: Select one or multiple stock symbols
- Example: Filter for "AAPL" to see all Apple-related posts

**Industry Filter**: Focus on specific industries
- Example: "Software", "Semiconductors", "Banking"

**Sector Filter**: Broader market segment filtering
- Example: "Technology", "Financial", "Healthcare"

**Sentiment Filter**: Show only positive, negative, or neutral posts

**Date Range**: Analyze specific time periods
- Uses YYYY-MM-DD format
- Supports both start and end dates

### Chart Interactions
- **Hover** over data points for detailed tooltips
- **Click** legend items to toggle datasets
- Charts auto-update when filters change

---

## ⚙️ Configuration

### `config.json`
Located in `backend/config.json`:

```json
{
  "reddit": {
    "subreddits": ["stocks", "StockMarket", "investing", "wallstreetbets", "finance", "options"],
    "user_agent": "finance-sentiment-dashboard/2.0",
    "default_query": "stocks OR finance OR investing OR trading"
  },
  "sentiment": {
    "model": "ProsusAI/finbert",
    "confidence_threshold": 0.6
  },
  "api": {
    "version": "v1",
    "default_page_size": 50,
    "max_page_size": 1000
  },
  "server": {
    "port": 5000,
    "debug": false
  }
}
```

**Key Settings**:
- `subreddits` - List of subreddits to fetch from
- `confidence_threshold` - Minimum confidence for sentiment classification
- `default_page_size` - API pagination size

### `ticker_mappings.json`
Maps ticker symbols to company metadata:

```json
{
  "AAPL": {
    "company": "Apple Inc.",
    "sector": "Technology",
    "industry": "Consumer Electronics"
  }
}
```

**Add New Tickers**: Simply extend this file with new entries following the same structure.

---

## 🔌 API Documentation

Full API documentation available in [API.md](./API.md)

### Quick Examples

**Analyze Custom Text**:
```bash
curl -X POST http://localhost:5000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "NVDA earnings beat expectations! Stock surging."}'
```

**Get Posts for Specific Ticker**:
```bash
curl "http://localhost:5000/api/v1/posts?ticker=TSLA&limit=20"
```

**Compare Multiple Stocks**:
```bash
curl "http://localhost:5000/api/v1/sentiment-comparison?tickers=AAPL,MSFT,GOOGL"
```

**Market Pulse Overview**:
```bash
curl "http://localhost:5000/api/v1/market-pulse"
```

---

## 📁 Project Structure

```
sentiment-analysis-finance-posts/
├── backend/
│   ├── app.py                    # Main Flask application
│   ├── api_utils.py              # API response utilities
│   ├── database.py               # Database layer (repositories pattern)
│   ├── migrations.py             # Database schema migrations
│   ├── sentiment_analyzer.py     # FinBERT sentiment analysis engine
│   ├── ticker_extractor.py       # Stock symbol extraction logic
│   ├── industry_classifier.py    # Industry/sector classification
│   ├── reddit_rss_client.py      # Reddit RSS feed parser
│   ├── config.json               # Application configuration
│   ├── ticker_mappings.json      # Ticker metadata (100+ stocks)
│   ├── known_tickers.json        # Ticker validation list
│   └── requirements.txt          # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.jsx              # Main dashboard component
│   │   │   ├── MarketPulse.jsx            # Market overview widget
│   │   │   ├── SentimentChart.jsx         # Trend line charts
│   │   │   ├── StockComparisonChart.jsx   # Multi-ticker comparison
│   │   │   ├── IndustryHeatmap.jsx        # Sector heatmap visualization
│   │   │   ├── VolumeSentimentChart.jsx   # Volume correlation chart
│   │   │   ├── SentimentByStockChart.jsx  # Per-ticker breakdown
│   │   │   ├── PostsList.jsx              # Paginated posts view
│   │   │   ├── TickerFilter.jsx           # Ticker selection dropdown
│   │   │   ├── IndustryFilter.jsx         # Industry filter
│   │   │   ├── SectorFilter.jsx           # Sector filter
│   │   │   ├── DateRangeFilter.jsx        # Date range picker
│   │   │   ├── LoadingSpinner.jsx         # Loading state component
│   │   │   ├── ErrorMessage.jsx           # Error display
│   │   │   ├── EmptyState.jsx             # Empty data state
│   │   │   └── Tooltip.jsx                # Custom tooltip
│   │   ├── App.jsx                        # Root React component
│   │   ├── main.jsx                       # React entry point
│   │   └── index.css                      # Global styles
│   ├── index.html                         # HTML template
│   ├── vite.config.js                     # Vite build configuration
│   └── package.json                       # Node dependencies
│
├── API.md                        # Complete API documentation
├── README.md                     # This file
└── .gitignore                    # Git ignore rules
```

---

## 🛠️ Technologies Used

### Core Technologies
- **Python 3.8+** - Backend runtime
- **React 19** - Frontend framework
- **Flask 3.0** - Web framework
- **SQLite** - Embedded database
- **Vite 7.3** - Frontend build tool

### AI/ML Libraries
- **transformers 4.48+** - HuggingFace library for FinBERT
- **torch 2.2+** - PyTorch (CPU-optimized)
- **numpy 1.26+** - Numerical computing

### Frontend Libraries
- **axios 1.13** - HTTP client
- **chart.js 4.5** - Charting library
- **react-chartjs-2 5.3** - React Chart.js wrapper
- **react-dom 19.2** - React DOM renderer

### Backend Libraries
- **flask-cors 4.0** - CORS middleware
- **requests 2.31** - HTTP requests
- **python-dateutil 2.8** - Date parsing

---

## 🎯 Features in Detail

### Ticker Extraction
The ticker extraction system uses a multi-stage approach:

1. **Pattern Matching** - Identifies potential ticker symbols using regex (`$SYMBOL` or uppercase words)
2. **Known Ticker Validation** - Checks against a database of 100+ major stocks
3. **False Positive Filtering** - Removes common words (CEO, PR, DD, ETA, etc.)
4. **Context Analysis** - Validates tickers appear in financial context

**Supported Formats**:
- `$AAPL` - Dollar sign prefix
- `AAPL` - Plain uppercase symbols
- `AAPL, MSFT` - Comma-separated lists

### Industry Classification
Automatically categorizes stocks into industries and sectors:

- **Sectors**: Technology, Financial, Healthcare, Energy, Consumer Cyclical, etc.
- **Industries**: Software, Semiconductors, Banking, Pharmaceuticals, etc.
- **Mapping**: Configured via `ticker_mappings.json`
- **Extensibility**: Easy to add new classifications

### Market Pulse
Real-time market overview providing:
- **Most Discussed Stocks** - Ranked by post volume
- **Most Positive Stocks** - Highest average sentiment scores
- **Most Negative Stocks** - Lowest sentiment scores
- **Sentiment by Sector** - Aggregated sector-level metrics
- **Overall Market Sentiment** - Platform-wide average

### Advanced Charts

**Sentiment Trends Chart**
- Daily/weekly sentiment distribution over time
- Stacked area chart showing positive/neutral/negative
- Filterable by ticker, industry, sector, date range

**Stock Comparison Chart**
- Side-by-side sentiment comparison for multiple tickers
- Grouped bar chart visualization
- Shows sentiment score distributions

**Industry Heatmap**
- Color-coded sentiment intensity per industry
- Aggregated metrics with percentage breakdowns
- Quick visual identification of hot/cold sectors

**Volume-Sentiment Correlation**
- Dual-axis chart showing post volume and sentiment
- Identifies trending periods and sentiment shifts
- Useful for spotting market momentum changes

---

## 🗄️ Database Schema

### Tables

**posts**
- Primary post data (title, text, author, subreddit)
- Sentiment analysis results (label, score, confidence)
- Reddit metadata (URL, created_at, reddit_id)

**tickers**
- Stock symbols with company names
- Sector and industry classifications
- Unique constraint on symbol

**industries**
- Industry names and descriptions
- Foreign key relationships to tickers

**sectors**
- Sector names and descriptions
- Foreign key relationships to tickers

**post_tickers** (Junction Table)
- Many-to-many relationship between posts and tickers
- Enables multi-ticker posts

### Indexes
Optimized for common query patterns:
- `idx_posts_sentiment` - Fast sentiment filtering
- `idx_posts_created_at` - Date range queries
- `idx_post_tickers_lookup` - Ticker-post associations

---

## 💻 Development

### Running in Development Mode

**Backend** (with auto-reload):
```bash
cd backend
FLASK_ENV=development python app.py
```

**Frontend** (with HMR):
```bash
cd frontend
npm run dev
```

### Testing Approach

**Manual Testing**:
1. Fetch posts from various subreddits
2. Verify sentiment classifications are reasonable
3. Test all filters independently and in combination
4. Validate chart data accuracy
5. Check API responses against documentation

**Recommended Test Scenarios**:
- Positive sentiment: "AAPL earnings beat! Stock soaring 🚀"
- Negative sentiment: "TSLA recalls, stock plummeting"
- Neutral sentiment: "Fed announces rate decision today"
- Multi-ticker: "Comparing MSFT vs GOOGL performance"

### Building for Production

**Frontend Build**:
```bash
cd frontend
npm run build
```
Output: `frontend/dist/` (static files ready for deployment)

**Backend Deployment**:
- Use production WSGI server (gunicorn, uWSGI)
- Set `debug: false` in config.json
- Enable database backups
- Configure reverse proxy (nginx)

---

## 🐛 Troubleshooting

### Common Issues

**FinBERT Model Download Fails**
```bash
# Manually download model
python -c "from transformers import AutoTokenizer, AutoModelForSequenceClassification; \
AutoTokenizer.from_pretrained('ProsusAI/finbert'); \
AutoModelForSequenceClassification.from_pretrained('ProsusAI/finbert')"
```

**Database Locked Error**
- Ensure only one backend instance is running
- Close any SQLite browser connections
- Check file permissions on `finance_sentiment.db`

**CORS Errors**
- Verify Flask CORS is enabled in `app.py`
- Check frontend is accessing correct backend URL
- Ensure no conflicting CORS headers

**No Posts Fetched from Reddit**
- Verify internet connection
- Check subreddit names in `config.json` are valid
- Reddit RSS feeds may have rate limits (retry after delay)

**Charts Not Rendering**
- Check browser console for JavaScript errors
- Verify Chart.js is loaded (check network tab)
- Ensure data format matches chart component expectations

**Ticker Not Detected**
- Add ticker to `ticker_mappings.json`
- Add to `known_tickers.json` validation list
- Restart backend server to reload configs

### Performance Optimization

**Slow Sentiment Analysis**:
- Use CPU-optimized PyTorch build (already configured)
- Reduce batch size if memory constrained
- Consider GPU support for high-volume deployments

**Database Query Optimization**:
- Indexes are pre-configured for common filters
- Use pagination (`limit` parameter) for large datasets
- Archive old posts to reduce table size

---

## 🚀 Future Enhancements

### Planned Features
- 🔐 **User Authentication** - Multi-user support with saved preferences
- 🔔 **Real-time Alerts** - Notify on sentiment threshold changes
- 📥 **Export Functionality** - CSV/JSON export of filtered data
- 🔍 **Custom Search Queries** - User-defined Reddit searches
- 📊 **Historical Backtesting** - Sentiment vs. actual stock performance
- 🌐 **WebSocket Updates** - Real-time dashboard updates
- 📱 **Mobile App** - Native iOS/Android applications
- 🤖 **Advanced AI Models** - Support for GPT-based analysis
- 📈 **Price Integration** - Live stock price overlays
- 🗂️ **Watchlists** - Save and track custom ticker lists

### Extensibility Ideas
- Multi-language sentiment support
- Cryptocurrency ticker detection
- News aggregation from financial websites
- Social media integration (beyond Reddit)
- Sentiment-based trading signals

---

## 📄 License

**ISC License**

Copyright (c) 2024

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Reporting Bugs
- Open an issue with detailed reproduction steps
- Include error messages, screenshots, and system info
- Check if issue already exists before creating new one

### Suggesting Features
- Open an issue tagged as "enhancement"
- Describe use case and expected behavior
- Consider implementation complexity and scope

### Code Contributions
1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** changes (`git commit -m 'Add amazing feature'`)
4. **Push** to branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines
- Follow existing code style and conventions
- Add comments for complex logic
- Test thoroughly before submitting PR
- Update documentation if adding new features
- Keep commits focused and descriptive

---

## 🙏 Acknowledgments

- **HuggingFace** - For the Transformers library and FinBERT model
- **ProsusAI** - For training and releasing the FinBERT model
- **Reddit** - For providing RSS feeds
- **Chart.js** - For excellent charting capabilities
- **React Team** - For the amazing React framework

---

## 📧 Support

For questions, issues, or suggestions:
- 📝 Open a GitHub issue
- 💬 Check existing documentation in `API.md`
- 🔍 Search closed issues for similar problems

---

**Built with ❤️ for the financial analysis community**
