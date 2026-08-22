"""Top-level facade for the duplicate-detection engine.

This module re-exports the implementation that lives inside the `mdx` package so
existing code can continue to import the function as a top-level module.
"""

from mdx.tm1_mdx_dim_dupe_check import find_rollup_duplicates_fast

__all__ = ["find_rollup_duplicates_fast"]
