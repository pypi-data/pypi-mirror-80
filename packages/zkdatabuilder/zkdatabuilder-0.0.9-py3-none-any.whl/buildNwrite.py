def buildNwrite(um,filetoread,filetowrite):
    from membrane import membrane
    from freeTF import freetf 
    from angler import angler
    from bonder import bonder
    from radius import radius
    from boundTF import boundtf
    import numpy as np
    
    pos =  boundtf(filetoread)
    ps = len(pos)
    n = int(ps/23*20)
    r,sysVol = radius(n)
    
    ftf = freetf(um,ps,n)
    ft = len(ftf) 
    index = ft + ps
    
    mem = membrane(r,index,6)
    angles = angler(n,um)
    bonds = bonder(n,um)
    
    atoms1 = np.append(pos,ftf)
    atoms =np.append(atoms1,mem)
    
    boy = len(atoms)
    ncol = 6
    nrow = int(boy/ncol)
    
    atoms = atoms.reshape(nrow,ncol)
    
    
    ll = open(filetowrite,"w")
    
    ll.write("\n\n")
    
    num_atoms = str(nrow)
    ll.write(num_atoms+" atoms\n")
    ll.write("6 atom types\n")
    bnds = str(len(bonds))
    ll.write(bnds+" bonds\n")
    ll.write("2 bond types\n")
    angls = str(len(angles))
    ll.write(angls+" angles\n")
    ll.write("2 angle types\n\n")
    
    x = 5.2324242
    ll.write(str(-3*r-x)+" "+str(3*r+x)+" xlo xhi\n")
    ll.write(str(-r-x)+" "+str(r+x)+" ylo yhi\n")
    ll.write(str(-r-x)+" "+str(r+x)+" zlo zhi\n\n")
    
    ll.write("Masses\n\n")
    ll.write("1 1\n")   
    ll.write("2 1\n")
    ll.write("3 2\n")
    ll.write("4 2\n")
    ll.write("5 2\n")
    ll.write("6 1\n\n")
    
    ll.write("Pair Coeffs # lj/cut\n\n")
    
    ll.write("1 12 1\n")   
    ll.write("2 12 1\n")
    ll.write("3 12 1\n")
    ll.write("4 12 1\n")
    ll.write("5 12 1\n")
    ll.write("6 12 1\n\n")
    
    ll.write("Bond Coeffs # fene\n\n")
    
    ll.write("1 30 1.5 1 1\n")   
    ll.write("2 30 2.0 1.3 1.3\n\n")
    
    ll.write("Angle Coeffs # harmonic\n\n")
    
    ll.write("1 1 180.0\n")
    ll.write("2 12 40\n\n")
    
    ll.write("Atoms # angle\n\n")
    
    for row in atoms:
        for i in range (6):
            if i<3:
                ii = int(row[i])
                ll.write(str(ii)+" ")
            else:
                ll.write(str(row[i])+" ")
        ll.write("\n")
    
    ll.write("\nBonds\n\n")
    
    for row in bonds:
        for i in range (4):
                ii = int(row[i])
                ll.write(str(ii)+" ")
        ll.write("\n")
    
    ll.write("\nAngles\n\n")
    for row in angles:
        for i in range (5):
                ii = int(row[i])
                ll.write(str(ii)+" ")
        ll.write("\n")
    return
