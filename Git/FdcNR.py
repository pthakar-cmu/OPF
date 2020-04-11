import numpy as np
import math as mt
from dPdQ import delPdelQ

def delVdelD(Y, P, Q, V, delta, PV_Bus, PQ_Bus, slack_no=0):

# To convert System into PerUnit, uncomment the commands below:
##
    # Zb = (max(np.array(V)) ** 2 / max(abs(np.concatenate([P, Q]))))
    # P = P / max(abs(np.concatenate([P, Q])))
    # Q = Q / max(abs(np.concatenate([P, Q])))
    # V = V / max(np.array(V))
    # Y = Zb * Y
##

    [delP,delQ]=delPdelQ(Y, P, Q, V, delta)
    delP=np.array(delP)
    delQ=np.array(delQ)
    V=np.array(V)
    delta=np.array(delta)

    pv = np.array(PV_Bus)
    for i in range(len(PV_Bus)):
        pv[i] = pv[i] - 1

    pq = np.array(PQ_Bus)
    for i in range(len(PQ_Bus)):
        pq[i] = pq[i] - 1

    pvpq = PV_Bus + PQ_Bus
    for i in range(len(pvpq)):
        pvpq[i] = pvpq[i] - 1
    pvpq.sort()
    pvpq = np.array(pvpq)

    Bdash = np.delete(Y, slack_no, 1)
    Bdash = np.delete(Bdash, slack_no, 0)
    Bdash = np.imag(Bdash)
    Bdash_inv = np.linalg.inv(-Bdash)      ### Check for negative sign
    # print ("B'_inv", Bdash_inv)
    # print ("B''_inv",Bdashdash_inv)

    slack_no = np.array([slack_no])
    sp = np.concatenate((slack_no, pv))
    Bdashdash = np.delete(Y, sp, 1)
    Bdashdash = np.delete(Bdashdash, sp, 0)
    Bdashdash = np.imag(Bdashdash)
    Bdashdash_inv = np.linalg.inv(-Bdashdash)      ### Check for negative sign

    iteration = 0
    tolerance = 1
    while tolerance > 0.001:
    # for iteration in range(0,20):
    #     print("delP delQ", delP, delQ)

        delD = np.matmul(Bdash_inv, delP[pvpq]/V[pvpq])
        delV = np.matmul(Bdashdash_inv, delQ[pq]/(V[pq]))

        # print("delV delD", delV, delD)

        # delD_rad = np.radians(delD)
        delta[pvpq] = delta[pvpq] + delD
        V[pq] = V[pq] + delV

        # print("V", V)
        # print("Delta", np.degrees(delta)
        [delP, delQ] = delPdelQ(Y, P, Q, V, delta)
        delP = np.array(delP)
        delQ = np.array(delQ)

        Error = np.concatenate([delP[pvpq], delQ[pq]])
        tolerance = abs(max(Error))
        iteration = iteration+1


    return iteration,V,np.degrees(delta)