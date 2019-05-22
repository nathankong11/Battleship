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

game = Grid()
state = State(game)
new_state = state.generateSuccessor((0,0))