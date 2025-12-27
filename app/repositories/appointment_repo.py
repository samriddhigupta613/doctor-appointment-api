from sqlalchemy import select, and_
from app.models.appointment import Appointment

class AppointmentRepository:
    def __init__(self, session):
        self.session = session

    async def is_conflict(self, doctor_id, start, end):
        result = await self.session.execute(
            select(Appointment).where(
                and_(
                    Appointment.doctor_id == doctor_id,
                    Appointment.start_time < end,
                    Appointment.end_time > start,
                )
            )
        )
        return result.scalar_one_or_none()

    async def create(self, appointment: Appointment):
        self.session.add(appointment)
        await self.session.commit()
        return appointment
