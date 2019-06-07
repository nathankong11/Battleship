import random
from copy import *
import pickle
from collections import *
import math
import time

class State:
    """
    A 2-dimensional array. Data is accessed
    via grid[x][y] where (x,y) are positions with x horizontal,
    y vertical and the origin (0,0) in the top left corner.

    ships[x][y]:
    None: empty
    destroyer: (2 hole ship)
    submarine: (3 hole ship)
    cruiser: (3 hole ship)
    battleship: (4 hole ship)
    carrier: (5 hole ship)

    attempts[x][y]:
    0: no attempt
    1: miss
    2: hit
    """

    def __init__(self, size = 10):
        if size < 5:
            raise Exception('size should be at least 5. The value of size was: {}'.format(size))

        self.width = size
        self.height = size
        self.ship_size = {
        'destroyer': 2,
        'submarine': 3,
        'cruiser': 3,
        'battleship': 4,
        'carrier': 5,
        }

        self.ships = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.attempts = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.num_attempts = 0
        self.num_hit = 0
        self.num_miss = 0
        self.num_sunk = 0
        self.num_consecutive_miss = 0
        self.ship_hits = {
        'destroyer': 0,
        'submarine': 0,
        'cruiser': 0,
        'battleship': 0,
        'carrier': 0,
        }
        self.sunk_ships = {
        'destroyer': 0,
        'submarine': 0,
        'cruiser': 0,
        'battleship': 0,
        'carrier': 0,
        }

    # returns if (x,y) is inside the grid
    def inside(self, x, y):
        return x >= 0 and x < self.width and y >= 0 and y < self.height

    def shipSize(self, ship):
        return self.ship_size[ship]

    def shipHits(self, ship):
        return self.ship_hits[ship]

    # return if there is a ship at (x,y)
    def shipAt(self, x, y):
        if self.ships[x][y] == None:
            return False
        return True

    # return if there is an attempt at (x,y)
    def attemptAt(self, x,y):
        if self.attempts[x][y] == 0:
            return False
        return True

    # updates sunk_ships and returns 1 if sunk ship
    def sunkShip(self, ship):
        sunk_ship = self.ship_size[ship] == self.ship_hits[ship]
        self.sunk_ships[ship] = sunk_ship
        return sunk_ship

    # returns 1 if placement is legal
    def legalPlacement(self, x, y):
        return self.inside(x, y) and not self.shipAt(x, y)

    # attempts to place a ship. Returns true if successful
    def placeShip(self, ship, x, y, direction):
        coords = []
        for n in range(self.ship_size[ship]):
            x1 = x
            y1 = y
            if direction == 'up':
                y1 += n
            if direction == 'down':
                y1 -= n
            if direction == 'left':
                x1 -= n
            if direction == 'right':
                x1 += n
            if not self.legalPlacement(x1, y1):
                return False
            coords.append((x1, y1))
        for coord in coords:
            self.ships[coord[0]][coord[1]] = ship
        return True

    # randomly places ships on the grid
    def randomPlacement(self):
        for ship in self.ship_size:
            successful = False
            while not successful:
                x = random.randint(0, self.width-1)
                y = random.randint(0, self.height-1)
                direction = ['up', 'down', 'left', 'right']
                successful = self.placeShip(ship, x, y, random.choice(direction))

    # returns 1 if shot is legal
    def legalShot(self, x,y):
        return self.inside(x,y) and self.attempts[x][y] == 0

    # Makes an attempt at (x,y) Returns 0 if miss, 1 if hit, or size of ship if sunk ship. Returns -1 if invalid shot
    def shoot(self, x,y):
        # if illegal shot
        if not self.legalShot(x,y):
            return -1
        self.num_attempts += 1
        # if hit
        if self.shipAt(x,y):
            self.num_hit += 1
            self.num_consecutive_miss = 0
            self.attempts[x][y] = 2
            ship = self.ships[x][y]
            self.ship_hits[ship] += 1

            # if sunk
            if self.sunkShip(ship):
                self.num_sunk += 1
                return self.ship_size[ship]
            return 1
        # if miss
        else:
            self.num_miss += 1
            self.num_consecutive_miss += 1
            self.attempts[x][y] = 1
            return 0

    # randomly shoots on the grid
    def randomShoot(self):
        successful = False
        while not successful:
            x = random.randint(0, self.width-1)
            y = random.randint(0, self.height-1)
            successful = self.shoot(x,y) > -1

    # returns a list of coords of legal shots that can be taken
    def getLegalShots(self):
        coords = []
        for x in range(self.width):
            for y in range(self.height):
                if self.legalShot(x,y):
                    coords.append((x,y))
        return coords

    # returns 1 if game is over
    def isEnd(self):
        return self.num_sunk == 5

    # Prints the state of all the ships on the grid
    def printShips(self):
        out = ''
        for x in range(len(self.ships)):
            for y in range(len(self.ships[x])):
                ship = self.ships[x][y]
                out += '' + str(0) if ship == None else str(self.ship_size[ship])
                out += ' '
            if x < len(self.ships) - 1:
                out += '\n'
        print out

    # Prints the state of all the attempts on the grid
    def printAttempts(self):
        out = ''
        for x in range(len(self.attempts)):
            for y in range(len(self.attempts[x])):
                out += '' + str(self.attempts[x][y])
                out += ' '
            if x < len(self.attempts) - 1:
                out += '\n'
        print out

    # Resets the grid to default state
    def reset(self):
        self.ships = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.attempts = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.num_attempts = 0
        self.num_hit = 0
        self.num_miss = 0
        self.num_sunk = 0
        self.num_consecutive_miss = 0
        self.ship_hits = {
        'destroyer': 0,
        'submarine': 0,
        'cruiser': 0,
        'battleship': 0,
        'carrier': 0,
        }
        self.sunk_ships = {
        'destroyer': 0,
        'submarine': 0,
        'cruiser': 0,
        'battleship': 0,
        'carrier': 0,
        }

