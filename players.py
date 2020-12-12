import copy, itertools, pickle, random
import pandas as pd

class PhysicalPlayer():
    def __init__(self, amount, playerNum):
        self.playerNum = playerNum
        print(f"There are {amount} players playing, you are player number {playerNum}")

    def play(self, slots, resources, maxMeeples, topCards, stackHeights, prod, points):
        print(f"\n\nFilled slots: {slots},\n\nresources: {resources},\n\nmaxMeeples: {maxMeeples}\n\ntop cards of stacks: {topCards}\n\ncard stack heights: {stackHeights}\n\nProduction levels: {prod}\n\npoints: {points}")
        res = input(f"Enter your turn, number {self.playerNum}, format: '<name of slot> <amount of meeples>': ")
        return res.split()


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
