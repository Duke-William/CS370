# search.py
# ---------
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
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    """
    Code Explanation:

    The way my code works is it first makes a stack and pushes the first node onto it. After that it loops through the stack, popping the top element and getting its successors. Those new nodes then
    get added to the stack and this continues while keeping track of any visited nodes. A dictionary (parentRecored) is used with the key being the child nodes and the return value being the parrent 
    and the path from the parent to the child. The path is not made until the end. When the current node is found to be the goal state, the pathList gets made from checking the current node in the 
    dictionary and getting the parrent node. This gets checked until we reach the start node in which we now have a list of paths from end to start. From there we just reverse the list and return.



    """
    visited = set()
    pathList = []
    parentRecored = {}
    stacky = util.Stack()
    node = problem.getStartState()
    nodes = node
    stacky.push(nodes)
    while not stacky.isEmpty():
        nodes = stacky.pop()
        if nodes not in visited:
            visited.add(nodes)
            if  problem.isGoalState(nodes):
                x = nodes
                while x != node:
                    (parent, totalPath) = parentRecored[x]
                    if x != parent:
                        pathList.append(totalPath)
                        x = parent
                    
                pathList.reverse()    
                break
            y = problem.getSuccessors(nodes)
            for holder in y:
                (child , path , cost) = holder
                if child not in visited:
                    parentRecored[child] = (nodes, path)
                stacky.push(child)
                
    
    return pathList

    util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    """
    Code Explanation:

    The way my code works is it first makes a stack and pushes the first node onto it. After that it loops through the queue, popping the first element and getting its successors. Those new nodes then
    get added to the queue and this continues while keeping track of any visited nodes. A dictionary (parentRecored) is used with the key being the child nodes and the return value being the parrent 
    and the path from the parent to the child. The path is not made until the end. When the current node is found to be the goal state, the pathList gets made from checking the current node in the 
    dictionary and getting the parrent node. This gets checked until we reach the start node in which we now have a list of paths from end to start. From there we just reverse the list and return.



    """

    visited = set()
    pathList = []
    parentRecored = {}
    q_ey = util.Queue()
    node = problem.getStartState()
    nodes = node
    q_ey.push(nodes)
    while not q_ey.isEmpty():
        nodes = q_ey.pop()
        if nodes not in visited:
            visited.add(nodes)
            if  problem.isGoalState(nodes):
                x = nodes
                while x != node:
                    (parent, totalPath) = parentRecored[x]
                    if x != parent:
                        pathList.append(totalPath)
                        x = parent      
                pathList.reverse()   
                break
            y = problem.getSuccessors(nodes)
            for holder in y:
                (child , path , cost) = holder
                if child not in visited:
                    if child not in parentRecored:
                        parentRecored[child] = (nodes, path)
                q_ey.push(child)
                
    
    return pathList
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    """
    Code Explanation:

    Originally I tried to use the same method that I used in BFS and DFS but I ran into the problem that I could not compare total costs of paths until the end. This meant that while
    comparing total costs of locals paths I could not take into account the total cost differences. Even if I am able to solve those differences, I am not able to maintain the path
    those costs belong to. After this I tried to look for another way to maintain total paths and cost of total paths at the same time.

    First try at it:

    import time
    visited = set()
    pathList = []
    parentRecored = {}
    priorityQ_ey = util.PriorityQueue()
    node = problem.getStartState()
    nodes = node
    priorityQ_ey.push((nodes, 0 ), 0)
    counter = 1
    totalCost = 0
    while True:

        for depth in range(counter):
            (nodes, totalCost) = priorityQ_ey.pop()
            if  nodes not in visited:
                visited.add( nodes)
                if  problem.isGoalState( nodes):
                    x =  nodes                                                         #Since I am maintaining paths and costs already this part of the code is not needed
                    while x != node:
                        (parent, totalPath) = parentRecored[x]
                        if x != parent:
                            pathList.append(totalPath)
                        x = parent
                    pathList.reverse()   
                    return pathList
                y = problem.getSuccessors( nodes)
            
                for holder in y:
                
                    (child , path , cost) = holder
                    if child not in visited:
                        parentRecored[child] = ( nodes, path)                           #These prints and sleep can be ignored, they were just used in debugging
                        print('totalCost = ', totalCost)
                        print('totalCost+ cost = ', totalCost + cost)
                        print(nodes, ' ->', child)
                        time.sleep(3)
                    priorityQ_ey.push((child,totalCost + cost) , totalCost + cost)       #At this point I realized no matter what I did I needed to find a way to keep track of paths and costs at
            counter = counter +1                                                         #the same time because otherwise it will only chose the locally smallest cost but not the overall best
            if not priorityQ_ey.isEmpty():
                break
               
    
    return pathList
    """
    """
    The way this code works is by having a prority queue (priorityQ_ey read: Queue - E) hold the nodes. We start off with our start state and then push it to the queue. Unlike the
    previous ways of using a queue, this time the queue not only holds the node but instead it holds a triple with the node, total cost and the total path to get to said node.
    This makes it possible to compare one totalpath to another. In my previous attempt I was only able to compare costs of local paths. This means I do not need to have a dictionary holding
    paths from a parrent node to a child since I am keeping the paths from the start.

    """

    priorityQ_ey = util.PriorityQueue()
    visited = set()
    node = problem.getStartState()  
    path= []
    priorityQ_ey.push((node,0,path) , 0)

    while not priorityQ_ey .isEmpty():
        (nodes, cost, path) = priorityQ_ey.pop()
        if problem.isGoalState(nodes):
            return path
        if not nodes in visited:
            visited.add(nodes)
            for x in problem.getSuccessors(nodes):
                totalCost = cost + x[2]
                totalPath = path + [x[1]]
                newNode = (x[0], totalCost, totalPath)
                priorityQ_ey.push(newNode,totalCost)

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    """
    This code works just like uniform cost except this time the total cost = totalPathCost so far + node.

    """


    priorityQ_ey = util.PriorityQueue()
    visited = set()
    node = problem.getStartState()  
    path= []
    priorityQ_ey.push((node,0,path) , 0)

    while not priorityQ_ey .isEmpty():
        (nodes, cost, path) = priorityQ_ey.pop()
        if problem.isGoalState(nodes):
            return path
        if not nodes in visited:
            visited.add(nodes)
            for x in problem.getSuccessors(nodes):
                totalCost = (cost + x[2])
                totalPath = path + [x[1]]
                newNode = (x[0], totalCost, totalPath)
                priorityQ_ey.push(newNode,totalCost + heuristic(x[0], problem))


    util.raiseNotDefined()




# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
