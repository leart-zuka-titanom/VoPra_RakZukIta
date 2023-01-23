import csv
import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

df = pd.read_csv("data.csv")               # reads in values from csv u need to add the line "single,double" at the top
y_single = np.array(df["single"])           # reads numbers for single count
y_double = np.array(df["double"])           # reads numbers for double count
x = np.linspace(1, 63, 63)                  # general array with how many numbers there are
cunt_y = []
cunt_x = []
for i in range(31, 63):                     # this is just so that I have a numpy array with the right range
    cunt_y.append(y_single[i])
    cunt_x.append(x[i])
y_single_real = np.array(cunt_y)            # put that in a numpy array
x_real = np.array(cunt_x)                   # put that in a numpy array

def lin_func(x,a,b):                        # linear func
    return a * x + b

cunt1,cunt2 = curve_fit(lin_func,x,y_double)    # fit for that func for the double dataset
fity_lin = lin_func(x,cunt1[0],cunt1[1])        # array with the y values for the lin func fit

def func(x,a,b,c,d,f):                          # quadratic func + gaussian func
    return a*(x-b)**2 + c + d*np.exp(-f*x**2)

params, cov = curve_fit(func,x_real,y_single_real,p0=[0,0,0,0,0])   # fit for the sum of functions
print(params)                                                       # prints the parameters
fitX = np.linspace(32,63,100)                                       # array with right x values
fitY = func(fitX,params[0],params[1],params[2],params[3],params[4]) # array with the y values of the one sum func


plt.plot(x, y_single)
plt.plot(x_real, y_single_real)
plt.plot(fitX,fitY)
plt.show()
plt.plot(x,y_double)
plt.plot(x,fity_lin)
plt.show()
