from mdxpy import MdxBuilder, MdxHierarchySet, Member, MdxTuple
from typing import Union, List, Tuple

class DynamicMdxEngine:
    def __init__(self, cube_name: str):
        self.cube_name = cube_name
        self.builder = MdxBuilder(cube=cube_name)

    def _build_axis_set(self, dimensions: Union[str, List[str]], subset_name: str = "Default") -> MdxHierarchySet:
        """Helper method to convert a string or a list of dimensions into a cross-joined MDX set."""
        dim_list = [dimensions] if isinstance(dimensions, str) else dimensions

        if not dim_list:
            raise ValueError("At least one dimension is required")

        axis_set = MdxHierarchySet.tm1_subset_all(dim_list[0], subset_name)

        for dim in dim_list[1:]:
            next_set = MdxHierarchySet.tm1_subset_all(dim, subset_name)
            axis_set = MdxHierarchySet.cross_joins([axis_set, next_set])

        return axis_set

    def configure_columns(self, dimensions: Union[str, List[str]], subset_name: str = "Default"):
        """Stitches one or multiple dimensions onto the Column Axis (Axis 0)."""
        axis_set = self._build_axis_set(dimensions, subset_name)
        self.builder.add_hierarchy_set_to_column_axis(axis_set)
        return self

    def configure_rows(self, dimensions: Union[str, List[str]], subset_name: str = "Default", suppress_zeros: bool = True):
        """Stitches one or multiple dimensions onto the Row Axis (Axis 1)."""
        axis_set = self._build_axis_set(dimensions, subset_name)
        self.builder.add_hierarchy_set_to_row_axis(axis_set)

        if suppress_zeros:
            self.builder.rows_non_empty()

        return self

    def configure_context_filter(self, slices: List[Tuple[str, str]]):
        """Creates a context coordinate slice (WHERE clause) using MDX members."""
        if slices:
            member_objects = [Member.of(dim, element) for dim, element in slices]
            self.builder.where(*member_objects)
        return self

    def generate(self) -> str:
        """Compiles and returns the final raw MDX query string."""
        return self.builder.to_mdx()
