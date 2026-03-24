from fastapi import APIRouter, Depends
from app.services.reconciliation_service import reconcile_medication
from app.auth import verify_api_key

router = APIRouter()

@router.post("/api/reconcile/medication", dependencies=[Depends(verify_api_key)])

def reconcile_medication_endpoint(data: dict):
    return reconcile_medication(data)