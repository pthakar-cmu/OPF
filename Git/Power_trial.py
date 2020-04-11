from dPdQ import delPdelQ
from FdcNR import delVdelD
import Ymatrix
from File import DP
import numpy as np
Y=Ymatrix.mat
P=[2.22400000000000, 0.193000000000000, -0.992000000000000, -0.478000000000000, -0.0760000000000000, -0.112000000000000, 0, 0, -0.3000000000000, -0.100000000000000, -0.40000000000000,-0.0620000000000000,-0.135000000000000,-0.149000000000000]
Q=[-0.180, 0.3, 0.0440, 0.1, -0.018, 0.050, 0, 0.1840, -0.1660, -0.0580, -0.0180, -0.020, -0.060, -0.0600]
V=[ 1.0600, 1.0450, 1.0100, 1.0000, 1.0000, 1.0700, 1.0000, 1.0900, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000]
delta=np.zeros(14)*1.0
PV_Bus = [2,3,6,8]
PQ_Bus = [4,5,7,9,10,11,12,13,14]
DLPDLQ = delPdelQ(Y, P, Q, V, delta)
DLDDLV = delVdelD(Y, P, Q, V, delta, PV_Bus, PQ_Bus, slack_no=0)
print(DLPDLQ)
print(DLDDLV)