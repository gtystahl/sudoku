# Project: Sudoku Solving AI proj 6
# Program name: driver.py
# Author: Greg Tystahl
# Date Created: 11/19/2020
# Purpose: Solve the puzzle using both AC3 and FC and putting that result in a finish file

# How to run: python3 driver.py. The name of the input file needs to be called in.txt and the name of the output
#   file will be output.txt

import queue
import sys
import copy

def createConstraints(mat):
    # This creates the contraints so I dont have to.

    # This the list that will holds the constraints to be returned
    ret = []

    # This goes through each row of the matrix
    for a in range(9):
        # This will hold each item in the rows contraints
        row = []
        # Goes through each item in the row
        for b in range(9):
            # Grabs the item
            item = mat[a][b]
            # creates a list that will hold the items constraints
            col = []

            # The creates the row constraints and adds it to the col list if it isn't already in there
            for item2 in mat[a]:
                if not item2 in col and item2 != item:
                    col.append(item2)

            # Adds the column constraints to col if they are not in there
            for i in range(9):
                item2 = mat[i][b]
                if not item2 in col and item2 != item:
                    col.append(item2)

            # Below is for the box it is in
            # This x and y determine the cordinate of the box
            # [0,0][1,0][2,0]
            # [0,1][1,1][2,1]
            # [0,2][1,2][2,2]
            y = a // 3
            x = b // 3

            # This goes through each row of the box
            for c in range(3):
                # This goes through each item of the box
                for d in range(3):
                    # This gets the item of the box
                    item2 = mat[(y * 3) + c][(x * 3) + d]
                    # If the item is not in the col list, add it
                    if not item2 in col and item2 != item:
                        col.append(item2)
            # Add all of the constraints to the row
            row.append(col)
        # Add the row to the returning matrix
        ret.append(row)
    # Return the list made
    return ret

def createMatrix():
    # This creates the matrix.

    # Letters in the form of a string cause I was lazy
    letters = "A B C D E F G H I"

    # Splits the letters into elements of a list
    lets = letters.split(" ")

    # This is the variable that will hold the matrix to be returned
    ret = []

    # Goes through each letter in the list of letters
    for let in lets:
        # This lst is the current row of the matrix
        lst = []
        # This goes through 1 - 10 to combine them to the letters
        for i in range(1,10):
            # Adds the combination to the row
            lst.append(let + str(i))
        # Adds the row to the matrix
        ret.append(lst)
    # Returns the finished matrix
    return ret

# This creates the matrix of a 9x9. To configure for a different size, you must change a lot of things to scale
variable_matrix = createMatrix()

# This creates the constraints for the matrix given above. Configured for a 9x9
constraints = createConstraints(variable_matrix)

# For the inclass code all I changed was to scale what we did so that all the functions work for a 9x9
# Beginning of class stuff:


def BTS_search(csp):

    return BTS(csp)


def BTS(csp):
    
    if doneQ(csp):
        return csp

    var=MRV(csp)
    if var=='':
        return None
    
    domains=csp[var][0]

    for i in domains:
        
        tempCSP=copy.deepcopy(csp)

        tempCSP[var][0]=[i]

        forwardCheck(tempCSP)
    
        if not collisionTest(tempCSP,var):
            result=BTS(tempCSP)

            if result!=None:
                return result

    return None


def collisionTest(csp,val):
    collisions=0

    domain1=csp[val][0]
    if len(domain1)==1:
         constraints=csp[val][1]
         for k in constraints:
             domain2=csp[k][0]
             if len(domain2)==1:
                 if domain1[0]==domain2[0]:
                    collisions=collisions+1
    
                     
    if collisions==0:
        return False
    return True


def DomainsComplete(csp):

    for i in range(9):
        for j in range(9):
            key=variable_matrix[i][j]
            domain=csp[key][0]

            if len(domain)>1:
                return False

    return True


def generate_domain(board):
    domain=[[],[],[],[],[],[],[],[],[]]

    temp=list(board)
    temp2=[]
    for i in temp:
        temp2.append(int(i))

    for i in range(9):
        for j in range(9):
            domain[i].append([temp2[9*i+j]])


    for i in range(9):
        for j in range(9):
            if domain[i][j][0]==0:
                domain[i][j]=[1,2,3,4,5,6,7,8,9]
    
    return domain
        

def forwardCheck(csp):

    for i in range(9):
        for j in range(9):
            key=variable_matrix[i][j]
            domainDi=csp[key][0]
            if len(domainDi)!=1:
                
                constraints=csp[key][1]

                for keyJ in constraints:
                    domainDj=csp[keyJ][0]

                    if len(domainDj)==1 and len(domainDi)>1:
                        try:
                            csp[key][0].remove(domainDj[0])
                        except:
                            pass


def doneQ(csp):
    total=0
    for i in range(9):
        for j in range(9):
            tmp=variable_matrix[i][j][0]
            if len(csp[variable_matrix[i][j]][0])==1:
                total=total+1

    if total==81 and not totalColTest(csp):
        return True

    return False


def totalColTest(csp):
    collisions=0

    for i in range(9):
        for j in range(9):
            val=variable_matrix[i][j]
            if collisionTest(csp,val):
                return True

    return False

# End of class stuff


