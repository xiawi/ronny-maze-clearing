from math import floor

class Ronny:
    def __init__(self, rubbishSize=0, rubbishWeight=0):
        self.rubbishSize = rubbishSize
        self.rubbishWeight = rubbishWeight

    def addRubbish(self, rubbishSize, rubbishWeight):
        self.rubbishSize += rubbishSize
        self.rubbishWeight += rubbishWeight

    def dispose(self):
        self.rubbishSize = 0
        self.rubbishWeight = 0

    def hasRubbish(self):
        if self.rubbishSize != 0 or self.rubbishWeight != 0:
            return True
        else:
            return False

class SpecialCell:
    def __init__(self, x, y, rubbishSize, rubbishWeight):
        self.x = x
        self.y = y
        self.rubbishSize = rubbishSize
        self.rubbishWeight = rubbishWeight

class Node:
    def __init__(self, x, y, ronny: Ronny, special_cells: [SpecialCell], goal:SpecialCell = None):
        self.x = x      # Ronny's x position
        self.y = y      # Ronnt's y position
        self.ronny = ronny
        self.special_cells = special_cells
        self.goal = goal

    def totalRubbish(self):
        disposal_rooms = 0
        for cell in self.special_cells:
            if cell.rubbishSize == 0 and cell.rubbishWeight == 0:
                disposal_rooms += 1
        total_rubbish_cells = len(self.special_cells) - disposal_rooms
        return total_rubbish_cells

    def updateGoal(self, goal):
        self.goal = goal

    def state(self):
        total_rubbish_cells = self.totalRubbish()
        return [f"Ronny is at {self.x},{self.y}, carrying {self.ronny.rubbishSize} m3 and {self.ronny.rubbishWeight} kg of rubbish.", \
                      f"Number of Rubbish Cells Remaining: {total_rubbish_cells}"]

    def goalReached(self):
        if self.x == self.goal.x and self.y == self.goal.y:
            if self.goal.rubbishSize != 0 and self.goal.rubbishWeight != 0:
                self.ronny.addRubbish(self.goal.rubbishSize, self.goal.rubbishWeight)
                self.special_cells.remove(self.goal)
                self.goal = None
            else:
                self.ronny.dispose()
                self.goal = None

def selectGoal(node):
    weightage = .5
    h = []  # List of h values
    for cell in node.special_cells: # Heuristic used for goal selection
        dy = abs(node.y - cell.y)
        dx = abs(node.x - cell.x)
        distance = dx + max(0, (dy-dx)/2)   # Distance formula from https://www.redblobgames.com/grids/hexagons/
        totalSize = node.ronny.rubbishSize + cell.rubbishSize
        totalWeight = node.ronny.rubbishWeight + cell.rubbishWeight
        if totalSize > 5 or totalWeight > 40:
            h.append(999999999) # "infinity"
        else:
            h.append(floor(distance + weightage * max((5/(totalSize + .0001)),(40/(totalWeight + .0001)))))

    min_h = h[0]

    for i in range (0,len(h)):
        min_h = min(min_h, h[i])

    node.updateGoal(node.special_cells[h.index(min_h)])
    print()
    print(f"Current Goal: {node.goal.x,node.goal.y}")
    print()

def transitionModel(action):
    if action == "N":
        dx = 0
        dy = -2
    if action == "S":
        dx = 0
        dy = 2
    if action == "NE":
        dx = 1
        dy = -1
    if action == "SE":
        dx = 1
        dy = 1
    if action == "NW":
        dx = -1
        dy = -1
    if action == "SW":
        dx = -1
        dy = 1
    return [dx,dy]

def optimalMove(node, maze_width, maze_height):
    actions = ["N", "S", "NE", "SE", "NW", "SW"]
    h = [] # List of h values
    possibleActions = [] # List of all possible actions
    for action in actions:
        [dx,dy] = transitionModel(action)
        if (node.x + dx < 0) or (node.x + dx > maze_width) or (node.y + dy < 0) or (node.y + dy > maze_height):
            # Checking if actions will lead to Ronny to leave the confines of the maze
            continue
        else:
            # Check if action will put Ronny in our goal cell
            if (node.x + dx == node.goal.x) and (node.y + dy == node.goal.y):
                node.x += dx
                node.y += dy
                node.goalReached()
                return action
            else:
                if ((node.x+dx, node.y+dy) in [(cell.x,cell.y) for cell in node.special_cells]):
                    continue
                else:
                    possibleActions.append(action)
                    hdx = abs(node.x+dx - node.goal.x)
                    hdy = abs(node.y+dy - node.goal.y)
                    distance = hdx + max(0, (hdy-hdx)/2)
                    h.append(distance)
    min_h = h[0]

    for i in range (0,len(h)):
        min_h = min(min_h, h[i])

    optimalAction = possibleActions[h.index(min_h)]
    [dx,dy] = transitionModel(optimalAction)
    node.x += dx
    node.y += dy
    return optimalAction


def gbfs(node, size):
    [maze_width, maze_height] = size
    goal_changes = 0
    step = 0
    listOfActions = []
    print("Step 0:" + str(node.state()))
    while node.ronny.hasRubbish() or node.totalRubbish() != 0:
        step += 1
        if node.goal == None:
            goal_changes += 1
            selectGoal(node)
        listOfActions.append(optimalMove(node, maze_width, maze_height))
        print(f"Step {step}:" + str(node.state()))
    print()
    print(listOfActions)
    print("Total Actions: %d" % len(listOfActions))
    print("Total Goal Changes: %d" % goal_changes)

def main():
    maze_size = [8,11]  # w * h
    maze = Node(0,1,Ronny(),[
        SpecialCell(0,11,1,10), SpecialCell(1,6,3,30), SpecialCell(2,5,1,5),
        SpecialCell(2,11,0,0), SpecialCell(3,2,1,5), SpecialCell(3,8,3,5),
        SpecialCell(4,5,2,10), SpecialCell(4,9,1,20), SpecialCell(5,0,0,0),
        SpecialCell(6,3,2,10), SpecialCell(6,9,2,5), SpecialCell(7,0,1,30),
        SpecialCell(7,6,2,20), SpecialCell(8,3,3,10), SpecialCell(8,11,0,0)
        ])
    gbfs(maze, maze_size)

if __name__ == '__main__':
    main()