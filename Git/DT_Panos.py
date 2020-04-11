import numpy as np
import csv

# input file to list
def read_file(filename):
    with open(filename) as f:
        reader = csv.reader(f, delimiter="\t")
        d = list(reader)
    return (d)

# initialize gen limits
def checked_fill(arr):
    chk1=np.amin(arr[:,:-1], axis=0)
    chk2=np.amax(arr[:,:-1], axis=0)
    chk=[]
    for i in range(len(chk1)):
        chk=np.append(chk,0.9999*chk1[i])
        chk=np.append(chk,1.0001*chk2[i])
    return(chk)

# compare rule to training set and count T/Fs
def count_TFs(arr,match):
    t_size, atts = arr.shape
    atts = atts-1
    countr=0
    countrT=0
    for j in range(t_size):
        i=0
        while i<atts:
            if arr[j][i]>=match[2*i] and arr[j][i]<=match[2*i+1]:
                i=i+1
            else:
                i=atts+5
        if i==atts:
            countrT=countrT + arr[j][i]
            countr=countr+1
    return(int(countrT),int(countr))

# Shannon entropy calculation
def Sh_entr(perc):
    if perc==0 or perc==1:
        return(0)
    else:
        return(-perc*np.log2(perc)-(1-perc)*np.log2(1-perc))

# ~~ MAIN ~~
# read input
t_set = np.array(read_file("DT_PopulationPerm1.txt")).astype(np.float)
t_set_size, atts = t_set.shape
atts = atts - 1

# initialize rules matrix
checked=[1]
checked=np.append(checked,np.array(checked_fill(t_set)).astype(np.float))
Tr, tot = count_TFs(t_set,checked[+1:])
checked=np.append(checked,float(Tr/tot))
checked=checked[np.newaxis,:]
# checked matrix: every line one node (root, internal or leaf)
# in every line first column whether it has been checked for a
# split or not (see following), every next pair of columns min
# and max of every generator in the subset of that node and
# final column how many elements in that node are True

bins=50

while 1 in checked[:,0]:
    # 1 if node has not been checked for a split yet
    # 0 if it has been split
    # -1 if it is a leaf-node (checked and can't be split further)
    split=[-1,0,0]
    # split[0] attribute to split,
    # split[1] splitting value of attribute,
    # split[2] IG
    sz,clns = checked.shape
    i=0
    while i<sz:
        if checked[i][0]==1:
            fd=i
            i=sz+5
        else:
            i=i+1
    Tr, tot = count_TFs(t_set,checked[fd,+1:-1])
    Hpre=Sh_entr(Tr/tot)
    for i in range(atts):
        bn=(checked[fd,1+2*i+1]-checked[fd,1+2*i])/bins
        if bn>0:
            lol=[]
            upl=[]
            for j in range(bins-1):
                lol[:]=checked[fd,+1:-1]
                lol[2*i+1]=checked[fd,1+2*i]+(j+1)*bn
                upl[:]=checked[fd,+1:-1]
                upl[2*i]=checked[fd,1+2*i]+(j+1)*bn
                Tr1, tot1 = count_TFs(t_set,lol)
                Tr2, tot2 = count_TFs(t_set,upl)
                if tot1>0 and tot2>0:
                    
                    Hy=Sh_entr(Tr1/tot1)
                    Hn=Sh_entr(Tr2/tot2)
                    IG=Hpre-tot1*Hy/(tot1+tot2)-tot2*Hn/(tot1+tot2)
                    #IG=2*IG/(Hpre+Sh_entr(tot1/(tot1+tot2)))
                    #*(Hpre+Sh_entr(tot1/(tot1+tot2)))/2
                    if IG>split[2] and IG*(tot1+tot2)>10.7168:
                        split=[i,upl[2*i],IG]
    tmp=[]
    if split[0]>-1:
        # add the two new children-nodes in the checked matrix
        # copy-paste the father-node and update the upper-lower
        # of the split generator and the count of Trues
        tmp[:]=checked[fd,+1:-1]
        tmp[2*split[0]+1]=split[1]
        Tr, tot = count_TFs(t_set,tmp)
        tmp=np.append([1],tmp)
        tmp=np.append(tmp,[Tr/tot])
        checked=np.vstack([checked,tmp])
        tmp=[]
        tmp[:]=checked[fd,+1:-1]
        tmp[2*split[0]]=split[1]
        Tr, tot = count_TFs(t_set,tmp)
        tmp=np.append([1],tmp)
        tmp=np.append(tmp,[Tr/tot])
        checked=np.vstack([checked,tmp])
        checked[fd][0]=0
    else:
        checked[fd][0]=-1
    #print(checked)

np.savetxt('2darray.csv', checked, delimiter=',', fmt='%f')
print('done!')