class MDP:
    def __init__(self, size = 10):
        self.start = self.startState(size)
    # Return the start state.
    def startState(self, size):
        state = State(size)
        state.randomPlacement()
        return state

    # Return set of actions possible from |state|.
    def getLegalActions(self, state):
        if state == None:
            return []
        return state.getLegalShots()

    def generateSuccessor(self, state, action):
        if state.isEnd():
            return None

        new_state = deepcopy(state)
        x, y = action
        new_state.shoot(x,y)
        return new_state

    # Return a reward for taking an action from state to new_state
    def getReward(self, state, action, new_state):
        if new_state.isEnd():
            return 1000 / state.num_attempts
        if state.shipAt(action[0],action[1]):
            return 2
        return -1

    # Return a list of (new_state, prob, reward) tuples corresponding to edges
    # coming out of |state|.
    # Mapping to notation from class:
    #   state = s, action = a, new_state = s', prob = T(s, a, s'), reward = Reward(s, a, s')
    # If IsEnd(state), return the empty list.
    def succAndProbReward(self, state, action):
        if state.isEnd():
            return []
        if action == None:
            return []
        new_state = self.generateSuccessor(state, action)
        if new_state == None:
            return []
        return [(new_state, 1.0, self.getReward(state, action, new_state))]

    def discount(self):
        return 1.0

