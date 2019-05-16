'''
state:

grid of attempted shots
which ships are sunk
number of attempts
'''

game = Grid()

class State:
    def __init__(self, game):
        self.game = game
        self.attempts = game.attempts
        self.sunk_ships = game.sunk_ships
        self.numAttempts = 0

    def generateSuccessor(self, shot):
        newState = State(self, self.game)
        x, y = shot

        newState.game.shoot(x,y)
        newState.attempts = newState.game.attempts
        newState.sunk_ships = newState.game.sunk_ships
        newState.numAttempts = self.numAttempts + 1

        return newState

    def isEnd(self):
        return self.game.gameOver()

    def getLegalActions(self):
        return self.game.getLegalShots()



class Agent:
    getAction(self, gameState):
