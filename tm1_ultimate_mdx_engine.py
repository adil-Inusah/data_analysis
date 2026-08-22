"""Compatibility wrapper for the advanced MDX builder.

The implementation now lives under the mdx/ package. This root-level file exists so
existing imports continue to work while the repo is organized into clearer
package directories.
"""

from mdx.tm1_ultimate_mdx_engine import UltimateMdxEngine

__all__ = ["UltimateMdxEngine"]
