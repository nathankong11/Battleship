from game import *

rl = QLearningAlgorithm(1.0, 0.2)
# We call this here so that the stepSize will be 1
print("beginning simulate")
simulate(rl, 10000, verbose=True)
print("finished simulate")
