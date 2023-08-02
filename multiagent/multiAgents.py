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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
          
        
        total = currentGameState.getScore() #Current score in the game that we will be comparing to

        oldPos = currentGameState.getPacmanPosition()

        x = successorGameState.getGhostPositions()  #a list of ghost positions but since for these tests there usually only 1 we just worry about x[0]

        oldDistGhost = manhattanDistance(oldPos, x[0])  #distance to ghost given old position
        newDistGhost = manhattanDistance(newPos, x[0])  #distance to ghost given new position

        temp = (random.randint(0,100),random.randint(0,100)) #This is initialized to a random coridinate since any constant makes pacman get stuck in a corner
        for pos in newFood.asList():
            if manhattanDistance(newPos,pos ) <  manhattanDistance(newPos,temp ):   #keeps track of closest food pellet
                temp = pos

        if manhattanDistance(newPos, temp) < manhattanDistance(oldPos, temp):   #if action will take you closer to the food pellet, total + 14
            total = total + 14  
            if manhattanDistance(newPos, x[0]) > 4:                             #if the ghost is far from pacman, then add a random amount to total, to be more risk prone
                total = total + manhattanDistance(newPos, x[0])

        if newScaredTimes[0] == 0:                                              #if ghosts are not scared and the old distance to the ghost is more than the new dist. then total - 13
            if oldDistGhost > newDistGhost:
                total = total - 13

        if newPos == oldPos:                                                    #if the action provided is to just stay still, then total -14
            total = total - 14

        if  manhattanDistance(newPos, temp) >=  manhattanDistance(x[0], temp):  #if the ghost is closer to the food pellet than pacman, total - a random int
               total = total -  random.randint(0,3)

        return total

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def getMax(depth , state):
            value = -100000000000000000.00
            diction = {}
            if state.isLose() or state.isWin() or depth == self.depth:  #These are our terminal points and where we will be going up the call stack
                return self.evaluationFunction(state)
            if depth == 0:#if we are at depth 0, then this means it is time to return our action and not a score so we find the corrosponding score and action
                for action in state.getLegalActions(0):
                    diction.update({(getMin(depth, state.generateSuccessor(0, action), 1)) : action})   
                return diction[max(diction)]    #Here a dictionary is used in order to keep track of the actions and value. Not much space is used since it is only kept for the first depth
            for action in state.getLegalActions(0):
                value = max(value, (getMin(depth, state.generateSuccessor(0, action), 1)))  #we are calling for a max of all possible game states given the possible actions of the ghosts
            return value
       

        def getMin(depth , state, nums):
            value = 100000000000000000.00
            
            if state.isLose() or state.isWin(): #or (depth == self.depth) :
                return self.evaluationFunction(state)
            elif nums == gameState.getNumAgents()-1: # the agent in question here is pacman
                for action in state.getLegalActions(nums):
                    value = min(value, getMax(depth +1, state.generateSuccessor(nums, action)))  #we are calling for a min of all possible game states given the possible actions of pacman
                return value
            else:    
                for action in state.getLegalActions(nums):
                    value = min(value, getMin(depth, state.generateSuccessor(nums, action), nums+1)) #we are calling for a min of all possible game states given the possible actions of the other ghosts
                return value


        return getMax(0 ,gameState)

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """

        '''
        This code works very similar to the min max except now we are pruning. Most of the added code is taken from the slides pseudocode. 
        
        '''
        "*** YOUR CODE HERE ***"
        def getMax(depth , state, alpha, beta):
            value = -100000000000000000.00
            diction = {}
            if state.isLose() or state.isWin() or depth == self.depth:
                return self.evaluationFunction(state)
            if depth == 0:# if we are at depth 0, then this means it is time to return our action and not a score so we find the corrosponding score and action
                for action in state.getLegalActions(0):
                    value = getMin(depth, state.generateSuccessor(0, action), 1, alpha, beta)
                    diction.update({value : action}) #Here a dictionary is used in order to keep track of the actions and value. Not much space is used since it is only kept for the first depth
                    if value > beta: #we will never chose beta if it is less than value since we want to maximize here
                        return value
                    alpha = max(alpha, value)  
                return diction[max(diction)]
            for action in state.getLegalActions(0):
                value = max(value, (getMin(depth, state.generateSuccessor(0, action), 1, alpha, beta)))
                if value > beta:
                    return value
                alpha = max(alpha, value) 
            return value
       

        def getMin(depth , state, nums, alpha, beta):
            value = 100000000000000000.00
            
            if state.isLose() or state.isWin(): #or (depth == self.depth) :
                return self.evaluationFunction(state)
            elif nums == gameState.getNumAgents()-1: #if agent num = 0 then the agent in question is pacman
                for action in state.getLegalActions(nums):
                    value = min(value, getMax(depth +1, state.generateSuccessor(nums, action), alpha, beta))
                    if value < alpha:
                        return value
                    beta = min(beta, value)
                return value
            else:    
                for action in state.getLegalActions(nums):
                    value = min(value, getMin(depth, state.generateSuccessor(nums, action), nums+1, alpha, beta))
                    if value < alpha: #we will never chose alpha if it is more than value since we want to minimize here
                        return value
                    beta = min(beta, value)
                return value


        return getMax(0 ,gameState, -1000000000000000000 , 1000000000000000000)

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

        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        '''
        So this code is very similar to min max search so a lot of that code is resused. The biggest difference is that the value of nodes is now the expected value of termincal points.
        This means that the value of get min nodes is now the sum of the terminal nodes divided by the amount of possible sucessors. This is why it is "return value/len(state.getLegalActions(nums))"
        
        '''

        "*** YOUR CODE HERE ***"
        def getMax(depth , state):
            value = 0
            diction = {}
            if state.isLose() or state.isWin() or depth == self.depth:
                return self.evaluationFunction(state)
            if depth == 0:#if we are at depth 1, then this means it is time to return our action and not a score so we find the corrosponding score and action
                for action in state.getLegalActions(0):
                    diction.update({(getMin(depth, state.generateSuccessor(0, action), 1)) : action})   
                return diction[max(diction)]
            for action in state.getLegalActions(0):
                value = max(value, (getMin(depth, state.generateSuccessor(0, action), 1)))
            return value
       

        def getMin(depth , state, nums):
            value = 0
            
            if state.isLose() or state.isWin(): #or (depth == self.depth) :
                return self.evaluationFunction(state)
            elif nums == gameState.getNumAgents()-1: #if agent num = 0 then the agent in question is pacman
                for action in state.getLegalActions(nums):
                    value = value + getMax(depth +1, state.generateSuccessor(nums, action))
                return value/len(state.getLegalActions(nums))
            else:    
                for action in state.getLegalActions(nums):
                    value = value + getMin(depth, state.generateSuccessor(nums, action), nums+1)
                return value/len(state.getLegalActions(nums))


        return getMax(0 ,gameState)

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """

    '''
    so the way this evaluator works is by doing simple addition and subtraction. Less food pellets on the board game mean higher value in score. The reason I chose 400 is because it gave 
    the right weight to the food without making food more imporant than being cautious of the ghost. If the distance to the ghost is greater than 2, then the score gets increased
    by a random number between 4 and 11. By doing it this way, we can also add some randomness into pacman's moves. This helps in preventing pacman from being too cautious all the time.
    If the distance from the ghost is less than 2 then we subtract a random amount between 8 and 11. This makes it so being in states close to the ghost aren't welcome. 
    Finally if the ghost is scared then we decide to be super agressive with our actions.
    '''

    "*** YOUR CODE HERE ***"
    value = 0
    newFood = currentGameState.getFood()
    newPos = currentGameState.getPacmanPosition()
    newGhostStates = currentGameState.getGhostStates()
    distGhost = manhattanDistance(newPos, currentGameState.getGhostPositions()[0])


    value = value + (550 - newFood.count(True)) 
    
    if distGhost > 2:
        value = value + random.randint(4,11)

    if distGhost < 2:
        value = value - random.randint(8,11)
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    if newScaredTimes[0] != 0:                                             
        value = value + 1000

    return value

# Abbreviation
better = betterEvaluationFunction
