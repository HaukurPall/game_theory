# Nash equilibrium solver
### Authors
Haukur Páll Jónsson and Grzegorz Lisowski
## Running the code
### Prerequisites
- python 3.5+
- numpy

### Game definition
1st line is the name of the game.
2nd line is the first row of utilities for player 1, values are separated with ",".
3rd line is the second row of utilities for player 1.
4th line is the second row of utilities for player 2.
5th line is the second row of utilities for player 2.

For an example

    Prioner's dilemma
    -10,-25
    0,-20
    -10,0
    -25,-20
    
Then provide the game definition to the program when running
    
### Executing
    python NE_solver.py game_definition.txt
### Output

    ((0.0,1.0),(1.0,0.0))
    ((1.0,0.0),(0.0,1.0))
    ((1.0,0.0),(0.4,0.6))
    ((1.0,0.0),(0.4-e,0.6+e))
When and interval is also contained in mixed solution that is denoted by putting + or -. F.ex. (0.4-e,0.6+e) means that (0.399, 0.601) to (0.0, 1.0) is also in the solution 