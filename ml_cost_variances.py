import pandas as pd
import numpy as np

# -------------------------------------------------------------------------
# STEP 1: DEFINE MOCK DATA EXTRACTS FROM SAP TABLES
# -------------------------------------------------------------------------

# 1. CKMLHD: Material Ledger Header (Resolves Material + Plant to Internal Key KALNR)
ckmlhd_data = {
    "MATNR": ["RM_BASE", "SFG_SOLVENT", "FG_FINAL"],
    "WERKS": ["1000", "1000", "1000"],
    "KALNR": ["100001", "100002", "100003"]
}
df_ckmlhd = pd.DataFrame(ckmlhd_data)

# 2. CKMLCR / MLDOC Period Balances: Pulls Period-End Standard vs Actual Prices
ckmlcr_data = {
    "KALNR": ["100001", "100002", "100003"],
    "POPER": ["09", "09", "09"],
    "GJAHR": ["2026", "2026", "2026"],
    "STPRS": [10.00, 40.00, 100.00],  # Standard Price
    "PVPRS": [12.50, 52.50, 115.00]   # Actual Cost (Periodic Unit Price - PUP)
}
df_ckmlcr = pd.DataFrame(ckmlcr_data)

# 3. MLDOC / AUFM Goods Movement Execution Layer: Captures Material Consumption/Receipts
# This simulates a recursive loop: RM_BASE makes SFG_SOLVENT, but SFG_SOLVENT is cycled back into RM_BASE.
mldoc_data = {
    "AUFNR": ["ORD_A01", "ORD_A01", "ORD_B02", "ORD_B02", "ORD_C03", "ORD_C03"],
    "BWART": ["261", "131", "261", "131", "261", "131"],  # 261 = Issue, 131 = Receipt
    "MATNR": ["SFG_SOLVENT", "RM_BASE", "RM_BASE", "SFG_SOLVENT", "SFG_SOLVENT", "FG_FINAL"],
    "MENGE": [2.0, 10.0, 8.0, 4.0, 3.0, 1.0]  # Quantities processed
}
df_mldoc = pd.DataFrame(mldoc_data)

# 4. AFPO: Order Item Details (Confirms the targeted parent output of an order)
afpo_data = {
    "AUFNR": ["ORD_A01", "ORD_B02", "ORD_C03"],
    "MATNR": ["RM_BASE", "SFG_SOLVENT", "FG_FINAL"]
}
df_afpo = pd.DataFrame(afpo_data)


# -------------------------------------------------------------------------
# STEP 2: PIPELINE ENGINE & VARIANCE CALCULATION
# -------------------------------------------------------------------------

# Compute Variance Rate per unit from valuation records
df_variance = df_ckmlcr.copy()
df_variance["VAR_RATE"] = df_variance["PVPRS"] - df_variance["STPRS"]
df_variance = df_variance.merge(df_ckmlhd, on="KALNR", how="inner")

# Isolate Component Consumptions (Movement Type 261)
df_components = df_mldoc[df_mldoc["BWART"] == "261"][["AUFNR", "MATNR", "MENGE"]]
df_components.columns = ["AUFNR", "COMPONENT_MAT", "QUANTITY_CONSUMED"]

# Attach the component's financial variance rate to the transaction lines
df_components = df_components.merge(df_variance[["MATNR", "VAR_RATE"]], 
                                     left_on="COMPONENT_MAT", right_on="MATNR", how="left")
df_components.drop(columns=["MATNR"], inplace=True)
df_components["VAR_RATE"] = df_components["VAR_RATE"].fillna(0.0)

# Calculate total component dollar variance passed downstream
df_components["TOTAL_COMP_VARIANCE"] = df_components["QUANTITY_CONSUMED"] * df_components["VAR_RATE"]

# Isolate Order Outputs (Movement Type 131 Cross-referenced with AFPO)
df_outputs = df_mldoc[df_mldoc["BWART"] == "131"][["AUFNR", "MATNR"]]
df_outputs.columns = ["AUFNR", "PARENT_MAT"]

# Join Components and Parent Outputs together using the Production Order ID (AUFNR)
df_lineage_base = df_components.merge(df_outputs, on="AUFNR", how="inner")


# -------------------------------------------------------------------------
# STEP 3: RECURSIVE LINEAGE TRAILER WITH LOOP GUARDRAILS
# -------------------------------------------------------------------------

def trace_material_lineage(current_mat, current_order=None, visited_path=None):
    """
    Recursively traces lineage from a given material downstream,
    calculating costs while utilizing a tracking list to prevent infinite loop crashes.
    """
    if visited_path is None:
        visited_path = []
        
    node_id = f"{current_mat} ({current_order})" if current_order else current_mat
    
    # LOOP GUARDRAIL CHECK: If this exact node has been processed in this path, terminate branch
    if node_id in visited_path:
        return [{
            "Component": current_mat,
            "Production Order": current_order,
            "Parent Output": "INFINITE RECURSIVE LOOP DESTINATION",
            "Qty Consumed": 0,
            "Comp Unit Var": 0,
            "Total Rolled Var": 0,
            "Status": "Loop Blocked"
        }]
    
    # Log current step into the tracking list
    updated_path = visited_path + [node_id]
    
    # Find records where the current material acts as a component input
    child_records = df_lineage_base[df_lineage_base["COMPONENT_MAT"] == current_mat]
    
    if child_records.empty:
        return []
        
    lineage_tree = []
    for _, row in child_records.iterrows():
        record = {
            "Component": row["COMPONENT_MAT"],
            "Production Order": row["AUFNR"],
            "Parent Output": row["PARENT_MAT"],
            "Qty Consumed": row["QUANTITY_CONSUMED"],
            "Comp Unit Var": row["VAR_RATE"],
            "Total Rolled Var": row["TOTAL_COMP_VARIANCE"],
            "Status": "Normal Flow"
        }
        lineage_tree.append(record)
        
        # Deep trace down the next level of the assembly line
        next_level = trace_material_lineage(row["PARENT_MAT"], row["AUFNR"], updated_path)
        lineage_tree.extend(next_level)
        
    return lineage_tree

# -------------------------------------------------------------------------
# STEP 4: EXECUTE WORKFLOW & EXPORT DATA FRAME
# -------------------------------------------------------------------------

# Kick off lineage trace starting with base constituent material
full_lineage_report = trace_material_lineage(current_mat="SFG_SOLVENT")
df_report = pd.DataFrame(full_lineage_report)

# Save output data directly to CSV format matching template specifications
df_report.to_csv("generated/material_variance_bom_tracker.csv", index=False)
print("Data Pipeline Completed Successfully. File saved to: generated/material_variance_bom_tracker.csv")
