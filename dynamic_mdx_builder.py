from mdxpy import MdxBuilder, MdxHierarchySet, Member, MdxTuple
from typing import Union, List, Tuple

class DynamicMdxEngine:
    def __init__(self, cube_name: str):
        self.cube_name = cube_name
        self.builder = MdxBuilder(cube=cube_name)
        
    def _build_axis_set(self, dimensions: Union[str, List[str]], subset_name: str = "Default") -> MdxHierarchySet:
        """Helper method to convert a string or a list of dimensions into a cross-joined MDX set."""
        dim_list = [dimensions] if isinstance(dimensions, str) else dimensions
        
        # Initialize the base set with the first dimension
        axis_set = MdxHierarchySet.tm1_subset_all(dim_list[0], subset_name)
        
        # Sequentially cross-join all remaining dimensions to stitch them onto the axis
        for dim in dim_list[1:]:
            next_set = MdxHierarchySet.tm1_subset_all(dim, subset_name)
            axis_set = axis_set.cross_join(next_set)
            
        return axis_set

    def configure_columns(self, dimensions: Union[str, List[str]], subset_name: str = "Default"):
        """Stitches one or multiple dimensions onto the Column Axis (Axis 0)."""
        axis_set = self._build_axis_set(dimensions, subset_name)
        self.builder.add_hierarchy_set_to_column_axis(axis_set)
        return self

    def configure_rows(self, dimensions: Union[str, List[str]], subset_name: str = "Default", suppress_zeros: bool = True):
        """Stitches one or multiple dimensions onto the Row Axis (Axis 1)."""
        axis_set = self._build_axis_set(dimensions, subset_name)
        row_axis = self.builder.add_hierarchy_set_to_row_axis(axis_set)
        
        if suppress_zeros:
            row_axis.suppress_zeroes()
            
        return self

    def configure_context_filter(self, slices: List[Tuple[str, str]]):
        """Creates a context coordinate slice (WHERE clause) using an MDX Tuple."""
        if slices:
            member_objects = [Member.of(dim, element) for dim, element in slices]
            context_tuple = MdxTuple.of(*member_objects)
            self.builder.add_tuple_to_where_clause(context_tuple)
        return self

    def generate(self) -> str:
        """Compiles and returns the final raw MDX query string."""
        return self.builder.to_mdx()
