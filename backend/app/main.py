from fastapi import FastAPI
from app.routes import reconcile, validate
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(reconcile.router)
app.include_router(validate.router)

@app.get("/")
def root():
    return {"message": "EHR reconciliation API is running!"}