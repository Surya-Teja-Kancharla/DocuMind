# 🚀 DocuMind - Complete Setup & Deployment Guide

## 📋 What's Been Implemented

### ✅ **Backend Enhancements**

1. **Session Management API** (`backend/app/api/sessions.py`)
   - `POST /sessions/create` - Create new chat session
   - `GET /sessions/list/{user_id}` - Get all user sessions
   - `GET /sessions/{session_id}/messages` - Load conversation history
   - `PATCH /sessions/{session_id}/title` - Update session title
   - `DELETE /sessions/{session_id}` - Delete session and messages
   - `POST /sessions/{session_id}/generate-title` - Auto-generate ChatGPT-like title

2. **Enhanced LLM Service** (`backend/app/services/llm.py`)
   - Added synchronous `generate_answer()` for title generation
   - Maintains existing async streaming for chat

3. **Updated Main Application** (`backend/app/main.py`)
   - Integrated sessions router
   - All endpoints properly registered

### ✅ **Frontend Enhancements**

1. **Complete Session Management** (`frontend/src/api/chat.js`)
   - Full CRUD operations for sessions
   - Message loading and persistence
   - Auto-title generation integration

2. **Persistent HomePage** (`frontend/src/components/HomePage.jsx`)
   - Loads all sessions from Supabase on startup
   - Creates new sessions via API
   - Deletes sessions with API integration
   - Handles empty state gracefully

3. **Smart ChatWindow** (`frontend/src/components/ChatWindow.jsx`)
   - Auto-generates title after first message
   - Improved toast notifications
   - Better error handling

4. **Environment Configuration** (`frontend/.env`)
   - API base URL properly configured

---

## 🛠️ Setup Instructions

### **Prerequisites**

- Python 3.10+
- Node.js 18+
- Docker & Docker Compose
- Supabase account (already set up ✅)

### **1. Backend Setup**

#### A. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

#### B. Configure Environment Variables

Create `backend/.env`:

```env
# LLM API
GROQ_API_KEY=your_groq_api_key_here

# Redis
REDIS_URL=redis://localhost:6379

# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

#### C. Start Infrastructure

```bash
# Start Milvus + Redis
docker-compose -f docker-compose-milvus.yml up -d

# Verify services
docker ps  # Should see: milvus, etcd, minio, redis
```

#### D. Start Backend Server

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

**Verify Backend:**

```bash
curl http://localhost:8000/health
# Expected: {"status": "DocuMind backend running"}
```

---

### **2. Frontend Setup**

#### A. Install Dependencies

```bash
cd frontend
npm install
```

#### B. Verify Environment

Check `frontend/.env`:

```env
VITE_API_BASE=http://localhost:8000
```

#### C. Start Frontend

```bash
npm run dev
```

**Frontend will be available at:** `http://localhost:5173`

---

## 🧪 Testing the Complete System

### **Test 1: Session Creation**

1. Open http://localhost:5173
2. Wait for "Loading your chats..." to complete
3. If no sessions exist, one will be created automatically
4. Click "+ New Chat" to create additional sessions

**Expected:** New session appears in sidebar with "New Chat" title

### **Test 2: Document Upload & Chat**

1. Click the "+" button in the chat input
2. Upload a PDF/DOCX/PPTX file
3. Wait for "Document indexed successfully" toast
4. Type a question and press Enter

**Expected:**

- Streaming response appears
- Title auto-generates after first message
- Session title updates in sidebar

### **Test 3: Session Persistence**

1. Create a chat and send messages
2. Refresh the page (F5)
3. All sessions should reload
4. Click any old session to resume

**Expected:** All conversations persist and can be resumed

### **Test 4: Session Deletion**

1. Hover over a session in sidebar
2. Click the trash icon (🗑️)
3. Session disappears

**Expected:** Session and all messages deleted from Supabase

---

## 🔍 API Endpoint Documentation

### **Session Endpoints**

#### Create Session

```bash
POST /sessions/create
Content-Type: application/json

{
  "user_id": "local-user",
  "title": "New Chat"
}

Response: {
  "session_id": "uuid",
  "user_id": "local-user",
  "title": "New Chat",
  "created_at": "2026-01-17T...",
  "updated_at": "2026-01-17T..."
}
```

#### List Sessions

```bash
GET /sessions/list/local-user

Response: [
  {
    "session_id": "uuid",
    "user_id": "local-user",
    "title": "Python Tutorial Questions",
    "created_at": "2026-01-17T...",
    "updated_at": "2026-01-17T..."
  }
]
```

#### Get Session Messages

```bash
GET /sessions/{session_id}/messages

Response: [
  {
    "role": "user",
    "content": "What is Python?",
    "created_at": "2026-01-17T..."
  },
  {
    "role": "assistant",
    "content": "Python is a programming language...",
    "created_at": "2026-01-17T..."
  }
]
```

#### Generate Title

```bash
POST /sessions/{session_id}/generate-title

Response: {
  "status": "success",
  "session_id": "uuid",
  "title": "Python Programming Questions"
}
```

