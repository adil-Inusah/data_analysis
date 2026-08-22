"""Basic example for the lightweight MDX builder."""

from mdx.dynamic_mdx_builder import DynamicMdxEngine


complex_query = (
    DynamicMdxEngine(cube_name="Finance")
    .configure_columns(dimensions=["Account", "Measures"], subset_name="Default")
    .configure_rows(dimensions=["Region", "Department", "Project"], subset_name="Default", suppress_zeros=True)
    .configure_context_filter([("Year", "2026"), ("Version", "Actual")])
    .generate()
)


if __name__ == "__main__":
    print(complex_query)
