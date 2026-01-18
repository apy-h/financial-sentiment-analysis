# API Documentation

## Finance Sentiment Analysis Dashboard - API v1

Base URL: `http://localhost:5000/api/v1`

All API responses follow a standardized format:

### Success Response Format
```json
{
  "success": true,
  "data": { ... },
  "meta": { ... }  // Optional, for pagination
}
```

### Error Response Format
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message"
  }
}
```

## HTTP Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request parameters
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## Endpoints

### Health Check

#### `GET /api/v1/health`

Check if the API is running.

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "timestamp": "2024-01-18T10:30:00.000000",
    "version": "v1"
  }
}
```

---

### Text Analysis

#### `POST /api/v1/analyze`

Analyze sentiment of custom text.

**Request Body:**
```json
{
  "text": "Apple stock is performing great today!"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "sentiment": {
      "label": "positive",
      "score": 0.92,
      "scores": {
        "positive": 0.92,
        "negative": 0.04,
        "neutral": 0.04
      }
    },
    "tickers": ["AAPL"]
  }
}
```

---

### Fetch Posts

#### `GET /api/v1/fetch-posts`

Fetch and analyze new Reddit posts.

**Query Parameters:**
- `query` (optional) - Search query (default: "stocks OR finance OR investing")
- `max_results` (optional) - Maximum posts to fetch (1-100, default: 10)

**Response:**
```json
{
  "success": true,
  "data": {
    "posts": [...],
    "count": 15
  }
}
```

---

### Get Posts

#### `GET /api/v1/posts`

Retrieve stored posts with filtering and pagination.

**Query Parameters:**
- `page` (optional) - Page number (default: 1)
- `limit` (optional) - Items per page (default: 50, max: 1000)
- `ticker` (optional) - Filter by ticker symbol (e.g., "AAPL")
- `industry` (optional) - Filter by industry name
- `sector` (optional) - Filter by sector name
- `sentiment` (optional) - Filter by sentiment: "positive", "negative", "neutral"
- `start_date` (optional) - Start date in YYYY-MM-DD format
- `end_date` (optional) - End date in YYYY-MM-DD format

**Example:**
```
GET /api/v1/posts?ticker=AAPL&sentiment=positive&limit=20
```

**Response:**
```json
{
  "success": true,
  "data": [...],
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 145,
    "total_pages": 8,
    "has_next": true,
    "has_prev": false
  }
}
```

---

### Get Tickers

#### `GET /api/v1/tickers`

Get all unique tickers detected across posts.

**Response:**
```json
{
  "success": true,
  "data": {
    "tickers": [
      {
        "symbol": "AAPL",
        "company_name": "Apple Inc.",
        "sector": "Technology",
        "industry": "Consumer Electronics"
      },
      ...
    ]
  }
}
```

---

### Get Industries

#### `GET /api/v1/industries`

Get all unique industries.

**Response:**
```json
{
  "success": true,
  "data": {
    "industries": [
      {"id": 1, "name": "Consumer Electronics"},
      {"id": 2, "name": "Software"},
      ...
    ]
  }
}
```

---

### Get Sectors

#### `GET /api/v1/sectors`

Get all unique sectors.

**Response:**
```json
{
  "success": true,
  "data": {
    "sectors": [
      {"id": 1, "name": "Technology"},
      {"id": 2, "name": "Financial"},
      ...
    ]
  }
}
```

---

### Get Statistics

#### `GET /api/v1/stats`

Get sentiment statistics with optional filtering.

**Query Parameters:**
- `ticker` (optional) - Filter by ticker
- `industry` (optional) - Filter by industry
- `sector` (optional) - Filter by sector
- `start_date` (optional) - Start date (YYYY-MM-DD)
- `end_date` (optional) - End date (YYYY-MM-DD)

**Response:**
```json
{
  "success": true,
  "data": {
    "total": 250,
    "by_sentiment": {
      "positive": {
        "count": 120,
        "percentage": 48.0
      },
      "neutral": {
        "count": 80,
        "percentage": 32.0
      },
      "negative": {
        "count": 50,
        "percentage": 20.0
      }
    }
  }
}
```

---

### Get Trends

#### `GET /api/v1/trends`

Get sentiment trends over time.

**Query Parameters:**
- `days` (optional) - Number of days to include (default: 7, max: 365)
- `ticker` (optional) - Filter by ticker
- `industry` (optional) - Filter by industry
- `sector` (optional) - Filter by sector
- `start_date` (optional) - Start date (YYYY-MM-DD)
- `end_date` (optional) - End date (YYYY-MM-DD)
- `granularity` (optional) - "day" or "week" (default: "day")

**Response:**
```json
{
  "success": true,
  "data": {
    "trends": [
      {
        "date": "2024-01-15",
        "positive": 45,
        "neutral": 30,
        "negative": 25
      },
      ...
    ]
  }
}
```

---

### Get Sentiment by Ticker

#### `GET /api/v1/sentiment-by-ticker`

Get sentiment breakdown per ticker.

**Query Parameters:**
- `tickers` (optional) - Comma-separated ticker symbols (e.g., "AAPL,TSLA,NVDA")
- `start_date` (optional) - Start date (YYYY-MM-DD)
- `end_date` (optional) - End date (YYYY-MM-DD)

