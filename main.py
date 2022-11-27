
# import the scene class
from random import randint
from BaseModel import DrawModelFromMesh
from FloorModel import Floor
from ShadowMapping import *
from TerrainModel import Terrain
from blender import load_obj_file
from lightSource import LightSource
from scene import Scene
from OpenGL.GL import *
from matutils import *
import pygame
from shaders import *
from environmentMapping import *
from skyBox import SkyBox
from sphereModel import Sphere

class JungleScene(Scene):
    def __init__(self):
        self.width = 100
        self.height = 100
        scale = 10
        Scene.__init__(self)

        self.light = LightSource(self, position=[1000, 1000, -1000])

        self.shaders='phong'

        self.shadows = ShadowMap(light=self.light)
        self.show_shadow_map = ShowTexture(self, self.shadows)
        self.skybox = SkyBox(scene=self)
        self.terrain = DrawModelFromMesh(scene=self, M=poseMatrix(position=[-(self.width/2)*10, 0, -(self.height/2)*10]), mesh=Terrain(width=self.width, height=self.height), shader=PhongShader())
        self.floor = DrawModelFromMesh(scene=self, M=poseMatrix(position=[-200, 0.1, -200]), mesh=Floor(width=40, height=40), shader=PhongShader())
        self.terrain_items = []

        tree = load_obj_file("./models/palm.obj")
        self.tree = [(DrawModelFromMesh(scene=self, M=poseMatrix(position=[0, 10, 0],scale=20), mesh=mesh, shader=PhongShader())) for mesh in tree]
        #generate all terrain items
        # self.generate_jungle()

    def draw_shadow_map(self):
        # first we need to clear the scene, we also clear the depth buffer to handle occlusions
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.terrain.draw()
        # also all models from the table
        for model in self.terrain_items:
            model.draw()

        # # and for the box
        # for model in self.box:
        #     model.draw()
        for model in self.tree:
            model.draw()

    def generate_jungle(self, num_items = 10):

        locations = []
        #Iterate till all items are placed
        while num_items > 0:
            #Pick random coordinate between 1 row up and terrain size 1 row down as we don't want an edge
            vertex = randint(self.height+1, len(self.terrain.mesh.vertices)-self.height)

            if vertex % self.height == 0 or (vertex+1) % self.height == 0:
                continue
            #Check no item is placed here
            if vertex not in locations:
                locations.append(vertex)
                pos = [self.terrain.mesh.vertices[vertex][0]-(self.width/2)*10, self.terrain.mesh.vertices[vertex][1], self.terrain.mesh.vertices[vertex][2]-(self.height/2)*10]
                local_model = DrawModelFromMesh(scene=self, M=poseMatrix(position=pos, scale=10), mesh=Sphere(material=Material(Ka=[10,10,10])), shader=FlatShader())
                self.terrain_items.append(local_model)
                num_items-=1


    def draw(self, framebuffer=False):
        '''
        Draw all models in the scene
        :return: None
        '''

        # first we need to clear the scene, we also clear the depth buffer to handle occlusions
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # when using a framebuffer, we do not update the camera to allow for arbitrary viewpoint.
        if not framebuffer:
            self.camera.update()

        self.skybox.draw()
            
        self.shadows.render(self)

        # when rendering the framebuffer we ignore the reflective object
        if not framebuffer:
            # self.environment.update(self)
            self.terrain.draw()
            
            self.floor.draw()
            # for obj in self.tree:
            #     obj.draw()
        # then we loop over all models in the terrain list and draw them
        for model in self.terrain_items:
            model.draw()

        # once we are done drawing, we display the scene
        # Note that here we use double buffering to avoid artefacts:
        # we draw on a different buffer than the one we display,
        # and flip the two buffers once we are done drawing.
        if not framebuffer:
            pygame.display.flip()

if __name__ == '__main__':

    scene = JungleScene()

    scene.run()