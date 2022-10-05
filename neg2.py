from ast import Num
import math
import matplotlib.pyplot as plt

ba = 2

def to10(n,b):
    num = 0
    nlist = list(str(n))
    for i in range(0,len(nlist)):
        if (i-1) % 2 == 0:
            num-= int(nlist[-i-1]) * (b)**(i)
        else:
            num+= int(nlist[-i-1]) * (b)**(i)
    return num
def b(b):
    global ba
    ba = b

def listto(n):
    arr = []
    for i in range(n):
        arr.append(to10(inttobase(i)))

def plot(n,b):
    arr = []
    arr2 = []
    for i in range(n):
        arr.append(int(to10(inttobase(i,b),b)))
        arr2.append(i)
    plt.plot(arr2,arr,'ro')
    #plt.axis([0,n,-1*abs(arr[-1]),abs(arr[-1])])
    plt.show()

digequiv = ["0","1","2","3","4","5","6","7","8","9"]

def inttobase(n,b): # Converts int_10 (int) into integer_tobase (str)
    n = int(n)
    if n == 0:
        return '0'
    num = [] # resultant int_tobase (list)
    lenout = math.floor(math.log(n,b) + 1.0000000000001) # digits length of resultant number
    for exp in range(lenout-1,-1,-1): # for each order of magnitude (number of digits) in integer_10, starting at highest (furthest left)
        mag = b**exp # tobase raised to power of digit currently being written
        times = math.floor(n/mag) # number of times mag fits into n, rounded down 
        n -= times * mag # determines remainder (rounded down portion in previous line)
        num.append(digequiv[times]) # appends the digit corresponding to how many times the current order of magnitude fit into the original number
    return(int(''.join(num))) # returns integer_tobase (str)

        


#def from10(n):

