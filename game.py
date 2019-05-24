import random
from copy import *

class State:
    """
    A 2-dimensional array. Data is accessed
    via grid[x][y] where (x,y) are positions with x horizontal,
    y vertical and the origin (0,0) in the top left corner.

    ships(x,y):
    None: empty
    destroyer: (2 hole ship)
    submarine: (3 hole ship)
    cruiser: (3 hole ship)
    battleship: (4 hole ship)
    carrier: (5 hole ship)

    attempts(x,y):
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
        # if ship at location
        if self.shipAt(x,y):
            self.num_hit += 1
            self.attempts[x][y] = 2
            ship = self.ships[x][y]
            self.ship_hits[ship] += 1
            # if sunk ship
            if self.sunkShip(ship):
                self.num_sunk += 1
                return self.ship_size[ship]
            return 1
        # if ship not at location
        else:
            self.num_miss += 1
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
    def __init__(self):
        self.start = self.startState()
    # Return the start state.
    def startState(self):
        state = State(5)
        state.randomPlacement()
        print("_____")
        state.printShips()
        print("_____")
        return state

    # Return set of actions possible from |state|.
    def getLegalActions(self, state):
        actions = state.getLegalShots()
        return actions if actions != None else None

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
            return 100
        if state.shipAt(action[0],action[1]):
            return 2
        return -1

    # Return a list of (new_state, prob, reward) tuples corresponding to edges
    # coming out of |state|.
    # Mapping to notation from class:
    #   state = s, action = a, new_state = s', prob = T(s, a, s'), reward = Reward(s, a, s')
    # If IsEnd(state), return the empty list.
    def succAndProbReward(self, state, action):
        new_state = self.generateSuccessor(state, action)
        if new_state == None:
            return []
        return [(new_state, 1.0, self.getReward(state, action, new_state))]

    def discount(self):
        return 0.9

    # Compute set of states reachable from startState.  Helper function for
    # MDPAlgorithms to know which states to compute values and policies for.
    # This function sets |self.states| to be the set of all states.
    def computeStates(self):
        self.states = set()
        queue = []
        self.states.add(self.start)
        queue.append(self.start)
        while len(queue) > 0:
            print len(self.states)
            state = queue.pop()
            for action in self.getLegalActions(state):
                for newState, prob, reward in self.succAndProbReward(state, action):
                    if newState not in self.states:
                        self.states.add(newState)
                        queue.append(newState)
            '''
                new_state = self.generateSuccessor(state, action)
                if new_state == None:
                    continue
                #new_state.printAttempts()
                #print new_state.num_attempts
                #print '__________'
                if new_state not in self.states:
                    self.states.add(new_state)
                    queue.append(new_state)
            '''