def freetf(um=1,index=0,n=2400):
    from random import random
    import numpy as np
    from radius import radius
    
    
    sap = 5
    typ = 3
    
    r,sysVol = radius(n)
    
    ttf = um
    avag = 6.022*(10**23) #avagdaro number mol
    m2l = 1000 #m^3 to liter
    m2u = 10**(-6) #meter to micrometer
    
    ftf = avag*m2l*m2u*sysVol*ttf #molarite to number
    
    ntf = int(ftf)
    
    kok2 = 2**(1/2)
    
    free = np.zeros([3*ntf,6])
    
    index = index+1
    for i in range (0,3*ntf,3):
        xcr = 4*r*random()-2*r
        ycr = 2*r*random()/kok2 -r/kok2
        zcr = 2*r*random()/kok2 -r/kok2
        
        free[i]=[index,typ,typ,xcr,ycr,zcr]
        free[i+1]=[index+1,sap,sap,xcr-0.66,ycr+0.56,zcr+0.61]
        free[i+2]=[index+2,typ,typ,xcr+0.33,ycr+0.67,zcr+0.48]
        index +=3
        
    return free

free = freetf(10)
