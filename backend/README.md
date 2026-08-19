# Portfolio backend

FastAPI skeleton + Project data model/endpoints + full RAG pipeline
(chunking, embeddings, Qdrant, LLM via OpenRouter) behind `/api/v1/chat`.

## Structure

```
app/
├── main.py              # App entry point, CORS, router mounting, table creation
├── core/
│   ├── config.py        # Settings (env vars via pydantic-settings)
│   └── logging.py       # Console logging setup
├── api/
│   ├── router.py        # Aggregates all route modules under /api/v1
│   └── routes/
│       ├── health.py    # GET /api/v1/health
│       ├── projects.py  # GET /api/v1/projects, GET /api/v1/projects/{slug}
│       └── chat.py      # POST /api/v1/chat
├── schemas/
│   ├── health.py
│   ├── project.py
│   ├── rag.py            # DocumentChunk model
│   └── chat.py            # ChatRequest / ChatResponse
├── models/
│   └── project.py         # SQLAlchemy Project model
├── db/
│   ├── base.py            # Declarative base
│   └── session.py         # Engine + get_db dependency
└── services/
    └── rag/
        ├── chunking.py      # Splits data/raw/*.md into section-based chunks
        ├── embeddings.py    # Local multilingual embedding model wrapper
        ├── qdrant_store.py  # Qdrant connection, collection, upsert, search
        ├── llm_client.py    # OpenRouter chat completions wrapper
        └── chat_service.py  # Orchestration + the anti-hallucination guardrail
data/
└── raw/                   # Your real CV, bio, and project write-ups (.md)
scripts/
├── seed_projects.py       # Populates the DB with Arsène's real projects
└── ingest_documents.py    # Chunks + embeds + uploads data/raw/*.md into Qdrant
tests/
├── test_health.py
├── test_projects.py       # Isolated in-memory SQLite DB
├── test_rag_chunking.py   # Runs against the real files in data/raw
├── test_chat_service.py   # RAG orchestration logic, Qdrant/LLM mocked
└── test_chat_endpoint.py  # HTTP-level test of POST /api/v1/chat
```

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python scripts/seed_projects.py
uvicorn app.main:app --reload
```

Then visit:
- `http://localhost:8000/api/v1/health`
- `http://localhost:8000/api/v1/projects`
- `http://localhost:8000/docs` — try `/api/v1/chat` directly from here
- `POST http://localhost:8000/api/v1/chat` with `{"session_id": "x", "message": "..."}`

## Run tests

```bash
pytest -v
ruff check .
```

20 tests, including full orchestration-logic coverage of the chat service
with Qdrant and the LLM mocked out — the retrieval threshold, source
deduplication, and both failure modes (retrieval down, LLM down) are all
covered without needing live credentials.

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

## Set up OpenRouter (for the LLM)

1. Sign up at [openrouter.ai](https://openrouter.ai) (no credit card needed for free models).
2. **Keys → Create Key**, copy it.
3. Add to `.env`:
   ```
   OPENROUTER_API_KEY=your-key-here
   ```

The default model is `meta-llama/llama-3.3-70b-instruct:free`. OpenRouter's
free-tier lineup changes fairly often — if this model ever gets delisted,
check [openrouter.ai/models](https://openrouter.ai/models) for a current
`:free` model and update `LLM_MODEL_NAME` in `.env`. No code change needed.

## Ingest your documents into Qdrant

Once Qdrant is configured:

```bash
python scripts/ingest_documents.py
```

Chunks `data/raw/*.md`, embeds locally (downloads the embedding model on
first run, ~130MB, no API key needed for this part), and uploads to
Qdrant. Safe to re-run after editing your documents — it fully refreshes
the collection each time.

## What was verified vs. what needs your credentials

**Verified end-to-end in this environment:**
- Document chunking against your real CV/project files (11 chunks, correct
  sections) — `test_rag_chunking.py`.
- The full chat orchestration logic — retrieval, the similarity threshold
  that prevents hallucination, source deduplication, and graceful handling
  of both a retrieval failure and an LLM failure — all with Qdrant/OpenRouter
  mocked, so this logic is genuinely tested, not just written.
  `test_chat_service.py`, `test_chat_endpoint.py`.
- The live `/api/v1/chat` endpoint was called for real with no Qdrant/LLM
  configured yet, and correctly returned a clean 200 with a "not ready"
  message instead of crashing — proving the error handling actually works,
  not just the happy path.

**Needs your real credentials to verify (can't be done in this sandbox,
which has no network access to Hugging Face, Qdrant, or OpenRouter):**
- Running `scripts/ingest_documents.py` against your real Qdrant cluster.
- A real `/api/v1/chat` call that actually retrieves your chunks and gets
  an answer back from Llama 3.3 via OpenRouter.

## Deploy (Render / Railway)

Both platforms can build directly from the `Dockerfile`. Set these env vars
in the platform dashboard: `ALLOWED_ORIGINS`, `DATABASE_URL`, `QDRANT_URL`,
`QDRANT_API_KEY`, `QDRANT_COLLECTION_NAME`, `OPENROUTER_API_KEY`,
`LLM_MODEL_NAME`.

## What's next 

- Add the chat widget to the frontend (floating button, streaming
  responses, suggested questions, sources shown under each answer).
- Rate-limit `/api/v1/chat` so it can't burn through free-tier quota.
