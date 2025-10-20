from fastapi import FastAPI
from .app.core.db import engine, Base
from .app.routers import family_members

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Family Members Service", version="1.0.0")

# Include routers
app.include_router(family_members.router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "Family Members Service"}

@app.get("/")
def root():
    return {"message": "Family Members Service API"}

