from fastapi import FastAPI
from .app.core.db import engine, Base
from .app.routers import meetings

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Meetings Service", version="1.0.0")

# Include routers
app.include_router(meetings.router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "Meetings Service"}

@app.get("/")
def root():
    return {"message": "Meetings Service API"}


