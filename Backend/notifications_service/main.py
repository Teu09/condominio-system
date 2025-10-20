from fastapi import FastAPI
from .app.core.db import engine, Base
from .app.routers import notifications

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Notifications Service", version="1.0.0")

# Include routers
app.include_router(notifications.router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "Notifications Service"}

@app.get("/")
def root():
    return {"message": "Notifications Service API"}

