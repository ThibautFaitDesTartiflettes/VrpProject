from math import sqrt
from random import randint, uniform
import datetime
import os


def Distance(a, b):
    return sqrt( (b.x-a.x)*(b.x-a.x) + (b.y-a.y)*(b.y-a.y) )

def SumDistance(points):
    s = 0
    for i in range(len(points)):
        dist = Distance(points[i], points[(i+1) % len(points)])
        s += dist
    return s

def PickSelection(myList, probabilities):
    i = 0
    r = uniform(0, 1)

    while r > 0:
        r -= probabilities[i]
        i += 1
    i -= 1
    return myList[i].copy()

def LexicalOrder(orderList):
    x = -1
    y = -1

    # Step 1 : Find the largest x such that Order[x]<Order[x+1]
    # (If there is no such x, Order is the last permutation.)
    for i in range(len(orderList)):
        if orderList[i] < orderList[(i+1)%len(orderList)]:
            x = i
    if x == -1:
        return orderList

    # Step 2 : Find the largest y such that Order[x]<Order[y].
    for i in range(len(orderList)):
        if orderList[x] < orderList[i]:
            y = i
    # Step 3 : Swap Order[x] and Order[y].
    orderList[x], orderList[y] = orderList[y], orderList[x]

    # Step 4 : Reverse Order[x+1 .. n].
    RightSidereversed = orderList[x+1:][::-1]
    orderList = orderList[:x+1]
    orderList.extend(RightSidereversed)
    # print(orderList)

    return orderList

def translateValue(value, min1, max1, min2, max2):
    return min2 + (max2 - min2)* ((value-min1)/(max1-min1))

def Factorial(n):
    if n == 1:
        return 1
    else:
        return n * Factorial(n - 1)

def FactorialOpti(n):
    s = 1
    for i in range(1,n):
        s*=i
    return s

def GetTimeStr(time):

    h = round((time%1) * 24)
    m = round(((time%1 * 24)%1)*60)
    if (time > 1):
        output =str(round(time))+" days "+ str(h)+':'+str(m)
    else:
        output = str(h)+':'+str(m)
    return output

def WriteFile(manager,selectedIndex, timeX,timeIteration):
    t = datetime.datetime.now()
    folderName = "Result"
    if (not(os.path.isdir(folderName))):
        os.mkdir(folderName)
    fileName =  folderName+"\\"+"CesiDPD_Result_"+str(t.year)+'-'+str(t.month)+'-'+str(t.day)+'_'+str(t.hour)+"h"+str(t.minute)+"min"+str(t.second)+"s"
    fileName+=".txt"
    f = open(fileName, "w")
    content = str()
    
    if (selectedIndex != 2): #no fourmi algo
        for i in range(len(manager.OptimalRoutes)):
            content+="Vertex : "+str(i)+"  "+str(manager.OptimalRoutes[i])+"\n"
    else: # fourmi algo
        for i in range(len(manager.antColony.best_tour)):
            #vertex
            content+="Vertex : "+str(i)+"  "+str(manager.antColony.nodes[i])+ " at "+ GetTimeStr(timeX) +"\n\n"

            #edges
            e = manager.antColony.edges[i][(i+1)%len(manager.antColony.best_tour)]
            content+="\t\tEdge betwen  "+ str(manager.antColony.nodes[e.b]) + "  to  "+ str(manager.antColony.nodes[e.a])+"\n"
            content+="\t\theuristic : "+str(round(e.heuristic,2))+"\n"
            content+="\t\tpheromone : "+str(round(e.pheromone,2))+"\n"
            content+="\t\tduration  :"+"("+str(round(e.coef1,2))+"cos("+str(round(timeX,2))+"*2*Pi))/6"
            content+="("+str(round(e.coef2,2))+"*cos("+str(round(timeX,2))+"*3*Pi))/6"
            content+="("+str(round(e.coef3,2))+"*cos("+str(round(timeX,2))+"*5*Pi))/6"
            content+="("+str(round(e.coef4,2))+"*cos("+str(round(timeX,2))+"*6*Pi))/6"
            timeTravel = e.CalcDist(timeX%1)
            content+=" = "+str(round(timeTravel,2)) + "  =  "+ GetTimeStr(timeTravel)
            content+="\n\n"
            timeX+=e.CalcDist(timeX)
            timeX = timeX

    f.write("calcul realized at  : "+str(datetime.datetime.now())+"\n")
    f.write("done in             : "+str(manager.timePassed)+"s\n")
    f.write("iteration           : "+str(manager.counter)+"\n")
    f.write("iteration time      : "+str(sum(timeIteration)/len(timeIteration))+"\n")
    f.write("n_points            : "+str(manager.n_points)+"\n")
    f.write("\n\n\nBest distance : "+str(manager.recordDistance))
    f.write("\n\npath : \n")
    f.write(content)

