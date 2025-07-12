import pandas as pd
import plotly.express as px
from pathlib import Path

# Load data
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
df = pd.read_csv(DATA_DIR / "sunburst_data.csv")

# Create sunburst chart
fig = px.sunburst(
    df,
    path=["region", "category", "subcategory"],
    values="value",
    title="Multi-Level Sunburst Chart of Business Categories"
)

# Export as HTML
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
fig.write_html(OUTPUT_DIR / "golden_image.html")

print("Dashboard created at outputs/golden_image.html")

