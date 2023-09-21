import collections
import math
import sys,random

items=[]
classes=[]
vecSize=None
graphSize=0
totDist=0
class classification:
    def __init__(self):
        self.vector=[]
        self.items=[]
        for _ in range(vecSize):
            self.vector.append(random.randint(0,int(graphSize*3/4)))
        self.name=chr(65+len(classes))
    def addItem(self,i):
        self.items.append(i)
    def reset(self):
        self.items = []
    def resetCenteroid(self):
        newCenter=avg(self.items)
        if newCenter is not None:
            self.vector=newCenter
    def __eq__(self, other):
        return self.name==other.name



class item:
    def __init__(self,line):
        global vecSize,graphSize
        self.vector=line.split(",")[:-1]
        self.vector=list(map(float,self.vector))
        self.classification=line.split(",")[-1]
        self.assignedClass = None
        self.previousClass = None
        if vecSize is None:
            vecSize=len(self.vector)
        graphSize=int(max(self.vector+[graphSize]))
    def setClass(self,cls):
        self.previousClass=self.assignedClass
        self.assignedClass=cls
        cls.addItem(self)
    def classChanged(self):
        return(self.assignedClass!=self.previousClass)
    def getClosest(self):
        global totDist
        min=classes[0]
        minDist=getDistance(classes[0].vector,self.vector)
        for i in classes:
            dist=getDistance(i.vector,self.vector)
            if dist<minDist:
                min=i
                minDist=dist
        self.setClass(min)
        totDist+=minDist

def avg(items):
    if len(items)==0:
        return None
    sm=[0]*len(items[0].vector)
    for i in range(len(sm)):
        for j in items:
            sm[i]+=j.vector[i]
        sm[i]=sm[i]/len(items)
    return sm
def getDistance(v1,v2):
    sum=0
    for i in range(len(v1)):
        sum+=math.pow(v1[i]-v2[i],2)
    return math.sqrt(sum)
def readTo(file,l):
    with open(file) as file:
        for line in file:
            l.append(item(line.rstrip()))
def assignToClass():
    for i in classes:
        i.reset()
    for i in items:
        i.getClosest()
def realignClasses():
    for i in classes:
        i.resetCenteroid()
def anyChange():
    for i in items:
        if i.classChanged():
            return True
    return False
def report():
    total = collections.Counter(map(lambda i: i.classification,items))
    for i in classes:
        print(i.name+":")
        contents=collections.Counter(map(lambda i: i.classification,i.items))
        for j in contents:
            print("   {}: {}%".format(j,contents[j]/total[j]*100))
        print()
def classify(k):
    global classes,totDist
    classes=[]
    for _ in range(k):
        classes.append(classification())
    i=0
    while i<2 or anyChange():
        assignToClass()
        realignClasses()
        i+=1
        print("Iteration {}: {}".format(i,totDist))
        totDist=0
    report()
if __name__ == "__main__":
    readTo(sys.argv[1],items)
    for i in range(5):
        print("-------------------------------------------Test {}-----------------------------------------------".format(i+1))
        classify(int(sys.argv[2]))
