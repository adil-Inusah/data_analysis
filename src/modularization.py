"""Simple text-analysis workflow split into reusable helper functions.

This module demonstrates a clean, modular pattern for reading text files,
normalizing content, tokenizing it, counting word frequencies, and returning the
most common words. It is intentionally small and easy to follow for teaching or
quick prototyping.
"""

import numpy as np
import pathlib as path

# Folder used for exported or generated data files.
export_dir = path.Path(__file__).parent.parent / "data"
print(f"Export directory: {export_dir}")

# file_path = export_dir / "test_dataset.csv"
# print(f"File path: {file_path}")

# ---------------------------------------------------------------------------
# Helper functions (small, well-scoped operations used by the workflow)
# ---------------------------------------------------------------------------


def load_text(file_path):
    """Read raw text from a file and return it as a string."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


# raise NotImplementedError("This module is a placeholder for modularized functions. Please implement the required functionality.")


def clean_text(text):
    """Lowercase the text and normalize repeated whitespace into single spaces."""
    return " ".join(text.lower().split())


def tokenize(text):
    """Split a text string into a list of words."""
    return text.split(" ")


def count_words(tokens):
    """Count occurrences of each word in a token list."""
    freq = {}
    for t in tokens:
        freq[t] = freq.get(t, 0) + 1
    return freq


def summarize(freq_dict, top_n=5):
    """Return the most frequent words, sorted by count descending."""
    sorted_items = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)
    return sorted_items[:top_n]


# ---------------------------------------------------------------------------
# Main workflow (higher-level orchestration)
# ---------------------------------------------------------------------------

def analyze_text(file_path):
    """Read, clean, tokenize, count, and summarize text in one workflow."""
    raw = load_text(file_path)
    cleaned = clean_text(raw)
    tokens = tokenize(cleaned)
    freq = count_words(tokens)
    summary = summarize(freq)
    return summary


# ---------------------------------------------------------------------------
# Example usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    file_path = export_dir / "test_dataset.csv"
    result = analyze_text(file_path)
    print("Top words:", result)
