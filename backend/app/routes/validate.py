from fastapi import APIRouter
from app.services.validation_service import validate_data_quality

router = APIRouter()

@router.post("/api/validate/data-quality")

def validate_data_quality_endpoint(data: dict):
    return validate_data_quality(data)