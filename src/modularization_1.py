"""Reusable data-cleaning and transformation helpers.

This file mixes low-level pandas utilities with a higher-level CSV processing flow.
It is a useful example of how to break a data pipeline into small functions so each
step can be tested, reused, and combined in different ways.
"""

"""Reusable data-cleaning and transformation helpers.

This file mixes low-level pandas utilities with a higher-level CSV processing flow.
It is a useful example of how to break a data pipeline into small functions so each
step can be tested, reused, and combined in different ways.
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ---------------------------------------------------------------------------
# Low-level file and DataFrame helpers
# ---------------------------------------------------------------------------


def load_text(file_path: Path) -> str:
    """Read raw text from a file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def load_csv(file_path: Path) -> pd.DataFrame:
    """Load a CSV file into a pandas DataFrame."""
    return pd.read_csv(file_path)


def export_csv(df: pd.DataFrame, file_path: Path):
    """Write a DataFrame to disk as a CSV without the index column."""
    df.to_csv(file_path, index=False)


# ---------------------------------------------------------------------------
# Data cleaning helpers
# ---------------------------------------------------------------------------


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Strip whitespace and lowercase every column name for consistency."""
    df.columns = df.columns.str.strip().str.lower()
    return df


def drop_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Remove any row containing missing values."""
    return df.dropna()


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Apply the standard column-cleaning and missing-value workflow."""
    df = standardize_columns(df)
    df = drop_missing(df)
    return df


# ---------------------------------------------------------------------------
# Summary and transform helpers
# ---------------------------------------------------------------------------


def compute_stats(df: pd.DataFrame, column: str) -> dict:
    """Return common summary statistics for a single numeric column."""
    return {
        "mean": df[column].mean(),
        "median": df[column].median(),
        "std": df[column].std(),
        "min": df[column].min(),
        "max": df[column].max(),
    }


def normalize(df: pd.DataFrame, column: str, new_col: str) -> pd.DataFrame:
    """Scale a numeric column into the 0-to-1 range."""
    col = df[column]
    df[new_col] = (col - col.min()) / (col.max() - col.min())
    return df


def add_ratio(df: pd.DataFrame, num_col: str, denom_col: str, new_col: str) -> pd.DataFrame:
    """Create a new column by dividing one value by another."""
    df[new_col] = df[num_col] / df[denom_col]
    return df


def plot_hist(df: pd.DataFrame, column: str):
    """Plot a histogram for a selected column."""
    df[column].hist()
    plt.title(f"Histogram of {column}")
    plt.show()


# ---------------------------------------------------------------------------
# Example high-level pipeline
# ---------------------------------------------------------------------------
# The imports below show the intended project structure if these helpers were
# split across modules such as helpers/io.py, helpers/cleaning.py, etc.
from helpers.io import load_csv, export_csv
from helpers.cleaning import clean_dataframe
from helpers.stats import compute_stats
from helpers.transforms import normalize


def process_csv(file_path: Path):
    """Run a simple pipeline: load, clean, summarize, normalize, and export."""
    df = load_csv(file_path)
    df = clean_dataframe(df)

    stats = compute_stats(df, "sales")
    print("Sales stats:", stats)

    df = normalize(df, "sales", "sales_norm")

    export_csv(df, file_path.parent / "cleaned_output.csv")
