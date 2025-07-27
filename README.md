# tech-tree-tools
A tool for exploring and analysing technology trees

## Creating a technology tree object

The technology tree object must be created with a name first.

```python
tech_tree = TechTree("A name")
```

Then a directed graph is created from a csv file.

```python
tech_tree.from_csv("path-to-csv")
```

## Some analysis options

View the tree:

```python
tech_tree.draw_graph()
```

Show predecessors of a node:

```python
tech_tree.list_predecessors("node_name")
```

Feature list to be developed:

* add resource calculations
* calculate minimum development plan for technology given a progress state