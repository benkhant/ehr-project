# Architecture Decisions

## Overview

This system uses a hybrid architecture combining rule-based logic with LLM-generated explanations. The backend is implemented with FastAPI and the frontend with React, communicating via REST APIs.

---

## Key Decisions

### 1. Rule-based logic + LLM integration

Core decision-making (reconciliation and data quality scoring) is handled using deterministic rule-based logic. LLMs are used only for generating explanations and summaries.

**Why:**
- Ensures predictable and testable behavior
- Avoids relying on LLMs for critical decisions
- Improves interpretability for clinical use

---

### 2. No database (in-memory approach)

The system does not use persistent storage.

**Why:**
- Database was optional in the assignment
- Focus was placed on API design and AI integration
- Simplifies architecture while meeting requirements

---

### 3. Simple API key authentication

Endpoints are protected using a basic API key mechanism.

**Why:**
- Meets security requirement without overengineering
- Keeps implementation lightweight and focused

---

### 4. Frontend simplicity

The React frontend prioritizes clarity over design complexity.

**Why:**
- Focus on clinician usability
- Clear display of scores, reasoning, and decisions

---

### 5. Deployment architecture

- Backend deployed on Render
- Frontend deployed on Vercel

**Why:**
- Simple and widely used deployment platforms
- Enables real-world full-stack demonstration