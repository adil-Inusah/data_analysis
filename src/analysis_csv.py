from pathlib import Path
import pandas as pd

def review_csv():
    # ---------------------------------------------------------
    # 1. Locate the CSV file
    # ---------------------------------------------------------
    csv_path = Path(r"C:\Projects\data_analysis\data\test_dataset.csv")

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found at: {csv_path}")

    print(f"Loading dataset from: {csv_path}\n")

    # ---------------------------------------------------------
    # 2. Load the CSV
    # ---------------------------------------------------------
    df = pd.read_csv(csv_path)

    # ---------------------------------------------------------
    # 3. Basic shape
    # ---------------------------------------------------------
    print("=== Dataset Shape ===")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}\n")

    # ---------------------------------------------------------
    # 4. Column overview
    # ---------------------------------------------------------
    print("=== Columns ===")
    print(df.columns.tolist(), "\n")

    # ---------------------------------------------------------
    # 5. Head & Tail
    # ---------------------------------------------------------
    print("=== First 5 Rows ===")
    print(df.head(), "\n")

    print("=== Last 5 Rows ===")
    print(df.tail(), "\n")

    # ---------------------------------------------------------
    # 6. Missing values
    # ---------------------------------------------------------
    print("=== Missing Values ===")
    print(df.isna().sum(), "\n")

    # ---------------------------------------------------------
    # 7. Descriptive statistics
    # ---------------------------------------------------------
    print("=== Descriptive Statistics ===")
    cols_to_review = ["TotalCost", "UnitPrice", "Quantity"]
    print(df[cols_to_review].describe(), "\n")


    # ---------------------------------------------------------
    # 8. Sort by TotalCost and UnitPrice
    # ---------------------------------------------------------
    print("=== Sorted by TotalCost, UnitPrice (ascending) ===")
    df_sorted = df.sort_values(by=["TotalCost", "UnitPrice"], ascending=[True, True])
    print(df_sorted.head(), "\n")

    # ---------------------------------------------------------
    # 9. Top 10 most expensive rows
    # ---------------------------------------------------------
    print("=== Top 10 Most Expensive ===")
    print(df.nlargest(10, "TotalCost"), "\n")

    # ---------------------------------------------------------
    # 10. Summary by Vendor
    # ---------------------------------------------------------
    print("=== Total Cost by Vendor ===")
    vendor_summary = df.groupby("Vendor")["TotalCost"].sum().sort_values(ascending=False)
    print(vendor_summary, "\n")

    print("Review complete.")

if __name__ == "__main__":
    review_csv()
