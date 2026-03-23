# EHR Reconciliation & Data Quality Dashboard

A full-stack application that reconciles conflicting medication records and evaluates clinical data quality using a hybrid rule-based + LLM-assisted approach.

The system combines deterministic rule-based logic for decision-making with LLM-generated explanations for interpretability, delivered through a FastAPI backend and a React frontend dashboard.

---

## Features

### Medication Reconciliation

Aggregates medication data from multiple sources (EHR, Primary Care, Pharmacy) 
and selects the most trustworthy record based on:
* Source reliability scoring
* Recency of records
* Conflicting data across systems

Provides:
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

## LLM Choice

This project uses the OpenAI API to generate:

* Clinical reasoning for reconciliation decisions
* Human-readable summaries for data quality findings

I chose OpenAI because it provides strong structured reasoning capabilities, integrates easily with a Python backend, and produces concise, clinically interpretable outputs when guided with structured prompts.

---

## AI Integration

* Used OpenAI API to generate clinical reasoning and summaries
* Prompt includes structured clinical context:
  * patient data
  * detected issues
* Designed for:
  * accuracy
  * concise explanations
  * clinician readability
* Includes fallback logic when API is unavailable

---

## Frontend Dashboard

* Simple, clinician-friendly UI
* Features:

  * JSON input panels for testing
  * Color-coded scores (green / yellow / red)
  * Clear issue visualization with severity levels
  * Confidence display
  * AI reasoning and summaries
  * Approve / Reject interaction to simulate clinician validation

---

## API Protection

The backend uses a simple API key check for protected endpoints. Clients must send the `x-api-key` header, and the expected key is configured through the `APP_API_KEY` environment variable.

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

## Deployment

* Backend deployed on Render
* Frontend deployed on Vercel

Production environment variables:
* OPENAI_API_KEY
* APP_API_KEY
* REACT_APP_API_BASE_URL
* REACT_APP_API_KEY

---

## Live Demo

Frontend: https://ehr-project-six.vercel.app  
Backend: https://ehr-project.onrender.com

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
APP_API_KEY=your_app_key_here
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
```

Create a `.env.local` file in the `frontend/` folder:

```
REACT_APP_API_BASE_URL=http://127.0.0.1:8000
REACT_APP_API_KEY=your_app_key_here
```

Then start the app:

```
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

## Design Trade-offs

* Used rule-based logic for core decision-making and LLMs only for explanation, ensuring deterministic and testable outputs
* Did not include a database to prioritize core functionality and keep the system simple, as persistence was optional
* Implemented a simple API key mechanism instead of full authentication to balance security with development speed
* Used heuristic scoring rather than trained calibration models to maintain interpretability and simplicity

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
* Containerize the stack with Docker

---

## Estimated Time Spent

Approximately 8-12 hours total, including:

- Backend development and API design
- AI integration and prompt design
- Frontend dashboard implementation
- Testing and debugging
- Deployment setup (Vercel + Render)

---

## Notes

This project is not intended for real clinical use.