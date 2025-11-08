# 🤖 Hogyan Működnek az AI Tanács Ágensek?

## 🎯 Áttekintés

Az AI Tanács egy **multi-agent rendszer**, ahol **12 különböző "személyiségű" AI ágens** dolgozik együtt hogy a legjobb választ adja egy kérdésre.

## 🏗️ Architektúra

```
Felhasználó Kérdése
        ↓
   [AI Tanács]
        ↓
  ┌─────────────────────────────────────┐
  │  12 Ágens Párhuzamosan Dolgozik     │
  ├─────────────────────────────────────┤
  │  1. Stratéga    → GPT-4o-mini      │
  │  2. Kreatív     → GPT-4o-mini      │
  │  3. Praktikus   → GPT-4o-mini      │
  │  4. Filozófus   → GPT-4o-mini      │
  │  5. Technikus   → GPT-4o-mini      │
  │  6. Szkeptikus  → GPT-4o-mini      │
  │  7. Empatikus   → GPT-4o-mini      │
  │  8. Kísérleti   → GPT-4o-mini      │
  │  9. Történész   → GPT-4o-mini      │
  │  10. Gyakorlati → GPT-4o-mini      │
  │  11. Részletes  → GPT-4o-mini      │
  │  12. Humorista  → GPT-4o-mini      │
  └─────────────────────────────────────┘
        ↓
   [Szavazás]
   - Borda Count
   - IRV
   - MRR
   - Hybrid
        ↓
  [Legjobb Válasz]
```

## 🧠 Hogyan Működik egy Ágens?

### 1. BaseAgent Osztály

Minden ágens egy `BaseAgent` osztályból származik:

```python
class BaseAgent(ABC):
    def __init__(
        self,
        name: str,              # Ágens neve (pl. "Stratéga")
        short_name: str,        # Rövidítés (pl. "STR")
        color: str,             # Hex color (#3b82f6)
        bio: str,               # Rövid leírás
        expertise: list[str],   # Szakértői területek
        speed_multiplier: float, # Sebesség (0.7 - 1.5x)
        provider: str,          # "openai"
        model: str              # "gpt-4o-mini"
    ):
```

### 2. System Prompt = Személyiség

Minden ágensnek van egy **system prompt** ami definiálja a személyiségét:

**Példa - Filozófus:**
```python
def get_system_prompt(self) -> str:
    return """Filozófus vagy - a mélyebb értékeket és jelentést keresed.
Gondolkodj:
- Mi a helyes dolog etikailag?
- Milyen értékeket tükröz ez?
- Mi a döntés filozófiai jelentősége?
- Hogyan hat ez az emberi kondícióra?

Lassan gondolkodj, de mélyen. Adj perspektívát az élet nagy kérdéseihez."""
```

**Példa - Gyakorlati:**
```python
def get_system_prompt(self) -> str:
    return """Praktikus executor vagy - a leggyorsabb út a megoldáshoz.
Fókuszálj:
- Mi az első lépés MOST?
- Hogyan kezdjük el AZONNAL?
- Mi a MVP (Minimum Viable Product)?
- Quick wins - mik a gyors győzelmek?

Légy akcióorientált. Tömör, gyors, konkrét lépések. Nincs idő filozofálni."""
```

### 3. Think Metódus - Az Ágens "Gondolkodik"

Amikor kérdést kapsz, minden ágens meghívja a `think()` metódust:

```python
async def think(self, question: str, context: Optional[Dict] = None, api_client = None):
    # 1. Status: thinking
    self.status = "thinking"
    self.progress = 0

    # 2. Prompt összeállítás
    full_prompt = f"{self.get_base_prompt_prefix()}\n\n{self.get_system_prompt()}\n\nKérdés: {question}"

    # 3. OpenAI API hívás
    response_text, confidence = await self._call_api(full_prompt, question, api_client)

    # 4. Status: complete
    self.status = "complete"
    self.progress = 100

    # 5. Visszatérés válasszal
    return {
        "agent": self.name,
        "text": response_text,
        "confidence": confidence,
        "score": confidence,  # Ez számít a szavazásban!
        "elapsed_seconds": elapsed,
        "color": self.color,
        "bio": self.bio
    }
```

