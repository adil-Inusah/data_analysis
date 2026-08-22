# Configuration details
TM1_CONFIG = {
    "address": "localhost", "port": 8001, "user": "admin", "password": "password", "ssl": True
}

DIM = "Product"
HIERARCHY = "Product"
TARGET_ROLLUPS = ["Total Europe", "Total Americas", "Total APAC"]

# Execution
with TM1Service(**TM1_CONFIG) as tm1:
    duplicate_report = find_dimension_duplicates(
        tm1_service=tm1,
        dimension_name=DIM,
        hierarchy_name=HIERARCHY,
        rollups_to_check=TARGET_ROLLUPS
    )
    
    # Process the modular output
    if duplicate_report:
        print(f"\n❌ Found {len(duplicate_report)} duplicate elements:")
        for child, parents in duplicate_report.items():
            print(f" - '{child}' exists under multiple rollups: {parents}")
    else:
        print("\n✅ No duplicates found among the specified rollups.")
