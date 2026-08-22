"""Backward-compatible entry point for the basic MDX example.

This file remains in the repo root so older scripts continue to work, while the
actual implementation now lives under the mdx/ package.
"""

from examples.basic_mdx_example import complex_query


if __name__ == "__main__":
    print(complex_query)
