# 🎯 AI Resume ATS Scorer & Screening Agent

> **Selection Round Submission — Junior AI Research Associate**
> 
> **One-Sentence Agent Job Statement:**  
> *"My agent takes a candidate's resume (PDF/DOCX/DOC) and an optional job description, performs NLP entity extraction and Sentence-BERT semantic similarity matching, and produces a comprehensive ATS score breakdown, actionable suggestions, and context-aware chat coaching."*

---

## 📋 Table of Contents
1. [Agent Architecture & Capabilities](#-agent-architecture--capabilities)
2. [Step-by-Step System Design](#-step-by-step-system-design)
   - [Step 1: One Job & Expected Capabilities](#step-1-one-job--expected-capabilities)
   - [Step 2: Model & API Setup](#step-2-model--api-setup)
   - [Step 3: System Prompts](#step-3-system-prompts)
   - [Step 4: Data & Tools (RAG & Parsing)](#step-4-data--tools-rag--parsing)
   - [Step 5: Agent Loop Architecture](#step-5-agent-loop-architecture)
   - [Step 6: Installation & Execution Guide](#step-6-installation--execution-guide)
3. [Sample Inputs & Outputs](#-sample-inputs--outputs)
4. [Design Tradeoffs & Engineering Decisions](#-design-tradeoffs--engineering-decisions)
5. [Evaluation Rubric Alignment](#-evaluation-rubric-alignment)

---

## 🏗️ Agent Architecture & Capabilities

The **AI Resume ATS Screening Agent** is an end-to-end intelligence system that screens candidates, parses unstructured documents, measures semantic fit against job requirements, and provides an interactive coaching loop.

```
                  ┌─────────────────────────────────────────┐
                  │            User Input                   │
                  │ (Upload Resume / Paste JD / Query Chat) │
                  └────────────────────┬────────────────────┘
                                       │
                                       ▼
                  ┌─────────────────────────────────────────┐
                  │          Parsing & NLP Extraction       │
                  │   (pdfplumber / python-docx / spaCy)    │
                  └────────────────────┬────────────────────┘
                                       │
                                       ▼
                  ┌─────────────────────────────────────────┐
                  │       Semantic Vector Embedding         │
                  │ (Sentence Transformers: all-MiniLM-L6)  │
                  └────────────────────┬────────────────────┘
                                       │
                                       ▼
                  ┌─────────────────────────────────────────┐
                  │         Scoring & Feedback Engine       │
                  │  (ATS Weights + Cosine Similarity Match)│
                  └────────────────────┬────────────────────┘
                                       │
                                       ▼
                  ┌─────────────────────────────────────────┐
                  │           LLM Agent & RAG Loop          │
                  │   (Groq Llama-3.3-70b + Supabase Context)│
                  └────────────────────┬────────────────────┘
                                       │
                                       ▼
                  ┌─────────────────────────────────────────┐
                  │               Outputs                   │
                  │ (Web Dashboard / CLI Agent / PDF Report)│
                  └─────────────────────────────────────────┘
```

---

## 🛠️ Step-by-Step System Design

### Step 1: One Job & Expected Capabilities
- **Core Job**: Automated ATS resume screening, scoring, and candidate optimization.
- **Capabilities**:
  1. **Document Parsing**: Extracts text from `.pdf`, `.docx`, and `.doc` files.
  2. **Entity & Skill Extraction**: Uses spaCy (`en_core_web_md`) to extract technical skills, experience metrics, education, and action verbs.
  3. **Semantic Similarity Matching**: Uses Sentence Transformers (`all-MiniLM-L6-v2`) to compute high-dimensional vector embeddings and cosine similarity against job descriptions.
  4. **Multi-Category ATS Scoring**: Evaluates candidates across 5 key dimensions:
     - **Formatting** (20%)
     - **Keyword Matching** (25%)
     - **Content Quality** (25%)
     - **Skill Validation** (15%)
     - **ATS Compatibility** (15%)
  5. **Interactive Coaching Agent Loop**: Provides continuous Input → Think → Act → Output loops via both a Streamlit Web UI and a CLI script.
  6. **Report Generation & Persistence**: Generates downloadable PDF reports (WeasyPrint) and saves session histories to Supabase.

---

### Step 2: Model & API Setup
The agent combines deterministic local NLP with cloud-hosted LLM reasoning:
- **LLM Engine**: Groq API (`llama-3.3-70b-versatile` / `llama-3-8b-8192`) via official `groq` SDK for fast, low-latency suggestions and parsing.
- **Primary NLP Model**: spaCy `en_core_web_md` for named entity recognition (NER) and token matching.
- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2` (768-dimensional embeddings) for dense semantic vector matching.

---

### Step 3: System Prompts
The agent utilizes structured system prompts to ensure deterministic JSON outputs for parsing and persona-consistent responses for coaching.

#### 1. Resume Parsing System Prompt
```text
You are a resume parser. Extract information from the resume and return ONLY a valid JSON object. No explanation, no markdown.
```

#### 2. AI Coach Persona Prompt
```text
You are an expert ATS Resume Coach. Help the user optimize their resume, giving highly professional, detailed, and actionable advice. Use lists and bullet points.
```

---

### Step 4: Data & Tools (RAG & Parsing)
- **Document Extractors**: `pdfplumber`, `PyPDF2`, `python-docx`.
- **Validation Tools**: Custom regex checkers for quantifiable metrics (e.g. percentages, metrics), action verbs, and contact headers.
- **Database & Storage**: Supabase PostgREST API and Auth for persisting past candidate screenings (`public.analyses`).

---

### Step 5: Agent Loop Architecture
The system supports two execution loops implementing the **Input → Think → Act → Output** cycle:

1. **Streamlit Web UI (`frontend/views/coach.py`)**:
   - *Input*: User queries via `st.chat_input()`.
   - *Think*: Reads candidate's past analysis history from Supabase for context.
   - *Act*: Posts prompt + context payload to FastAPI backend (`/api/v1/coach/chat`), invoking Groq.
   - *Output*: Renders response in interactive chat bubbles using `st.chat_message()`.

2. **Terminal CLI Agent (`cli_agent.py`)**:
   - *Input*: Terminal prompt `> What's your question?`.
   - *Think*: Queries Supabase history for candidate metrics.
   - *Act*: Invokes Groq API.
   - *Output*: Prints formatted advice directly to the console.

---

### Step 6: Installation & Execution Guide

#### 1. Prerequisites
- Python 3.10+
- Git

#### 2. Clone & Setup Virtual Environment
```powershell
git clone <your-repo-url>
cd ai-resume-ats-main
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### 3. Install Dependencies & NLP Models
```powershell
pip install -r requirements.txt
python -m spacy download en_core_web_md
pip install python-magic-bin
```

#### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```env
SUPABASE_URL="https://aiqxaizswjifbfikzmon.supabase.co"
SUPABASE_KEY="your-supabase-service-role-key"
SUPABASE_ANON_KEY="your-supabase-anon-key"
SUPABASE_JWT_SECRET="your-supabase-jwt-secret"
GROQ_API_KEY="gsk_your_groq_api_key"
PORT=8000
HOST=0.0.0.0
```

#### 5. Database Table Setup (Supabase)
Run the following query in your Supabase SQL Editor to create the required table:
```sql
create table public.analyses (
  id bigint generated by default as identity primary key,
  user_id uuid not null,
  filename text not null,
  ats_score numeric,
  keyword_match numeric,
  missing_keywords jsonb default '[]'::jsonb,
  analysis_result jsonb not null,
  created_at timestamptz default now()
);

alter table public.analyses enable row level security;
```

#### 6. Run the Application

##### Option A: Web Application (FastAPI + Streamlit)
1. **Start Backend Server**:
   ```powershell
   .\venv\Scripts\uvicorn.exe backend.main:app --host 0.0.0.0 --port 8000
   ```
2. **Start Frontend Client** (in a new terminal):
   ```powershell
   .\venv\Scripts\streamlit.exe run frontend\streamlit_app.py
   ```
   *Access the web app at `http://localhost:8501`.*

##### Option B: Interactive CLI Agent Loop
```powershell
.\venv\Scripts\python.exe cli_agent.py
```

---

## 📊 Sample Inputs & Outputs

### Sample API Health Check Output
```json
{
  "status": "healthy",
  "nlp_loaded": true,
  "embedder_loaded": true
}
```

### Sample Screening Result Response (`POST /api/v1/analyze-resume`)
```json
{
  "ATS_score": 85.0,
  "component_scores": {
    "formatting_score": 18.0,
    "keyword_score": 22.5,
    "content_score": 21.0,
    "skill_validation_score": 12.0,
    "ats_compatibility_score": 11.5
  },
  "issues_summary": [
    "Most Skills Lack Supporting Evidence",
    "Missing Professional Summary"
  ],
  "jd_match_analysis": {
    "match_percentage": 82.5,
    "semantic_similarity": 0.842,
    "matched_keywords": ["Python", "FastAPI", "React", "Docker"],
    "missing_keywords": ["Kubernetes", "CI/CD", "GraphQL"],
    "skills_gap": ["Kubernetes", "GraphQL"]
  }
}
```

### Sample CLI Agent Output
```text
=============================================
      ATS RESUME AI COACH ACTIVE
=============================================
Ask me questions about optimizing your CV, ATS scoring,
formatting tips, or matching job descriptions.
Type 'exit' or 'quit' to end the session.

> What's your question?
> How can I improve my missing skills for a DevOps role?

Thinking...

------------------ ANSWER ------------------
1. Add a Dedicated Projects Section:
   - Build a project using Kubernetes and Terraform.
   - Document your CI/CD pipeline in your GitHub repository.
2. Quantify Achievements:
   - Instead of 'Worked with Docker', write 'Containerized 5 microservices using Docker, reducing deployment time by 40%'.
--------------------------------------------
```

---

## ⚖️ Design Tradeoffs & Engineering Decisions

1. **Hybrid Architecture (spaCy + Sentence Transformers + LLM)**:
   - *Tradeoff*: Rather than passing raw text directly to an expensive LLM for full scoring, we use spaCy for deterministic parsing and Sentence Transformers for embedding similarity.
   - *Reasoning*: Reduces LLM API costs, eliminates score hallucinations, guarantees reproducible metrics, and speeds up analysis.

2. **Model Choice (`all-MiniLM-L6-v2` vs `all-mpnet-base-v2`)**:
   - *Tradeoff*: `all-MiniLM-L6-v2` is 5x smaller (~80 MB) and significantly faster than `all-mpnet-base-v2` (~438 MB).
   - *Reasoning*: As evaluated in `jupyter notebooks/02_BERT_EMBEDDINGS.ipynb`, `MiniLM` provides comparable cosine similarity accuracy while enabling fast cold-starts on local developer hardware.

3. **Database Selection (Supabase / PostgREST)**:
   - *Tradeoff*: Used Supabase REST endpoints instead of traditional ORMs (e.g. SQLAlchemy).
   - *Reasoning*: Keeps backend stateless, leverages Supabase Row Level Security (RLS), and allows seamless JWT verification across Streamlit and FastAPI.

4. **Graceful Degradation for Windows GTK Dependencies**:
   - *Tradeoff*: WeasyPrint requires GTK+ C-libraries for PDF rendering.
   - *Reasoning*: Handled import exceptions to allow core scoring and AI coaching to run without crashing when GTK+ is missing, while providing automated `winget` installation scripts.

---

## 🎯 Evaluation Rubric Alignment

| Rubric Criteria | Weight | Implementation Highlights |
| :--- | :---: | :--- |
| **Working end-to-end resume screening agent** | **30** | Full pipeline: Document parsing, skill extraction, semantic matching, ATS score calculation, report generation, and interactive web/CLI agent loops. |
| **Approach, NLP similarity method, and model choice** | **25** | Dense vector embeddings via Sentence Transformers, cosine similarity matching, spaCy NER tokenization, and Groq `llama-3.3-70b` LLM suggestions. |
| **Code quality and organization** | **20** | Clean directory structure separating FastAPI backend services, Streamlit frontend views, Pydantic schemas, and research notebooks. |
| **README clarity and reproducibility** | **15** | Clear installation instructions, environment setup, database queries, and step-by-step verification commands. |
| **Tradeoff notes and reasoning** | **10** | Detailed engineering breakdown explaining hybrid scoring, model selection benchmarks, and stateless API design. |
#   A u t o m a t e d - A T S - r e s u m e  
 