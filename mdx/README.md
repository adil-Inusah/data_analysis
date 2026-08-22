Duplicate Detection Engine (mdx/engine.py)

This folder contains the in-memory duplicate-detection implementation for dimension rollups.

File: engine.py
- find_rollup_duplicates_fast(tm1_service, dimension_name, hierarchy_name, rollups_to_check) -> Dict[str, List[str]]
  - Traverses the dimension hierarchy using a single bulk call to tm1_service.elements.get_edges
  - Builds an in-memory parent->children tree and resolves level-0 leaves for each target rollup
  - Deduplicates rollup memberships and returns deterministic sorted lists for stable output

Notes:
- The top-level module `tm1_mdx_dim_dupe_check.py` re-exports the function for backward compatibility.
- Consider naming this module `duplicate_engine.py` if you want a clearer surface name; rename both the file and the facade when ready.