### 4. Változó Sebességek

Minden ágensnek más a **speed_multiplier** értéke:

| Ágens | Sebesség | Miért? |
|-------|----------|--------|
| **Filozófus** | 0.7x 🐢 | Mély gondolkodás, lassú |
| **Részletes** | 0.75x | Alapos elemzés |
| **Történész** | 0.9x | Kontextus keresés |
| **Gyakorlati** | 1.5x 🚀 | Gyors, akcióorientált |
| **Technikus** | 1.4x | Hatékony problémamegoldás |
| **Praktikus** | 1.3x | Pragmatikus megközelítés |

Ez **vizuálisan látszik** a frontend-en - a Filozófus később fejezi be mint a Gyakorlati!

## 🗳️ Szavazási Rendszer

Miután mind a 12 ágens válaszolt, **szavazás** dönt:

### 1. Borda Count (Default)

```python
def borda_count(responses: List[Dict], weights: Dict[str, float]):
    n = len(responses)
    scores = {}

    for i, response in enumerate(responses):
        agent_name = response["agent"]
        weight = weights.get(agent_name, 1.0)  # Súly kérdésenként
        base_score = response["score"]         # Confidence (0-10)

        # Borda pontok: (n - position) * weight * score
        borda_points = (n - i) * weight * base_score
        scores[response["text"]] = borda_points

    # Legnagyobb pontszámú nyeri
    winner = max(scores.items(), key=lambda x: x[1])
    return winner[0], scores
```

**Példa:**
- 12 ágens válaszolt
- Filozófus válasza: 1. hely → 12 pont × 1.4 weight × 9.2 confidence = **154.56 pont**
- Gyakorlati válasza: 5. hely → 8 pont × 1.6 weight × 8.1 confidence = **103.68 pont**

### 2. Súlyok (Weights) - Kérdésenként Változnak!

Minden kérdéshez **különböző súlyok**:

**Kérdés: "Minek tanuljak programozni?"**
```python
weights = {
    'TEC': 1.9,  # Technikus súlya magas (releváns!)
    'PRA': 1.8,  # Praktikus
    'GYO': 1.6,  # Gyakorlati
    'PHI': 1.2,  # Filozófus (kevésbé releváns)
    'HUM': 1.1   # Humorista
}
```

**Kérdés: "Online vs offline tanulás?"**
```python
weights = {
    'HUM': 1.8,  # Humanista súlya magas (emberi tanulás!)
    'EMP': 1.7,  # Empatikus
    'PRA': 1.6,  # Praktikus
    'TEC': 1.3   # Technikus (kevésbé releváns)
}
```

## 🔄 Teljes Flow - Lépésről Lépésre

### 1. Frontend Kérdés Elküldése (WebSocket)

```javascript
ws.send(JSON.stringify({
    question: "Minek tanuljak programozni?",
    weights: { STR: 1.5, TEC: 1.9, PRA: 1.6 },
    voting_method: "borda"
}));
```

### 2. Backend - Párhuzamos Agent Végrehajtás

```python
# main.py - WebSocket handler
async def websocket_ask(websocket: WebSocket):
    # Fogadd a kérdést
    data = await websocket.receive_json()
    question = data["question"]

    # 12 agent párhuzamosan fut!
    tasks = [agent.think(question, api_client=api_client) for agent in council]
    responses = await asyncio.gather(*tasks)  # ⚡ Párhuzamos!

    # Válaszok rendezése
    responses_sorted = sorted(responses, key=lambda x: x["score"], reverse=True)

    # Szavazás
    voting_fn = get_voting_system("borda")
    winner_text, voting_scores = voting_fn(responses_sorted, weights)

    # Eredmény visszaküldése
    await websocket.send_json({
        "type": "result",
        "winner": winner_text,
        "all_responses": responses_sorted,
        "voting_scores": voting_scores
    })
```

### 3. Frontend - Vizualizáció

A frontend **real-time** kapja az update-eket:

```javascript
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);

    if (data.type === 'agent_update') {
        // Agent status frissítés
        const agent = demoAgents.find(a => a.name === data.agent);
        agent.status = data.status;      // 'thinking' → 'responding' → 'complete'
        agent.progress = data.progress;  // 0 → 100%
    }

    if (data.type === 'result') {
        // Végeredmény megjelenítése
        showRealResults(data);
    }
};
```

