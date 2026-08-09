"""Seed the database with Arsène Godonou's real projects.

Usage:
    python scripts/seed_projects.py
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from sqlalchemy import select  # noqa: E402

from app.db.base import Base  # noqa: E402
from app.db.session import SessionLocal, engine  # noqa: E402
from app.models.project import Project  # noqa: E402

SAMPLE_PROJECTS = [
    {
        "slug": "credit-card-fraud-detection",
        "title": "Credit card fraud detection",
        "short_description": (
            "A complete data science project (CRISP-DM) detecting fraud in a "
            "highly imbalanced real-world transaction dataset."
        ),
        "problem_statement": (
            "Detect fraudulent transactions in a dataset of 284,807 real "
            "transactions where only 0.17% are fraud — a case where accuracy "
            "is meaningless and the real challenge is choosing the right "
            "metrics and decision threshold."
        ),
        "architecture_summary": (
            "Exploratory data analysis with bias detection and data leakage "
            "prevention, followed by comparison of several supervised models "
            "using metrics suited to imbalanced data (PR-AUC, F-beta). The "
            "final decision threshold was chosen through a documented "
            "precision/recall trade-off, with SHAP-based interpretability of "
            "the key variables. Best result: XGBoost, PR-AUC 0.825, Recall "
            "78%, Precision 97%."
        ),
        "tech_stack": ["Python", "Pandas", "Scikit-learn", "XGBoost", "SHAP"],
        "github_url": "https://github.com/Arsene666/credit-card-fraude-detection",
        "demo_url": None,
        "demo_slug": None,
        "images": ["/projects/fraude_detection.jpg"],
        "is_featured": True,
    },
    {
        "slug": "rag-assistant",
        "title": "Document RAG assistant",
        "short_description": (
            "An end-to-end RAG pipeline with multi-turn conversational memory "
            "and live web search fallback."
        ),
        "problem_statement": (
            "Let a user ask natural-language questions across multi-format "
            "documents and get grounded answers, with the ability to fall "
            "back to live web search when the answer isn't in the documents."
        ),
        "architecture_summary": (
            "Multi-format document ingestion, adaptive semantic chunking, "
            "multilingual embeddings via Cohere, and vector storage in "
            "Qdrant. Retrieval uses cosine similarity search; conversational "
            "memory is simulated by re-injecting prior turns into the LLM "
            "context. SerpApi extends the agent with real-time web search "
            "for out-of-scope questions, served through a streaming "
            "Streamlit interface."
        ),
        "tech_stack": ["Python", "LangChain", "Cohere", "Qdrant", "Streamlit", "SerpApi"],
        "github_url": "https://github.com/Arsene666/rag-assistant",
        "demo_url": None,
        "demo_slug": None,
        "images": ["/projects/rag.jpg"],
        "is_featured": True,
    },
    {
        "slug": "object-detection-api",
        "title": "Object detection API (Faster R-CNN)",
        "short_description": "A FastAPI service exposing a Faster R-CNN model for object detection.",
        "problem_statement": (
            "Train and serve a custom object detection model through a "
            "simple REST API, without relying on a paid vision API."
        ),
        "architecture_summary": (
            "Faster R-CNN (PyTorch) trained on 1,340 annotated images across "
            "9 classes plus background, with preprocessing and normalization "
            "of heterogeneous image formats and sizes. Achieved mAP ≈ 0.64 "
            "on CPU. Served through a FastAPI endpoint accepting image "
            "uploads and returning bounding boxes and labels, containerized "
            "with Docker."
        ),
        "tech_stack": ["Python", "PyTorch", "FastAPI", "Docker"],
        "github_url": "https://github.com/Arsene666/object-detection",
        "demo_url": None,
        "demo_slug": "object-detection",
        "images": ["/projects/iot_tomate.jpg"],
        "is_featured": True,
    },
    {
        "slug": "agro-ia-postharvest",
        "title": "AGRO-IA — post-harvest monitoring system",
        "short_description": (
            "An embedded + AI prototype estimating remaining shelf life of "
            "harvested produce."
        ),
        "problem_statement": (
            "Reduce post-harvest food loss by giving producers an early, "
            "data-driven estimate of how much longer their produce will "
            "stay good, instead of relying on guesswork."
        ),
        "architecture_summary": (
            "An embedded module (Arduino + environmental sensors) feeds "
            "readings that are fused with the output of a CNN image "
            "classification model to estimate remaining shelf life, plus a "
            "recommendation system to help preserve quality. Validated as a "
            "prototype in a simulated environment."
        ),
        "tech_stack": ["Arduino", "CNN", "Python", "IoT sensors"],
        "github_url": None,
        "demo_url": None,
        "demo_slug": None,
        "images": ["/projects/tomato_detection.jpg"],
        "is_featured": False,
    },
    {
        "slug": "rag-portfolio-assistant",
        "title": "This portfolio's RAG assistant",
        "short_description": "A retrieval-augmented chatbot that answers questions using only my own documents.",
        "problem_statement": (
            "Let recruiters interactively ask questions about my background "
            "and get accurate, sourced answers instead of skimming a static "
            "CV."
        ),
        "architecture_summary": (
            "My CV, bio, and project write-ups are chunked and embedded, "
            "then stored in Qdrant. Incoming questions are embedded, matched "
            "against the closest chunks, and passed to an LLM with a strict "
            "system prompt forbidding answers outside the retrieved context."
        ),
        "tech_stack": ["Python", "FastAPI", "Qdrant", "OpenRouter", "Next.js"],
        "github_url": None,
        "demo_url": None,
        "demo_slug": None,
        "images": ["/projects/live_rag.jpg"],
        "is_featured": True,
    },
]


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        for data in SAMPLE_PROJECTS:
            exists = db.execute(
                select(Project).where(Project.slug == data["slug"])
            ).scalar_one_or_none()

            if exists:
                print(f"Skipping '{data['slug']}' (already exists)")
                continue

            db.add(Project(**data))
            print(f"Added '{data['slug']}'")

        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()
