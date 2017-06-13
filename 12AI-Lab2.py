import random
from copy import deepcopy

class Controller:
    def __init__(self, n):
        self.n = n
        self.size = n*(n+1)/2
        self.instance = Problem(n)
        #self.currentState = self.createM()

    def getMatrix(self):
        return self.instance.getMatrix()

    def printMatrix(self):
        for i in range(0, int(self.instance.getSize()/self.instance.getN())):
            for j in range(0, self.n):
                print(self.instance.getMatrix()[i][j], end=' ')
            print('\n', end='')

    def DFS(self):
        toVisit=[self.instance.getInitialState()]
        visited=[]
        i = 0
        found = False
        solutions = []
        print(self.instance.column)
        while(len(toVisit) != 0):
            node=toVisit.pop(0)
            x = node.getCost()
            if x >= self.instance.maxCost:
                solutions.append(node)
            else:
                visited.append(node)
                aux=self.instance.expand(node)
                #aux = self.instance.expand(node)
                children=[]
                for x in aux:
                    if x not in visited:
                        children.append(x)
                toVisit=children+toVisit

        print("To Visit: ", end='')
        for x in solutions:
            print(x.road, ' ', x.getCost())

    def GBFS(self):
        toVisit=[self.instance.getInitialState()]
        visited=[]
        solutions = []
        found = False
        while(len(toVisit)!=0) and found == False:
            node=toVisit.pop(0)
            if node.getCost() >= self.instance.maxCost-19:
                solutions.append(node)
                found = True
            else:
                visited.append(node)
                aux=self.instance.expand(node)
                children=[]
                for x in aux:
                    if x not in visited:
                        children.append(x)
                children.sort(key= lambda x: x.getCost(),reverse=True)
                toVisit=children+toVisit
        for x in solutions:
            print(x.road, ' ', x.getCost())


#Controller(9)

class State:
    def __init__(self, x, y, w):
        self.x = x
        self.y = y
        self.road = []
        self.road.append((x, y)) #drum care il face ce noduri trece
        self.cost = w

    def getPosition(self):
        return self.x, self.y

    def setPosition(self,x, y):
        self.x = x
        self.y = y

    def getRoad(self):
        return self.road

    def getCost(self):
        return self.cost
    
    def newStep(self,x, y, w):
        self.road.append((x, y))
        self.cost += w
        self.x = x
        self.y = y
    
    def visited(self, x, y):
        return (x, y) in self.road


