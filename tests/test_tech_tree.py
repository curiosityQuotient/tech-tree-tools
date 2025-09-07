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

def test_list_predecessors():
    """Test list predecessors functionality."""
    tech_tree = TechTree("Minimal Tech Tree")
    tech_tree.from_csv("tests/fixtures/minimal.csv")
    predecessor_list = tech_tree.list_predecessors("C")
    assert predecessor_list == ["A", "B"]

def test_set_progress():
    """Test that progress is set correctly"""
    tech_tree = TechTree("Minimal Tech Tree")
    tech_tree.from_csv("tests/fixtures/minimal.csv")
    tech_tree.set_progress(["B"])
    assert tech_tree.tech_graph.nodes["B"]["completed"]
    assert tech_tree.tech_graph.nodes["A"]["completed"]
    assert ~tech_tree.tech_graph.nodes["C"]["completed"]

def test_path_to_target():
    """Test path to target calculation."""
    tech_tree = TechTree("Minimal Tech Tree")
    tech_tree.from_csv("tests/fixtures/minimal.csv")
    path_tree = tech_tree.path_to_target("B")
    assert "A" in path_tree.tech_graph.nodes
    assert "B" in path_tree.tech_graph.nodes
    assert "C" not in path_tree.tech_graph.nodes
