from math import sqrt
from random import random
import numpy as np
# imports all openGL functions
from OpenGL.GL import *
from material import Material
from matutils import *
from perlin_noise import PerlinNoise

from mesh import Mesh
from texture import Texture

class Terrain(Mesh):
    '''
    A model for drawing base terrain.
    '''
    def __init__(self, width, height, material=Material(Ka=[0.5,0.5,0.5], Kd=[0.6,0.6,0.9], Ks=[1.,1.,0.9], Ns=15.0)):
        n = width*height
        vertices = np.zeros((n, 3), 'f')
        vertex_colors = np.zeros((n, 3), 'f')
        textureCoords = np.zeros((n, 2), 'f')
        slope = 5
        flat = 20
        water = 5
        water_depth = -10
        for i in range(height):
            for j in range(width):
                v = (i*height)+j
                vertices[v, 0] = j*10
                #Calculate distance from centre using pythag
                dist = sqrt(pow((width/2-j),2) + pow((height/2-i),2))
                if(dist > flat):
                    vertices[v, 1] = (dist-flat) * slope
                elif(dist < water):
                    vertices[v, 1] = water_depth
                else:
                    vertices[v, 1] = 0
                # vertices[v, 1] = 0
                vertices[v, 2] = i*10
                vertex_colors[v, 0] = float(i) / float(width)
                vertex_colors[v, 1] = float(j) / float(height)
                textureCoords[v, 1] = (float(i) / float(width))*8
                textureCoords[v, 0] = (float(j) / float(height))*8
        
        

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

        # # last triangle at the top
        # indices[k, :] = [0, 1, height]

        # last triangle at the bottom
        # indices[k + 1, :] = [lastrow + 1, n - 1, n-2]

        # for j in range(height-1):
        #     if(j%2 == 0):
        #         for i in range(width):
        #             indices.append(j+i*width)
        #             indices.append(j+(i+1)*width)
        #     else:
        #         for i in range(width-1, 0, -1):
        #             indices.append(j+(i+1)*width)
        #             indices.append((j-1)+i*width)
                    
        # print(indices)
        # if(height%2==1 and height > 2):
        #     indices.append((height-1)*width)
        # indices = np.array(indices, dtype=np.uint32)
        # np.savetxt("./test.txt", indices, '%f')
        Mesh.__init__(self,
                      vertices=vertices,
                      faces=indices,
                      textureCoords=textureCoords,
                      material=material
                      )

        self.textures.append(Texture('StyleGrass.jpg'))

    # def draw(self, Mp):
    #     '''
    #     Draws the model using OpenGL functions
    #     :return:
    #     '''
    #     if self.visible:

    #         if self.mesh.vertices is None:
    #             print('(W) Warning in {}.draw(): No vertex array!'.format(self.__class__.__name__))

    #         # bind the Vertex Array Object so that all buffers are bound correctly and following operations affect them
    #         glBindVertexArray(self.vao)

    #         # setup the shader program and provide it the Model, View and Projection matrices to use
    #         # for rendering this model
    #         self.shader.bind(
    #             model=self,
    #             M=np.matmul(Mp, self.M)
    #         )

    #         #print('---> object {} rendered using shader {}'.format(self.name, self.shader.name))

    #         # bind all textures. Note that your shader needs to handle each one with a sampler object.
    #         for unit, tex in enumerate(self.mesh.textures):
    #             glActiveTexture(GL_TEXTURE0 + unit)
    #             tex.bind()

    #         # check whether the data is stored as vertex array or index array
    #         if self.mesh.faces is not None:
    #             # draw the data in the buffer using the index array
    #             indices_count = (self.width*self.height) + (self.width-1)*(self.height-1)
    #             glDrawElements(GL_TRIANGLE_STRIP, indices_count, GL_UNSIGNED_INT, ctypes.c_void_p(0))
    #         else:
    #             # draw the data in the buffer using the vertex array ordering only.
    #             glDrawArrays(self.primitive, 0, self.mesh.vertices.shape[0])

    #         # unbind the shader to avoid side effects
    #         glBindVertexArray(0)