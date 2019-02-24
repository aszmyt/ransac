#!/usr/bin/env python
import matplotlib.pyplot as plt
import random
import numpy as np
from math import sin,cos,tan,degrees
from ransac import *
import json
json_data = open('line_detection_2.json')
data = json.load(json_data)

skan=data[0]["scan"]
pozycja=data[0]["pose"]

x = np.arange(0,512)
theta = (np.pi/512 )*(x-256)  # kat w radianach


x=[]
y=[]
xys=np.zeros((512, 2))
for i in range(0,511):
	xx = cos(theta[i])*skan[i]
	x.append(xx)
	yy = sin(theta[i])*skan[i]
	y.append(yy)
	xys[i,0]=xx
	xys[i,1]=yy


#fig3 = plt.figure()
#ax3 = fig3.add_axes([0.1,0.1,0.8,0.8])
#line, = ax3.plot(x,y)
#ax3.set_xlim(-5,5)
#ax3.set_ylim(-5,5)
#plt.show()


def augment(xys):
	axy = np.ones((len(xys), 3))
	axy[:, :2] = xys
	return axy

def estimate(xys):
	axy = augment(xys[:2])
	return np.linalg.svd(axy)[-1][-1, :]

def is_inlier(coeffs, xy, threshold):
	return np.abs(coeffs.dot(augment([xy]).T)) < threshold

if __name__ == '__main__':
	from matplotlib import pylab
        
	n = 512
        max_iterations = 50
	goal_inliers = n*0.1
        


	# RANSAC dla jednej linii
        #m, b = run_ransac(xys, estimate, lambda x, y: is_inlier(x, y, 0.01), goal_inliers, max_iterations, 20)
        #a, b, c = m
	# RANSAC dla wielu linii
        a,b,c,num,dane =  run_ransac(xys, estimate, lambda x, y: is_inlier(x, y, 0.006), goal_inliers, max_iterations, 400)
	lx=np.arange(-5.0, 5.0, 0.1)
	ly=np.zeros((100, num))
        A1=None
	for j in range(0,num):
		for i in range(len(lx)):
			temp = -a[j]/b[j]*lx[i] -c[j]/b[j]
			ly[i][j]=temp
                        #print(a[j],b[j],c[j], temp)
        for j in range(0,num):
            Y=-a[j]/b[j]
            for i in range(j,num):
                Y1=-a[i]/b[i]
                #print(Y,Y1,j,i)
                if Y*Y1<-0.95 and Y*Y1>-1.05:
                    A1=j
                    A2=i
                    #print("znalazlem",A1,A2)
        lx_1=np.arange(-5.0,5.0,0.01)
        if A1 != None:
            A=[]
            A.append(A1)
            A.append(A2)

            for j in range(0,2):
                #print(j)
                for i in range(len(lx_1)):
                    x1=lx_1[i]
                    y1=-a[j]/b[j]*lx_1[i] -c[j]/b[j]
                    x2=pozycja[0]
                    y2=pozycja[1]
                    A1=x1-x2
                    B1=-y1-x2
                    C1=y2*x1+y1*x2
                    if -a[j]/b[j]>0:
                        if A1/B1*a[j]/b[j] <-0.99 and A1/B1*a[j]/b[j] >-1.01:
                            p_x=-x2+x1
                            kat=90+degrees(tan(a[j]/b[j]/(1-a[j]/b[j])))

                    else:
                        if A1/B1*a[j]/b[j] <-0.99 and A1/B1*a[j]/b[j] >-1.01:
                            p_y=-y2+y1

            print([p_x],[p_y],[kat])
        if A1 == None:
            kat=None
            p_x=None
            tmp2=-9999.00
            for j in range(0,num):
                for i in range(len(lx)):
                    temp = -a[j]/b[j]*lx[i] -c[j]/b[j]
                    if temp > tmp2:
                        A=a[j]
                        B=b[j]
                        C=c[j]
                        tmp2=temp
            for i in range(len(lx_1)):
                x1=lx_1[i]
                y1=-A/B*lx_1[i] -C/B
                x2=pozycja[0]
                y2=pozycja[1]
                A1=x1-x2
                B1=-y1-x2
                C1=y2*x1+y1*x2
                if A1/B1*A/B <-0.95 and A1/B1*A/B >-1.05:
                    print("s")
                    p_x=-x2+x1
                    kat=90+degrees(tan(a[j]/b[j]/(1-a[j]/b[j])))
            print([p_x],[kat])
        fig3 = plt.figure()
	ax3 = fig3.add_axes([0.1,0.1,0.8,0.8])
        #line, = ax3.plot(lx,ly,color=(0, 1, 0))
        ax3.plot(lx,ly,color=(0, 1, 0))
        ax3.set_xlim(-5,5)
        ax3.set_ylim(-5,5)
	#plt.scatter(x, y)
	line2, = ax3.plot(x,y)
	plt.show()




