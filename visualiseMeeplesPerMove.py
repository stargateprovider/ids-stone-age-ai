from game import game
from players import *
from random import shuffle
from collections import deque
import matplotlib.pyplot as plt

f=open("maatriksf.txt","r")
a=[list(map(int,i.split(" "))) for i in f.readlines()]

AIPlayers=[]
for i in range(11):
        AIPlayers.append(AIPlayer(0,a[0+11*i:11+11*i]))

moves = {'wood': [0],
    'clay': [0],
    'stone': [0],
    'gold': [0],
    'food': [0],
    'tent': [0],
    'card1': [0],
    'card2': [0],
    'card3': [0],
    'card4': [0],
    'prod': [0]
 }
moveamounts = [0]


n=0
n0=0
N=10**5
for i in range(1000):
        r1 = AIPlayers[0]
        r1.setPlayerNum(0)
        r2 = AIPlayers[1]
        r2.setPlayerNum(1)
        r3 = AIPlayers[2]
        r3.setPlayerNum(2)
        rd=[r1,r2,r3]
        g = game(rd)
        over = False
        counter = 0
        while not over:
            g.make_plays()
            if len(moves["wood"])<=counter:
                for slot in moves:
                    moves[slot].append(0)
                moveamounts.append(0)
            moveamounts[counter]+=1
            for slot in g.slots:
                moves[slot][counter]+=sum(g.slots[slot])
            counter+=1
            over = g.resolve_workers()
            print()
        AIPlayers.append(r1)
        if g.points[0]==max(g.points):
                n+=1
        if 0>=max(g.points[1:]):
                n0+=1
        print(g.points)

for slot in moves:
    for i in range(len(moves[slot])):
        moves[slot][i]/=(moveamounts[i]*3)
cumsum = [0]*len(moves["wood"])
lastcumsum = [0]*len(moves["wood"])
slotsrev = {'wood': 'Wood',
    'clay': "Clay",
    'stone': "Stone",
    'gold': "Gold",
    'food': "Food",
    'tent': "Tent",
    'card4': "Cards",
    'prod': "Prod"
}
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
for slot in moves:
    cumsum = [cumsum[i]+moves[slot][i] for i in range(len(moves["wood"]))]
    if slot not in ["card1","card2","card3"]:
        ax.plot(cumsum)
        ax.fill_between(range(len(cumsum)),cumsum,lastcumsum, label=slotsrev[slot])
        lastcumsum = cumsum.copy()
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1], loc="upper right")
ax.set_xlabel("Move nr")
ax.set_ylabel("# of meeples")
plt.show()


