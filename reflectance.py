import numpy as np
import matplotlib.pyplot as plt
import csv

#=====USER INPUTS================#
wlmin=200  #lower wavelength limit (nm)
wlmax=850  #upper wavelength limit (nm)
dwl=1      #wavelength interval
#Load refractive index data (suffix .csv is attached automatically)
materials=["Ag","Si","MgF2","SiO2"] 

#Define the multilayer optical coating 
layers_d=[100,200,250,100] #thickness of each layer. 1st entry= thickness of 1st layer on substrate, last entry= last layer on top of the system facing air
layers_m=["Ag","TiO2","MgF2","SiO2","MgF2"] #Define the material of each layer, using the entries of the dictionary "materials"
substrate="Si" #Define the substrate here
#================================#


c0=3E-8
def read_csv(filename):
  """Read the .csv file containing the 
  refractive index data of a material.
  Input: string (e.g. "Ag.csv")
  Returns: A tuple containing a list for the wavelength, real refractive index and extinction coefficient"""
  lamb,nr,k=[],[],[]
  with open(filename, 'r') as file:
    reader = csv.reader(file, delimiter=';')
    next(reader, None)  
    for row in reader:
      lamb.append(float(row[0]))
      nr.append(float(row[1]))
      k.append(float(row[2]))
    return lamb, nr, k

def grid(X,Y):
  """ The data sets from the two measurement series do not neccessarily have identical 
  sampling points and the sampling points are generally not equidistant. This enforces
  sampling points on a welldefined, equidistant grid
  
  Input: Arrays for X and Y data (wavelength and refractive index)
  Output: Array with interpolated Y data, for the wavelength grid defined in the user inputs
  """
  X_grid = np.arange(wlmin, wlmax, dwl)
  Y_grid=[]
  for x in X_grid:
      i=1
      while X[i]<x and i<len(X)-1:
          i+=1
      x1,x2,y1,y2=X[i-1],X[i],Y[i-1],Y[i]
      Y_grid.append(y1+(x-x1)*(y2-y1)/(x2-x1))
  Y_grid=np.array(Y_grid)
  return Y_grid  

def get_n(material):
  """Inititiate reading the raw data and turning it into a complex array, containing the refractice indices""" 
  wl_raw, nr_raw, k_raw =read_csv("n_"+material+".csv")
  nr_grid=grid(wl_raw,nr_raw)
  k_grid=grid(wl_raw,k_raw)
  return nr_grid - 1j*k_grid

wl= np.arange(wlmin, wlmax, dwl)
n = {material: get_n(material) for material in materials}


def delta(i,j):
  """Compute face shift in a layer """
  return 2*np.pi*n[layers_m[i]][j]*layers_d[i]/wl[j]

def M_(i,j):
  """Compute transfer matrix of a layer"""
  Mi=np.zeros((2,2),dtype = 'complex_')
  Mi[0][0]=np.cos(delta(i,j))
  Mi[0][1]=(1j)*np.sin(delta(i,j))*c0/n[layers_m[i]][j]
  Mi[1][0]=1j*n[layers_m[i]][j]*np.sin(delta(i,j))/c0
  Mi[1][1]=np.cos(delta(i,j))
  return Mi


#=====MAIN============
Transfermatrices=[]
for j in range(len(wl)):
  M=np.identity(2,dtype = 'complex_')
  for i in range(len(layers_d)):
    M=M_(i,j)@ M
  Transfermatrices.append(M)
  
  
R=[]
for j in range(len(wl)):
    M=Transfermatrices[j]
    y0,ys=1/c0, n[substrate][j]/c0
    rj=(y0*M[0][0]+y0*ys*M[0][1]- M[1][0]-ys*M[1][1])/(y0*M[0][0]+y0*ys*M[0][1]+M[1][0]+M[1][1]*ys)
    R.append(np.absolute(rj)**2)

#Output    
plt.plot(wl,R)
plt.ylim(0,1)
plt.xlim(200,800)
plt.xlabel("Wavelength (nm)")
plt.ylabel("Reflectance (1)")
plt.show()
