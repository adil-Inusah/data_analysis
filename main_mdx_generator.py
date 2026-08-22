# Instantiate the engine for a comprehensive financial reporting scenario
complex_query = (
    DynamicMdxEngine(cube_name="Finance")
    
    # Stitching MULTIPLE dimensions on COLUMNS: Nested display of Accounts and Measures
    .configure_columns(dimensions=["Account", "Measures"], subset_name="Default")
    
    # Stitching MULTIPLE dimensions on ROWS: Nested grid display of Region, Department, and Project
    .configure_rows(dimensions=["Region", "Department", "Project"], subset_name="Default", suppress_zeros=True)
    
    # Slicing the entire data view by specific timeline context coordinates
    .configure_context_filter([("Year", "2026"), ("Version", "Actual")])
    
    # Generate the resulting MDX string
    .generate()
)

print(complex_query)
