# The following code implements A* search to solve the path finding problem in a 10x10 maze.
# However, it has some BUGS leading to infinite loops and nonoptimal solutions! 
''' 
DEBUG the code to make it work with the maze map given in the exercise. 
Hint: You might want to print the current_node and the closed_list (explored set) for each loop 
      to check if the current_node is in the closed_list.
'''


from sqlite3 import Row
import tkinter as tk
from tkinter.tix import COLUMN, ROW

class Node:
    """A node class for A* search"""

    def __init__(self, position,parent=None):
        self.position = position
        self.parent = parent
        self.g = 0 # PATH-COST to the node
        self.h = 0 # heuristic to the goal: straight-line distance hueristic
        self.f = 0 # evaluation function f(n) = g(n) + h(n)

    def __eq__(self, other):
        return self.position == other.position

    #def ChildNode(selt, maze):
        
        #return children
''' DEBUG THE FOLLOWING FUNCTION '''
def astar(maze, start, end):
    """Returns a list of tuples as a solution from "start" to "end" state in "maze" map using A* search.
    See lecture slide for the A* algorithm."""

    # Create start and end node
    start_node = Node(start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(end)  
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []    # frontier queue
    closed_list = []  # explored set
    
    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Check if we found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Expansion: Generate children
        
       # children= current_node.ChildNode(maze)
        # Loop through children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(node_position,parent= current_node)

            # Append
            children.append(new_node)
        for child in children:
            #Tinh gia tri f, g, h cua child node

            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            def Check(list):
                '''
                Dùng để kiểm tra xem child đã có trong list hay chưa. Nếu đã tồn tại, mà child.g nhỏ hơn (đường đi qua child có chi phí thấp hơn), thì replace đường đi cũ bằng đường đi mới (đi qua node child)
                list: open_list hoặc losed_list
                '''
                for index, node in enumerate(list):
                    if node == child and node.g > child.g:
                        list.pop(index)
                        open_list.append(child)
                        return 

            #Kiem tra child node
            if child not in open_list and child not in closed_list:
                open_list.append(child)
            elif child in open_list:
                Check(open_list)
            elif child in closed_list:
                Check(closed_list)
            else:
                continue
def GUI(maze,start,goal,path):
    window= tk.Tk()
    window.title("MAZE")
    window.geometry("700x700")
    titleMain = tk.Label(window,text="Mê Cung",fg="Black",font=("Arial Bold",40))
    titleMain.place(x=200,y=40)
    frame= tk.Frame(window,bd=0.5,relief="solid")
    frame.place(x=100,y=120)
    label = []
    for i in range(0,100):
        x=i//10
        y=i%10
        label.append(tk.Label(frame,bg="White",relief="solid",height=2,width=4,font=("Arial Bold",12)))
        label[i].grid(row=x,column=y)
        if (maze[x][y]==1):
            label[i].config(bg="Black")
    label[start[0]*10+start[1]].config(bg="Green")
    label[goal[0]*10+goal[1]].config(bg="Red")
    
    def NextState():
        global index
        if index < len(path):
            (m,n)=path[index]
            label[m*10+n].config(bg="Yellow")
            index+=1
    buttonNext= tk.Button(window,text="Next",fg="Black",height=1,width=4,font=("Arial Bold",30),command=NextState)
    buttonNext.place(x=200,y=600)
    window.mainloop()


if __name__ == '__main__':

    ''' CHANGE THE BELOW VARIABLE TO REFLECT TO THE MAZE MAP IN THE EXERCISE '''
    maze =     [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 1, 1, 1, 1, 0],  # 1: obstacle position
                [0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
                [0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 0, 0, 0]]

    start = (0, 0)
    goal = (8, 9)

    path = astar(maze, start, goal)
    print(path)  
    index=0
    GUI(maze,start,goal,path)        