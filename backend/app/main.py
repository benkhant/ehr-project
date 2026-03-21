from fastapi import FastAPI
from app.routes import reconcile, validate

app = FastAPI()
app.include_router(reconcile.router)
app.include_router(validate.router)

@app.get("/")
def root():
    return {"message": "EHR reconciliation API is running!"}