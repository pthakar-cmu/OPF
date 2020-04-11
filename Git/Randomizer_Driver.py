from Randomizer import Randomizer
P_min = [1,2,3,2]
P_max = [10,11,12,14]
ActiveLoad = 38
Power_Generated = Randomizer(ActiveLoad, P_max, P_min)
print (Power_Generated)