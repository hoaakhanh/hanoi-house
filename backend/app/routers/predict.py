# API dự đoán giá nhà
# backend/app/routers/predict.py

from fastapi import APIRouter

from backend.app.deps import Model
from backend.app.schemas import HouseFeatures, PredictionOut


# Tạo router dành cho API dự đoán
router = APIRouter(
    tags=["predictions"]
)


@router.post("/predict", response_model=PredictionOut)
def predict(
    house: HouseFeatures,
    model: Model
):
    price_per_m2 = round(model.predict(house), 2)

    return PredictionOut(
        price_per_m2=price_per_m2,
        total_price=round(
            price_per_m2 * house.area_m2 / 1000,
            2
        ),
        model_version=model.version,
    )