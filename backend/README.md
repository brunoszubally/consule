# AI Tanács - Backend API

FastAPI backend for the AI Council multi-agent system with real-time WebSocket support.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
nano .env  # or use your favorite editor
```

Add your API keys:
```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

### 3. Run the Server

```bash
# Development mode (auto-reload)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or using Python
python main.py
```

Server will start at: **http://localhost:8000**

## 📡 API Endpoints

### REST API

#### `GET /`
Health check and service info

#### `GET /api/agents`
Get list of all 12 agents with their info

#### `GET /api/health`
Health check endpoint

#### `POST /api/ask`
Ask the AI Council a question

**Request:**
```json
{
  "question": "Minek tanuljak programozni?",
  "weights": {
    "STR": 1.5,
    "TEC": 1.8,
    "PRA": 1.6
  },
  "voting_method": "borda"
}
```

**Response:**
```json
{
  "question": "Minek tanuljak programozni?",
  "winner": "Winner response text...",
  "winner_score": 9.2,
  "all_responses": [...],
  "voting_scores": {...},
  "voting_method": "borda",
  "total_time_seconds": 14.5,
  "timestamp": "2025-11-06T12:34:56"
}
```

### WebSocket API

#### `WS /ws/ask`
Real-time agent updates via WebSocket

**Connect and send:**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/ask');

ws.onopen = () => {
  ws.send(JSON.stringify({
    question: "Minek tanuljak programozni?",
    weights: { STR: 1.5, TEC: 1.8 },
    voting_method: "borda"
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data);
};
```

**Message Types:**
- `status` - Phase updates (thinking, responding, voting, complete)
- `agent_update` - Individual agent progress
- `result` - Final council decision
- `error` - Error messages

## 🤖 The 12 Agents

| Agent | Short | Speed | Provider | Specialty |
|-------|-------|-------|----------|-----------|
| Stratéga | STR | 0.9x | OpenAI GPT-4o-mini | Long-term strategy |
| Kreatív | CRE | 1.2x | OpenAI GPT-4o-mini | Innovation |
| Praktikus | PRA | 1.3x | OpenAI GPT-4o-mini | Practical solutions |
| Filozófus | PHI | 0.7x | OpenAI GPT-4o-mini | Ethics & values |
| Technikus | TEC | 1.4x | OpenAI GPT-4o-mini | Technical expertise |
| Szkeptikus | SKE | 0.8x | OpenAI GPT-4o-mini | Critical analysis |
| Empatikus | EMP | 1.1x | OpenAI GPT-4o-mini | Human factors |
| Kísérleti | KIS | 1.0x | OpenAI GPT-4o-mini | Data-driven science |
| Történelem | TÖR | 0.9x | OpenAI GPT-4o-mini | Historical patterns |
| Gyakorlati | GYO | 1.5x | OpenAI GPT-4o-mini | Fast execution |
| Részletes | RÉS | 0.8x | OpenAI GPT-4o-mini | Attention to detail |
| Humorista | HUM | 1.1x | OpenAI GPT-4o-mini | Lighter perspective |

## 🗳️ Voting Methods

- **`borda`** (default) - Weighted Borda Count
- **`irv`** - Instant Runoff Voting
- **`mrr`** - Mean Reciprocal Rank
- **`hybrid`** - 40% Borda + 40% MRR + 20% IRV

## 📁 Project Structure

```
backend/
├── main.py              # FastAPI app + WebSocket
├── config.py            # Settings & environment
├── voting.py            # Voting mechanisms
├── api_client.py        # OpenAI/Anthropic client
├── agents/
│   ├── __init__.py
│   ├── base.py          # BaseAgent class
│   └── council.py       # 12 agent implementations
├── requirements.txt     # Dependencies
├── .env.example         # Environment template
└── README.md            # This file
```

## 🔧 Configuration

Edit `.env` to customize:

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | 0.0.0.0 | Server host |
| `PORT` | 8000 | Server port |
| `MAX_TOKENS` | 500 | Max response tokens |
| `TEMPERATURE` | 0.7 | AI creativity (0-1) |
| `TIMEOUT_SECONDS` | 30 | API call timeout |
| `VOTING_METHOD` | borda | Default voting method |

## 📊 Performance

- **Response Time:** ~10-15s (parallel execution)
- **Concurrent Requests:** Supports multiple WebSocket connections
- **Cost per Query:** ~$0.15-0.40 (depending on models used)

## 🧪 Testing

Test the API with curl:

```bash
# Health check
curl http://localhost:8000/api/health

# Get agents
curl http://localhost:8000/api/agents

# Ask a question
curl -X POST http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Mi a jövője a mesterséges intelligenciának?",
    "voting_method": "borda"
  }'
```

## 📝 Notes

- **API Keys Required:** You need OpenAI and/or Anthropic API keys
- **Costs:** Each query calls up to 12 LLM APIs (parallel)
- **Rate Limits:** Respect provider rate limits
- **Mock Mode:** Works without API keys (returns mock responses)

## 🐛 Troubleshooting

**No responses?**
- Check API keys in `.env`
- Check rate limits
- Check internet connection

**Slow responses?**
- Some agents (Filozófus) are intentionally slower
- Check provider API latency
- Consider using GPT-3.5 for faster agents

**CORS errors?**
- Update `CORS_ORIGINS` in `.env`
- Restart server after config changes

## 📚 Next Steps

1. ✅ Set up API keys
2. ✅ Test REST API endpoint
3. ✅ Test WebSocket connection
4. 🔜 Connect frontend to backend
5. 🔜 Deploy to production
