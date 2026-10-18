# backend/scripts/train_model.py
"""Train the price model and save it to ml_models/."""
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

CATEGORICAL = ["district", "house_type", "legal_status"]
NUMERIC = ["area_m2", "floors", "bedrooms"]
TARGET = "price_per_m2"
VERSION = "v1"

df = pd.read_csv("backend/data/listings_clean.csv")
X, y = df[CATEGORICAL + NUMERIC], df[TARGET]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = Pipeline([
    ("prep", ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL),
    ], remainder="passthrough")),
    ("reg", HistGradientBoostingRegressor(random_state=42)),
])
model.fit(X_train, y_train)

mae = mean_absolute_error(y_test, model.predict(X_test))
print(f"MAE: {mae:.1f} million VND/m²")

joblib.dump(
    {"model": model, "version": VERSION, "features": CATEGORICAL + NUMERIC, "mae": mae},
    f"ml_models/price_model_{VERSION}.joblib",
)

'''
Khi FastAPI khởi động, tải lại model đó.
bundle = joblib.load("../ml_models/price_model_v1.joblib")
model = bundle["model"]
'''

