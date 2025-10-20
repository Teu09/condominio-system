from fastapi import FastAPI
from .app.core.db import engine, Base
from .app.routers import service_providers

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Service Providers Service", version="1.0.0")

# Include routers
app.include_router(service_providers.router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "Service Providers Service"}

@app.get("/")
def root():
    return {"message": "Service Providers Service API"}

