from fastapi import FastAPI
from app.routers import tenants, health

app = FastAPI(title="Tenant Service", version="1.0.0")

app.include_router(health.router)
app.include_router(tenants.router)


@app.get("/")
async def root():
    return {"message": "Tenant Service is running"}
