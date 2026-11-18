# EstateAI – Real Estate AI Chatbot

An AI-powered real estate assistant that helps users explore property projects and listings from **DarGlobal** and **Wasalt** using natural-language questions.

EstateAI combines keyword-based property retrieval, an LLM powered by OpenRouter, and a React chat interface to provide relevant property information with source links.

## Features

- **Natural-language chat:** Ask questions about property projects and listings.
- **Property retrieval:** Search property records using keyword matching and relevance scoring.
- **AI-generated responses:** Generate conversational answers using an OpenRouter-hosted language model.
- **Source references:** Display links to the original property sources.
- **Markdown rendering:** Format responses with headings, lists, bold text, and hyperlinks.
- **Source filtering:** Prioritize Wasalt or DarGlobal when explicitly requested.
- **Fallback handling:** Return a clear message when no matching property is found.
- **Docker support:** Run the frontend and backend using Docker Compose.

## Technology Stack

| Component | Technologies |
|---|---|
| Frontend | React, Vite, CSS |
| Backend | Python, FastAPI |
| Database | SQLite, SQLAlchemy |
| AI Integration | OpenRouter API |
| LLM Client | OpenAI Python SDK |
| Markdown | React Markdown |
| Deployment Environment | Docker, Docker Compose |
| API Communication | REST API |

## Architecture

```text
User
 |
 v
React Frontend
 |
 | POST /api/chat
 v
FastAPI Backend
 |
 v
Property Retrieval Service
 |
 +---------------------+
 |                     |
 v                     v
DarGlobal Projects   Wasalt Listings
 |                     |
 +----------+----------+
            |
            v
     Relevant Context
            |
            v
       OpenRouter API
            |
            v
    Generated Response
            |
            v
       React Chat UI
            |
            v
    Answer + Source Links
```

## Project Structure

```text
real-estate-ai-chatbot/
│
├── backend/
│   ├── app/
│   │   ├── database/
│   │   ├── routes/
│   │   ├── scraper/
│   │   ├── services/
│   │   ├── schemas/
│   │   ├── config.py
│   │   └── main.py
│   │
│   ├── tests/
│   ├── requirements.txt
│   ├── init_db.py
│   ├── seed_db.py
│   ├── seed_wasalt.py
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
│
├── data/
│   ├── raw/
│   └── processed/
│
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md
```

## Data Sources

The application currently uses manually curated property records from:

### 1. DarGlobal

Includes five property project records, covering developments in Dubai, London, and Oman.

Examples:
- D-Villas at Jumeirah Golf Estates
- DG1
- The Great Escape 2
- The Mulliner
- 7&8 Albert Hall Mansions

Source: [DarGlobal Official Website](https://darglobal.co.uk/)

### 2. Wasalt

Includes a manually curated property listing:

- Property: 81 sqm Floor with 3 Bedrooms
- Location: Riyadh, Saudi Arabia
- Area: 81 sqm
- Price: 1,195,000 SAR

Source: [Wasalt Official Website](https://wasalt.sa/)

**Data note:** The current database contains a limited sample of manually collected property records. It is not a comprehensive or continuously updated property database. Listing details and availability should be verified with the original sources.

## How Property Retrieval Works

1. The user submits a natural-language question.
2. FastAPI receives the request through `/api/chat`.
3. The retrieval service tokenizes the question and property records.
4. It identifies matching keywords and calculates relevance scores.
5. Relevant property records are selected from SQLite.
6. The retrieved information is passed to the OpenRouter language model.
7. The model generates an answer using the supplied property context.
8. The API returns the answer and matching source links.

**Important:** The current implementation uses keyword-based retrieval and relevance scoring. It does not use embeddings, semantic vector search, or a vector database.

## Getting Started

### Prerequisites

Install the following:

- Python 3.11 or later
- Node.js 22 or later
- Docker Desktop
- An OpenRouter API key

### 1. Clone the Repository

```bash
git clone https://github.com/SurajPandey-01/real-estate-ai-chatbot.git

cd real-estate-ai-chatbot
```

### 2. Configure Environment Variables

Create your local environment file:

```bash
cp .env.example .env
```

Open `.env` and configure:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_MODEL=openrouter/free
DATABASE_URL=sqlite:///./realestate.db
```

Replace the placeholder with your own OpenRouter API key.

**Security:** Never commit `.env` or expose API keys in public repositories.

### 3. Run with Docker Compose

Build and start the application:

```bash
docker compose up --build -d
```

Check running containers:

```bash
docker compose ps
```

### 4. Access the Application

| Service | URL |
|---|---|
| React Frontend | http://localhost:8080 |
| FastAPI Backend | http://localhost:8000 |
| API Documentation | http://localhost:8000/docs |
| Health Check | http://localhost:8000/health |

### 5. Stop the Application

```bash
docker compose down
```

## API Endpoints

### Health Check

`GET /health`

Returns the backend health status.

Example response:

```json
{
  "status": "healthy"
}
```

### Chat Endpoint

`POST /api/chat`

Accepts a natural-language property question.

Request:

```json
{
  "message": "Which villa projects are available in Dubai?"
}
```

Response structure:

```json
{
  "answer": "The matching property information...",
  "sources": [
    {
      "name": "D-Villas at Jumeirah Golf Estates",
      "source": "DarGlobal",
      "url": "https://darglobal.co.uk/d-villas-at-jge"
    }
  ]
}
```

## Example Questions

- Which villa projects are available in Dubai?
- What is the price and area of the Wasalt property with 3 bedrooms?
- Show me properties in Riyadh.
- Tell me about D-Villas at Jumeirah Golf Estates.
- What amenities are available at DG1?

## Current Limitations

- The property database contains a limited number of manually curated records.
- Property information is not automatically refreshed.
- Retrieval uses keyword matching rather than semantic vector search.
- AI response generation depends on OpenRouter API availability and model access.
- Prices, listing status, and project details should be verified with the original property source.

## Future Improvements

- Expand the property database with additional verified listings.
- Introduce embedding-based semantic retrieval.
- Add filters for location, price, property type, and bedrooms.
- Improve property comparison and recommendation functionality.
- Add automated data validation and database update workflows.
- Deploy the application to a public hosting platform.

## Author

**Suraj Kumar Pandey**

- GitHub: [SurajPandey-01](https://github.com/SurajPandey-01)

---

Built as a real estate AI chatbot project using React, FastAPI, SQLite, and OpenRouter.