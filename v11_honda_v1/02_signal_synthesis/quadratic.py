# 2*pi is one period use degrees internally
# signal is 9+3

#https://people.cs.clemson.edu/~dhouse/courses/405/notes/splines.pdf
#https://www.youtube.com/watch?v=bn8iJKFldq0

#python -m venv venv
#pip install scipy
#pip install matplotlib

#def signal_degree(x):
#    return x % 360

#print(signal_degree(30.1))
#print(signal_degree(30.1+360))


#https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.BPoly.from_derivatives.html
#https://docs.scipy.org/doc/scipy/tutorial/interpolate.html

from scipy.interpolate import BPoly
#function1 = BPoly.from_derivatives([0, 1, 30], [[0,0],[1,0],[-1,1]])
#function2 = BPoly.from_derivatives([0, 1, 30], [[0,0],[1,0],[-1,1]], orders=1)
#print(function1(1))

#0,3.75,7.5,11.25,15,18.75,22.5,26.25
#[0,0],[0,0],[0,0.02],[1,0],[0,-2.6],[-1,0],[0,0.02],[0,0]

#function1 = BPoly.from_derivatives(x, y, orders=1)
#function2 = BPoly.from_derivatives([0,3.75,7.5,11.25,15,18.75,22.5,26.25], [[0,0],[0,0],[0,0.02],[1,0],[0,-0.6],[-1,0],[0,0.02],[0,0]])




import matplotlib.pyplot as plt
import numpy as np

x = [e/100 for e in range(0,36000, 375)]
x2 = [e/1000 for e in range(0,360000, 375)]
y = [0,0,0,1,0,-1,0,0]*9+[0,0,0,0,0,0,0,0]*3
fp = [[0,0],[0,0],[0,0],[1,0],[0,0],[-1,0],[0,0],[0,0]]*9+[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]*3
gp = [[0,0],[0,0],[0,0.02],[1,0],[0,-0.6],[-1,0],[0,0.02],[0,0]]*9+[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]*3
hp = [[0,0],[0,0],[0.05,0.02],[1,0],[0,-0.6],[-1,0],[-0.05,0.02],[0,0]]*9+[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]*3

f = BPoly.from_derivatives(x, fp, orders=1)
g = BPoly.from_derivatives(x, gp)
h = BPoly.from_derivatives(x, hp)

#x = [0,3.75,7.5,11.25,15,18.75,22.5,26.25]
#y = [0,0,0,1,0,-1,0,0]
#y1 = [function1(e) for e in x] 
#y2 = [function2(e) for e in x] 
#plt.plot(x, y, 'o', y2)
#plt.legend(['data', 'linear', 'cubic'], loc='best')
plt.plot(x, y, 'bo', x, [f(e) for e in x], 'g--', x2, [g(e) for e in x2], 'r', x2, [h(e) for e in x2], 'b')
plt.axis([0,360, -1.25, 1.25])
plt.show()