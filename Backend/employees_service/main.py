from fastapi import FastAPI
from .app.core.db import engine, Base
from .app.routers import employees

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Employees Service", version="1.0.0")

# Include routers
app.include_router(employees.router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "Employees Service"}

@app.get("/")
def root():
    return {"message": "Employees Service API"}


