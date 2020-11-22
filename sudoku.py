import queue
import sys
import copy



variable_matrix=[["A1","A2","A3","A4"],["B1","B2","B3","B4"],["C1","C2","C3","C4"]
                 ,["D1","D2","D3","D4"]]

constraints=[
    [["A2","A3","A4","B1","C1","D1","B2"],["A1","A3","A4","B2","C2","D2","B1"],["A1","A2","A4","B3","C3","D3","B4"],["A1","A2","A3","B4","C4","D4","B3"]]
    ,[["B2","B3","B4","A1","C1","D1","A2"],["B1","B3","B4","A2","C2","D2","A1"],["B1","B2","B4","A3","C3","D3","A4"],["B1","B2","B3","A4","C4","D4","A3"]]
    ,[["C2","C3","C4","B1","A1","D1","D2"],["C1","C3","C4","B2","A2","D2","D1"],["C1","C2","C4","B3","A3","D3","D4"],["C1","C2","C3","B4","A4","D4","D3"]]
    ,[["D2","D3","D4","B1","C1","A1","C2"],["D1","D3","D4","B2","C2","A2","C1"],["D1","D2","D4","B3","C3","A3","C4"],["D1","D2","D3","B4","C4","A4","C3"]]
             ]

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

    for i in range(4):
        for j in range(4):
            key=variable_matrix[i][j]
            domain=csp[key][0]

            if len(domain)>1:
                return False

    return True


def generate_domain(board):
    domain=[[],[],[],[]]

    temp=list(board)
    temp2=[]
    for i in temp:
        temp2.append(int(i))

    for i in range(4):
        for j in range(4):
            domain[i].append([temp2[4*i+j]])


    for i in range(4):
        for j in range(4):
            if domain[i][j][0]==0:
                domain[i][j]=[1,2,3,4]
    
    return domain
        

def forwardCheck(csp):


    for i in range(4):
        for j in range(4):
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
    for i in range(4):
        for j in range(4):
            tmp=variable_matrix[i][j][0]
            if len(csp[variable_matrix[i][j]][0])==1:
                total=total+1
    

    if total==16 and not totalColTest(csp):
        return True

    return False

def totalColTest(csp):
    collisions=0

    for i in range(4):
        for j in range(4):
            val=variable_matrix[i][j]
            if collisionTest(csp,val):
                return True

    return False



#def AC_3(csp):

#def revise:

def MRV(csp):

    mrv=1000

    minkey=''
    
    for i in range(4):
        for j in range(4):
            key=variable_matrix[i][j]

            domain=csp[key][0]

            d1=len(domain)

            if d1<mrv and d1!=1:
                mrv=d1
                minkey=key

    return minkey


#def solutionQ(csp):



def display(csp):
    
    for i in range(4):
        line=[]
        for j in range(4):
            key=variable_matrix[i][j]
            domainDi=csp[key][0]
            line.append(domainDi)
        print(str(line))
            




            


def main():

    sys.argv=[sys.argv[0],'0403002000013000']

    csp={}

    domain=generate_domain(sys.argv[1])

    for i in range(4):
        for j in range(4):
            csp.update({variable_matrix[i][j]:[domain[i][j],constraints[i][j]]})
            #print(variable_matrix[i][j]+"  "+str(csp[variable_matrix[i][j]][0])+" "+str(csp[variable_matrix[i][j]][1]))

    solution=BTS_search(csp)

    display(solution)
    

if __name__=="__main__":
    main()
