def membrane(r,index,atom_type):
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

