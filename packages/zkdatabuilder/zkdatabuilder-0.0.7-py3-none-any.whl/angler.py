def angler(n=2400,um=20):

    from freeTF import freetf
    import numpy as np
    
    clps = (n/20*23)
    
    
    free = freetf(um,clps,n)
    
    fr = int(len(free)/3)
    btf = int(clps/23)
    
    ntyp = 1
    
    tfs = btf +fr
    
    
    num_angles = n+tfs
    angles = np.zeros([num_angles,5])
    index = 0
    
    for i in range(n):
        index += 1
        
        if i<n-2:
            angles[i]=[index,ntyp,index,index+1,index+2]
        elif i==n-2:
            angles[i]=[index,ntyp,index,index+1,1]
        elif i==n-1:
            angles[i]=[index,ntyp,index,1,2]
    
    tftyp = 2
    indx = index +1
    for j in range(tfs):
        index = index +1
        angles[n+j]=[index,tftyp,indx+j,indx+j+1,indx+j+2]
        indx = indx +2
        
    return angles

angles = angler(2400)