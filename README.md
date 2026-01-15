# 📄 DocuMind – A Production-Ready Conversational RAG System

DocuMind is an end-to-end **Retrieval-Augmented Generation (RAG)** chatbot system that allows users to upload documents (PDF, PPT, DOC) and interact conversationally with their content. The system is designed using industry-standard architecture, open-source tooling, and scalable infrastructure patterns.

This repository currently contains a **fully implemented backend** and a **scaffolded frontend**, aligned with production-grade system design practices.

---

## 🚀 Project Objective

Build a conversational RAG chatbot that:

- Accepts readable documents (PDF, PPT, DOC)
- Parses and indexes them into a vector database
- Enables grounded, conversational querying
- Maintains session awareness and chat persistence
- Supports offline evaluation of RAG quality
- Is deployable on cloud infrastructure (AWS-ready)

---

## 🧠 Finalized Tech Stack (Updated)

| Layer | Technology |
|------|------------|
| **LLM** | Groq API (LLaMA 3.1) |
| **RAG Framework** | LlamaIndex |
| **Vector Database** | Milvus |
| **Document Parsing** | MegaParser (format-specific parsers) |
| **Embeddings** | NOMIC (`nomic-embed-text-v1.5`) |
| **Model Access** | Hugging Face |
| **Session Store** | Redis |
| **Chat Persistence** | Supabase (PostgreSQL) |
| **Evaluation** | RAGAS |
| **Backend API** | FastAPI |
| **Frontend** | React JS (planned) |
| **Deployment Target** | AWS |

> ⚠️ **Note**  
> The original design referenced **Gemini API**.  
> The implementation has been **explicitly migrated to Groq API**, using OpenAI-compatible endpoints via `langchain-openai`.

---

## 🧩 System Architecture

DocuMind follows a **3-Tier Architecture**, which is standard in production systems.

### Tier 1: Presentation Tier
- React JS  
- Open-source Chat UI components  
- File upload UI  
- Streaming response display  

### Tier 2: Application Tier
- FastAPI backend  
- LlamaIndex orchestration  
- Groq LLM integration  
- Redis session management  
- Context assembly & prompt construction  

### Tier 3: Data Tier
- Supabase (PostgreSQL) – chat persistence  
- Milvus – vector embeddings  
- Redis – ephemeral session cache  

This separation ensures **independent scalability**, **clean ownership**, and **low coupling**.

---

## 🛠️ BACKEND IMPLEMENTATION (COMPLETED)

### 📂 Backend Structure

```
backend/
└── app/
├── api/ # FastAPI routes (/upload, /chat)
├── core/ # config, logging, redis
├── evaluation/ # RAGAS pipeline
├── models/ # data models
├── pipelines/ # indexing pipeline
├── services/ # RAG services
├── utils/ # helpers
└── main.py # app entry point
```


---

## ✅ STEP-BY-STEP BACKEND IMPLEMENTATION STATUS

---

### STEP 1: Document Upload & Ingestion ✅

**Objective**  
Accept user-uploaded documents and convert them into structured, machine-readable text.

**Key Capabilities**
- Multipart file upload  
- File validation and deduplication (SHA-256)  
- Background parsing  
- Structured logging  
- Non-blocking API response  

**Stack**
- FastAPI (`/upload`)  
- MegaParser (PDF/DOCX/PPTX)  
- LlamaIndex `Document`  
- Python logging  

**Status**
- ✔ Completed  
- ✔ Observable  
- ✔ Non-blocking  
- ✔ Production-aligned  

---

### STEP 2: Chunking & Metadata Enrichment ✅

**Objective**  
Split documents into retrievable chunks with preserved context.

**Highlights**
- Sentence-aware chunking  
- Configurable chunk size & overlap  
- Metadata enrichment:
  - `document_id`
  - `chunk index`
  - `timestamp`
  - placeholders for page/section  

**Stack**
- LlamaIndex `NodeParser`  
- Custom chunking logic  

**Status**
- ✔ Completed  
- ✔ Retrieval-ready  
- ✔ Backend-internal only  

---

### STEP 3: Embedding Generation ✅

**Objective**  
Convert text chunks into dense semantic vectors.

**Details**
- NOMIC embeddings (768-dim)  
- Hugging Face model loading  
- Cached after first run  
- Embedded via LlamaIndex interface  

