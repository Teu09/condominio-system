
from fastapi import FastAPI
from app.routers.units import router as units_router

app = FastAPI(title='Unit Service')

app.include_router(units_router)

@app.get('/health')
def health():
    return {'status': 'ok'}
