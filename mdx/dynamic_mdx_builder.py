"""Simple fluent MDX builder for a single TM1 cube.

This module is intentionally lightweight: it turns a few high-level inputs
(dimensions, filters, and axis settings) into a clean MDX SELECT statement.
It is useful when you want a readable, easy-to-use wrapper around mdxpy without
managing all of the deeper TM1-specific configuration details.
"""

from mdxpy import MdxBuilder, MdxHierarchySet, Member
from typing import Union, List, Tuple


class DynamicMdxEngine:
    """Build a basic OLAP query by chaining dimension and filter configuration.

    Example:
        query = (
            DynamicMdxEngine("Finance")
            .configure_columns(["Account", "Measures"])
            .configure_rows(["Region", "Department"])
            .configure_context_filter([("Year", "2026"), ("Version", "Actual")])
            .generate()
        )
    """

    def __init__(self, cube_name: str):
        self.cube_name = cube_name
        self.builder = MdxBuilder(cube=cube_name)

    def _build_axis_set(self, dimensions: Union[str, List[str]], subset_name: str = "Default") -> MdxHierarchySet:
        """Create a cross-joined set from one or many dimensions."""
        dim_list = [dimensions] if isinstance(dimensions, str) else dimensions

        if not dim_list:
            raise ValueError("At least one dimension is required")

        axis_set = MdxHierarchySet.tm1_subset_all(dim_list[0], subset_name)

        for dim in dim_list[1:]:
            next_set = MdxHierarchySet.tm1_subset_all(dim, subset_name)
            axis_set = MdxHierarchySet.cross_joins([axis_set, next_set])

        return axis_set

    def configure_columns(self, dimensions: Union[str, List[str]], subset_name: str = "Default"):
        """Attach one or many dimensions to the column axis."""
        axis_set = self._build_axis_set(dimensions, subset_name)
        self.builder.add_hierarchy_set_to_column_axis(axis_set)
        return self

    def configure_rows(self, dimensions: Union[str, List[str]], subset_name: str = "Default", suppress_zeros: bool = True):
        """Attach one or many dimensions to the row axis."""
        axis_set = self._build_axis_set(dimensions, subset_name)
        self.builder.add_hierarchy_set_to_row_axis(axis_set)

        if suppress_zeros:
            self.builder.rows_non_empty()

        return self

    def configure_context_filter(self, slices: List[Tuple[str, str]]):
        """Apply dimension members as a WHERE clause context filter."""
        if slices:
            member_objects = [Member.of(dim, element) for dim, element in slices]
            self.builder.where(*member_objects)
        return self

    def generate(self) -> str:
        """Return the final MDX query as a string ready for TM1 execution."""
        return self.builder.to_mdx()
