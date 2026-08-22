"""Example script for the advanced MDX builder.

This module shows how to generate a richer TM1 query with calculated members,
multiple row and column dimensions, and a context filter for the selected
reporting slice.
"""

from tm1_ultimate_mdx_engine import UltimateMdxEngine

# This script shows the advanced engine in action.
# It builds a single Finance cube MDX query with:
# - a custom calculated metric,
# - multi-dimensional row and column layouts,
# - context filtering for Year and Version,
# - optional attribute output for each row member.

# 1. Initialize Engine
engine = UltimateMdxEngine(cube_name="Finance")

# 2. Add an ad-hoc inline query metric calculation.
# This metric exists only for this query and does not alter the cube itself.
engine.add_calculated_member(
    dimension="Measures",
    member_name="Variance_Pct",
    formula_mdx="([Measures].[Amount]) / ([Measures].[Budget_Amount])"
)

# 3. Setup Layout Definitions
# Columns are usually where you place the measure(s) or their cross-product.
columns = [{"dimension": "Measures", "specific_members": ["Amount", "Variance_Pct"]}]

# Rows are typically the reporting entity axes (Account, Region, Department, etc.).
rows = [
    {
        "dimension": "Account",
        "level": 0,
        "sort_order": "ASC",  # Keep account labels alphabetized.
        "output_attributes": ["Description", "Account_Type"]  # Include these as extra display fields.
    },
    {
        "dimension": "Region",
        "subset": "All Countries"
    }
]

# 4. Generate the fully covered execution string.
mdx_statement = (
    engine.configure_columns(columns)
    .configure_rows(rows, suppress_zeros=True)
    .configure_context_filter([("Year", "Default", "2026"), ("Version", "Default", "Actual")])
    .generate()
)

print(mdx_statement)
