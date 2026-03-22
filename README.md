# EHR Reconciliation & Data Quality Dashboard

A full-stack clinical decision support tool that combines rule-based logic and AI to improve electronic health record (EHR) reliability.

This system performs:

* Medication reconciliation across multiple sources
* Data quality assessment with scoring and issue detection
* AI-generated clinical reasoning and summaries
* A clinician-facing dashboard for review and decision-making

---

## Features

### Medication Reconciliation

* Aggregates medication data from multiple sources (EHR, Primary Care, Pharmacy)
* Uses:

  * Source reliability scoring
  * Recency of records
* Selects the most trustworthy medication record
* Provides:

  * Confidence score
  * AI-generated clinical reasoning
  * Recommended follow-up actions

---

### Data Quality Assessment

* Evaluates clinical records across 4 dimensions:

  * Completeness
  * Accuracy
  * Timeliness
  * Clinical Plausibility
* Detects issues such as:

  * Missing demographics
  * Implausible vital signs
  * Outdated records
* Outputs:

  * Overall quality score
  * Detailed breakdown
  * Structured issue list
  * AI-generated clinical summary

---

### AI Integration

* Uses an LLM API to:

  * Generate clinical reasoning for reconciliation decisions
  * Summarize detected data quality issues
* Designed with:

  * Structured prompts including clinical context
  * Graceful fallback if API is unavailable
  * Cost-awareness (optional caching-ready design)

---

### Frontend Dashboard

* Simple, clinician-friendly UI
* Features:

  * JSON input panels for testing
  * Color-coded scores (green / yellow / red)
  * Clear issue visualization with severity levels
  * Confidence display
  * AI reasoning and summaries
  * Approve / Reject interaction to simulate clinician validation

---

## Tech Stack

**Backend**

* Python
* FastAPI
* Uvicorn

**Frontend**

* React (Create React App)

**AI**

* OpenAI API

---

## Project Structure

```
ehr-project/
│
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   ├── services/
│   │   └── main.py
│   ├── tests/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   └── package.json
│
└── README.md
```

---

## Setup Instructions

### 1. Clone the repository

```
git clone https://github.com/benkhant/ehr-project.git
cd ehr-project
```

---

### 2. Backend Setup

```
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file:

```
OPENAI_API_KEY=your_api_key_here
```

Run backend:

```
uvicorn app.main:app --reload
```

API available at:

```
http://127.0.0.1:8000/docs
```

---

### 3. Frontend Setup

```
cd frontend
npm install
npm start
```

Frontend runs at:

```
http://localhost:3000
```

---

## Example Inputs

### Medication Reconciliation

```json
{
  "patient_context": {
    "age": 67,
    "conditions": ["Type 2 Diabetes", "Hypertension"],
    "recent_labs": {"eGFR": 45}
  },
  "sources": [
    {
      "system": "Hospital EHR",
      "medication": "Metformin 1000mg twice daily",
      "last_updated": "2024-10-15",
      "source_reliability": "high"
    },
    {
      "system": "Primary Care",
      "medication": "Metformin 500mg twice daily",
      "last_updated": "2025-01-20",
      "source_reliability": "high"
    },
    {
      "system": "Pharmacy",
      "medication": "Metformin 1000mg daily",
      "last_filled": "2025-01-25",
      "source_reliability": "medium"
    }
  ]
}
```

---

### Data Quality Validation

```json
{
  "demographics": {
    "name": "John Doe",
    "dob": "1955-03-15",
    "gender": "M"
  },
  "medications": ["Metformin 500mg", "Lisinopril 10mg"],
  "allergies": [],
  "conditions": ["Type 2 Diabetes"],
  "vital_signs": {
    "blood_pressure": "340/180",
    "heart_rate": 72
  },
  "last_updated": "2024-06-15"
}
```

---

## Design Decisions

* Combined **rule-based logic + AI reasoning** for reliability and interpretability
* Prioritized **clinician readability over UI complexity**
* Implemented **human-in-the-loop validation** (approve/reject)
* Used scoring system to simulate **real-world data quality metrics**

---

## Limitations

* No persistent database (decisions not stored)
* Simplified clinical logic (not production-grade)
* Limited validation rules and edge case handling
* API usage depends on available credits

---

## Future Improvements

* Add database for audit trail and decision tracking
* Expand clinical validation rules (drug interactions, contraindications)
* Improve UI/UX with charts and visualizations
* Add authentication and user roles
* Implement caching for AI responses

---

## Notes

This project is not intended for real clinical use.