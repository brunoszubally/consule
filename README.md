# 🤖 AI Tanács (AI Council)

> **Voting-Based Multi-Agent AI System** - Production-ready architektúra egy 12 ágenses döntéshozatali rendszer megvalósításához.

## 📋 Projekt Áttekintés

Az **AI Tanács** egy többágenses AI rendszer, amely 12 különböző perspektívájú AI modellt kombinál súlyozott szavazási mechanizmussal a legmegbízhatóbb döntéshozatal érdekében.

### Főbb Jellemzők

- 🎯 **12 AI Ágens** különböző személyiségekkel és szakértői területekkel
- ⚡ **~14s válaszidő** párhuzamos feldolgozással
- 🗳️ **Súlyozott szavazás** (Borda Count, IRV, MRR kombinációja)
- 📊 **6 alternatív architektúra** különböző használati esetekre
- 🏗️ **3 fázisú implementációs terv** MVP-től enterprise-ig

## 📚 Dokumentáció

### Interaktív Implementációs Terv

A projekt részletes tervezési dokumentációja elérhető **interaktív HTML formátumban**:

📄 **[docs/ai-tanacs-implementation-plan.html](docs/ai-tanacs-implementation-plan.html)**

#### Interaktív Funkciók

A dokumentáció tartalmazza:

- ✨ **Particle rendszer** - Interaktív háttér animációkkal
- 🎯 **Custom cursor** - Világító kurzor effekt
- 🔢 **Animált számlálók** - Count-up animációk
- 🎴 **3D kártya effektek** - Mouse-követéses tilt
- 📊 **Smooth scroll reveal** - Scroll-alapú animációk
- 💫 **Timeline animációk** - Pulzáló idővonalas megjelenítés
- 🌈 **Gradient effektek** - Dinamikus színátmenetek
- 🚀 **Progress tracking** - Scroll progress bar

#### Megnyitás

Egyszerűen nyisd meg a fájlt böngészőben:

```bash
# Linux/Mac
open docs/ai-tanacs-implementation-plan.html

# Windows
start docs/ai-tanacs-implementation-plan.html

# Vagy használj egy helyi szervert
python -m http.server 8000
# Majd nyisd meg: http://localhost:8000/docs/ai-tanacs-implementation-plan.html
```

## 🏗️ Architektúrák

A dokumentáció 6 különböző megközelítést mutat be:

1. **Standard 12-ágent Council** - Kiegyensúlyozott, párhuzamos feldolgozás
2. **Hierarchikus Modell** - Cost-efficient, domain-specifikus
3. **Iteratív Deliberáció** - Maximum minőség, deliberatív konszenzus
4. **Dinamikus Válogató** - Adaptív team composition
5. **Adversarial Council** - Red-team validated outputs
6. **Hybrid Ensemble** - Best of both worlds

## 🚀 Implementációs Fázisok

### Fázis 1: MVP (2-3 hét)
- 6 ágens egyszerűsített személyiségekkel
- Simple majority voting
- REST API (FastAPI)
- **Target:** <10s response, 70%+ satisfaction

### Fázis 2: Production-Ready (3-4 hét)
- 12 teljes ágens
- Weighted Borda Count
- Redis cache + PostgreSQL
- **Target:** <14s response, 80%+ satisfaction

### Fázis 3: Advanced Features (4-6 hét)
- Iteratív deliberáció
- User memória (Vector DB)
- Kubernetes deployment
- **Target:** 99.5% uptime, 85%+ satisfaction

## 🛠️ Tech Stack

- **Backend:** Python 3.11+, FastAPI, Celery
- **Database:** PostgreSQL 15+ (pgvector), Redis 7+
- **AI Integration:** LangChain (OpenAI, Anthropic, Google)
- **Infrastructure:** Kubernetes, Docker
- **Monitoring:** Prometheus, Grafana, ELK Stack

## 📊 Várható Mutatók

- **AI Ágensek:** 12
- **Átlagos válaszidő:** 14s
- **Cache hit rate:** 40%+
- **Költség:** $0.15-0.40/query (standard mode)

## 🚀 Quick Start Guide

### 1. Nézd Meg az Interaktív Dokumentációt

```bash
# Nyisd meg böngészőben
open docs/ai-tanacs-implementation-plan.html

# Vagy indíts egy szervert
python -m http.server 8000
# Majd: http://localhost:8000/docs/ai-tanacs-implementation-plan.html
```

### 2. Próbáld Ki a Valódi AI Backend-et

#### Backend Indítás

```bash
# Lépj be a backend mappába
cd backend

# Telepítsd a függőségeket
pip install -r requirements.txt

# Konfiguráld az API kulcsokat
cp .env.example .env
nano .env  # Add hozzá az OpenAI/Anthropic API kulcsokat

# Indítsd a szervert
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Használat (Real AI Mode)

1. Nyisd meg a `docs/ai-tanacs-implementation-plan.html` fájlt böngészőben
2. Scrollolj le a **"Live Demo"** szekcióhoz
3. Kapcsold BE a **"🤖 Valódi AI Backend"** toggle-t
4. Válassz egy kérdést a 4 demo közül
5. Kattints **"🚀 AI Indítása"**
6. Nézd ahogy 12 AI ágens valós időben dolgozik és szavaz!

#### Tesztelés API-val

```bash
# Health check
curl http://localhost:8000/api/health

# Kérdezd az AI Tanácsot
curl -X POST http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Mi a jövője a mesterséges intelligenciának?",
    "voting_method": "borda"
  }'
```

## 📂 Projekt Struktúra

```
consule/
├── docs/
│   └── ai-tanacs-implementation-plan.html   # Interaktív dokumentáció + Live Demo
├── backend/
│   ├── main.py              # FastAPI app + WebSocket
│   ├── config.py            # Settings
│   ├── voting.py            # Szavazási algoritmusok
│   ├── api_client.py        # OpenAI/Anthropic kliens
│   ├── agents/
│   │   ├── base.py          # BaseAgent osztály
│   │   └── council.py       # 12 AI ágens implementáció
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
└── README.md                # Ez a fájl
```

## 🎯 Jelenlegi Status

✅ **Implementálva:**
- Interaktív HTML dokumentáció
- Live Demo vizualizáció (szimuláció + valódi AI)
- FastAPI backend (REST + WebSocket)
- 12 AI ágens egyedi személyiségekkel
- OpenAI & Anthropic integráció
- 4 szavazási mechanizmus (Borda, IRV, MRR, Hybrid)
- Real-time WebSocket kommunikáció
- Párhuzamos agent végrehajtás

🔜 **Következő Lépések:**
1. Production deployment (Docker + Kubernetes)
2. PostgreSQL + Redis cache
3. User memória (Vector DB)
4. Rate limiting & monitoring
5. Frontend webapp (React/Next.js)

## 📖 További Információ

Az összes részlet, matematikai formulák, implementációs útmutatók és best practice-ek megtalálhatók a **[interaktív dokumentációban](docs/ai-tanacs-implementation-plan.html)**.

---

**Verzió:** 1.0 MVP
**Dátum:** 2025. November
**Status:** ✅ Functional Prototype - Backend + Frontend Working!
