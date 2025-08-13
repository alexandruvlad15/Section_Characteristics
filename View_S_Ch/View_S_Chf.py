from Controller_S_Ch.Controller_S_Chf import CONTROLLER_SECTION_CH

class VIEW_SECTION_CH:

    def Read_Ch(self): # read
        nsh=int(input("Number of parts:")) # number of figures
        t=[] # type of shape
        y=[] # x coordinates
        z=[] # y coordinates
        op=[] # operation: add(A)/remove(R)
        s_or=[] # (T/B/L/R) the orientations of semicircles (we need them in order to determine the position of CG)
        R=0 # radius of the possible circle

        for i in range(nsh):
            tp=input("Type of shape (R,T,C,S):")
            t.append(tp)

            opr=input("Type of operation (A/R):")
            op.append(opr)


            if(tp=='R'): # rectangle
                # we need 2 points(left-top and right-bottom)
                y1=float(input("y1="))
                z1=float(input("z1="))
                y.append(y1)
                z.append(z1)
                y2=float(input("y2="))
                z2=float(input("z2="))
                y.append(y2)
                z.append(z2)

            if(tp=='T'): #triangle
                # we need 3 points (apex, base point 1, base point 2)
                y1=float(input("y1 (apex)="))
                z1=float(input("z1 (apex)="))
                y.append(y1)
                z.append(z1)
                y2=float(input("y2 (base point 1)="))
                z2=float(input("z2 (base point 1)="))
                y.append(y2)
                z.append(z2)
                y3=float(input("y3 (base point 2)="))
                z3=float(input("z3 (base point 2)="))
                y.append(y3)
                z.append(z3)

            if(tp=='C'): # circle
                # we need the center and radius
                y_c=float(input("y_c="))
                z_c=float(input("z_c="))
                y.append(y_c)
                z.append(z_c)
                R=float(input("R="))

            if(tp=='S'): # semicircle
                # we need the start and end point
                y_s=float(input("y_s="))
                z_s=float(input("z_s="))
                y.append(y_s)
                z.append(z_s)
                y_e=float(input("y_e="))
                z_e=float(input("z_e="))
                y.append(y_e)
                z.append(z_e)
                orientation=input("Semicircle orientation (T/B/L/R): ")
                s_or.append(orientation)

        return nsh,t,op,y,z,s_or,R
    
    def Write(self,nsh,ycg,zcg,iy,iz,izy,A,area):
        cont_sch=CONTROLLER_SECTION_CH()
        yCG,zCG,Iy,Iz,Izy,alpha,I1,I2=cont_sch.Solve(nsh,ycg,zcg,iy,iz,izy,A,area)
        print("Y position of CG= ",yCG)
        print("Z position of CG= ",zCG)
        print("Iy= ",Iy)
        print("Iz= ",Iz)
        print("Izy= ",Izy)
        print("alpha= ",alpha) # rad
        print("I1= ",I1)
        print("I2= ", I2)



            

