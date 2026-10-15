from enum import Enum
from pydantic import BaseModel, Field

class HouseType(str, Enum):
    PRIVATE_HOUSE = "Nhà riêng"
    APARTMENT = "Chung cư"
    VILLA = "Biệt thự"
class HouseFeatures(BaseModel):
    district: str
    house_type : HouseType
    area_m2 : float = Field(gt=0)
    floors : int | None = None
    bedrooms : int | None = None

class HouseFeaturesResponse(BaseModel):
    district: str
    area_m2: float
    house_type: HouseType