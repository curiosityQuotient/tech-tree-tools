from techtreetools import TechTree

def test_init_tech_tree():
    """Test the initialization of the TechTree class."""
    tech_tree = TechTree("Test Tree")
    assert tech_tree.name == "Test Tree"

def test_from_csv():
    """Test loading a tech tree from a CSV file."""
    tech_tree = TechTree("Minimal Tech Tree")
    tech_tree.from_csv("tests/fixtures/minimal.csv")
    assert len(tech_tree.tech_graph.nodes) == 3
    assert "A" in tech_tree.tech_graph.nodes
    assert "B" in tech_tree.tech_graph.nodes
    assert "C" in tech_tree.tech_graph.nodes