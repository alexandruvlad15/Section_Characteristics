from Controller_S_Ch.Controller_S_Chf import CONTROLLER_SECTION_CH
import matplotlib.pyplot as plt # drawings
from matplotlib.patches import Polygon as MplPolygon,Circle,Wedge # types of figures
from shapely.geometry import Polygon as ShapelyPolygon,Point # geometrical objects
from shapely.ops import unary_union # mix of figures
import numpy as np # lists
import tkinter as tk # GUI
from tkinter import messagebox,ttk # GUI objects
from PIL import Image,ImageTk # images
import os # link with files

class VIEW_SECTION_CH:

    def ShowShapeForm(self): # main window
        root=tk.Tk() # create the window
        root.title("START") # title of window
        width,height=600,400 # dimensions of window
        screen_width,screen_height=root.winfo_screenwidth(),root.winfo_screenheight() # dimensions of screen
        x,y=(screen_width-width)//2,(screen_height-height)//2 # center of screen
        root.geometry(f"{width}x{height}+{x}+{y}") # position of window
        root.resizable(False,False) # window is not resizable

        image_path=os.path.join(os.path.dirname(os.path.dirname(__file__)),"Images","Start_background.jpg") # path to image for main background
        canvas=tk.Canvas(root,width=width,height=height)
        canvas.pack(fill="both",expand=True) # complete filling
        if(os.path.exists(image_path)): # if the image exists
            pil_image=Image.open(image_path).resize((width,height),Image.LANCZOS) # open image file
            self.bg_image=ImageTk.PhotoImage(pil_image) # convert the image and keep it safe from deletion
            canvas.create_image(0,0,image=self.bg_image,anchor="nw") # show the background

        self.nsh=None # define number of figures

        def submit(): # submit function
            try: # if the input is ok
                self.nsh=int(entry.get()) # nsh gets the value
                root.destroy() # unshow the window
            except ValueError: # if not
                messagebox.showerror("Error","Please enter a valid number!") # show the message

        lbl=tk.Label(root,text="Number of figures:",font=("Calibri",16,"bold","italic")) # orientation text field attributes
        entry=tk.Entry(root,font=("Calibri",16,"bold"),fg="blue") # input field attributes
        btn=tk.Button(root,text="START",command=submit,font=("Calibri",20,"bold"),bg="green",fg="white") # submit button attributes

        canvas.create_window(width//3,height//2-20,window=lbl) # create the orientation field 
        canvas.create_window(width//2+100,height//2-20,window=entry) # create the input field
        canvas.create_window(width//2,height//2+40,window=btn) # create submit button

        root.mainloop() # start the loop
        return self.nsh # keep in mind number of figures

    def ShowShapeFrames(self,nsh): # window where the user build his section
        self.t,self.op,self.y,self.z,self.s_or=[],[],[],[],[] # type, operation, y, z, semicircle orientation
        self.R,self.completed=0,0 # radius of circle and the validation of number of figures
        self.images=[] # we need it in order to keep previous images

        root=tk.Tk() # create the window
        root.title("Enter figure") # name of window
        root.geometry("1450x800") # dimension
        canvas=tk.Canvas(root, width=1450,height=800) # create the main window for the 4 cases
        canvas.pack(fill="both",expand=True) # complete filling

        # background
        image_path=os.path.join(os.path.dirname(os.path.dirname(__file__)),"Images","Geometry.jpg")
        if(os.path.exists(image_path)):
            pil_image=Image.open(image_path).resize((1450,800),Image.LANCZOS)
            self.bg_image_frames=ImageTk.PhotoImage(pil_image)
            canvas.create_image(0,0,image=self.bg_image_frames,anchor="nw")

        frames={} # figures list
        types=["R","T","C","S"] # types list
        names={"R":"Rectangle (R) 1:left-top 2:right-bottom","T":"Triangle (T) 1:apex 2:left-base 3:right-left","C":"Circle (C) c:center R:radius","S":"Semicircle (S) s:start-base e:end-base"} # notations dictionary

        for i, tp in enumerate(types): # index and type for every figure
            frame=tk.LabelFrame(canvas,text=names[tp],padx=10,pady=10,bg="dodgerblue",fg="white") # create the frame for the shape
            canvas.create_window(180+i*330,380,window=frame,width=320,height=420) # position
            frames[tp]=frame # collect the current frame

        def submit_frame(tp,entries,orient_entry=None):
            try:
                op_val="A" if entries["op"].get()=="Add" else "R" # operation selected Add/Remove
                if(tp=="R"): # rectangle
                    # coordinates
                    y_vals=[float(entries["y1"].get()),float(entries["y2"].get())]
                    z_vals=[float(entries["z1"].get()),float(entries["z2"].get())]
                    # keep in mind the values
                    self.t.append("R")
                    self.op.append(op_val)
                    self.y.extend(y_vals) 
                    self.z.extend(z_vals)
                elif(tp=="T"): # triangle
                    y_vals=[float(entries["y1"].get()),float(entries["y2"].get()),float(entries["y3"].get())]
                    z_vals=[float(entries["z1"].get()),float(entries["z2"].get()),float(entries["z3"].get())]
                    self.t.append("T")
                    self.op.append(op_val)
                    self.y.extend(y_vals)
                    self.z.extend(z_vals)
                elif(tp=="C"): # circle
                    y_c,z_c=float(entries["yc"].get()),float(entries["zc"].get())
                    self.t.append("C")
                    self.op.append(op_val)
                    self.y.append(y_c)
                    self.z.append(z_c)
                    self.R=float(entries["R"].get())
                elif(tp=="S"): # semicircle
                    y_vals=[float(entries["ys"].get()),float(entries["ye"].get())]
                    z_vals=[float(entries["zs"].get()),float(entries["ze"].get())]
                    self.t.append("S")
                    self.op.append(op_val)
                    self.y.extend(y_vals)
                    self.z.extend(z_vals)
                    map_orient={"Top":"T","Bottom":"B","Left":"L","Right":"R"} # orientation dictionary
                    orientation=map_orient[orient_entry.get()] # get the semicircle orientation
                    self.s_or.append(orientation) # add the semicircle orientation in list

                messagebox.showinfo("Saved", f"Data for {tp} saved!") # safety message
                self.completed+=1 # one more complet iteration
                if self.completed>=nsh:
                    root.destroy() # we can close the window if all the data was read
            except Exception as e:
                messagebox.showerror("Error", f"Please fill all fields correctly.\n{e}") # if not, show the message

        for tp,frame in frames.items():
            entries={} # entries list
            tk.Label(frame,text="Operation (Add/Remove):",bg="dodgerblue",fg="white").pack() # operation selection field
            entries["op"]=ttk.Combobox(frame,values=["Add","Remove"]) # combobox for Add/Remove
            entries["op"].pack(pady=(4,6)) # save the choice

            fields_frame=tk.Frame(frame,bg="lavender") # data fields (left)
            fields_frame.pack(side="left",fill="both",expand=True,padx=5,pady=5) # data fields parameters

            img_frame=tk.Frame(frame,bg="dodgerblue") # image (right)
            img_frame.pack(side="right",fill="y",padx=5) # image field parameters

            if(tp=="R"):
                for f in ["y1","z1","y2","z2"]: # input fields
                    tk.Label(fields_frame,text=f,bg="lavender",fg="black").pack() # label
                    e=tk.Entry(fields_frame,font=("Calibri",12,"bold"),fg="blue") # input field
                    e.pack() # import data
                    entries[f]=e # keep data
                img_file="Rectangle.png" # import image
            elif(tp=="T"):
                for f in ["y1","z1","y2","z2","y3","z3"]:
                    tk.Label(fields_frame,text=f,bg="lavender",fg="black").pack()
                    e=tk.Entry(fields_frame,font=("Calibri",12,"bold"),fg="blue")
                    e.pack()
                    entries[f]=e
                img_file="Triangle.png"
            elif(tp=="C"):
                for f in ["yc","zc","R"]:
                    tk.Label(fields_frame,text=f,bg="lavender",fg="black").pack()
                    e=tk.Entry(fields_frame, font=("Calibri",12,"bold"),fg="blue")
                    e.pack()
                    entries[f]=e
                img_file="Circle.png"
            elif(tp=="S"):
                for f in ["ys","zs","ye","ze"]:
                    tk.Label(fields_frame,text=f,bg="lavender",fg="black").pack()
                    e=tk.Entry(fields_frame,font=("Calibri",12,"bold"),fg="blue")
                    e.pack()
                    entries[f]=e
                tk.Label(fields_frame, text="Orientation",bg="lavender",fg="black").pack(pady=(4,2))
                orient_entry=ttk.Combobox(fields_frame,values=["Top","Bottom","Left","Right"]) # combobox for semicircle orientation
                orient_entry.pack(pady=(2,6))
                img_file="Semicircle.png"

            img_path=os.path.join(os.path.dirname(os.path.dirname(__file__)),"Images",img_file)
            if os.path.exists(img_path):
                pil_img=Image.open(img_path).resize((140, 140),Image.LANCZOS)
                img=ImageTk.PhotoImage(pil_img)
                self.images.append(img)
                img_label=tk.Label(img_frame,image=img,bg="dodgerblue")
                img_label.pack()
         # submit button
            if(tp=="S"):
                tk.Button(fields_frame,text="Submit",font=("Calibri",14,"bold"),bg="purple",fg="white",command=lambda tp=tp,e=entries,o=orient_entry:submit_frame(tp,e,o)).pack(pady=8)
            else:
                tk.Button(fields_frame,text="Submit",font=("Calibri",14,"bold"),bg="purple",fg="white",command=lambda tp=tp,e=entries:submit_frame(tp,e)).pack(pady=8)

        root.mainloop()
        return self.t,self.op,self.y,self.z,self.s_or,self.R

    def Read_Ch(self,nsh): # read function
        cnt,semi=0,0 # number of coordinates and orientations
        t,op,y,z,s_or=[],[],[],[],[] # type,operation, y,z coordinates, semicircle orientation
        R=self.R # radius of circle
        section_shapes=[]

        for i in range(nsh):
            tp,opr=self.t[i],self.op[i]
            t.append(tp)
            new_shape=None # define a new input

            if(tp=='R'):
                # go through coordinates
                y1,y2=self.y[cnt],self.y[cnt+1]
                z1,z2=self.z[cnt],self.z[cnt+1]
                # add data in coordinates lists
                y+=[y1,y2]
                z+=[z1,z2]
                cnt+=2 # we have 2 points
                new_shape=ShapelyPolygon([(y1,z1),(y2,z1),(y2,z2),(y1,z2)]) # rectangle figure
            elif(tp=='T'):
                y1,y2,y3=self.y[cnt],self.y[cnt+1],self.y[cnt+2]
                z1,z2,z3=self.z[cnt],self.z[cnt+1],self.z[cnt+2]
                y+=[y1,y2,y3]
                z+=[z1,z2,z3]
                cnt+=3 # 3 points
                new_shape=ShapelyPolygon([(y1,z1),(y2,z2),(y3,z3)]) # triangle figure
            elif(tp=='C'): 
                y_c,z_c=self.y[cnt],self.z[cnt]
                cnt+=1 # 1 point
                y.append(y_c); 
                z.append(z_c)
                new_shape=Point(y_c,z_c).buffer(R) # circle figure
            elif(tp=='S'):
                y_s,y_e=self.y[cnt],self.y[cnt+1]
                z_s,z_e=self.z[cnt],self.z[cnt+1]
                orientation=self.s_or[semi]
                cnt+=2
                semi+=1
                y+=[y_s,y_e]
                z+=[z_s,z_e]
                s_or.append(orientation)
                r=((y_e-y_s)**2+(z_e-z_s)**2)**0.5/2
                cy,cz=(y_s+y_e)/2,(z_s + z_e)/2
                # generate points in the specific area
                if(orientation=="T"):
                    angle=np.linspace(0,np.pi,75)
                elif(orientation=="B"):
                    angle=np.linspace(np.pi,2*np.pi,75)
                elif(orientation=="L"):
                    angle=np.linspace(np.pi/2,3*np.pi/2,75)
                elif(orientation=="R"): 
                    angle=np.linspace(-np.pi/2,np.pi/2,75)
                pts=[(cy+r*np.cos(a),cz+r*np.sin(a)) for a in angle]
                new_shape=ShapelyPolygon(pts)

            # check intersections
            for existing in section_shapes:
                if(opr=='A' and new_shape.intersection(existing).area>0 and not new_shape.touches(existing)):
                    print("There are intersections!!")
            section_shapes.append(new_shape)

        # check gaps
        union_section=unary_union(section_shapes) # combine the figures to obtain the section
        hull=union_section.convex_hull # hull
        gap_area=hull.difference(union_section).area # total gaps
        if(gap_area>0.5): # verify tolerance
            print("There are gaps!!")

        return nsh,t,op,y,z,s_or,R

    def Write(self,nsh,yCG,zCG,Iy,Iz,Izy,alpha,I1,I2,A,area): # write the results
     root=tk.Tk()
     root.title("Results")
     width,height=1200,600
     screen_width,screen_height=root.winfo_screenwidth(),root.winfo_screenheight()
     x,y=(screen_width - width)//2,(screen_height-height)//2
     root.geometry(f"{width}x{height}+{x}+{y}")
     root.resizable(False,False)

     canvas=tk.Canvas(root,width=width,height=height)
     canvas.pack(fill="both",expand=True)
     image_path=os.path.join(os.path.dirname(os.path.dirname(__file__)),"Images","Results.jpg")
     if(os.path.exists(image_path)):
        pil_image=Image.open(image_path).resize((width,height),Image.LANCZOS)
        self.bg_results=ImageTk.PhotoImage(pil_image)
        canvas.create_image(0,0,image=self.bg_results,anchor="nw")

     results={"Y CG":yCG,"Z CG":zCG,"Iy":Iy,"Iz":Iz,"Izy":Izy,"alpha(deg)":alpha,"I1":I1,"I2":I2}

     frame=tk.Frame(canvas,bg="lavender",bd=3,relief="ridge")
     canvas.create_window(width//2,height//2,window=frame)

     for key,value in results.items(): # key-name, value-numerical value
        row=tk.Frame(frame,bg="lavender")
        row.pack(fill="x",padx=10,pady=5)
        tk.Label(row,text=f"{key} =",font=("Calibri",14,"bold"),bg="lavender").pack(side="left") # show in format key=
        val=tk.Entry(row,font=("Calibri",14,"bold"),fg="blue",width=40) # parameters for numerical values fields
        if(isinstance(value,(list, tuple))): # list
            val_str=",".join(f"{v:.3f}" for v in value) # every number has 3 decimals and they have the fornamt val1,val2 etc
        else: # numerical
            val_str=f"{value:.3f}" # directly
        val.insert(0,val_str) # put the value in the field
        val.config(state="readonly") # read only
        val.pack(side="left",padx=10) # position

     tk.Button(frame,text="Close",font=("Calibri",14,"bold"),bg="darkred",fg="white",command=root.destroy).pack(pady=10) # close button

     root.mainloop()



    def Draw(self,nsh,t,op,y,z,s_or,R,yCG_section=None,zCG_section=None): # build the section
        fig,ax=plt.subplots() # figure and axis system
        cnt,semi=0,0 # initial values

        for i in range(nsh):
            if(t[i]=='R'):
                rect_y=[y[cnt],y[cnt+1],y[cnt+1],y[cnt]]
                rect_z=[z[cnt],z[cnt],z[cnt+1],z[cnt+1]]
                col,alp=("skyblue",0.5) if op[i]=='A' else ("white",1) # draw respecting the operation 
                polygon=MplPolygon(list(zip(rect_y,rect_z)),fill=True,color=col,alpha=alp) # create the figure
                ax.add_patch(polygon) # add the figure
                cnt+=2
            elif(t[i]=='T'):
                col, alp=("skyblue",0.5) if op[i]=='A' else ("white",1)
                polygon=MplPolygon([(y[cnt],z[cnt]),(y[cnt+1],z[cnt+1]),(y[cnt+2],z[cnt+2])],fill=True,color=col,alpha=alp)
                ax.add_patch(polygon)
                cnt+=3
            elif(t[i]=='C'):
                col,alp=("skyblue",0.5) if op[i]=='A' else ("white",1)
                circle=Circle((y[cnt],z[cnt]),R,fill=True,color=col,alpha=alp)
                ax.add_patch(circle)
                cnt+=1
            elif(t[i]=='S'):
                y_s,z_s,y_e,z_e=y[cnt],z[cnt],y[cnt+1],z[cnt+1]
                orientation=s_or[semi]
                r=((y_e-y_s)**2+(z_e-z_s)**2)**0.5/2
                cy,cz=(y_s+y_e)/2,(z_s+z_e)/2
                if(orientation=="T"): # top
                    start,end=0,180
                elif(orientation=="B"): # bottom
                    start,end=180,360
                elif(orientation=="L"): # left
                    start,end=90,270
                elif(orientation=="R"): # right
                    start,end=-90,90
                col,alp=("skyblue",0.5) if op[i]=='A' else ("white",1)
                wedge=Wedge((cy, cz),r,start,end,color=col,alpha=alp)
                ax.add_patch(wedge)
                cnt+=2
                semi+=1

        if(yCG_section is not None and zCG_section is not None):
            ax.plot(yCG_section, zCG_section,'ro') # show the CG

        ax.set_aspect('equal') # equal proportions
        # axis labels
        plt.xlabel("Y")
        plt.ylabel("Z")
        plt.title("Section") # title
        plt.show() # show the section

