import os
import numpy as np
import pandas as pd
from pathlib import Path

# Set up data directory
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Create hierarchical category data
np.random.seed(42)

categories = {
    "Electronics": ["Phones", "Computers", "TVs"],
    "Clothing": ["Men", "Women", "Children"],
    "Home": ["Kitchen", "Furniture", "Decor"],
}

regions = ["North America", "Europe", "Asia"]

data = []

for region in regions:
    for parent, subs in categories.items():
        for sub in subs:
            value = np.random.randint(100, 1000)
            data.append([region, parent, sub, value])

df = pd.DataFrame(data, columns=["region", "category", "subcategory", "value"])
df.to_csv(DATA_DIR / "sunburst_data.csv", index=False)
print("sunburst_data.csv generated in /data")

