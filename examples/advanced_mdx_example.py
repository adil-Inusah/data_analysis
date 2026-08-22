"""Advanced example for the feature-rich MDX builder."""

from mdx.tm1_ultimate_mdx_engine import UltimateMdxEngine


engine = UltimateMdxEngine(cube_name="Finance")
engine.add_calculated_member(
    dimension="Measures",
    member_name="Variance_Pct",
    formula_mdx="([Measures].[Amount]) / ([Measures].[Budget_Amount])",
)

columns = [{"dimension": "Measures", "specific_members": ["Amount", "Variance_Pct"]}]
rows = [
    {
        "dimension": "Account",
        "level": 0,
        "sort_order": "ASC",
        "output_attributes": ["Description", "Account_Type"],
    },
    {"dimension": "Region", "subset": "All Countries"},
]

mdx_statement = (
    engine.configure_columns(columns)
    .configure_rows(rows, suppress_zeros=True)
    .configure_context_filter([("Year", "Default", "2026"), ("Version", "Default", "Actual")])
    .generate()
)


if __name__ == "__main__":
    print(mdx_statement)
