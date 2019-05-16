from game import *

g = Grid()
g.randomPlacement()
g.printShips()

g.printAttempts()

num_turns = 0
while not g.gameOver():
    g.randomShoot()
    num_turns += 1
print num_turns