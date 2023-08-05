def boundtf(fname):
    
    
    import numpy as np
    from position import steal
    
    atoms = steal(fname)
    
    nrow = len(atoms)
    n = nrow
    ncol = 6
    
    bound = np.zeros([int(nrow*3/20),ncol]) 
    
    i = 0
    for r in range(n-1):
        
        row = atoms[r]
        rowr = atoms[r+1]
        
        if (r+1)%20 == 1:
            bound[i]=[i+n+1,4,4,row[3]+0.6,row[4],row[5]]
            bound[i+1]=[i+n+2,5,5,row[3]+1.4,row[4],row[5]]
            bound[i+2]=[i+n+3,4,4,rowr[3]+0.6,rowr[4],rowr[5]]
            i +=3
            
    total = np.append(atoms,bound)
    nrow = int(len(total)/6)
    total = total.reshape(nrow,ncol)

    return total
