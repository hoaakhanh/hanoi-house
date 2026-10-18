import joblib
import pandas as pd

from backend.app.schemas import HouseFeatures


class PriceModel:
    def __init__(self, path: str):
        bundle = joblib.load(path)

        self.pipeline = bundle["model"]
        self.version = bundle["version"]
        self.features = bundle["features"]

    def predict(self, house: HouseFeatures) -> float:
        row = pd.DataFrame(
            [house.model_dump(mode="json")]
        )[self.features]

        return float(self.pipeline.predict(row)[0])