def cylinder(r,index,atom_type):

    import math
    import numpy as np
    typ = atom_type
    cyl = np.array([])
    
    pir = r*3.14159
    pr = int(pir)
    
    for xcr in range (-2*r,2*r+1):
        
        
        for x in range(-pr,pr+1):
    
            index +=1
            ycr = math.cos(x/r)*r
            zcr = math.sin(x/r)*r
            coor = [index,typ,typ,xcr,ycr, zcr]
            coor = np.array(coor)
            
            cyl = np.append(cyl,coor)
            
    
    ncol = 6
    row = len(cyl)/ncol
    nrow =  int(row)
    
    cyl = cyl.reshape(nrow,ncol)
    return cyl
