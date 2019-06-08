from game import *

rl = QLearningAlgorithm(0.5, 0.0)
simulate(rl, 10000, verbose=True)
