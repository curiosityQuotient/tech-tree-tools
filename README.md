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

TBC