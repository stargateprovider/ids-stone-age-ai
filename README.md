# ids-stone-age-ai

## Datasets
* Can be created using genData.py
* Dataset 1 is obtained with 3 RandomPlayers
* Datasets 2-3 are obtained with 1 TrainedPlayer and 2 RandomPlayers
* Dataset 4 is obtained with 3 WeighedRandomPlayers

## The matrixes
* Can be generated using genDataNN.py
* The final data we generated was from playing the game with a AIPlayer, which uses a neural network approach.
* maatriksf.txt ended up being our best matrix to use for a player
* DatasetNN1.csv and datasetNN11.csv are examples from when we flattened the matrix file to columns and added the corresponding game points as another column

## Instructions for playing the game:
* create desired amount of computer/physical player objects in main.py
* run main.py

## Simplified game rules:
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

## Compiling
* The necessary game files can be easily compiled using compile.py
* This gives slightly better performance

## All .py files explained
* game.py - the class for running the game
* genDataNN.py - teaches neural networks (output goes to maatriksg.txt)
* genData.py - generates dataset by letting given type of players play thourgh the game many times and saves the results into dataset[x].csv
* getAIwinrate.py - tests neural networks in maatriksf.txt for how many games they win agains random players
* main.py - let's you play through the game once, you can set the players in the beginning of the code
* players.py - classes for different players
* plotFromFile.py - generates plot for visualiseNeuralLearning.py using the temporary dump files that visualiseNeuralLearning.py creates while running
* visualiseMeeplesPerMove.py - generates graph for which fields neural networks in maatriksf.txt place their meeples on on which turns 
* visualiseNeuralLearning.py - generates graph of model families that are made during training the neural networks