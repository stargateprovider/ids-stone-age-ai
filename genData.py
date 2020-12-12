import itertools, os
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing

from game import game
from players import *

prefix = input("Datasets folder path: ")
if prefix: prefix += "/"

i = 1
filepath = lastfilepath = f"{prefix}dataset{i}.csv"
while os.path.isfile(filepath):
    i += 1
    lastfilepath = filepath
    filepath = filepath[:len(prefix)+7] + str(i) + ".csv"

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

def fitModel(dataset, model):
    df = pd.read_csv(dataset)
    slots = {"food":1,"wood":2,"clay":3,"stone":4,"gold":5,"card1":6,"card2":7,"card3":8,"card4":9,"prod":10,"tent":11}
    df = df.applymap(lambda x: slots[x] if x in slots else x)

    X = df.drop("fitness",axis=1)
    y = df["fitness"]
    encoder = preprocessing.LabelEncoder()
    y_enc = encoder.fit_transform(y)

    return model.fit(X,y_enc)

model_file = "KNN100model"
if os.path.isfile(model_file):
    t1 = TrainedPlayer(0, model_file = model_file)
else:
    print("No model file, creating model...", end="\t")
    model = KNeighborsClassifier(n_neighbors = 100)
    #t1 = TrainedPlayer(0, model = fitModel(lastfilepath, model))
    print("Done!")


for j in range(10000):
    players = [
        SavingPlayer(WeighedRandomPlayer(0)),
        SavingPlayer(WeighedRandomPlayer(1)),
        SavingPlayer(WeighedRandomPlayer(2))
    ]
    g = game(players)
    over = False
    while not over:
        g.make_plays()
        over = g.resolve_workers()
    print (f"Scores: {g.points}", end="\t")
    
    avgpoints = sum(g.points)/3
    fit = [i-avgpoints for i in g.points]
    
    mems = itertools.chain.from_iterable([p.getMem() for p in players])

    for mem in mems:
        playerNums = (mem[-1], (mem[-1]+1)%3, (mem[-1]+2)%3)
        row = {}

        for nr in range(3):
            playerNr = playerNums[nr]

            for slot in mem[0]:
                row[f"{slot}Slot{nr}"] = mem[0][slot][playerNr]
            for resource in mem[1]:
                row[f"{resource}{nr}"] = mem[1][resource][playerNr]
            row[f"maxMeeples{nr}"] = mem[2][playerNr]
            row[f"prod{nr}"] = mem[5][playerNr]
            row[f"points{nr}"] = mem[6][playerNr]

        for i in range(4):
            for resource in range(4):
                row[f"card{i}resource{resource}"] = mem[3][i][resource]
            row[f"height{i}"] = mem[4][i]

        row["moveSlot"] = mem[7]
        row["moveAmount"] = mem[8]
        row["fitness"] = fit[mem[-1]]
        
        res=res.append(row, ignore_index=True)
    
    print(j)
    if j%300==0:
        res.to_csv(filepath, index=False)

res.to_csv(filepath, index=False)
