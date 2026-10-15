from fastapi import FastAPI, HTTPException

app = FastAPI(title="HanoiHouse API")

LISTINGS = [
    {"id": 1, "district": "Quận Cầu Giấy", "area_m2": 46, "price_per_m2": 86.96},
    {"id": 2, "district": "Quận Thanh Xuân", "area_m2": 37, "price_per_m2": 116.22},
    {"id": 3, "district": "Quận Hai Bà Trưng", "area_m2": 40, "price_per_m2": 65.0},
]

@app.get("/")
def root():
    return {"mesesage": "Welcome to HanoiHouse"}

@app.get("/listings")
def list_listings(district: str | None = None, limit: int = 10):
    results = LISTINGS
    if district:
        results = [item for item in results if item["district"] == district]
    return results[:limit]

@app.get("/listings/{listing_id}")
def get_listing(listing_id: int):
    for item in LISTINGS:
        if item["id"] == listing_id:
            return item
    raise HTTPException(status_code=404, detail="Listing not found") 

@app.get("/listings")
def list_listing(district: str | None = None, min_price: float | None = None, limit: int = 10):
    results = LISTINGS
    if district:
        results = [item for item in results if item["district"] == district]
    if min_price:
        results = [item for item in results if item["price_per_m2"] >= min_price]
    return results[:limit]

