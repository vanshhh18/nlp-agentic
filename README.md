# 🤖 NLP Agentic Helpdesk

An intelligent customer support system that automatically classifies tickets, routes them to the correct department, and generates AI-powered responses using RAG.

[![Streamlit App](https://img.shields.io/badge/Streamlit-Live%20Demo-FF4B4B?style=for-the-badge&logo=streamlit)](https://nlp-agentic-dawto6kavvg8wrmmycm4xq.streamlit.app/)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-API-FFD21E?style=for-the-badge&logo=huggingface)](https://huggingface.co/spaces/vanshhh-18/nlp-agentic)

---

## 🚀 What it does

1. **User submits a support ticket** via the Streamlit UI
2. **NLP model classifies** the ticket into a department and priority level
3. **LangGraph workflow routes** the ticket to the appropriate department agent
4. **RAG pipeline retrieves** relevant knowledge base documents
5. **Groq LLM generates** a professional AI response
6. **Confirmation email** is sent to the user with ticket details

---

## 🏗️ Architecture

```
User (Streamlit UI)
        ↓
FastAPI Backend (HuggingFace Spaces)
        ↓
┌───────────────────────────────────┐
│         NLP Classification        │
│  scikit-learn (LinearSVC)         │
│  → Department + Priority          │
└───────────────────────────────────┘
        ↓
┌───────────────────────────────────┐
│       LangGraph Workflow          │
│  → Route to Department Agent      │
└───────────────────────────────────┘
        ↓
┌───────────────────────────────────┐
│         RAG Pipeline              │
│  ChromaDB + Sentence Transformers │
│  → Retrieve relevant docs         │
│  → Groq LLM generates response    │
└───────────────────────────────────┘
        ↓
    AI Response returned to user
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| Backend | FastAPI, Uvicorn |
| NLP Model | scikit-learn (LinearSVC) |
| Orchestration | LangGraph |
| RAG | LangChain, ChromaDB, Sentence Transformers |
| LLM | Groq (LLaMA) |
| Deployment | HuggingFace Spaces, Streamlit Cloud |

---

## 📂 Project Structure

```
nlp-agentic/
├── main.py                  # FastAPI entry point
├── email_service.py         # Email notification service
├── agents/                  # Department-specific agents
├── graph_workflow/          # LangGraph workflow definition
├── rag/                     # RAG retriever
├── llm/                     # Groq LLM setup
├── vectorstore/             # ChromaDB vector store
├── Knowledge_base/          # Source documents for RAG
├── ticket_classifier.pkl    # Trained NLP classification model
├── tfidf_vectorizer.pkl     # TF-IDF vectorizer
└── requirements.txt
```

---

## ⚙️ Local Setup

```bash
# Clone the repo
git clone https://github.com/vanshhh-18/nlp-agentic.git
cd nlp-agentic

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GROQ_API_KEY=your_groq_api_key

# Run FastAPI backend
uvicorn main:app --host 0.0.0.0 --port 8000

# Run Streamlit frontend (in a separate terminal)
streamlit run app.py
```

---

## 🌐 Live Demo

- **Frontend:** https://nlp-agentic-dawto6kavvg8wrmmycm4xq.streamlit.app/
- **Backend API:** https://huggingface.co/spaces/vanshhh-18/nlp-agentic
- **API Docs:** https://vanshhh-18-nlp-agentic.hf.space/docs

---

## 📊 Model Details

- **Task:** Multi-output classification (Department + Priority)
- **Algorithm:** LinearSVC with MultiOutputClassifier
- **Features:** TF-IDF vectorization
- **Departments:** 10 categories (IT Support, Billing, HR, Technical Support, etc.)
- **Priority Levels:** High, Medium, Low
