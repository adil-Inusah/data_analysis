import numpy as np
import pathlib as path

export_dir = path.Path(__file__).parent.parent / "data"
print(f"Export directory: {export_dir}")

#file_path = export_dir / "test_dataset.csv"
#print(f"File path: {file_path}")

# -----------------------------
# Helper Functions (Modularized)
# -----------------------------

def load_text(file_path):
    """Read text from a file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

#raise NotImplementedError("This module is a placeholder for modularized functions. Please implement the required functionality.")

def clean_text(text):
    """Normalize whitespace and lowercase the text."""
    return " ".join(text.lower().split())


def tokenize(text):
    """Split text into words."""
    return text.split(" ")


def count_words(tokens):
    """Return a dictionary of word frequencies."""
    freq = {}
    for t in tokens:
        freq[t] = freq.get(t, 0) + 1
    return freq


def summarize(freq_dict, top_n=5):
    """Return the top N most frequent words."""
    sorted_items = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)
    return sorted_items[:top_n]

# -----------------------------
# Main Function (High-Level Flow)
# -----------------------------

def analyze_text(file_path):
    """High-level workflow using helper functions."""
    raw = load_text(file_path)
    cleaned = clean_text(raw)
    tokens = tokenize(cleaned)
    freq = count_words(tokens)
    summary = summarize(freq)
    return summary

# -----------------------------
# Example Usage
# -----------------------------
if __name__ == "__main__":
    file_path = export_dir / "test_dataset.csv"
    result = analyze_text(file_path)
    print("Top words:", result)
