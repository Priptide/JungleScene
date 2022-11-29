# pygame is just used to create a window with the operating system on which to draw.
import pygame

# imports all openGL functions
from OpenGL.GL import *
from OpenGL.GLU import *

# we will use numpy to store data in arrays
import numpy as np

# import a bunch of useful matrix functions (for translation, scaling etc)
from matutils import *


class Camera:
    '''
    Base class for handling the camera.
    '''


    def __init__(self, size):
        self.V = np.identity(4)
        self.phi = 0.
        self.psi = 276
        self.distance = -200.
        self.center = [0.,0.,0.]
        self.update()
        self.x = (self.V[0][0] * self.V[0][3]) + (self.V[0][1] * self.V[1][3])+ (self.V[0][2] * self.V[2][3])
        self.y = (self.V[1][0] * self.V[0][3]) + (self.V[1][1] * self.V[1][3])+ (self.V[1][2] * self.V[2][3])
        self.z = (self.V[2][0] * self.V[2][3]) + (self.V[2][1] * self.V[2][3])+ (self.V[2][2] * self.V[2][3])

    def update(self):
        # we change the origin of the coordinate system
        D = translationMatrix(self.center)
        
        # we rotate around both X and Y axes by the set angles
        R = np.matmul(rotationMatrixX(self.psi), rotationMatrixY(self.phi))

        # we move the camera away from the origin, looking back.
        T = translationMatrix([0., 0., self.distance])
        # # note the order of the matrices. It is important!
        self.V = np.matmul(np.matmul(T, R), D)

        self.x = (self.V[0][0] * self.V[0][3]) + (self.V[0][1] * self.V[1][3])+ (self.V[0][2] * self.V[2][3])
        self.y = (self.V[1][0] * self.V[0][3]) + (self.V[1][1] * self.V[1][3])+ (self.V[1][2] * self.V[2][3])
        self.z = (self.V[2][0] * self.V[2][3]) + (self.V[2][1] * self.V[2][3])+ (self.V[2][2] * self.V[2][3])
