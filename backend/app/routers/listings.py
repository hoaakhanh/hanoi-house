# Các API liên quan đến tin đăng nhà
from typing import Annotated, Literal

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select, func

from backend.app.deps import DbSession
from backend.app.models import Listing
from backend.app.schemas import ListingOut, ListingPage, DistrictStats


# Tạo router dành cho các API tin đăng
router = APIRouter(
    prefix="/listings",
    tags=["listings"]
)


@router.get("/{listing_id}", response_model=ListingOut)
def get_listing(
    listing_id: int,
    db: DbSession
):
    house = db.get(Listing, listing_id)

    if house is None: # Nếu không kiểm tra, API có thể trả về None thay vì thông báo lỗi rõ ràng khi ID không tồn tại.
        raise HTTPException(
            status_code=404,
            detail="Listing not found"
        )

    return house

@router.get("", response_model=ListingPage)
def list_listings(
    db: DbSession,
    district: str | None = None,
    house_type: str | None = None,
    min_price: Annotated[float | None, Query(ge=0)] = None,
    max_price: Annotated[float | None, Query(ge=0)] = None,
    sort: Literal["price_asc", "price_desc", "newest"] = "newest",
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 20,
):
    query = select(Listing)
    if district:
        query = query.where(Listing.district == district)
    if house_type:
        query = query.where(Listing.house_type == house_type)
    if min_price is not None:
        query = query.where(Listing.price_per_m2 >= min_price)
    if max_price is not None:
        query = query.where(Listing.price_per_m2 <= max_price)

    total = db.scalar(select(func.count()).select_from(query.subquery()))

    order = {
        "price_asc": Listing.price_per_m2.asc(),
        "price_desc": Listing.price_per_m2.desc(),
        "newest": Listing.posted_on.desc(),
    }[sort]
    items = db.scalars(
        query
        .order_by(order, Listing.id)
        .offset((page - 1) * size)
        .limit(size)
    ).all()

    return ListingPage(items=items, total=total, page=page, size=size)

@router.get("/stats/districts", response_model=list[DistrictStats])
def district_stats(db: DbSession, min_listings: int = 50):
    rows = db.execute(
        select(
            Listing.district,
            func.count().label("listings"),
            func.avg(Listing.price_per_m2).label("avg_price_per_m2"),
        )
        .group_by(Listing.district)
        .having(func.count() >= min_listings)
        .order_by(func.avg(Listing.price_per_m2).desc())
    ).all()
    return [DistrictStats.model_validate(row, from_attributes=True) for row in rows]