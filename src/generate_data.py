"""Generate a realistic sample purchase dataset for analysis and demos.

This script creates synthetic transaction-like data with vendors, cost centres,
products, quantities, prices, and total cost values. The output is saved to a CSV
under the repository's data folder so the other analysis scripts can read it.
"""

import pandas as pd
import numpy as np
import pathlib as path

# Directory where generated CSV files are stored.
export_dir = path.Path(__file__).parent.parent / "data"
export_dir.mkdir(exist_ok=True)

# Use a fixed random seed so the generated data is reproducible.
np.random.seed(42)

# Sample domains for realistic-looking business data.
cost_centres = [f"CC{str(i).zfill(3)}" for i in range(1, 11)]
skus = [f"SKU{str(i).zfill(4)}" for i in range(100, 200)]
vendors = [
    "Alpha Supply Co",
    "BlueLine Traders",
    "Crescent Wholesale",
    "Delta Goods",
    "Everest Imports"
]

# A small set of office and warehouse addresses with matching ZIP codes.
addresses = [
    ("101 Main St, Dallas, TX", "75201"),
    ("55 Commerce Rd, Houston, TX", "77002"),
    ("88 Industrial Ave, Austin, TX", "73301"),
    ("12 Market St, San Antonio, TX", "78205"),
    ("200 Supply Blvd, Fort Worth, TX", "76102")
]

# Create a date range to simulate transaction dates across a full year.
dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq="D")

# Number of sample rows to generate.
n = 300

# Randomly assign addresses to rows.
chosen_addresses = np.random.choice(len(addresses), n)

# Build the dataset.
df = pd.DataFrame({
    "Date": np.random.choice(dates, n),
    "CostCentre": np.random.choice(cost_centres, n),
    "SKU": np.random.choice(skus, n),
    "Vendor": np.random.choice(vendors, n),
    "Address": [addresses[i][0] for i in chosen_addresses],
    "ZipCode": [addresses[i][1] for i in chosen_addresses],
    "Quantity": np.random.randint(1, 50, n),
    "UnitPrice": np.round(np.random.uniform(5.0, 150.0, n), 2)
})

# Derive total cost from quantity and unit price.
df["TotalCost"] = df["Quantity"] * df["UnitPrice"]

# Sort by highest spend to make the dataset easier to inspect in reports.
df_sorted = df.sort_values(by=["TotalCost", "UnitPrice"], ascending=False).reset_index(drop=True)

print(df_sorted.head())
print(df_sorted.describe())

# Optional: Save to CSV for other scripts.
# df.to_csv("data/test_dataset.csv", index=False)
# print("\nSaved 300-record dataset to data/test_dataset.csv")

export_path = export_dir / "test_dataset.csv"
df_sorted.to_csv(export_path, index=False)
print(f"\nSaved sorted dataset to {export_path}")

