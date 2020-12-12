from game import game
from players import *

#r1 = TrainedPlayer(0,"KNN100model")
r1 = RandomPlayer(0)
r2 = RandomPlayer(1)
r3 = RandomPlayer(2)
g = game([r1,r2,r3])
over = False
while not over:
    g.make_plays()
    over = g.resolve_workers()
print (f"Scores: {g.points}")