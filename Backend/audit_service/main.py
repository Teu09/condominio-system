from fastapi import FastAPI
from .app.core.db import engine, Base
from .app.routers import audit

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Audit Service", version="1.0.0")

# Include routers
app.include_router(audit.router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "Audit Service"}

@app.get("/")
def root():
    return {"message": "Audit Service API"}

