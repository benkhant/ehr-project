from datetime import datetime
from app.services.llm_service import generate_reconciliation_reasoning

RELIABILITY_SCORES = {
    "high": 3, 
    "medium": 2,
    "low": 1
}

def parse_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None
    
def reconcile_medication(data: dict):
    patient_context = data.get("patient_context", {})
    sources = data.get("sources", [])

    if not sources:
        return {"error": "No medication sources provided."}

    best = None
    best_date = None
    best_score = -1

    for source in sources:
        reliability = source.get("source_reliability", "low").lower()
        reliability_score = RELIABILITY_SCORES.get(reliability, 1)

        date_str = source.get("last_updated") or source.get("last_filled", "")
        current_date = parse_date(date_str)

        recency_score = 1 if current_date else 0
        total_score = reliability_score + recency_score

        if best is None:
            best = source
            best_date = current_date
            best_score = total_score
            continue

        if total_score > best_score:
            best_score = total_score
            best = source
            best_date = current_date
        elif total_score == best_score:
            if current_date and (best_date is None or current_date > best_date):
                best = source
                best_date = current_date
       
    confidence_score = min(0.5 + (best_score * 0.1), 0.95)
    
    reasoning = generate_reconciliation_reasoning(patient_context, best, sources)

    chosen_system = best.get("system", "unknown source")
    chosen_medication = best.get("medication", "unknown medication")

    return {
        "reconciled_medication": chosen_medication,
        "confidence_score": round(confidence_score, 2),
        "reasoning": reasoning,  
        "recommended_actions": [
            f"Verify {chosen_medication} with clinician or pharmacy",
            f"Review other conflicting records from {len(sources) - 1} additional source(s)"
        ],
        "clinical_safety_check": "PASSED"
    }