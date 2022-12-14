# pygame is just used to create a window with the operating system on which to draw.
import pygame

# imports all openGL functions
from OpenGL.GL import *

# we will use numpy to store data in arrays
import numpy as np
from lightSource import LightSource

# import the camera class
from camera import Camera

# and we import a bunch of helper functions
from matutils import *

class Scene:
    '''
    This is the main class for adrawing an OpenGL scene using the PyGame library
    '''
    def __init__(self, width=800, height=600):
        '''
        Initialises the scene
        '''

        self.window_size = (width, height)

        # by default, wireframe mode is off
        self.wireframe = False

        # the first two lines initialise the pygame window. You could use another library for this,
        # for example GLut or Qt
        pygame.init()
        screen = pygame.display.set_mode(self.window_size, pygame.OPENGL | pygame.DOUBLEBUF, 24)

        # Here we start initialising the window from the OpenGL side
        glViewport(0, 0, self.window_size[0], self.window_size[1])

        # this selects the background color
        glClearColor(0.7, 0.7, 1.0, 1.0)

        # enable the vertex array capability
        glEnableClientState(GL_VERTEX_ARRAY)

        #enable texture depth blending
        glEnable( GL_BLEND )
        glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )

        # enable depth test for clean output (see lecture on clipping & visibility for an explanation
        glEnable(GL_DEPTH_TEST)

        # initialise the projective transform
        near=1.5
        far=5000
        left=-1.0
        right=1.0
        top=-1.0
        bottom=1.0

        # to start with, we use an orthographic projection; change this.
        self.P = frustumMatrix(left,right,top,bottom,near,far)

        # initialises the camera object
        self.camera = Camera(self.window_size)

        #initalise a light source
        self.light = LightSource(self, position=[5., 5., 5.])

        self.mode = 1

        # This class will maintain a list of models to draw in the scene,
        # we will initalise it to empty
        self.models = []

    def add_model(self,model):
        '''
        This method just adds a model to the scene.
        :param model: The model object to add to the scene
        :return: None
        '''
        self.models.append(model)

    def add_models_list(self,models_list):
        '''
        This method just adds a model to the scene.
        :param model: The model object to add to the scene
        :return: None
        '''
        self.models.extend(models_list)

    def draw(self, framebuffer=False):
        '''
        Draw all models in the scene
        :return: None
        '''

        # first we need to clear the scene, we also clear the depth buffer to handle occlusions
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        #update camera position
        self.camera.update()

        # then we loop over all models in the list and draw them
        for model in self.models:
            model.draw(Mp=poseMatrix())

        # once we are done drawing, we display the scene
        # Note that here we use double buffering to avoid artefacts:
        # we draw on a different buffer than the one we display,
        # and flip the two buffers once we are done drawing.
        pygame.display.flip()


    def keyboard(self, event):
        if event.key == pygame.K_q:
            self.running = False
        elif event.key == pygame.K_a:
            self.camera.center[0] -= 1
            print(self.camera.V)
        elif event.key == pygame.K_d:
            self.camera.center[0] += 1
            print(self.camera.V)
        elif event.key == pygame.K_w:
            self.camera.center[1] -= 1
            print(self.camera.V)
        elif event.key == pygame.K_s:
            self.camera.center[1] += 1
            print(self.camera.V)
        # flag to switch wireframe rendering
        elif event.key == pygame.K_0:
            if self.wireframe:
                print('--> Rendering using colour wireframe')
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
                self.wireframe = False
            else:
                print('--> Rendering using colour fill')
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
                self.wireframe = True
        
    def pygameEvents(self):
        # check whether the window has been closed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # keyboard events
            elif event.type == pygame.KEYDOWN:
                self.keyboard(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.camera.distance += 10
                elif event.button == 5:
                    self.camera.distance -= 10

            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    if self.mouse_mvt is not None:
                        self.mouse_mvt = pygame.mouse.get_rel()
                        self.camera.center[0] -= (float(self.mouse_mvt[0]) / self.window_size[0]) * 30
                        self.camera.center[1] += (float(self.mouse_mvt[1]) / self.window_size[1]) * 30
                    else:
                        self.mouse_mvt = pygame.mouse.get_rel()

                elif pygame.mouse.get_pressed()[2]:
                    if self.mouse_mvt is not None:
                        self.mouse_mvt = pygame.mouse.get_rel()
                        self.camera.phi -= (float(self.mouse_mvt[0]) / self.window_size[0])
                        self.camera.psi -= (float(self.mouse_mvt[1]) / self.window_size[1])
                    else:
                        self.mouse_mvt = pygame.mouse.get_rel()
                else:
                    self.mouse_mvt = None

    def run(self):
        '''
        Draws the scene in a loop until exit.
        '''

        # We have a classic program loop
        self.running = True
        while self.running:

            self.pygameEvents()

            # otherwise, continue drawing
            self.draw()
