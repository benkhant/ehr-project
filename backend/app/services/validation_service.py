from datetime import datetime
from app.services.llm_service import review_data_quality_with_llm

def validate_data_quality(data: dict):
    breakdown = {
        "completeness": 100,
        "accuracy": 100,
        "timeliness": 100,
        "clinical_plausibility": 100
    }

    PENALTIES = {
    "missing_demographics": 20,
    "missing_medications": 20,
    "missing_allergies": 10,
    "missing_conditions": 10,
    "invalid_bp": {"plausibility": 60, "accuracy": 40},
    "invalid_bp_format": 20,
    "old_data": 30,
    "missing_last_updated": 40,
    "invalid_last_updated": 20
    }

    issues_detected = []

    demographics = data.get("demographics", {})
    medications = data.get("medications", [])
    allergies = data.get("allergies", [])
    conditions = data.get("conditions", [])
    vital_signs = data.get("vital_signs", {})
    last_updated = data.get("last_updated", "")

    if not demographics.get("name") or not demographics.get("dob") or not demographics.get("gender"):
        breakdown["completeness"] -= PENALTIES["missing_demographics"]
        issues_detected.append({
            "field": "demographics",
            "issue": "Missing one or more required demographic fields",
            "severity": "high"
        })

    if not medications:
        breakdown["completeness"] -= PENALTIES["missing_medications"]
        issues_detected.append({
            "field": "medications",
            "issue": "No medications documented",
            "severity": "medium"
        })

    if not allergies:
        breakdown["completeness"] -= PENALTIES["missing_allergies"]
        issues_detected.append({
            "field": "allergies",
            "issue": "No allergies documented - likely incomplete",
            "severity": "medium"
        })

    if not conditions:
        breakdown["completeness"] -= PENALTIES["missing_conditions"]
        issues_detected.append({
            "field": "conditions",
            "issue": "No conditions documented",
            "severity": "medium"
        })

    bp = vital_signs.get("blood_pressure")
    if bp: 
        try: 
            systolic, diastolic = map(int, bp.split("/"))
            if systolic > 300 or diastolic > 200:
                breakdown["clinical_plausibility"] -= PENALTIES["invalid_bp"]["plausibility"]
                breakdown["accuracy"] -= PENALTIES["invalid_bp"]["accuracy"]
                issues_detected.append({
                    "field": "vital_signs.blood_pressure",
                    "issue": f"Blood pressure reading {bp} is physiologically implausible",
                    "severity": "high"
                })
        except ValueError:
            breakdown["accuracy"] -= PENALTIES["invalid_bp"]
            issues_detected.append({
                "field": "vital_signs.blood_pressure",
                "issue": "Blood pressure format is invalid",
                "severity": "medium"
            })

    if last_updated:
        try:
            updated_date = datetime.strptime(last_updated, "%Y-%m-%d")
            days_old = (datetime.now() - updated_date).days
            if days_old > 180:
                breakdown["timeliness"] -= PENALTIES["old_data"]
                issues_detected.append({
                    "field": "last_updated",
                    "issue": "Data is 6+ months old",
                    "severity": "medium"
                })
        except ValueError:
            breakdown["timeliness"] -= PENALTIES["invalid_last_updated"]
            issues_detected.append({
                "field": "last_updated",
                "issue": "Invalid date format for last_updated",
                "severity": "medium"
            })
    else:
        breakdown["timeliness"] -= PENALTIES["missing_last_updated"]
        issues_detected.append({
            "field": "last_updated",
            "issue": "Missing last_updated field",
            "severity": "high"
        })

    overall_score = round(sum(breakdown.values()) / len(breakdown))
    llm_review = review_data_quality_with_llm(data, issues_detected)
    combined_issues = issues_detected + llm_review.get("additional_issues", [])

    return {
        "overall_score": overall_score,
        "breakdown": breakdown,
        "issues_detected": combined_issues,
        "llm_summary": llm_review.get("summary", "")
    }