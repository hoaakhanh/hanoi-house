# Gom các dependency dùng chung
# backend/app/deps.py

from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.ml import PriceModel


# Dependency dùng chung cho database
DbSession = Annotated[Session, Depends(get_db)]


# Lấy mô hình Machine Learning từ ứng dụng FastAPI
def get_price_model(request: Request) -> PriceModel:
    return request.app.state.price_model


# Dependency dùng chung cho mô hình Machine Learning
Model = Annotated[PriceModel, Depends(get_price_model)]