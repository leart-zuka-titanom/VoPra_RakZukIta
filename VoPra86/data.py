import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import math

df = pd.read_csv("data.csv")               # reads in values from csv u need to add the line "single,double" at the top
y_single = np.array(df["single"])           # reads numbers for single count
y_double = np.array(df["double"])           # reads numbers for double count
thetamax = 0.0157
x = np.linspace(-1*thetamax, thetamax, 63)                 # general array with how many numbers there are
values_y = []
values_x = []
goodvalue = 31
for i in range(goodvalue, 63):                     # this is just so that I have a numpy array with the right range
    values_y.append(y_single[i])
    values_x.append(x[i])
y_single_real = np.array(values_y)            # put that in a numpy array
x_real = np.array(values_x)                   # put that in a numpy array
const = []
for i in range(0, goodvalue-1):
    const.append(y_single[i])
baseline = sum(const)/len(const)
temp = 0
for i in const:
    temp += (i-baseline)**2
u_base = math.sqrt(temp/(len(const)-1))
bruh = []
for i in range(goodvalue, 63):
    bruh.append(y_single[i]/y_double[i])
scale = sum(bruh)/len(bruh)

def lin_func(x,a,b):                        # linear func
    return a * x + b

linear1,linear2 = curve_fit(lin_func,x,y_double)    # fit for that func for the double dataset
fity_lin = lin_func(x,linear1[0],linear1[1])        # array with the y values for the lin func fit
slope = scale*linear1[0]
correction = lin_func(x_real,-slope,0)
y_new = np.zeros(len(y_single_real))
for i in range(len(y_new)):
    y_new[i] = y_single_real[i] + correction[i]

def func(x,a,b,c,d,f):                          # quadratic func + gaussian func
    return a*(x-b)**2 + c + d*np.exp(-f*(x-b)**2)

def quad(x,a,b,c):
    return a*(x-b)**2 + c

params, cov = curve_fit(func,x_real,y_new,p0=[-5e5,0.005,-4e1,1e2,-10])   # fit for the sum of functions
print(params)                                                       # prints the parameters
up = np.sqrt(np.diag(cov))
fitX = np.linspace(x_real[0],thetamax,100)                                       # array with right x values
fitY = func(fitX,params[0],params[1],params[2],params[3],params[4]) # array with the y values of the one sum func
quadX = np.linspace(-thetamax/2, thetamax, 100)
quadY = quad(quadX,params[0],params[1],params[2]+params[3])
baseX = np.linspace(-thetamax, x_real[0]-thetamax/63, 100)
baseY = np.ones(100)*baseline

x_bad = []
for i in range(0,goodvalue-1):
    x_bad.append(x[i])
plt.plot(x_bad, const, '.')
plt.plot(x_real, y_new, '.')
plt.plot(fitX,fitY,'g')
plt.plot(baseX,baseY,'g')
plt.plot(quadX,quadY,'b')
#plt.plot(x_real,correction,'r')
plt.show()
#plt.plot(x,y_double, '.')
#plt.plot(x,fity_lin)
#plt.show()
#plt.plot(x_real,y_single_real,'.')
#plt.plot(x_real,y_new,'.')
#plt.show()

a = params[0]
u_a = up[0]
b = -2*params[0]*params[1]
u_b = b*math.sqrt((up[0]/params[0])**2 + (up[0]/params[1])**2)
c = params[0]*params[1]**2 + params[2] + params[3] - baseline
u_c = params[0]*params[1]**2*math.sqrt((up[0]/params[0])**2 + (2*up[1]/params[1])**2) + up[2] + up[3] + u_base
diff = math.sqrt(b**2-4*a*c)/a
u_diff = math.sqrt((u_a*(2*c*a-b**2)/(a**2*math.sqrt(b**2-4*a*c)))**2 + (u_b*b/(a*math.sqrt(b**2-4*a*c)))**2 + (u_c*2/math.sqrt(b**2-4*a*c))**2)
m = 9.11e-31
c0 = 3e8
e = 1.602e-19
p = diff*m*c0/2
u_p = p*2*u_diff/diff
E = p**2/(2*m*e)
u_E = 2*E*u_p/p
print(E, u_E)


#29, 30, 31: p0=[-5e5,0.005,-4e1,1e2,-10]
#32: p0=[-5e5,1e-3,-1e4,1e2,-1e1]