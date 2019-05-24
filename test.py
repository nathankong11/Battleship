from game import *

g = State(5)
g.randomPlacement()
g.printShips()
g.printAttempts()


avg_turns = 0
for _ in range(1000):
    num_turns = 0
    while not g.isEnd():
        g.printAttempts()
        print '\n'
        g.randomShoot()
        num_turns += 1
    print 'end'
    avg_turns += num_turns
    g.reset()
    g.randomPlacement()
avg_turns /= 1000
print avg_turns