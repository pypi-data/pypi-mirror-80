def radius(n):

    import math
    
    pi = math.pi

    basepair = 4.6*10**6 #bp
    volume = 6.7*10**(-19) #m3
    bp_dens = basepair/volume #bp/m3
    realN = n*10 #my polymer bp
    sysVol = realN/bp_dens#bp/(bp/m3)
    sigma = 34*10**(-10) #1 sigma corresponds to 10 bp and 10bp length is 34 armstrong
    rreal = (3*sysVol/(16*pi))**(1/3) #2a^3 = m3, a = (m3/2)^(1/3)
    r = int(rreal/sigma+1)
    
    return r,sysVol