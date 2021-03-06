# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

# look at GameState (a class) and AgentState (a class) in pacman.py and game.py
# get a bunch of numbers from the agent and game states and then play around with them
# use manhattan distances, other things

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        gameScore = successorGameState.getScore()
        newFood = newFood.asList()
        for food in newFood:
          if util.manhattanDistance(food, newPos) < 2:
            gameScore += 10
          gameScore += 1/(util.manhattanDistance(food, newPos)+1)

        smallest_dist = float("inf")
        newGhostPos = successorGameState.getGhostPositions()
        for pos in newGhostPos:
          if (util.manhattanDistance(pos, newPos)) < smallest_dist:
            smallest_dist = util.manhattanDistance(pos, newPos)
        if smallest_dist < 2:
          gameScore -= 20

        return gameScore


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        def maxvalue(gameState, depth):
            player_num = depth % gameState.getNumAgents()
            ply_num = depth // gameState.getNumAgents()

            # either game is over or we reach maximum depth
            if ply_num == self.depth or gameState.isWin() or gameState.isLose():
              return self.evaluationFunction(gameState) 

            actions = gameState.getLegalActions(0)
            mv = float("-inf")
            for action in actions:
              successor = gameState.generateSuccessor(0, action)
              mv = max(mv, minvalue(successor,depth+1))

            # print " "*depth, ply_num, mv
            return mv


        def minvalue(gameState, depth):
            player_num = depth % gameState.getNumAgents()
            ply_num = depth // gameState.getNumAgents()

            miv = float("inf")

            if ply_num == self.depth or gameState.isWin() or gameState.isLose():
              return self.evaluationFunction(gameState)
              
            actions = gameState.getLegalActions(player_num)
            for action in actions:
              successor = gameState.generateSuccessor(player_num, action)
              if player_num == (gameState.getNumAgents() - 1):
                miv = min(miv, maxvalue(successor,depth+1))
              else:
                miv = min(miv, minvalue(successor,depth+1))
            # print " "*depth, ply_num, miv
            return miv

        depth = 0
        player_num = depth % gameState.getNumAgents()
        actions = gameState.getLegalActions(0)
        miv = float("-inf")
        act2 = ""
        for action in actions:
          successor = gameState.generateSuccessor(player_num, action)
          
          b = minvalue(successor, depth+1)
          if (miv < b):
            act2 = action
            miv = b
        return act2


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def maxvalue_ex(gameState, depth):
            player_num = 0
            ply_num = 0
            player_num = depth % gameState.getNumAgents()
            ply_num = depth // gameState.getNumAgents()

            # either game is over or we reach maximum depth
            if ply_num == self.depth or gameState.isWin() or gameState.isLose():
              return self.evaluationFunction(gameState) 

            actions = gameState.getLegalActions(0)
            mv = float("-inf")
            for action in actions:
              successor = gameState.generateSuccessor(0, action)
              mv = max(mv, expectedLevel_ex(successor,depth+1))

            # print " "*depth, ply_num, mv
            return mv


        def expectedLevel_ex(gameState, depth):
          player_num = 0
          ply_num = 0
          player_num = depth % gameState.getNumAgents()
          ply_num = depth // gameState.getNumAgents()  

          ev = 0

          if gameState.isWin() or gameState.isLose() or ply_num == self.depth:
              return self.evaluationFunction(gameState)
          else:
            actions = gameState.getLegalActions(player_num)
            for action in actions:
              successor = gameState.generateSuccessor(player_num, action)
              if player_num == (gameState.getNumAgents() - 1):
                ev += maxvalue_ex(successor,depth+1)
              else:
                ev += expectedLevel_ex(successor,depth+1)
            # print " "*depth, ply_num, miv
            return (ev)*(1/float(len(actions)))



        depth = 0
        player_num = depth % gameState.getNumAgents()
        actions = gameState.getLegalActions(0)
        miv = float("-inf")
        act2 = ""
        for action in actions:
          successor = gameState.generateSuccessor(player_num, action)
          b = expectedLevel_ex(successor, depth+1)
          if (miv < b):
            act2 = action
            miv = b
        return act2

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    cap = len(currentGameState.getCapsules())

    successorGameState = currentGameState
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    gameScore = successorGameState.getScore()
    newFood = newFood.asList()
    for food in newFood:
      if util.manhattanDistance(food, newPos) < 2:
        gameScore += 5
      gameScore += 1/(util.manhattanDistance(food, newPos)+1)

    smallest_dist = float("inf")
    newGhostPos = successorGameState.getGhostPositions()
    for pos in newGhostPos:
      if (util.manhattanDistance(pos, newPos)) < smallest_dist:
        smallest_dist = util.manhattanDistance(pos, newPos)
    if smallest_dist < 3:
      gameScore -= 10 

    return gameScore - 110*(cap)
  

# Abbreviation
better = betterEvaluationFunction

