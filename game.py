import random

class Grid:
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
        self.reset(size)

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

    # Makes an attempt at (x,y) Returns 0 if miss, 1 if hit, size of ship if sunk ship, returns -1 if invalid shot
    def shoot(self, x,y):
        if not self.legalShot(x,y):
            return -1
        if self.shipAt(x,y):
            self.num_hit += 1
            self.attempts[x][y] = 2

            ship = self.ships[x][y]
            self.ship_hits[ship] += 1
            if self.sunkShip(ship):
                self.num_sunk += 1
                return self.ship_size[ship]
            return 1
        else:
            self.num_miss += 1
            self.attempts[x][y] = 1
            return 0

    # randomly shoots on the grid
    def randomShoot(self):
        success = -1
        while success == -1:
            x = random.randint(0, self.width-1)
            y = random.randint(0, self.height-1)
            success = self.shoot(x,y)

    # returns a list of coords of legal shots that can be taken
    def getLegalShots(self):
        coords = []
        for x in self.width:
            for y in self.height:
                if legalShot(x,y):
                    coords.append((x,y))
        return coords

    # returns 1 if game is over
    def gameOver(self):
        for ship in self.sunk_ships:
            if not self.sunk_ships[ship]:
                return 0
        return 1

    # Prints the state of all the ships on the grid
    def printShips(self):
        out = ''
        for x in range(len(self.ships)):
            for y in range(len(self.ships[x])):
                ship = self.ships[x][y]
                out += '' + str(0) if ship == None else str(self.ship_size[ship])
                out += ' '
            out += '\n'
        print out

    # Prints the state of all the attempts on the grid
    def printAttempts(self):
        out = ''
        for x in range(len(self.attempts)):
            for y in range(len(self.attempts[x])):
                out += '' + str(self.attempts[x][y])
                out += ' '
            out += '\n'
        print out

    # Resets the grid to default state
    def reset(self, size):
        self.width = size
        self.height = size
        self.ships = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.attempts = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.num_hit = 0
        self.num_miss = 0
        self.num_sunk = 0
        self.ship_size = {
        'destroyer': 2,
        'submarine': 3,
        'cruiser': 3,
        'battleship': 4,
        'carrier': 5,
        }
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