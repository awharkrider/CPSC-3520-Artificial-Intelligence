"""
PathPlanning.py
Aaron Harkrider
Collaborated with: Ally Wallace, Garrett Henderson

02-06-2018


# Map a path for a UGV(unmanned ground vehicle) to successfully navigate through a grid as fast as possible.

- Two uninformed search algorithms and
    * breadth_first_search
    * depth_first_graph search
- One informed search algorithm
    * A_star

"""

import argparse
import logging
import numpy
import math
from utils import (vector_add, distance)
from search import (
    Problem, breadth_first_search, depth_first_graph_search, astar_search
)


class PathingProblem(Problem):
    """ PathingProblem Implements Problem and gets passed into the search functions.
    PathingProblem lets the searches know how to handle taking an action and determine path_cost.

    """

    def __init__(self, initial, goal, grid):
        Problem.__init__(self, initial, goal)
        """In the constructor we take in the initial state and goal state.
        
       """
        self.initial = initial
        self.goal = goal
        self.grid = grid
        self.max_speed = (numpy.matrix(self.grid).max())

    def actions(self, state):
        """State will show the position we are currently in the grid.
        Will return all the possible action agent can execute in the given state.

        :param state: current state
        :return: all possible action from the current state in a list of tuples
        """

        # array of all possible movements
        # Horizontal/vertical movement: up = (-1, 0)  down = (1, 0) left = (0, -1) right = (0, 1)
        # Diagonal movement: up&left=(-1, -1) down&left=(1, -1) up&right=(-1, 1) down&right=(1, 1)
        all_moves = [(1, 0), (-1, 0), (0, -1), (0, 1), (1, -1), (-1, -1), (1, 1), (-1, 1)]
        valid_moves = []
        for move in all_moves:
            possible_state = vector_add(state, move)
            if valid_position(self.grid, possible_state):
                # Make sure we don't leave the grid and don't run into a wall
                valid_moves.append(move)
        return valid_moves

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state.

        :param state: current state
        :param action: action to take
        :return: The state that results from executing the given action.
        """
        # vector_add does the same thing as my code: tuple(map(sum, zip(state, action)))
        return vector_add(state, tuple(action))

    def path_cost(self, cost_so_far, current_state, action, future_state):
        """ Calculates the path cost by determining the distance based off what action we are taking.
        Then we calculate time: distance divided by the current speed plus the distance divided by the future speed.
        We then add time to the cost_so_far and return that.

        :param cost_so_far: Cost of traversing path so far
        :param current_state: Current location state
        :param action: The action to take
        :param future_state: THe future location state
        :return: cost_so_far + the time it took to execute the action
        """
        # Get the speed values from the locations
        current_speed = self.grid[current_state]
        future_speed = self.grid[future_state]

        if 0 in action:
            # Horizontal/vertical movement: up = (-1, 0)  down = (1, 0) left = (0, -1) right = (0, 1)
            dist = .5
        else:
            # Diagonal movement: up&left=(-1, -1) down&left=(1, -1) up&right=(-1, 1) down&right=(1, 1)
            dist = math.sqrt(2) / 2
        time = (dist / current_speed) + (dist / future_speed)
        return cost_so_far + time

    def h(self, node):
        """h(Heuristic) function is straight-line distance from a node's state to goal.

        :return estimated cost of the cheapest path from the state at node n to a goal state.
        """
        return distance(node.state, self.goal) / self.max_speed


def valid_position(grid, state):
    """Checking to make sure that the state is still in the grid and that it is not an obstacle.

    :param grid: Used to make sure the state is within the the grid and the state is not 0 (an obstacle)
    :param state: The possible state to validate
    :return: boolean, true if state is a valid
    """

    # Checking that <i>,<j> from this state are in the grid and that the value is not a obstacle(value of 0)
    if state[0] in range(0, grid.shape[0]) and state[1] in range(0, grid.shape[1]) and grid[state] != 0:
        return True
    else:
        return False


# _____________________________________________________________________________

def run(algorithm, grid, start, stop):
    """Verify that the start and stop locations are valid then run the indicated search algorithms
    and return the final node. If no algorithm is indicated it will default to A_star search

    :param algorithm: The search algorithm to use
    :param grid: grid to find a path through
    :param start: starting location
    :param stop: goal location
    :return: The path taken
    """

    # Verify start and stop position are valid
    if not valid_position(grid, start):
        try:
            if grid[start] == 0:
                print(start, 'Is not a valid start position, it is in an obstacle.')
        except IndexError:
            print(start, 'Is not a valid start position. Start position must be within the grid: ', grid.shape)
        exit()
    if not valid_position(grid, stop):
        try:
            if grid[stop] == 0:
                print(stop, 'Is not a valid stop position, it is an obstacle.')
        except IndexError:
            print(stop, 'Is not a valid stop position. Stop position must be within the range of the grid shape:',
                  grid.shape)
        exit()

    my_problem = PathingProblem(start, stop, grid)  # Creating instance of PathingProblem

    if algorithm == 'breadth_first_search' or algorithm == 'b':
        return breadth_first_search(my_problem)
    elif algorithm == 'depth_first_graph_search' or algorithm == 'd':
        return depth_first_graph_search(my_problem)
    else:  # Defaults to a_star search
        return astar_search(my_problem)


def main():
    """ Parses in arguments from user and prints out what thier starting and goal locations are,
    then runs program.
    Prints out the path_cost, path length, and the path taken.
    """
    parser = argparse.ArgumentParser(description='Plan route through a grid.')
    parser.add_argument("grid", help="map/grid filename (a csv file)")
    parser.add_argument("start", help="starting location as a pair r,c")
    parser.add_argument("stop", help="ending location as a pair r,c")
    parser.add_argument("--alg", default='a_star', help='algorithm to use to search (defaults: A_star)')
    parser.add_argument("-v", "--verbose", help="increase output verbosity")

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(filename=__file__ + '.log', filemode='w', level=logging.DEBUG)

    i, j = args.start.split(',')
    start = (int(i), int(j))
    print('Starting location is:', start)

    i, j = args.stop.split(',')
    stop = (int(i), int(j))
    print('Goal location is:', stop)

    grid = numpy.loadtxt(args.grid, delimiter=',')  # loading csv file that represents the grid/map

    node = run(args.alg, grid, start, stop)
    print('The path cost was:', node.path_cost)
    print('The path length is:', len(node.path()))
    print('The path is:', node.path())


# Standard boilerplate to call the main function, if executed
if __name__ == '__main__':
    main()
