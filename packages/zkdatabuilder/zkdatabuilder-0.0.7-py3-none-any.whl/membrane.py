def membrane(r=14,index=0,atom_type=1):
    import numpy as np
    from cap import cap
    from cylinder import cylinder
    
    cyl = cylinder(r,index,atom_type)
    index += len(cyl)
    
    cap = cap(r,index,atom_type)
    
    memb = np.append(cyl,cap)
    memb = np.array(memb)
    ncol = 6
    nrow = int(len(memb)/ncol)
    memb = memb.reshape(nrow,ncol)
    return memb

