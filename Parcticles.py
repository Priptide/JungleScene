from math import sqrt
from random import randint, random, uniform
import time
import numpy as np
# imports all openGL functions
from OpenGL.GL import *
from BaseModel import DrawModelFromMesh
from material import Material
from matutils import *
from perlin_noise import PerlinNoise

from mesh import Mesh
from shaders import ParticleShader
from sphereModel import Sphere
from texture import Texture

class Particle(DrawModelFromMesh):
	def __init__(self, scene, position=np.array([0,0,0]), velocity=np.array([0,0,0]), longevity=0,rotation=np.array([0,0,0]), scale=1):
		self.position=position
		self.velocity=velocity
		self.lifetime = 0
		self.longevity = longevity
		self.rotation = rotation
		self.scale = scale
		self.time = time.time()
		DrawModelFromMesh.__init__(self, scene=scene, M=poseMatrix(position=self.position, orientation=45), mesh=Sphere(nvert=7, nhoriz=7), shader=ParticleShader())

	def update(self):
		diff = time.time() - self.time
		self.time = time.time()
		self.position = self.position + (self.velocity * diff)
		pos = poseMatrix(self.position)
		rotation = np.matmul(rotationMatrixX(self.rotation[0]), rotationMatrixY(self.rotation[1]), rotationMatrixZ(self.rotation[2]))
		self.M = np.matmul(pos, rotation)
		self.lifetime += diff
		if(self.lifetime < self.longevity):
			self.draw()
			return True
		return False
		

# class ParticleModel(Mesh):
#     '''
#     A model for drawing base terrain.
#     '''
#     def __init__(self, width, height, depth=2, material=Material(Ka=[0.5,0.5,0.5], Kd=[0.6,0.6,0.9], Ks=[1.,1.,0.9], Ns=15.0)):
#         n = width*height
#         vertices = np.zeros((n, 3), 'f')
#         vertex_colors = np.zeros((n, 3), 'f')
#         textureCoords = np.zeros((n, 2), 'f')

#         for i in range(height):
#         	for j in range(width):
# 				v = (i*height)+j
# 				vertices[v, 0] = i
# 				vertices[v, 1] = j
# 				vertices[v, 2] = 0
# 				vertex_colors[v, 0] = float(i) / float(width)
# 				vertex_colors[v, 1] = float(j) / float(height)
# 				textureCoords[v, 1] = (float(i) / float(width))
# 				textureCoords[v, 0] = (float(j) / float(height))
        
        

#     	nfaces = 2*(width-1)*(height-1)
#         indices = np.zeros((nfaces, 3), dtype=np.uint32)
#         k = 0

#         for i in range(height-1):
#             if(i%2 == 0):
#                 for j in range(width-1):
#                     indices[k, 2] = (i*width)+j
#                     indices[k, 1] = ((i+1)*width)+j
#                     indices[k, 0] = (i*width)+j+1
#                     k+=1
#                     indices[k, 0] = (i*width)+j+1
#                     indices[k, 1] = ((i+1)*width)+j+1
#                     indices[k, 2] = ((i+1)*width)+j
#                     k+=1
#             else:
#                 for j in range(width-1, 0, -1):
#                     indices[k, 0] = (i*width)+j
#                     indices[k, 1] = ((i+1)*width)+j
#                     indices[k, 2] = (i*width)+j-1
#                     k+=1
#                     indices[k, 2] = (i*width)+j-1
#                     indices[k, 1] = ((i+1)*width)+j-1
#                     indices[k, 0] = ((i+1)*width)+j
#                     k+=1

#         Mesh.__init__(self,
#                       vertices=vertices,
#                       faces=indices,
#                       textureCoords=textureCoords,
#                       material=material
#                       )

class ParticleRenderer():
	def __init__(self, scene, count=10, origin=np.array([0,0,0]), max_x=1, min_x=0, max_z=1, min_z=0):
		self.particles = []
		self.origin = origin
		self.max_x = max_x
		self.min_x = min_x
		self.max_z = max_z
		self.min_z = min_z
		for i in range(count):
			longevity = random()
			spawn = np.array([origin[0]+randint(min_x, max_x), origin[1] ,origin[2]+randint(min_z, max_z)])
			self.particles.append(Particle(scene=scene, position=spawn, velocity=np.array([0,6,0]), longevity=longevity*8))
	
	def update(self, scene):
		for particle in self.particles:
			if(not particle.update()):
				print("Deletion")
				self.particles.remove(particle)
				longevity = random()
				spawn = np.array([self.origin[0]+randint(self.min_x, self.max_x), self.origin[1] ,self.origin[2]+randint(self.min_z, self.max_z)])
				self.particles.append(Particle(scene=scene, position=spawn, velocity=np.array([0,6,0]), longevity=longevity*8))
