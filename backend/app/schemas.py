from datetime import date
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field

class HouseType(str, Enum):
    ALLEY_HOUSE = "Nhà ngõ, hẻm"
    STREET_HOUSE = "Nhà mặt phố, mặt tiền"
    TOWNHOUSE = "Nhà phố liền kề"
    VILLA = "Nhà biệt thự"
class HouseFeatures(BaseModel):
    district: str
    house_type : HouseType
    area_m2 : float = Field(gt=0)
    legal_status: str | None = None
    floors : int | None = None
    bedrooms : int | None = None

class HouseFeaturesResponse(BaseModel):
    district: str
    area_m2: float
    house_type: HouseType

class PredictionOut(BaseModel):
    price_per_m2: float
    total_price: float
    model_version: str

class ListingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True) # rom_attributes=True cho phép Pydantic đọc dữ liệu từ các thuộc tính đó để tạo dữ liệu đầu ra theo ListingOut

    id: int
    posted_on: date
    district: str
    ward: str | None = None
    house_type: str
    legal_status: str | None = None
    floors: int | None = None
    bedrooms: int | None = None
    area_m2: float
    price_per_m2: float