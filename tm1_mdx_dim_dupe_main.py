from tm1py.services import TM1Service
from mdx.engine import find_rollup_duplicates_fast

# Configuration details for TM1
TM1_CONFIG = {
    "address": "localhost", "port": 8001, "user": "admin", "password": "password", "ssl": True
}

# Define your testing scope across multiple dimensions
JOBS_TO_RUN = {
    "Product": {
        "hierarchy": "Product",
        "rollups": ["Total Europe", "Total Americas", "Total APAC", "All Products"]
    },
    "Customer": {
        "hierarchy": "Customer",
        "rollups": ["Corporate Clients", "Retail Clients", "Internal Accounts"]
    },
    "CostCenter": {
        "hierarchy": "CostCenter",
        "rollups": ["Operations", "Backoffice", "Marketing Division"]
    }
}

# Run the master sweep
with TM1Service(**TM1_CONFIG) as tm1:
    print("🚀 Starting global duplicate validation sweep...")
    
    global_report = {}
    
    for dim_name, config in JOBS_TO_RUN.items():
        print(f"Analyzing {dim_name}...")
        
        dim_duplicates = find_rollup_duplicates_fast(
            tm1_service=tm1,
            dimension_name=dim_name,
            hierarchy_name=config["hierarchy"],
            rollups_to_check=config["rollups"]
        )
        
        if dim_duplicates:
            global_report[dim_name] = dim_duplicates

    # Final Summary Output
    print("\n================ DETECTED DUPLICATES SUMMARY ================")
    if not global_report:
        print("✅ Clean sweep! No duplicates found in any specified rollups.")
    else:
        for dim, duplicates in global_report.items():
            print(f"\n📁 Dimension: {dim} ({len(duplicates)} duplicates found)")
            for leaf, parents in duplicates.items():
                print(f"  ❌ Leaf '{leaf}' is repeated in: {parents}")
