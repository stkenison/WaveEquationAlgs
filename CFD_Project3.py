import numpy as np; import os;import matplotlib.pyplot as plt;import math;
os.system('cls')
plt.rcParams['font.family'] = 'Times New Roman'

#define constants for problem
c = 1; cfl = 0.25
gridsize = [40, 80, 160];num_of_algs = 3
dx = np.zeros(len(gridsize));dt = np.zeros(len(gridsize));g = np.zeros(len(gridsize))
x_interval = [0, 10];t_interval = [0, 20]
for i in range(0,len(gridsize)): #define dx based on interval and grid size
    dx[i] = (x_interval[1]-x_interval[0])/gridsize[i]
for i in range(0,len(gridsize)): #define dt based on cfl, dx, and c
    dt[i] = cfl*dx[i]/c

for z in range(0,num_of_algs): #loop for different plotting algorithms
    for i in range(0,len(gridsize)): #loop through 3 different grid sizes
        
        #define initial arrays with initial values for x, y, and time
        x_vals = np.linspace(x_interval[0],x_interval[1]-dx[i],gridsize[i])
        y_vals = np.zeros(gridsize[i])
        for j in range(0,len(y_vals)):
            if x_vals[j]<=2*3.14159265:
                y_vals[j]= 1-np.cos(x_vals[j])

        #plot initial curve & analytical solutions with proper titles
        plt.figure(i+1+3*z)
        if z==0: alg_type='First-Order Upwind'
        elif z==1: alg_type='Second-Order Central Difference'
        elif z==2: alg_type='Beam-Warming Second Order Upwind'
        plt.title('Wave Function - Gridsize of {grid} | {alg}'.format(grid=gridsize[i],alg=alg_type))
        plt.xlabel("X");plt.ylabel("Y");t=0
        plt.plot(x_vals,y_vals,label='t = {}'.format(t))
        #plt.plot(x_vals+3,y_vals) #plot theoretical solutions
        
        #iterate with respect to time
        for k in range(1,int((t_interval[1]-t_interval[0])/dt[i])+1):
            t = dt[i]*k
            y_vals_old = y_vals #save y values from last iteration
            
            if z==0: #iterate through points for next timestep (first order upwind)
                for j in range(0,len(y_vals)):
                    y_vals[j] = y_vals_old[j]-cfl*(y_vals_old[j]-y_vals_old[j-1])
            
            elif z==1: #iterate through points for next timestep (second order central difference)
                for j in range(0,len(y_vals)):
                    y_vals[j] = y_vals_old[j]+cfl/2*(y_vals_old[(j+1)%gridsize[i]]+y_vals_old[j-1])

            elif z==2: #iterate through points for next timestep (second order upwind)
                for j in range(0,len(y_vals)):
                    nj = y_vals_old[j]
                    nj1 = y_vals_old[j-1]
                    nj2 = y_vals_old[j-2]
                    y_vals[j] = nj-cfl/2*(3*nj-4*nj1+nj2)+cfl/2*(nj-2*nj1+nj2)
            
            #plot solution if it fits in desired values
            if t==1 or t==5 or t==20:
                x_vals1 = np.concatenate((x_vals,[10]),axis=0) #plot x_val from t=0 to t=10
                y_vals1 = np.concatenate((y_vals,[y_vals[0]]),axis=0) #plot y_val from t=0 to t=10
                plt.plot(x_vals1,y_vals1,label='t = {}'.format(t))
        
        #format plot
        plt.legend(loc='upper right')
        plt.xlim(0,10);plt.ylim(0,2.5)
plt.show()
