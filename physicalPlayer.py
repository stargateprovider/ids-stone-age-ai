class physicalPlayer():
    def __init__(self, amount, playerNum):
        self.amount = amount
        self.playerNum = playerNum
        print(f"There are {amount} players playing, you are player number {playerNum}")
    def play(self, slots, resources, maxMeeples, topCards, stackHeights, prod, points):
        print (f"\n\nFilled slots: {slots},\n\nresources: {resources},\n\nmaxMeeples: {maxMeeples}\n\ntop cards of stacks: {topCards}\n\ncard stack heights: {stackHeights}\n\nProduction levels: {prod}\n\npoints: {points}")
        res = input(f"Enter your turn, number {self.playerNum}, format: '<name of slot> <amount of meeples>': ")
        return res.split()
    