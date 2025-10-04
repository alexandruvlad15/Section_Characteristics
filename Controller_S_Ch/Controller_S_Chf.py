import math

class CONTROLLER_SECTION_CH:

    def Solve(self,nsh,yCG,zCG,Iy,Iz,Izy,A,area): # let's determine the CG of our section, Iy, Iz, Iyz, alpha, I1,2
        yA=0 # sum of y*A products
        zA=0 # sum of z*A products
        Iy_section=0
        Iz_section=0
        Izy_section=0
        for i in range(nsh):
            yA=yA+yCG[i]*A[i]
            zA=zA+zCG[i]*A[i]
        yCG_section=yA/area
        zCG_section=zA/area
        for i in range(nsh):
            Iy_section=Iy_section+Iy[i]+A[i]*(zCG[i]-zCG_section)**2
            Iz_section=Iz_section+Iz[i]+A[i]*(yCG[i]-yCG_section)**2
            Izy_section=Izy_section+Izy[i]+A[i]*(yCG[i]-yCG_section)*(zCG[i]-zCG_section)
        alpha=math.atan2(2*Izy_section,Iz_section-Iy_section)/2 # the main direction
        # main inertia momentums
        I1=(Iy_section+Iz_section)/2+0.5*math.sqrt((Iy_section-Iz_section)**2+4*Izy_section**2)
        I2=(Iy_section+Iz_section)/2-0.5*math.sqrt((Iy_section-Iz_section)**2+4*Izy_section**2)

        return yCG_section,zCG_section,Iy_section,Iz_section,Izy_section,alpha,I1,I2




