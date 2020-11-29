from game import game
from physicalPlayer import physicalPlayer
from randomPlayer import randomPlayer

r1 = randomPlayer(3,0)
r2 = randomPlayer(3,1)
r3 = randomPlayer(3,2)
g = game([r1,r2,r3])
over = False
while not over:
    g.make_plays()
    over = g.resolve_workers()
print (f"Scores: {g.points}")