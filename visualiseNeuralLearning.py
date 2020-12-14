from game import game
from players import *
from random import shuffle
from collections import deque
import matplotlib.pyplot as plt
import pickle

#r1 = TrainedPlayer(0,"KNN100model")
f=open("maatriks.txt","r")
a=[list(map(int,i.split(" "))) for i in f.readlines()]

names = [i for i in open("lemmad2013.txt","r")]
random.shuffle(names)
namecur = 0

generations = {}
familyTree = []
births = {}
#births["random"] = 0
#generations["random"] = []

AIPlayers=deque()
for i in range(11):
	AIPlayers.append([AIPlayer(0),names[namecur]])
	births[names[namecur]] = 0
	generations[names[namecur]]= []
	namecur+=1
for k in range(1000000):
	rnam = [1,1]
	[r1,rnam[0]] = AIPlayers.popleft()
	r1.setPlayerNum(0)
	[r2,rnam[1]] = AIPlayers.popleft()
	r2.setPlayerNum(1)
	r3 = RandomPlayer(2)
	rd=[r1,r2,r3]
	g = game(rd)
	over = False
	while not over:
	    g.make_plays()
	    over = g.resolve_workers()
	võitja=g.points.index(max(g.points))
	
	for i in [0,1]:
		if rnam[i] not in generations:
			generations[rnam[i]] = []
			if rnam[i] not in births:
				print("Something is wrong, call tech support")
		generations[rnam[i]].append(g.points[i])
#	generations["random"].append(g.points[2])
	
	if võitja!=2:
		vnam = rnam[g.points.index(max(g.points))]
		AIPlayers.append([rd[võitja], vnam])
		ctr = 2
		while vnam+" "+str(ctr) in familyTree:
			ctr+=1
		
		AIPlayers.append([AIPlayer(0,rd[võitja].m), vnam+" "+str(ctr)])
		familyTree.append(vnam+" "+str(ctr))
		births[vnam+" "+str(ctr)] = births[vnam]+len(generations[vnam])
	else:
		AIPlayers.append([AIPlayer(0),names[namecur]])
		births[names[namecur]] = births[rnam[0]]+len(generations[rnam[0]])
		namecur+=1
		AIPlayers.append([AIPlayer(0),names[namecur]])
		births[names[namecur]] = births[rnam[0]]+len(generations[rnam[0]])
		namecur+=1
	f=open("maatriksg.txt","w")
	for [p,_] in AIPlayers:
		for j in p.m:
			f.write(" ".join(map(str,j))+"\n")
	f.close()
	if k%200==0:
		print(k)
		pickle.dump(generations,open("generationsSave","wb"))
		pickle.dump(births,open("birthsSave","wb"))
	
for nam in generations:
	b = births[nam]
	l = generations[nam]
	if len(l)>10:
		plt.plot(range(b,b+len(l)),generations[nam],label=nam.split()[0]+" taseme "+str(len(nam.split())-1)+" järglane, vanus: "+str(len(l)))
plt.legend()
plt.show()








	