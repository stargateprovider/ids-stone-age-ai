from game import game
from players import *
from random import shuffle
from collections import deque

#r1 = TrainedPlayer(0,"KNN100model")
f=open("maatriksf.txt","r")
a=[list(map(int,i.split(" "))) for i in f.readlines()]

AIPlayers=deque()
for i in range(11):
	AIPlayers.append(AIPlayer(0,a[0+11*i:11+11*i]))
n=0
n0=0
N=10**5
for i in range(1):
	r1 = AIPlayers.popleft()
	r1.setPlayerNum(0)
	r2=PhysicalPlayer(1,1)
	r3 = WeighedRandomPlayer(2)
	rd=[r1,r2,r3]
	g = game(rd)
	over = False
	while not over:
	    g.make_plays()
	    over = g.resolve_workers()
	    print()
	AIPlayers.append(r1)
	if g.points[0]==max(g.points):
		n+=1
	if 0>=max(g.points[1:]):
		n0+=1
	print(g.points)
	
	









	