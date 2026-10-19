from fastapi import FastAPI, HTTPException, Depends

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from typing import Annotated

from backend.app.ml import PriceModel
from backend.app.schemas import HouseFeatures, HouseFeaturesResponse, PredictionOut
from backend.app.database import get_db
from backend.app.models import Listing
from backend.app.schemas import ListingOut

@asynccontextmanager
async def lifespan(app: FastAPI):
    model_path = Path(__file__).resolve().parents[2] / "ml_models" / "price_model_v1.joblib"
    app.state.price_model = PriceModel(str(model_path))
    yield

app = FastAPI(
    title="HanoiHouse API",
    lifespan=lifespan # lifespan có nhiệm vụ tải mô hình Machine Learning khi ứng dụng khởi động
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict", response_model=PredictionOut)
def predict(house: HouseFeatures):
    model = app.state.price_model

    price_per_m2 = round(model.predict(house), 2)

    return PredictionOut(
        price_per_m2=price_per_m2,
        total_price=round(price_per_m2 * house.area_m2 / 1000, 2),
        model_version=model.version,
    )

@app.get("/listings/{listing_id}", response_model=ListingOut)
def get_listing(
    listing_id: int,
    db: Annotated[Session, Depends(get_db)]
):
    house = db.get(Listing, listing_id)

    if house is None:
        raise HTTPException(
            status_code=404,
            detail="Listing not found"
        )

    return house

