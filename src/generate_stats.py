"""Very small statistics demo using pandas, NumPy, and seaborn.

This file exists mainly to confirm the environment is working and to show a simple
example of generating a DataFrame, summarizing it, and plotting a quick scatter
chart.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    """Print a summary and create a basic scatter plot for two random variables."""
    print("Environment ready.")
    print("Pandas:", pd.__version__)
    print("Numpy:", np.__version__)

    # 1) Create a small sample DataFrame.
    df = pd.DataFrame({
        "A": np.random.randint(1, 100, 10),
        "B": np.random.randint(1, 100, 10)
    })

    print("\nSample DataFrame:")
    print(df)

    # 2) Show basic statistics for each column.
    print("\nSummary statistics:")
    print(df.describe())

    # 3) Plot a simple relationship between A and B.
    sns.scatterplot(data=df, x="A", y="B")
    plt.title("Scatter Plot of A vs B")
    plt.show()


if __name__ == "__main__":
    main()

