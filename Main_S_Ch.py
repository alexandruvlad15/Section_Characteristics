from Model_S_Ch.Model_S_Chf import MODEL_SECTION_CH # relations/formulas
from View_S_Ch.View_S_Chf import VIEW_SECTION_CH # read/write
from Controller_S_Ch.Controller_S_Chf import CONTROLLER_SECTION_CH # final results

def main():
    view_sch=VIEW_SECTION_CH() 
    
    nsh=view_sch.ShowShapeForm() # get the number of figures
    t,op,y,z,s_or,R=view_sch.ShowShapeFrames(nsh) # get the data
    
    model_sch=MODEL_SECTION_CH() # formulas
    ycg,zcg,iy,iz,izy,A,area=model_sch.Coordinates(nsh,t,op,y,z,s_or,R) # characteristics for each figures
    
    cont_sch=CONTROLLER_SECTION_CH() # results
    yCG_section,zCG_section,Iy_section,Iz_section,Izy_section,alpha,I1,I2=cont_sch.Solve(nsh,ycg,zcg,iy,iz,izy,A,area) # characteristics for our section
    
    view_sch.Draw(nsh,t,op,y,z,s_or,R,yCG_section,zCG_section) # get a representation of the section
    view_sch.Write(nsh,yCG_section,zCG_section,Iy_section,Iz_section,Izy_section,alpha,I1,I2,A,area) # write the characteristics

if(__name__=="__main__"):
    main() # call main function
