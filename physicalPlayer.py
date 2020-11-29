class physicalPlayer():
    def __init__(self, amount, playerNum):
        self.amount = amount
        self.playerNum = playerNum
        print(f"There are {amount} players playing, you are player number {playerNum}")
    def play(self, slots, resources, maxMeeples, topCards, stackHeights):
        print (f"\nFilled slots: {slots},\nresources: {resources},\nmaxMeeples: {maxMeeples}\ntop cards of stacks: {topCards}\ncard stack heights: {stackHeights}")
        res = input("Enter your turn, number {playerNum}, format: '<name of slot> <amount of meeples>': ")
        return res.split()
    