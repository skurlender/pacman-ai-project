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

        # Write value iteration code here
        # states = 
        for i in range(self.iterations):
            count_states = util.Counter()
            for state in self.mdp.getStates():
                action = self.getAction(state)
                if action != None:
                    count_states[state]=self.getQValue(state, action)
            self.values = count_states
                

# I would try running value iteration for 1, then 2, then 3, then 4, then 5 iterations and checking against 
# the followup in this post: @149. Are the values right at the first iteration? The second? Where do the 
# errors start to be introduced? Note that you can click on the image of the gridworld and press a key 
# (might have to be enter?) to get the q-values to show up, so that you can see what is going on in even 
# more detail.



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
        t_states = self.mdp.getTransitionStatesAndProbs(state, action)
        qval = 0.0
        for (ts, prob) in t_states:
            qval += prob*(self.mdp.getReward(state, action, ts) + (self.discount*self.getValue(ts)))
        return qval

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        maxv = -float("inf")
        maxa = None
        if self.mdp.isTerminal(state):
            return None

        count_actions = util.Counter()
        actions = self.mdp.getPossibleActions(state)
        for action in actions:
            count_actions[action] = self.computeQValueFromValues(state, action)

        return count_actions.argMax()


        # actions = self.mdp.getPossibleActions(state)
        # for action in actions:
        #     if (maxv <= self.getQValue(state, action)):
        #         maxv = self.getQValue(state, action)
        #         maxa = action
        # return action

            

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
