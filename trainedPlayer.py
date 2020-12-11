import pandas as pd
import pickle

class trainedPlayer():
    def __init__(self, playerNum, model_file):
        self.model = pickle.load(open(model_file,"rb"))
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
    def play(self, slots, resources, maxMeeples, topCards, stackHeights, prod, points):
        bestMove = []
        bestY = -99999999
        meeples = maxMeeples[self.playerNum]
        gamestate = {}
        playerNum =  self.playerNum
        for slot in slots:
            for playNum in range(3):
                gamestate[slot+"Slot"+str(playNum)] = [slots[slot][(playerNum+playNum)%3]]
        for resource in resources:
            for playNum in range(3):
                gamestate[resource+str(playNum)] = [resources[resource][(playerNum+playNum)%3]]
        for playNum in range(3):
            gamestate["maxMeeples"+str(playNum)] = [maxMeeples[(playNum+playerNum)%3]]
        for playNum in range(3):
            gamestate["prod"+str(playNum)] = [prod[(playNum+playerNum)%3]]
        for playNum in range(3):
            gamestate["points"+str(playNum)] = [points[(playNum+playerNum)%3]]
        for resource in range(4):
            for i in range(4):
                gamestate["card"+str(i)+"resource"+str(resource)] = [topCards[i][resource]]
        for i in range(4):
            gamestate["height"+str(i)] = [stackHeights[i]]
        
        
        for slot in slots:
            meeples -= slots[slot][self.playerNum]
        for slot in slots:
            for i in range(1,min(meeples, self.maxes[slot]-sum(slots[slot]))+1):
                # All possible valid amounts of meeples to put on that field
                slots_to_num = {"food":1, "wood":2,"clay":3,"stone":4,"gold":5,"card1":6,"card2":7,"card3":8,"card4":9,"prod":10,"tent":11}
                gamestate["moveSlot"] = [slots_to_num[slot]]
                gamestate["moveAmount"] = [i]
                fit = self.model.predict(pd.DataFrame(data=gamestate))[0]
                if fit>bestY:
                    bestY = fit
                    bestMove = [slot,i]
        #print(bestMove)
        return bestMove