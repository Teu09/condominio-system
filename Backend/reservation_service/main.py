
from fastapi import FastAPI
from app.routers.reservations import router as reservations_router

app = FastAPI(title='Reservation Service')

app.include_router(reservations_router)

@app.get('/health')
def health():
    return {'status': 'ok'}
