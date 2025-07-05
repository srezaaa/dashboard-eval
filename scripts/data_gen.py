import os
from pathlib import Path
import numpy as np
import pandas as pd

np.random.seed(42)
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

regions = ["North", "South", "East", "West"]
cities_per_region = {
    "North": ["Toronto", "Ottawa", "Montreal"],
    "South": ["Houston", "Dallas", "Miami"],
    "East": ["New York", "Boston", "Philadelphia"],
    "West": ["Los Angeles", "San Francisco", "Seattle"],
}
product_lines = ["A", "B", "C"]
start = "2024-01-01"
end = "2024-12-31"
daily_index = pd.date_range(start, end, freq="D")

def seasonal_multiplier(dates):
    month = dates.month.to_numpy()
    return 1 + 0.15 * np.cos((month - 1) / 12 * 2 * np.pi) + 0.25 * (month >= 10)

def gen_store_daily(store_id, city, region):
    base = 100 + 15 * np.random.randn(len(daily_index))
    season = seasonal_multiplier(daily_index)
    noise = np.random.randn(len(daily_index)) * 8
    revenue = np.maximum(base * season + noise, 0).round(2)
    units = (revenue * np.random.uniform(9, 12) / 100).astype(int)
    df = pd.DataFrame(
        {
            "date": daily_index,
            "store_id": store_id,
            "city": city,
            "region": region,
            "product_line": np.random.choice(product_lines, len(daily_index)),
            "revenue_kUSD": revenue,
            "units_sold": units,
        }
    )
    return df

store_frames = []
store_counter = 1
for reg in regions:
    for city in cities_per_region[reg]:
        store_frames.append(gen_store_daily(f"S{store_counter:03d}", city, reg))
        store_counter += 1

local_sales = pd.concat(store_frames, ignore_index=True)
local_sales.to_csv(DATA_DIR / "local_sales_data.csv", index=False)

local_sales["month"] = local_sales["date"].dt.to_period("M").dt.to_timestamp()

monthly = (
    local_sales.groupby(["month", "region", "product_line"], as_index=False)
    .agg(
        revenue_kUSD=("revenue_kUSD", "sum"),
        units_sold=("units_sold", "sum"),
    )
)
monthly.to_csv(DATA_DIR / "sales_data.csv", index=False)

print("Data generation complete.")

