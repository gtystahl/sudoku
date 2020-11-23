#TODO: At the end of this before turning the project in, print out the contents of all of the lists that are made in constraintmaker


import queue
import sys
import copy
# Wont need this in the end
# from constraintMaker import *

def createConstraints():
    # This creates the contraints so I dont have to.
    mat = createMatrix()
    ret = []
    for a in range(9):
        row = []
        for b in range(9):
            item = mat[a][b]
            col = []

            # Here is the rows contraints
            for item2 in mat[a]:
                if not item2 in col and item2 != item:
                    col.append(item2)

            # Here is the column constraint
            for i in range(9):
                item2 = mat[i][b]
                if not item2 in col and item2 != item:
                    col.append(item2)

            # Here is the box. A little harder
            y = a // 3
            x = b // 3

            for c in range(3):
                for d in range(3):
                    item2 = mat[(y * 3) + c][(x * 3) + d]
                    if not item2 in col and item2 != item:
                        col.append(item2)
            row.append(col)
        ret.append(row)
    return ret

def createMatrix():
    # This creates the matrix. Will be printed out at the end to be turned in
    letters = "A B C D E F G H I"
    # letters = "A B C D"
    lets = letters.split(" ")
    ret = []
    for let in lets:
        lst = []
        for i in range(1,10):
            lst.append(let + str(i))
        ret.append(lst)
    return ret

variable_matrix = createMatrix()

variable_matrix2=[["A1","A2","A3","A4"],["B1","B2","B3","B4"],["C1","C2","C3","C4"]
                 ,["D1","D2","D3","D4"]]


constraints = createConstraints()

constraints2=[
    [["A2","A3","A4","B1","C1","D1","B2"],["A1","A3","A4","B2","C2","D2","B1"],["A1","A2","A4","B3","C3","D3","B4"],["A1","A2","A3","B4","C4","D4","B3"]]
    ,[["B2","B3","B4","A1","C1","D1","A2"],["B1","B3","B4","A2","C2","D2","A1"],["B1","B2","B4","A3","C3","D3","A4"],["B1","B2","B3","A4","C4","D4","A3"]]
    ,[["C2","C3","C4","B1","A1","D1","D2"],["C1","C3","C4","B2","A2","D2","D1"],["C1","C2","C4","B3","A3","D3","D4"],["C1","C2","C3","B4","A4","D4","D3"]]
    ,[["D2","D3","D4","B1","C1","A1","C2"],["D1","D3","D4","B2","C2","A2","C1"],["D1","D2","D4","B3","C3","A3","C4"],["D1","D2","D3","B4","C4","A4","C3"]]
             ]

# print(variable_matrix == variable_matrix2)
# print(constraints == constraints2)
print()


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



# Notes:
# The formats of stuff
# csp: {cell : [[list of possibles], [constraints]]}
# xi and xj are the items. They are in their key form
# domain is the list of possibles values
# xi.neighbors is the constraints
# The format will come close to the book but will deviate in format
def Asearch(csp):
    if doneQ(csp):
        return csp

    var = MRV(csp)
    if var == '':
        return None

    domains = csp[var][0]

    for i in domains:

        tempCSP = copy.deepcopy(csp)

        tempCSP[var][0] = [i]

        AC_3(csp)

        if not collisionTest(tempCSP, var):
            result = BTS(tempCSP)

            if result != None:
                return result

    return None

def AC_3(csp):
    # This needs to contain the arcs of the csp
    q = queue.Queue()
    createArcs(csp, q)

    while not q.empty():
        # display(csp)
        (xi, xj) = q.get()
        if revise(csp,xi,xj):
            if csp[xi][0] == 0:
                return False
            for xk in csp[xi][1]:
                if xk != xj:
                    q.put(xk, xi)
    return True

def revise(csp, xi, xj):
    revised = False
    good = False
    lst = []
    for num1 in csp[xi][0]:
        for num2 in csp[xj][0]:
            if num1 != num2:
                good = True
                break
        if good:
           lst.append(num1)
        else:
            revised = True
    csp[xi][0] = lst

def createArcs(csp, q):
    for key in csp:
        for con in csp[key][1]:
            q.put((key, con))

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


#def solutionQ(csp):



def display(csp):
    
    for i in range(9):
        line=[]
        for j in range(9):
            key=variable_matrix[i][j]
            domainDi=csp[key][0]
            line.append(domainDi)
        print(str(line))
            




            


def main():

    # sys.argv=[sys.argv[0],'0403002000013000']
    sys.argv = [sys.argv[0], '000000000302540000050301070000000004409006005023054790000000050700810000080060009']

    csp={}

    domain=generate_domain(sys.argv[1])

    for i in range(9):
        for j in range(9):
            csp.update({variable_matrix[i][j]:[domain[i][j],constraints[i][j]]})
            #print(variable_matrix[i][j]+"  "+str(csp[variable_matrix[i][j]][0])+" "+str(csp[variable_matrix[i][j]][1]))

    solution = Asearch(csp)
    display(solution)

    # solution=BTS_search(csp)
    # display(solution)
    

if __name__=="__main__":
    main()
