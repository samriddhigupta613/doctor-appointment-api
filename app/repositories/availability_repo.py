from sqlalchemy import select
from app.models.availability import Availability

class AvailabilityRepository:
    def __init__(self, session):
        self.session = session

    async def create(self, availability: Availability):
        self.session.add(availability)
        await self.session.commit()
        return availability

    async def get_by_doctor(self, doctor_id: int):
        result = await self.session.execute(
            select(Availability).where(Availability.doctor_id == doctor_id)
        )
        return result.scalars().all()
