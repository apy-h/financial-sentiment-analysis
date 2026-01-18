# Finance Sentiment Analysis Web App

A web application that performs real-time sentiment analysis on finance-related Reddit posts using FinBERT, a specialized BERT model fine-tuned for financial sentiment analysis.

## Features

- **Real-time Analysis**: Fetch and analyze finance posts from Reddit RSS feeds (no API keys required)
- **FinBERT Model**: Uses ProsusAI/finbert for accurate financial sentiment classification
- **Interactive Dashboard**: Clean UI showing sentiment statistics, trends, and recent posts
- **Data Persistence**: SQLite database for storing analyzed posts
- **RESTful API**: Flask backend with multiple endpoints for data access

## Architecture

### Backend (Python/Flask)
- **Flask API** with CORS support
- **FinBERT Model** via HuggingFace Transformers
- **Reddit RSS Client** - fetches posts without requiring API authentication
- **SQLite Database** for data storage
- **JSON Configuration** - easy customization via config.json

### Frontend (React/Vite)
- **React 19** with modern hooks
- **Chart.js** for sentiment trend visualization
- **Axios** for API communication
- **Responsive design** with clean CSS

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup
<!-- TODO: add venv -->
1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp ../.env.example .env
# Edit .env and add your X API bearer token (optional)
```

4. Run the backend server:
```bash
python app.py
```

The backend will start on `http://localhost:5000`

**Note**: On first run, the FinBERT model (~500MB) will be downloaded from HuggingFace. This may take a few minutes.

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The frontend will start on `http://localhost:3000`

## Usage

1. **Start both servers** (backend and frontend)
2. **Open the browser** to `http://localhost:3000`
3. **Click "Fetch New Posts"** to analyze finance posts from Reddit RSS feeds
4. **View the dashboard** showing:
   - Sentiment distribution (positive/negative/neutral)
   - Recent analyzed posts with sentiment scores
   - Trend charts over time

## API Endpoints

### Backend API

- `GET /health` - Health check
- `POST /api/analyze` - Analyze custom text
- `GET /api/fetch-posts` - Fetch and analyze new posts from Reddit RSS
- `GET /api/posts` - Get stored analyzed posts
- `GET /api/stats` - Get sentiment statistics
- `GET /api/trends` - Get sentiment trends over time

### Example API Usage

```bash
# Analyze custom text
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Apple stock is performing great today!"}'

# Fetch and analyze posts
curl http://localhost:5000/api/fetch-posts?max_results=10

# Get statistics
curl http://localhost:5000/api/stats
```

## X API Configuration

### Getting an X API Bearer Token (Free Tier)

1. Go to [Twitter Developer Portal](https://developer.twitter.com/)
2. Create a new app or use existing one
3. Configure subreddits in `backend/config.json` (optional - defaults provided)

## Model Information

This app uses **FinBERT** (ProsusAI/finbert), a pre-trained NLP model fine-tuned for financial sentiment analysis. It classifies text into three categories:

- **Positive**: Optimistic financial sentiment
- **Negative**: Pessimistic financial sentiment
- **Neutral**: Neutral or factual financial information

The model is specifically trained on financial texts and performs better than general-purpose sentiment models for finance-related content.

## Project Structure

```
.
├── backend/
│   ├── app.py                 # Flask application
│   ├── sentiment_analyzer.py  # FinBERT sentiment analysis
│   ├── reddit_rss_client.py   # Reddit RSS feed client
│   ├── database.py            # SQLite database operations
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── App.jsx           # Main React app
│   │   ├── main.jsx          # React entry point
│   │   └── index.css         # Styles
│   ├── index.html            # HTML template
│   ├── vite.config.js        # Vite configuration
│   └── package.json          # Node dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## Technologies Used

### Backend
- Flask - Web framework
- Transformers - HuggingFace library for FinBERT
- PyTorch - Deep learning framework
- SQLite - Database
- Requests - HTTP client for X API

### Frontend
- React - UI framework
- Vite - Build tool
- Chart.js - Data visualization
- Axios - HTTP client

## Development

### Running Tests

Run both servers and click "Fetch New Posts" to fetch real Reddit posts via RSS feeds.

### Building for Production

Frontend:
```bash
cd frontend
npm run build
```

The built files will be in `frontend/dist/`

## License

ISC

## Future Enhancements

- User authentication
- Custom search queries
- Historical data analysis
- Export functionality
- Real-time WebSocket updates
- Advanced filtering and sorting
