
from fastapi import FastAPI
from app.routers.health import router as health_router

app = FastAPI(title='Visitor Service')

app.include_router(health_router)
