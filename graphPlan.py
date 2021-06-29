# graphPlan.py
# ------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In graphPlan.py, you will implement graph plan planning methods which are called by
Pacman agents (in graphPlanAgents.py).
"""

import util
import sys
import logic
import game
from graphplanUtils import *

OPEN = "Open"
WALL = "Wall"
FOOD = "Food"
PACMAN = "Pacman"

class PlanningProblem:
    """
    This class outlines the structure of a planning problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the planning problem.
        """
        util.raiseNotDefined()

    def getGhostStartStates(self):
        """
        Returns a list containing the start state for each ghost.
        Only used in problems that use ghosts (FoodGhostPlanningProblem)
        """
        util.raiseNotDefined()
        
    def getGoalState(self):
        """
        Returns goal state for problem. Note only defined for problems that have
        a unique goal state such as PositionPlanningProblem
        """
        util.raiseNotDefined()

def tinyMazePlan(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


def modelToString(model):
    """Converts the model to a string for printing purposes. The keys of a model are 
    sorted before converting the model to a string.
    
    model: Either a boolean False or a dictionary of Expr symbols (keys) 
    and a corresponding assignment of True or False (values). This model is the output of 
    a call to logic.pycoSAT.
    """
    if model == False:
        return "False" 
    else:
        # Dictionary
        modelList = sorted(model.items(), key=lambda item: str(item[0]))
        return str(modelList)

"""
    Create and solve the pacman navigation problem. 
    You will create instances, variables, and operators for pacman's actions 
    'North','South','East','West'
    Operators contain lists of preconditions, add effects, and delete effects
    which are all composed of propositions (boolean descriptors of the environment)
    Operators will test the current state propositions to determine whether all
    the preconditions are true, and then add and delete state propositions 
    to update the state.

    o_west = Operator('West', # the name of the action
                      [],     # preconditions
                      [],     # add effects   
                      []      # delete effects                         
                      )  
                      
    A GraphPlan problem requires a list of all instances, all operators, the start state and 
    the goal state. You must create these lists for GraphPlan.solve.
