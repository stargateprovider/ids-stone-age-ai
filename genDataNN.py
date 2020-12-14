from game import game
from players import *
from random import shuffle
from collections import deque

#r1 = TrainedPlayer(0,"KNN100model")
f=open("maatriks.txt","r")
a=[list(map(int,i.split(" "))) for i in f.readlines()]

AIPlayers=deque()
for i in range(11):
	AIPlayers.append(AIPlayer(0))
while True:
	r1 = AIPlayers.popleft()
	r1.setPlayerNum(0)
	r2 = AIPlayers.popleft()
	r2.setPlayerNum(1)
	r3 = RandomPlayer(2)
	rd=[r1,r2,r3]
	g = game(rd)
	over = False
	while not over:
	    g.make_plays()
	    over = g.resolve_workers()
	võitja=g.points.index(max(g.points))
	if võitja!=2:
		AIPlayers.append(rd[võitja])
		AIPlayers.append(AIPlayer(0,rd[võitja].m))
	else:
		AIPlayers.append(AIPlayer(0))
		AIPlayers.append(AIPlayer(0))
	f=open("maatriksg.txt","w")
	for i in AIPlayers:
		for j in i.m:
			f.write(" ".join(map(str,j))+"\n")
	f.close()
	









	