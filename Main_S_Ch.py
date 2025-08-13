# we are going to use a general measure unit (the user is free to consider it mm, for example)
# small values (between -0.15 and 0.15) for iy, iz or izy are going to be considered practically 0

from Model_S_Ch.Model_S_Chf import MODEL_SECTION_CH
from View_S_Ch.View_S_Chf import VIEW_SECTION_CH

def main():
    view_sch=VIEW_SECTION_CH()
    nsh,t,op,y,z,sor,R=view_sch.Read_Ch()
    model_sch=MODEL_SECTION_CH()
    ycg,zcg,iy,iz,izy,A,area=model_sch.Coordinates(nsh,t,op,y,z,sor,R)
    view_sch.Write(nsh,ycg,zcg,iy,iz,izy,A,area)


if __name__=="__main__":
  main()