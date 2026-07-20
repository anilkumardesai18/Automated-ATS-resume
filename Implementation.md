# Implementation Plan - Selection Round Alignment

This plan documents the completion of the project alignment with the **Junior AI Research Associate Selection Round** guidelines and scoring rubric.

---

## 1. Objectives Completed

- **One-Sentence Agent Job Statement**: Added clear definition to `README.md` and project artifacts.
- **6-Step Guide Alignment**:
  - **Step 1**: Scope & Capabilities definition.
  - **Step 2**: Groq, spaCy, and Sentence Transformers setup documentation.
  - **Step 3**: System Prompts (Parsing & AI Coach).
  - **Step 4**: Data Parsing & RAG Integration (pdfplumber, docx, Supabase).
  - **Step 5**: Input → Think → Act → Output Loops (Web Chat UI + Terminal CLI Agent).
  - **Step 6**: Foolproof Setup & Reproducibility Guide.
- **Design Tradeoffs & Honest Engineering**: Documented rationale for hybrid scoring vs pure LLM generation, model benchmarking choices, and serverless persistence.
- **Rubric Scoring Alignment**: Structured all documentation to maximize the 100-point universal evaluation rubric.

---

## 2. Project Architecture Summary

```
ATS_SCORER/
├── backend/                  FastAPI App, NLP Services, API Routes
│   ├── api/                  Auth verification & Route handlers (/analyze-resume, /coach/chat, /history)
│   ├── core/                 Config & Environment loaders
│   ├── database/             Supabase Client & database handlers
│   ├── models/               Pydantic schemas
│   └── services/             spaCy NLP, Sentence-BERT matcher, Groq LLM parser, WeasyPrint PDF exporter
├── frontend/                 Streamlit Web Client
│   ├── components/           Dashboard visualizers & metric scorecards
│   ├── services/             API Client & Supabase auth handlers
│   └── views/                Landing, Scorer, History, Resources, and Coach Chat UI
├── cli_agent.py              Interactive CLI Agent Loop (Terminal)
├── generate_mock_dataset.py  Dataset builder script
├── dataset/                  Generated training/testing datasets
├── jupyter notebooks/        Research & model evaluation notebooks
└── README.md                 Selection Round Submission Documentation
```

---

## 3. Universal Rubric Alignment

- **Working end-to-end resume screening agent (30 pts)**: Verified end-to-end parsing, vector similarity scoring, suggestion generation, and interactive loops.
- **Approach, NLP similarity method, and model choice (25 pts)**: Dense embeddings via `sentence-transformers/all-MiniLM-L6-v2`, spaCy NER tokenization, and Groq `llama-3.3-70b` LLM.
- **Code quality and organization (20 pts)**: Clean directory structure separating FastAPI backend services, Streamlit frontend views, Pydantic schemas, and research notebooks.
- **README clarity and reproducibility (15 pts)**: Complete step-by-step setup guide with virtual environment setup, model downloads, and database schema queries.
- **Tradeoff notes and reasoning (10 pts)**: Documented engineering choices detailing hybrid scoring vs pure LLM inference, embedding model sizes, and stateless API design.
