# cpsc-3520-path-planning-project
**Path Planning Program**
- Author: Aaron Harkrider
- Collaborated with: Ally Wallace and Garrett Henderson
- Date: 02-06-2018
- Class: CPSC 3520 Into to Artificial Intelligence
- Due date of Project: 02-16-2018

The Program will perform path planning on a map represented as a grid with the objective of navigating an unmanned ground vehicle (UGV) through the grid.
Each square in the grid contains the speed of the UGV while in that square. 
Any obstacle is represented as a 0 for the speed of the square.

# Program Implementation
For this program I imported search.py and utils.py from the "Artificial Intelligence: A Modern Approach" (AIMA) code library and then implement a problem class I called "PathingProblem" which I pass to the searches.

#### Algorithms Implemented

* Two uninformed search algorithms
    * breadth_first_search
        * Is complete, optimal for unit step costs, but has exponential space complexity. 
        * Averaged to be the middle of the road in performance of searches implemented.
    * depth_first_graph search
        * Not complete or optimal but has a decent space complexity of linear. 
        * Least optimal search implemented in this project.
* One informed search algorithm
    * a_star
        * Complete and optimal using heuristic to find best path. Space complexity is high.
        * Most optimal of searches implemented


Definition of search properties:
* Completeness: Is the algorithm guaranteed to find a solution when there is one? 
* Optimality: Does the strategy find the optimal solution?
* Time complexity: How long does it take to find a solution?
* Space complexity: How much memory is needed to perform the search?

# Running the Program

**Packages Required**

In addition to python this program requires the numpy or tensorflow package to be installed. 

To install dependencies run: 

        pip install -r requirements.txt

### Run Program from command line:

    python3 PathPlanning.py --alg a map1.csv 1,1 4,4
    
Arguments are:

    <program name> <optional algorithm> <map filename> <starting location> <ending location>
* To indicate which search algorithm to use `--alg` then the algorithm
    * `a` or `a_star` (This is the default search if no algorithm is indicated)
    * `b` or `breadth_first_search`
    * `d` or `depth_first_graph_search`
* start position in the grid indicated by a pair `(i,j)` with no spaces
* stop(goal) position in the grid indicated indicated by a pair `(i,j)` with no spaces

# Math for Step Cost

**Calculating Cost of a Single Step**

To calculate the cost of a single step we first determine teh distance based off of the type of movement.
If the move is horizontal/vertical distance is .5, 
else it is diagonal and we calculate the angle by getting the square root of 2 divided by 2.
We then calculate the time by dividing distance by the speed of our current location plus the
distance divided by the speed at the location we are moving into. 

Time then represent the cost of this step.

        if 0 in action:
            # Horizontal/vertical movement: up = (-1, 0)  down = (1, 0) left = (0, -1) right = (0, 1)
            dist = .5
        else:
            # Diagonal movement: up&left=(-1, -1) down&left=(1, -1) up&right=(-1, 1) down&right=(1, 1)
            dist = math.sqrt(2) / 2
        time = (dist / current_speed) + (dist / future_speed)

**Calculating Path Cost**

To calculate the path cost we take the accumulated cost so far and the cost of the next step (which is described above) 
and add them together.


