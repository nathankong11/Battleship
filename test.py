from game import *

g = Grid()
g.randomPlacement()
g.printShips()
g.printAttempts()


avg_turns = 0
for _ in range(1000):
    num_turns = 0
    while not g.gameOver():
        g.randomShoot()
        num_turns += 1
    avg_turns += num_turns
    g.reset()
    g.randomPlacement()
avg_turns /= 1000
print avg_turns