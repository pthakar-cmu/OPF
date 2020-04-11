import numpy as np
import math as mt

def delPdelQ(Y, P, Q, V, delta):

    Zb = (max(np.array(V)) ** 2 / max(abs(np.concatenate([P, Q]))))
    P = P / max(abs(np.concatenate([P, Q])))
    Q = Q / max(abs(np.concatenate([P, Q])))
    V = V / max(np.array(V))
    Y = Zb * Y

    n = np.shape(Y)
    Yintermediate = -Y
    num_row = n[0]
    num_col = n[1]
    delP = []
    delQ = []
    for k in range(num_row):
        SumP = 0
        SumQ = 0
        for m in range(num_col):
            if k!=m:
                SumP = SumP + (V[k] * V[m] * ((np.real(Yintermediate[k, m]) * mt.cos(delta[k] - delta[m])) +
                                            (np.imag(Yintermediate[k, m]) * mt.sin(delta[k] - delta[m]))))
                SumQ = SumQ + (V[k] * V[m] * ((np.real(Yintermediate[k, m]) * mt.sin(delta[k] - delta[m])) -
                                            (np.imag(Yintermediate[k, m]) * mt.cos(delta[k] - delta[m]))))

        Pc = P[k] - ((V[k]**2)*np.real(Y[k, k])) + SumP - 1
        Qc = Q[k] + ((V[k]**2)*np.imag(Y[k, k])) + SumQ - 1
        delP.append(Pc)
        delQ.append(Qc)
        ActivePower_losses = sum(P+Pc)
        ReactivePower_losses = sum(Q+Qc)

    return delP,delQ

