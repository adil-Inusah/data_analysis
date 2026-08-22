from mdxpy import MdxBuilder, MdxHierarchySet, Member, MdxTuple, CalculatedMember, DimensionProperty, Order
from typing import Union, List, Tuple, Dict, Any

class UltimateMdxEngine:
    """
    A comprehensive factory engine covering advanced multi-axis stitching,
    subsets, level/attribute filtering, unique members, dynamic sorting,
    and inline calculated members.
    """
    def __init__(self, cube_name: str):
        self.cube_name = cube_name
        self.builder = MdxBuilder(cube=cube_name)

    def _build_advanced_set(self, config: Dict[str, Any]) -> MdxHierarchySet:
        """Parses advanced dimension parameters to construct a tailored MDX hierarchy set."""
        dim = config["dimension"]
        hierarchy = config.get("hierarchy", "Default")

        if "specific_members" in config and config["specific_members"]:
            member_objs = [Member.of(dim, hierarchy, m) for m in config["specific_members"]]
            axis_set = MdxHierarchySet.members(member_objs)

        elif "subset" in config and config["subset"]:
            axis_set = MdxHierarchySet.tm1_subset_to_set(dim, hierarchy, config["subset"])

        elif "level" in config and config["level"] is not None:
            axis_set = MdxHierarchySet.tm1_subset_all(dim, hierarchy).filter_by_level(config["level"])

        else:
            axis_set = MdxHierarchySet.tm1_subset_all(dim, hierarchy)

        if "attribute_filter" in config and config["attribute_filter"]:
            attr_name, attr_val = list(config["attribute_filter"].items())[0]
            axis_set = axis_set.filter_by_attribute(attr_name, [attr_val])

        sort_attr = config.get("sort_attribute")
        if "sort_order" in config and config["sort_order"] and sort_attr:
            axis_set = axis_set.order_by_attribute(sort_attr, config["sort_order"])

        return axis_set

    def configure_columns(self, dimension_configs: List[Dict[str, Any]]):
        """Processes and cross-joins column configurations."""
        if not dimension_configs:
            return self
        axis_set = self._build_advanced_set(dimension_configs[0])
        for config in dimension_configs[1:]:
            axis_set = MdxHierarchySet.cross_joins([axis_set, self._build_advanced_set(config)])
        self.builder.add_hierarchy_set_to_column_axis(axis_set)
        return self

    def configure_rows(self, dimension_configs: List[Dict[str, Any]], suppress_zeros: bool = True):
        """Processes rows and registers extra element attributes to display in Pandas."""
        if not dimension_configs:
            return self

        axis_set = self._build_advanced_set(dimension_configs[0])
        for config in dimension_configs[1:]:
            axis_set = MdxHierarchySet.cross_joins([axis_set, self._build_advanced_set(config)])

        self.builder.add_hierarchy_set_to_row_axis(axis_set)
        if suppress_zeros:
            self.builder.rows_non_empty()

        for config in dimension_configs:
            if "output_attributes" in config:
                for attr in config["output_attributes"]:
                    prop = DimensionProperty.of(config["dimension"], config.get("hierarchy", "Default"), attr)
                    self.builder.add_properties_to_row_axis(prop)

        return self

    def add_calculated_member(self, dimension: str, member_name: str, formula_mdx: str):
        """Injects a dynamic runtime equation directly into the query footprint."""
        calc_member = CalculatedMember(dimension, dimension, member_name, formula_mdx)
        self.builder.with_member(calc_member)
        return self

    def configure_context_filter(self, slices: List[Tuple[str, str, str]]):
        """Creates a slice context tuple (WHERE clause)."""
        if slices:
            member_objects = [Member.of(dim, hi, elem) for dim, hi, elem in slices]
            self.builder.where(*member_objects)
        return self

    def generate(self) -> str:
        """Compiles the final raw MDX query."""
        return self.builder.to_mdx()
