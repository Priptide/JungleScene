from math import sqrt
from random import random
import numpy as np
# imports all openGL functions
from OpenGL.GL import *
from material import Material
from matutils import *

from mesh import Mesh
from texture import Texture

class Floor(Mesh):
    '''
    A model for drawing the scenes floor.
    '''
    def __init__(self, width, height, material=Material(Ka=[0.5,0.5,0.5], Kd=[0.6,0.6,0.9], Ks=[1.,1.,0.9], Ns=15.0), textures=None):

        #Define the number of vertices
        n = width*height

        #Create a vertice, vertex and texture array
        vertices = np.zeros((n, 3), 'f')
        vertex_colors = np.zeros((n, 3), 'f')
        textureCoords = np.zeros((n, 2), 'f')
        
        #Define the water width and max depth
        water = 8
        water_depth = -60

        #Loop through each vertice
        for i in range(height):
            for j in range(width):

                #Get the vertice number and give the x and z the current position
                v = (i*height)+j

                #Times the x and z by a scalar to make the poly count lower
                vertices[v, 0] = j*10
                vertices[v, 2] = i*10

                #Calculate the distance from the center of the plane
                dist = sqrt(pow((width/2-j),2) + pow((height/2-i),2))

                # Make the y the depth of the water if we are in the radius of water
                if(dist < water):
                    vertices[v, 1] = water_depth
                else:
                    vertices[v, 1] = 0
                
                #Update the vertex colors and texture cords, times by a constant for tiling
                vertex_colors[v, 0] = float(i) / float(width)
                vertex_colors[v, 1] = float(j) / float(height)
                textureCoords[v, 1] = (float(i) / float(width))*4
                textureCoords[v, 0] = (float(j) / float(height))*4
        
        
        #Create an array for the indices
        nfaces = 2*(width-1)*(height-1)
        indices = np.zeros((nfaces, 3), dtype=np.uint32)
        k = 0

        #Map odd and even indices in different directions
        for i in range(height-1):
            if(i%2 == 0):
                for j in range(width-1):
                    indices[k, 2] = (i*width)+j
                    indices[k, 1] = ((i+1)*width)+j
                    indices[k, 0] = (i*width)+j+1
                    k+=1
                    indices[k, 0] = (i*width)+j+1
                    indices[k, 1] = ((i+1)*width)+j+1
                    indices[k, 2] = ((i+1)*width)+j
                    k+=1
            else:
                for j in range(width-1, 0, -1):
                    indices[k, 0] = (i*width)+j
                    indices[k, 1] = ((i+1)*width)+j
                    indices[k, 2] = (i*width)+j-1
                    k+=1
                    indices[k, 2] = (i*width)+j-1
                    indices[k, 1] = ((i+1)*width)+j-1
                    indices[k, 0] = ((i+1)*width)+j
                    k+=1

        Mesh.__init__(self,
                      vertices=vertices,
                      faces=indices,
                      textureCoords=textureCoords,
                      material=material
                      )

        #If we provide a texture array then place it on the image
        if textures is None or len(textures) == 0:
            self.textures.append(Texture('StyleGrass.jpg'))
        else:
            self.textures = textures