# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        for count in range(self.iterations):
          val = self.values.copy()
          for state in self.mdp.getStates():
              value = util.Counter()
              for action in self.mdp.getPossibleActions(state):
                  for probState, probability in self.mdp.getTransitionStatesAndProbs(state, action):
                      value[action] += probability * (self.mdp.getReward(state, action, probState) + self.discount * val[probState])
              self.values[state] = value[value.argMax()]


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        value = 0
        
        for probState, probability in  self.mdp.getTransitionStatesAndProbs(state,action):
          value = value + probability * (self.mdp.getReward(state, action, probState) + (self.discount * self.values[probState]))

        return value
        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        possibleAct = self.mdp.getPossibleActions(state)
        if '' in possibleAct:
            return None

        values = util.Counter()
        for action in possibleAct:
            for probState, probability in self.mdp.getTransitionStatesAndProbs(state, action):
                values[action] += probability * (self.mdp.getReward(state, action, probState) + self.discount * self.values[probState])

        return values.argMax()
        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        
        counter = 0

        while counter < self.iterations:
          for state in self.mdp.getStates():
            stateQ = util.Counter()
            
            for action in self.mdp.getPossibleActions(state):
              stateQ[action] = self.computeQValueFromValues(state, action)
            
            self.values[state] = stateQ[stateQ.argMax()]
            
            counter += 1
            if counter >= self.iterations:
              return None


class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

        mdp = self.mdp
        values = self.values
        discount = self.discount
        iterations = self.iterations
        theta = self.theta
        states = mdp.getStates()


        previous = {} 
        for state in states:
          previous[state] = set()

        queuey = util.PriorityQueue()

       
        for state in states:
          counts = util.Counter()

          for action in mdp.getPossibleActions(state):
            
             
            for (possibleState, prob) in mdp.getTransitionStatesAndProbs(state, action):
              if prob != 0:
                previous[possibleState].add(state)

            counts[action] = self.computeQValueFromValues(state, action)

          if not mdp.isTerminal(state): 
            maxcounts = counts[counts.argMax()]
            diff = abs(values[state] - maxcounts)
            queuey.update(state, -diff)


        
        for i in range(iterations):
          if queuey.isEmpty():
            return

          state = queuey.pop()

          if not mdp.isTerminal(state):
            counts = util.Counter()
            for action in mdp.getPossibleActions(state):
              counts[action] = self.computeQValueFromValues(state, action)

            values[state] = counts[counts.argMax()]

          for pobState in previous[state]:
            Q_p = util.Counter()
            for action in mdp.getPossibleActions(pobState):
              
              Q_p[action] = self.computeQValueFromValues(pobState, action)

            
            maxQ_p = Q_p[Q_p.argMax()]
            diff = abs(values[pobState] - maxQ_p)
              
            if diff > theta:
              queuey.update(pobState, -diff)