class Problem:
    def __init__(self, n):
        self.n = n
        self.size = n*(n+1)/2
        self.matrix = []
        self.matrix = self.readMatrix()
        self.column = len(self.matrix[0])
        self.rows = len(self.matrix)
        self.initialState = State(0, int(len(self.matrix[0])/2), self.matrix[0][int(len(self.matrix[0])/2)])
        self.finalState = 1
        self.maxCost = 79
    
    def getInitialState(self):
        return self.initialState

    def createM(self, n):
        list = [i for i in range(1, self.n)]
        matrix = [['x' for x in range(self.n)] for y in range(int(self.size/self.n))]
        k = 0
        for i in range(0, int(self.size/self.n)):
            k = 0
            for j in range(0, i+1):
                if k != 0 :
                    matrix[i][int(self.n/2)-k] = random.choice(list)
                    matrix[i][int(self.n/2)+k] = random.choice(list)
                else:
                    matrix[i][int(self.n/2)] = random.choice(list)
                k += 1
        for i in range(0, int(self.size/self.n)):
            for j in range(0, self.n):
                print(matrix[i][j], end=' ')
            print('\n', end='')
        return matrix    

    def getMatrix(self):
        return self.matrix

    def getSize(self):
        return self.size
    
    def getN(self):
        return self.n

    def readMatrix(self):
        f=open("matrix.txt","r")
        matrix = []
        for line in f:
            members=line.split(' ')
            row=[]
            for cell in members:
                print(cell)
                if cell != 'x' and cell != 'x\n':
                    row.append(int(cell))
                else:
                    row.append('x')
            print(row)
            matrix.append(row)
        return matrix

    def heuristic(self, state1, state2):
        if state1.getCost() > state2.getCost():
            return state1
        return state2
    def expand(self, state):
        possibleStates = []
        down = deepcopy(state)
        right = deepcopy(state)
        left = deepcopy(state)

        x, y = state.getPosition()
        print(self.column, ' Columsn and Rows ', self.rows)
        if y + 1 < self.column:
            if self.matrix[x][y+1] != 'x' and not state.visited(x, y+1):
                #right.setPosition(x, y+1)
                right.newStep(x, y+1, self.matrix[x][y+1])
                possibleStates.append(right)
        if y - 1 >= 0:
            if self.matrix[x][y-1] != 'x' and not state.visited(x, y-1):
                #left.setPosition(x, y-1)
                left.newStep(x, y-1, self.matrix[x][y-1])
                possibleStates.append(left)
        if x + 1 < self.rows:
            if self.matrix[x+1][y] != 'x' and not state.visited(x+1, y):
                #down.setPosition(x+1, y)
                down.newStep(x+1, y, self.matrix[x+1][y])
                possibleStates.append(down)
        return possibleStates

    def expandGreedy(self, state):
        possibleStates = []
        down = deepcopy(state)
        right = deepcopy(state)
        left = deepcopy(state)

        x, y = state.getPosition()

        if y + 1 < self.column:
            if self.matrix[x][y+1] != 'x' and not state.visited(x, y+1):
                right.setPosition(x, y+1)
                right.newStep(x, y+1, self.matrix[x][y+1])
                #possibleStates.append(right)
        if y - 1 != 0:
            if self.matrix[x][y-1] != 'x' and not state.visited(x, y-1):
                left.setPosition(x, y-1)
                left.newStep(x, y-1, self.matrix[x][y-1])
                #possibleStates.append(left)
        if x + 1 < self.column:
            if self.matrix[x+1][y] != 'x' and not state.visited(x+1, y):
                down.setPosition(x+1, y)
                down.newStep(x+1, y, self.matrix[x+1][y])
                #possibleStates.append(down)
        if down.getCost() == max(right.getCost(), down.getCost(), left.getCost()):
            if down.getCost() != right.getCost() and down.getCost() != left.getCost():
                possibleStates.append(down)
                return possibleStates
            else:
                if down.getCost() == right.getCost():
                    possibleStates.append(down)
                    possibleStates.append(right)
                if down.getCost() == left.getCost():
                    possibleStates.append(down)
                    possibleStates.append(left)
                return possibleStates
        if right.getCost() == max(right.getCost(), down.getCost(), left.getCost()):
            if down.getCost() != right.getCost() and right.getCost() != left.getCost():
                possibleStates.append(right)
                return possibleStates
            else:
                if down.getCost() == right.getCost():
                    possibleStates.append(down)
                    possibleStates.append(right)
                if right.getCost() == left.getCost():
                    possibleStates.append(right)
                    possibleStates.append(left)
                return possibleStates
        if left.getCost() == max(right.getCost(), down.getCost(), left.getCost()):
            if left.getCost() != right.getCost() and down.getCost() != left.getCost():
                possibleStates.append(left)
                return possibleStates
            else:
                if left.getCost() == right.getCost():
                    possibleStates.append(left)
                    possibleStates.append(right)
                if down.getCost() == left.getCost():
                    possibleStates.append(down)
                    possibleStates.append(left)
                return possibleStates
        
        return possibleStates

class UI:
    def __init__(self, controller):
        self.controller = controller

    def mainMenu(self):
        print("Option 1: DFS Solution\nOption 2: GBFS Solution\nOption 0: EXIT")
        nb = int(input("Choose an option: "))
        while nb != 0:
            if nb == 1:
                self.controller.DFS()
            if nb == 2:
                self.controller.GBFS()
            print("New")
            self.controller.printMatrix()
            print("Option 1: DFS Solution\nOption 2: GBFS Solution\nOption 0: EXIT")
            nb = int(input("Choose an option: "))
        print("Exiting...")

class RUN:
    def __init__(self):
        n = int(input("N: "))
        c = Controller(n)
        u = UI(c)
        u.mainMenu()

r = RUN()