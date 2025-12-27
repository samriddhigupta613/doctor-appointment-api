from fastapi import APIRouter, Depends
from app.core.dependencies import require_role
from app.schemas.availability import AvailabilityCreate
from app.models.availability import Availability
from app.repositories.availability_repo import AvailabilityRepository
from app.db.session import AsyncSessionLocal

router = APIRouter(prefix="/doctors", tags=["Doctors"])


@router.post("/availability")
async def set_availability(
    data: AvailabilityCreate,
    user=Depends(require_role("doctor")),
):
    async with AsyncSessionLocal() as session:
        repo = AvailabilityRepository(session)
        availability = Availability(
            doctor_id=user["id"],
            start_time=data.start_time,
            end_time=data.end_time,
        )
        return await repo.create(availability)


@router.get("/{doctor_id}/availability")
async def view_availability(doctor_id: int):
    async with AsyncSessionLocal() as session:
        repo = AvailabilityRepository(session)
        return await repo.get_by_doctor(doctor_id)


@router.get("")
async def list_doctors():
    from app.repositories.user_repo import UserRepository
    async with AsyncSessionLocal() as session:
        repo = UserRepository(session)
        return await repo.list_doctors()
