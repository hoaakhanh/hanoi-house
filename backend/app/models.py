# Định nghĩa các bảng database bằng SQLAlchemy
from datetime import date

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database import Base

class Listing(Base):
    __tablename__ = "listings"

    id: Mapped[int] = mapped_column(primary_key=True)
    posted_on: Mapped[date]
    district: Mapped[str] = mapped_column(String(50), index=True)
    ward: Mapped[str | None] = mapped_column(String(50))
    house_type: Mapped[str] = mapped_column(String(50))
    legal_status: Mapped[str | None] = mapped_column(String(50))
    floors: Mapped[int | None]
    bedrooms: Mapped[int | None]
    area_m2: Mapped[float]
    price_per_m2: Mapped[float] = mapped_column(index=True)