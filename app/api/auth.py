from fastapi import APIRouter, Depends, HTTPException
from app.schemas.auth import RegisterSchema, LoginSchema
from app.repositories.user_repo import UserRepository
from app.services.auth_service import AuthService
from app.db.session import AsyncSessionLocal

router = APIRouter(prefix="/auth")

@router.post("/register")
async def register(data: RegisterSchema):
    async with AsyncSessionLocal() as session:
        service = AuthService(UserRepository(session))
        return await service.register(data)

@router.post("/login")
async def login(data: LoginSchema):
    async with AsyncSessionLocal() as session:
        service = AuthService(UserRepository(session))
        token = await service.login(data)
        if not token:
            raise HTTPException(status_code=401)
        return {"access_token": token}
