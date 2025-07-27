from tech_tree import TechTree

def test_init_tech_tree():
    """Test the initialization of the TechTree class."""
    tech_tree = TechTree("Test Tree")
    assert tech_tree.name == "Test Tree"
    assert hasattr(tech_tree, 'tech_graph')  # Ensure tech_graph is initialized