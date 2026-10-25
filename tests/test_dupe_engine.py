import unittest
from unittest.mock import Mock

from tm1_mdx_dim_dupe_check import find_rollup_duplicates_fast

class TestDuplicateEngine(unittest.TestCase):
    def test_find_rollup_duplicates_fast_basic(self):
        # Prepare a fake TM1Service with the expected elements.get_edges signature
        tm1 = Mock()
        # edges is a dict keyed by (parent, child) -> weight
        edges = {
            ("All Products", "ProdA"): 1,
            ("All Products", "ProdB"): 1,
            ("Total Europe", "ProdA"): 1,
            ("Total Americas", "ProdB"): 1,
        }
        tm1.elements.get_edges.return_value = edges

        duplicates = find_rollup_duplicates_fast(
            tm1_service=tm1,
            dimension_name="Product",
            hierarchy_name="Product",
            rollups_to_check=["Total Europe", "All Products"]
        )

        # ProdA is in Total Europe and All Products -> should be reported
        expected = {"ProdA": ["All Products", "Total Europe"]}
        self.assertEqual(duplicates, expected)

if __name__ == "__main__":
    unittest.main()
