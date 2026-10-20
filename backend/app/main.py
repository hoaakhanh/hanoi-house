# backend/app/main.py

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.ml import PriceModel
from backend.app.routers import listings, predict


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Tải mô hình ML khi ứng dụng khởi động
    model_path = (
        Path(__file__).resolve().parents[2]
        / "ml_models"
        / "price_model_v1.joblib"
    )

    app.state.price_model = PriceModel(str(model_path))

    yield


# Khởi tạo ứng dụng FastAPI
app = FastAPI(
    title="HanoiHouse API",
    lifespan=lifespan
)


# Cấu hình CORS cho frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Đăng ký các router
app.include_router(listings.router)
app.include_router(predict.router)


# Endpoint kiểm tra ứng dụng
@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_version": app.state.price_model.version
    }

