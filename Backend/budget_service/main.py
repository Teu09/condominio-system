from fastapi import FastAPI
from .app.core.db import engine, Base
from .app.routers import budgets

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Budget Service", version="1.0.0")

# Include routers
app.include_router(budgets.router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "Budget Service"}

@app.get("/")
def root():
    return {"message": "Budget Service API"}


