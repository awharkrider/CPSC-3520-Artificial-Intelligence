from search import (
    GraphProblem, astar_search, romania_map
)


def main():
    node = astar_search(GraphProblem('Lugoj', 'Bucharest', romania_map))
    print(node.path())


# Standard boilerplate to call the main function, if executed
if __name__ == '__main__':
    main()
