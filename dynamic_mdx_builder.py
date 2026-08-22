"""Compatibility wrapper for the lightweight MDX builder.

The implementation now lives under the mdx/ package. This root-level file exists so
existing imports keep working while the project structure is cleaned up.
"""

from mdx.dynamic_mdx_builder import DynamicMdxEngine

__all__ = ["DynamicMdxEngine"]
