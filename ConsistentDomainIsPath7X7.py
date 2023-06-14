import time
import numpy
from variable import Variable
import math
import itertools
import Tests


colorStart = dict()
colorEnd = dict()
''' gets in initial board and return a list of variables
 each variable represents a square in the board
'''
def setVariables(board):
    variables = []
    colors = allColors.copy()
    for i in range(len(board)):
        for j in range(len(board)):
            variables.append(Variable((i,j), board[i][j]))
            if(board[i][j] != '0' and board[i][j] not in colors):
                variables[i*len(board) + j].isTarget =True
                colorEnd[board[i][j]] = variables[i*len(board) + j]
            if(board[i][j] in colors):
                colors.remove(board[i][j])
                variables[i*len(board) + j].isSource =True
                colorStart[board[i][j]] = variables[i*len(board) + j]
    return variables


''' get a list of variables and prints it in a matrix form , each variable is printed and presented in the following format:
 (previous variable, color of square, next variable)
'''
def printvars(variables, length):
    for i in range(length):
        for j in range(length):
            if variables[i*length + j].isSource:
                if variables[i*length + j].next == None:
                    print(("s",variables[i*length + j].color, '-' ),end="",flush=True)
                else:
                    print(("s",variables[i*length + j].color, variables[i*length + j].next.position),end="",flush=True)
            elif variables[i*length + j].isTarget:
                if variables[i*length + j].previous == None:
                    print(("-",variables[i*length + j].color, "t"),end="",flush=True)
                else:
                    print((variables[i*length + j].previous.position, variables[i*length + j].color,"t"),end="",flush=True)
            else:
                if variables[i*length + j].previous == None and variables[i*length + j].next == None:
                    print (('-',variables[i*length + j].color, '-'),end="",flush=True)
                else:
                    print((variables[i*length + j].previous.position, variables[i*length + j].color,variables[i*length + j].next.position ),end="",flush=True)
            print(" ",end="",flush=True)
        print()
        
''' print a  board
'''
def printMatrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            print(matrix[i][j],end="",flush=True)
            print(" ",end="",flush=True)
        print()

'''
print a the variables in board format and only color of variables
'''
def printVarBoard(varBoard):
    for i in range(len(varBoard)):
        for j in range(len(varBoard)):
            print(varBoard[i][j].color,end="",flush=True)
            print(" ",end="",flush=True)
        print()
"""
getting color and checks if there is an path between the source and the
Target
"""
def is_Path(color):
    VarStart = colorStart[color]  
    VarEnd = colorEnd[color]
    while(VarStart.next != None):
            if(VarStart.next == VarEnd):
                break
            VarStart = VarStart.next
    if(VarStart.next == VarEnd):
            return True
    else:
            return False
        
'''
constraints return true if an assiagnment fullfills the constraints
'''
def constraints(variable, value):
    
    # here the value is a suggested neighbor to be the source's 'next'
    if variable.isSource:
        # this is constraint on next in general value == next
        for neighbor in variable.getNeighbors():
            if neighbor.previous == variable and neighbor != value:
                
                return False
        if value.isTarget or (value.color != '0' and value.color != variable.color) or (value.color == variable.color and value.previous != None and value.previous != variable):
            return False
        return True
    # here the value is a suggested neighbor to be the target's 'previous'
    elif variable.isTarget:
        #this is constraint on previous in general
        for neighbor in variable.getNeighbors():
            if neighbor.next == variable and neighbor != value:
                return False
            if value.isSource or (value.color != '0' and value.color != variable.color) or (value.color == variable.color and   value.next != None and value.next != variable):
                return False
        return True
    # here the suggest value is a vector (neighbor for previous, color , neighbor for next)
    else:
        #checking if there is a path for this color
        if (is_Path(value[1])):
            return False
        ##constraint on next (value[2])
        for neighbor in variable.getNeighbors():
            if neighbor.previous == variable and neighbor != value[2]:
                return False
        if  value[2].isSource or (value[2].color != '0' and value[2].color != value[1]) or (value[2].color == value[1] and value[2].previous != None and value[2].previous != variable):
            return False
        for neighbor in variable.getNeighbors():
            if neighbor.next == variable and neighbor != value[0]:
                return False
        ##constraint on previous (value[0])
        if  value[0].isTarget or (value[0].color != '0' and value[0].color != value[1]) or (value[0].color == value[1] and value[0].next != None and  value[0].next != variable):
            return False
        return True
    
'''
select a value to be assigned that is consistent
'''
def selectValue(variable):
    while(len(variable.legalValues) > 0): 
        value =  variable.legalValues[0]
        variable.legalValues.remove(value)
        if constraints(variable, value): # value is consistent
            return value
    return None


def getConsistentDomain(variable, allcolors):
    neighbors = variable.getNeighbors()
    if(variable.isSource):
        domain = neighbors # the possiblitites is only on the next neighbor to go to not the color.
        domain = [ d for d in domain if constraints(variable, d)]                   # the assignment is only on what is the next variable , color is already assigned, and no previous for this variable
    elif(variable.isTarget):
        domain = neighbors # possibilities is only on the previous neighbor not color
        domain = [ d for d in domain if constraints(variable, d)]
    else:
        domain = list(itertools.product(neighbors, allcolors, neighbors))
        domain =  [d for d in domain if d[0] != d[2] and constraints(variable, d)]
    return domain

'''reseting the variable's legal to to a domain consistent with the current assignmen
'''
def resetVariable(variable, allcolors):
    variable.legalValues = getConsistentDomain(variable, allcolors)
    if not(variable.isTarget or variable.isSource):
        variable.color = '0'
    variable.next = None
    variable.previous = None
    return variable
'''
iterative backtracking algorithm for the csp problem.
'''
def backtrack(variables,allcolors):
    i = 0
    variables[i] = resetVariable(variables[i], allcolors)
    while(i >= 0 and i < len(variables)):
        value = selectValue(variables[i])
        if value == None:
            # backtracking
            variables[i] = resetVariable(variables[i], allcolors)
            i -= 1
        else:
            # moving forward
            variables[i].setVariable(value)
            i += 1
            if i < len(variables):                
                variables[i]= resetVariable(variables[i], allcolors)        
    if i < 0 :
        return None
    else:
        return variables

for game in Tests.all7X7games:
    allColors =  game[0]
    board = game[1]
    length = len(board)
    print("board to solve")
    printMatrix(board)
    variables = setVariables(board)
##    print("display variables after being set")
##    printvars(variables,length)
    # set the neighbor of each variable
    for var in variables:
        var.setNeighbors(variables,length)
    # set the the lagal values for each 
    for var in variables:
        var.setVarDomain(allColors)         
    t0 = time.time()        
    variables = backtrack(variables,allColors)
    t1 = time.time() - t0
    print("----------solution-----------------")
    if variables == None:
        print("failure")
    else:
        for i in range(length):
                for j in range(length):
                    print(Variable.getVarByPos((i,j), variables).color,end="",flush=True)
                    print(" ",end="",flush=True)
                print()
    print("solution found after", t1, "seconds")
