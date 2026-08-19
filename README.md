# Arsène Godonou — AI/ML Portfolio

A full-stack portfolio with an interactive AI assistant: ask it questions
about my background, and it answers using a real RAG (Retrieval-Augmented
Generation) pipeline grounded in my actual CV and project write-ups —
never invented.

**Live site:** [asene-portfolio.vercel.app](https://asene-portfolio.vercel.app/)
**API:** [arsene-portfolio-api.onrender.com](https://arsene-portfolio-api.onrender.com/docs)

---

## What this project demonstrates

This isn't just a portfolio *about* AI/ML engineering — it's built as a
real, working example of one:

- A **RAG pipeline** from scratch: document chunking, embeddings, vector
  search (Qdrant), and an LLM that's explicitly instructed to refuse
  answering rather than hallucinate when it doesn't have the information.
- A **streaming chat API** (Server-Sent Events) with per-session
  conversation memory and rate limiting.
- A **FastAPI backend** with a clean layered architecture (routes →
  services → models), fully tested (36+ tests).
- A **Next.js frontend** with server-side data fetching, an EN/FR language
  switcher, dark/light theming, and scroll-triggered animations.
- Deployed on **free-tier infrastructure end to end** (Vercel, Render,
  Qdrant Cloud, Cohere, OpenRouter) — including working around real
  constraints like a 512MB memory limit.

## Architecture

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────┐
│  Frontend         │      │  Backend           │      │  Qdrant       │
│  Next.js / Vercel │─────▶│  FastAPI / Render  │─────▶│  (vectors)    │
└─────────────────┘      └──────────────────┘      └─────────────┘
                                    │
                                    ▼
                          ┌──────────────────┐
                          │  Cohere (embeddings)│
                          │  OpenRouter (LLM)    │
                          └──────────────────┘
```

## Repository structure

```
.
├── backend/          # FastAPI app, RAG pipeline, tests — see backend/README.md
└── frontend/         # Next.js app, chat widget, i18n — see frontend/README.md
```

Each folder has its own README with setup instructions, environment
variables, and implementation notes specific to that part of the stack.

## Tech stack

**Frontend:** Next.js 14 (App Router), TypeScript, TailwindCSS, Framer Motion, Lucide Icons

**Backend:** FastAPI, SQLAlchemy, Qdrant, Cohere (embeddings), OpenRouter (LLM)

**Infra:** Vercel (frontend), Render (backend), Qdrant Cloud, all on free tiers

## Getting started locally

```bash
git clone https://github.com/Arsene666/Portfolio.git
cd Portfolio

# Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then fill in your own API keys
python scripts/seed_projects.py
uvicorn app.main:app --reload

# Frontend (in a separate terminal)
cd ../frontend
npm install
cp .env.local.example .env.local
npm run dev
```

Full details, including how to set up Qdrant Cloud, Cohere, and
OpenRouter, are in [`backend/README.md`](backend/README.md) and
[`frontend/README.md`](frontend/README.md).

## Contact

- **LinkedIn:** [linkedin.com/in/arsène-godonou](https://www.linkedin.com/in/ars%C3%A8ne-godonou)
- **Email:** godonouarsene18@gmail.com
- **GitHub:** [@Arsene666](https://github.com/Arsene666)

Currently looking for a one-year apprenticeship (1 month / 1 month
rhythm) in ML/AI engineering or backend Python development.