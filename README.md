# LangGraph Multi-User AI Chatbot

A production-style multi-user AI chatbot platform built with **LangGraph, Groq LLM, Streamlit, and Supabase Postgres**, supporting authentication, conversation management, streaming responses, and persistent chat threads.

This project demonstrates how to build a **stateful, agent-style LLM application with real user accounts and conversation memory**, similar to modern chat platforms.

---

## Overview

This application allows multiple users to:
- Create accounts
- Log in securely
- Chat with an AI assistant
- Manage conversation threads
- Reset passwords
- Rename and delete conversations
- Search past conversations

The chatbot uses **LangGraph for stateful execution** and **Groq Llama‑3‑70B** for fast LLM responses.

---

## Features

### Authentication & Security
- User signup
- JWT-based authentication
- bcrypt password hashing
- Logout functionality
- Password reset via security question
- Case-insensitive security answer validation
- Per-user conversation isolation

---

### Conversation Management
- Multiple chat threads per user
- Sidebar conversation navigation
- Search conversations by title
- Rename conversation
- Delete conversation
- Temporary "Untitled Chat" placeholder
- Automatic thread title generation
- Automatic title updates

---

### Automatic Thread Title Generation
Thread titles are generated dynamically using the LLM:

- Title created after **first user message**
- Title updated after **every 3 user messages**
- Sidebar updates automatically
- No UI blocking during title generation

---

### Chat Experience
- Streaming AI responses
- Typing indicator
- Instant user message rendering
- Persistent conversation history
- Multi-thread chat memory
- Chat-style UI layout

---

### AI System (LangGraph)

The chatbot uses a **state graph execution model**:

- LangGraph state workflow
- Message-based state management
- Streaming LLM responses
- Groq Llama‑3‑70B model

This demonstrates **agentic orchestration rather than simple API prompting**.

---

### Persistence Layer

#### Supabase Postgres
Stores:
- Users
- Thread metadata
- Thread titles

Provides:
- Multi-user persistence
- Conversation ownership isolation
- Production-ready storage

---

#### SQLite (LangGraph Checkpointing)
Stores:
- Conversation state
- Message history

Used for:
- Fast checkpoint persistence
- Graph state recovery

---

## Tech Stack

**Frontend**
- Streamlit

**LLM / Agents**
- LangGraph
- LangChain Core
- Groq LLM (Llama‑3‑70B)

**Backend**
- Python

**Database**
- Supabase Postgres
- SQLite

**Security**
- JWT
- bcrypt

---

## Project Structure

```
project/
│
├── backend.py
├── frontend.py
├── requirements.txt
├── .env
└── memory.db
```

---

## Installation

### 1. Clone repository
```bash
git clone <repo-url>
cd project
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create `.env`
```
GROQ_API_KEY=your_key
JWT_SECRET=your_secret
DATABASE_URL=your_supabase_pooler_url
```

### 4. Run the app
```bash
streamlit run frontend.py
```

---

## Deployment

The app is designed to run on:

- Streamlit Community Cloud
- Supabase Postgres
- Groq API

Architecture:

```
Browser
   ↓
Streamlit App
   ↓
LangGraph
   ↓
Groq LLM
   ↓
Supabase Postgres
   ↓
SQLite Checkpoints
```

---

## Learning Outcomes

This project demonstrates:

- Building a multi-user AI system
- LangGraph stateful workflows
- LLM streaming integration
- Authentication with JWT
- Password hashing with bcrypt
- Database-backed conversation management
- UI state synchronization
- Production-style chatbot architecture

---

## Future Improvements
- Email‑OTP password reset
- RAG knowledge base integration
- Conversation export
- Conversation timestamps
- Pinned chats
- Admin dashboard
- Conversation analytics

---

## Author
Aryan Singh
