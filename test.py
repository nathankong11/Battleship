from game import *

g = Grid(10)
g.reset()
g.randomPlacement()

g.printShips()
g.randomShoot()

g.printAttempts()