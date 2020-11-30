from game import game
from physicalPlayer import physicalPlayer
from randomPlayer import randomPlayer
from savingPlayer import savingPlayer
import pandas as pd

gTemp = game([])

cols1 = [i+"Slot" for i in gTemp.slots]
cols1 += [i for i in gTemp.resources]
cols1 += ["maxMeeples"]
cols1 += ["prod"]
cols1 += ["points"]
cols = [cols1[i//3]+str(i%3) for i in range(len(cols1)*3)]
cols += ["card"+str(i//4)+"resource"+str(i%4) for i in range(16)]
cols += ["height"+str(i) for i in range(4)]
cols += ["moveSlot"]
cols += ["moveAmount"]
cols += ["fitness"]

print(len(cols))
res = pd.DataFrame(data={i:[] for i in cols})

dic = {}
for col in cols:
    if col=="moveSlot":
        dic[col] = "string"
    elif col=="fitness":
        dic [col] = "float"
    else:
        dic[col] = "int32"

res = res.astype(dic)

#if col=="moveAmount" else (col: 'float' if col=="fitness" else col:'int32')

for j in range(10000):
    r1 = savingPlayer(3,0)
    r2 = savingPlayer(3,1)
    r3 = savingPlayer(3,2)
    g = game([r1,r2,r3])
    over = False
    while not over:
        g.make_plays()
        over = g.resolve_workers()
    print (f"Scores: {g.points}")
    
    avgpoints = sum(g.points)/3
    fit = [i-avgpoints for i in g.points]
    
    mems = r1.getMem()
    mems += r2.getMem()
    mems += r3.getMem()
    for mem in mems:
        row = {}
        for slot in mem[0]:
            for playerNum in range(3):
                row[slot+"Slot"+str(playerNum)] = mem[0][slot][[mem[-1],(mem[-1]+1)%3,(mem[-1]+2)%3][playerNum]]
        for resource in mem[1]:
            for playerNum in range(3):
                row[resource+str(playerNum)] = mem[1][resource][[mem[-1],(mem[-1]+1)%3,(mem[-1]+2)%3][playerNum]]
        for playerNum in range(3):
            row["maxMeeples"+str(playerNum)] = mem[2][[mem[-1],(mem[-1]+1)%3,(mem[-1]+2)%3][playerNum]]
        for playerNum in range(3):
            row["prod"+str(playerNum)] = mem[5][[mem[-1],(mem[-1]+1)%3,(mem[-1]+2)%3][playerNum]]
        for playerNum in range(3):
            row["points"+str(playerNum)] = mem[6][[mem[-1],(mem[-1]+1)%3,(mem[-1]+2)%3][playerNum]]
        for resource in range(4):
            for i in range(4):
                row["card"+str(i)+"resource"+str(resource)] = mem[3][i][resource]
        for i in range(4):
            row["height"+str(i)] = mem[4][i]
        row["moveSlot"] = mem[7]
        row["moveAmount"] = mem[8]
        row["fitness"] = fit[mem[-1]]
        
        res=res.append(row, ignore_index=True)
    
    print (j)
    if j%300==0:
        res.to_csv("dataset.csv", index=False)

res.to_csv('dataset.csv', index=False)
        
                