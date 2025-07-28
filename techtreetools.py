# Test of a tech tree visualiser tool
import csv
import networkx as nx
import matplotlib.pyplot as plt


class TechTree:
    """Class for technology tree."""

    def __init__(self, name: str):
        self.name = name

    def from_csv(self, csv_path: str):
        """Populates a technology tree object from a csv."""
        # Import data from csv
        with open(csv_path) as csvfile:
            spamreader = csv.reader(csvfile, delimiter=",", quotechar='"')
            headers = next(spamreader)
            raw_csv_data = []
            for row in spamreader:
                node = {
                    headers[0]: row[0],
                    headers[1]: row[1].split(";"),
                    headers[2]: row[2].split(";"),
                }
                raw_csv_data.append(node)

        # create nodes
        tech_tree = nx.DiGraph()
        tech_list = []
        for tech in raw_csv_data:
            tech_list.append(
                (
                    tech[headers[0]],
                    {headers[1]: tech[headers[1]], headers[2]: tech[headers[2]]},
                )
            )
            tech_tree.add_node(
                tech[headers[0]],
                **{headers[1]: tech[headers[1]], headers[2]: tech[headers[2]]},
            )
        # add edges
        for tech in raw_csv_data:
            current_tech = tech[headers[0]]
            prereqs = tech[headers[1]]
            for prereq in prereqs:
                if prereq:  # skip empty strings
                    tech_tree.add_edge(prereq, current_tech)

        self.tech_graph = tech_tree

    def draw_graph(self):
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

        nx.draw(self.tech_graph, posns, with_labels=True)
        plt.show()

    def list_predecessors(self, node_name: str):
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


if __name__ == "__main__":
    tech_tree = TechTree("Freeciv technology tree")
    raw_csv_path = "freeciv_tech_tree.csv"  # "tech_tree_example.csv"
    tech_tree.from_csv(raw_csv_path)
    tech_tree.list_predecessors("Democracy")
    tech_tree.draw_graph()
