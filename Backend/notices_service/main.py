from fastapi import FastAPI
from .app.core.db import engine, Base
from .app.routers import notices

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Notices Service", version="1.0.0")

# Include routers
app.include_router(notices.router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "Notices Service"}

@app.get("/")
def root():
    return {"message": "Notices Service API"}

