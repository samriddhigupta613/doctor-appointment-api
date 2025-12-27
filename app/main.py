from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api import auth, appointments, doctors
from app.api import auth, appointments
from app.db.session import engine
from app.db.base import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Doctor Appointment API running"}


app.include_router(auth.router)
app.include_router(appointments.router)
app.include_router(doctors.router)



