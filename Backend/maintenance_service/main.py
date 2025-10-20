
from fastapi import FastAPI
from app.routers.health import router as health_router
from app.routers.maintenance import router as maintenance_router

app = FastAPI(title='Maintenance Service')

app.include_router(health_router)
app.include_router(maintenance_router)
