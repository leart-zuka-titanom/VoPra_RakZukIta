import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd

df = pd.read_csv('4.2K.csv')

magnet_np = np.array(df["Magnet"])
lockin_u_np = np.array(df["Lockin_U"])
lockin_uh_np = np.array(df["Lockin_Uh"])

plt.plot(magnet_np,lockin_u_np)
plt.plot(magnet_np,lockin_uh_np)
plt.savefig('4.2K.svg', format='svg',dpi=1200)
plt.show()

df = pd.read_csv('4.2K_illu.csv')

magnet_np = np.array(df["Magnet"])
lockin_u_np = np.array(df["Lockin_U"])
lockin_uh_np = np.array(df["Lockin_Uh"])

plt.plot(magnet_np,lockin_u_np)
plt.plot(magnet_np,lockin_uh_np)
plt.savefig('4.2K_illu.svg', format='svg',dpi=1200)
plt.show()

df = pd.read_csv('1.4K_illu.csv')

magnet_np = np.array(df["Magnet"])
lockin_u_np = np.array(df["Lockin_U"])
lockin_uh_np = np.array(df["Lockin_Uh"])

plt.plot(magnet_np,lockin_u_np)
plt.plot(magnet_np,lockin_uh_np)
plt.savefig('1.4K_illu.svg', format='svg',dpi=1200)
plt.show()


#FUCK THIS THING
df = pd.read_csv('1.4K_illu_fine.csv')

magnet_np = np.array(df["Magnet"])
lockin_u_np = np.array(df["Lockin_U"])
lockin_uh_np = np.array(df["Lockin_Uh"])

plt.plot(magnet_np,lockin_u_np)
plt.plot(magnet_np,lockin_uh_np)
plt.savefig('1.4K_illu_fine.svg', format='svg',dpi=1200)
plt.show()
