import pandas as pd

from sqlalchemy.orm import Session

from backend.app.database import engine
from backend.app.models import Listing


# 1. Đọc dữ liệu đã làm sạch
csv_path = "backend/data/listings_clean.csv"
df = pd.read_csv(csv_path)

# 2. Chuyển NaN của Pandas thành None của Python
df = df.astype(object).where(pd.notna(df), None)

# 3. Chuyển từng dòng thành đối tượng Listing
records = df.to_dict(orient="records")
listings = [Listing(**record) for record in records]

# 4. Thêm dữ liệu vào PostgreSQL
with Session(engine) as session:
    session.add_all(listings)
    session.commit()

print(f"Đã import {len(listings)} bản ghi.")
