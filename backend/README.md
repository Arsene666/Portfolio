# Portfolio backend

FastAPI + full RAG pipeline (chunking, Cohere embeddings, Qdrant, LLM via
OpenRouter) behind `/api/v1/chat` and `/api/v1/chat/stream`.

## Structure

```
app/
├── main.py              # App entry point, CORS, router mounting, auto-seeding on boot
├── core/
│   ├── config.py        # Settings (env vars via pydantic-settings)
│   └── logging.py       # Console logging setup
├── api/
│   ├── router.py        # Aggregates all route modules under /api/v1
│   └── routes/
│       ├── health.py    # GET /api/v1/health
│       ├── projects.py  # GET /api/v1/projects, GET /api/v1/projects/{slug}
│       └── chat.py      # POST /api/v1/chat, POST /api/v1/chat/stream
├── schemas/
│   ├── health.py
│   ├── project.py
│   ├── rag.py            # DocumentChunk model
│   └── chat.py            # ChatRequest / ChatResponse
├── models/
│   └── project.py         # SQLAlchemy Project model
├── db/
│   ├── base.py             # Declarative base
│   ├── session.py          # Engine + get_db dependency
│   └── seed.py              # Project data + idempotent seed(), called on every app boot
└── services/
    └── rag/
        ├── chunking.py      # Splits data/raw/*.md into section-based chunks
        ├── embeddings.py    # Cohere Embed API client (hosted — see note below)
        ├── qdrant_store.py  # Qdrant connection, collection, upsert, search
        ├── llm_client.py    # OpenRouter chat completions wrapper (streaming + non-streaming)
        ├── memory.py        # Per-session conversation history + question counter
        └── chat_service.py  # Orchestration + the anti-hallucination guardrail
data/
└── raw/                   # Real CV, bio, and project write-ups (.md)
scripts/
├── seed_projects.py           # CLI wrapper around app/db/seed.py, for manual re-seeding
├── ingest_documents.py        # Chunks + embeds (via Cohere) + uploads data/raw/*.md into Qdrant
├── diagnose_qdrant.py         # Connection/auth troubleshooting
├── diagnose_qdrant_detailed.py
└── diagnose_similarity.py     # Shows real similarity scores for a test question
tests/
├── test_health.py
├── test_projects.py       # Isolated in-memory SQLite DB
├── test_rag_chunking.py   # Runs against the real files in data/raw
├── test_chat_service.py   # RAG orchestration logic, Qdrant/LLM mocked
├── test_chat_stream.py    # Streaming orchestration, same guardrails
├── test_chat_endpoint.py  # HTTP-level tests of both /chat and /chat/stream
└── test_memory.py         # Conversation history + question counter
```

## Why Cohere for embeddings, not a local model

This project originally used a local embedding model
(`sentence-transformers`, then the lighter `fastembed`). Both were
abandoned after real production failures: Render's free tier caps memory
at **512MB**, and even `fastembed`'s ~220MB model, added on top of the
rest of the app, was enough to trigger repeated out-of-memory restarts
under real traffic (confirmed via Render's own crash emails and a
before/after memory measurement: ~750MB for `sentence-transformers` vs.
~120MB total with zero local embedding library).

Calling Cohere's hosted Embed API instead removes the model from the
process entirely — the trade-off is a network round-trip per request
instead of a local computation, which is a good trade for a low-traffic
portfolio chat. If you deploy somewhere with more memory headroom, you
could switch back to a local model by reimplementing `embeddings.py`.

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in QDRANT_URL, QDRANT_API_KEY, COHERE_API_KEY, OPENROUTER_API_KEY
python scripts/seed_projects.py
uvicorn app.main:app --reload
```

Then visit:
- `http://localhost:8000/api/v1/health`
- `http://localhost:8000/api/v1/projects`
- `http://localhost:8000/docs` — try `/api/v1/chat` directly from here
- `POST http://localhost:8000/api/v1/chat` with `{"session_id": "x", "message": "..."}`
- `POST http://localhost:8000/api/v1/chat/stream` — same, but streams the answer as Server-Sent Events

Note: the database re-seeds itself automatically on every app startup
(`app/db/seed.py`, called from `main.py`) — this isn't optional, it's what
keeps `/api/v1/projects` populated on hosts like Render where the local
SQLite file doesn't survive a redeploy or restart. `scripts/seed_projects.py`
still exists for manual re-seeding after editing the project data.

## Run tests

```bash
pytest -v
ruff check .
```

36 tests, covering: project CRUD, document chunking against the real CV
files, the full chat orchestration logic (both streaming and non-streaming)
with Qdrant/LLM mocked — including the anti-hallucination threshold, source
deduplication, the per-session question limit, and graceful handling of
retrieval/LLM failures — and the conversation memory module itself.

