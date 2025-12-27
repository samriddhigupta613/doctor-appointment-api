from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Availability(Base):
    __tablename__ = "availabilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    doctor_id: Mapped[int]
    start_time: Mapped[datetime]
    end_time: Mapped[datetime]
