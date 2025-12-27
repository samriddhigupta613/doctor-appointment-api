from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token

class AuthService:
    def __init__(self, repo):
        self.repo = repo

    async def register(self, data):
        user = User(
            email=data.email,
            password_hash=hash_password(data.password),
            role=data.role,
            name=data.name
        )
        return await self.repo.create(user)

    async def login(self, data):
        user = await self.repo.get_by_email(data.email)
        if not user or not verify_password(data.password, user.password_hash):
            return None

        return create_access_token(
            {
                "sub": str(user.id),
                "role": user.role,
            }
        )