**Stack**
- `nomic-ai/nomic-embed-text-v1.5`  
- Hugging Face Hub  
- LlamaIndex embeddings  

**Status**
- ✔ Completed  
- ✔ Verified  
- ✔ In-memory only (by design)  

---

### STEP 4: Vector Storage & Indexing (Milvus) ✅

**Objective**  
Persist embeddings for efficient similarity search.

**Implementation**
- Docker-based Milvus standalone  
- etcd + MinIO dependencies  
- Collection reuse (non-destructive)  
- Metadata retained per vector  

**Stack**
- Milvus (Docker Compose)  
- `pymilvus`  
- LlamaIndex `MilvusVectorStore`  

**Status**
- ✔ Completed  
- ✔ Infrastructure-stable  
- ✔ Retrieval-ready  

---

### STEP 5: User Query Handling (Chat Entry Point) ✅

**Objective**  
Handle user queries with conversational awareness.

**Flow**
1. User submits query  
2. Session fetched from Redis  
3. Vector similarity search (Top-K)  
4. Context assembled  
5. Response streamed  

**Stack**
- FastAPI `/chat/stream`  
- Redis  
- Milvus  
- LlamaIndex Retriever  
- Groq API (streaming)  

**Status**
- ✔ Completed  
- ✔ Streaming enabled  
- ✔ End-to-end verified  

---

### STEP 6: Context Assembly (Core RAG Logic) ✅

**Objective**  
Construct grounded prompts with controlled token usage.

**Includes**
- Retrieved document chunks  
- Recent conversation turns  
- Optional summarization  
- Deterministic prompt template  

**Stack**
- LlamaIndex  
- Custom context assembler  
- Redis + Supabase memory  

**Status**
- ✔ Completed  
- ✔ Token-safe  
- ✔ Grounded  

---

### STEP 7: LLM Generation (Groq) ✅

**Objective**  
Generate grounded responses with real-time streaming.

**Implementation**
- Groq OpenAI-compatible endpoint  
- LLaMA 3.1 models  
- Token streaming via FastAPI  

**Stack**
- Groq API  
- `langchain-openai`  
- FastAPI `StreamingResponse`  

**Status**
- ✔ Completed  
- ✔ Gemini fully replaced  
- ✔ Production-grade  

---

### STEP 8: Response Storage & Chat Persistence ✅

**Objective**  
Ensure zero data loss and chat continuity.

**What’s Stored**
- User messages  
- Assistant responses  
- Session metadata  

**Stack**
- Supabase (PostgreSQL)  
- Redis (TTL-based session cache)  

**Status**
- ✔ Completed  
- ✔ Durable  
- ✔ Replay-ready  

---

### STEP 9: Evaluation & Quality Measurement (Offline) ✅

**Objective**  
Quantitatively evaluate RAG correctness and grounding.

**Metrics**
- Faithfulness  
- Context Precision  
- Context Recall  

**Implementation**
- Automatic QA generation  
- RAGAS evaluation  
- CSV output artifacts  

**Stack**
- RAGAS  
- Groq LLM (judge)  
- Hugging Face embeddings  

**Status**
- ✔ Completed  
- ✔ Metrics validated  
- ✔ No runtime errors  

---

## 🧪 Backend Verification Summary

- All backend steps **STEP 1 → STEP 9** are complete  
- Milvus, Redis, Supabase fully integrated  
- Groq API migration successful  
- Evaluation pipeline producing valid metrics  
- Architecture clean and industry-aligned  

---

## 🖥️ FRONTEND (PLANNED / PARTIALLY SCAFFOLDED)

The frontend directory exists and contains a **React + Vite** setup.  
No production UI is finalized yet.

**Planned responsibilities**
- Document upload UI  
- Chat interface with sidebar sessions  
- Streaming response rendering  
- API integration only (no business logic)  

Frontend implementation will begin **after backend hardening is finalized**.

---

## 🛑 BACKEND IMPLEMENTATION ENDS HERE

**DocuMind Backend is COMPLETE, VERIFIED, and PRODUCTION-READY.**

**Next logical milestones**
- Frontend UI completion  
- Authentication hardening  
- AWS deployment (STEP 10)

