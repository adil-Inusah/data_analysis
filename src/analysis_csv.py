"""Quick CSV review script for an operational dataset.

This file is a lightweight data-quality and exploratory analysis script. It opens a
CSV file, prints the key properties of the dataset, checks for missing values, and
shows a few useful summaries such as top rows, sorting, and vendor totals.
"""

from pathlib import Path
import pandas as pd


def review_csv():
    """Inspect a CSV file and print a useful summary of the dataset."""

    # 1) Locate the source file.
    # The CSV lives in the repo's sibling data folder; we fail early if it is missing.
    csv_path = Path(r"C:\Projects\data_analysis\data\test_dataset.csv")

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found at: {csv_path}")

    print(f"Loading dataset from: {csv_path}\n")

    # 2) Read the file into a DataFrame.
    df = pd.read_csv(csv_path)

    # 3) Basic dataset shape and schema.
    print("=== Dataset Shape ===")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}\n")

    print("=== Columns ===")
    print(df.columns.tolist(), "\n")

    # 4) Show the beginning and end of the dataset to confirm content layout.
    print("=== First 5 Rows ===")
    print(df.head(), "\n")

    print("=== Last 5 Rows ===")
    print(df.tail(), "\n")

    # 5) Check for missing values before any modeling or reporting.
    print("=== Missing Values ===")
    print(df.isna().sum(), "\n")

    # 6) Summarize numeric columns to understand distribution and scale.
    print("=== Descriptive Statistics ===")
    cols_to_review = ["TotalCost", "UnitPrice", "Quantity"]
    print(df[cols_to_review].describe(), "\n")

    # 7) Sort by cost to highlight lower-cost and higher-cost records.
    print("=== Sorted by TotalCost, UnitPrice (ascending) ===")
    df_sorted = df.sort_values(by=["TotalCost", "UnitPrice"], ascending=[True, True])
    print(df_sorted.head(), "\n")

    # 8) Identify the most expensive purchases in the dataset.
    print("=== Top 10 Most Expensive ===")
    print(df.nlargest(10, "TotalCost"), "\n")

    # 9) Aggregate by vendor to understand spend concentration.
    print("=== Total Cost by Vendor ===")
    vendor_summary = df.groupby("Vendor")["TotalCost"].sum().sort_values(ascending=False)
    print(vendor_summary, "\n")

    print("Review complete.")


if __name__ == "__main__":
    review_csv()
