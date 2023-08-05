def bonder(n=2400,um=20):

    from freeTF import freetf
    import numpy as np


    clps = int(n/20*23)
    free = freetf(um,clps,n)
    fr = int(len(free)/3)
    btf = int(clps/23)
    
    ntyp = 1
    
    tfs = btf +fr
    
    num_bonds = n+tfs*2
    bonds = np.zeros([num_bonds,4])
    index = 0
    
    ntyp = 1
    for i in range(n):
        index +=1
        if index < n:
            bonds[i] = [index,ntyp,index,index+1]
        elif index == n:
            bonds[i] = [index,ntyp,index,1]
            
    
    tftyp = 2
    indx = n
    b = 0
    for index in range(n+1,n+tfs*3+1,3):
        ilk = index
        iki = index+1
        uc = index+2
        bonds[indx] = [index+b,tftyp,ilk,iki]
        indx +=1
        bonds [indx] = [index+b+1,tftyp,iki,uc]
        indx +=1
        b-=1
    
    return bonds

bonds = bonder(2400)