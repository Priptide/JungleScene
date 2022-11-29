from math import sqrt
from random import randint, random
import time
import numpy as np
# imports all openGL functions
from OpenGL.GL import *
from BaseModel import DrawModelFromMesh
from matutils import *
from shaders import ParticleShader
from sphereModel import Sphere

class Particle(DrawModelFromMesh):
	'''
	Create a model for a single particles
	'''
	def __init__(self, scene, position=np.array([0,0,0]), velocity=np.array([0,0,0]), longevity=0,rotation=np.array([0,0,0]), scale=1):

		#Save our particles core information
		self.position=position
		self.velocity=velocity
		self.lifetime = 0
		self.longevity = longevity
		self.rotation = rotation
		self.scale = scale

		#Save the creation time for our particle
		self.time = time.time()

		DrawModelFromMesh.__init__(self, scene=scene, M=poseMatrix(position=self.position, orientation=45), mesh=Sphere(nvert=7, nhoriz=7), shader=ParticleShader())

	def update(self, plane):

		#Work out the time passed since last updated
		diff = time.time() - self.time

		#Update our time last updated
		self.time = time.time()

		#Update our position using the velocity of the particle
		self.position = self.position + (self.velocity * diff)

		#Update the position too a matrix
		pos = poseMatrix(self.position)
		
		#Update the roatation if we are moving it around
		rotation = np.matmul(rotationMatrixX(self.rotation[0]), rotationMatrixY(self.rotation[1]), rotationMatrixZ(self.rotation[2]))

		#Calculate and update the final position
		self.M = np.matmul(pos, rotation)

		#Update our current lifetime
		self.lifetime += diff

		#Check and return if the particle is still alive
		if(self.lifetime < self.longevity):
			self.draw(plane=plane)
			return True
		return False

class ParticleRenderer():
	'''
	Create a particle emitter used to render a number of particles
	'''
	def __init__(self, scene, count=10, origin=np.array([0,0,0]), max_x=1, min_x=0, max_z=1, min_z=0):
		#Create an empty list of particles and register an origin
		self.particles = []
		self.origin = origin

		#Define the max and min spread in x and z directions
		self.max_x = max_x
		self.min_x = min_x
		self.max_z = max_z
		self.min_z = min_z

		#Create a number of particle equal to the count
		for i in range(count):
			#Generate a random longevity and velocity value
			longevity = random()
			velocity = randint(3,8)

			#Generate a random spawn position
			spawn = np.array([origin[0]+randint(min_x, max_x), origin[1] ,origin[2]+randint(min_z, max_z)])

			#Create a new particle and add it too the scene
			particle = Particle(scene=scene, position=spawn, velocity=np.array([0,velocity,0]), longevity=longevity*8)
			self.particles.append(particle)
	
	def update(self, scene, plane=np.array([0, -1, 0, 10000], 'f')):
		for particle in self.particles:
			#Update each particle checking if it is still alive
			if(not particle.update(plane=plane)):
				#If not remove the particle
				self.particles.remove(particle)

				#Generate a random longevity and velocity value
				longevity = random()
				velocity = randint(3,8)

				#Generate a random spawn location
				spawn = np.array([self.origin[0]+randint(self.min_x, self.max_x), self.origin[1] ,self.origin[2]+randint(self.min_z, self.max_z)])

				#Create a new particle, render it and add it too the scene
				new_particle = Particle(scene=scene, position=spawn, velocity=np.array([0,velocity,0]), longevity=longevity*8)
				new_particle.update(plane=plane)
				self.particles.append(new_particle)
