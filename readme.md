Dynamic MDX Engine & Cross-Cube Blending Guide

This repository contains a production-ready, reusable Python framework designed to abstract, generate, and blend **Multi-Dimensional Expression (MDX)** queries across multiple **IBM Planning Analytics (TM1)** cubes using `mdxpy` and `TM1py`.

---

## 🛠 Core Component: `DynamicMdxEngine`

The `DynamicMdxEngine` implements a **Fluent Builder Pattern**. This structural pattern allows you to cleanly chain programmatic configurations together to output pristine MDX syntax strings without risking structural text formatting errors.

### Key Capabilities
* **Dynamic Multi-Axis Mapping:** Seamlessly maps a single dimension string or a list of multiple nested dimensions to columns or rows.
* **Auto-Scoping Elements:** Automates underlying hierarchy mapping via functional subset boundaries (`tm1_subset_all`).
* **Tuple Filter Contextualization:** Automatically converts lists of key-value pairs into isolated multi-dimensional intersection slices for the `WHERE` clause.
* **Zero-Suppression Toggling:** Native programmatic hooks to toggle zero-suppression states (`NON EMPTY`) on an axis.

---

## 🚀 Reusable Implementation Code

Save the code below as `dynamic_mdx_builder.py` to use across your implementation pipelines:

```python
from typing import List, Union, Tuple
from mdxpy import MdxBuilder, MdxHierarchySet, MdxTuple, Member

class DynamicMdxEngine:
    """
    A reusable programmatic factory engineered to generate complex MDX queries 
    dynamically for any TM1 cube architecture layout.
    """
    def __init__(self, cube_name: str):
        self.builder = MdxBuilder(cube=cube_name)
        
    def configure_columns(self, dimensions: Union[str, List[str]], subset_name: str = "Default") -> 'DynamicMdxEngine':
        """Configures the Axis 0 (Columns) layouts dynamically."""
        dims = [dimensions] if isinstance(dimensions, str) else dimensions
        for dim in dims:
            self.builder.add_hierarchy_set_to_column_axis(
                MdxHierarchySet.tm1_subset_all(dimension=dim, hierarchy="Default")
            )
        return self

    def configure_rows(self, dimensions: Union[str, List[str]], suppress_zeros: bool = True) -> 'DynamicMdxEngine':
        """Configures Axis 1 (Rows) layouts with optional programmatic zero-suppression."""
        dims = [dimensions] if isinstance(dimensions, str) else dimensions
        axis = None
        for dim in dims:
            axis = self.builder.add_hierarchy_set_to_row_axis(
                MdxHierarchySet.tm1_subset_all(dimension=dim, hierarchy="Default")
            )
        if suppress_zeros and axis is not None:
            axis.suppress_zeroes()
        return self

    def configure_context_filter(self, filters: List[Tuple[str, str]]) -> 'DynamicMdxEngine':
        """Assembles a clean multi-dimensional slicing context tuple for the WHERE statement."""
        if filters:
            members = [Member.of(dimension=dim, element=ele) for dim, ele in filters]
            self.builder.add_tuple_to_where_clause(MdxTuple.of(*members))
        return self

    def generate(self) -> str:
        """Compiles accumulated axis and mapping metadata into a clean MDX statement."""
        return self.builder.to_mdx()
```

---

## 🔀 Advanced Blueprint: Multi-Cube Data Blending Pipeline

Because a single MDX execution statement is strictly restricted to one source cube (`FROM [Cube]`), combining data across distinct cubes must happen downstream. 

This framework bypasses TM1 architectural rule footprints by extracting isolated, coordinate-aligned snapshots from separate cubes and orchestrating an **outer-join** at the Python layer via `pandas`.

```python
import pandas as pd
from TM1py.Services import TM1Service
from dynamic_mdx_builder import DynamicMdxEngine

def execute_cross_cube_pipeline() -> pd.DataFrame:
    # 1. Instantiate the factory engine for the Sales Cube
    sales_query = (
        DynamicMdxEngine(cube_name="Sales")
        .configure_columns(dimensions="Measures", subset_name="Amount")
        .configure_rows(dimensions=["Region", "Product"], suppress_zeros=True)
        .configure_context_filter([("Year", "2026"), ("Month", "Jan")])
        .generate()
    )

    # 2. Instantiate the exact same factory layout for the Inventory Cube
    inventory_query = (
        DynamicMdxEngine(cube_name="Inventory")
        .configure_columns(dimensions="InvMeasures", subset_name="StockOnHand")
        .configure_rows(dimensions=["Region", "Product"], suppress_zeros=True)
        .configure_context_filter([("Year", "2026"), ("Month", "Jan")])
        .generate()
    )

    # 3. Stream data from separate cubes and merge on row intersections
    with TM1Service(address="localhost", port=8001, user="admin", password="pwd", ssl=True) as tm1:
        df_sales = tm1.cubes.cells.execute_mdx_dataframe(sales_query)
        df_inventory = tm1.cubes.cells.execute_mdx_dataframe(inventory_query)
        
        # Blending datasets on shared row headers 
        unified_dataset = pd.merge(
            df_sales, 
            df_inventory, 
            on=["Region", "Product"], 
            how="outer"
        )
        return unified_dataset
```

---

## 🚀 Execution & Quick Start
1. Ensure dependencies are satisfied:
   ```bash
   pip install mdxpy TM1py pandas
   ```
2. Import `DynamicMdxEngine` into your ETL pipeline script.
3. Call your builder methods using chained fluent expressions to extract and process data frames seamlessly.

---

## 🔍 Duplicate Detection Engine (Rollup duplicates)

The duplicate-detection engine that identifies leaf elements appearing in multiple specified rollups has been moved into the `mdx` package for better organization. The canonical implementation now lives at [mdx/engine.py](C:/Projects/data_analysis.worktrees/duplicate-identification-logic-update/mdx/engine.py).

To keep existing scripts and examples working with minimal changes, a thin top-level facade is provided at [tm1_mdx_dim_dupe_check.py](C:/Projects/data_analysis.worktrees/duplicate-identification-logic-update/tm1_mdx_dim_dupe_check.py) so you can import the function directly without referencing the package.

API
- find_rollup_duplicates_fast(tm1_service, dimension_name, hierarchy_name, rollups_to_check) -> Dict[str, List[str]]
  - Returns a mapping from leaf element -> sorted list of rollups that contain it (only includes leaves that appear in more than one of the specified rollups).
  - Uses in-memory traversal of hierarchy edges for speed and deduplicates rollup occurrences before returning.
  - Returns an empty dict on error (and prints a warning).

Examples

Top-level import (recommended for backward compatibility):

```python
from TM1py.Services import TM1Service
from tm1_mdx_dim_dupe_check import find_rollup_duplicates_fast

with TM1Service(address='localhost', port=8001, user='admin', password='pwd', ssl=True) as tm1:
    duplicates = find_rollup_duplicates_fast(
        tm1_service=tm1,
        dimension_name='Product',
        hierarchy_name='Product',
        rollups_to_check=['Total Europe', 'All Products']
    )
    print(duplicates)
```

Package import (explicit):

```python
from mdx.engine import find_rollup_duplicates_fast
```

Notes
- The engine output is deterministic (rollup lists are sorted) and guards against false positives by deduplicating rollup entries internally.
- If you prefer a different module name under `mdx/` (for example `duplicate_engine.py`), rename the module and update the top-level facade; I can do that if you'd like.