def Asearch(csp):
    # This function is the same as BTS above but is changed to work for AC_3 instead
    if doneQ(csp):
        return csp

    var = MRV(csp)
    if var == '':
        return None

    domains = csp[var][0]

    for i in domains:

        tempCSP = copy.deepcopy(csp)

        tempCSP[var][0] = [i]

        # Here is where the AC_3 replaces the forward checking
        AC_3(csp)

        if not collisionTest(tempCSP, var):
            # The name was also changed here to Asearch. Ran into a problem here earlier
            result = Asearch(tempCSP)

            if result != None:
                return result

    return None


def AC_3(csp):
    # This is the AC_3 function. It uses pairs of items to filter out the numbers that cannot go in certain places
    # This and revise follow the format of the book

    # This queue holds the pairs of items
    q = queue.Queue()

    # This creates the arcs or as I have called them pairs for everything
    createArcs(csp, q)

    # While the queue is not empty
    while not q.empty():
        # Get the next pair of items
        (xi, xj) = q.get()
        # Revises the possible values of xi by the possibles of xj
        if revise(csp,xi,xj):
            # If there was a revision, check to make sure the new possibles of xi is not empty
            if len(csp[xi][0]) == 0:
                # If it is then there is a conflict. Return False
                return False
            # Go through all of the connections and add them back to the queue
            for xk in csp[xi][1]:
                if xk != xj:
                    q.put((xk, xi))
    # Return true if it cannot revise any longer and there are no conflicts
    return True


def revise(csp, xi, xj):
    # This revises the possible values of xi based on the possible values of xj

    # This is the variable that checks to see if there was a revision
    revised = False

    # This is the list that will hold the revised values of xi
    lst = []

    # Goes through each possible value of xi
    for num1 in csp[xi][0]:
        # This is a bool that checks to see if that value has a possible connection
        good = False
        # Goes through each possible value of xj
        for num2 in csp[xj][0]:
            # If there is a possible connection
            if num1 != num2:
                # Set good to True
                good = True
                # leave this for loop to save time
                break
        # If there is a connection
        if good:
            # Add the number back into xi possibles
            lst.append(num1)
        else:
            #If there is not a connection, dont add it back and set revised to True
            revised = True
    # Set the possibles of xi to lst
    csp[xi][0] = lst

    # Return the state of revised
    return revised


def createArcs(csp, q):
    # This creates connections of all items in the matrix. Only used at the start to fill the queue

    # For every item in the matrix
    for key in csp:
        # For each constraint of the item
        for con in csp[key][1]:
            # Add the pair to the queue
            q.put((key, con))


# In-class stuff again:
def MRV(csp):

    mrv=1000

    minkey=''
    
    for i in range(9):
        for j in range(9):
            key=variable_matrix[i][j]

            domain=csp[key][0]

            d1=len(domain)

            if d1<mrv and d1!=1:
                mrv=d1
                minkey=key

    return minkey


def display(csp):
    
    for i in range(9):
        line=[]
        for j in range(9):
            key=variable_matrix[i][j]
            domainDi=csp[key][0]
            line.append(domainDi)
        print(str(line))

# End of in class stuff


def main():

    # This clears out the old output
    f = open("output.txt", "w")
    f.close()

    # This opens the input file
    f = open("in.txt", "r")

    # This goes through each line of the input file
    for line in f:
        # This gets rid of the newline
        line = line.rstrip()

        # Creates the csp
        csp={}

        # Gets the domain of the puzzle
        domain=generate_domain(line)

        # Fills the csp with the values needed
        for i in range(9):
            for j in range(9):
                csp.update({variable_matrix[i][j]:[domain[i][j],constraints[i][j]]})

        # Creates a copy for the forward checking portion
        csp2 = copy.deepcopy(csp)

        # Gets the solution based on AC3
        solution = Asearch(csp)

        # If the solution is not none
        if solution:
            # Creates the line to be added to the output
            nl = ""
            # Goes through the matrix and gets the values and adds it to nl
            for key in solution:
                nl += str(solution[key][0][0])
            # Adds the AC3 label
            nl += " AC3"
            # Prints it to the screen to show its working
            print(nl)
            #Add it to output
            f2 = open("output.txt", "a")
            f2.write(nl + "\n")
            f2.close()
        else:
            # If it is none, set nl to the old line and add FAIL
            nl = line + " FAIL"
            # Print the line to show it failed
            print(nl)
            # Add the fail to the output
            f2 = open("output.txt", "a")
            f2.write(nl + "\n")
            f2.close()

        # Gets the solution of forward checking
        solution=BTS_search(csp2)

        # If the solution is not none
        if solution:
            # Creates the line to be added to the output
            nl = ""
            # Goes through the matrix and gets the values and adds it to nl
            for key in solution:
                nl += str(solution[key][0][0])
            # Adds the AC3 label
            nl += " FC"
            # Prints it to the screen to show its working
            print(nl)
            # Add it to output
            f2 = open("output.txt", "a")
            f2.write(nl + "\n")
            f2.close()
        else:
            # If it is none, set nl to the old line and add FAIL
            nl = line + " FAIL"
            # Print the line to show it failed
            print(nl)
            # Add the fail to the output
            f2 = open("output.txt", "a")
            f2.write(nl + "\n")
            f2.close()
    f.close()
    

if __name__=="__main__":
    main()
