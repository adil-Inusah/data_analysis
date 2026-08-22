"""Backward-compatible entry point for the advanced MDX example.

This file remains in the repo root so older scripts continue to work, while the
actual implementation now lives under the mdx/ package.
"""

from examples.advanced_mdx_example import mdx_statement


if __name__ == "__main__":
    print(mdx_statement)
