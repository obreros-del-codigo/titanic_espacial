#!/usr/bin/env python3
#
# n-body.py Solve the n-body problem using Newton
# 
# Copyright (C) 2019  Titanic Espacial
#                      
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


####################################################################################
#### This code was made based on and thanks to Victor de la Luz's code for n-Body###
####################################################################################

import math
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import numpy as np
import scipy.ndimage
import math

G=6.674e-11         #m^3kg^-1s^-2

class Particle:
    
    def __init__(self, p, v, m, dt=1):
        self.p = p #position
        self.v = v #velocity
        self.m = m #mass
        self.dt = dt
        self.trajectory = [p]
        self.time = [0.0]

    def setdt(self,dt):
        self.dt = dt

    def computeR(self,p1):
        r = math.sqrt( (p1[0]-self.p[0])**2 + (p1[1]-self.p[1])**2 + (p1[2]-self.p[2])**2)
        return r

    def computeU(self,p1):
        u=[0,0,0]
        i=0
        for a,b in zip(self.p,p1):
            u[i] = b - a
            i+=1
        return u

    def getPosition(self):
        return self.p

    def getVelocity(self):
        return self.v

    def getKineticEnergy(self):
        k= (1/2)*self.m*(math.sqrt( self.v[0]^2 +self.v[1]^2+self.v[2]^2))
        return k    

    #def integrate(self,dt,p1,m1):
    def computeV(self,B):
        r = self.computeR(B.p)
        u = self.computeU(B.p)


        Vx=(G*B.m*self.dt/(r**3))*u[0]
        Vy=(G*B.m*self.dt/(r**3))*u[1]
        Vz=(G*B.m*self.dt/(r**3))*u[2]
        #print(u)
        #print(r)
        #print((G*B.m/(r**3))*u[0],(G*B.m/(r**3))*u[1],(G*B.m/(r**3))*u[2])         
        return [Vx,Vy,Vz]


    #def integrate(self,dt,p1,m1):
    def updateV(self,w):
        self.v[0] += w[0]
        self.v[1] += w[1]
        self.v[2] += w[2]
        
    #def integrate(self,dt,p1,m1):
    def updatePosition(self,time,save):        
        self.p = [self.p[0]+ (self.v[0]) *dt,self.p[1]+ (self.v[1])*dt,self.p[2]+ (self.v[2])*dt]
        if save:
            self.time.append(time)
            self.trajectory.append(self.p)


    def getTrajectory(self):
        return self.time, self.trajectory
        
class Potential:
    
    def __init__(self, system, dt):
        self.system = system #set of Particles
        self.dt = dt #how often we measure changes

    def integrate(self,time,save):

        for particle in self.system:
            for other in self.system:
                if other != particle:
                    velocity = particle.computeV(other)
                    particle.updateV(velocity)
        for particle in self.system:
            particle.updatePosition(time,save)

        return self.system

lenTime=3600.0*24*10  #sec
dt=1      #sec  
  
def test_rocket(grados,velocidad):
	print("Grados:",grados,"Velocidad inicial:", velocidad,"m/s")	
	
	compx=velocidad*math.cos(grados*math.pi/180)
	compy=velocidad*math.sin(grados*math.pi/180)
	print("Velocidad en x:",compx,"Velocidad en y:",compy)
	earth = Particle([0,0,0], [0, 0, 0], 6e24,dt)   #position in meters, velocity in meters/s, mass in kg dt in seconds
	satelite = Particle([0,6371002,0],[compx,compy,0],75e4,dt)



	particles = [earth,satelite]

	n_steps = int(lenTime/dt)
	twoBody = Potential(particles,dt)

	x=[]
	y=[]


	skip=0
	save=False
	for t in range(1,n_steps):
		if skip == 100: #save every 1000 iterations
		    skip=0
		    save=True
		system = twoBody.integrate(float(t)*dt,save)
		save=False
		skip += 1

	fig = plt.figure()

	ax = fig.add_subplot(111, projection='3d')
	ax.set_xlim3d(-5e7, 5e7)
	ax.set_ylim3d(-5e7,5e7)
	ax.set_zlim3d(-5e7,5e7)


	i=0
	c=['g']


	
	time, trajectory = particles[1].getTrajectory()
	for x,y in enumerate(trajectory):
		if np.linalg.norm(y)<6371000:
			print("El cohete chocó")
			plt.close()
			return 1

		ax.scatter(y[0], y[1], y[2], marker='o',c=c[i])
	i=i+1



	#add a sphere for earth#
	u = np.linspace(0, 2 * np.pi, 13)
	v = np.linspace(0, np.pi, 7)

	x = 6371000 * np.outer(np.cos(u), np.sin(v))
	y = 6371000 * np.outer(np.sin(u), np.sin(v))
	z = 6371000 * np.outer(np.ones(np.size(u)), np.cos(v))


	xdata = scipy.ndimage.zoom(x, 3)
	ydata = scipy.ndimage.zoom(y, 3)
	zdata = scipy.ndimage.zoom(z, 3)

	ax.plot_surface(xdata, ydata, zdata, rstride=2, cstride=2, color='b', shade=0)

	print("Mision Exitosa!")
	plt.show()

	return 0


velocidad=8000  #Aquí se edita la velocidad inicial del barrido
while velocidad<=11500:
	for grados in range(0,90,10):  # Aquí se especifica desde que grado hasta que grado se quiere iterar y con saltos de cuántos grados
		x=test_rocket(grados,velocidad)
		#if x==1:    # esto es para detener el barrido si falla la mision
		#	break
		#if x==0:    # esto es para detener el barrido si es exitosa la mision
		#	break
	velocidad+=500 # Aquí se cambia el cambio de velocidad por iteración

