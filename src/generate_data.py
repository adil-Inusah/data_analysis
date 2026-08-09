import pandas as pd
import numpy as np

# Seed for reproducibility
np.random.seed(42)

# Sample domains
cost_centres = [f"CC{str(i).zfill(3)}" for i in range(1, 11)]
skus = [f"SKU{str(i).zfill(4)}" for i in range(100, 200)]
vendors = [
    "Alpha Supply Co",
    "BlueLine Traders",
    "Crescent Wholesale",
    "Delta Goods",
    "Everest Imports"
]

# Addresses paired with realistic ZIP codes
addresses = [
    ("101 Main St, Dallas, TX", "75201"),
    ("55 Commerce Rd, Houston, TX", "77002"),
    ("88 Industrial Ave, Austin, TX", "73301"),
    ("12 Market St, San Antonio, TX", "78205"),
    ("200 Supply Blvd, Fort Worth, TX", "76102")
]

# Generate dates
dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq="D")

# Number of records
n = 300

# Random selections
chosen_addresses = np.random.choice(len(addresses), n)

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

# Total cost
df["TotalCost"] = df["Quantity"] * df["UnitPrice"]

print(df.head())

# Optional: Save to CSV
#df.to_csv("data/test_dataset.csv", index=False)
#print("\nSaved 300‑record dataset to data/test_dataset.csv")
