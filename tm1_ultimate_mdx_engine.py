"""Advanced MDX builder for complex TM1 reporting layouts.

This class is designed for reporting scenarios where a single query needs more
than a simple list of dimensions. It handles multiple dimensions per axis,
attribute filtering, level filtering, calculated members, and context slices.
The builder keeps the MDX creation logic encapsulated behind a fluent API so the
calling code stays readable and easier to maintain.
"""

from mdxpy import MdxBuilder, MdxHierarchySet, Member, CalculatedMember, DimensionProperty
from typing import List, Tuple, Dict, Any


class UltimateMdxEngine:
    """Factory-like engine for generating complex MDX queries.

    A configuration dictionary is used for each dimension, which gives the caller a
    declarative way to describe the exact slice of the hierarchy needed on a row or
    column axis.
    """

    def __init__(self, cube_name: str):
        # The cube we are querying at runtime.
        self.cube_name = cube_name
        # mdxpy builder is the central query object that accumulates all axis sets
        # and the WHERE clause before finally rendering the MDX string.
        self.builder = MdxBuilder(cube=cube_name)

    def _build_advanced_set(self, config: Dict[str, Any]) -> MdxHierarchySet:
        """Convert a dimension config into a valid hierarchy set.

        Supported patterns include:
        - specific members
        - TM1 named subsets
        - level-based members
        - default all-members fallback

        After the base set is created, optional filters and sort rules are applied.
        """
        dim = config["dimension"]
        hierarchy = config.get("hierarchy", "Default")

        # 1) Explicit members: useful when you want a fixed list like [Revenue, Margin].
        if "specific_members" in config and config["specific_members"]:
            member_objs = [Member.of(dim, hierarchy, m) for m in config["specific_members"]]
            axis_set = MdxHierarchySet.members(member_objs)

        # 2) TM1 subset: useful when the reporting model has a reusable named subset.
        elif "subset" in config and config["subset"]:
            axis_set = MdxHierarchySet.tm1_subset_to_set(dim, hierarchy, config["subset"])

        # 3) Level filter: useful for leaf-level members or hierarchy branch targeting.
        elif "level" in config and config["level"] is not None:
            axis_set = MdxHierarchySet.tm1_subset_all(dim, hierarchy).filter_by_level(config["level"])

        # 4) Default fallback: all members in the default hierarchy.
        else:
            axis_set = MdxHierarchySet.tm1_subset_all(dim, hierarchy)

        # Optional attribute filter such as "Region Type = North" or similar.
        if "attribute_filter" in config and config["attribute_filter"]:
            attr_name, attr_val = list(config["attribute_filter"].items())[0]
            axis_set = axis_set.filter_by_attribute(attr_name, [attr_val])

        # Optional attribute-based ordering, e.g. sort by Description or Category.
        sort_attr = config.get("sort_attribute")
        if "sort_order" in config and config["sort_order"] and sort_attr:
            axis_set = axis_set.order_by_attribute(sort_attr, config["sort_order"])

        return axis_set

    def configure_columns(self, dimension_configs: List[Dict[str, Any]]):
        """Build the column axis from a list of dimension configurations.

        Each config is converted into a set and then cross-joined with later configs,
        resulting in a nested column layout like Measures x Account or Month x Scenario.
        """
        if not dimension_configs:
            return self

        axis_set = self._build_advanced_set(dimension_configs[0])
        for config in dimension_configs[1:]:
            axis_set = MdxHierarchySet.cross_joins([axis_set, self._build_advanced_set(config)])

        self.builder.add_hierarchy_set_to_column_axis(axis_set)
        return self

    def configure_rows(self, dimension_configs: List[Dict[str, Any]], suppress_zeros: bool = True):
        """Build the row axis and optionally hide zero rows.

        This is where the main reporting view is usually assembled: rows may include
        Region, Department, Product, or Account hierarchies. The method also allows
        line-item attribute metadata to be returned alongside the row members.
        """
        if not dimension_configs:
            return self

        axis_set = self._build_advanced_set(dimension_configs[0])
        for config in dimension_configs[1:]:
            axis_set = MdxHierarchySet.cross_joins([axis_set, self._build_advanced_set(config)])

        self.builder.add_hierarchy_set_to_row_axis(axis_set)
        if suppress_zeros:
            # This mirrors NON EMPTY behavior for the row axis.
            self.builder.rows_non_empty()

        # Add optional properties such as Description, Account Type, or other text
        # attributes to be returned as additional display columns in the result set.
        for config in dimension_configs:
            if "output_attributes" in config:
                for attr in config["output_attributes"]:
                    prop = DimensionProperty.of(config["dimension"], config.get("hierarchy", "Default"), attr)
                    self.builder.add_properties_to_row_axis(prop)

        return self

    def add_calculated_member(self, dimension: str, member_name: str, formula_mdx: str):
        """Inject a calculated member into the WITH clause.

        This is useful for metrics such as variance %, margin %, or custom ratios
        that are only needed within the current query and should not be stored in the
        cube as a permanent member.
        """
        calc_member = CalculatedMember(dimension, dimension, member_name, formula_mdx)
        self.builder.with_member(calc_member)
        return self

    def configure_context_filter(self, slices: List[Tuple[str, str, str]]):
        """Apply a fixed context to the query using a WHERE tuple.

        Each tuple is a three-part value: (dimension, hierarchy, element), which
        narrows the result to a specific slice such as Year=2026 and Version=Actual.
        """
        if slices:
            member_objects = [Member.of(dim, hi, elem) for dim, hi, elem in slices]
            self.builder.where(*member_objects)
        return self

    def generate(self) -> str:
        """Compile the configured axes and filters into a final MDX string."""
        return self.builder.to_mdx()
