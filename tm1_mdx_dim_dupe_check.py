from typing import List, Dict
from tm1py.services import TM1Service
from mdxpy import MdxBuilder, Member, Dimension

def find_dimension_duplicates(
    tm1_service: TM1Service, 
    dimension_name: str, 
    hierarchy_name: str, 
    rollups_to_check: List[str]
) -> Dict[str, List[str]]:
    """
    Checks specified roll-ups within a TM1 dimension for duplicate leaf elements.
    
    :param tm1_service: An active TM1Service connection object
    :param dimension_name: Name of the TM1 dimension
    :param hierarchy_name: Name of the hierarchy (use dimension name for default)
    :param rollups_to_check: A list of consolidation element names to inspect
    :return: A dictionary of duplicates found -> { 'child_element': ['RollupA', 'RollupB'] }
    """
    element_mappings = {}  # Tracks { child_element: [parent_rollup1, parent_rollup2, ...] }
    
    for rollup in rollups_to_check:
        # Build the MDX query to fetch leaf elements under this specific rollup
        mdx_query = (
            MdxBuilder.from_cube(f"}}ElementAttributes_{dimension_name}")
            .rows_on_axis(
                Dimension(dimension_name)
                .tm1_filter_by_level(0)  # Level 0 catches leaves where double-counting hurts
                .tm1_drill_down_member(Member.of(dimension_name, rollup))
            )
            .to_mdx()
        )
        
        try:
            # Execute MDX and capture the child elements
            child_elements = tm1_service.elements.execute_mdx(mdx_query)
            
            for child in child_elements:
                if child not in element_mappings:
                    element_mappings[child] = []
                element_mappings[child].append(rollup)
                
        except Exception as e:
            print(f"⚠️ Warning: Could not process rollup '{rollup}'. Error: {e}")
            continue

    # Filter the mappings down to only elements that appear in more than one passed rollup
    duplicates = {
        element: parents 
        for element, parents in element_mappings.items() 
        if len(parents) > 1
    }
    
    return duplicates
