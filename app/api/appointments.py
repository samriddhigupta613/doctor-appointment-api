from fastapi import APIRouter, Depends, HTTPException
from app.core.dependencies import require_role
from app.schemas.appointment import AppointmentCreate
from app.models.appointment import Appointment
from app.repositories.appointment_repo import AppointmentRepository
from app.repositories.availability_repo import AvailabilityRepository
from app.db.session import AsyncSessionLocal

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.post("")
async def book_appointment(
    data: AppointmentCreate,
    user=Depends(require_role("patient")),
):
    async with AsyncSessionLocal() as session:
        availability_repo = AvailabilityRepository(session)
        appointment_repo = AppointmentRepository(session)

        slots = await availability_repo.get_by_doctor(data.doctor_id)
        valid = any(
            slot.start_time <= data.start_time and slot.end_time >= data.end_time
            for slot in slots
        )

        if not valid:
            raise HTTPException(status_code=400, detail="Outside availability")

        if await appointment_repo.is_conflict(
            data.doctor_id, data.start_time, data.end_time
        ):
            raise HTTPException(status_code=400, detail="Time slot already booked")

        appointment = Appointment(
            doctor_id=data.doctor_id,
            patient_id=user["id"],
            start_time=data.start_time,
            end_time=data.end_time,
        )

        return await appointment_repo.create(appointment)

@router.delete("/{appointment_id}")
async def cancel_appointment(
    appointment_id: int,
    user=Depends(require_role("patient")),
):
    from sqlalchemy import select
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Appointment).where(
                Appointment.id == appointment_id,
                Appointment.patient_id == user["id"],
            )
        )
        appointment = result.scalar_one_or_none()
        if not appointment:
            raise HTTPException(status_code=404)

        await session.delete(appointment)
        await session.commit()
        return {"status": "cancelled"}
