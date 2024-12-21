from imco import *


def import_tree_from_file(filename):
    """
    Reads a tree from a text file and returns it as a list of lists.

    Each line in the file represents a row in the tree.
    """
    tree = []
    with open(filename, "r") as file:
        for line in file:
            # Convert the line into a list of integers
            row = list(map(int, line.strip().split()))
            tree.append(row)
    return tree


tree = import_tree_from_file("./files/67.txt")


@cache
def f(x, y):
    if x >= len(tree) or y >= len(tree[x]):
        return 0
    return tree[x][y] + max(f(x + 1, y), f(x + 1, y + 1))


print(f(0, 0))
