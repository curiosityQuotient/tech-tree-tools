# Test of a tech tree visualiser tool
import csv
import networkx as nx
import matplotlib.pyplot as plt

from dataclasses import dataclass

@dataclass
class TechNode:
    """Defaults for a technology node."""
    name: str = ""
    predecessors: list[str] = None
    completed: bool = False


class TechTree:
    """Class for technology tree."""

    def __init__(self, name: str):
        self.name = name

    def from_csv(self, csv_path: str):
        """Populates a technology tree object from a csv."""
        # Import data from csv
        tech_nodes = []
        with open(csv_path) as csvfile:
            spamreader = csv.reader(csvfile, delimiter=",", quotechar='"')
            _ = next(spamreader) # skip header
            for row in spamreader:
                tech_nodes.append(TechNode(row[0], row[1].split(";")))

        # create nodes
        tech_tree = nx.DiGraph()
        for tech in tech_nodes:
            tech_tree.add_node(tech.name,
                predecessors= tech.predecessors if tech.predecessors else [],
                completed= tech.completed
            )
        # add edges
        for tech in tech_nodes:
            current_tech = tech.name
            prereqs = tech.predecessors
            for prereq in prereqs:
                if prereq:  # skip empty strings
                    tech_tree.add_edge(prereq, current_tech)

        self.tech_graph = tech_tree

    def draw_graph(self, path: str):
        """Draws the graph that has been created."""
        # generation calcuations
        gen_info = [gen for gen in nx.topological_generations(self.tech_graph)]
        width = len(gen_info)
        height = max([len(gen) for gen in gen_info])

        print(f"Width:{width}, Height:{height}")

        offset = height - 1
        posns = {}
        for ii, techs in enumerate(gen_info):
            # ii is width
            horz = ii
            for jj, tech in enumerate(techs):
                vert = jj + offset
                posns[tech] = (ii, jj)

        colours = []
        for node in self.tech_graph.nodes:
            if self.tech_graph.nodes[node]['completed']:
                colours.append("green")
            else:
                colours.append("red")

        fig, ax = plt.subplots(figsize=(10, 8), layout='constrained')
        nx.draw(self.tech_graph, posns, with_labels=True, node_color=colours, font_size=8)
        plt.savefig(path)

    def list_predecessors(self, node_name: str) -> list:
        """Lists all predecessors of a given node."""
        if self.tech_graph.size() < 1:
            raise Exception("Graph is empty, populate it first")
        if node_name not in list(self.tech_graph.nodes):
            raise ValueError("node_name not in graph")

        # loop through all predecessors
        all_predecessors = set()
        to_visit = [node_name]
        while to_visit:
            current = to_visit.pop()
            for pred in self.tech_graph.predecessors(current):
                if pred not in all_predecessors:
                    print(f"Found predecessor: {pred} for {current}")
                if pred not in all_predecessors:
                    all_predecessors.add(pred)
                    to_visit.append(pred)
        print("All predecessors:", all_predecessors)
        return list(all_predecessors)

    def set_progress(self, completed_techs: list[str]):
        """Sets the progress of the tech tree."""
        for tech in completed_techs:
            if tech in self.tech_graph.nodes:
                self.tech_graph.nodes[tech]['completed'] = True
            else:
                raise ValueError(f"Tech {tech} not found in the graph")
            # set predecessors as completed
            predecessors = self.list_predecessors(tech)
            for pred in predecessors:
                self.tech_graph.nodes[pred]['completed'] = True
        print("Progress updated for:", completed_techs)

    def path_to_target(self, target:str):
        """Calculate the technology path to a target technology."""
        predecessors = self.list_predecessors(target)
        predecessors.append(target)
        path_tree = TechTree(f"Path to {target}")
        path_tree.tech_graph = self.tech_graph.subgraph(predecessors)
        return path_tree


if __name__ == "__main__":
    # create a TechTree object
    tech_tree = TechTree("Freeciv technology tree")
    # Populate a TechTree from a csv
    raw_csv_path = "freeciv_tech_tree.csv"  # "tech_tree_example.csv"
    tech_tree.from_csv(raw_csv_path)
    # List all predecessors of a technology
    tech_tree.list_predecessors("Democracy")
    # Set progress
    tech_tree.set_progress(["Advanced Flight"])
    tech_tree.draw_graph("output/tech_tree.png")
    path_tree = tech_tree.path_to_target("Banking")
    path_tree.draw_graph("output/tech_path.png")
    print("Done")