**Response:**
```json
{
  "success": true,
  "data": {
    "ticker_sentiments": [
      {
        "ticker": "AAPL",
        "sentiments": {
          "positive": 85,
          "neutral": 40,
          "negative": 20
        },
        "avg_scores": {
          "positive": 0.82,
          "neutral": 0.45,
          "negative": 0.19
        }
      },
      ...
    ]
  }
}
```

---

### Compare Tickers

#### `GET /api/v1/sentiment-comparison`

Compare sentiment of multiple tickers side-by-side.

**Query Parameters:**
- `tickers` (required) - Comma-separated ticker symbols (e.g., "AAPL,TSLA,NVDA")
- `start_date` (optional) - Start date (YYYY-MM-DD)
- `end_date` (optional) - End date (YYYY-MM-DD)

**Response:**
```json
{
  "success": true,
  "data": {
    "comparison": [...]
  }
}
```

---

### Industry Heatmap

#### `GET /api/v1/industry-heatmap`

Get industry-level sentiment aggregation.

**Query Parameters:**
- `start_date` (optional) - Start date (YYYY-MM-DD)
- `end_date` (optional) - End date (YYYY-MM-DD)

**Response:**
```json
{
  "success": true,
  "data": {
    "heatmap": [
      {
        "industry": "Consumer Electronics",
        "total": 145,
        "sentiments": {
          "positive": {"count": 85, "percentage": 58.62},
          "neutral": {"count": 40, "percentage": 27.59},
          "negative": {"count": 20, "percentage": 13.79}
        }
      },
      ...
    ]
  }
}
```

---

### Market Pulse

#### `GET /api/v1/market-pulse`

Get market overview metrics.

**Query Parameters:**
- `start_date` (optional) - Start date (YYYY-MM-DD)
- `end_date` (optional) - End date (YYYY-MM-DD)

**Response:**
```json
{
  "success": true,
  "data": {
    "most_discussed_stocks": [
      {
        "ticker": "AAPL",
        "post_count": 145,
        "avg_sentiment_score": 0.72
      },
      ...
    ],
    "most_positive_stocks": [
      {
        "ticker": "NVDA",
        "avg_sentiment": 0.85,
        "post_count": 67
      },
      ...
    ],
    "most_negative_stocks": [
      {
        "ticker": "TSLA",
        "avg_sentiment": -0.62,
        "post_count": 89
      },
      ...
    ],
    "sentiment_by_sector": {
      "Technology": {
        "positive": 45,
        "neutral": 30,
        "negative": 25
      },
      ...
    },
    "overall_market_sentiment": {
      "average_score": 0.12,
      "distribution": {
        "positive": 40,
        "neutral": 35,
        "negative": 25
      }
    }
  }
}
```

---

### Volume-Sentiment Correlation

#### `GET /api/v1/volume-sentiment-correlation`

Get post volume vs sentiment over time.

**Query Parameters:**
- `days` (optional) - Number of days (default: 7, max: 365)
- `ticker` (optional) - Filter by ticker
- `start_date` (optional) - Start date (YYYY-MM-DD)
- `end_date` (optional) - End date (YYYY-MM-DD)

**Response:**
```json
{
  "success": true,
  "data": {
    "correlation": [
      {
        "date": "2024-01-15",
        "volume": 100,
        "avg_sentiment": 0.15,
        "positive": 45,
        "neutral": 30,
        "negative": 25
      },
      ...
    ]
  }
}
```

---

## Error Codes

| Code | Description |
|------|-------------|
| `INVALID_JSON` | Request body is not valid JSON |
| `NO_TEXT` | No text provided for analysis |
| `INVALID_PARAM` | Invalid query parameter |
| `MISSING_PARAM` | Required parameter missing |
| `INVALID_TICKER` | Ticker symbol not found |
| `DATABASE_ERROR` | Database operation failed |
| `FETCH_ERROR` | Error fetching posts from Reddit |

---

## Rate Limiting

Currently, there are no rate limits enforced. This may change in future versions.

---

## Legacy Endpoints (Deprecated)

The following endpoints are maintained for backward compatibility but may be removed in future versions:

- `GET /health` → Use `/api/v1/health`
- `POST /api/analyze` → Use `/api/v1/analyze`
- `GET /api/fetch-posts` → Use `/api/v1/fetch-posts`
- `GET /api/posts` → Use `/api/v1/posts`
- `GET /api/stats` → Use `/api/v1/stats`
- `GET /api/trends` → Use `/api/v1/trends`

---

## Examples

### Fetch Recent Posts for AAPL

```bash
curl "http://localhost:5000/api/v1/posts?ticker=AAPL&limit=10"
```

### Get Positive Sentiment Posts from Last Week

```bash
curl "http://localhost:5000/api/v1/posts?sentiment=positive&start_date=2024-01-11&end_date=2024-01-18"
```

### Compare AAPL vs TSLA Sentiment

```bash
curl "http://localhost:5000/api/v1/sentiment-comparison?tickers=AAPL,TSLA"
```

### Get Market Pulse for Today

```bash
curl "http://localhost:5000/api/v1/market-pulse?start_date=2024-01-18"
```
