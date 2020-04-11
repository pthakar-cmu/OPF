import numpy as np
import random as rd
def Randomizer(ActiveLoad, P_max, P_min):

    nbus = len(P_max)

    P_gen=np.zeros(nbus).tolist()

    for i in range(0,nbus):
            P_gen[i] = np.arange(P_min[i], P_max[i], 1).tolist()
            P_gen[i] = [x+1 for x in P_gen[i]]
    P_gen = np.array(P_gen)

    P_output=np.zeros(nbus).tolist()

    while True:
            for i in range(0,nbus):
                P_output[i] = rd.choice(P_gen[i])
            if sum(P_output) == ActiveLoad:
                print(P_output)
            break

    return (P_output)
