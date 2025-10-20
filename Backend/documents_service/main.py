from fastapi import FastAPI
from .app.core.db import engine, Base
from .app.routers import documents

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Documents Service", version="1.0.0")

# Include routers
app.include_router(documents.router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "Documents Service"}

@app.get("/")
def root():
    return {"message": "Documents Service API"}


