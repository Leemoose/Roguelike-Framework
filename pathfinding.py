import objects as O
import heapq

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position
    
    def __lt__(self, other):
        return self.f < other.f

    def __str__(self):
        return str(self.position)


def astar(maze, start, goal, monster_map, player, monster_blocks = False, player_blocks = False):
    return astar_multi_goal(maze, start, [goal], monster_map, player, monster_blocks, player_blocks)

def astar_multi_goal(maze, start, goals, monster_map, player, monster_blocks = False, player_blocks = False):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""
    # reverse is a flag that determines if we're moving towards end or away from it

    # Create start and end node
    end_node = Node(None, start) # a little counter-intuitive, but we want to end the search backwards.
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = set()

    # Add the start node
    for position in goals:
        node = Node(None, position)
        node.g = node.h = node.f = 0
        heapq.heappush(open_list, node)

    # Loop until you find the end
    while len(open_list) > 0:
        # Get the current node
        current_node = heapq.heappop(open_list)
        closed_list.add(current_node.position)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path # Return reversed path
        
        current_position = current_node.position
        
        # Make sure walkable terrain
        if not maze[current_position[0]][current_position[1]].passable:
            continue
        if monster_blocks == True and (not monster_map.get_passable(current_position[0],current_position[1])): # and not start == (node_position[0],node_position[1])):
            continue
        if player_blocks == True and (player.x == current_position[0] and player.y == current_position[1]):
            continue

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list - by invariants, we can skip
            if child.position in closed_list:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2) ** 0.5
            child.f = child.g + child.h

            heapq.heappush(open_list, child)

    return []


def main():
    maze= []
    for x in range(10):
        temp = []
        for y in range(10):
            if x == 4 and y == 4:
                temp.append(O.Tile(x, y, 1, False))
            else:
                temp.append(O.Tile(x, y, 1, True))

        maze.append(temp)

    for n in maze:
        line = ""
        for m in n:
            line += str(m)
        print(line)

    start = (0,0)
    end = (7, 6)

    path = astar(maze, start, end)
    print(path)

if __name__=="__main__":
    main()