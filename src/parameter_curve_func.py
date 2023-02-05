import numpy as np
#from scipy import interpolate
import matplotlib.pyplot as plt
import  math


t = np.linspace(0,1,50)


x_0=0
y_0=0
x_1=1
y_1=0
x_2=0
y_2=1
x_3=1
y_3=1




def f(t):
	return (1-t)*((1-t)*((1-t)*x_0+t*x_0)+t*((1-t)*x_1+t*x_2))+t*((1-t)*((1-t)*x_1+t*x_2)+t*((1-t)*x_2+t*x_3))
def g(t):
	return (1-t)*((1-t)*((1-t)*y_0+t*y_1)+t*((1-t)*y_1+t*y_2))+t*((1-t)*((1-t)*y_1+t*y_2)+t*((1-t)*y_2+t*y_3))

x = [f(t_i) for t_i in t]
y = [g(t_i) for t_i in t]
#plt.figure(figsize=(10,10))
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.set_aspect('equal')
ax.plot(x, y,label="controlpoint")



def function(input):
	for i in range(len(t)-1):
		if input >= x[i] and input < x[i+1]:
			output = (y[i+1]-y[i])/(x[i+1]-x[i])*(input-x[i])+y[i]
			return  output
		else:
			continue
		
	

plt.title("bezier")
