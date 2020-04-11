import math
def Entropy(x):
    return((-x*math.log2(x))-((1-x)*math.log2(1-x)))
