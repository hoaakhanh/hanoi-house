from fastapi import FastAPI, HTTPException

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi.middleware.cors import CORSMiddleware

from backend.app.ml import PriceModel
from backend.app.schemas import HouseFeatures, HouseFeaturesResponse, PredictionOut

app = FastAPI(title="HanoiHouse API")

@app.get("/")
def root():
    return {"mesesage": "Welcome to HanoiHouse"}

@asynccontextmanager
async def lifespan(app: FastAPI):
    model_path = Path(__file__).resolve().parents[2] / "ml_models" / "price_model_v1.joblib"
    app.state.price_model = PriceModel(str(model_path))
    yield

app = FastAPI(
    title="HanoiHouse API",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5501",
        "http://localhost:5501",
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