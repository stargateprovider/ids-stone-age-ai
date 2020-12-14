import copy, itertools, pickle, random


class PhysicalPlayer():
    def __init__(self, amount, playerNum):
        self.playerNum = playerNum
        print(f"There are {amount} players playing, you are player number {playerNum}")

    def play(self, slots, resources, maxMeeples, topCards, stackHeights, prod, points):
        print(f"\n\nFilled slots: {slots},\n\nresources: {resources},\n\nmaxMeeples: {maxMeeples}\n\ntop cards of stacks: {topCards}\n\ncard stack heights: {stackHeights}\n\nProduction levels: {prod}\n\npoints: {points}")
        res = input(f"Enter your turn, number {self.playerNum}, format: '<name of slot> <amount of meeples>': ")
        return res.split()

class AIPlayer():
    maxes = {
            'wood': 7,
            'clay': 7,
            'stone': 7,
            'gold': 7,
            'food': 9999999999999,
            'tent': 2,
            'card1': 1,
            'card2': 1,
            'card3': 1,
            'card4': 1,
            'prod': 1
        }
    v={0: 'wood', 1: 'clay', 2: 'stone', 3: 'gold', 4: 'food', 5: 'tent', 6: 'card1', 7: 'card2', 8: 'card3', 9: 'card4', 10: 'prod'}
       
    def __init__(self,playNum,*n):
        self.playerNum=playNum
        self.m=[]
        if len(n)>0:
            for i in n[0]:
                rida=[]
                for j in i:
                    rida.append(j+random.randint(-2,2))
                self.m.append(rida)
        else:
            for i in range(11):
                rida=[]
                for j in range(25):
                    rida.append(random.randint(-100,100))
                self.m.append(rida)

    def play(self, slots, resources, maxMeeples, topCards, stackHeights, prod, points):
        r=[]
        for i in resources:
            r.append(int(resources[i][self.playerNum]))
        mM=maxMeeples[self.playerNum]-7
        tC=[]
        for i in topCards:
            tC+=i
        p=prod[self.playerNum]
        if points[self.playerNum]==max(points):
            po=1
        else:
            po=-1
        inp=r+tC+[mM,p,po,sum([slots[i][self.playerNum] for i in slots])]
        w=[(j,self.v[i]) for i,j in enumerate(self.korruta(inp))]
        w.sort()
        for i in w:
            if sum(slots[i[1]])<self.maxes[i[1]]:
                if i=="food":
                    return [i[1],mM-sum([slots[j][self.playerNum] for j in slots])]
                elif i=="tent":
                    if mM-sum([slots[j][self.playerNum] for j in slots])>=2:
                        return ["tent",2]
                    else:
                        continue
                else:
                    return [i[1],1]

    def korruta(self,a):
        b=self.m
        o=[]
        for i in b:
            s=0
            for j in range(len(i)):
                s+=a[j]*i[j]
            o.append(s)
        return o
    def setPlayerNum(self,playerNum):
        self.playerNum=playerNum





class RandomPlayer():
    maxes = {
        'wood': 7,
        'clay': 7,
        'stone': 7,
        'gold': 7,
        'food': 9999999999999,
        'tent': 2,
        'card1': 1,
        'card2': 1,
        'card3': 1,
        'card4': 1,
        'prod': 1
    }
    def __init__(self, playerNum):
        self.playerNum = playerNum

    # Random choices
    def play(self, slots, resources, maxMeeples, topCards, stackHeights, prod, points):
        slot = random.choice(list(slots))
        maxAmount = 0
        meeples = self.getFreeMeeples(slots, maxMeeples)

        while not maxAmount:
            slot = random.choice(list(slots))
            maxAmount = min(meeples, self.maxes[slot]-sum(slots[slot]))
        amount = random.randrange(1,maxAmount+1)
        #print(meeples)
        return [slot, amount]

    def getFreeMeeples(self, slots, maxMeeples):
        meeples = maxMeeples[self.playerNum]
        for slot in slots:
            meeples -= slots[slot][self.playerNum]
        return meeples

class WeighedRandomPlayer(RandomPlayer):
    def __init__(self, playerNum):
        super().__init__(playerNum)

    def canBuy(self, card, resources):
        cant = False
        for i in range(4):
            if card[i]>resources[["wood","clay","stone","gold"][i]][self.playerNum]:
                cant = True
        return not cant
    
    # Random choices but making food is twice as likely
    # and cards are bought if and only if the resource requirements are met
    def play(self, slots, resources, maxMeeples, topCards, stackHeights, prod, points):
        for i in range(4):
            if self.canBuy(topCards[i], resources) and sum(slots[f"card{i+1}"])==0:
                #print(f"card{i+1}")
                return [f"card{i+1}", 1]
        
        availableSlots = ["wood","clay","stone","gold","food","food","tent","prod"]
        slot = random.choice(availableSlots)
        maxAmount = 0
        meeples = self.getFreeMeeples(slots, maxMeeples)

        while not maxAmount:
            slot = random.choice(availableSlots)
            maxAmount = min(meeples, self.maxes[slot]-sum(slots[slot]))
        amount = random.randrange(1,maxAmount+1)
        #print(f"{slot} {amount}")
        return [slot, amount]

'''
class TrainedPlayer(RandomPlayer):
    def __init__(self, playerNum, model_file=None, model=None):
        super().__init__(playerNum)
        if model_file:
            self.model = pickle.load(open(model_file,"rb"))
        elif model:
            self.model = model
        else:
            raise ValueError("Either model or model_file parameter is required")

    def play(self, slots, resources, maxMeeples, topCards, stackHeights, prod, points):
        bestMove = []
        bestY = -99999999
        gamestate = {}

        for playNum in range(3):
            nr = (self.playerNum + playNum) % 3
            for slot in slots:
                gamestate[f"{slot}Slot{playNum}"] = [slots[slot][nr]]
            for resource in resources:
                gamestate[resource+str(playNum)] = [resources[resource][nr]]
            gamestate["maxMeeples"+str(playNum)] = [maxMeeples[nr]]
            gamestate["prod"+str(playNum)] = [prod[nr]]
            gamestate["points"+str(playNum)] = [points[nr]]

        for i in range(4):
            for resource in range(4):
                gamestate[f"card{i}resource{resource}"] = [topCards[i][resource]]
            gamestate[f"height{i}"] = [stackHeights[i]]
        
        meeples = self.getFreeMeeples(slots, maxMeeples)
        slots_to_num = {"food":1,"wood":2,"clay":3,"stone":4,"gold":5,"card1":6,"card2":7,"card3":8,"card4":9,"prod":10,"tent":11}

        for slot in slots:
            for i in range(1,min(meeples, self.maxes[slot]-sum(slots[slot]))+1):
                # All possible valid amounts of meeples to put on that field
                gamestate["moveSlot"] = [slots_to_num[slot]]
                gamestate["moveAmount"] = [i]
                fit = self.model.predict(pd.DataFrame(data=gamestate))[0]
                if fit>bestY:
                    bestY = fit
                    bestMove = [slot,i]
        #print(bestMove)
        return bestMove
'''

class SavingPlayer():
    def __init__(self, player):
        self.memory = []
        self.player = player

    def play(self, *args):
        slot, amount = self.player.play(*args)
        self.memory.append(
            tuple(itertools.chain(copy.deepcopy(args), (slot, amount, self.player.playerNum)))
        )
        return [slot, amount]

    def getMem(self):
        return self.memory