from game import *
from copy import *

class State:
    '''
    state:

    grid of attempted shots
    which ships are sunk
    number of attempts
    '''

    def __init__(self, game):
        self.game = game
        self.attempts = game.attempts
        self.sunk_ships = game.sunk_ships
        self.numAttempts = 0

'''
class MC:
    def getTransitionProb(self, state, action, new_state):
        return float(1)/(state.game.width * state.game.height - state.numAttempts)
'''


class QLearningAlgorithm:
    def __init__(self, actions, discount, featureExtractor, explorationProb=0.2):
        self.actions = actions
        self.discount = discount
        self.featureExtractor = featureExtractor
        self.explorationProb = explorationProb
        self.weights = defaultdict(float)
        self.numIters = 0

    def identityFeatureExtractor(state, action):
        featureKey = (state, action)
        featureValue = 1
        return [(featureKey, featureValue)]

    # Return the Q function associated with the weights and features
    def getQ(self, state, action):
        score = 0
        for f, v in self.featureExtractor(state, action):
            score += self.weights[f] * v
        return score

    # This algorithm will produce an action given a state.
    # Here we use the epsilon-greedy algorithm: with probability
    # |explorationProb|, take a random action.
    def getAction(self, state):
        self.numIters += 1
        if random.random() < self.explorationProb:
            return random.choice(self.actions(state))
        else:
            return max((self.getQ(state, action), action) for action in self.actions(state))[1]

    # Call this function to get the step size to update the weights.
    def getStepSize(self):
        return 1.0 / math.sqrt(self.numIters)

    def copyTuple(self, oldTuple, indexToChange, newValue):
        newTuple = ()
        for i in range(len(oldTuple)):
            if i == indexToChange:
                newTuple += (newValue,)
            else:
                newTuple += (oldTuple[i],)
        return newTuple

    # We will call this function with (s, a, r, s'), which you should use to update |weights|.
    # Note that if s is a terminal state, then s' will be None.  Remember to check for this.
    # You should update the weights using self.getStepSize(); use
    # self.getQ() to compute the current estimate of the parameters.
    def incorporateFeedback(self, state, action, reward, newState):
        # BEGIN_YOUR_CODE (our solution is 12 lines of code, but don't worry if you deviate from this)
        phi = self.featureExtractor(state, action)
        Q = self.getQ(state, action)
        eta = self.getStepSize()
        Vopt = max(self.getQ(newState, newAction) for newAction in self.actions(newState))
        if newState == None:
            Vopt = 0
        intermediateValue = (eta * (Q - (reward + self.discount * Vopt)))
        for i in range(len(phi)):
            phi[i] = self.copyTuple(phi[i], 1, intermediateValue * phi[i][1])

        for f, v in phi:
            self.weights[f] -= v
        # END_YOUR_CODE

game = Grid()
state = State(game)
new_state = state.generateSuccessor((0,0))