## Set up Qdrant Cloud

1. Sign up at [cloud.qdrant.io](https://cloud.qdrant.io) (no credit card needed).
2. **Clusters → Create a Free Cluster**, pick a nearby region.
3. Copy the **API key** (API Keys tab) and the **cluster URL**.
4. Add both to `.env`:
   ```
   QDRANT_URL=https://xxxxx.cloud.qdrant.io
   QDRANT_API_KEY=your-key-here
   ```

⚠️ Free clusters suspend after 1 week of inactivity, delete after 4 weeks.

## Set up Cohere (for embeddings)

1. Sign up at [dashboard.cohere.com](https://dashboard.cohere.com) (no credit card needed).
2. **API Keys** in the sidebar → copy your Trial key.
3. Add to `.env`:
   ```
   COHERE_API_KEY=your-key-here
   ```

The default model is `embed-multilingual-light-v3.0` (384 dimensions,
handles French and English). Free trial keys give 1,000 API calls/month —
each chat question costs one call (document embeddings are computed once,
during ingestion, not per chat request).

## Set up OpenRouter (for the LLM)

1. Sign up at [openrouter.ai](https://openrouter.ai) (no credit card needed for free models).
2. **Keys → Create Key**, copy it.
3. Add to `.env`:
   ```
   OPENROUTER_API_KEY=your-key-here
   ```
4. Go to **Settings → Privacy** on OpenRouter and enable *"Enable free
   endpoints that may train on inputs"* and *"...may publish prompts"* —
   without these, every `:free` model request returns 404, even with a
   valid key.

The default model is a specific pinned free model, not OpenRouter's
`openrouter/free` auto-router — the auto-router was tried first, but it
occasionally routes to a model that leaks moderation metadata
(`User Safety: safe`) directly into its response text. A pinned model
avoids that. OpenRouter's free-tier lineup still changes often; if the
configured model gets delisted, check
[openrouter.ai/models](https://openrouter.ai/models) for a current
`:free` model and update `LLM_MODEL_NAME` in `.env` — no code change
needed.

## Ingest your documents into Qdrant

Once Qdrant and Cohere are both configured:

```bash
python scripts/ingest_documents.py
```

Chunks `data/raw/*.md`, embeds each chunk via the Cohere API, and uploads
to Qdrant. Safe to re-run after editing your documents — it fully
refreshes the collection each time.

**After changing the embedding model or provider, always re-run this
script.** Different embedding models produce incompatible vector spaces
even at the same dimensionality — old vectors won't match new queries.

## Calibrating `RAG_SIMILARITY_THRESHOLD`

This threshold is specific to whichever embedding model is configured —
it is **not portable** across models. Use `scripts/diagnose_similarity.py`
to see real scores before picking a value:

```bash
python scripts/diagnose_similarity.py "Why should I hire Arsène?"
```

Compare the top score for a genuinely relevant question against an
obviously unrelated one (e.g. "What is the capital of France?") to find
the gap, then set the threshold safely between the two. Current value
(`0.22`) was calibrated this way for `embed-multilingual-light-v3.0`.

## Session limits

- `MAX_QUESTIONS_PER_SESSION` (default `10`) caps how many questions a
  single browser session can ask, checked *before* any embedding/search/LLM
  call — protects the free API quotas (OpenRouter's free tier is roughly
  50 requests/day without purchased credits) from being exhausted by one
  visitor.
- Conversation history sent to the LLM is separately capped at the last 5
  exchanges (`MAX_TURNS` in `memory.py`) to keep prompts small — this is
  independent from the question-count limit above.

## Deploy (Render)

Builds directly from the `Dockerfile`. Set these env vars in the Render
dashboard: `ALLOWED_ORIGINS` (your real Vercel URL, not localhost),
`DATABASE_URL`, `QDRANT_URL`, `QDRANT_API_KEY`, `QDRANT_COLLECTION_NAME`,
`COHERE_API_KEY`, `OPENROUTER_API_KEY`, `LLM_MODEL_NAME`,
`RAG_SIMILARITY_THRESHOLD`, `MAX_QUESTIONS_PER_SESSION`.

⚠️ Render's free tier has a **512MB memory limit** and spins the service
down after 15 minutes of inactivity (expect a ~30-60s cold start on the
first request after a period of inactivity). This is why embeddings run
through Cohere's API rather than a local model — see the note above.

## What's next

- A real backend endpoint for the contact form (currently `mailto:` only
  on the frontend — see `frontend/README.md`).
- An interactive ML demo (e.g. the object detection project) exposed
  through its own endpoint.