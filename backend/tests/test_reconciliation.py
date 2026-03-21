from app.services.reconciliation_service import reconcile_medication

def test_picks_highest_reliability():
    data = {
    "patient_context": {},
    "sources": [
        {"medication": "A", "source_reliability": "low"},
        {"medication": "B", "source_reliability": "high"}
        ]
    }

    result = reconcile_medication(data)
    assert result["reconciled_medication"] == "B"

def test_tie_break_by_recency():
    data = {
        "patient_context": {},
        "sources": [
            {
                "medication": "Old",
                "source_reliability": "medium",
                "last_updated": "2023-10-10"
            },
            {
                "medication": "New",
                "source_reliability": "medium",
                "last_updated": "2024-01-01"
            }
        ]
    }

    result = reconcile_medication(data)
    assert result["reconciled_medication"] == "New"

def test_no_sources_returns_error():
    data = {
        "patient_context": {},
        "sources": []
    }

    result = reconcile_medication(data)
    assert "error" in result
    assert result["error"] == "No medication sources provided."