"""
def positionGraphPlan(problem):
    width, height = problem.getWidth(), problem.getHeight()

    start_x = problem.startState[0]
    start_y = problem.startState[1]

    goal_x = problem.goal[0]
    goal_y = problem.goal[1]

    # Instances
    i_pacman = Instance('pacman',PACMAN)
    i_ints = [Instance(0, INT),
              Instance(1, INT),
              Instance(2, INT)]
    i_open = Instance('open',OPEN)
    i_wall = Instance('wall',WALL)
    i_start_x = Instance(start_x, INT)
    i_start_y = Instance(start_y, INT)
    i_goal_x = Instance(goal_x, INT)
    i_goal_y = Instance(goal_y, INT)

    allinstances = [i_pacman,i_ints[0],i_ints[1], i_ints[0] ,i_open,i_wall,i_start_x,i_start_y,i_goal_x, i_goal_x ] # Make sure you fill this with ALL the instances you define
    
    walls = problem.walls     # if walls[x][y] is True, then that means there is a wall at (x,y)
    
    ## Crea los estados final e inicial, al inicial se le anade el laberinto.
    start_state = [Proposition('at', i_pacman, i_start_x, i_start_y)]
    goal_state = [Proposition('at', i_pacman, i_goal_x, i_goal_y)]

    for x in range(width):
        for y in range(height):
            temp_x = Instance(x, INT)
            temp_y = Instance(y, INT)
            allinstances.append(temp_x)
            allinstances.append(temp_y)
            if(walls[x][y] == True):
                start_state.append(Proposition('at',i_wall,temp_x,temp_y))
            else:
                start_state.append(Proposition('at',i_open,temp_x,temp_y))
    
   
    x_to = Variable('x_to',INT)
    x_from = Variable('x_from',INT)
    y_to = Variable('y_to',INT)
    y_from = Variable('y_from',INT)

   

    o_south = Operator('South',
         ## Primero comprueba que el pacman esta en xfrom y from y luego que en el to no hay una pared.
        [Proposition('at', i_pacman, x_from, y_from),
         Proposition('at', i_open, x_to, y_to),
         ## des pues comprueba que la x es la misma y la y de from es uno mas abajo.
         Proposition(EQUAL, x_from, x_to),
         Proposition(SUM, i_ints[1], y_to, y_from)],

        [Proposition('at', i_pacman,x_to, y_to)],
        [Proposition('at', i_pacman,x_from, y_from)])

    o_west = Operator('West',
         ## Primero comprueba que el pacman esta en xfrom y from y luego que en el to no hay una pared.
        [Proposition('at', i_pacman, x_from, y_from),
         Proposition('at', i_open, x_to, y_to),
         ## des pues comprueba que la y es la misma y la x de from es uno mas a la derecha.
         Proposition(EQUAL, y_from, y_to),
         Proposition(SUM, i_ints[1], x_to, x_from)],

        [Proposition('at', i_pacman,x_to, y_to)],
        [Proposition('at', i_pacman,x_from, y_from)])

    o_north = Operator('North',
         ## Primero comprueba que el pacman esta en xfrom y from y luego que en el to no hay una pared.
        [Proposition('at', i_pacman, x_from, y_from),
         Proposition('at', i_open, x_to, y_to),
         ## des pues comprueba que la x es la misma y la y de from es uno mas arriba.
         Proposition(EQUAL, x_from, x_to),
         Proposition(SUM, i_ints[1], y_from, y_to)],

        [Proposition('at', i_pacman,x_to, y_to)],
        [Proposition('at', i_pacman,x_from, y_from)])

    o_east = Operator('East',
         ## Primero comprueba que el pacman esta en xfrom y from y luego que en el to no hay una pared.
        [Proposition('at', i_pacman, x_from, y_from),
         Proposition('at', i_open, x_to, y_to),
         ## des pues comprueba que la y es la misma y la x de from es uno mas a la izquierda.
         Proposition(EQUAL, y_from, y_to),
         Proposition(SUM, i_ints[1], x_from, x_to)],

        [Proposition('at', i_pacman,x_to, y_to)],
        [Proposition('at', i_pacman,x_from, y_from)])


    alloperators = [o_south,o_west,o_north,o_east] 

    acciones_return = []
    problem = GraphPlanProblem('final_xy',allinstances,alloperators,start_state, goal_state)
    solucion = problem.solve()
    acciones = problem.getactions()
    
    ## Mira todas las acciones y si son popsibles para el pacman.
    for nivel in solucion:
        for accion in nivel:
            if accion in acciones:
                acciones_return.append(accion.print_name())
    
    return acciones_return

    

"""
Now use the operators for moving along with an eat operator you must create to eat 
all the food in the maze.
"""
def foodGraphPlan(problem ):
    width, height = problem.getWidth(), problem.getHeight()
    walls = problem.walls     # if walls[x][y] is True, then that means there is a wall at (x,y)
    start_x = problem.start[0][0]
    start_y = problem.start[0][1]
    foodlist = problem.start[1].asList() 
    

    # Instances
    allinstances = [] # Make sure you fill this with ALL the instances you define
    i_pacman = Instance('pacman', PACMAN)
    i_foods = []
    i_wall = Instance('wall', WALL)
    i_open = Instance('open', OPEN)
    i_start_x = Instance(start_x, INT)
    i_start_y = Instance(start_y, INT)
    i_ints = [Instance(0, INT), 
          Instance(1, INT), 
          Instance(2, INT)]

   

    allinstances = [i_pacman,i_ints[0],i_ints[1], i_ints[0] ,i_open,i_wall,i_start_x,i_start_y ] # Make sure you fill this with ALL the instances you define
    
    walls = problem.walls     # if walls[x][y] is True, then that means there is a wall at (x,y)
    ## Crea los estados final e inicial, al inicial se le anade el laberinto.
    start_state = [Proposition('at', i_pacman, i_start_x, i_start_y)]
    goal_state = []
    counter = 0
    for x in range(width):
        for y in range(height):
            
            temp_x = Instance(x, INT)
            temp_y = Instance(y, INT)
            allinstances.append(temp_x)
            allinstances.append(temp_y)
            ## Se anaden a las instancias las coordenadas de la comida y la comida.
            temp_foodx = Instance(x, INT)
            temp_foody = Instance(y, INT)   
            temp_food = Instance(counter, FOOD)
            allinstances.append(temp_foodx)
            allinstances.append(temp_foody)
            allinstances.append(temp_food)
            ## Si se encuentra comida se anade a las proposiciones.
            if (x,y) in foodlist:
                start_state.append(Proposition('at', temp_food, temp_foodx,temp_foody))
                goal_state.append(Proposition('eat', temp_food, i_pacman))
            else:
                start_state.append(~Proposition('at', temp_food, temp_foodx,temp_foody))
            counter += 1

            if(walls[x][y] == True):
                start_state.append(Proposition('at',i_wall,temp_x,temp_y))
            else:
                start_state.append(Proposition('at',i_open,temp_x,temp_y))
    
   
    x_to = Variable('x_to',INT)
    x_from = Variable('x_from',INT)
    y_to = Variable('y_to',INT)
    y_from = Variable('y_from',INT)

    v_food_x = Variable('place_x', INT)
    v_food_y = Variable('place_y', INT)
    v_food = Variable('food', FOOD)

   

    o_south = Operator('South',
         ## Primero comprueba que el pacman esta en xfrom y from y luego que en el to no hay una pared.
        [Proposition('at', i_pacman, x_from, y_from),
         Proposition('at', i_open, x_to, y_to),
         ## Despues comprueba que la x es la misma y la y de from es uno mas abajo.
         Proposition(EQUAL, x_from, x_to),
         Proposition(SUM, i_ints[1], y_to, y_from)],

        [Proposition('at', i_pacman,x_to, y_to)],
        [Proposition('at', i_pacman,x_from, y_from)])

    o_west = Operator('West',
         ## Primero comprueba que el pacman esta en xfrom y from y luego que en el to no hay una pared.
        [Proposition('at', i_pacman, x_from, y_from),
         Proposition('at', i_open, x_to, y_to),
         ## Despues comprueba que la y es la misma y la x de from es uno mas a la derecha.
         Proposition(EQUAL, y_from, y_to),
         Proposition(SUM, i_ints[1], x_to, x_from)],

        [Proposition('at', i_pacman,x_to, y_to)],
        [Proposition('at', i_pacman,x_from, y_from)])

    o_north = Operator('North',
         ## Primero comprueba que el pacman esta en xfrom y from y luego que en el to no hay una pared.
        [Proposition('at', i_pacman, x_from, y_from),
         Proposition('at', i_open, x_to, y_to),
         ## Despues comprueba que la x es la misma y la y de from es uno mas arriba.
         Proposition(EQUAL, x_from, x_to),
         Proposition(SUM, i_ints[1], y_from, y_to)],

        [Proposition('at', i_pacman,x_to, y_to)],
        [Proposition('at', i_pacman,x_from, y_from)])

    o_east = Operator('East',
         ## Primero comprueba que el pacman esta en xfrom y from y luego que en el to no hay una pared.
        [Proposition('at', i_pacman, x_from, y_from),
         Proposition('at', i_open, x_to, y_to),
         ## Despues comprueba que la y es la misma y la x de from es uno mas a la izquierda.
         Proposition(EQUAL, y_from, y_to),
         Proposition(SUM, i_ints[1], x_from, x_to)],

        [Proposition('at', i_pacman,x_to, y_to)],
        [Proposition('at', i_pacman,x_from, y_from)])
    
    o_eat= Operator('Eat', 
        ## Para comer comprueba que el pacman esta en el sitio y que hay comida.
        [Proposition('at', i_pacman, v_food_x, v_food_y),
         Proposition('at', v_food, v_food_x, v_food_y),],
        [Proposition('eat', v_food, i_pacman)],      
        [Proposition('at', v_food, v_food_x, v_food_y)])


    alloperators = [o_south,o_west,o_north,o_east, o_eat] 

    acciones_return = []
    problem = GraphPlanProblem('eatfood',allinstances,alloperators,start_state, goal_state)
    solucion = problem.solve()
    acciones = problem.getactions()
    
    ## Mira todas las acciones y si son posibles para el pacman.
    for nivel in solucion:
        for accion in nivel:
            if accion in acciones:
                if accion in acciones and accion.print_name() != 'Eat':
                    acciones_return.append(accion.print_name())
    
    return acciones_return
    



# Abbreviations
pgp = positionGraphPlan
fgp = foodGraphPlan

# Sometimes the logic module uses pretty deep recursion on long expressions
sys.setrecursionlimit(100000)
    
