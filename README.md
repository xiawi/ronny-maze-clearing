# Ronny's Maze Problem
#### By  _**Yap Wei Xiang, Lee Boon Hoe and Asilbek Abdullaev**_
#### A program that utilises greedy best first search to select goals for Ronny's Maze Problem
----
## Final Path
![path](https://github.com/xiawi/ronny-maze-clearing/assets/122159364/1879f554-f23f-44eb-bb1a-92f6e3aa4e33)
## Usage
### Using the Floor Function
The `floor` function is a part of the `math` library and is used to round down a given floating-point number to the nearest integer. This function is helpful when you need to ensure that a number is always rounded down, regardless of its decimal part.

In our program, the function is used in our **goal selection heuristic**.

	def  selectGoal(node):
	weightage  =  .5
	h  = [] # List of h values
	for  cell  in  node.special_cells: # Heuristic used for goal selection
	dy  =  abs(node.y -  cell.y)
	dx  =  abs(node.x -  cell.x)
	distance  =  dx  +  max(0, (dy-dx)/2) # Distance formula from https://www.redblobgames.com/grids/hexagons/
	totalSize  =  node.ronny.rubbishSize +  cell.rubbishSize
	totalWeight  =  node.ronny.rubbishWeight +  cell.rubbishWeight
	if  totalSize  >  5  or  totalWeight  >  40:
	h.append(999999999) # "infinity"
	else:
	h.append(floor(distance  +  weightage  *  max((5/(totalSize  +  .0001)),(40/(totalWeight  +  .0001)))))
	min_h  =  h[0] 

	for  i  in  range (0,len(h)):

	min_h  =  min(min_h, h[i])

	node.updateGoal(node.special_cells[h.index(min_h)])

	print()
	print(f"Current Goal: {node.goal.x,node.goal.y}")
	print()
We use the `floor` function here to round down numbers to simplify the outputs of our heuristics. 

## Description
In our algorithm, Ronny essentially selects the best goal possible before moving. He does this using a heuristic function that takes into account how far a potential goal is from him, as well as how much it fills his bin. In the program, he calculates all the heuristics for all the goals and puts them into a list. He then compares each heuristic, selecting the goal associated with the lowest one to be his *goal*.

To traverse the maze, Ronny does not expand towards every direction, he simply looks at each neighbouring node and asks himself if it would bring him closer to his goal. We do this by using a distance function. Ronny will always move towards the cell which will bring him the closest to his current *goal*. If there are other rubbish cells in the way of his next goal, he simply ignores them.

The output on the console will show Ronny's `state`, which tells us:
1. where Ronny is,
2. how much rubbish Ronny is holding, and
3. The rubbish cells remaining.

and finally, it shows us the full path taken by Ronny to remove all the rubbish in the maze, as well as the total actions taken, and the number of goal changes Ronny took.

## Instructions
### Initialising the Maze
Simplify change the values below to specify the size of the new maze.

	maze_size  = [8,11] # w * h

Also, initialise the `Node` object with values that you wish to initialise it with, including starting position, as well as the list of special cells.

	maze  =  Node(0,1,Ronny(),[
	SpecialCell(0,11,1,10), SpecialCell(1,6,3,30), SpecialCell(2,5,1,5),
	SpecialCell(2,11,0,0), SpecialCell(3,2,1,5), SpecialCell(3,8,3,5),
	SpecialCell(4,5,2,10), SpecialCell(4,9,1,20), SpecialCell(5,0,0,0),
	SpecialCell(6,3,2,10), SpecialCell(6,9,2,5), SpecialCell(7,0,1,30),
	SpecialCell(7,6,2,20), SpecialCell(8,3,3,10), SpecialCell(8,11,0,0)
	])
Simply run the program after initialisation.

If you wish to change Ronny's capacity values, i.e. how much rubbish he can carry at a time, you can change them in the `selectGoal` function, under the heuristic calculation.

		def selectGoal(node):
		...
	            h.append(floor(distance + weightage * max((5/(totalSize + .0001)),(40/(totalWeight + .0001)))))
Here, you can change `5` and `40` to change his capacity values.

Additionally, the user can tweak the `weightage` value to see if there are any better values for their implementation.

	def selectGoal(node):
    weightage = .5


