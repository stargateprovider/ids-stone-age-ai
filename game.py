import random
class game():
    def __init__(self, players):
        self.players = [p for p in players]
        self.num = len(self.players)
        self.slots = {'wood': [0]*self.num,
                        'clay': [0]*self.num,
                        'stone': [0]*self.num,
                        'gold': [0]*self.num,
                        'food': [0]*self.num,
                        'tent': [0]*self.num,
                        'card1': [0]*self.num,
                        'card2': [0]*self.num,
                        'card3': [0]*self.num,
                        'card4': [0]*self.num,
                        'prod': [0]*self.num
                     }
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
        self.resources = {'wood': [0]*self.num,
                        'clay': [0]*self.num,
                        'stone': [0]*self.num,
                        'gold': [0]*self.num,
                        'food': [0]*self.num
                     }
        self.cards = [[2,1,0,0],
                        [2,0,1,0],
                        [1,2,0,0],
                        [2,0,0,1],
                        [1,0,2,0],
                        [0,2,1,0],
                        [0,2,0,1],
                        [0,1,2,0],
                        [0,0,2,1],
                        [1,1,1,0],
                        [1,1,1,0],
                        [1,1,0,1],
                        [1,1,0,1],
                        [1,0,1,1],
                        [1,0,1,1],
                      #  [0,1,1,1],
                        [0,1,1,1]
                     ]
        self.prodlvl = [0]*self.num
        self.points = [0]*self.num
        random.shuffle(self.cards)
        self.stacks = [self.cards[:len(self.cards)//4],
                        self.cards[len(self.cards)//4:2*len(self.cards)//4],
                        self.cards[2*len(self.cards)//4:3*len(self.cards)//4],
                        self.cards[3*len(self.cards)//4:]]
        self.meeples = [5]*self.num
        self.maxMeeples = [5]*self.num
        self.starting = 0
        
    def make_plays(self):
        turn = self.starting
        while sum(self.meeples):
            while not self.meeples[turn]:
                turn = (turn+1)%self.num
            [slot, amount] = self.players[turn].play(self.slots, self.resources, self.maxMeeples, [self.stacks[i][0] for i in range(4)], [len(self.stacks[i]) for i in range(4)], self.prodlvl, self.points)
            amount = int(amount)
            if not slot in self.slots or amount > self.meeples[turn] or amount+sum(self.slots[slot]) > self.maxes[slot]:
                print (f"Invalid play! turn: {turn}, slot: {slot}, amount: {amount}")
                continue
            else:
                self.meeples[turn] -= amount
                self.slots[slot][turn] += amount
                turn = (turn+1)%self.num
                
    def resolve_workers(self):
        over = False
        turn = self.starting
        while sum(self.maxMeeples)-sum(self.meeples):
            if self.slots['tent'][turn] == 2:
                self.maxMeeples[turn]+=1
            if self.slots['food'][turn]:
                self.resources['food'][turn]+=sum([random.randrange(1,7) for i in range(self.slots['food'][turn])])//2
            if self.slots['wood'][turn]:
                self.resources['wood'][turn]+=sum([random.randrange(1,7) for i in range(self.slots['wood'][turn])])//3
            if self.slots['clay'][turn]:
                self.resources['clay'][turn]+=sum([random.randrange(1,7) for i in range(self.slots['clay'][turn])])//4
            if self.slots['stone'][turn]:
                self.resources['stone'][turn]+=sum([random.randrange(1,7) for i in range(self.slots['stone'][turn])])//5
            if self.slots['gold'][turn]:
                self.resources['gold'][turn]+=sum([random.randrange(1,7) for i in range(self.slots['gold'][turn])])//6

            for nr in range(4):
                if not self.slots[f'card{nr+1}'][turn]:
                    continue

                notEnough = False
                price = 0
                for i in range(4):
                    price += self.stacks[nr][0][i]*(i+3)
                    if self.stacks[nr][0][i] > self.resources[['wood','clay','stone','gold'][i]][turn]:
                        notEnough = True
                if not notEnough:
                    for i in range(4):
                        self.resources[['wood','clay','stone','gold'][i]][turn] -= self.stacks[nr][0][i]
                    self.stacks[nr].pop(0)
                    self.points[turn] += price

            if self.slots['prod'][turn]:
                self.prodlvl[turn]+=1     
                               
            for slot in self.slots:
                self.slots[slot][turn] = 0
            self.meeples[turn] = self.maxMeeples[turn]
            if min([len(self.stacks[i]) for i in range(4)]) == 0:
                over = True
                
            if self.resources['food'][turn]+self.prodlvl[turn] < self.meeples[turn]:
                self.points[turn] -= 10
            else:
                self.resources['food'][turn] -= (self.meeples[turn]-self.prodlvl[turn])
            turn = (turn+1)%self.num
            
        self.starting = (self.starting+1)%self.num
        return over