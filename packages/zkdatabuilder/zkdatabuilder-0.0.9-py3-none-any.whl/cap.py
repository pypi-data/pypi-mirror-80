def cap(r,index,atom_type):
    import math
    import numpy as np
    
    r = r
    if 1 == 1:
        pi = math.pi
        r = r
        gs = r
        angle_num=int(pi*gs/2)
        cap = np.array([])
        typ = atom_type
        ncol = 6
        
    for xl in range (0,angle_num+1):
    
        angle = (pi/2)*xl/angle_num
        xcr = gs*math.cos(angle)
    
    
        r_new = math.sqrt(gs**2-xcr**2)
        num = int (2*pi*r_new)
        
    
        for i  in range (0,num,2):
            index +=1
    
            zcr = math.cos(2*pi/num*i)*r_new
            ycr = math.sin(2*pi/num*i)*r_new
            
            coor = [index,typ,typ,xcr+2*r+0.5,ycr, zcr]
            coor = np.array(coor)
            cap = np.append(cap,coor)
    
    
    r = -r
    gs = r
    angle_num = int(pi*gs/2)
    for xl in range (0,angle_num-1,-1):
    
        angle = (pi/2)*xl/angle_num
        xcr = gs*math.cos(angle)
    
    
        r_new = math.sqrt(gs**2-xcr**2)
        num = int (2*pi*r_new)
        
    
        for i  in range (0,-num,-2):
            index +=1
    
            zcr = math.cos(2*pi/num*i)*r_new
            ycr = math.sin(2*pi/num*i)*r_new
            
            coor = [index,typ,typ,xcr+2*r-0.5,ycr, zcr]
            coor = np.array(coor)
            cap = np.append(cap,coor)
    
    row = len(cap)/6
    nrow = int(row)
    cap = cap.reshape(nrow,ncol)
    return cap

