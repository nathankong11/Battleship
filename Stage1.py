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

    def generateSuccessor(self, action):
        new_game = deepcopy(game)
        new_state = State(new_game)
        x, y = action

        new_state.game.shoot(x,y)
        new_state.attempts = new_state.game.attempts
        new_state.sunk_ships = new_state.game.sunk_ships
        new_state.numAttempts = self.numAttempts + 1

        return new_state

    def isEnd(self):
        return self.game.gameOver()

    def getLegalActions(self):
        return self.game.getLegalShots()

class MC:
    def getTransitionProb(self, state, action, new_state):
        return float(1)/(state.game.width * state.game.height - state.numAttempts)

    def getReward(self, state, action, new_state):
        if new_state.isEnd():
            return 100
        if state.game.shipAt(action[0],action[1]):
            return 2
        return -1

class QLearningAlgorithm:
    def __init__(self, discount, explorationProb=0.2):
        self.discount = discount
        self.featureExtractor = self.identityFeatureExtractor
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
        actions = state.getLegalActions()
        if random.random() < self.explorationProb:
            return random.choice(actions)
        else:
            return max((self.getQ(state, action), action) for action in actions)[1]

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
        newStateActions = newState.getLegalActions()
        Vopt = max(self.getQ(newState, newAction) for newAction in newStateActions)
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
