from math import sqrt
import numpy as np
# imports all openGL functions
from OpenGL.GL import *
from material import Material
from matutils import *

from mesh import Mesh
from texture import Texture

class Cover(Mesh):
    '''
    A model for drawing base terrain.
    '''
    def __init__(self, width, height, material=Material(Ka=[0.5,0.5,0.5], Kd=[0.6,0.6,0.9], Ks=[1.,1.,0.9], Ns=15.0)):
        n = width*height
        vertices = np.zeros((n, 3), 'f')
        vertex_colors = np.zeros((n, 3), 'f')
        textureCoords = np.zeros((n, 2), 'f')
        slope = 7
        flat = 10
        max_depth = -70
        for i in range(height):
            for j in range(width):
                v = (i*height)+j
                vertices[v, 0] = j*10
                dist = sqrt(pow((width/2-j),2) + pow((height/2-i),2))
                if(dist < flat):
                    vertices[v, 1] = max_depth
                else:
                    vertices[v, 1] = min(0, max_depth +((dist-flat)*slope))
                vertices[v, 2] = i*10
                vertex_colors[v, 0] = float(i) / float(width)
                vertex_colors[v, 1] = float(j) / float(height)
                textureCoords[v, 1] = (float(i) / float(width))*4
                textureCoords[v, 0] = (float(j) / float(height))*4
        
        

        nfaces = 2*(width-1)*(height-1)
        indices = np.zeros((nfaces, 3), dtype=np.uint32)
        k = 0

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

        self.textures.append(Texture('StoneFloor.jpg'))