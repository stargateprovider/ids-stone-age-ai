import random
import copy

class savingPlayer():
    def __init__(self, amount, playerNum):
        self.amount = amount
        self.playerNum = playerNum
        self.maxes = {'wood': 7,
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
        self.memory = []
    def play(self, slots, resources, maxMeeples, topCards, stackHeights, prod, points):
        slot = random.choice(list(slots))
        maxAmount = 0
        meeples = maxMeeples[self.playerNum]
        for slot in slots:
            meeples -= slots[slot][self.playerNum]
            #print (slots[slot][self.playerNum])
        while not maxAmount:
            slot = random.choice(list(slots))
            maxAmount = min(meeples, self.maxes[slot]-sum(slots[slot]))
        amount = random.randrange(1,maxAmount+1)
        #print(meeples)
        self.memory.append(copy.deepcopy([slots,resources,maxMeeples,topCards,stackHeights, prod, points,slot,amount,self.playerNum]))
        return [slot, amount]
    def getMem(self):
        return self.memory