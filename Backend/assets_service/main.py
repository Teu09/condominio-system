from fastapi import FastAPI
from .app.core.db import engine, Base
from .app.routers import assets

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Assets Service", version="1.0.0")

# Include routers
app.include_router(assets.router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "Assets Service"}

@app.get("/")
def root():
    return {"message": "Assets Service API"}


