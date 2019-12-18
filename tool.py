# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 10:32:59 2019

@author: kai
"""

from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox
import pydicom
import numpy
import math
import pickle
import pandas as pd 
import numpy as np 
import random


# GUI buttons
window = Tk()
window.title("MLC QA")
lbl = Label(window, text="IMRT")
lbl.grid(column=2, row=1) 
lbl1 = Label(window, text="VMAT")
lbl1.grid(column=2, row=3) 
lbl2 = Label(window, text="DICOM File")
lbl2.grid(columnspan=4, row=0)








def clicked():
    global file
    file = filedialog.askopenfilename()
    
    lbl2.configure(text=file)
    """
    global li
    li=[]
    
    ds = pydicom.dcmread(file) 
    
    global num_beam
    num_beam=ds[0x300a,0x70][0][0x300a,0x80].value    
    
    for field_number in range (num_beam): 
        type = ds[0x300a,0xb0][field_number][0x300a,0xce].value
        treatment = "TREATMENT" in type
        if treatment is False:
            dataset=[]  
            df = pd.DataFrame(dataset,columns =['Index','MLC_position','MLC_velocity','MLC_acceleration','Control_point',
                                                 'Dose_rate', 'Gravity_vector', 'Gantry_velocity', 'Gantry_acceleration'])
            li.append(df)
        else:
            # Number of Contorl Point
            cp=ds[0x300a,0xb0][field_number][0x300a,0x110].value                
            # Prescription Monitor Unit
            mu=ds[0x300a,0x70][0][0x300c,0x04][field_number][0x300a,0x86].value
            # Dose Rate Set
            dr=ds[0x300a,0xb0][field_number][0x300a,0x111][0][0x300a,0x115].value
            # MU/min => MU/sec
            dr_s=dr/60                 
            # Gantry Angle
            gantry_angle_actualdegree=[]
            gantry_angle_degree=[]
            gantry_angle_rad=[]
            for i in range(cp): 
                ga=ds[0x300a,0xb0][field_number][0x300a,0x111][i][0x300a,0x11e].value  
                gantryangle=ga/180*math.pi
                gantry_angle_actualdegree.append(ga)
                if ga<180:
                    ga=180-ga
                elif ga>180:
                    ga=540-ga        
                gantry_angle_degree.append(ga)
                gantry_angle_rad.append(gantryangle)
            # Collimator Angle
            ca=ds[0x300a,0xb0][field_number][0x300a,0x111][0][0x300a,0x120].value 
            collimatorangle=ca/180*math.pi  
            # Cumulative Meterset Weight
            meterset_weight=[]
            for i in range(cp):
                weight=ds[0x300a,0xb0][field_number][0x300a,0x111][i][0x300a,0x134].value
                meterset_weight.append(weight)
            # Monitor Unit at CP
            meterset_mu=[]
            meterset_cumulative_mu=[]
            for j in range(1,cp):   
                weight_diff=meterset_weight[j]-meterset_weight[j-1]
                weight_mu=mu*weight_diff
                weight_cumulative_mu=mu*meterset_weight[j]
                meterset_mu.append(weight_mu)
                meterset_cumulative_mu.append(weight_cumulative_mu)
            # Time Interval at CP
            gantry_speed=4.8
            meterset_time=[]
            for k in range(cp-1): 
                max_mu_cp=abs(gantry_angle_degree[k+1]-gantry_angle_degree[k])*dr_s/gantry_speed
                if meterset_mu[k]<max_mu_cp:
                    weight_time=abs(gantry_angle_degree[k+1]-gantry_angle_degree[k])/gantry_speed
                elif meterset_mu[k]>max_mu_cp:
                    weight_time=meterset_mu[k]/dr_s
                meterset_time.append(weight_time)
            # MLC Position at CP
            mlc=[]
            weight_mlc=ds[0x300a,0xb0][field_number][0x300a,0x111][0][0x300a,0x11a][2][0x300a,0x11c].value
            mlc.append(weight_mlc)
            for j in range(1,cp):
                weight_mlc=ds[0x300a,0xb0][field_number][0x300a,0x111][j][0x300a,0x11a][0][0x300a,0x11c].value
                mlc.append(weight_mlc)
            mlc_position=[["MLC_position"]]
            for i in range(cp):
                mlc_cp=(mlc[i][:])
                mlc_position.append(mlc_cp)
            # MLC Velocity at CP
            mlc_velocity=[["MLC_velocity"],[0]*120] 
            for j in range(1,cp):
                mlc_velocity_cp=[]
                for m in range(120):
                    diff=(mlc_position[j+1][m]-mlc_position[j][m])
                    velocity=diff/meterset_time[j-1]    
                    mlc_velocity_cp.append(velocity)
                mlc_velocity.append(mlc_velocity_cp)            
            # MLC Acceleration at CP
            mlc_acceleration=[["MLC_acceleration"],[0]*120] 
            for j in range(1,cp):
                mlc_acceleration_cp=[]
                for m in range(120):
                    diff=(mlc_velocity[j+1][m]-mlc_velocity[j][m])
                    acceleration=diff/meterset_time[j-1]    
                    mlc_acceleration_cp.append(acceleration)
                mlc_acceleration.append(mlc_acceleration_cp) 
            # Control Point
            control_point=[["Control_point"]] 
            for i in range(cp):
                control_point_cp=[]
                for m in range(120):
                    controlpointcp=i/cp
                    control_point_cp.append(controlpointcp)
                control_point.append(control_point_cp) 
            # Dose Rate
            dose_rate=[["Dose_rate"],[0]*120] 
            for j in range(1,cp):
                dose_rate_cp=[]
                for m in range(120):
                    doseratecp=1
                    dose_rate_cp.append(doseratecp)
                dose_rate.append(dose_rate_cp)   
            # Gravity Vector
            gravity_vector=[["Gravity_vector"]] 
            for i in range(cp):
                gravity_vector_cp=[]
                for m in range(120):
                    gravityvector=math.sin(gantry_angle_rad[i])*math.cos(collimatorangle)
                    gravity_vector_cp.append(gravityvector)
                gravity_vector.append(gravity_vector_cp)
            # Gantry Velocity at CP
            gantry_velocity=[["Gantry_velocity"],[0]*120] 
            for k in range(cp-1):
                gantry_velocity_cp=[]
                for m in range(120):
                    diff=(gantry_angle_degree[k+1]-gantry_angle_degree[k])
                    velocity=diff/meterset_time[k]    
                    gantry_velocity_cp.append(velocity)
                gantry_velocity.append(gantry_velocity_cp)    
            # Gantry Acceleration at CP
            gantry_acceleration=[["Gantry_acceleration"],[0]*120] 
            for j in range(1,cp):
                gantry_acceleration_cp=[]
                for m in range(120):
                    diff=(gantry_velocity[j+1][m]-gantry_velocity[j][m])
                    acceleration=diff/meterset_time[j-1]    
                    gantry_acceleration_cp.append(acceleration)
                gantry_acceleration.append(gantry_acceleration_cp)         
            # Index
            index=[["Index"]] 
            for i in range(cp):
                index_cp=[]
                for m in range(120):
                    indexcp=str(i)+"_"+str(m)
                    index_cp.append(indexcp)
                index.append(index_cp)
            
            dataset=[]
            index_1 = [x for xs in index for x in xs]
            mlc_position_1 = [x for xs in mlc_position for x in xs]
            mlc_velocity_1 = [x for xs in mlc_velocity for x in xs]
            mlc_acceleration_1 = [x for xs in mlc_acceleration for x in xs]
            control_point_1 = [x for xs in control_point for x in xs]
            dose_rate_1 = [x for xs in dose_rate for x in xs]
            gravity_vector_1 = [x for xs in gravity_vector for x in xs]
            gantry_velocity_1 = [x for xs in gantry_velocity for x in xs]
            gantry_acceleration_1 = [x for xs in gantry_acceleration for x in xs]
            dataset.append(index_1)
            dataset.append(mlc_position_1)
            dataset.append(mlc_velocity_1)
            dataset.append(mlc_acceleration_1)
            dataset.append(control_point_1)
            dataset.append(dose_rate_1)
            dataset.append(gravity_vector_1)
            dataset.append(gantry_velocity_1)
            dataset.append(gantry_acceleration_1)
            matrix_t =list(map(list, zip(*dataset)))
            del matrix_t[0]
            df = pd.DataFrame(matrix_t,columns =['Index','MLC_position','MLC_velocity','MLC_acceleration','Control_point',
                                                 'Dose_rate', 'Gravity_vector', 'Gantry_velocity', 'Gantry_acceleration'])
            li.append(df)
            
            field_num = str(field_number) 
            numpy.savetxt("RTDICOM_VMAT_"+field_num+".csv", matrix_t, delimiter=",",fmt='%s')
     """
btn = Button(window, text="Open", command=clicked)
btn.grid(column=4, row=0)
    


 
def clicked1():
    global clf
    global filename
    filename = 'IMRT_linearVonly.sav'
    clf = pickle.load(open(filename, 'rb'))
    
def clicked2():
    global clf
    global filename
    filename = 'IMRT_linear.sav'
    clf = pickle.load(open(filename, 'rb'))
    
def clicked3():
    global clf
    global filename
    filename = 'IMRT_tree.sav'
    clf = pickle.load(open(filename, 'rb'))
    
def clicked4():
    global clf
    global filename
    filename = 'IMRT_boosted.sav'
    clf = pickle.load(open(filename, 'rb'))
    
def clicked5():
    global clf
    global filename
    filename = 'IMRT_bagged.sav'
    clf = pickle.load(open(filename, 'rb'))

def clicked6():
    global clf
    global filename
    filename = 'VMAT_linearVonly.sav'
    clf = pickle.load(open(filename, 'rb'))
    
def clicked7():
    global clf
    global filename
    filename = 'VMAT_linear.sav'
    clf = pickle.load(open(filename, 'rb'))
    
def clicked8():
    global clf
    global filename
    filename = 'VMAT_tree.sav'
    clf = pickle.load(open(filename, 'rb'))
    
def clicked9():
    global clf
    global filename
    filename = 'VMAT_boosted.sav'
    clf = pickle.load(open(filename, 'rb'))
    
def clicked10():
    global clf
    global filename
    filename = 'VMAT_bagged.sav'
    clf = pickle.load(open(filename, 'rb'))

v = IntVar()
rad1 = Radiobutton(window,text='LinearVonly', variable = v, value=1, command=clicked1)
rad1.grid(column=0, row=2)
rad2 = Radiobutton(window,text='Linear', variable = v, value=2, command=clicked2)
rad2.grid(column=1, row=2)
rad3 = Radiobutton(window,text='Decision Tree', variable = v, value=3, command=clicked3)
rad3.grid(column=2, row=2) 
rad4 = Radiobutton(window,text='Bossted Tree', variable = v, value=4, command=clicked4)
rad4.grid(column=3, row=2)
rad5 = Radiobutton(window,text='Bagged Tree', variable = v, value=5, command=clicked5)
rad5.grid(column=4, row=2)  
rad6 = Radiobutton(window,text='LinearVonly', variable = v, value=6, command=clicked6)
rad6.grid(column=0, row=4)
rad7 = Radiobutton(window,text='Linear', variable = v, value=7, command=clicked7)
rad7.grid(column=1, row=4)
rad8 = Radiobutton(window,text='Decision Tree', variable = v, value=8, command=clicked8)
rad8.grid(column=2, row=4) 
rad9 = Radiobutton(window,text='Bossted Tree', variable = v, value=9, command=clicked9)
rad9.grid(column=3, row=4)
rad10 = Radiobutton(window,text='Bagged Tree', variable = v, value=10, command=clicked10)
rad10.grid(column=4, row=4)  



chk_state = BooleanVar()
chk_state.set(False) #set check state
chk = Checkbutton(window, text='Random Error', var=chk_state)
chk.grid(column=1, row=5)



combo = Combobox(window)
combo['values']= (10, 20, 30, 4, 5)
combo.grid(column=3, row=5)
a = combo.get()




def clicked11(): 
    
    #path = r'C:\Users\kc353.DHE\Box Sync\Research- Kai\test dicom file\tool'
    #all_files = glob.glob(path + "/*.csv")
    #li = []

    #for filename in all_files:
     #   df = pd.read_csv(filename,  sep=',', dtype='a',error_bad_lines=False)
     #  li.append(df)


    #Extract Mechanical Parameters from DICOM    
    global li
    li=[]
    ds = pydicom.dcmread(file) 
    global num_beam
    num_beam=ds[0x300a,0x70][0][0x300a,0x80].value    
    global mlc_position
    
    model1 = "IMRT_linearVonly.sav" in filename
    model2 = "IMRT_linear.sav" in filename
    model3 = "IMRT_tree.sav" in filename
    model4 = "IMRT_boosted.sav" in filename
    model5 = "IMRT_bagged.sav" in filename
    
    
    if model1 or model2 or model3 or model4 or model5 is True: 
        for field_number in range (num_beam): 
            type = ds[0x300a,0xb0][field_number][0x300a,0xce].value
            treatment = "TREATMENT" in type
            if treatment is False:
                dataset=[]  
                df = pd.DataFrame(dataset,columns =['Index','MLC_position','MLC_velocity','MLC_acceleration','Control_point',
                                                     'Dose_rate', 'Gravity_vector'])
                li.append(df)
            else:
                # Number of Contorl Point
                cp=ds[0x300a,0xb0][field_number][0x300a,0x110].value
                # Prescription Monitor Unit
                mu=ds[0x300a,0x70][0][0x300c,0x04][field_number][0x300a,0x86].value
                # Dose Rate Set
                dr=ds[0x300a,0xb0][field_number][0x300a,0x111][0][0x300a,0x115].value
                # MU/min => MU/sec
                dr_s=dr/60 
                # Gantry Angle
                ga=ds[0x300a,0xb0][field_number][0x300a,0x111][0][0x300a,0x11e].value  
                gantryangle=ga/180*math.pi
                # Collimator Angle
                ca=ds[0x300a,0xb0][field_number][0x300a,0x111][0][0x300a,0x120].value 
                collimatorangle=ca/180*math.pi
                # Cumulative Meterset Weight
                meterset_weight=[]
                for i in range(cp):
                    weight=ds[0x300a,0xb0][field_number][0x300a,0x111][i][0x300a,0x134].value
                    meterset_weight.append(weight)    
                # Monitor Unit at CP
                meterset_mu=[]
                meterset_cumulative_mu=[]
                for j in range(1,cp):   
                    weight_diff=meterset_weight[j]-meterset_weight[j-1]
                    weight_mu=mu*weight_diff
                    weight_cumulative_mu=mu*meterset_weight[j]
                    meterset_mu.append(weight_mu)
                    meterset_cumulative_mu.append(weight_cumulative_mu)
                # Time Interval at CP
                meterset_time=[]
                for k in range(cp-1):   
                    weight_time=meterset_mu[k]/dr_s
                    meterset_time.append(weight_time)      
                # MLC Position at CP
                mlc=[]
                weight_mlc=ds[0x300a,0xb0][field_number][0x300a,0x111][0][0x300a,0x11a][2][0x300a,0x11c].value
                mlc.append(weight_mlc)
                for j in range(1,cp):
                    weight_mlc=ds[0x300a,0xb0][field_number][0x300a,0x111][j][0x300a,0x11a][0][0x300a,0x11c].value
                    mlc.append(weight_mlc)
                
                mlc_position=[["MLC_position"]]
                for i in range(cp):
                    mlc_cp=(mlc[i][:])
                    mlc_position.append(mlc_cp)      
                # MLC Velocity at CP
                mlc_velocity=[["MLC_velocity"],[0]*120] 
                for j in range(1,cp):
                    mlc_velocity_cp=[]
                    for m in range(120):
                        diff=(mlc_position[j+1][m]-mlc_position[j][m])
                        velocity=diff/meterset_time[j-1]    
                        mlc_velocity_cp.append(velocity)
                    mlc_velocity.append(mlc_velocity_cp)        
                # MLC Acceleration at CP
                mlc_acceleration=[["MLC_acceleration"],[0]*120] 
                for j in range(1,cp):
                    mlc_acceleration_cp=[]
                    for m in range(120):
                        diff=(mlc_velocity[j+1][m]-mlc_velocity[j][m])
                        acceleration=diff/meterset_time[j-1]    
                        mlc_acceleration_cp.append(acceleration)
                    mlc_acceleration.append(mlc_acceleration_cp) 
                # Control Point
                control_point=[["Control_point"]] 
                for i in range(cp):
                    control_point_cp=[]
                    for m in range(120):
                        controlpointcp=i/cp
                        control_point_cp.append(controlpointcp)
                    control_point.append(control_point_cp) 
                # Dose Rate
                dose_rate=[["Dose_rate"],[0]*120] 
                for j in range(1,cp):
                    dose_rate_cp=[]
                    for m in range(120):
                        doseratecp=1
                        dose_rate_cp.append(doseratecp)
                    dose_rate.append(dose_rate_cp) 
                # Gravity Vector
                gravity_vector=[["Gravity_vector"]] 
                for i in range(cp):
                    gravity_vector_cp=[]
                    for m in range(120):
                        gravityvector=math.sin(gantryangle)*math.cos(collimatorangle)
                        gravity_vector_cp.append(gravityvector)
                    gravity_vector.append(gravity_vector_cp)   
                # Index
                index=[["Index"]] 
                for i in range(cp):
                    index_cp=[]
                    for m in range(120):
                        indexcp=str(i)+"_"+str(m)
                        index_cp.append(indexcp)
                    index.append(index_cp)
                    
                dataset=[]
                index_1 = [x for xs in index for x in xs]
                mlc_position_1 = [x for xs in mlc_position for x in xs]
                mlc_velocity_1 = [x for xs in mlc_velocity for x in xs]
                mlc_acceleration_1 = [x for xs in mlc_acceleration for x in xs]
                control_point_1 = [x for xs in control_point for x in xs]
                dose_rate_1 = [x for xs in dose_rate for x in xs]
                gravity_vector_1 = [x for xs in gravity_vector for x in xs]
                dataset.append(index_1)
                dataset.append(mlc_position_1)
                dataset.append(mlc_velocity_1)
                dataset.append(mlc_acceleration_1)
                dataset.append(control_point_1)
                dataset.append(dose_rate_1)
                dataset.append(gravity_vector_1)
                matrix_t =list(map(list, zip(*dataset)))
                del matrix_t[0]
                df = pd.DataFrame(matrix_t,columns =['Index','MLC_position','MLC_velocity','MLC_acceleration','Control_point',
                                                     'Dose_rate', 'Gravity_vector'])
                li.append(df)
                
                """field_num = str(field_number) 
                numpy.savetxt("RTDICOM_IMRT_"+field_num+".csv", matrix_t, delimiter=",",fmt='%s')"""

    
    
    else:
        for field_number in range (num_beam): 
            type = ds[0x300a,0xb0][field_number][0x300a,0xce].value
            treatment = "TREATMENT" in type
            if treatment is False:
                dataset=[]  
                df = pd.DataFrame(dataset,columns =['Index','MLC_position','MLC_velocity','MLC_acceleration','Control_point',
                                                     'Dose_rate', 'Gravity_vector', 'Gantry_velocity', 'Gantry_acceleration'])
                li.append(df)
            else:
                # Number of Contorl Point
                cp=ds[0x300a,0xb0][field_number][0x300a,0x110].value                
                # Prescription Monitor Unit
                mu=ds[0x300a,0x70][0][0x300c,0x04][field_number][0x300a,0x86].value
                # Dose Rate Set
                dr=ds[0x300a,0xb0][field_number][0x300a,0x111][0][0x300a,0x115].value
                # MU/min => MU/sec
                dr_s=dr/60                 
                # Gantry Angle
                gantry_angle_actualdegree=[]
                gantry_angle_degree=[]
                gantry_angle_rad=[]
                for i in range(cp): 
                    ga=ds[0x300a,0xb0][field_number][0x300a,0x111][i][0x300a,0x11e].value  
                    gantryangle=ga/180*math.pi
                    gantry_angle_actualdegree.append(ga)
                    if ga<180:
                        ga=180-ga
                    elif ga>180:
                        ga=540-ga        
                    gantry_angle_degree.append(ga)
                    gantry_angle_rad.append(gantryangle)
                # Collimator Angle
                ca=ds[0x300a,0xb0][field_number][0x300a,0x111][0][0x300a,0x120].value 
                collimatorangle=ca/180*math.pi  
                # Cumulative Meterset Weight
                meterset_weight=[]
                for i in range(cp):
                    weight=ds[0x300a,0xb0][field_number][0x300a,0x111][i][0x300a,0x134].value
                    meterset_weight.append(weight)
                # Monitor Unit at CP
                meterset_mu=[]
                meterset_cumulative_mu=[]
                for j in range(1,cp):   
                    weight_diff=meterset_weight[j]-meterset_weight[j-1]
                    weight_mu=mu*weight_diff
                    weight_cumulative_mu=mu*meterset_weight[j]
                    meterset_mu.append(weight_mu)
                    meterset_cumulative_mu.append(weight_cumulative_mu)
                # Time Interval at CP
                gantry_speed=4.8
                meterset_time=[]
                for k in range(cp-1): 
                    max_mu_cp=abs(gantry_angle_degree[k+1]-gantry_angle_degree[k])*dr_s/gantry_speed
                    if meterset_mu[k]<max_mu_cp:
                        weight_time=abs(gantry_angle_degree[k+1]-gantry_angle_degree[k])/gantry_speed
                    elif meterset_mu[k]>max_mu_cp:
                        weight_time=meterset_mu[k]/dr_s
                    meterset_time.append(weight_time)
                # MLC Position at CP
                mlc=[]
                weight_mlc=ds[0x300a,0xb0][field_number][0x300a,0x111][0][0x300a,0x11a][2][0x300a,0x11c].value
                mlc.append(weight_mlc)
                for j in range(1,cp):
                    weight_mlc=ds[0x300a,0xb0][field_number][0x300a,0x111][j][0x300a,0x11a][0][0x300a,0x11c].value
                    mlc.append(weight_mlc)
                mlc_position=[["MLC_position"]]
                for i in range(cp):
                    mlc_cp=(mlc[i][:])
                    mlc_position.append(mlc_cp)
                # MLC Velocity at CP
                mlc_velocity=[["MLC_velocity"],[0]*120] 
                for j in range(1,cp):
                    mlc_velocity_cp=[]
                    for m in range(120):
                        diff=(mlc_position[j+1][m]-mlc_position[j][m])
                        velocity=diff/meterset_time[j-1]    
                        mlc_velocity_cp.append(velocity)
                    mlc_velocity.append(mlc_velocity_cp)            
                # MLC Acceleration at CP
                mlc_acceleration=[["MLC_acceleration"],[0]*120] 
                for j in range(1,cp):
                    mlc_acceleration_cp=[]
                    for m in range(120):
                        diff=(mlc_velocity[j+1][m]-mlc_velocity[j][m])
                        acceleration=diff/meterset_time[j-1]    
                        mlc_acceleration_cp.append(acceleration)
                    mlc_acceleration.append(mlc_acceleration_cp) 
                # Control Point
                control_point=[["Control_point"]] 
                for i in range(cp):
                    control_point_cp=[]
                    for m in range(120):
                        controlpointcp=i/cp
                        control_point_cp.append(controlpointcp)
                    control_point.append(control_point_cp) 
                # Dose Rate
                dose_rate=[["Dose_rate"],[0]*120] 
                for j in range(1,cp):
                    dose_rate_cp=[]
                    for m in range(120):
                        doseratecp=1
                        dose_rate_cp.append(doseratecp)
                    dose_rate.append(dose_rate_cp)   
                # Gravity Vector
                gravity_vector=[["Gravity_vector"]] 
                for i in range(cp):
                    gravity_vector_cp=[]
                    for m in range(120):
                        gravityvector=math.sin(gantry_angle_rad[i])*math.cos(collimatorangle)
                        gravity_vector_cp.append(gravityvector)
                    gravity_vector.append(gravity_vector_cp)
                # Gantry Velocity at CP
                gantry_velocity=[["Gantry_velocity"],[0]*120] 
                for k in range(cp-1):
                    gantry_velocity_cp=[]
                    for m in range(120):
                        diff=(gantry_angle_degree[k+1]-gantry_angle_degree[k])
                        velocity=diff/meterset_time[k]    
                        gantry_velocity_cp.append(velocity)
                    gantry_velocity.append(gantry_velocity_cp)    
                # Gantry Acceleration at CP
                gantry_acceleration=[["Gantry_acceleration"],[0]*120] 
                for j in range(1,cp):
                    gantry_acceleration_cp=[]
                    for m in range(120):
                        diff=(gantry_velocity[j+1][m]-gantry_velocity[j][m])
                        acceleration=diff/meterset_time[j-1]    
                        gantry_acceleration_cp.append(acceleration)
                    gantry_acceleration.append(gantry_acceleration_cp)         
                # Index
                index=[["Index"]] 
                for i in range(cp):
                    index_cp=[]
                    for m in range(120):
                        indexcp=str(i)+"_"+str(m)
                        index_cp.append(indexcp)
                    index.append(index_cp)  
            
                dataset=[]
                index_1 = [x for xs in index for x in xs]
                mlc_position_1 = [x for xs in mlc_position for x in xs]
                mlc_velocity_1 = [x for xs in mlc_velocity for x in xs]
                mlc_acceleration_1 = [x for xs in mlc_acceleration for x in xs]
                control_point_1 = [x for xs in control_point for x in xs]
                dose_rate_1 = [x for xs in dose_rate for x in xs]
                gravity_vector_1 = [x for xs in gravity_vector for x in xs]
                gantry_velocity_1 = [x for xs in gantry_velocity for x in xs]
                gantry_acceleration_1 = [x for xs in gantry_acceleration for x in xs]
                dataset.append(index_1)
                dataset.append(mlc_position_1)
                dataset.append(mlc_velocity_1)
                dataset.append(mlc_acceleration_1)
                dataset.append(control_point_1)
                dataset.append(dose_rate_1)
                dataset.append(gravity_vector_1)
                dataset.append(gantry_velocity_1)
                dataset.append(gantry_acceleration_1)
                matrix_t =list(map(list, zip(*dataset)))
                del matrix_t[0]
                df = pd.DataFrame(matrix_t,columns =['Index','MLC_position','MLC_velocity','MLC_acceleration','Control_point',
                                                     'Dose_rate', 'Gravity_vector', 'Gantry_velocity', 'Gantry_acceleration'])
                li.append(df)
                
                """field_num = str(field_number) 
                numpy.savetxt("RTDICOM_VMAT_"+field_num+".csv", matrix_t, delimiter=",",fmt='%s')"""

    
    
    # Change SOP Instance UID for reimport
    UID = ds[0x08,0x18].value
    a = UID.split('.')
    b = random.random()
    c = str(int(round(b,14)*100000000000000))
    a[8] = c 
    d = ".".join(a)
    ds[0x08,0x18].value = d
    
    # RMS & Max Error
    rms_list=[]
    max_list=[]
    
    # Modify MLC positions   
    for field_number in range (num_beam): 
        type = ds[0x300a,0xb0][field_number][0x300a,0xce].value
        treatment = "TREATMENT" in type
        if treatment is False:
            pass
        else: 
            model1 = "IMRT_linearVonly.sav" in filename
            model2 = "IMRT_linear.sav" in filename
            model3 = "IMRT_tree.sav" in filename
            model4 = "IMRT_boosted.sav" in filename
            model5 = "IMRT_bagged.sav" in filename
            model6 = "VMAT_linearVonly.sav" in filename
            model7 = "VMAT_linear.sav" in filename
            
            global y1
            if model1 or model6 is True:
                X = li[field_number]['MLC_velocity'].values.reshape(-1,1)
                y1 = clf.predict(X)
                y1 = [x for xs in y1 for x in xs]
                y1 = np.array(y1)
             
            elif model2 is True:
                X = li[field_number][['MLC_velocity','MLC_acceleration','Control_point','Dose_rate','Gravity_vector']].values.reshape(-1,5)
                y1 = clf.predict(X)
                y1 = [x for xs in y1 for x in xs]
                y1 = np.array(y1)
                
            elif model3 or model4 or model5 is True:
                X = li[field_number][['MLC_velocity','MLC_acceleration','Control_point','Dose_rate','Gravity_vector']].values.reshape(-1,5)
                y1 = clf.predict(X)
                
            elif model7 is True:
                X = li[field_number][['MLC_velocity','MLC_acceleration','Control_point','Dose_rate',
                         'Gravity_vector','Gantry_velocity','Gantry_acceleration']].values.reshape(-1,7)
                y1 = clf.predict(X)
                y1 = [x for xs in y1 for x in xs]
                y1 = np.array(y1)
                                
            else:
                X = li[field_number][['MLC_velocity','MLC_acceleration','Control_point','Dose_rate',
                         'Gravity_vector','Gantry_velocity','Gantry_acceleration']].values.reshape(-1,7)
                y1 = clf.predict(X)
              
                           
            mlc_position = pd.to_numeric((li[field_number]['MLC_position']), errors='coerce')
            mlc_new_position = mlc_position + y1
            li[field_number]['MLC_diff'] = y1 
            li[field_number]['MLC_New_position'] = mlc_new_position 
            #li[field_number].to_csv(all_files[field_number])
            
            
            #  RMS & Max Error
            rms = np.sqrt(np.mean(y1**2))
            max_error = float(max(y1))
            rms_list.append(rms)
            max_list.append(max_error)            
            
            
            # Take actual MLC position
            actual_mlc=[]
            col = li[field_number]['MLC_New_position']
            actual_mlc.append(col)
                
            cp_number = int(len(col)/120)
            
            # Take actual MLC position
            actual_mlc1=[]
            for j in range(cp_number):
                actual_mlc2=[]
                for k in range(120):  
                    a=(actual_mlc[0][120*j+k])
                    actual_mlc2.append(a)
                actual_mlc1.append(actual_mlc2)    
            
            
            
            # read dicom file
            print(str(field_number)+'con0',ds[0x300a,0xb0][field_number][0x300a,0x111][0][0x300a,0x11a][2][0x300a,0x11c].value)
            
            
            # modify control point 0 dicom file
            ds[0x300a,0xb0][field_number][0x300a,0x111][0][0x300a,0x11a][2][0x300a,0x11c].value = actual_mlc1[0]
            print(str(field_number)+'con0',ds[0x300a,0xb0][field_number][0x300a,0x111][0][0x300a,0x11a][2][0x300a,0x11c].value)
            
            
            # modify control point 1~ second last dicom file
            for m in range(1,cp_number):
                print(str(field_number)+'con',m,ds[0x300a,0xb0][field_number][0x300a,0x111][m][0x300a,0x11a][0][0x300a,0x11c].value)
                
                ds[0x300a,0xb0][field_number][0x300a,0x111][m][0x300a,0x11a][0][0x300a,0x11c].value = actual_mlc1[m]
                print(str(field_number)+'con',m,ds[0x300a,0xb0][field_number][0x300a,0x111][m][0x300a,0x11a][0][0x300a,0x11c].value)

    
    # Write a new dicom file
    def square(list):
        return [i ** 2 for i in list]
    rms_all = str(round(np.sqrt(np.mean(square(rms_list))),4))
    max_all = str(round(max(max_list),4))
    lbl3.configure(text="RMS Error: "+rms_all+ " mm")
    lbl4.configure(text="Max Error: "+max_all+ " mm")
    
    # Save new revised DICOM
    ds.save_as("new_dicom.dcm")

lbl3 = Label(window, text="RMS Error:")
lbl3.grid(column=0, columnspan=2, row=7)
lbl4 = Label(window, text="Max Error:")
lbl4.grid(column=2, columnspan=2, row=7)
btn = Button(window, text="Run", command=clicked11)
btn.grid(column=2, row=8)





window.mainloop()

