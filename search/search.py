# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

# Sam Kurlender

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first
  [2nd Edition: p 75, 3rd Edition: p 87]
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm 
  [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  """
  "*** YOUR CODE HERE ***"
##  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
##  print "Start's successors:", problem.getSuccessors(problem.getStartState())
##  stack = util.Stack()
##  stack.push("test")
##  print stack.pop()

  fringe = util.Stack()
  fringe.push((problem.getStartState(), []))
  explored = set()

  while fringe.isEmpty() != True:
    curr_state,path = fringe.pop()
    if curr_state not in explored:
      if problem.isGoalState(curr_state) == True:
        return path
      explored.add(curr_state)
      successors = problem.getSuccessors(curr_state)
      for successor, action, stepCost in successors:
        fringe.push((successor, path+[action]))
      

def breadthFirstSearch(problem):
  """
  Search the shallowest nodes in the search tree first.
  [2nd Edition: p 73, 3rd Edition: p 82]
  """
  "*** YOUR CODE HERE ***"
  fringe = util.Queue()
  fringe.push((problem.getStartState(), []))
  explored = set()

  while fringe.isEmpty() != True:
    curr_state,path = fringe.pop()
    if curr_state not in explored:
      if problem.isGoalState(curr_state) == True:
        print curr_state
        return path
      explored.add(curr_state)
      successors = problem.getSuccessors(curr_state)
      for successor, action, stepCost in successors:
        fringe.push((successor, path+[action]))
        print successor
  # print action
      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  
  frontier = util.PriorityQueue()
  frontier.push((problem.getStartState(), [], 0), 0)
  explored = set()

  while not frontier.isEmpty():
    (curr_state,path, cost_before) = frontier.pop()
    if curr_state not in explored:
      if problem.isGoalState(curr_state):
        return path
      explored.add(curr_state)
      print(curr_state)
      successors = problem.getSuccessors(curr_state)
      for successor, action, stepCost in successors:
        frontier.push((successor, path+[action], cost_before+stepCost), cost_before+stepCost)
  

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  frontier = util.PriorityQueue()
  frontier.push((problem.getStartState(), [], 0), 0)
  # start state, action, cost, heuristic cost
  explored = set()

  while not frontier.isEmpty():
    (curr_state,path, cost) = frontier.pop()
    if curr_state not in explored:
      if problem.isGoalState(curr_state):
        return path
      explored.add(curr_state)
      print(curr_state)
      successors = problem.getSuccessors(curr_state)
      for successor, action, stepCost in successors:
        frontier.push((successor, path+[action], cost+stepCost), cost+stepCost+heuristic(successor,problem))

  print "Start state heuristic value is: ", heuristic(problem.getStartState(), problem)
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
