
from fastapi import FastAPI
from app.routers.health import router as health_router
from app.routers.visitors import router as visitors_router

app = FastAPI(title='Visitor Service')

app.include_router(health_router)
app.include_router(visitors_router)
