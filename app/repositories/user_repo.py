from sqlalchemy import select
from app.models.user import User

class UserRepository:
    def __init__(self, session):
        self.session = session

    async def get_by_email(self, email: str):
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(self, user: User):
        self.session.add(user)
        await self.session.commit()
        return user
    
    async def list_doctors(self):
        from sqlalchemy import select
        from app.models.user import User

        result = await self.session.execute(
            select(User).where(User.role == "doctor")
        )
        return result.scalars().all()

