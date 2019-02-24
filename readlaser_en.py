#!/usr/bin/env python
from time import sleep
from drive import RosAriaDriver

from math import sin, cos

### replace X with the robot number
robot=RosAriaDriver('/PIONIER4')
skan=robot.ReadLaser()

### read and write in json format
import json
with open('data_stereo.json','w') as json_data_file:
    json.dump(skan,json_data_file)
## print to stdout
#print(json.dumps(skan))
## read data from file
#json_data = open('skan.json')
#data = json.load(json_data)

import matplotlib.pyplot as plt
import numpy as np

plt.ion()

x = np.arange(0,512)
theta = (np.pi/512 )*(x-256)  # angle in rad

#fig2 = plt.figure()
#ax2 = fig2.add_axes([0.1,0.1,0.8,0.8])
#line, = ax2.plot(theta,skan,lw=2.5)
#ax2.set_xlim(-3,3)
#ax2.set_ylim(-3,3)  # distance range
#plt.show()
plt.show()

skan=robot.ReadLaser()
a=[]
b=[]
for i in range(0,511):
	xx = cos(theta[i])*skan[i]
	a.append(xx)
	yy = sin(theta[i])*skan[i]
	b.append(yy)
fig3 = plt.figure()
ax3 = fig3.add_axes([0.1,0.1,0.8,0.8])
line, = ax3.plot(a,b)
  # distance range

while True:
	skan=robot.ReadLaser()
	aa=[]
	bb=[]
	for i in range(0,511):
		xx = cos(theta[i])*skan[i]
		aa.append(xx)
		yy = sin(theta[i])*skan[i]
		bb.append(yy)
	line.set_xdata(aa)
	line.set_ydata(bb)
	plt.draw()
	plt.pause(0.05)



			
