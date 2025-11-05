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

## 🎯 Következő Lépések

1. **Stakeholder Alignment** - Csapat bemutató, budget approval
2. **Prototípus Döntés** - MVP scope finalizálás
3. **API Account Setup** - OpenAI, Anthropic, Google credentials
4. **Infrastructure** - Cloud provider, Docker, PostgreSQL setup

## 📖 További Információ

Az összes részlet, matematikai formulák, implementációs útmutatók és best practice-ek megtalálhatók a **[interaktív dokumentációban](docs/ai-tanacs-implementation-plan.html)**.

---

**Verzió:** 1.0
**Dátum:** 2025. November
**Status:** Planning & Design Phase
