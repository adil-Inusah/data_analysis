from typing import List, Dict, Set
from tm1py.services import TM1Service

def find_rollup_duplicates_fast(
    tm1_service: TM1Service, 
    dimension_name: str, 
    hierarchy_name: str, 
    rollups_to_check: List[str]
) -> Dict[str, List[str]]:
    """
    Finds duplicate leaf elements across specified rollups instantly using 
    in-memory edge evaluation instead of repeated MDX queries.
    """
    # 1. Fetch ALL hierarchy relationships (edges) in one bulk database call
    # Returns a dict of {(parent, child): weight}
    try:
        edges = tm1_service.elements.get_edges(dimension_name, hierarchy_name)
    except Exception as e:
        print(f"⚠️ Error fetching edges for dimension '{dimension_name}': {e}")
        return {}

    # 2. Re-structure edges into a fast lookup tree: { parent: [children] }
    tree = {}
    all_children = set()
    for parent, child in edges.keys():
        if parent not in tree:
            tree[parent] = []
        tree[parent].append(child)
        all_children.add(child)
        
    # Elements that are never children are top-level consolidations
    all_parents = set(tree.keys())
    # Leaf elements are elements that never act as a parent to anything
    leaf_elements = all_children - all_parents

    # 3. Helper function to recursively find all level-0 leaves under a consolidation
    def get_all_leaves(element: str, memo: Dict[str, Set[str]]) -> Set[str]:
        if element in leaf_elements:
            return {element}
        if element in memo:
            return memo[element]
        
        leaves = set()
        # If it's a consolidation, look up its children
        if element in tree:
            for child in tree[element]:
                leaves.update(get_all_leaves(child, memo))
                
        memo[element] = leaves
        return leaves

    # Cache to optimize recursive lookups
    memo_cache = {}
    element_mappings = {}  # { leaf_element: [rollup1, rollup2, ...] }
    
    # 4. Map leaves to our target rollups
    for rollup in rollups_to_check:
        if rollup not in tree and rollup not in leaf_elements:
            print(f"⚠️ Warning: Rollup '{rollup}' not found in dimension '{dimension_name}'.")
            continue
            
        rollup_leaves = get_all_leaves(rollup, memo_cache)
        
        for leaf in rollup_leaves:
            if leaf not in element_mappings:
                element_mappings[leaf] = []
            element_mappings[leaf].append(rollup)

    # 5. Extract only elements tied to more than one target rollup
    duplicates = {
        element: parents 
        for element, parents in element_mappings.items() 
        if len(parents) > 1
    }
    
    return duplicates