---

## 🐛 Troubleshooting

### **Issue: "Database unavailable"**

**Solution:** Check Supabase credentials in `.env`

```bash
# Test Supabase connection
curl -H "apikey: your_supabase_key" \
     "your_supabase_url/rest/v1/chat_sessions?select=*&limit=1"
```

### **Issue: "Redis unavailable"**

**Solution:** Verify Redis is running

```bash
docker ps | grep redis
# If not running:
docker-compose -f docker-compose-milvus.yml up -d redis
```

### **Issue: "Milvus connection failed"**

**Solution:** Restart Milvus stack

```bash
docker-compose -f docker-compose-milvus.yml down
docker-compose -f docker-compose-milvus.yml up -d
```

### **Issue: "Frontend can't connect to backend"**

**Solution:**

1. Verify backend is running on port 8000
2. Check `frontend/.env` has correct `VITE_API_BASE`
3. Clear browser cache and restart dev server

---

## 📊 Database Schema (Already Created ✅)

### **chat_sessions**

```sql
CREATE TABLE chat_sessions (
  session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id TEXT NOT NULL,
  title TEXT DEFAULT 'New Chat',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_sessions_user ON chat_sessions(user_id, updated_at DESC);
```

### **chat_messages**

```sql
CREATE TABLE chat_messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id TEXT NOT NULL,
  session_id TEXT NOT NULL,
  role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
  content TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_chat_session ON chat_messages(session_id, created_at);
```

---

## 🚀 Deployment to AWS (Production)

### **Option 1: AWS EC2 (Recommended for Resume)**

#### Backend Deployment

1. Launch EC2 instance (t3.medium or larger)
2. Install Docker, Docker Compose, Python
3. Clone repository
4. Set up `.env` with production credentials
5. Run: `docker-compose up -d`
6. Run: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
7. Configure security group: Open ports 8000, 19530, 6379
8. Use Nginx as reverse proxy

#### Frontend Deployment

1. Build frontend: `npm run build`
2. Upload `dist/` to S3 bucket
3. Enable static website hosting
4. Configure CloudFront for CDN
5. Update `.env.production` with production API URL

### **Option 2: AWS Elastic Beanstalk**

1. Create Elastic Beanstalk application
2. Deploy backend as Docker container
3. Frontend served via S3 + CloudFront

### **Option 3: Docker Compose on Single EC2**

```yaml
# docker-compose.prod.yml
version: "3.8"
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_KEY=${SUPABASE_KEY}
    depends_on:
      - milvus
      - redis

  frontend:
    build: ./frontend
    ports:
      - "80:80"
```

---

## ✅ Resume Highlights

**Key Achievements:**

1. ✅ Built production-grade RAG system with LlamaIndex
2. ✅ Implemented full session management (ChatGPT-like)
3. ✅ Used Groq for LLM inference (cost-efficient)
4. ✅ Integrated Milvus for vector search
5. ✅ Session persistence with Supabase
6. ✅ Redis caching for performance
7. ✅ RAGAS evaluation framework
8. ✅ Modern React frontend with streaming
9. ✅ Docker containerization
10. ✅ AWS deployment ready

**Tech Stack Demonstrated:**

- **Backend:** FastAPI, LlamaIndex, Groq API
- **Vector DB:** Milvus
- **Storage:** Supabase (PostgreSQL), Redis
- **Frontend:** React 19, Vite, Tailwind CSS
- **ML/AI:** NOMIC embeddings, RAG architecture
- **DevOps:** Docker, Docker Compose, AWS-ready

---

## 🎯 Next Steps (Optional Enhancements)

1. **Authentication:** Add user login with Supabase Auth
2. **Multi-user:** Support multiple authenticated users
3. **Document Management:** UI to view/delete uploaded documents
4. **Export:** Download conversations as PDF/Markdown
5. **Search:** Search across all conversations
6. **Analytics:** Track usage metrics
7. **Rate Limiting:** Implement API rate limits
8. **Monitoring:** Add Prometheus + Grafana
9. **CI/CD:** GitHub Actions for automated deployment
10. **Mobile App:** React Native version

---

## 📝 Final Checklist

- [x] Backend session API implemented
- [x] Frontend session management complete
- [x] Auto-title generation working
- [x] Session persistence to Supabase
- [x] Session loading on startup
- [x] Document upload working
- [x] Chat streaming working
- [x] Session deletion working
- [x] All endpoints tested
- [x] Error handling robust
- [x] Loading states implemented
- [x] Toast notifications working
- [x] Responsive design
- [x] Production-ready architecture
- [x] Resume-worthy features

---

## 🎉 Congratulations!

You now have a **production-ready, ChatGPT-like RAG chatbot** with:

- ✅ Full session management
- ✅ Document-based conversations
- ✅ Persistent chat history
- ✅ Auto-title generation
- ✅ Modern, responsive UI
- ✅ Scalable architecture
- ✅ AWS deployment ready

**This is a strong portfolio project for ML/AI engineer roles!** 🚀
