from math import sqrt
import numpy as np
# imports all openGL functions
from OpenGL.GL import *
from material import Material
from matutils import *

from mesh import Mesh
from texture import Texture

class Pond(Mesh):
    '''
    A model for drawing the pond base.
    '''
    def __init__(self, width, height, material=Material(Ka=[0.5,0.5,0.5], Kd=[0.6,0.6,0.9], Ks=[1.,1.,0.9], Ns=15.0), textures=None):

        #Create vertice, vertex and texture arrays
        n = width*height
        vertices = np.zeros((n, 3), 'f')
        vertex_colors = np.zeros((n, 3), 'f')
        textureCoords = np.zeros((n, 2), 'f')

        #Define our slope and water depth
        slope = 6
        water_depth = -50
        for i in range(height):
            for j in range(width):

                #Calculate the current vertex number
                v = (i*height)+j

                #Times the x and z by a scalar to make the poly count lower for large planes
                vertices[v, 0] = j*10
                vertices[v, 2] = i*10

                #Check the distane and calculate the y value on that clamping to max of zero
                dist = sqrt(pow((width/2-j),2) + pow((height/2-i),2))
                vertices[v, 1] = min(water_depth + (dist * slope),0)
                
                #Update the vertex colors and texture cords, times by a constant for tiling
                vertex_colors[v, 0] = float(i) / float(width)
                vertex_colors[v, 1] = float(j) / float(height)
                textureCoords[v, 1] = (float(i) / float(width))*4
                textureCoords[v, 0] = (float(j) / float(height))*4
        
        
        #Create array for indices
        nfaces = 2*(width-1)*(height-1)
        indices = np.zeros((nfaces, 3), dtype=np.uint32)
        k = 0

        #Map indices too array
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

        #If we provide a texture array use that otherwise a single texture
        if textures is None or len(textures) == 0:
            self.textures.append(Texture('Sand.jpg'))
        else:
            self.textures = textures