class QLearningAlgorithm:
    def __init__(self, discount, explorationProb=0.2):
        self.discount = discount
        self.featureExtractor = self.identityFeatureExtractor
        self.explorationProb = explorationProb
        self.weights = defaultdict(float)
        self.numIters = 0

    def isAdjacent(self, state, action):
        adjacent = 0
        if action == None:
            return adjacent

        x = action[0]
        y = action[1]

        if state.inside(x-1, y) and state.attempts[x-1][y] > 1:
            adjacent = 1
        if state.inside(x+1, y) and state.attempts[x+1][y] > 1:
            adjacent = 1
        if state.inside(x, y-1) and state.attempts[x][y-1] > 1:
            adjacent = 1
        if state.inside(x, y+1) and state.attempts[x][y+1] > 1:
            adjacent = 1
        return adjacent

    def isDiag(self, state, action):
        diag = 0
        if action == None:
            return diag

        x = action[0]
        y = action[1]

        if state.inside(x-1, y-1) and state.attempts[x-1][y-1] > 1:
            diag = 1
        if state.inside(x-1, y+1) and state.attempts[x-1][y+1] > 1:
            diag = 1
        if state.inside(x+1, y-1) and state.attempts[x+1][y-1] > 1:
            diag = 1
        if state.inside(x+1, y+1) and state.attempts[x+1][y+1] > 1:
            diag = 1
        return diag

    def isLine(self, state, action):
            if action == None:
                return 0

            x = action[0]
            y = action[1]

            if state.inside(x-1, y) and state.attempts[x-1][y] > 1:
                if state.inside(x-2, y) and state.attempts[x-2][y] > 1:
                    return 1
            if state.inside(x+1, y) and state.attempts[x+1][y] > 1:
                if state.inside(x+2, y) and state.attempts[x+2][y] > 1:
                    return 1
            if state.inside(x, y-1) and state.attempts[x][y-1] > 1:
                if state.inside(x, y-2) and state.attempts[x][y-2] > 1:
                    return 1
            if state.inside(x, y+1) and state.attempts[x][y+1] > 1:
                if state.inside(x, y+2) and state.attempts[x][y+2] > 1:
                    return 1
            return 0

    def identityFeatureExtractor(self, state, action):
        adjacent_feature = ((action, "adj"), self.isAdjacent(state, action))
        diag_feature = ((action, "diag"), self.isDiag(state, action))
        line_feature = ((action, "line"), self.isLine(state, action))

        return [adjacent_feature, diag_feature, line_feature]

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
        actions = state.getLegalShots()
        if actions == []:
            return None

        if random.random() < self.explorationProb:
            return random.choice(actions)
        else:
            best_actions = []
            best_val = float('-Inf')
            for action in actions:
                val = self.getQ(state, action)
                if val > best_val:
                    best_val = val
                    best_actions = [action]
                if val == best_val:
                    best_actions.append(action)
            return random.choice(best_actions)

            #return max((self.getQ(state, action), action) for action in actions)[1]

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
        Vopt = 0
        if newState != None:
            newStateActions = newState.getLegalShots()
            if newStateActions != []:
                Vopt = max(self.getQ(newState, newAction) for newAction in newStateActions)
        intermediateValue = (eta * (Q - (reward + self.discount * Vopt)))
        for i in range(len(phi)):
            phi[i] = self.copyTuple(phi[i], 1, intermediateValue * phi[i][1])

        for f, v in phi:
            self.weights[f] -= v
        # END_YOUR_CODE

def simulate(rl, numTrials=10, maxIterations=1000, verbose=False, sort=False):
    # Return i in [0, ..., len(probs)-1] with probability probs[i].
    def sample(probs):
        target = random.random()
        accum = 0
        for i, prob in enumerate(probs):
            accum += prob
            if accum >= target: return i
        raise Exception("Invalid probs: %s" % probs)

    totalRewards = []  # The rewards we get on each trial
    lastAverage = 0.0
    mdp = MDP()
    for trial in range(numTrials):
        if trial % 4 == 0:
            mdp = MDP()
        state = mdp.start
        sequence = [state]
        totalDiscount = 1
        totalReward = 0
        total_attempts = 0
        for n in range(maxIterations):
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
            total_attempts += 1
            '''
            if trial % 100 == 0:
                print '------------------'
                state.printAttempts()
                print '\n'
                if n < 30:
                    time.sleep(0.5)
                else:
                    time.sleep(0.1)
            '''
            state = newState
        if verbose:
            lastAverage += total_attempts
            if trial % 100 == 0 and trial != 0:
                print "Last 100 average: %f" % (1.0*lastAverage/100)
                lastAverage = 0
        totalRewards.append(totalReward)
    return totalRewards