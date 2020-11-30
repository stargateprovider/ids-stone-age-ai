# ids-stone-age-ai
## Instructions for playing the game:
* create desired amount of random/physical player object in main.py
* run main.py

## Simplified game rules and terminology:
* In the beginning each player has 5 workers and there are 4 stacks of 4 cards on the game board.
* Each round of the game consists of 2 phases: placing workers and resolving actions.
* In the first phase each player can place their workers on any of the 11 fields on the game board. Each player can place any amount of his workers on one field at once (as long as the field capacity is not exceeded), then the next player gets to place their workers, when all players have placed workers, they start placing new once starting from the first player again and so on until all players have run out of workers. The fields are as follows:  
  * Agricultural field (max capacity: 1) - when a player places a worker here, their agricultural level increases by 1
  * Tent field (max capacity: 2) - when a player places two workers here, they receive a new worker (nothing happens when 1 worker is placed there)
  * Four card fields (max capacity: 1 each) - players can buy the cards for resources written on the cards to earn points, each resource has a set number of points they give. If a player places a worker here but doesn’t have enough resources at the end of the resolution phase then nothing happens
  * Food field (max capacity: unbounded) - players can roll a die for each worker they place here and receive food equal to the sum of the rolled dice divided by 2, rounded down
  * Resource fields (max capacity: 7 each) - players can roll a die for each worker they place here and receive the corresponding resource equal to the sum of the dice divided by the value of the resource, rounded down
* The second phase is the action resolving phase, in that phase all the workers receive their products and go home, one player at a time. At the end of this phase each player has to feed each of their workers 1 food minus their agricultural level. If they don’t have enough food they don’t give any of it away and they lose 10 points.
* The game ends when one of the card stacks is depleted at the end of a second phase and the player with the highest points wins.

Game terminology:  
*Fields* - fields on the game board on which players place workers aka meeples  
*Resources* - items that workers can get from certain fields and with which players can buy cards that give points. Unlike the original game the total number resources is only bounded by the size of your RAM  
*Values of resources* - wood is worth 3, clay 4, stone 5 and gold 6 units. This is the amount of points you gain for buying a building using that resource, you don’t get any points if you have the raw resource at the end of the game  
*Cards* aka *buildings* - on the gameboard there are 4 stacks of cards of which players can only see the top ones. They can buy those cards for resources to earn points. The game ends when one of these stacks is emptied  
*Production level* aka *agricultural level* - for each production level the player has to feed one less worker without losing points  
