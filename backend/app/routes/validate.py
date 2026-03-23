from fastapi import APIRouter, Depends
from app.services.validation_service import validate_data_quality
from backend.app.auth import verify_api_key

router = APIRouter()

@router.post("/api/validate/data-quality", dependencies=[Depends(verify_api_key)])

def validate_data_quality_endpoint(data: dict):
    return validate_data_quality(data)