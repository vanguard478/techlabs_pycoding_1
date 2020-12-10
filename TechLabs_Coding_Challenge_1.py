import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy import interpolate, optimize
import csv
import timeit


# Directory to be scanned 
#"01-data" directory needs to to specified -- where all the data folders(different gas mixutures) are located
rootdir = r'C:\Users\Raza\IDrive-Sync\RoboSys\Study Materials\RoboSys\TechLabs  AI\github_commit\py_challenges\01_challenge\01-data'
dir_obj = os.scandir(rootdir) 
dirs=[]
filenames_all=[]
data=[]
col_names=['time','current','voltage']
OCV_all=[]
ASR_all=[]
cell_area=0.785
J_curr_den_all=[]
heading='CO2-(%) CO-(%)	T-(°C)	OCV-(V)	ASR-(ohm-cm^2)	J@1.4V-A/cm^2'.split()

with open(r"03-result\result.csv", 'w', newline='') as myfile:
     wr = csv.writer(myfile)
     wr.writerow(heading)
for entry in dir_obj :
    dirs.append(entry.name)
    curr_path=rf'{rootdir}\{entry.name}'
    file_obj = os.scandir(curr_path) 
    df=[pd.read_csv(files,delim_whitespace=True,   names=col_names,header=0) for files in file_obj]
    data.append(df)
    file_obj = os.scandir(curr_path)
    filenames=[f_names.name for f_names in file_obj]
    filenames_all.append(filenames)
  
for j in range(len(data)):
    fig,axes=plt.subplots()
    OCV=[]
    ASR=[]
    J_curr_den=[]
    for i in range(len(filenames_all[j])):
        df_curr=data[j][i]
        
        #Combining voltage response from the two cycles of current(I) flow [0 -> max(I) ->0 -> max(I) -> 0]
        # axes.plot(df_curr['current']/cell_area,df_curr['voltage'],lw=0.7) # for plotting the default dataframe
        df_curr['gradient']=df_curr['current'].diff()>=0 #Creating Marker for increasing or decreasing current(I) 
        #Datapoints for increasing current(I)
        df1=df_curr[df_curr['gradient']==True].groupby(['current'],as_index=False).mean()
        #Datapoints for decreasing current(I)
        
        df2=df_curr[df_curr['gradient']==False].groupby(['current'],as_index=False).mean().sort_values('current',ascending=False)
        df_final=pd.concat([df1,df2]).reset_index(drop=True)
        #filtering out rows where the change in current is minuscule
        df_final=df_final[df_final['current'].pct_change().abs()>1e-03]
        
        #plotting the Voltage vs Current Density
        current_density=df_final['current']/cell_area
        voltage1=df_final['voltage']
        
        axes.plot(current_density,voltage1,lw=1.5,label=filenames[i].split(' ')[1]) #for plotting the filtered Current Voltage values
        
        #Curve_Fitting to find the OCV and ASR(@100 mA) using the derivative of 
        #the fitted curve ##local region around 0 is choosen using current<0.15
        
        x=df_final[df_final['current']<0.15]['current']/cell_area
        y=df_final[df_final['current']<0.15]['voltage']
        
        #function for intercept, x is the current density value
        def func(x,a,b,c):
            return  a*x**2+b*x+c
        
        (a,b,c), pcov = optimize.curve_fit(func, x, y)
        #OCV @ J=0
        OCV.append(func(0,a,b,c).round(decimals=3))
        #function for slope,  x is the current density value
        def func_derivative(x):
            return 2*a*x+b
        
        
        
        #ASR Value @100 mA of current
        ASR.append(func_derivative(0.1/cell_area).round(decimals=3))  
        

        #For plotting the fitted curve and tangent line around the 100 mA current 
        # x1=0.1/cell_area
        # y1=func(x1,a,b,c)
        # def line(x, x1, y1):
        #     return func_derivative(x1)*(x - x1) + y1
        # xrange = np.linspace(x1-0.2, x1+0.2, 10)
        # axes.plot(xrange,func(xrange,a,b,c))
        # axes.plot(xrange,line(xrange,x1,y1),lw=2)

                
        #Interpolation of the curve around the region where the voltage=1.4
        #To implement the spline interpolation splrep the x values should be in increasing order
        
        
        xx1=df_final[(df_final['voltage']>1.25)&(df_final['voltage'].diff(-1)>=0)].sort_values('current')['current'] /cell_area        
        yy1=df_final[(df_final['voltage']>1.25)&(df_final['voltage'].diff(-1)>=0)].sort_values('current')['voltage']
       
        xx2=df_final[(df_final['voltage']>1.25)&(df_final['voltage'].diff(-1)<=0)&(df_final['current'].diff(-1)<=0)]['current'] /cell_area
        yy2=df_final[(df_final['voltage']>1.25)&(df_final['voltage'].diff(-1)<=0)&(df_final['current'].diff(-1)<=0)]['voltage']
        
        #Interpolation for the part in which current is increasing
        spl1 = interpolate.UnivariateSpline(xx1, yy1, k=3 ,s=1)
        
     
        #Interpolation for the part in which current is decreasing
        spl2 = interpolate.UnivariateSpline(xx2, yy2, k=3 ,s=1)

        #Roots for J
        spl1r = interpolate.UnivariateSpline(xx1, yy1-1.4, k=3 ,s=1).roots()
        spl2r = interpolate.UnivariateSpline(xx2, yy2-1.4, k=3 ,s=1,bbox=[xx2.min(),1.2*xx2.max()]).roots()
        
        #current denstiy for measured V=1.4 is estimated using mean of the current density obtained @increasing current I and decreasing current I
        J_curr_den.append(0.5*(spl1r[0]+spl2r[0]).round(decimals=3)) 

        #plotting the points for current density
        # axes.scatter(spl1r,np.array([1.4]),marker='*',color='red')
        # axes.scatter(spl2r,np.array([1.4]),marker='*',color='red')

        #Writing Values to CSV files
        co2_per=int(dirs[j].split('CO')[0])
        temp=filenames[i].split(' ')[1]
        co_per=100-co2_per
        # plt.savefig(fname=rf'03-result\{dirs[j]}.jpg',format='jpg',dpi=100)
        with open(r"03-result\result.csv","a+") as f:
            f.write(f'{co2_per},{co_per},{temp},{OCV[i]},{ASR[i]},{J_curr_den[i]}\n')
        
    OCV_all.append(OCV)
    ASR_all.append(ASR)
    J_curr_den_all.append(J_curr_den)
    axes.set_xlabel(r'$J/A\: cm^{-2}$')
    axes.set_ylabel(r'$E/V$')
    axes.set_title(dirs[j].split('_'))
    axes.legend(loc=0) 
print(timeit.timeit())
plt.tight_layout()
plt.show()    

