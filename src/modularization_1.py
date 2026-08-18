import pandas as pd
from pathlib import Path

def load_text(file_path: Path) -> str:
    """Read raw text from a file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def load_csv(file_path: Path) -> pd.DataFrame:
    """Load a CSV into a DataFrame."""
    return pd.read_csv(file_path)

def export_csv(df: pd.DataFrame, file_path: Path):
    """Export DataFrame to CSV."""
    df.to_csv(file_path, index=False)

def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Lowercase and strip column names."""
    df.columns = df.columns.str.strip().str.lower()
    return df

def drop_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows with missing values."""
    return df.dropna()

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Apply all standard cleaning steps."""
    df = standardize_columns(df)
    df = drop_missing(df)
    return df


def compute_stats(df: pd.DataFrame, column: str) -> dict:
    """Return basic statistics for a column."""
    return {
        "mean": df[column].mean(),
        "median": df[column].median(),
        "std": df[column].std(),
        "min": df[column].min(),
        "max": df[column].max(),
    }


def normalize(df: pd.DataFrame, column: str, new_col: str) -> pd.DataFrame:
    """Normalize a column to 0–1 range."""
    col = df[column]
    df[new_col] = (col - col.min()) / (col.max() - col.min())
    return df

def add_ratio(df: pd.DataFrame, num_col: str, denom_col: str, new_col: str) -> pd.DataFrame:
    """Create a ratio column."""
    df[new_col] = df[num_col] / df[denom_col]
    return df


def plot_hist(df: pd.DataFrame, column: str):
    """Plot a histogram for a column."""
    df[column].hist()
    plt.title(f"Histogram of {column}")
    plt.show()


from pathlib import Path
from helpers.io import load_csv, export_csv
from helpers.cleaning import clean_dataframe
from helpers.stats import compute_stats
from helpers.transforms import normalize

def process_csv(file_path: Path):
    df = load_csv(file_path)
    df = clean_dataframe(df)

    stats = compute_stats(df, "sales")
    print("Sales stats:", stats)

    df = normalize(df, "sales", "sales_norm")

    export_csv(df, file_path.parent / "cleaned_output.csv")
