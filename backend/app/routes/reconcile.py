from fastapi import APIRouter
from app.services.reconciliation_service import reconcile_medication

router = APIRouter()

@router.post("/api/reconcile/medication")

def reconcile_medication_endpoint(data: dict):
    return reconcile_medication(data)