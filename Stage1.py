from game import *
import math

'''
class MC:
    def getTransitionProb(self, state, action, new_state):
        return float(1)/(state.width * state.height - state.numAttempts)
'''


class QLearningAlgorithm:
    def __init__(self, mdp, discount, explorationProb=0.2):
        self.mdp = mdp
        self.discount = discount
        self.featureExtractor = self.identityFeatureExtractor
        self.explorationProb = explorationProb
        self.weights = defaultdict(float)
        self.numIters = 0

    def identityFeatureExtractor(self, state, action):
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
        actions = self.mdp.getLegalActions(state)
        if actions == []:
            return None
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
        newStateActions = self.mdp.getLegalActions(newState)
        if newStateActions == []:
            Vopt = 0
        else:
            Vopt = max(self.getQ(newState, newAction) for newAction in newStateActions)
        if newState == None:
            Vopt = 0
        intermediateValue = (eta * (Q - (reward + self.discount * Vopt)))
        for i in range(len(phi)):
            phi[i] = self.copyTuple(phi[i], 1, intermediateValue * phi[i][1])

        for f, v in phi:
            self.weights[f] -= v
        # END_YOUR_CODE

def simulate(mdp, rl, numTrials=10, maxIterations=1000, verbose=False,
             sort=False):
    # Return i in [0, ..., len(probs)-1] with probability probs[i].
    def sample(probs):
        target = random.random()
        accum = 0
        for i, prob in enumerate(probs):
            accum += prob
            if accum >= target: return i
        raise Exception("Invalid probs: %s" % probs)

    totalRewards = []  # The rewards we get on each trial
    for trial in range(numTrials):
        state = mdp.start
        sequence = [state]
        totalDiscount = 1
        totalReward = 0
        for _ in range(maxIterations):
            action = rl.getAction(state)
            transitions = mdp.succAndProbReward(state, action)
            if sort: transitions = sorted(transitions)
            if len(transitions) == 0:
                rl.incorporateFeedback(state, action, 0, None)
                break

            # Choose a random transition
            i = sample([prob for newState, prob, reward in transitions])
            newState, prob, reward = transitions[i]
            sequence.append(action)
            sequence.append(reward)
            sequence.append(newState)

            rl.incorporateFeedback(state, action, reward, newState)
            totalReward += totalDiscount * reward
            totalDiscount *= mdp.discount()
            state = newState
        if verbose:
            print "Trial %d (totalReward = %s): %s" % (trial, totalReward, sequence)
        totalRewards.append(totalReward)
    return totalRewards


mdp = MDP()
#print("beginning compute states")
#mdp.computeStates()
#print("finished compute states")
rl = QLearningAlgorithm(mdp, 0.95, 0.2)
# We call this here so that the stepSize will be 1
print("beginning simulate")
simulate(mdp, rl, 100, verbose=True)
print("finished simulate")
