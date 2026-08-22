from ultimate_mdx_engine import UltimateMdxEngine

# 1. Initialize Engine
engine = UltimateMdxEngine(cube_name="Finance")

# 2. Add an ad-hoc inline query metric calculation
engine.add_calculated_member(
    dimension="Measures", 
    member_name="Variance_Pct", 
    formula_mdx="([Measures].[Amount]) / ([Measures].[Budget_Amount])"
)

# 3. Setup Layout Definitions
columns = [{"dimension": "Measures", "specific_members": ["Amount", "Variance_Pct"]}]

rows = [
    {
        "dimension": "Account",
        "level": 0,
        "sort_order": "ASC", # Enforce alphabetized ascending sorting
        "output_attributes": ["Description", "Account_Type"] # Returns these text values as data columns!
    },
    {
        "dimension": "Region",
        "subset": "All Countries"
    }
]

# 4. Generate the fully covered execution string
mdx_statement = (
    engine.configure_columns(columns)
    .configure_rows(rows, suppress_zeros=True)
    .configure_context_filter([("Year", "Default", "2026"), ("Version", "Default", "Actual")])
    .generate()
)

print(mdx_statement)
