import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    print("Environment ready.")
    print("Pandas:", pd.__version__)
    print("Numpy:", np.__version__)

    # Create a sample DataFrame
    df = pd.DataFrame({
        "A": np.random.randint(1, 100, 10),
        "B": np.random.randint(1, 100, 10)
    })

    print("\nSample DataFrame:")
    print(df)

    # Basic statistics
    print("\nSummary statistics:")
    print(df.describe())

    # Simple visualization
    sns.scatterplot(data=df, x="A", y="B")
    plt.title("Scatter Plot of A vs B")
    plt.show()

if __name__ == "__main__":
    main()

