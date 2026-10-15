"""Clean the raw Kaggle CSV into data/listings_clean.csv."""
import pandas as pd

RAW = "data/VN_housing_dataset.csv"
OUT = "data/listings_clean.csv"

COLUMNS = {
    "Ngày": "posted_on",
    "Quận": "district",
    "Huyện": "ward",
    "Loại hình nhà ở": "house_type",
    "Giấy tờ pháp lý": "legal_status",
    "Số tầng": "floors",
    "Số phòng ngủ": "bedrooms",
    "Diện tích": "area_m2",
    "Giá/m2": "price_raw",
}


def parse_price(text: str) -> float | None:
    """'86,96 triệu/m²' -> 86.96 (million VND per m²)."""
    if not isinstance(text, str):
        return None
    number, unit = text.split(" ", 1)
    value = float(number.replace(".", "").replace(",", "."))
    if unit.startswith("triệu"):
        return value
    if unit.startswith("tỷ"):
        return value * 1000
    return None  # 'đ/m²' rows are data-entry errors


def parse_count(text) -> float | None:
    """'5 phòng' -> 5, 'nhiều hơn 10 phòng' / 'Nhiều hơn 10' -> 11."""
    if not isinstance(text, str):
        return None
    if text.lower().startswith("nhiều hơn"):
        return 11
    return float(text.split()[0])


def clean(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw[list(COLUMNS)].rename(columns=COLUMNS)

    df["price_per_m2"] = df["price_raw"].map(parse_price)
    df["area_m2"] = df["area_m2"].str.replace(" m²", "").astype(float)
    df["bedrooms"] = df["bedrooms"].map(parse_count)
    df["floors"] = df["floors"].map(parse_count)
    df["posted_on"] = pd.to_datetime(df["posted_on"]).dt.date

    df = df.dropna(subset=["district", "house_type", "price_per_m2", "area_m2"])
    df = df[df["price_per_m2"].between(10, 1000) & df["area_m2"].between(10, 500)]
    df.loc[df["floors"] > 11, "floors"] = None  # e.g. 45 floors for a house

    return df.drop(columns="price_raw").drop_duplicates()


if __name__ == "__main__":
    raw = pd.read_csv(RAW)
    df = clean(raw)
    df.to_csv(OUT, index=False)
    print(f"{len(raw)} raw rows -> {len(df)} clean rows")
    