## 📊 Példa - Egy Kérdés Életciklusa

```
T=0s    : User kérdés: "Minek tanuljak programozni?"
T=0.5s  : WebSocket connection established
T=1s    : Mind a 12 agent elkezd gondolkodni
          ├─ Filozófus (0.7x sebesség) → lassú
          ├─ Technikus (1.4x sebesség) → gyors
          └─ Gyakorlati (1.5x sebesség) → leggyorsabb

T=3s    : Gyakorlati ágens kész! ✓
          Response: "AI copilot vagy, nem autopilot..."
          Confidence: 8.7/10

T=4.5s  : Technikus ágens kész! ✓
          Response: "Az AI kódot ír, DE te kell hogy tudd..."
          Confidence: 9.1/10

T=7s    : Filozófus ágens kész! ✓ (leglassabb)
          Response: "A programozás problémamegoldás..."
          Confidence: 8.4/10

T=8s    : Mind a 12 ágens válaszolt!

T=8.5s  : Szavazás (Borda Count)
          - Technikus (9.1 × 1.9 weight) = 17.29 pont
          - Gyakorlati (8.7 × 1.6 weight) = 13.92 pont
          - Filozófus (8.4 × 1.2 weight) = 10.08 pont

T=9s    : Nyertes: Technikus válasza! 🏆
          "Az AI kódot ír, DE te kell hogy tudd mi a jó kód..."

T=9.5s  : Frontend megjeleníti Top 3 választ
```

## 🎨 Miért Jó Ez a Rendszer?

### ✅ Előnyök

1. **Sokféle Perspektíva** - 12 különböző nézőpont
2. **Súlyozott Döntés** - Releváns ágensek számítanak többet
3. **Párhuzamos Végrehajtás** - Gyors (8-15s)
4. **Robusztus** - Ha 1-2 ágens rossz választ ad, a szavazás kijavítja
5. **Látható "Gondolkodás"** - User látja hogy az ágensek dolgoznak

### 🎯 Mikor Melyik Ágens Számít?

| Kérdés Típusa | Fontos Ágensek | Kevésbé Fontos |
|---------------|----------------|----------------|
| **Technikai** | Technikus, Praktikus, Kísérleti | Filozófus, Humorista |
| **Etikai** | Filozófus, Empatikus, Humanista | Gyakorlati, Technikus |
| **Üzleti** | Stratéga, Szkeptikus, Részletes | Humorista, Történész |
| **Kreatív** | Kreatív, Humorista, Filozófus | Részletes, Gyakorlati |

## 🔧 Debugging - Hogyan Nézheted Meg?

### 1. Backend Log-ok

```bash
cd backend
uvicorn main:app --reload

# Látsz ilyeneket:
INFO: Agent Filozófus started thinking...
INFO: Agent Filozófus completed in 4.2s (confidence: 8.4)
INFO: Voting winner: Technikus (score: 17.29)
```

### 2. Frontend Console

```javascript
// Nyisd meg a böngésző Console-t (F12)
// Látod a WebSocket üzeneteket:

{type: 'agent_update', agent: 'Filozófus', status: 'thinking'}
{type: 'agent_update', agent: 'Filozófus', status: 'complete', response: {...}}
{type: 'result', winner: '...', all_responses: [...]}
```

### 3. API Tesztelés

```bash
# Kérdezd az AI Tanácsot közvetlenül
curl -X POST http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Mi a jövője az AI-nak?",
    "voting_method": "borda"
  }' | jq .
```

## 📚 Összefoglalás

**1 Kérdés → 12 Ágens → 12 Válasz → Szavazás → 1 Legjobb Válasz**

- Minden ágens **egyedi személyiség** (system prompt)
- Minden ágens **OpenAI GPT-4o-mini**
- **Párhuzamos** végrehajtás (async)
- **Változó sebességek** (0.7x - 1.5x)
- **Súlyozott szavazás** (kérdésenként más súlyok)
- **Real-time** frontend frissítés (WebSocket)

**Eredmény:** Sokféle nézőpont kombinálva → jobb, kiegyensúlyozottabb válasz! 🎯
