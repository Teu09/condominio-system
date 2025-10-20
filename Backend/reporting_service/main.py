
from fastapi import FastAPI
from app.routers.health import router as health_router
from app.routers.reports import router as reports_router

app = FastAPI(title='Reporting Service')

app.include_router(health_router)
app.include_router(reports_router)
