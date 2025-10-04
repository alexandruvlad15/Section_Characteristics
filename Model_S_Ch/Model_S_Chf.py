import math

class MODEL_SECTION_CH:

  def Coordinates(self,nsh,t,op,y,z,sor,R):
    y_CG=[] # y coordinate of CG
    z_CG=[] # z coordinate of CG
    A=[] # area vector
    Iy=[] # y axis inertia momentums vector
    Iz=[] # z axis inertia momentums vector
    Izy=[] # centrifugal momentums vector
    T_A=0 # total area
    cnt=0 # it tell us where we are situated in y and z vectors
    semi=0 # the variable which count the semicircles, in order to use their orientation
    for i in range(nsh):
      if(t[i]=='R'):
        # we know the 2 points, it is enough to know the center of the rectangle
        yCG=(y[cnt]+y[cnt+1])/2
        zCG=(z[cnt]+z[cnt+1])/2
        y_CG.append(yCG)
        z_CG.append(zCG)
        iy=abs(y[cnt+1]-y[cnt])*(abs(z[cnt+1]-z[cnt]))**3/12
        iz=abs(z[cnt+1]-z[cnt])*(abs(y[cnt+1]-y[cnt]))**3/12
        Ai=abs(y[cnt+1]-y[cnt])*abs(z[cnt+1]-z[cnt]) # area of a rectangle
        if(op[i]=='A'): # add this area
          A.append(Ai)
          Iy.append(iy)
          Iz.append(iz)
          Izy.append(0)
        if(op[i]=='R'): # remove this area
          Ai=-Ai
          iy=-iy
          iz=-iz
          A.append(Ai)
          Iy.append(iy)
          Iz.append(iz)
          Izy.append(0)

        cnt=cnt+2 # rectangle->2 points

      if(t[i]=='T'):
        # we have all the 3 points of the triangle
        yCG=(y[cnt]+y[cnt+1]+y[cnt+2])/3
        zCG=(z[cnt]+z[cnt+1]+z[cnt+2])/3
        y_CG.append(yCG)
        z_CG.append(zCG)
        if(z[cnt+1]==z[cnt+2]): # horizontal base
          b=abs(y[cnt+2]-y[cnt+1]) # base
          h=abs(z[cnt]-z[cnt+1]) # height
        
        if(y[cnt+1]==y[cnt+2]): # vertical base
          b=abs(z[cnt+2]-z[cnt+1])
          h=abs(y[cnt]-y[cnt+1]) 
        
        Ai=b*h/2
        iy=b*h**3/36
        iz=h*b**3/36
        izy=-b**2*h**2/72
        if(op[i]=='A'):
          A.append(Ai)
          Iy.append(iy)
          Iz.append(iz)
          Izy.append(izy)
        if(op[i]=='R'):
          Ai=-Ai
          iy=-iy
          iz=-iz
          izy=-izy
          A.append(Ai)
          Iy.append(iy)
          Iz.append(iz)
          Izy.append(izy)
        cnt=cnt+3 # triangle->3 points

      if(t[i]=='C'):
        # center coordinates and radius
        y_CG.append(y[cnt])
        z_CG.append(z[cnt])
        iy=math.pi*(2*R)**4/64
        iz=math.pi*(2*R)**4/64
        Ai=math.pi*R**2
        if(op[i]=='R'):
          Ai=-Ai
          iy=-iy
          iz=-iz
        A.append(Ai)
        Iy.append(iy)
        Iz.append(iz)
        Izy.append(0)
        cnt=cnt+1 # only 1 point

      if(t[i]=='S'):
        if(sor[semi]=='T'): # top semicircle
          r=abs((y[cnt]+y[cnt+1])/2-y[cnt]) # radius
          yCG=(y[cnt]+y[cnt+1])/2
          zCG=z[cnt]+4*r/(3*math.pi)
          y_CG.append(yCG)
          z_CG.append(zCG)
          Ai=math.pi*r**2/2
          iy=0.00686*(2*r)**4
          iz=math.pi*(2*r)**4/128

        if(sor[semi]=='B'): # bottom semicircle
          r=abs((y[cnt]+y[cnt+1])/2-y[cnt])
          yCG=(y[cnt]+y[cnt+1])/2
          zCG=z[cnt]-4*r/(3*math.pi)
          y_CG.append(yCG)
          z_CG.append(zCG)
          Ai=math.pi*r**2/2
          iy=0.00686*(2*r)**4
          iz=math.pi*(2*r)**4/128

        if(sor[semi]=='R'): # right semicircle
          r=abs((z[cnt]+z[cnt+1])/2-z[cnt])
          yCG=y[cnt]+4*r/(3*math.pi)
          zCG=(z[cnt]+z[cnt+1])/2
          y_CG.append(yCG)
          z_CG.append(zCG)
          Ai=math.pi*r**2/2
          iy=0.00686*(2*r)**4
          iz=math.pi*(2*r)**4/128

        if(sor[semi]=='L'): # left semicircle
          r=abs((z[cnt]+z[cnt+1])/2-z[cnt])
          yCG=y[cnt]+4*r/(3*math.pi)
          zCG=(z[cnt]+z[cnt+1])/2
          y_CG.append(yCG)
          z_CG.append(zCG)
          Ai=math.pi*r**2/2
          iy=0.00686*(2*r)**4
          iz=math.pi*(2*r)**4/128
          
        if(op[i]=='R'):
           Ai=-Ai
           iy=-iy
           iz=-iz
        Iy.append(iy)
        Iz.append(iz)
        Izy.append(0)
        A.append(Ai)
        
        cnt=cnt+2
        semi=semi+1

    for i in range(nsh):
      T_A=T_A+A[i]

    return y_CG,z_CG,Iy,Iz,Izy,A,T_A

      
      
