import numpy as np
import math as mt

def DelPDelQ(Y, P, Q, V, delta, PV_Bus, PQ_Bus, slack_no=0):


    n = np.shape(Y)
    Yintermediate = -Y
    num_row = n[0]
    num_col = n[1]
    Pc = []
    Qc = []
    for k in range(num_row):
        SumP = 0
        SumQ = 0
        for m in range(num_col):
            if k!=m:
                SumP = SumP + (V[k] * V[m] * ((np.real(Yintermediate[k, m]) * mt.cos(delta[k] - delta[m])) +
                                          (np.imag(Yintermediate[k, m]) * mt.sin(delta[k] - delta[m]))))
                SumQ = SumQ + (V[k] * V[m] * ((np.real(Yintermediate[k, m]) * mt.sin(delta[k] - delta[m])) -
                                          (np.imag(Yintermediate[k, m]) * mt.cos(delta[k] - delta[m]))))

        delP =  P[k] - ((V[k]**2)*np.real(Y[k, k])) + SumP
        delQ =  Q[k] + ((V[k]**2)*np.imag(Y[k, k])) + SumQ
        Pc.append(delP)
        Qc.append(delQ)

    return Pc,Qc
